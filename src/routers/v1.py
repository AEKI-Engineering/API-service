from fastapi import APIRouter

router = APIRouter()

@router.post(
    "/object-detection/predict",
    name="Detect objects in the image.",
    description="Returns a list of localized object annotations."
)
async def predict():
    return {"foo": "bar"}

@router.post(
    "/object-detection/predict/batch",
    name="Batch detection on multiple images.",
    description="Returns a list of localized object annotations for each image."
)
async def predict_batch():
    return {"foo": "bar"}