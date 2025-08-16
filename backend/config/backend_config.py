from pydantic_settings import BaseSettings
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    DB_PATH: str
    CONVERSATION_TABLE_NAME: str
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    class Config:
        env_file = ".env"
        extra="allow"

def get_provider_models():
    config_path = Path(__file__).parent / "models_config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    llm_config = config.get("llm", {})
    return {provider.lower(): models for provider, models in llm_config.items()}

backend_settings = Settings()

# example usage
# print(get_provider_models(), backend_settings.API_HOST)
