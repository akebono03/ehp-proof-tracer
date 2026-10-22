import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'audit.py'
spec = importlib.util.spec_from_file_location('r214_audit', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_preview_none():
    assert module.preview(None) is None


def test_preview_truncation():
    assert module.preview('x' * 300) == 'x' * 240
