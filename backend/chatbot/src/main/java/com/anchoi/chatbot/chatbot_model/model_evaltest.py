from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/evaluate")
def evaluate(req: ChatRequest):
    if "ㅋㅋㅋ" in req.message:
        return {"response": "ㅋㅋㅋㅋㅋㅋㅋ"}
    return {"response": "안녕!"}