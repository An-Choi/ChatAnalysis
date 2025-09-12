import torch
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

repo_id = "louisan1128/chatanalysis"
model_path = "../resources/finetuned"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = GPT2LMHeadModel.from_pretrained(model_path).to(device)
model.eval()



# 챗봇 응답 생성 함수
@app.post("/evaluate")
def generate_response(req: ChatRequest, prompt, max_len=100, top_p=0.9, top_k=50):
    input_text = f"{ME_TKN}{req.message}{SENT}{YOU_TKN}"
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)

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

    tokenizer.decode(output[0], skip_special_tokens=False)
    
    


    return {"response": response}


### 예시
if __name__ == "__main__":
    print("🤖 KoGPT2 챗봇 (단발성 대화) 시작! (종료하려면 'quit' 입력)")

    while True:
        user_input = input("👤 You: ")
        if user_input.lower() in ["quit", "exit", "종료"]:
            print("대화를 종료합니다.")
            break
        
        user_input = f"{ME_TKN}{user_input}{SENT}{YOU_TKN}"
        answer = generate_response(user_input)
        print(f"🤖 Bot:{answer}")
