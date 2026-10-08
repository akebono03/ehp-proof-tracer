"""Phase 161 R3: concrete EHP backward goal expansion, without proof execution."""

from homotopy_groups import (
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase161_backward_goal_schema import (
    BackwardGoalExpansion,
    expand_phase161_r2_suspension_isomorphism_goal,
)
from toda_rules import (
    TodaDeltaInjectiveStatement,
    TodaDeltaZeroStatement,
    TodaHopfInvariantSurjectiveStatement,
    TodaHopfInvariantZeroStatement,
    TodaProp42ExactnessStatement,
    TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
    toda_53_n3_delta_injective_hopf_zero_inference_rule,
    toda_53_n3_delta_zero_suspension_injective_inference_rule,
    toda_53_n3_hopf_surjective_delta_zero_inference_rule,
    toda_53_n3_hopf_zero_suspension_surjective_inference_rule,
)


_PI_3_2 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
_PI_4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
_PI_5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
_PI_5_5 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
_PI_6_3 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
_PI_6_5 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)

_E = TodaSuspensionMap(source_group=_PI_4_2, target_group=_PI_5_3)
_H5 = TodaHopfInvariantMap(source_group=_PI_5_3, target_group=_PI_5_5)
_H6 = TodaHopfInvariantMap(source_group=_PI_6_3, target_group=_PI_6_5)
_DELTA5 = TodaDeltaMap(source_group=_PI_5_5, target_group=_PI_3_2)
_DELTA6 = TodaDeltaMap(source_group=_PI_6_5, target_group=_PI_4_2)


def _exactness(source, middle, target, first_map, second_map):
    return TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
            source_term=source,
            middle_term=middle,
            target_term=target,
            first_map=first_map,
            second_map=second_map,
        )
    )


def expand_phase161_r3_ehp_goal(goal: object) -> BackwardGoalExpansion | None:
    """Expand the four concrete EHP consequences; leave literature goals unresolved.

    The second subgoal is always the independently required exactness statement.
    No ProofStep is created and no GIVEN or INFERENCE provenance is invented.
    """
    cases = (
        (
            TodaSuspensionInjectiveStatement(map=_E),
            toda_53_n3_delta_zero_suspension_injective_inference_rule,
            TodaDeltaZeroStatement(map=_DELTA6),
            _exactness(_PI_6_5, _PI_4_2, _PI_5_3, EHP_DELTA_MAP, EHP_E_MAP),
        ),
        (
            TodaDeltaZeroStatement(map=_DELTA6),
            toda_53_n3_hopf_surjective_delta_zero_inference_rule,
            TodaHopfInvariantSurjectiveStatement(map=_H6),
            _exactness(_PI_6_3, _PI_6_5, _PI_4_2, EHP_H_MAP, EHP_DELTA_MAP),
        ),
        (
            TodaSuspensionSurjectiveStatement(map=_E),
            toda_53_n3_hopf_zero_suspension_surjective_inference_rule,
            TodaHopfInvariantZeroStatement(map=_H5),
            _exactness(_PI_4_2, _PI_5_3, _PI_5_5, EHP_E_MAP, EHP_H_MAP),
        ),
        (
            TodaHopfInvariantZeroStatement(map=_H5),
            toda_53_n3_delta_injective_hopf_zero_inference_rule,
            TodaDeltaInjectiveStatement(map=_DELTA5),
            _exactness(_PI_5_3, _PI_5_5, _PI_3_2, EHP_H_MAP, EHP_DELTA_MAP),
        ),
    )
    for expected_goal, factory, property_goal, exactness_goal in cases:
        if goal != expected_goal or type(goal) is not type(expected_goal):
            continue
        rule = factory()
        expected_types = (type(property_goal), TodaProp42ExactnessStatement)
        if tuple(p.statement_type for p in rule.premise_patterns) != expected_types:
            raise RuntimeError(f"Production premise types changed: {rule.name}")
        if rule.premise_patterns[0].proof_rule is None:
            raise RuntimeError(f"Production requires derived property: {rule.name}")
        if rule.conclusion_builder is None or rule.match_guard is None:
            raise RuntimeError(f"Production inference contract changed: {rule.name}")
        return BackwardGoalExpansion(
            goal=goal,
            inference_rule=rule,
            subgoals=(property_goal, exactness_goal),
        )
    return None


def expand_phase161_r3_goal(goal: object) -> BackwardGoalExpansion | None:
    """Compose the R2 root step with the four R3 EHP expansion cases."""
    root_expansion = expand_phase161_r2_suspension_isomorphism_goal(goal)
    if root_expansion is not None:
        return root_expansion
    return expand_phase161_r3_ehp_goal(goal)
