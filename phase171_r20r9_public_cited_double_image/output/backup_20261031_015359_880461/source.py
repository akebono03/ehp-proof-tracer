"""Typed equality substitution from a cited relation and a proved E-image.

This module defines an inference schema, not an additional literature axiom.
Neither its constructor nor its expansion certifies a database group goal.
"""
from __future__ import annotations

from expression import MapApplication, Multiple
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_E_MAP
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e5_composite_generator_image.rule import _endpoints
from proof import (
    InferenceRule,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)


def typed_double_image_conclusion(
    relation: object, image: object,
) -> Relation | None:
    """Return a typed substitution, but only for a matching suspension image.

    For a cited equality m*a=b and an inferred E(x)=b this constructs
    m*a=E(x). The object equality of b includes its full composition tree;
    display text and aliases alone are not accepted.
    """
    if (
        not isinstance(relation, Relation)
        or relation.relation_type is not RelationType.EQUALITY
        or not isinstance(relation.lhs, Multiple)
        or type(relation.lhs.coefficient) is not int
        or relation.lhs.coefficient <= 0
        or not isinstance(image, GeneratorImage)
        or not isinstance(image.map, TodaSuspensionMap)
        or relation.rhs != image.target_generator
    ):
        return None
    src = _endpoints(image.source_generator)
    dst = _endpoints(image.target_generator)
    left = _endpoints(relation.lhs.expression)
    if (
        src is None
        or dst is None
        or left is None
        or left != dst
        or dst != (src[0] + 1, src[1] + 1)
        or image.map.source_group != TodaPrimaryGroup(*src)
        or image.map.target_group != TodaPrimaryGroup(*dst)
    ):
        return None
    return Relation(
        lhs=relation.lhs,
        rhs=MapApplication(EHP_E_MAP, image.source_generator),
        relation_type=RelationType.EQUALITY,
    )


def typed_double_image_rule(
    relation: Relation, image: GeneratorImage,
) -> InferenceRule:
    """Require exactly one cited GIVEN and one independently inferred image."""
    target = typed_double_image_conclusion(relation, image)
    if target is None:
        raise ValueError("source equality and inferred generator image are not type-compatible")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and not premises[0].premises
            and premises[1].rule is ProofRule.INFERENCE
            and premises[0].conclusion == relation
            and premises[1].conclusion == image
            and typed_double_image_conclusion(relation, image) == target
        )

    return InferenceRule(
        name="substitute independently proved typed suspension image into cited equality",
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=relation,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=image,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=target,
    )
