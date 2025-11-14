from fastapi import FastAPI, APIRouter, BackgroundTasks
from pydantic import BaseModel
import os
import re
import pandas as pd
import unicodedata
import sys
import csv
import subprocess

processing_router = APIRouter()


UPLOAD_DIR = "/app/resources/uploads"
SAVE_DIR = "/app/resources/processed"

class ProcessRequest(BaseModel):
    filename: str

##텍스트 파일 전처리
def processing_text_file(txt_path, csv_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 상대방 이름 추출
    first_line = lines[0].strip()
    m = re.match(r"^(.*?) 님과 카카오톡 대화", first_line)
    you_name = m.group(1) if m else None

    dialogues = []
    last_speaker = None
    buffer = ""

    # 1. 전체 대화 파싱
    for line in lines[1:]:  # 첫 줄 제외
        m_line = re.match(r"\[(.*?)\] \[.*?\] (.*)", line.strip())
        if not m_line:
            continue
        speaker, message = m_line.groups()
        current = "<you>" if speaker == you_name else "<me>"

        if last_speaker == current:
            buffer += " " + message
        else:
            if buffer:
                dialogues.append((last_speaker, buffer))
            buffer = message
            last_speaker = current

    if buffer:
        dialogues.append((last_speaker, buffer))

    # 2. 첫 발화가 <you>라면 제거
    if dialogues and dialogues[0][0] == "<you>":
        dialogues.pop(0)

    # 3. conversation 단위 생성
    conversations = []
    temp_me, temp_you = "", ""
    for speaker, msg in dialogues:
        if speaker == "<me>":
            if temp_me and temp_you:
                # 이전 턴 완성하면 저장
                conversations.append(f"<me>{temp_me}<sent><you>{temp_you}<s>")
                temp_me, temp_you = msg, ""
            else:
                temp_me += (" " + msg) if temp_me else msg
        else:  # <you>
            temp_you += (" " + msg) if temp_you else msg

    # 마지막 남은 턴 저장
    if temp_me:
        conversations.append(f"<me>{temp_me}<sent><you>{temp_you if temp_you else '다음대화'}<s>")

    # 4. CSV 저장
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["conversation"])
        for conv in conversations:
            writer.writerow([conv])

    print(f"CSV 저장 완료: {csv_path}")
        


##csv파일 전처리
def processing_csv_file(file_path, csv_path):
    ##파일 읽기
    df = pd.read_csv(file_path)

    ##파일 이름에서 학습 대상 이름 추출
    ##한글 비교 시 유니코드 정규화 통일 후 비교
    filename = os.path.splitext(os.path.basename(file_path))[0]
    filename_nfc = unicodedata.normalize('NFC', filename)
    users = df['User'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
    target = None
    for user in users:
        if user in filename_nfc:
            target = user
            break
    
    dialogues = []
    last_speaker = None
    buffer = ""

    for _, row in df.iterrows():
        speaker = row['User']
        message = str(row['Message']).strip()
        current = "<me>" if speaker == target else "<you>"

        if last_speaker == current:
            buffer += " " + message
        else:
            if buffer:
                dialogues.append((last_speaker, buffer))

            buffer = message
            last_speaker = current

    if buffer:
        dialogues.append((last_speaker, buffer))

    if dialogues and dialogues[0][0] == "<you>":
        dialogues.pop(0)

    conversations = []
    temp_me = ""
    temp_you = ""

    for speaker, msg in dialogues:
        if speaker == "<me>":
            if temp_me and temp_you:
                conversations.append(f"<me>{temp_me}<sent><you>{temp_you}<s>")
                temp_me = msg
                temp_you = ""
            else:
                temp_me += (" " + msg) if temp_me else msg
        else:
            temp_you += (" " + msg) if temp_you else msg

    if temp_me:
        conversations.append(f"<me>{temp_me}<sent><you>{temp_you if temp_you else '다음대화'}<s>")
    
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["conversation"])
        for conv in conversations:
            writer.writerow([conv])

def run_model_training(processed_csv_path: str):
    print("모델 학습 시작")
    model_script_path = os.path.join(os.path.dirname(__file__), "model.py")
    try:
        subprocess.run(
            [sys.executable, model_script_path, "--csv_file_path", processed_csv_path],
            check=True,
            capture_output=True,
            text=True
        )
        print("모델 학습 완료")
    except subprocess.CalledProcessError as e:
        print("모델 학습 중 오류 발생:")
        print(e.stderr)

@processing_router.post("/process")
def process_file(req: ProcessRequest, background_tasks: BackgroundTasks):
    print("process called!") 
    try:
        filename = req.filename
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        print(f"전처리 요청: {file_path}")

        #os.makedirs(SAVE_DIR, exist_ok=True) 
        out_file = os.path.join(SAVE_DIR, 'processed.csv')

        type = os.path.splitext(filename)[1].lower()

        if type == '.txt':
            processing_text_file(file_path, out_file)
        elif type == '.csv':
            processing_csv_file(file_path, out_file)
        else:
            return {"status": "error", "message": "지원하지 않는 파일 형식입니다."}

        background_tasks.add_task(run_model_training, out_file)

        return {"status": "success", "message": "파일 전처리가 완료되었습니다. 모델 학습이 백그라운드에서 진행됩니다.", "output": out_file}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
