# API endpoint to return provider and models data
from fastapi import APIRouter
from backend.services.provider_models import fetch_provider_models

router = APIRouter()

@router.get("/provider-models")
def get_provider_models_api():
    return fetch_provider_models()

