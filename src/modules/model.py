import json
from typing import Any, Tuple
from pathlib import Path
import torch

import wandb

from src.logger import get_logger
from src.config import settings

log = get_logger(__name__)


class Model:
    def __init__(
        self, model_root: str, tag: str, backend: str, cache: bool = True
    ) -> None:
        self.model_root = model_root
        self.tag = tag
        self.cache = cache
        self.backend = backend.lower()

        self.model, self.stride, self.names = self._load_model()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.model

    def _load_model(self) -> Tuple[Any, int, list]:
        log.info(f"Loading model, tag='{self.tag}', backend='{self.backend}'...")
        model_path = None

        # Serve model from cache if exists
        if self.cache and Path(self.model_root, self.tag).is_dir():
            try:
                model_path = list(
                    Path(self.model_root, self.tag).glob(f"*.{self.backend}")
                )[0]
                log.info(f"Serving model from local cache...")
            except IndexError:
                # Silently pass and serve model from model registry
                pass

        # Get model from model registry
        if model_path == None:
            # Initialize WandB API
            api = wandb.Api()

            # Download tag artifacts
            log.info("Fetching model from WandB model registry...")
            artifact = api.artifact(
                f"{settings.WANDB_ENTITY}/{settings.WANDB_PROJECT}/{settings.WANDB_REGISTERED_MODEL}:{self.tag}"
            )
            artifact.download(root=f"{self.model_root}/{self.tag}")

            # Get model path
            try:
                model_path = list(
                    Path(self.model_root, self.tag).glob(f"*.{self.backend}")
                )[0]
            except IndexError:
                log.error(f"Failed to fetch model for backend='{self.backend}'")
                return None, None, None

        if self.backend == "torchscript":
            # TorchScript backend stores stride and names in config file
            extra_files = {"config.txt": ""}
            model = torch.jit.load(Path(model_path), _extra_files=extra_files)
            if extra_files["config.txt"]:  # load metadata dict
                data = json.loads(
                    extra_files["config.txt"],
                    object_hook=lambda data: {
                        int(k) if k.isdigit() else k: v for k, v in data.items()
                    },
                )
                stride, names = int(data["stride"]), data["names"]
            else:
                stride = 32
                names = None
        elif self.backend == "pt":
            # PyTorch format needs class in working directory
            model = torch.load(Path(model_path))
            stride = max(int(self.model.stride.max()), 32)
            names = self.model.names
        else:
            log.error(f"Unsupported backend type: {self.backend}")
            return None, None, None

        if names:
            log.info(
                f"Successfully loaded '{self.backend}' model, with stride='{stride}' and {len(names)} classes."
            )
        else:
            log.info(
                f"Successfully loaded '{self.backend}' model, with stride='{stride}'"
            )
        return model, stride, names
