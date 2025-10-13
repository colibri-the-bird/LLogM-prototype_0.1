"""Placeholder for sleep phase scheduling utilities in HWR64."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def sleep_phase(duration: float) -> Iterator[None]:
    """Context manager that sleeps for the desired duration."""

    try:
        yield
    finally:
        time.sleep(duration)


__all__ = ["sleep_phase"]
