"""Function replacement is AST-scoped, source-validated and idempotent."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r12_public_two_summand_quotient import installer


def miniature() -> str:
    return (
        "from __future__ import annotations\n\n"
        "def untouched():\n    return 17\n\n"
        "def shared_expansion_provider(bridge):\n"
        + installer.ANCHOR
        + "    return bridge\n"
    )


def test_only_entire_shared_function_changes_and_is_idempotent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        installer.previous, "function_replacement",
        lambda baseline: (baseline, "", baseline),
    )
    original = miniature()
    updated, whole_fn, baseline = installer.function_replacement(original)
    assert baseline == original
    assert updated.count(installer.ADDITION) == 1
    assert updated.count("def untouched()") == 1
    assert "def untouched():\n    return 17" in updated
    assert whole_fn.startswith("def shared_expansion_provider(bridge):")
    assert installer.function_replacement(updated)[:2] == (updated, whole_fn)
    ast.parse(updated)


def test_duplicate_insertion_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        installer.previous, "function_replacement",
        lambda baseline: (baseline, "", baseline),
    )
    original = miniature().replace(installer.ANCHOR, installer.ANCHOR + installer.ADDITION * 2)
    with pytest.raises(RuntimeError, match="R4R12_ANCHOR_OR_ADDITION_DRIFT"):
        installer.function_replacement(original)


def test_unreviewed_prior_module_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        installer.previous, "function_replacement",
        lambda baseline: (baseline + "# fake source drift", "", baseline),
    )
    with pytest.raises(RuntimeError, match="R4R12_R4R11_NOT_INSTALLED"):
        installer.function_replacement(miniature())


def test_missing_target_function_rejected() -> None:
    with pytest.raises(RuntimeError, match="R4R12_SHARED_FUNCTION_NOT_UNIQUE"):
        installer.function_replacement("def untouched():\n    pass\n")


def test_duplicate_function_rejected() -> None:
    with pytest.raises(RuntimeError, match="R4R12_SHARED_FUNCTION_NOT_UNIQUE"):
        installer.function_replacement(miniature() + "\ndef shared_expansion_provider(x):\n    return x\n")
