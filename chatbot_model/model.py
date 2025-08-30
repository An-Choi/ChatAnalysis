import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
import os
from tqdm import tqdm
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel, Trainer, TrainingArguments 

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.abspath(os.path.join(
    CURRENT_DIR,
    "../../../../../resources/processed_data"
))

ME_TKN = "<me>" #user
YOU_TKN = "<you>" #bot
BOS = "</s>" #begin sentence
EOS = "</s>" #end sentence
MASK = "<mask>"
SENT = "<sent>" #문장 구분
PAD = "<pad>" #패딩

save_dir = "saved_models"
os.makedirs(save_dir, exist_ok=True)

#kogpt 토크나이저
koGPT2_TOKENIZER = PreTrainedTokenizerFast.from_pretrained(
    "skt/kogpt2-base-v2",
    bos_token=BOS,
    eos_token=EOS,
    unk_token="<unk>",
    pad_token=PAD,
    mask_token=MASK,
)

print("test1")

#최종 목표
#(ME_TKN) + 사용자 데이터 + (SENT) + (YOU_TKN) + 상대방 데이터 + (EOS)

class ChatDataset(Dataset):
    def __init__(self, data, max_len=50):
        self.data = data
        self.max_len = max_len

        self.me_token = ME_TKN
        self.you_token = YOU_TKN
        self.eos = EOS
        self.mask = MASK
        self.sent = SENT
        self.tokenizer = koGPT2_TOKENIZER

    
    def __len__(self):
        return len(self.data)
    

    def __getitem__(self, idx):
        turn = self.data.iloc[idx]

        me = turn["me"]
        you = turn["you"]

        me_t = self.tokenizer.tokenize(self.me_token + me + self.sent) #사용자 토큰화
        me_len =len(me_t)

        you_t = self.tokenizer.tokenize(self.you_token + you + self.eos) #챗봇 토근화
        you_len = len(you_t)


        #max 길이 초과에 따른 길이 재조정 필요
        #길이 초과
        total_len = me_len + you_len
        if total_len > self.max_len:
            you_len = self.max_len - me_len

            #me 길이만으로 최대 길이 초과
            if you_len <= 0:
                me_t = me_t[-(int(self.max_len/2)):] #최대 길이 반으로
                me_len = len(me_t)
                you_len = self.max_len - me_len

            you_t = you_t[:you_len]
            you_len = len(you_t)

        ###전체 대화 학습

        #입력용
        input = me_t + you_t 
        input_ids = self.tokenizer.convert_tokens_to_ids(input) 
        attention_mask = [1] * len(input_ids)

        #학습용
        labels = input_ids.copy()
        
        #패딩 추가
        padding_len = self.max_len - len(input_ids)
        if padding_len > 0:
            input_ids += [self.tokenizer.pad_token_id] * padding_len
            attention_mask += [0] * padding_len
            labels += [-100] * padding_len

        return {
            "input_ids": torch.tensor(input_ids),
            "attention_mask": torch.tensor(attention_mask),
            "labels": torch.tensor(labels),
        }


#kogpt 모델
dataname = "processed.csv"
file_path = os.path.join(SAVE_DIR, 'processed.csv')
Chatbot_data = pd.read_csv(file_path)

print("test2")

####모델 만들기
train_set = ChatDataset(Chatbot_data, max_len=50)

#학습 배치 단위 설정 필요 (대화 단위로 묶기?)
training_args = TrainingArguments(
    output_dir="./trained_test",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    save_total_limit=1,
    fp16=torch.cuda.is_available(),
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = GPT2LMHeadModel.from_pretrained("skt/kogpt2-base-v2").to(device)

trainer = Trainer(
    model = model,
    args = training_args,
    train_dataset=train_set
)

trainer.train()

model.save_pretrained("./trained_test")

print("Model Saved At: ./trained_test")
