import os
import csv
import json

UPLOAD_DIR = "uploads"

##텍스트 파일 전처리
def processing_text_file(file_path, proccessed):
    NotImplemented
##csv파일 전처리
def processing_csv_file(file_path, processed):
    ##asdf
    NotImplemented

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