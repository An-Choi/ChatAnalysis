package com.anchoi.chatbot.Controller;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin(origins = "http://localhost:3000")
@RestController
@RequestMapping("/api/chat")
public class ChatbotController {
    
    @PostMapping
    public ChatResponse chat(@RequestBody ChatRequest request) {
        String userMessage = request.getMessage();
        //여기에 챗봇 모델 추가/연동
        String answer = "안녕";
        if (userMessage.contains("ㅋㅋㅋㅋㅋ"))
            answer = "ㅋㅋㅋㅋㅋㅋㅋㅋ";

        return new ChatResponse(answer);
    }

    public static class ChatRequest {
        private String message;

        public ChatRequest() {
        }

        public ChatRequest(String message) {
            this.message = message;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }
    }
    
    public static class ChatResponse {
        private String response;

        public ChatResponse() {
        }

        public ChatResponse(String response) {
            this.response = response;
        }

        public String getResponse() {
            return response;
        }

        public void setResponse(String response) {
            this.response = response;
        }
    }
}
