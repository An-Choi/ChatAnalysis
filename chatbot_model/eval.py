import torch
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import os

processing_router1 = APIRouter()

class ChatRequest(BaseModel):
    message: str

ME_TKN = "<me>" #user
YOU_TKN = "<you>" #bot
BOS = "</s>" #begin sentence
EOS = "</s>" #end sentence
MASK = "<mask>"
SENT = "<sent>" #문장 구분
PAD = "<pad>" #패딩

tokenizer = PreTrainedTokenizerFast.from_pretrained(
    "skt/kogpt2-base-v2",
    bos_token=EOS,
    eos_token=EOS,
    unk_token="<unk>",
    pad_token=PAD,
    mask_token=MASK,
)

special_tokens = [ME_TKN, YOU_TKN, SENT]
tokenizer.add_tokens(special_tokens)

# repo_id = "louisan1128/chatanalysis"
model_path = "/app/resources/finetuned"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = GPT2LMHeadModel.from_pretrained(model_path).to(device)
# model.eval()
model = None



# 챗봇 응답 생성 함수
@processing_router1.post("/evaluate")
def generate_response(req: ChatRequest, max_len=100, top_p=0.9, top_k=50):
    global model
    if model is None:
        print("모델이 아직 로드되지 않았습니다.")
        required_files = ['config.json']

        for f in required_files:
            if not os.path.exists(os.path.join(model_path, f)):
                raise HTTPException(
                    status_code=503,
                    detail=f"모델 파일이 준비되지 않았습니다. ({f} 파일이 없습니다)"
                )
        print(f"모델 파일이 준비되었습니다. {model_path}에서 모델을 로드합니다.")
        try:
            model = GPT2LMHeadModel.from_pretrained(model_path).to(device)
            model.eval()
            print("모델이 성공적으로 로드되었습니다.")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"모델 로드 중 오류가 발생했습니다: {str(e)}"
            )
        
    print(req.message)
    input_text = f"{ME_TKN}{req.message}{SENT}{YOU_TKN}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

    output = model.generate(
        input_ids,
        max_length=len(input_ids[0]) + max_len,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=top_k,
        top_p=top_p,
        temperature=0.8,
        repetition_penalty=1.5,
    )

    response = tokenizer.decode(output[0], skip_special_tokens=False)
    
    you_index = response.find(YOU_TKN)
    if you_index != -1:
        response = response[you_index + len(YOU_TKN):]

    for tok in [ME_TKN, YOU_TKN, SENT, PAD, MASK, EOS]:
        response = response.replace(tok, "")


    return {"response": response}


### 예시
# if __name__ == "__main__":
#     print("🤖 KoGPT2 챗봇 (단발성 대화) 시작! (종료하려면 'quit' 입력)")

#     while True:
#         user_input = input("👤 You: ")
#         if user_input.lower() in ["quit", "exit", "종료"]:
#             print("대화를 종료합니다.")
#             break
        
#         user_input = f"{ME_TKN}{user_input}{SENT}{YOU_TKN}"
#         answer = generate_response(user_input)
#         print(f"🤖 Bot:{answer}")
