"""Atomic function replacement and Windows CRLF boundary checks."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r3r11_cited_hopf_narrative import install


def _fixture(tmp_path: Path, *, eol: bytes = b"\n") -> Path:
    target = tmp_path / install.TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    text = b"# unrelated top-level declarations\n\n" + install.BASE.encode("utf-8")
    target.write_bytes(text.replace(b"\n", eol))
    return tmp_path


def test_full_function_is_only_changed_segment(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    plan = install.plan_patch(root)
    assert plan.status == "PATCH_REQUIRED"
    assert plan.new_bytes.startswith(b"# unrelated top-level declarations\n\n")
    assert plan.new_bytes.endswith(install.FULL.encode("utf-8"))
    install.apply_patch(root, plan)
    again = install.plan_patch(root)
    assert again.status == "ALREADY_APPLIED"
    assert again.old_bytes == again.new_bytes


def test_crlf_fixture_preserves_only_crlf(tmp_path: Path) -> None:
    root = _fixture(tmp_path, eol=b"\r\n")
    plan = install.plan_patch(root)
    install.apply_patch(root, plan)
    raw = (root / install.TARGET).read_bytes()
    assert plan.status == "PATCH_REQUIRED"
    assert b"\r\r\n" not in raw
    assert raw.count(b"\r\n") == raw.count(b"\n")
    assert raw.endswith(install.FULL.encode("utf-8").replace(b"\n", b"\r\n"))
    assert install.plan_patch(root).status == "ALREADY_APPLIED"


def test_rejects_unreviewed_formatter_and_mixed_eol(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    target = root / install.TARGET
    target.write_bytes(target.read_bytes().replace(b"Keep the original", b"Discard the original"))
    with pytest.raises(RuntimeError, match="REVIEWED_FORMATTER_MISMATCH"):
        install.plan_patch(root)
    root = _fixture(tmp_path)
    target.write_bytes(b"# first\r\n# second\n" + install.BASE.encode("utf-8"))
    with pytest.raises(RuntimeError, match="MIXED_EOL"):
        install.plan_patch(root)


def test_patch_is_stale_write_protected(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    plan = install.plan_patch(root)
    target = root / install.TARGET
    target.write_bytes(target.read_bytes() + b"# concurrent change\n")
    with pytest.raises(RuntimeError, match="TARGET_CHANGED_SINCE_PREFLIGHT"):
        install.apply_patch(root, plan)
