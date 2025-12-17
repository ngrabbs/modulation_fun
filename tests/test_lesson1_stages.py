"""Tests for Lesson 1 stage helpers."""

import numpy as np
import pytest

from waveform_app.lesson1.stages import bits_to_symbols, symbols_to_waveform


def test_bits_to_symbols_default_mapping():
    bits = [0, 1, 0, 1]
    symbols = bits_to_symbols(bits)
    np.testing.assert_array_equal(symbols, np.array([-1.0, 1.0, -1.0, 1.0]))


def test_bits_to_symbols_inverted_mapping():
    bits = [0, 1, 1, 0]
    symbols = bits_to_symbols(bits, mapping="0->+1")
    np.testing.assert_array_equal(symbols, np.array([1.0, -1.0, -1.0, 1.0]))


def test_bits_to_symbols_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        bits_to_symbols([0, 2, 1])
    with pytest.raises(ValueError):
        bits_to_symbols([0, 1], mapping="invalid")


def test_symbols_to_waveform_generates_rectangular_pulse_and_boundaries():
    symbols = np.array([-1.0, 1.0])
    waveform, boundaries = symbols_to_waveform(symbols, sps=4)
    np.testing.assert_array_equal(
        waveform, np.array([-1.0, -1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0])
    )
    np.testing.assert_array_equal(boundaries, np.array([0, 4, 8]))
    assert waveform.size == symbols.size * 4


def test_symbols_to_waveform_requires_positive_sps():
    with pytest.raises(ValueError):
        symbols_to_waveform([1.0, -1.0], sps=0)
