"""Data augmentation stubs for HWR64 datasets."""

from __future__ import annotations

from typing import Callable

import torch


def identity_augment() -> Callable[[torch.Tensor], torch.Tensor]:
    """Return a no-op augmentation callable."""

    def _apply(x: torch.Tensor) -> torch.Tensor:
        return x

    return _apply


__all__ = ["identity_augment"]
