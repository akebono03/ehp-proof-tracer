"""Infer the finite cardinality of the middle group of a short exact sequence.

No fixed group result or proof leaf is created here.  This generic rule
requires independently supported finite cyclic end-group presentations.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r5_short_exact_sequence.source import EHPShortExactSequence
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


@dataclass(frozen=True)
class FiniteGroupCardinality:
    """Typed statement: the finite group has exactly ``order`` elements."""

    group: TodaPrimaryGroup
    order: int


def cardinality_from_short_exact(
    left: object, sequence: object, right: object,
) -> FiniteGroupCardinality | None:
    """Apply |B|=|A||C| only to correctly matched finite end groups.

    This function constructs a candidate conclusion.  It is not evidence;
    the inference rule additionally requires proof steps for all inputs.
    """
    if not isinstance(sequence, EHPShortExactSequence):
        return None
    if not all(
        isinstance(statement, Relation)
        and statement.relation_type is RelationType.EQUALITY
        and isinstance(statement.lhs, TodaPrimaryGroup)
        and isinstance(statement.rhs, FiniteCyclicGroup)
        and type(statement.rhs.order) is int
        and statement.rhs.order > 0
        for statement in (left, right)
    ):
        return None
    if left.lhs != sequence.source_group or right.lhs != sequence.target_group:
        return None
    if (
        sequence.injection.source_group != sequence.source_group
        or sequence.injection.target_group != sequence.middle_group
        or sequence.projection.source_group != sequence.middle_group
        or sequence.projection.target_group != sequence.target_group
    ):
        return None
    return FiniteGroupCardinality(
        group=sequence.middle_group,
        order=left.rhs.order * right.rhs.order,
    )


def finite_cardinality_from_short_exact_rule(
    goal: FiniteGroupCardinality,
) -> InferenceRule:
    """Require a short-exact INFERENCE and verified end-group statements."""
    if (
        not isinstance(goal, FiniteGroupCardinality)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or type(goal.order) is not int
        or goal.order <= 0
    ):
        raise ValueError("a positive typed finite-cardinality goal is required")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[1].rule is ProofRule.INFERENCE
            and premises[2].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and cardinality_from_short_exact(
                premises[0].conclusion,
                premises[1].conclusion,
                premises[2].conclusion,
            ) == goal
        )

    return InferenceRule(
        name="finite middle-group cardinality from short exact sequence",
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=EHPShortExactSequence,
            ),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_finite_cardinality_from_short_exact(
    goal: object,
    left: object,
    sequence: object,
    right: object,
) -> tuple[GoalExpansion, ...]:
    """Return one backward proof obligation, never a fact from a database."""
    if (
        not isinstance(goal, FiniteGroupCardinality)
        or cardinality_from_short_exact(left, sequence, right) != goal
    ):
        return ()
    return (GoalExpansion(
        finite_cardinality_from_short_exact_rule(goal),
        (left, sequence, right),
    ),)
