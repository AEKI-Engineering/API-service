from pydantic import BaseSettings

class Settings(BaseSettings):
    # TODO: Get version from pyproject.toml file
    APP_VERSION: str = "0.1.0"

    API_V1_PREFIX: str = "/api/v1"
    API_LATERST_PREFIX: str = "/api/latest"

settings = Settings()