"""Placeholder TinyNet-style model for HWR64 experiments."""

from __future__ import annotations

import torch
from torch import nn


class A1DSTinyNet(nn.Module):
    """Lightweight convolutional encoder stub."""

    def __init__(self, in_channels: int = 1, num_classes: int = 10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 16, kernel_size=3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Linear(32, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        feats = self.features(x)
        return self.classifier(feats.flatten(1))


__all__ = ["A1DSTinyNet"]
