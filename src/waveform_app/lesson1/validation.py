"""Input validation helpers for Lesson 1."""

from __future__ import annotations


def validate_bitstring(bitstring: str) -> str:
    """
    Ensure the provided bitstring contains only 0/1 characters and is 1-64 bits long.

    Returns the stripped bitstring for convenience.
    """

    if not isinstance(bitstring, str):
        raise TypeError("Bitstring must be a string of 0s and 1s.")

    normalized = bitstring.strip()
    if not normalized:
        raise ValueError("Bitstring cannot be empty.")

    if len(normalized) > 64:
        raise ValueError("Bitstring cannot exceed 64 bits.")

    invalid_chars = sorted(set(c for c in normalized if c not in ("0", "1")))
    if invalid_chars:
        raise ValueError("Bitstring may only contain 0 or 1 characters.")

    return normalized
