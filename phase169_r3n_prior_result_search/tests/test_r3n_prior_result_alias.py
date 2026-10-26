"""Focused integration tests for source-positioned DB result presentation."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, eta, nu
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase169_r3m_prior_result_catalog import prior_results
from phase169_r3n_prior_result_alias import resolve_prior_result_alias_step
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def _relation(n: int, *, ascii_name: bool) -> Relation:
    subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    left_name = f"η_{n}" if ascii_name else "η" + str(n).translate(subscript)
    right_name = f"η_{n + 1}" if ascii_name else "η" + str(n + 1).translate(subscript)
    left = HomotopyElement(
        name=left_name, dimension=n, source=n + 1, target=n,
        generator=GeneratorSymbol(family="η", index=n),
    )
    right = HomotopyElement(
        name=right_name, dimension=n + 1, source=n + 2, target=n + 1,
        generator=GeneratorSymbol(family="η", index=n + 1),
    )
    return Relation(
        TodaPrimaryGroup(n + 2, n),
        FiniteCyclicGroup(2, Composition(left, right)),
        RelationType.EQUALITY,
    )


def _context(*, source_pos=6000, target_pos=7000, linked=True, source_n=2):
    source = _relation(source_n, ascii_name=False)
    target = _relation(source_n + 1, ascii_name=False)
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "source", ReferenceKind.PROPOSITION, "Proposition A",
        publication_position=source_pos,
    ))
    registry.add_reference(LiteratureEntry(
        "target", ReferenceKind.PROPOSITION, "Proposition B",
        publication_position=target_pos,
    ))
    registry.add_assertion(AssertionEntry(
        "source_id", "source", AssertionKind.STATEMENT, source,
        origin=AssertionOrigin.FIXED_STATEMENT, component_position=100,
    ))
    registry.add_assertion(AssertionEntry(
        "target_id", "target", AssertionKind.STATEMENT, target,
        origin=AssertionOrigin.FIXED_STATEMENT, component_position=200,
    ))
    links = (ProofStepLink(
        "source_id", step=ProofStep(source, (), ProofRule.GIVEN),
    ),) if linked else ()
    return RegistryBridgeResult(registry, (), links), source


def test_r3n_prior_result_matches_alias_without_completed_proof(monkeypatch):
    bridge, original = _context()
    db = _relation(2, ascii_name=True)
    monkeypatch.setattr(prior_results, "_database_result_candidates", lambda **kwargs: (db,))
    derived = resolve_prior_result_alias_step(db, bridge, "target_id")
    assert derived is not None
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == db
    assert len(derived.premises) == 1
    assert derived.premises[0].rule is ProofRule.GIVEN
    assert derived.premises[0].conclusion == original


def test_r3n_source_without_screened_fixed_leaf_is_not_used(monkeypatch):
    bridge, _ = _context(linked=False)
    db = _relation(2, ascii_name=True)
    monkeypatch.setattr(prior_results, "_database_result_candidates", lambda **kwargs: (db,))
    assert resolve_prior_result_alias_step(db, bridge, "target_id") is None


def test_r3n_later_reference_is_not_used(monkeypatch):
    bridge, _ = _context(source_pos=8000)
    db = _relation(2, ascii_name=True)
    monkeypatch.setattr(prior_results, "_database_result_candidates", lambda **kwargs: (db,))
    assert resolve_prior_result_alias_step(db, bridge, "target_id") is None


def test_r3n_unrelated_generator_is_not_normalized(monkeypatch):
    bridge, _ = _context()
    db = _relation(2, ascii_name=True)
    monkeypatch.setattr(prior_results, "_database_result_candidates", lambda **kwargs: (db,))
    wrong = Relation(db.lhs, FiniteCyclicGroup(2, Composition(nu(2), eta(3))), RelationType.EQUALITY)
    assert resolve_prior_result_alias_step(wrong, bridge, "target_id") is None


def test_r3n_current_target_cannot_cite_itself(monkeypatch):
    bridge, _ = _context()
    db = _relation(3, ascii_name=True)
    monkeypatch.setattr(prior_results, "_database_result_candidates", lambda **kwargs: (db,))
    assert resolve_prior_result_alias_step(db, bridge, "target_id") is None


def test_r3n_prior_result_does_not_require_proof_completion(monkeypatch):
    from pathlib import Path
    source = Path(__file__).resolve().parents[1] / "new_files" / "phase169_r3n_prior_result_alias.py"
    text = source.read_text(encoding="utf-8")
    assert "CompletedInternalProof" not in text
    assert "ProofSearchStatus" not in text
    assert "proven_steps" not in text
    assert "reconstruct_registered_goal(" not in text


def test_r3n_web_pi53_still_has_a_verified_conclusion():
    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(n=3, k=2, citation_source="model", mode="narrative")
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
