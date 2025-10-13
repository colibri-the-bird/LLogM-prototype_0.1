"""Loss function stubs for HWR64 models."""

from __future__ import annotations

from typing import Callable

import torch
from torch import nn


def classification_loss() -> Callable[[torch.Tensor, torch.Tensor], torch.Tensor]:
    """Return a basic cross-entropy loss for experimentation."""

    return nn.CrossEntropyLoss()


__all__ = ["classification_loss"]
