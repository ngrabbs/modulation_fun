"""Dataclasses that describe Lesson 1 parameters and signal stages."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence

import numpy as np

# Lesson 1 presets that the UI can expose directly.
PRESET_BITSTRINGS: List[str] = ["01011010", "10101010", "11110000"]


@dataclass
class LessonParams:
    """User-configurable parameters for Lesson 1."""

    bitstring: str
    sps: int
    snr_db: float
    mapping: str
    seed: int


@dataclass
class SignalStage:
    """Container for a Lesson 1 processing stage."""

    name: str
    x: np.ndarray
    y: np.ndarray
    meta: Dict[str, object] = field(default_factory=dict)


@dataclass
class LessonRun:
    """Result of running the Lesson 1 pipeline."""

    params: LessonParams
    stages: Sequence[SignalStage]
    input_bits: np.ndarray
    output_bits: np.ndarray
    errors: Dict[str, object]
