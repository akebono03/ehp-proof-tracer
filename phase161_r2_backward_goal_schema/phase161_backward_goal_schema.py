"""Phase 161 R2: target-specific backwards selection, not proof construction."""

from dataclasses import dataclass

from homotopy_groups import (
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from proof import InferenceRule
from toda_rules import (
    TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
    toda_53_n3_suspension_isomorphism_inference_rule,
)


@dataclass(frozen=True)
class BackwardGoalExpansion:
    goal: object
    inference_rule: InferenceRule
    subgoals: tuple[object, ...]


_PHASE161_R2_MAP = TodaSuspensionMap(
    source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
    target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
)


def expand_phase161_r2_suspension_isomorphism_goal(goal: object) -> BackwardGoalExpansion | None:
    """Expand only the concrete n=3 rule's valid conclusion into its two premises.

    Returns None for unsupported goals. This does not create proof steps,
    invoke a conclusion builder, or treat an unproved goal as a premise.
    """
    if not isinstance(goal, TodaSuspensionIsomorphismStatement):
        return None
    if goal.map != _PHASE161_R2_MAP:
        return None

    rule = toda_53_n3_suspension_isomorphism_inference_rule()
    if len(rule.premise_patterns) != 2:
        raise RuntimeError("Unexpected isomorphism production premise count")
    expected_types = (
        TodaSuspensionInjectiveStatement,
        TodaSuspensionSurjectiveStatement,
    )
    actual_types = tuple(pattern.statement_type for pattern in rule.premise_patterns)
    if actual_types != expected_types:
        raise RuntimeError("Existing isomorphism production premise types changed")
    if rule.conclusion_builder is None or rule.match_guard is None:
        raise RuntimeError("Existing isomorphism production contract changed")

    return BackwardGoalExpansion(
        goal=goal,
        inference_rule=rule,
        subgoals=(
            TodaSuspensionInjectiveStatement(map=goal.map),
            TodaSuspensionSurjectiveStatement(map=goal.map),
        ),
    )
