"""Focused live-source regression tests for the single pi_8^4 direct-link suppression."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
)
from phase173_r4_r7_source_first_rule.rule import checked_inputs
from phase173_r4_r7_source_first_rule.source import screened_source_first_context
from phase173_r4_r1_lemma54_source_bridge.source import ADOPTED_ASSERTION_ID
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def _context(i: int):
    bridge = build_shared_typed_bridge()
    goal = exact_prior_database_result(4, i - 4)
    assert goal is not None
    path = Path(__file__).resolve().parents[2] / "sources/toda/Toda_05_2.tex"
    result = screened_source_first_context(
        bridge, goal=goal, chapter=path.read_text(encoding="utf-8-sig"),
    )
    return bridge, goal, result


def test_pi84_selects_only_authorized_prior_db_and_retains_original_reference() -> None:
    original, goal, screened = _context(8)
    assert screened is not None
    first, second = checked_inputs(goal)
    assert first == exact_prior_database_result(3, 4)
    assert admitted_db_step(first, proof_target=goal, bridge=screened) is not None
    assert admitted_db_step(second, proof_target=goal, bridge=screened) is not None
    assert not any(link.step is not None and link.step.conclusion == first
                   for link in screened.proof_links)
    assert not any(link.step is not None and link.step.conclusion == goal
                   for link in screened.proof_links)
    assert any(assertion.content == first and
               screened.registry.reference(assertion.reference_id).locator == "Proposition 5.8"
               for assertion in screened.registry._assertions.values()
               if assertion.origin is AssertionOrigin.FIXED_STATEMENT)
    assert ADOPTED_ASSERTION_ID not in original.registry._assertions
    assert ADOPTED_ASSERTION_ID in screened.registry._assertions


@pytest.mark.parametrize("i", (9, 10))
def test_pi9_pi10_keep_existing_source_first_context(i: int) -> None:
    original, goal, screened = _context(i)
    assert screened is not None
    assert checked_inputs(goal) is not None
    assert any(link.step is not None and link.step.rule is ProofRule.GIVEN
               for link in screened.proof_links)
    assert not any(link.step is not None and link.step.conclusion == goal
                   for link in screened.proof_links)
    assert ADOPTED_ASSERTION_ID not in original.registry._assertions


def test_pi84_fails_closed_when_direct_source_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    import phase173_r4_r7_source_first_rule.source as module
    _, goal, screened = _context(8)
    assert screened is not None
    monkeypatch.setattr(module, "screen_independent_sources_for_derived_goal",
                        lambda bridge, goal: screened)
    original = build_shared_typed_bridge()
    text = (Path(__file__).resolve().parents[2] / "sources/toda/Toda_05_2.tex").read_text(
        encoding="utf-8-sig"
    )
    assert screened_source_first_context(original, goal=goal, chapter=text) is None


def test_pi84_fails_closed_when_direct_source_is_duplicated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import phase173_r4_r7_source_first_rule.source as module
    bridge, goal, screened = _context(8)
    assert screened is not None
    original_screen = module.screen_independent_sources_for_derived_goal
    def duplicated(augmented: RegistryBridgeResult, *, goal):
        context = original_screen(augmented, goal=goal)
        first = exact_prior_database_result(3, 4)
        match = tuple(link for link in context.proof_links
                      if link.step is not None and link.step.conclusion == first)
        assert len(match) == 1
        return RegistryBridgeResult(context.registry, context.records,
                                    context.proof_links + match)
    monkeypatch.setattr(module, "screen_independent_sources_for_derived_goal", duplicated)
    chapter = (Path(__file__).resolve().parents[2] / "sources/toda/Toda_05_2.tex").read_text(
        encoding="utf-8-sig"
    )
    assert screened_source_first_context(bridge, goal=goal, chapter=chapter) is None
