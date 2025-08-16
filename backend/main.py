from fastapi import FastAPI
from backend.api.chat import router as chat_router
from backend.api.provider_models import router as provider_models_router
from backend.api.conversation import router as conversation_router
from backend.api.title import router as title_router
from backend.api.db_services import router as db_services_router

app = FastAPI()

app.include_router(chat_router, prefix="/api")
app.include_router(provider_models_router, prefix="/api")
app.include_router(conversation_router, prefix="/api")
app.include_router(title_router, prefix="/api")
app.include_router(db_services_router, prefix="/api")
