import base64
from io import BytesIO
from typing import List, Tuple, Union
import cv2
from cv2 import Mat
import numpy as np
from PIL import Image

from src.schemas import BaseImageModel

from .augmentations import letterbox


class ImagesLoader():

    def __init__(self, files: Union[List[BaseImageModel], BaseImageModel], img_size: int = 640, stride: int = 32):
        self.img_size = img_size
        self.stride = stride

        self.files = files if isinstance(files, list) else [files]
        self.nf = len(self.files)

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self) -> Tuple[str, np.ndarray, Mat, str]:
        if self.count == self.nf:
            raise StopIteration

        # Load image
        file = self.files[self.count].to_pil_image()

        # Load image in BGR
        img0 = cv2.cvtColor(np.array(file), cv2.COLOR_RGB2BGR)
        # Padded resize (YOLOv5 inference)
        img = letterbox(img0, self.img_size, stride=self.stride)[0]

        # Transform to RBG contiguous array
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)

        self.count += 1

        return "", img, img0, ""
