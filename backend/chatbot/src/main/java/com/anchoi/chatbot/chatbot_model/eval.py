import torch
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel


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

model_path = "./trained_test"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = GPT2LMHeadModel.from_pretrained(model_path).to(device)
model.eval()



# 챗봇 응답 생성 함수
def generate_response(user_input, max_len=50):
    input_text = f"{ME_TKN}{user_input}{SENT}{YOU_TKN}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

    # 모델 생성
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_len,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            do_sample=True,       
            top_k=50,
            top_p=0.95,
            temperature=0.9,
            no_repeat_ngram_size=3
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=False)

    # YOU_TKN 이후부터 출력 추출
    # if YOU_TKN in decoded:
    #     response = decoded.split(YOU_TKN)[-1].split(EOS)[0].strip()
    # else:
    #     response = decoded

    response = decoded
    return response


### 예시
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit"]:
        break
    response = generate_response(user_input)
    print("Bot:", response)