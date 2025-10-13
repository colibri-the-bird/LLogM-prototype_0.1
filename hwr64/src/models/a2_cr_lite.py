"""Placeholder convolutional-recurrent lite model for HWR64."""

from __future__ import annotations

import torch
from torch import nn


class A2CRLite(nn.Module):
    """Simple CNN + GRU stack for smoke testing."""

    def __init__(self, in_channels: int = 1, hidden_size: int = 64, num_classes: int = 10):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
        )
        self.rnn = nn.GRU(input_size=64 * 16, hidden_size=hidden_size, batch_first=True)
        self.classifier = nn.Linear(hidden_size, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        b, c, h, w = x.shape
        feats = self.cnn(x)
        feats = feats.permute(0, 3, 1, 2).contiguous().view(b, feats.shape[3], -1)
        out, _ = self.rnn(feats)
        return self.classifier(out[:, -1])


__all__ = ["A2CRLite"]
