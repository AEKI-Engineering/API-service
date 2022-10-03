from abc import ABC, abstractmethod
import base64
from io import BytesIO
from typing import Any, List, Union
from pydantic import BaseModel, constr, conbytes

from PIL import Image
import requests

UrlType = constr(regex="(https|http)?:\/\/.+")
BytesType = conbytes()

class BaseImageModel(ABC, BaseModel):

    @abstractmethod
    def to_pil_image(self) -> Image:
        return NotImplementedError

class ImageURL(BaseImageModel):
    __root__: UrlType

    def to_pil_image(self) -> Image:
        return Image.open(BytesIO(requests.get(self.__root__).content))


class ImageBytes(BaseImageModel):
    __root__: BytesType

    def to_pil_image(self) -> Image:
        return Image.open(BytesIO(base64.b64encode(self.__root__)))

class CoordinatesModel(BaseModel):
    x: float
    y: float

class DetectionModel(BaseModel):
    name: str
    score: float
    boundingBox: List[CoordinatesModel]

class PredictRequest(BaseModel):
    image: Union[ImageURL, ImageBytes]

class PredictResponse(BaseModel):
    detections: List[DetectionModel]