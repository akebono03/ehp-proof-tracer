"""R57-R18: replace a finite cyclic generator using a proved equality.

No family-specific group result and no GIVEN proof leaf are created.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup
from proof import InferenceRule, PremisePattern, Relation, RelationType


def _matching_generator_substitution(premises, bindings):
    source, equality = (step.conclusion for step in premises)
    if not isinstance(source, Relation) or not isinstance(equality, Relation):
        return False
    if source.relation_type is not RelationType.EQUALITY or equality.relation_type is not RelationType.EQUALITY:
        return False
    if not isinstance(source.rhs, FiniteCyclicGroup):
        return False
    return source.rhs.generator == equality.rhs


def _build_generator_substitution(premises):
    source, equality = (step.conclusion for step in premises)
    return Relation(
        lhs=source.lhs,
        rhs=FiniteCyclicGroup(order=source.rhs.order, generator=equality.lhs),
        relation_type=RelationType.EQUALITY,
    )


def finite_cyclic_generator_substitution_rule():
    """Transport a finite cyclic presentation along a proved generator identity."""
    return InferenceRule(
        name="generic finite cyclic generator substitution from proved equality",
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
        ),
        match_guard=_matching_generator_substitution,
        conclusion_builder=_build_generator_substitution,
    )
