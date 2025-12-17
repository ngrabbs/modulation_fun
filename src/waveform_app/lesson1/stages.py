"""Core Lesson 1 stage helpers."""

from __future__ import annotations

from typing import Literal, Sequence, Tuple

import numpy as np

MappingMode = Literal["0->-1", "0->+1"]


def bits_to_symbols(bits: Sequence[int], mapping: MappingMode = "0->-1") -> np.ndarray:
    """
    Map binary digits to antipodal BPSK symbols.

    Parameters
    ----------
    bits:
        Sequence containing 0/1 values.
    mapping:
        Controls the polarity of the mapping. By default 0 maps to -1 and 1 maps to +1.
        The alternate mode swaps those assignments.
    """

    if mapping not in ("0->-1", "0->+1"):
        raise ValueError("Mapping must be either '0->-1' or '0->+1'.")

    bits_array = np.asarray(bits, dtype=int)
    invalid = np.setdiff1d(bits_array, np.array([0, 1]))
    if invalid.size:
        raise ValueError("Bits sequence can only contain 0 or 1.")

    zero_symbol, one_symbol = (-1.0, 1.0) if mapping == "0->-1" else (1.0, -1.0)
    symbols = np.where(bits_array == 0, zero_symbol, one_symbol)
    return symbols.astype(float)


def symbols_to_waveform(symbols: Sequence[float], sps: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Expand symbol-rate samples into a rectangular pulse waveform.

    Parameters
    ----------
    symbols:
        Symbol amplitudes to up-sample.
    sps:
        Samples per symbol (must be >= 1).

    Returns
    -------
    waveform:
        1-D array with each symbol repeated ``sps`` times.
    boundaries:
        Sample indices corresponding to symbol boundaries for plotting. Includes the end index.
    """

    if sps < 1:
        raise ValueError("Samples-per-symbol must be >= 1.")

    symbols_array = np.asarray(symbols, dtype=float)
    waveform = np.repeat(symbols_array, sps)
    boundaries = np.arange(0, waveform.size + 1, sps)
    return waveform, boundaries
