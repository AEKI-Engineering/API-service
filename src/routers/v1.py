from fastapi import APIRouter, Depends
from src.dependencies import get_detector

from src.modules.detector import Detector
from ..schemas import PredictRequest, PredictResponse

router = APIRouter()


@router.post(
    "/object-detection/predict",
    name="Detect objects in the image.",
    description="Returns a list of localized object annotations.",
    response_model=PredictResponse,
)
async def predict(request: PredictRequest, detector: Detector = Depends(get_detector)):
    detections = detector.predict(request.image)
    return PredictResponse(detections=detections["results"])


@router.post(
    "/object-detection/predict/batch",
    name="Batch detection on multiple images.",
    description="Returns a list of localized object annotations for each image.",
)
async def predict_batch(detector: Detector = Depends(get_detector)):
    return {"foo": "bar"}
