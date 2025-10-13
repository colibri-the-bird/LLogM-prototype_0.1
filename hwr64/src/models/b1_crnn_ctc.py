"""Placeholder CRNN-CTC model for HWR64."""

from __future__ import annotations

import torch
from torch import nn


class B1CRNNCTC(nn.Module):
    """Tiny CRNN with linear CTC head."""

    def __init__(self, in_channels: int = 1, hidden_size: int = 128, num_classes: int = 64):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 2)),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 2)),
        )
        self.rnn = nn.LSTM(input_size=64 * 16, hidden_size=hidden_size, num_layers=2, batch_first=True, bidirectional=True)
        self.classifier = nn.Linear(hidden_size * 2, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        b, _, _, _ = x.shape
        feats = self.features(x)
        feats = feats.permute(0, 3, 1, 2).contiguous().view(b, feats.shape[3], -1)
        out, _ = self.rnn(feats)
        return self.classifier(out)


__all__ = ["B1CRNNCTC"]
