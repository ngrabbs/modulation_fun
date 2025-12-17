"""Tests for the matched filter stage."""

import numpy as np
import pytest

from waveform_app.lesson1.stages import matched_filter


def test_matched_filter_outputs_scaled_symbols_without_noise():
    symbols = np.array([-1.0, 1.0, -1.0])
    sps = 4
    tx_waveform = np.repeat(symbols, sps)

    y, decision_indices = matched_filter(tx_waveform, sps)

    assert decision_indices.size == symbols.size
    np.testing.assert_allclose(y[decision_indices], symbols * sps)


def test_decision_indices_are_increasing_and_in_bounds():
    symbols = np.array([1.0, -1.0, 1.0, -1.0])
    sps = 3
    tx_waveform = np.repeat(symbols, sps)

    y, decision_indices = matched_filter(tx_waveform, sps)

    assert decision_indices[0] == sps - 1
    np.testing.assert_array_equal(np.diff(decision_indices), np.full(decision_indices.size - 1, sps))
    assert decision_indices[-1] < y.size


def test_matched_filter_requires_positive_sps():
    with pytest.raises(ValueError):
        matched_filter([1.0, -1.0], sps=0)
