from abc import ABC, abstractmethod
import base64
from io import BytesIO
from typing import Any, Dict, List, Union
from pydantic import BaseModel, constr, conbytes

from PIL import Image
import requests

UrlType = constr(regex="(https|http)?:\/\/.+")


class BaseImageModel(ABC, BaseModel):
    @abstractmethod
    def to_pil_image(self) -> Image:
        return NotImplementedError


class ImageURL(BaseImageModel):
    __root__: UrlType

    def to_pil_image(self) -> Image:
        return Image.open(BytesIO(requests.get(self.__root__).content)).convert("RGB")


class ImageBytes(BaseImageModel):
    __root__: bytes

    def to_pil_image(self) -> Image:
        return Image.open(BytesIO(base64.b64decode(self.__root__))).convert("RGB")


class CoordinatesModel(BaseModel):
    x: float
    y: float


class DetectionModel(BaseModel):
    name: str
    score: float
    boundingBox: List[CoordinatesModel]


class BatchDetectionModel(BaseModel):
    source: str
    detections: List[DetectionModel]


class PredictRequest(BaseModel):
    image: Union[ImageURL, ImageBytes]


class PredictBatchRequest(BaseModel):
    images: List[Union[ImageURL, ImageBytes]]


class PredictResponse(BaseModel):
    detections: List[DetectionModel]
    time: float


class PredictBatchResponse(BaseModel):
    batchResults: List[BatchDetectionModel]
    time: float
