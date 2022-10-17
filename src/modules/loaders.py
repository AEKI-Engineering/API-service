import base64
from typing import List, Tuple, Union
import numpy as np

from src.schemas import BaseImageModel

from .augmentations import letterbox


class ImagesLoader:
    def __init__(
        self,
        files: Union[List[BaseImageModel], BaseImageModel],
        img_size: int = 640,
        stride: int = 32,
        auto: bool = False,
    ):
        self.img_size = img_size
        self.stride = stride
        self.auto = auto

        self.files = files if isinstance(files, list) else [files]
        self.nf = len(self.files)

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self) -> Tuple[str, np.ndarray, np.ndarray, str]:
        if self.count == self.nf:
            raise StopIteration

        # Load image
        file = self.files[self.count].to_pil_image()

        # Load image
        img0 = np.array(file)
        # Padded resize (YOLOv5 inference)
        img = letterbox(
            img0, new_shape=self.img_size, stride=self.stride, auto=self.auto
        )[0]

        # Transform to RBG contiguous array
        img = img.transpose(2, 0, 1)
        img = np.ascontiguousarray(img)

        self.count += 1

        return "", img, img0, ""
