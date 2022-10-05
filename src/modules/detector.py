import json
from typing import List, Tuple, Union
from pathlib import Path
from typing import Any, Dict
import numpy as np
import torch
from src.modules.loaders import ImagesLoader
from src.modules.utils import non_max_suppression, scale_coords
from src.logger import get_logger

log = get_logger(__name__)

from src.schemas import BaseImageModel


class Detector:
    def __init__(
        self,
        weights_path: str,
        img_size: int = 640,
        confidence_threshold: float = 0.1,
        iou_threshold: float = 0.25,
    ) -> None:
        self.img_size = img_size
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold

        self.device_name = "cpu"
        self.device = torch.device(self.device_name)

        # Detect backend
        self.backend = Path(weights_path).suffix.lower()

        if self.backend == ".torchscript":
            # TorchScript backend stores stride and names in config file
            extra_files = {"config.txt": ""}
            self.model = torch.jit.load(Path(weights_path), _extra_files=extra_files)
            if extra_files["config.txt"]:  # load metadata dict
                data = json.loads(
                    extra_files["config.txt"],
                    object_hook=lambda data: {
                        int(k) if k.isdigit() else k: v for k, v in data.items()
                    },
                )
                self.stride, self.names = int(data["stride"]), data["names"]
            else:
                self.stride = 32
                self.names = None
        elif self.backend == ".pt":
            # PyTorch format needs class in working directory
            self.model = torch.load(Path(weights_path))
            self.stride = max(int(self.model.stride.max()), 32)
            self.names = self.model.names
        else:
            raise AttributeError(f"Unsupported backend type: {self.backend}")

        log.info(f"Initializing detector class, backend='{self.backend}', device='{self.device_name}'")

    @torch.no_grad()
    def predict(self, x: Union[List[BaseImageModel], BaseImageModel]) -> Dict[str, Any]:
        # Load Images
        dataset = ImagesLoader(
            files=x,
            img_size=self.img_size,
            stride=self.stride,
            auto=False if self.backend == ".torchscript" else True,
        )

        results = []
        for _, img, img0s, _ in dataset:
            # Convert image to tensor
            img_tensor = self._image_to_tensor(img)

            # Detect
            all_detections = self._detect_image(img_tensor)

            # Process detections
            for detection in all_detections:
                results += self._process_detection(detection, img0s.copy(), img_tensor)

        return {"results": results}

    def _image_to_tensor(self, img: np.ndarray) -> torch.Tensor:
        img = torch.from_numpy(img).to(self.device)
        img = img / 255.0
        if len(img.shape) == 3:
            img = img[None]
        return img

    def _detect_image(self, img_tensor: torch.Tensor) -> Any:
        detections = self.model(img_tensor)[0]
        return non_max_suppression(
            detections,
            conf_thres=self.confidence_threshold,
            iou_thres=self.iou_threshold,
        )

    def _process_detection(
        self, detection: torch.Tensor, image: np.ndarray, img_tensor: torch.Tensor
    ) -> List[Any]:
        all_detections = []
        gain = torch.tensor(image.shape)[[1, 0, 1, 0]]

        if len(detection):
            detection[:, :4] = scale_coords(
                img_tensor.shape[2:], detection[:, :4], image.shape
            ).round()
            for (
                *xyxy,
                confidence_score,
                detected_class,
            ) in reversed(detection):
                result = self._prepare_results(
                    xyxy,
                    confidence_score,
                    detected_class,
                    gain,
                )
                all_detections.append(result)

        return all_detections

    def _prepare_results(
        self,
        xyxy: Tuple[torch.Tensor],
        confidence_score: torch.Tensor,
        detected_class: torch.Tensor,
        gain: torch.Tensor,
    ) -> Dict[str, Any]:
        normalized_xyxy = (torch.tensor(xyxy).view(1, 4) / gain).view(-1).tolist()

        x0, y0, x1, y1 = normalized_xyxy[:4]

        return {
            "name": self.names[int(detected_class.item())]
            if self.names
            else int(detected_class.item()),
            "score": round(confidence_score.item(), 2),
            "boundingBox": [
                {"x": x0, "y": y0},
                {"x": x1, "y": y0},
                {"x": x1, "y": y1},
                {"x": x0, "y": y1},
            ],
        }
