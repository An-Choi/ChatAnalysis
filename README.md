# ChatAnalysis  
AI 기반 카카오톡 대화 말투 모방 및 감정 분석 챗봇 프로젝트

---

## 🎯 프로젝트 개요  
ChatAnalysis는 카카오톡 대화 데이터를 기반으로  
사용자의 **말투 스타일을 모방**하고 **감정을 분석**하여 응답하는 AI 챗봇을 개발하는 프로젝트입니다.

- 카카오톡 txt/csv 대화 파일 전처리  
- 사용자별 말투(어투, 문체, 이모티콘 패턴) 학습  
- 감정 분석 + 스타일 모방 기반 응답 생성  
- Spring Boot 백엔드와 Python AI 모델 연동  
- 웹 서비스로 사용 가능하도록 설계

---

## 🧩 주요 기능  
- 카카오톡 대화 데이터 업로드 API (`/api/v1/files/upload`)
- 스타일 모방/감정 분석 챗봇 API (`/api/chat`)
- KoGPT2 기반 말투 생성 모델
- PyTorch 기반 감정 분석 모델 결합
- Docker 기반 전체 환경 구성

---

## 🏗 프로젝트 구조  
```bash
ChatAnalysis/
├── backend/ #Spring Boot 백엔드
├── chatbot_model/ #AI 모델(Fine-tuning, 추론)
├── frontend/ # 웹 프론트엔드
└── uploads/ # 업로드된 카카오톡 대화 파일
```

## ⚙️ 기술 스택  
### 🔹 AI / ML 
- Python, PyTorch  
- HuggingFace Transformers  
- KoGPT2 Fine-tuning  
- JSON/CSV 데이터 전처리  

### 🔹 Backend
- Java Spring Boot  
- REST API  
- Python 모델 스크립트 연동  
- Docker Compose

---

## 🚀 실행 방법  
### 1. 레포지토리 클론
```bash
git clone https://github.com/An-Choi/ChatAnalysis.git
cd ChatAnalysis
```

### 2. Docker Compose 실행
```bash
docker-compose up --build
```
### 3. 서비스 접속

API 서버: http://localhost:8080

프론트엔드: http://localhost:3000

## 🧪 모델 학습 및 추론
### 1) 데이터 전처리

카카오톡 txt/csv 파일을
```bash
chatbot_model/preprocess.py
```
로 전처리 → JSON/CSV 형태의 학습 데이터 생성

### 2) KoGPT2 학습
```bash
python train.py
```

### 3) 모델 추론

백엔드(Spring Boot) → Python 스크립트 호출
→ Fine-tuned 모델로 응답 생성


# 👥 Contributors
안승환:	AI 모델 개발 · 데이터 전처리 · KoGPT2 Fine-tuning

최병주:	Backend 개발(Spring Boot) · API 구축 · 서비스 연동
