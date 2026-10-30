"""Focused proof-rule and source-bound checks for the second cited Hopf map."""
from __future__ import annotations

from types import SimpleNamespace
from dataclasses import replace

import pytest

from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    SourceBoundGoal,
    reconstruct_registered_goal,
)
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r4_source_bound_hopf.audit import hopf_goal as first_hopf_goal
from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit import (
    _git,
    audit_second_source_bound_hopf,
    build_second_bound_context,
)
from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.source import bind_cited_hopf_codomain
from proof import ProofRule


@pytest.fixture(scope="module")
def context():
    return build_second_bound_context()


def test_second_hopf_has_one_source_bound_inferred_codomain(context):
    _, _, _, provider, bound, source_id, hopf = context
    assert isinstance(bound, SourceBoundGoal)
    assert isinstance(source_id, str) and source_id
    assert hopf != first_hopf_goal()
    options = provider(hopf)
    assert len(options) == 1
    assert options[0].subgoals[0] == bound
    assert options[0].subgoals[1] != bound


def test_reconstructs_codomain_as_inference_from_one_screened_source(context):
    screened, _, citing, provider, bound, _, _ = context
    step = reconstruct_registered_goal(
        bound, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == bound.conclusion
    assert len(step.premises) == 1
    assert step.premises[0].rule is ProofRule.GIVEN
    assert step.premises[0].conclusion == bound.source


def test_second_hopf_reconstructs_inference_given_pair(context):
    screened, _, citing, provider, bound, _, hopf = context
    step = reconstruct_registered_goal(
        hopf, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == hopf
    assert [item.rule for item in step.premises] == [ProofRule.INFERENCE, ProofRule.GIVEN]
    assert step.premises[0].conclusion == bound.conclusion


def test_first_hopf_remains_two_inferences(context):
    screened, _, citing, provider, _, _, _ = context
    step = reconstruct_registered_goal(
        first_hopf_goal(), screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert step.rule is ProofRule.INFERENCE
    assert len(step.premises) == 2
    assert all(item.rule is ProofRule.INFERENCE for item in step.premises)


def test_forged_source_cannot_prove_bound_group(context):
    screened, _, citing, provider, bound, _, _ = context
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            SourceBoundGoal(bound.conclusion, "invented source"),
            screened, citing, provider,
            lookup_mode="typed_reference_publication",
        )


def test_missing_earlier_screened_source_fails_closed(context):
    screened, _, citing, provider, _, _, _ = context
    root, _, _ = build_cyclic_pi63_proof()
    fake = SimpleNamespace(proof_links=(), registry=screened.registry)
    with pytest.raises(ValueError, match="unique screened"):
        bind_cited_hopf_codomain(
            root, fake, citing, provider,
            expected_locator="Proposition 5.1",
        )


def test_mismatched_locator_fails_closed(context):
    screened, _, citing, provider, _, _, _ = context
    root, _, _ = build_cyclic_pi63_proof()
    with pytest.raises(ValueError, match="unique screened"):
        bind_cited_hopf_codomain(
            root, screened, citing, provider,
            expected_locator="unrelated source",
        )


def test_other_hopf_goal_is_not_rewritten(context):
    _, _, _, provider, _, _, second_hopf = context
    wrong = replace(second_hopf, map=replace(
        second_hopf.map, target_group=second_hopf.map.source_group,
    ))
    assert provider(wrong) != provider(second_hopf)


def test_git_guard_blocks_writes():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_live_audit_has_two_genuine_inferred_hopf_goals():
    report = audit_second_source_bound_hopf()
    assert report["bound_group_inferred"] is True
    assert report["second_hopf_surjective_inferred"] is True
    assert report["first_hopf_preserved"] is True
    assert report["second_hopf_premise_rules"] == ["inference", "given"]
    assert report["new_given_added"] == 0
    assert report["public_provider_modified"] is False
    assert report["public_web_verified"] is False
    assert report["scoped_search_status"] in ("complete", "partial", "search_failed")
    if report["trust_boundary_accepted"]:
        assert report["scoped_search_complete"] is True
