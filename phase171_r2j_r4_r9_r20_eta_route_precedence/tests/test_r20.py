"""Focused R20 tests: provider precedence, provenance and canonical proof."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r57_r20_general_specialization import expand_cited_general_specialization
from phase165_r57_r8_eta_specialization import expand_registered_eta_specialization
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit import cardinality_route, probe_premise
from phase171_r2j_r4_r9_r20_eta_route_precedence.install import (
    ORIGINAL, REPLACEMENT, git_read, patch_text, source_function,
)
from phase171_r2j_r4_r9_r20_eta_route_precedence.source import (
    ETA_RULE, SCALAR_RULE, prefer_specific_cited_eta_specialization,
)
from homotopy_groups import TodaPrimaryGroup
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from proof import ProofRule


@dataclass(frozen=True)
class FakeRule:
    name: str


def test_does_not_suppress_unverified_or_different_source():
    generic = GoalExpansion(FakeRule(SCALAR_RULE), ("unverified",))
    specific = GoalExpansion(FakeRule(ETA_RULE), ("unverified",))
    assert prefer_specific_cited_eta_specialization(object(), (), (generic, specific)) == (generic, specific)
    with pytest.raises(TypeError):
        prefer_specific_cited_eta_specialization(object(), [], (generic,))
    with pytest.raises(TypeError):
        prefer_specific_cited_eta_specialization(object(), (), [generic])


def test_source_bounded_eta_precedence_on_real_registered_general_source():
    screened, root, _ = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    order = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    right = cardinality_route(provider, order).subgoals[2]
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    specific = expand_registered_eta_specialization(right, available)
    generic = expand_cited_general_specialization(right, available)
    assert len(specific) == len(generic) == 1
    assert specific[0].subgoals == generic[0].subgoals
    output = prefer_specific_cited_eta_specialization(
        right, available, generic + specific,
    )
    assert output == specific


def test_unrelated_scalar_specialization_not_suppressed():
    screened, root, _ = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    right = cardinality_route(provider, FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)).subgoals[2]
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    specific, = expand_registered_eta_specialization(right, available)
    generic, = expand_cited_general_specialization(right, available)
    unrelated = GoalExpansion(generic.rule, (object(),))
    observed = prefer_specific_cited_eta_specialization(right, available, (generic, specific, unrelated))
    assert observed == (specific, unrelated)


def test_shared_provider_keeps_only_unique_specific_eta_route():
    screened, root, _ = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    right = cardinality_route(provider, FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)).subgoals[2]
    names = [item.rule.name for item in provider(right)]
    assert names.count(ETA_RULE) == 1
    assert names.count(SCALAR_RULE) == 0


def test_right_group_is_inferred_with_real_cited_source():
    screened, root, citing = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    right = cardinality_route(provider, FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)).subgoals[2]
    observed, step = probe_premise(right, provider, screened, citing, root)
    assert observed["status"] == "proved"
    assert step.rule is ProofRule.INFERENCE
    assert observed["source_ids"]


def test_cardinality_is_inferred_without_importing_completed_proof():
    screened, root, citing = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    cardinality = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    observed, step = probe_premise(cardinality, provider, screened, citing, root)
    assert observed["status"] == "proved", observed["error"]
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == cardinality
    assert observed["source_ids"]


def test_guarded_installation_changes_exactly_one_complete_function():
    original = git_read("show", "HEAD:phase165_r52_r9_shared_math.py").decode("utf-8-sig").replace("\r\n", "\n")
    altered = patch_text(original)
    assert altered != original
    assert altered.count(REPLACEMENT) == 1
    assert altered.replace(REPLACEMENT, ORIGINAL) == original
    assert "def shared_expansion_provider(" in source_function(altered)
    assert "prefer_specific_cited_eta_specialization(" in source_function(altered)
    assert patch_text(altered) == altered
