"""Tests for Lesson 1 input validation."""

import pytest

from waveform_app.lesson1.models import PRESET_BITSTRINGS
from waveform_app.lesson1.validation import validate_bitstring


def test_validate_bitstring_accepts_min_and_max_length():
    assert validate_bitstring("0") == "0"
    max_bits = "01" * 32
    assert len(max_bits) == 64
    assert validate_bitstring(max_bits) == max_bits


@pytest.mark.parametrize("preset", PRESET_BITSTRINGS)
def test_presets_are_valid_bitstrings(preset: str):
    assert validate_bitstring(preset) == preset


@pytest.mark.parametrize(
    "value, expected_message",
    [
        ("", "Bitstring cannot be empty"),
        ("   ", "Bitstring cannot be empty"),
        ("012", "Bitstring may only contain 0 or 1 characters"),
        ("2", "Bitstring may only contain 0 or 1 characters"),
        ("01" * 33, "Bitstring cannot exceed 64 bits"),
    ],
)
def test_invalid_bitstrings_raise_user_friendly_errors(value: str, expected_message: str):
    with pytest.raises(ValueError) as excinfo:
        validate_bitstring(value)
    assert expected_message in str(excinfo.value)


def test_non_string_input_raises_type_error():
    with pytest.raises(TypeError):
        validate_bitstring(1010)  # type: ignore[arg-type]
