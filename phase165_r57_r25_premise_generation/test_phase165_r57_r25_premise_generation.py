"""R25 focused tests: goal-to-subgoal instantiation, not proof search."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from phase165_r57_r24_candidate_discovery import (
    DiscoveredRuleCandidate,
    discover_explicit_goal_candidates,
)
from phase165_r57_r25_premise_generation import (
    generate_candidate_premises,
    generate_discovered_premises,
)
from proof import InferenceRule, PatternVariable, PremisePattern, Relation, RelationType


@dataclass(frozen=True)
class TypedClaim:
    subject: object
    evidence: object


def _candidate(rule: InferenceRule, goal: object):
    found = discover_explicit_goal_candidates((rule,), goal)
    assert len(found) == 1
    return found[0]


def test_r25_builds_nested_typed_premise_from_bound_goal():
    x = PatternVariable("x")
    rule = InferenceRule(
        name="typed rule",
        conclusion_pattern=TypedClaim(x, "established"),
        premise_patterns=(PremisePattern(statement_pattern=TypedClaim(x, "known")),),
    )
    result = generate_candidate_premises(_candidate(rule, TypedClaim("group", "established")))
    assert result is not None
    assert result.expansion.rule is rule
    assert result.expansion.subgoals == (TypedClaim("group", "known"),)


def test_r25_instantiates_nested_relation_and_tuple():
    x = PatternVariable("x")
    rule = InferenceRule(
        name="nested rule",
        conclusion_pattern=TypedClaim(x, "done"),
        premise_patterns=(PremisePattern(statement_pattern=TypedClaim(
            Relation(x, "Z", RelationType.EQUALITY), (x, "source")
        )),),
    )
    result = generate_candidate_premises(_candidate(rule, TypedClaim("pi", "done")))
    assert result is not None
    assert result.expansion.subgoals == (
        TypedClaim(Relation("pi", "Z", RelationType.EQUALITY), ("pi", "source")),
    )


def test_r25_preserves_premise_order_and_duplicates():
    x = PatternVariable("x")
    first = PremisePattern(statement_pattern=TypedClaim(x, "first"))
    rule = InferenceRule(
        name="ordered rule", conclusion_pattern=TypedClaim(x, "done"),
        premise_patterns=(first, first, PremisePattern(statement_pattern=TypedClaim(x, "last"))),
    )
    result = generate_candidate_premises(_candidate(rule, TypedClaim("pi", "done")))
    assert result is not None
    assert result.expansion.subgoals == (
        TypedClaim("pi", "first"), TypedClaim("pi", "first"), TypedClaim("pi", "last")
    )


def test_r25_refuses_unbound_witness_variable():
    x, witness = PatternVariable("x"), PatternVariable("witness")
    rule = InferenceRule(
        name="unbound", conclusion_pattern=TypedClaim(x, "done"),
        premise_patterns=(PremisePattern(statement_pattern=TypedClaim(x, witness)),),
    )
    assert generate_candidate_premises(_candidate(rule, TypedClaim("pi", "done"))) is None


def test_r25_refuses_missing_premise_template_and_no_premises():
    x = PatternVariable("x")
    for premises in ((), (PremisePattern(statement_type=TypedClaim),)):
        rule = InferenceRule("missing", conclusion_pattern=TypedClaim(x, "done"), premise_patterns=premises)
        assert generate_candidate_premises(_candidate(rule, TypedClaim("pi", "done"))) is None


def test_r25_rejects_mismatched_premise_metadata():
    x = PatternVariable("x")
    mismatched_type = InferenceRule(
        "bad type", conclusion_pattern=TypedClaim(x, "done"),
        premise_patterns=(PremisePattern(statement_type=Relation, statement_pattern=TypedClaim(x, "known")),),
    )
    mismatched_relation = InferenceRule(
        "bad relation", conclusion_pattern=TypedClaim(x, "done"),
        premise_patterns=(PremisePattern(relation_type=RelationType.ZERO,
                                         relation_pattern=Relation(x, "Z", RelationType.EQUALITY)),),
    )
    for rule in (mismatched_type, mismatched_relation):
        assert generate_candidate_premises(_candidate(rule, TypedClaim("pi", "done"))) is None


def test_r25_batch_skips_noninvertible_without_inventing_premises():
    x = PatternVariable("x")
    good = InferenceRule("good", conclusion_pattern=TypedClaim(x, "done"),
                         premise_patterns=(PremisePattern(statement_pattern=TypedClaim(x, "source")),))
    bad = InferenceRule("bad", conclusion_pattern=TypedClaim(x, "done"),
                        premise_patterns=(PremisePattern(statement_pattern=TypedClaim(PatternVariable("unknown"), "source")),))
    candidates = discover_explicit_goal_candidates((bad, good), TypedClaim("pi", "done"))
    result = generate_discovered_premises(candidates)
    assert len(result) == 1
    assert result[0].key == candidates[1].key
    assert result[0].expansion.subgoals == (TypedClaim("pi", "source"),)


def test_r25_invalid_arguments_are_rejected():
    with pytest.raises(TypeError):
        generate_candidate_premises(object())
    with pytest.raises(TypeError):
        generate_discovered_premises([])
    with pytest.raises(TypeError):
        generate_discovered_premises((object(),))


def test_r25_never_creates_given_or_proof_step():
    x = PatternVariable("x")
    rule = InferenceRule("safe", conclusion_pattern=TypedClaim(x, "done"),
                         premise_patterns=(PremisePattern(statement_pattern=TypedClaim(x, "known")),))
    result = generate_candidate_premises(_candidate(rule, TypedClaim("pi", "done")))
    assert result is not None
    assert not hasattr(result, "proof_step")
    assert not hasattr(result.expansion, "proof_step")
