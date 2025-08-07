# KakaoTalk Style Chatbot

> 카카오톡 대화 스타일을 학습한 KoGPT2 기반 챗봇

이 프로젝트는 실제 카카오톡 대화 데이터를 기반으로 학습된 KoGPT2 챗봇입니다. 사용자 말투와 응답 스타일을 학습하여 자연스럽고 캐주얼한 대화를 구현합니다.

---

## 📌 주요 기능

- ✅ 카카오톡 `.txt` 또는 `.csv` 대화 파일 전처리
- ✅ 사용자와 챗봇 간 대화 데이터를 기반으로 KoGPT2 fine-tuning
- ✅ 챗봇 응답 생성 API (`/api/chat`)
- ✅ 파일 업로드 API (`/api/v1/files/upload`)
- ✅ Spring Boot + PyTorch 기반 서버 연동

---

## 📁 프로젝트 구조



⚙️ 모델 관련
사용 모델: skt/kogpt2-base-v2

입력 형식: <me>사용자 메시지<sent><you>응답</s>

토크나이저: PreTrainedTokenizerFast 사용

KoGPT2 학습 시 max_len=50, padding/attention mask 적용
