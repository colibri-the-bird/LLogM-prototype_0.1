"""Evaluation helpers placeholder for HWR64."""

from __future__ import annotations

from typing import Iterable

import torch


def accuracy(logits: torch.Tensor, targets: torch.Tensor) -> float:
    """Compute simple accuracy for classification batches."""

    if logits.numel() == 0:
        return 0.0
    preds = logits.argmax(dim=-1)
    correct = (preds == targets).float().mean().item()
    return float(correct)


def summarize_metrics(metrics: Iterable[float]) -> float:
    values = list(metrics)
    if not values:
        return 0.0
    return float(sum(values) / len(values))


__all__ = ["accuracy", "summarize_metrics"]
