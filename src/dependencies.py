from functools import cache
from src.modules.detector import Detector
from src.modules.model import Model
from src.config import settings


@cache
def get_detector():
    return Detector(
        model=Model(
            model_root=settings.MODEL_DIR,
            tag=settings.WANDB_DEFAULT_TAG,
            backend=settings.MODEL_DEFAULT_BACKEND,
        )
    )
