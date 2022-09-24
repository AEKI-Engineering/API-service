from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_PREFIX: str = "/api/v1"
    API_LATERST_PREFIX: str = "/api/latest"

settings = Settings()