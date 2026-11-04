"""Independent fail-closed contracts for the historical test-only corrections."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r17r3r4_historical_test_contract.patches import (
    CHANGES,
    FILES,
    transform,
)

ROOT = Path(__file__).resolve().parents[2]


def test_all_modified_tests_were_reviewed_and_are_syntactically_valid() -> None:
    assert set(FILES) == set(CHANGES)
    assert len(FILES) == 10
    for path in FILES:
        original = (ROOT / path).read_text(encoding="utf-8")
        updated = transform(path, original)
        assert updated != original.replace("\r\n", "\n")
        ast.parse(updated, filename=path)
        assert "pytest.skip" not in updated
        assert "pytest.xfail" not in updated


def test_every_replacement_is_fail_closed_and_not_repeatable() -> None:
    for path in FILES:
        updated = transform(path, (ROOT / path).read_text(encoding="utf-8"))
        with pytest.raises(RuntimeError, match="unreviewed or already patched"):
            transform(path, updated)


def test_unreviewed_test_path_is_rejected() -> None:
    with pytest.raises(ValueError, match="unreviewed test path"):
        transform("web_group_proof.py", "def test_dummy(): pass\n")


def test_helper_and_legacy_tests_are_preserved() -> None:
    p = ROOT / "phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py"
    updated = transform(p.relative_to(ROOT).as_posix(), p.read_text(encoding="utf-8"))
    assert "def test_source_verified_abstract_markdown_is_explicitly_partial" in updated
    assert "def test_shared_fallback_web_uses_same_abstract_projection" in updated
    assert "def test_trace_route_remains_without_added_narrative" in updated
    assert 'assert "証明済みの抽象群構造" in section' in updated
