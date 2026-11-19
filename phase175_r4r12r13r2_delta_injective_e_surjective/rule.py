"""Isolated, source-first general Delta injectivity and EHP E-surjectivity rules.

No new GIVEN, group fact, saved proof, or public provider is added here.
Every input remains an independently discharged backward proof goal.
"""
from __future__ import annotations

from expression import Multiple, Sum
from phase175_r4r12r13r7_typed_nu_prime_notation.notation import (
    same_typed_generator_notation,
)
from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_E_MAP, EHP_H_MAP, EHP_DELTA_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement, TodaProp42ExactnessStatement


DELTA_RULE_NAME = "free cyclic source and nonzero free coordinate imply Delta injectivity"
E_RULE_NAME = "injective Delta and consecutive EHP exactness imply suspension surjectivity"


def _linear_coordinates(value: object, free: object, torsion: object) -> tuple[int, int] | None:
    """Accept only a literal linear combination of two listed summand generators."""
    if same_typed_generator_notation(value, free):
        return 1, 0
    if same_typed_generator_notation(value, torsion):
        return 0, 1
    if isinstance(value, Multiple) and type(value.coefficient) is int:
        pair = _linear_coordinates(value.expression, free, torsion)
        if pair is not None:
            return value.coefficient * pair[0], value.coefficient * pair[1]
    if isinstance(value, Sum):
        left = _linear_coordinates(value.left, free, torsion)
        right = _linear_coordinates(value.right, free, torsion)
        if left is not None and right is not None:
            return left[0] + right[0], left[1] + right[1]
    return None


def delta_injective_inputs(
    goal: object,
    source: object,
    target: object,
    image: object,
) -> tuple[Relation, Relation, TodaDeltaImageUpToSignStatement] | None:
    """Check a free-cyclic source and an explicitly nonzero free image coordinate.

    The signed image may be either sign: nonzero free coordinate is invariant.
    The torsion coordinate must refer to the other actual direct-sum generator.
    """
    if not isinstance(goal, MapInjective) or not isinstance(goal.map, TodaDeltaMap):
        return None
    delta = goal.map
    if not all(isinstance(g, TodaPrimaryGroup) for g in (delta.source_group, delta.target_group)):
        return None
    if not isinstance(source, Relation) or not isinstance(target, Relation):
        return None
    if source.relation_type is not RelationType.EQUALITY or target.relation_type is not RelationType.EQUALITY:
        return None
    if source.lhs != delta.source_group or target.lhs != delta.target_group:
        return None
    if not isinstance(source.rhs, FreeCyclicGroup):
        return None
    if not isinstance(target.rhs, DirectSumGroup) or len(target.rhs.summands) != 2:
        return None
    free_parts = tuple(x for x in target.rhs.summands if isinstance(x, FreeCyclicGroup))
    finite_parts = tuple(x for x in target.rhs.summands if isinstance(x, FiniteCyclicGroup))
    if len(free_parts) != 1 or len(finite_parts) != 1 or finite_parts[0].order < 1:
        return None
    if not isinstance(image, TodaDeltaImageUpToSignStatement):
        return None
    if image.map != delta or image.element != source.rhs.generator:
        return None
    pair = _linear_coordinates(
        image.positive_value, free_parts[0].generator, finite_parts[0].generator,
    )
    if pair is None or pair[0] == 0:
        return None
    return source, target, image


def delta_injective_from_free_coordinate_rule(
    goal: MapInjective,
    required: tuple[Relation, Relation, TodaDeltaImageUpToSignStatement],
) -> InferenceRule:
    """ProofStep matcher; cannot infer a result merely from candidate subgoals."""
    if delta_injective_inputs(goal, *required) is None:
        raise ValueError("invalid free-coordinate Delta injectivity inputs")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and tuple(step.conclusion for step in premises) == required
            and delta_injective_inputs(goal, *required) == required
        )

    return InferenceRule(
        name=DELTA_RULE_NAME,
        description=(
            "A map Z -> Z + Z/m is injective when its generator has a "
            "nonzero integer coordinate in the free summand."
        ),
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=required[0]),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=required[1]),
            PremisePattern(statement_type=TodaDeltaImageUpToSignStatement,
                           statement_pattern=required[2]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_delta_injective_from_free_coordinate(
    goal: object, source: object, target: object, image: object,
) -> tuple[GoalExpansion, ...]:
    required = delta_injective_inputs(goal, source, target, image)
    if required is None:
        return ()
    return (GoalExpansion(delta_injective_from_free_coordinate_rule(goal, required), required),)


def e_surjective_inputs(
    goal: object,
) -> tuple[MapInjective, TodaProp42ExactnessStatement, TodaProp42ExactnessStatement] | None:
    """Build the only matching H-Delta and E-H windows for an E map."""
    if not isinstance(goal, MapSurjective) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    suspension = goal.map
    a, b = suspension.source_group, suspension.target_group
    if not isinstance(a, TodaPrimaryGroup) or not isinstance(b, TodaPrimaryGroup):
        return None
    if any(type(v) is not int for v in (
        a.group_dimension, a.sphere_dimension, b.group_dimension, b.sphere_dimension,
    )):
        return None
    if a.group_dimension + 1 != b.group_dimension or a.sphere_dimension + 1 != b.sphere_dimension:
        return None
    c = TodaPrimaryGroup(b.group_dimension, 2 * a.sphere_dimension + 1)
    d = TodaPrimaryGroup(b.group_dimension - 2, a.sphere_dimension)
    h_delta = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=b, middle_term=c, target_term=d,
        first_map=EHP_H_MAP, second_map=EHP_DELTA_MAP,
    ))
    e_h = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=a, middle_term=b, target_term=c,
        first_map=EHP_E_MAP, second_map=EHP_H_MAP,
    ))
    if prop42_exactness_indices(h_delta) is None or prop42_exactness_indices(e_h) is None:
        return None
    return MapInjective(TodaDeltaMap(c, d)), h_delta, e_h


def e_surjective_from_delta_injective_rule(goal: MapSurjective) -> InferenceRule:
    required = e_surjective_inputs(goal)
    if required is None:
        raise ValueError("invalid EHP suspension surjectivity goal")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and e_surjective_inputs(goal) == required
        )

    return InferenceRule(
        name=E_RULE_NAME,
        description=(
            "Exact H-Delta gives im(H)=ker(Delta)=0; exact E-H then gives "
            "im(E)=ker(H)=the whole middle group."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapInjective,
                           statement_pattern=required[0]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[1]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[2]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_e_surjective_from_delta_injective(goal: object) -> tuple[GoalExpansion, ...]:
    required = e_surjective_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(e_surjective_from_delta_injective_rule(goal), required),)
