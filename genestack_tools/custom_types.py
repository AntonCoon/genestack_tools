from pydantic import BaseModel

class AskModelRequest(BaseModel):
    prompt: str
    model: str
    max_tokens: int = 1000
    temperature: float = 0.1

class AskModelResponse(BaseModel):
    content: str
