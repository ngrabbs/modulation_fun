"""Lesson 1 DSP stage helpers."""

from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np


def matched_filter(x: Sequence[float], sps: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Apply a rectangular matched filter and return decision indices.

    Parameters
    ----------
    x:
        Received waveform samples containing an integer number of symbols.
    sps:
        Samples per symbol used to create the waveform. Must be >= 1.

    Returns
    -------
    y:
        Filtered waveform computed via convolution with a length-``sps`` ones kernel.
    decision_indices:
        Sample indices within ``y`` at which symbol decisions should be taken.
    """

    if sps < 1:
        raise ValueError("Samples-per-symbol must be >= 1.")

    samples = np.asarray(x, dtype=float)
    kernel = np.ones(sps, dtype=float)
    y = np.convolve(samples, kernel, mode="full")

    n_symbols = samples.size // sps
    if n_symbols == 0:
        decision_indices = np.array([], dtype=int)
    else:
        decision_indices = (sps - 1) + np.arange(n_symbols) * sps

    return y, decision_indices
