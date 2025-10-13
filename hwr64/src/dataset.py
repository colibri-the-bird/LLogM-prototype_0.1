"""Dataset registry placeholder for HWR64."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

import torch
from torch.utils.data import Dataset


@dataclass
class Sample:
    image: torch.Tensor
    label: int


class DummyDataset(Dataset[Sample]):
    """Small in-memory dataset for smoke tests."""

    def __init__(self, size: int = 4, image_shape: tuple[int, int] = (64, 64)):
        self.size = size
        self.image_shape = image_shape

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, idx: int) -> Sample:
        rng = torch.Generator().manual_seed(idx)
        image = torch.rand(1, *self.image_shape, generator=rng)
        return Sample(image=image, label=idx % 10)


def load_dataset(root: Path, factory: Optional[Callable[[], Dataset[Sample]]] = None) -> Dataset[Sample]:
    """Return a dataset instance for the given root."""

    if factory is not None:
        return factory()
    return DummyDataset()


__all__ = ["DummyDataset", "Sample", "load_dataset"]
