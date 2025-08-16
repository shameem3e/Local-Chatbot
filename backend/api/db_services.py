from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.db_services import add_message, create_new_conversation_id

router = APIRouter()

class AddMessageRequest(BaseModel):
    conversation_id: str = None
    role: str
    content: str

class AddMessageResponse(BaseModel):
    conversation_id: str
    status: str

@router.post("/add_message", response_model=AddMessageResponse)
def add_message_endpoint(request: AddMessageRequest):
    try:
        conv_id = request.conversation_id or create_new_conversation_id()
        add_message(conv_id, request.role, request.content)
        return AddMessageResponse(conversation_id=conv_id, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
