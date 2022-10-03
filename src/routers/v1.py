from fastapi import APIRouter

from src.modules.detector import Detector
from ..schemas import PredictRequest, PredictResponse

router = APIRouter()

@router.on_event("startup")
def startup_event():
    global detector
    detector = Detector("models/yolo5s-coco-base.torchscript")


@router.post(
    "/object-detection/predict",
    name="Detect objects in the image.",
    description="Returns a list of localized object annotations.",
    response_model=PredictResponse
)
async def predict(request: PredictRequest):
    detections = detector.predict(request.image)
    return PredictResponse(detections=detections["results"])

@router.post(
    "/object-detection/predict/batch",
    name="Batch detection on multiple images.",
    description="Returns a list of localized object annotations for each image."
)
async def predict_batch():
    return {"foo": "bar"}