from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.db_services import get_conversation, get_all_conversations, create_new_conversation

router = APIRouter()

class CreateConversationRequest(BaseModel):
    title: str = None
    role: str = None
    content: str = None

class CreateConversationResponse(BaseModel):
    conversation_id: str
    title: str
    first_message: dict = None

@router.get("/conversation/{conv_id}")
def get_conversation_endpoint(conv_id: str):
    try:
        conversation = get_conversation(conv_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations")
def get_all_conversations_endpoint():
    try:
        return get_all_conversations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversation", response_model=CreateConversationResponse)
def create_conversation_endpoint(request: CreateConversationRequest):
    try:
        conv_id = create_new_conversation(request.title, request.role, request.content)
        first_message = None
        if request.role and request.content:
            first_message = {"role": request.role, "content": request.content}
        return CreateConversationResponse(conversation_id=conv_id, title=request.title or "Untitled Conversation", first_message=first_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
