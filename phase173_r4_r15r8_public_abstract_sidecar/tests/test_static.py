"""Offline source-patch regression tests. Never monkeypatch mathematical evidence."""
from __future__ import annotations

import ast

import pytest

from phase173_r4_r15r8_public_abstract_sidecar.patch_source import (
    END_BRANCH, END_REPLACEMENT, MODEL_FIELD, ORDER_BRANCH, ORDER_REPLACEMENT,
    transform_model, transform_selector,
)


def source_model() -> bytes:
    return (
        "from dataclasses import dataclass\nfrom typing import Any\n"
        "from proof import ProofStep\n"
        "@dataclass(frozen=True)\nclass PartialProofResult:\n"
        "    conclusion: Any | None = None\n"
        "    def __post_init__(self) -> None:\n"
        "        if self.status is ProofSearchStatus.NOT_SEARCHED and self.proven_steps:\n"
        "            pass\n"
    ).encode()


def source_selector() -> bytes:
    return (
        "def search_group_from_registered_goal():\n"
        "    if proof_order_catalog is None:\n"
        "        proof_order_catalog, order_diagnostic = query()\n"
        + ORDER_BRANCH + END_BRANCH
    ).encode()


@pytest.mark.parametrize("eol", ("\n", "\r\n"))
def test_model_transform_preserves_eol_and_adds_entire_class(eol: str) -> None:
    changed = transform_model(source_model().replace(b"\n", eol.encode()))
    text = changed.decode()
    assert "class CertifiedAbstractStructure:" in text
    assert MODEL_FIELD.strip() in text
    assert "from proof import ProofRule, ProofStep" in text
    assert (b"\r\n" in changed) == (eol == "\r\n")
    ast.parse(text)


@pytest.mark.parametrize("eol", ("\n", "\r\n"))
def test_selector_transform_preserves_eol_and_existing_goal_selection(eol: str) -> None:
    changed = transform_selector(source_selector().replace(b"\n", eol.encode()))
    text = changed.decode()
    assert "attach_certified_abstract_structure" in text
    assert "if n == 4 and k >= 3:" in text
    assert "result.status is ProofSearchStatus.COMPLETE" in text
    assert "return result" in text
    assert (b"\r\n" in changed) == (eol == "\r\n")
    ast.parse(text)


def test_missing_model_guard_refuses_unreviewed_source() -> None:
    with pytest.raises(RuntimeError, match="anchor"):
        transform_model(source_model().replace(b"from proof import ProofStep", b"from proof import Other"))


def test_duplicate_model_refuses_install() -> None:
    with pytest.raises(RuntimeError, match="already"):
        transform_model(source_model().replace(
            b"@dataclass(frozen=True)\nclass PartialProofResult:",
            b"@dataclass(frozen=True)\nclass CertifiedAbstractStructure:\n"
            b"    pass\n@dataclass(frozen=True)\nclass PartialProofResult:",
        ))


def test_selector_rejects_a_rewritten_end_branch() -> None:
    with pytest.raises(RuntimeError, match="anchor"):
        transform_selector(source_selector().replace(END_BRANCH.encode(), b"    return None\n"))


def test_selector_rejects_a_rewritten_order_branch() -> None:
    with pytest.raises(RuntimeError, match="anchor"):
        transform_selector(source_selector().replace(ORDER_BRANCH.encode(), b"    return None\n"))


def test_gating_retains_original_complete_condition() -> None:
    assert END_REPLACEMENT.startswith("    if result.status is ProofSearchStatus.COMPLETE")
    assert ORDER_REPLACEMENT.count("if n == 4 and k >= 3:") == 1


def test_transforms_are_not_double_applied() -> None:
    with pytest.raises(RuntimeError):
        transform_model(transform_model(source_model()))
    with pytest.raises(RuntimeError):
        transform_selector(transform_selector(source_selector()))
