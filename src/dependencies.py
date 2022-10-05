from functools import cache
from src.modules.detector import Detector

@cache
def get_detector():
    return Detector("models/yolo5s-coco-base.torchscript")