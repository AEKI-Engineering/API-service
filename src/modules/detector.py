from typing import List, Tuple, Union
from pathlib import Path
from typing import Any, Dict
import numpy as np
import torch
from src.modules.loaders import ImagesLoader
from src.modules.utils import non_max_suppression, scale_coords

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

        self.device = torch.device("cpu")

        self.model = torch.load(Path(weights_path))
        self.stride = int(32)

    @torch.no_grad()
    def predict(self, x: Union[List[BaseImageModel], BaseImageModel]) -> Dict[str, Any]:
        # Load Images
        dataset = ImagesLoader(files=x, img_size=self.img_size, stride=self.stride)

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
        img = img / 255
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

    def _process_detection(self, detection: torch.Tensor, image: np.ndarray, img_tensor: torch.Tensor) -> List[Any]:
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

    def _prepare_results(self, xyxy: Tuple[torch.Tensor], confidence_score: torch.Tensor, detected_class: torch.Tensor, gain: torch.Tensor) -> Dict[str, Any]:
        normalized_xyxy = (torch.tensor(xyxy).view(1, 4) / gain).view(-1).tolist()

        x0, y0, x1, y1 = normalized_xyxy[:4]

        return {
            # "name": self.model.names[int(detected_class.item())],
            "name": int(detected_class.item()),
            "score": round(confidence_score.item(), 2),
            "boundingBox": [
                {"x": x0, "y": y0},
                {"x": x1, "y": y0},
                {"x": x1, "y": y1},
                {"x": x0, "y": y1},
            ],
        }

