from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.title import get_chat_title

router = APIRouter()

class TitleRequest(BaseModel):
    provider: str
    model: str
    query: str

class TitleResponse(BaseModel):
    title: str

@router.post("/title", response_model=TitleResponse)
def title_endpoint(request: TitleRequest):
    try:
        result = get_chat_title(request.provider, request.model, request.query)
        return TitleResponse(title=result["title"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

