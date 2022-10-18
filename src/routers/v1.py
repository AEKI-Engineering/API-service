import time
from fastapi import APIRouter, Depends
from src.dependencies import get_detector
from src.logger import get_logger

from src.modules.detector import Detector
from ..schemas import (
    BatchDetectionModel,
    PredictBatchRequest,
    PredictBatchResponse,
    PredictRequest,
    PredictResponse,
)

router = APIRouter()

log = get_logger(__name__)


@router.post(
    "/object-detection/predict",
    name="Detect objects in the image.",
    description="Returns a list of localized object annotations.",
    response_model=PredictResponse,
)
async def predict(request: PredictRequest, detector: Detector = Depends(get_detector)):
    log.info(f"Running detection on single {type(request.image).__name__}...")

    start_time = time.perf_counter()
    detections = detector.predict(request.image)
    end_time = time.perf_counter()

    log.info(
        f"Finished detection with {len(detections)} objects, in {round(end_time-start_time, 3)} seconds."
    )
    return PredictResponse(detections=detections, time=round(end_time - start_time, 3))


@router.post(
    "/object-detection/predict/batch",
    name="Batch detection on multiple images.",
    description="Returns a list of localized object annotations for each image.",
    response_model=PredictBatchResponse,
)
async def predict_batch(
    request: PredictBatchRequest, detector: Detector = Depends(get_detector)
):
    log.info(f"Running batch detection on {len(request.images)} images...")

    results = []
    start_time = time.perf_counter()
    for request_image in request.images:
        detections = detector.predict(request_image)
        results.append(
            BatchDetectionModel(
                source=str(request_image.__root__), detections=detections
            )
        )
    end_time = time.perf_counter()

    log.info(f"Finished batch detection, in {round(end_time-start_time, 3)} seconds.")
    return PredictBatchResponse(
        batchResults=results, time=round(end_time - start_time, 3)
    )
