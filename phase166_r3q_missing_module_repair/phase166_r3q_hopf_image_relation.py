"""Convert a proved Hopf generator image to a typed equality (never a new source)."""
from __future__ import annotations

from expression import HomotopyElement, MapApplication
from homotopy_groups import TodaHopfInvariantMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, Relation, RelationType


def _compatible_element(printed: HomotopyElement, typed: HomotopyElement) -> bool:
    """Allow omitted homotopy-domain metadata, but never contradictory metadata."""
    return (
        printed.dimension == typed.dimension
        and printed.generator == typed.generator
        and (printed.source is None or printed.source == typed.source)
        and (printed.target is None or printed.target == typed.target)
    )


def _is_image_equality(goal: object, image: object) -> bool:
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return False
    if not isinstance(image, GeneratorImage) or not isinstance(image.map, TodaHopfInvariantMap):
        return False
    lhs = goal.lhs
    if not isinstance(lhs, MapApplication) or not isinstance(lhs.expression, HomotopyElement):
        return False
    if getattr(lhs.map, "name", None) != "H" or not isinstance(goal.rhs, HomotopyElement):
        return False
    if lhs.expression != image.source_generator:
        return False
    if not isinstance(image.target_generator, HomotopyElement):
        return False
    source = image.map.source_group
    target = image.map.target_group
    if (source.group_dimension != lhs.expression.source
            or source.sphere_dimension != lhs.expression.target
            or target.group_dimension != image.target_generator.source
            or target.sphere_dimension != image.target_generator.target):
        return False
    return _compatible_element(goal.rhs, image.target_generator)


def hopf_image_relation_rule(goal: Relation) -> InferenceRule:
    """An equality is a consequence of the fully typed generator-image fact."""
    def guard(premises, bindings):
        return len(premises) == 1 and _is_image_equality(goal, premises[0].conclusion)

    return InferenceRule(
        name="typed Hopf generator image yields equality",
        premise_patterns=(PremisePattern(statement_type=GeneratorImage),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_hopf_image_relation(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """Offer only image premises supplied by the screened reference context."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not isinstance(goal, Relation):
        return ()
    images = []
    for value in available:
        if _is_image_equality(goal, value) and value not in images:
            images.append(value)
    return tuple(GoalExpansion(hopf_image_relation_rule(goal), (image,)) for image in images)
