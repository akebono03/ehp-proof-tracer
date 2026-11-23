"""Focused fail-closed tests for the R3R33R1 read-only audit."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

FILE = Path(__file__).resolve().parents[1] / "audit.py"
SPEC = importlib.util.spec_from_file_location("phase176_r3r33r1_audit", FILE)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def test_check_sources_rejects_missing_files(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="MISSING_SOURCE"):
        AUDIT.check_sources(tmp_path)


def test_check_sources_rejects_missing_anchor(tmp_path: Path) -> None:
    for name in AUDIT.FILES:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("pass\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_CHANGED"):
        AUDIT.check_sources(tmp_path)


def test_check_sources_requires_r3r31_binding(tmp_path: Path) -> None:
    for name, anchors in AUDIT.FILES.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join("# " + anchor for anchor in anchors) + "\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R3R31_PUBLIC_CONNECTION_MISSING"):
        AUDIT.check_sources(tmp_path)


def test_package_does_not_mutate_repository() -> None:
    text = FILE.read_text(encoding="utf-8")
    assert "write_bytes(" not in text
    assert "git reset" not in text
    assert "git checkout" not in text
