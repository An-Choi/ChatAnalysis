.PHONY: all python spring react

#Python FastAPI 서버 실행
python:
	uvicorn backend.chatbot.src.main.java.com.anchoi.chatbot.chatbot_model.eval:app --host 0.0.0.0 --port 8000 &

#Spring Boot 실행
spring:
	cd backend/chatbot && \
	./mvnw spring-boot:run &

#React 실행
react:
	cd frontend && \
	npm start &

#전체 실행
all: python spring react
	@echo "모든 서비스가 실행되었습니다."

stop:
	@pkill -f uvicorn || true
	@pkill -f java || true
	@pkill -f npm || true
	@echo "모든 서비스 중지"