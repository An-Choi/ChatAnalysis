from fastapi import FastAPI
from eval import processing_router1
from data_parsing import processing_router

app = FastAPI()

# eval.py의 모든 라우트 등록
# app.mount("/eval", eval_app)

# dataparsing.py의 모든 라우트 등록
app.include_router(processing_router, prefix="")
app.include_router(processing_router1, prefix="")

