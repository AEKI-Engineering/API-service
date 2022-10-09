from pydantic import BaseSettings

class Settings(BaseSettings):
    # TODO: Get version from pyproject.toml file
    APP_VERSION: str = "0.1.0"

    # API
    API_V1_PREFIX: str = "/api/v1"
    API_LATERST_PREFIX: str = "/api/latest"

    LOGGER_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "default": {"handlers": ["default"], "level": "DEBUG"},
        },
    }

    # Model
    MODEL_DIR: str = "models"
    MODEL_DEVICE: str = "cpu"
    MODEL_DEFAULT_BACKEND: str = 'torchscript'

    # WandB
    WANDB_ENTITY: str = "aeki-engineering"
    WANDB_PROJECT: str = "model-registry"
    WANDB_REGISTERED_MODEL: str = "yolov5"
    WANDB_DEFAULT_TAG: str = "latest"

settings = Settings()