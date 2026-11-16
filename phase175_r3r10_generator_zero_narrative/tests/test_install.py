"""Dry-run planning, complete function replacement, and fail-closed guards."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r3r10_generator_zero_narrative import install


def _fixture_root(tmp_path: Path) -> Path:
    path = tmp_path / install.TARGET_RELATIVE
    path.write_text(
        'from __future__ import annotations\n\n'
        + install.BASE_FILE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return tmp_path


def test_plan_dry_run_does_not_write_and_full_function_replaces(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    target = root / install.TARGET_RELATIVE
    initial = target.read_bytes()
    plan = install.plan_patch(root)
    assert plan.status == "PATCH_REQUIRED"
    assert target.read_bytes() == initial
    install.apply_patch(root, plan)
    assert target.read_bytes() != initial
    assert install.plan_patch(root).status == "ALREADY_APPLIED"
    assert install._normalized_function(target.read_text(encoding="utf-8")) == plan.replacement_function


def test_unknown_function_version_fails_closed(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    target = root / install.TARGET_RELATIVE
    target.write_text(target.read_text(encoding="utf-8").replace(
        '    return None\n', '    return "unreviewed"\n', 1,
    ), encoding="utf-8")
    with pytest.raises(RuntimeError, match="CURRENT_TYPED_SENTENCE_DIFFERS"):
        install.plan_patch(root)


def test_crlf_file_preserves_line_endings(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    target = root / install.TARGET_RELATIVE
    # Path.write_text() may already have produced CRLF on Windows.
    normalized = target.read_bytes().replace(b"\r\n", b"\n")
    target.write_bytes(normalized.replace(b"\n", b"\r\n"))
    assert b"\r\r\n" not in target.read_bytes()
    plan = install.plan_patch(root)
    assert plan.status == "PATCH_REQUIRED"
    install.apply_patch(root, plan)
    result = target.read_bytes()
    assert b"\r\n" in result
    assert b"\r\r\n" not in result
    assert result.count(b"\n") == result.count(b"\r\n")
