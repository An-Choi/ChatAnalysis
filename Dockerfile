FROM python:3.11-slim

WORKDIR /app

# 전체 프로젝트 복사
COPY . .

# Python 패키지 설치
COPY backend/chatbot/src/main/java/com/anchoi/chatbot/chatbot_model/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "backend.chatbot.src.main.java.com.anchoi.chatbot.chatbot_model.eval:app", "--host", "0.0.0.0", "--port", "8000"]
