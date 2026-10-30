"""R9-R4: source-bound Hopf goal without bypassing the matcher or DB order."""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    SourceBoundGoal,
    reconstruct_registered_goal,
)
from phase171_r2j_r4_r9_r4_source_bound_hopf.audit import (
    _git,
    audit_source_bound_search,
    build_source_bound_context,
    hopf_goal,
    previous_hopf_match_evidence,
)
from phase171_r2j_r4_r9_r4_source_bound_hopf.source import source_bound_hopf_provider
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from proof import ProofRule


@pytest.fixture(scope="module")
def context():
    return build_source_bound_context()


def test_hopf_goal_is_unique_and_bound_to_original_group(context):
    _, _, _, provider, bound, source_id = context
    assert isinstance(bound, SourceBoundGoal)
    assert "Proposition 5.3" in source_id
    proposals = provider(hopf_goal())
    assert len(proposals) == 1
    assert proposals[0].subgoals[0] == bound
    assert proposals[0].subgoals[1] != bound


def test_cited_codomain_is_inferred_instead_of_database_given(context):
    screened, _, citing, provider, bound, _ = context
    result = reconstruct_registered_goal(
        bound, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == bound.conclusion
    assert len(result.premises) == 1
    assert result.premises[0].rule is ProofRule.GIVEN
    assert result.premises[0].conclusion == bound.source


def test_canonical_hopf_rule_reconstructs_two_inferences(context):
    screened, _, citing, provider, bound, _ = context
    result = reconstruct_registered_goal(
        hopf_goal(), screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == hopf_goal()
    assert len(result.premises) == 2
    assert all(parent.rule is ProofRule.INFERENCE for parent in result.premises)
    assert result.premises[0].conclusion == bound.conclusion


def test_fake_source_bound_is_unprovable(context):
    screened, _, citing, provider, bound, _ = context
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            SourceBoundGoal(bound.conclusion, "not a cited theorem"),
            screened, citing, provider,
            lookup_mode="typed_reference_publication",
        )


def test_wrong_hopf_target_is_not_rewritten(context):
    _, _, _, provider, _, _ = context
    wrong = replace(hopf_goal(), map=replace(
        hopf_goal().map,
        target_group=hopf_goal().map.source_group,
    ))
    assert provider(wrong) != provider(hopf_goal())


def test_missing_screened_group_source_is_rejected(context):
    screened, _, citing, _, _, _ = context
    root, _, _ = build_cyclic_pi63_proof()
    empty = SimpleNamespace(proof_links=(), registry=screened.registry)
    with pytest.raises(ValueError, match="Proposition 5.3"):
        source_bound_hopf_provider(root, empty, citing, hopf_goal(), lambda goal: ())


def test_read_only_git_commands_only():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_live_audit_keeps_public_boundary_unchanged():
    report = audit_source_bound_search()
    assert report["bound_group_inferred"] is True
    assert isinstance(report["previous_hopf_match_evidence"]["available"], bool)
    assert report["hopf_surjective_inferred"] is True
    assert report["hopf_premise_rules"] == ["inference", "inference"]
    assert report["new_given_added"] == 0
    assert report["public_provider_modified"] is False
    assert report["public_web_verified"] is False
    if report["trust_boundary_accepted"]:
        assert report["scoped_search_complete"] is True
