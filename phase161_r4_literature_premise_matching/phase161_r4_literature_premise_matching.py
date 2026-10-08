"""Phase 161 R4: match existing proven literature premises for two terminal goals.

This module does not synthesize LiteratureStatement, ProofStep, or GIVEN steps.
"""

from dataclasses import dataclass
from itertools import product

from homotopy_groups import (
    TodaDeltaMap,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
)
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType
from toda_rules import (
    TodaDeltaInjectiveStatement,
    TodaHopfInvariantSurjectiveStatement,
    TodaProp51FiniteDimensionalStatement,
    toda_53_n3_hopf_eta5_surjective_inference_rule,
    toda_53_n3_prop51_delta_injective_inference_rule,
)


_PI_3_2 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
_PI_5_5 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
_PI_6_3 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
_PI_6_5 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)


@dataclass(frozen=True)
class BackwardPremiseRequirement:
    """An unmet premise specification; deliberately not a mathematical claim."""

    statement_type: type
    proof_rule: ProofRule | None
    relation_type: RelationType | None


@dataclass(frozen=True)
class BackwardLiteratureGoal:
    goal: object
    inference_rule: InferenceRule
    requirements: tuple[BackwardPremiseRequirement, ...]


@dataclass(frozen=True)
class BackwardLiteratureMatch:
    """Existing proof witnesses, not a newly derived conclusion."""

    plan: BackwardLiteratureGoal
    premises: tuple[ProofStep, ...]


def expand_phase161_r4_literature_goal(goal: object) -> BackwardLiteratureGoal | None:
    """Return exact Production premise contracts for the two n=3 terminal goals."""
    cases = (
        (
            TodaDeltaInjectiveStatement(
                map=TodaDeltaMap(source_group=_PI_5_5, target_group=_PI_3_2)
            ),
            toda_53_n3_prop51_delta_injective_inference_rule,
            (TodaProp51FiniteDimensionalStatement,),
        ),
        (
            TodaHopfInvariantSurjectiveStatement(
                map=TodaHopfInvariantMap(source_group=_PI_6_3, target_group=_PI_6_5)
            ),
            toda_53_n3_hopf_eta5_surjective_inference_rule,
            (Relation, TodaProp51FiniteDimensionalStatement),
        ),
    )
    for expected_goal, factory, expected_types in cases:
        if type(goal) is not type(expected_goal) or goal != expected_goal:
            continue
        rule = factory()
        patterns = rule.premise_patterns
        if tuple(p.statement_type for p in patterns) != expected_types:
            raise RuntimeError(f"Production premise types changed: {rule.name}")
        if any(p.proof_rule is not ProofRule.INFERENCE for p in patterns):
            raise RuntimeError(f"Production premise provenance changed: {rule.name}")
        if rule.conclusion_builder is None or rule.match_guard is None:
            raise RuntimeError(f"Production inference contract changed: {rule.name}")
        return BackwardLiteratureGoal(
            goal=goal,
            inference_rule=rule,
            requirements=tuple(
                BackwardPremiseRequirement(
                    statement_type=p.statement_type,
                    proof_rule=p.proof_rule,
                    relation_type=p.relation_type,
                )
                for p in patterns
            ),
        )
    return None


def match_phase161_r4_existing_premises(
    plan: BackwardLiteratureGoal, available_steps: tuple[ProofStep, ...]
) -> tuple[BackwardLiteratureMatch, ...]:
    """Select only existing inference steps accepted by the actual Production rule.

    Both the complete guard and the actual conclusion builder must agree.
    No ProofStep or premise fact is manufactured by this function.
    """
    if not isinstance(plan, BackwardLiteratureGoal):
        raise TypeError("plan must be BackwardLiteratureGoal")
    if not isinstance(available_steps, tuple) or any(
        not isinstance(step, ProofStep) for step in available_steps
    ):
        raise TypeError("available_steps must be a tuple of ProofStep")
    candidates = []
    for requirement in plan.requirements:
        candidates.append(
            tuple(
                step
                for step in available_steps
                if (requirement.proof_rule is None or step.rule is requirement.proof_rule)
                and isinstance(step.conclusion, requirement.statement_type)
                and (
                    requirement.relation_type is None
                    or (
                        isinstance(step.conclusion, Relation)
                        and step.conclusion.relation_type is requirement.relation_type
                    )
                )
            )
        )
    matches = []
    for premises in product(*candidates):
        if len(set(map(id, premises))) != len(premises):
            continue
        if not plan.inference_rule.match_guard(premises, ()):
            continue
        if plan.inference_rule.conclusion_builder(premises) != plan.goal:
            continue
        matches.append(BackwardLiteratureMatch(plan=plan, premises=premises))
    return tuple(matches)
