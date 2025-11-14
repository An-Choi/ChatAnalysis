import torch
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import os

processing_router1 = APIRouter()

MAX_TURNS = 3 #저장되는 최대 대화 턴
history = [] #대화 턴 저장


def build_prompt(user_message: str) -> str:
    prompt= []
    for m, u in history[-MAX_TURNS:] :
        prompt.append(f"{ME_TKN}{m}{SENT}{YOU_TKN}{u}{SENT}")

    prompt.append(f"{ME_TKN}{user_message}{SENT}{YOU_TKN}")

    return "".join(prompt)

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
    global model, history
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


    input_text = build_prompt(req.message)
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

    decoded = tokenizer.decode(output[0], skip_special_tokens=False)
    
    ##마지막 you token 찾기
    last_you = decoded.rfind(YOU_TKN)
    if last_you == -1:
        response = decoded  # fallback
    else:
        response = decoded[last_you + len(YOU_TKN):]

    #eos 앞 자르기
    eos_pos = response.find(EOS)
    if eos_pos != -1:
        response = response[:eos_pos]

    ##토큰 제거
    for tok in [ME_TKN, YOU_TKN, SENT, PAD, MASK, EOS]:
        response = response.replace(tok, "")


    ##history max turn까지 유지
    history.append((req.message, response))
    if len(history) > MAX_TURNS:
        history = history[-MAX_TURNS:]

    return {"response": response}

