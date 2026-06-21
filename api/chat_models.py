# models/chat_models.py

from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    question: str
    conversation_id : str



class ChatResponse(BaseModel):
    answer: str