from pydantic_settings import BaseSettings


class Settings(BaseSettings, extra="allow"):
    API_HOST: str = "localhost"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"
        extra = "allow"


frontend_settings = Settings()
