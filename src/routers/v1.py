from fastapi import APIRouter

router = APIRouter()

@router.post(
    "/object-detection/predict",
    summary="Returns a list of localized object annotations"
)
async def predict():
    return {"foo": "bar"}

@router.post(
    "/object-detection/predict/batch",

)
async def predict_batch():
    return {"foo": "bar"}