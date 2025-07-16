import os
import csv
import json
import pandas as pd
import unicodedata

UPLOAD_DIR = "uploads"

##텍스트 파일 전처리
def processing_text_file(file_path, proccessed):
    NotImplemented
##csv파일 전처리
def processing_csv_file(file_path, processed):
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
    
    ##한 사용자가 연속으로 메세지를 보낸 경우 하나의 row로 처리
    ##비어있는 new_df 생성 후 처리된 row를 추가
    new_df = pd.DataFrame(columns=['Date', 'User', 'Message'])
    current_user = None
    current_message = ""
    current_date = ""

    for index, row in df.iterrows():
        if current_user is None:
            current_date = row['Date']
            current_user = row['User']
            current_message += row['Message']
        elif current_user != row['User']:
            new_row = pd.DataFrame([{
                'Date': current_date,
                'User': current_user,
                'Message': current_message
            }])
            new_df = pd.concat([new_df, new_row], ignore_index=True)
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
        new_row = pd.DataFrame([{
            'Date': current_date,
            'User': current_user,
            'Message': current_message
        }])
        new_df = pd.concat([new_df, new_row], ignore_index=True)

    print(df.head(5))
    print(target)
    print(new_df.head(5))
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