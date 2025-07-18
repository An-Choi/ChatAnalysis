import os
import csv
import json
import re
import pandas as pd
import unicodedata

UPLOAD_DIR = "uploads"

##텍스트 파일 전처리
def processing_text_file(file_path, processed):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    

    #학습하는 대상
    first_line = lines[0]
    train_name = first_line.split('님과 카카오톡 대화')[0].strip()  
    
    #메세지 패턴
    msg_pattern = re.compile(r"\[(.*?)\] \[(오전|오후) (\d{1,2}):(\d{2})\] (.+)")

    #날짜 패턴
    date_pattern = re.compile(r"-+ (\d{4})년 (\d{1,2})월 (\d{1,2})일.*-+")
    
    curr_date = None
    prev_sender = None
    full_msg = ''
    prev_time = None

    for line in lines: 
        line = line.strip()

        #날짜 탐지 및 처리
        match_date = date_pattern.match(line)
        if match_date:
            year = match_date.group(1)
            month = match_date.group(2)
            date = match_date.group(3)
            curr_date = f"{int(year):04d}-{int(month):02d}-{int(date):02d}"
            continue

        
        #메세지 탐지 및 처리
        match_msg = msg_pattern.match(line)
        if match_msg:
            sender = match_msg.group(1)
            am_pm= match_msg.group(2)
            hour = match_msg.group(3)
            sec = match_msg.group(4)
            msg = match_msg.group(5)

            #오전 오후 처리
            hour = int(hour)
            if am_pm == "오후" and hour!=12:
                hour += 12
            elif am_pm == "오전" and hour == 12:
                hour = 0
            time = f"{curr_date} {hour}:{sec}"

            #메세지 누적
            if sender == prev_sender:
                full_msg += '\n' + msg
            else:  
                #보낸사람이 달라져서 메세지 저장
                if prev_sender is not None:
                    processed.append({
                        "sender":prev_sender,
                        "message":full_msg,
                        "time":prev_time,
                        "trainer": train_name == sender
                    })
                #사람 변경
                full_msg = msg
                prev_time = time
                prev_sender = sender

    #마지막 메세지 저장
    if prev_sender and full_msg:
        processed.append({
            "sender": prev_sender,
            "message": full_msg,
            "time": prev_time,
            "trainer": train_name == prev_sender
        })
        


##csv파일 전처리
def processing_csv_file(file_path, processed):
    ##파일 읽기
    df = pd.read_csv(file_path)

    ##초 단위 제거
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M')

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
    
    ##한 사용자가 연속으로 메세지를 보낸 경우 하나의 row로 처리
    ##processed 안에 dictionary 형식으로 저장
    current_user = None
    current_message = ""
    current_date = ""

    for index, row in df.iterrows():
        if current_user is None:
            current_date = row['Date']
            current_user = row['User']
            current_message += row['Message']
        elif current_user != row['User']:
            processed.append({
                "sender": current_user,
                "message": current_message,
                "time": current_date,
                "trainer": current_user == target
            })
            current_date = row['Date']
            current_user = row['User']
            current_message = row['Message']
        else:
            current_message += "\n" + row['Message']

    if current_user is not None:
        processed.append({
                "sender": current_user,
                "message": current_message,
                "time": current_date,
                "trainer": current_user == target
            })

    ##테스트용 프린트
    print(df.head(5))
    print(target)
    print(processed[:3])

##실행 함수
def execute_files(filename):
    file_path = os.path.join(UPLOAD_DIR, filename)
    processed = []

    #파일 없는 경우 (오류 처리)
    if not os.path.isfile(file_path):
        print("파일이 없습니다")
        return
    
    #파일 타입
    type = os.path.splitext(filename)[1].lower()

    ##json 파일로 return
    if type == '.txt':
        processing_text_file(file_path, processed)
    elif type == '.csv':
        processing_csv_file(file_path, processed)
    else:
        print("지원하지 않는 형식입니다.\n txt파일 혹은 csv파일을 업로드 해주세요")

    return processed

#main 함수
if __name__ == "__main__":
    result = []
    for filename in os.listdir(UPLOAD_DIR):
        result = execute_files(filename)
    
    ##json 파일 백엔드 서버로 보내기