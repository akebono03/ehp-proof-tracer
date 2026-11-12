"""R3R2 focused, typed contracts for source-bound subgoal separation."""
from __future__ import annotations

import pytest

pytest.importorskip("phase165_r3_recursive_search")

from phase165_r3_recursive_search import (
    GoalExpansion,
    RegisteredGoalUnresolved,
    SourceBoundGoal,
)
from phase175_r3_pi73_hopf_lift import frontier
from phase175_r3_pi73_hopf_lift.rule import RULE_NAME
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType


def sample():
    first, last = "hopf-injective", "hopf-image-equality"
    codomain = Relation("pi_codomain", "Z2-generator", RelationType.EQUALITY)
    source = Relation("earlier-universal-group", "group-schema", RelationType.EQUALITY)
    rule = InferenceRule(name=RULE_NAME)
    proposal = GoalExpansion(rule, (first, codomain, last))
    return proposal, source


def test_source_bound_replaces_only_codomain_subgoal(monkeypatch) -> None:
    proposal, source = sample()
    monkeypatch.setattr(
        frontier, "_eligible_group_instance",
        lambda possible, actual: possible == source and actual == proposal.subgoals[1],
    )
    candidate = frontier.source_bound_hopf_codomain(proposal, (source,))
    assert isinstance(candidate, GoalExpansion)
    assert candidate.rule is proposal.rule
    assert candidate.subgoals[0] == proposal.subgoals[0]
    assert candidate.subgoals[2] == proposal.subgoals[2]
    bound = candidate.subgoals[1]
    assert bound == SourceBoundGoal(proposal.subgoals[1], source)
    assert all(not isinstance(value, ProofStep) for value in candidate.subgoals)


def test_missing_cited_source_does_not_produce_bound_candidate(monkeypatch) -> None:
    proposal, source = sample()
    monkeypatch.setattr(frontier, "_eligible_group_instance", lambda a, b: False)
    assert frontier.source_bound_hopf_codomain(proposal, (source,)) is None
    assert frontier.source_bound_hopf_codomain(proposal, ()) is None


def test_ambiguous_cited_sources_are_rejected(monkeypatch) -> None:
    proposal, source = sample()
    second = Relation("another-earlier", "schema", RelationType.EQUALITY)
    monkeypatch.setattr(frontier, "_eligible_group_instance", lambda a, b: True)
    assert frontier.source_bound_hopf_codomain(proposal, (source, second)) is None


def test_unrelated_rule_cannot_be_source_bound(monkeypatch) -> None:
    proposal, source = sample()
    monkeypatch.setattr(frontier, "_eligible_group_instance", lambda a, b: True)
    unrelated = GoalExpansion(InferenceRule("unrelated rule"), proposal.subgoals)
    assert frontier.source_bound_hopf_codomain(unrelated, (source,)) is None


def test_malformed_or_non_cyclic_candidate_rejected() -> None:
    proposal, _ = sample()
    assert frontier.source_bound_hopf_codomain(proposal, "not a tuple") is None
    malformed = GoalExpansion(proposal.rule, ("one", "two"))
    assert frontier.source_bound_hopf_codomain(malformed, ()) is None


def test_independent_obligation_inferred_without_synthetic_given(monkeypatch) -> None:
    goal = "actual-mathematical-goal"
    parent = ProofStep("earlier mathematical premise", (), ProofRule.GIVEN)
    first = ProofStep(goal, (parent,), ProofRule.INFERENCE, inference_rule=InferenceRule("inferred"))

    def search(target, screened, citing_id, provider, **kwargs):
        assert target == goal
        assert citing_id == "earlier-citing-id"
        assert kwargs["lookup_mode"] == "typed_reference_publication"
        kwargs["progress_observer"]("proved", target, first)
        return first

    monkeypatch.setattr(frontier, "reconstruct_registered_goal", search)
    route = GoalExpansion(InferenceRule("test source-only route"), ("earlier-source",))
    result = frontier.inspect_independent_obligation(
        "hopf_injectivity", goal, object(), "earlier-citing-id",
        lambda value: (route,),
    )
    assert result["status"] == "INFERRED"
    assert result["actual_proof_rule"] == "inference"
    assert result["offered_routes"] == 1
    assert result["observed_proved"] == [repr(goal)]


def test_empty_inference_cannot_be_counted_as_independently_proved(monkeypatch) -> None:
    goal = "an unsupported mathematical result"
    monkeypatch.setattr(
        frontier, "reconstruct_registered_goal",
        lambda *args, **kwargs: ProofStep(goal, (), ProofRule.INFERENCE),
    )
    result = frontier.inspect_independent_obligation(
        "hopf", goal, object(), "citing", lambda value: (),
    )
    assert result["status"] == "UNBACKED_INFERENCE_REJECTED"
    assert result["actual_premise_count"] == 0

def test_direct_given_is_not_accepted_as_inferred_premise(monkeypatch) -> None:
    goal = "earlier database result"
    monkeypatch.setattr(
        frontier, "reconstruct_registered_goal",
        lambda *args, **kwargs: ProofStep(goal, (), ProofRule.GIVEN),
    )
    result = frontier.inspect_independent_obligation(
        "cyclic_codomain", goal, object(), "citing", lambda value: (),
    )
    assert result["status"] == "DIRECT_GIVEN_NOT_ACCEPTABLE"
    assert result["actual_premise_count"] == 0


def test_source_bound_obligation_is_passed_as_source_bound_goal(monkeypatch) -> None:
    proposal, source = sample()
    bound = SourceBoundGoal(proposal.subgoals[1], source)

    def search(target, screened, citing_id, provider, **kwargs):
        assert target is bound
        return ProofStep(target.conclusion, (ProofStep(source, (), ProofRule.GIVEN),),
                         ProofRule.INFERENCE, inference_rule=InferenceRule("specialization"))

    monkeypatch.setattr(frontier, "reconstruct_registered_goal", search)
    row = frontier.inspect_independent_obligation(
        "source_bound_cyclic_codomain", bound, object(), "citing", lambda value: (),
    )
    assert row["status"] == "INFERRED"
    assert row["source_bound"] is True


def test_unresolved_obligation_stays_unresolved(monkeypatch) -> None:
    goal = "missing mathematical fact"

    def search(target, screened, citing_id, provider, **kwargs):
        kwargs["progress_observer"]("unresolved", target, None)
        raise RegisteredGoalUnresolved("no verified derivation")

    monkeypatch.setattr(frontier, "reconstruct_registered_goal", search)
    row = frontier.inspect_independent_obligation(
        "hopf_image", goal, object(), "citing", lambda value: (),
    )
    assert row["status"] == "UNRESOLVED"
    assert row["observed_unresolved_count"] == 1
    assert "no verified derivation" in row["diagnostic"]


def test_invalid_provider_is_rejected_without_asserting_a_proof() -> None:
    with pytest.raises(TypeError, match="provider contract"):
        frontier.inspect_independent_obligation(
            "x", "goal", object(), "citing", lambda actual: ["invalid"],
        )
