"""Basic scaffolding tests for the Waveform Teaching App."""

import importlib


def test_package_imports() -> None:
    """The waveform_app package should be importable."""
    module = importlib.import_module("waveform_app")
    assert hasattr(module, "__version__")
