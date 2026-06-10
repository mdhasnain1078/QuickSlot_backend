from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "QuickSlot"
    API_V1_STR: str = "/api/v1"
    
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "quickslot"
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
