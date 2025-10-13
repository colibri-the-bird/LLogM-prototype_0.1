"""Model export stubs for HWR64."""

from __future__ import annotations

from pathlib import Path

import torch


def export_onnx(model: torch.nn.Module, out_path: Path, input_shape: tuple[int, ...] = (1, 1, 64, 64)) -> None:
    """Export the given model to ONNX format."""

    dummy = torch.randn(*input_shape)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.onnx.export(model, dummy, out_path)
    print(f"[HWR64] Exported model to {out_path}")


__all__ = ["export_onnx"]
