import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
import os
from tqdm import tqdm
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel, Trainer, TrainingArguments 
import argparse


ME_TKN = "<me>" #user
YOU_TKN = "<you>" #bot
BOS = "</s>" #begin sentence
EOS = "</s>" #end sentence
MASK = "<mask>"
SENT = "<sent>" #문장 구분
PAD = "<pad>" #패딩

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.abspath(os.path.join(
    CURRENT_DIR,
    "../resources/finetuned"
))
#save_dir = "/resources/finetuned"
#os.makedirs(save_dir, exist_ok=True)

#kogpt 토크나이저
koGPT2_TOKENIZER = PreTrainedTokenizerFast.from_pretrained(
    "skt/kogpt2-base-v2",
    bos_token=BOS,
    eos_token=EOS,
    unk_token="<unk>",
    pad_token=PAD,
    mask_token=MASK,
)

special_tokens_dict = {"additional_special_tokens": [ME_TKN, YOU_TKN, SENT]}
koGPT2_TOKENIZER.add_special_tokens(special_tokens_dict)

print("test1")


class ChatDataset(Dataset):
    def __init__(self, data, tokenizer, max_len=200):
        self.data = data
        self.tokenizer = tokenizer
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
        text = str(self.data.iloc[idx, 0])
        encoding = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_len,
            padding="max_length",
            return_tensors="pt",
        )
        input_ids = encoding["input_ids"].squeeze(0)
        attention_mask = encoding["attention_mask"].squeeze(0)
        labels = input_ids.clone()
        labels[labels == self.tokenizer.pad_token_id] = -100  # loss 계산 제외
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }


def train_model(csv_file_path : str):
    #kogpt 모델
    # asdf = os.path.abspath(os.path.join(
    #     CURRENT_DIR,
    #     "../resources/processed/processed.csv"
    # ))
    # processed_path = "/app/resources/processed/processed.csv"
    chat_data = pd.read_csv(csv_file_path)  ###수정 필요
    dataset = ChatDataset(chat_data, koGPT2_TOKENIZER, max_len=200)

    print("test2")

    ####모델 만들기
    training_args = TrainingArguments(
        output_dir=os.path.join(save_dir, "trained_test"),
        num_train_epochs=2,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        save_total_limit=2,
        save_steps=1000,
        logging_steps=200,
        fp16=False,
        report_to=[],
        disable_tqdm=False,
        learning_rate=5e-6,
    )

    # ===========================
    # 모델 로드 (1차 파인튜닝 모델)
    # ===========================
    ###hugging face 설정
    repo_id = "louisan1128/chatanalysis"

    model = GPT2LMHeadModel.from_pretrained(repo_id)

    model.resize_token_embeddings(len(koGPT2_TOKENIZER))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # ===========================
    # Trainer 생성 및 학습
    # ===========================
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    trainer.train()
    model.save_pretrained("/app/resources/finetuned")
    print("Model Saved At: app/resources/finetuned")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file_path", type=str, required=True, help="학습될 csv 파일 경로")
    args = parser.parse_args()
    train_model(args.csv_file_path)