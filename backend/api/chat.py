from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.chat import chat_qa


router = APIRouter()

class ChatRequest(BaseModel):
    provider: str
    model: str
    chat_history: list
    conversation_id: str = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str | None

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    conv_id = request.conversation_id
    result = chat_qa(request.provider, request.model, request.chat_history)
    return ChatResponse(response=result, conversation_id=conv_id)
