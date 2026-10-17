"""Bridge proved EHP surjectivity into the generic image/codomain vocabulary."""
from __future__ import annotations

from homotopy_groups import TodaSuspensionMap
from map_property_rules import ImageWholeStatement, SurjectiveMapStatement
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern


def ehp_surjective_implies_whole_image_rule() -> InferenceRule:
    """A surjective suspension map has its whole codomain as image."""
    def guard(premises, bindings):
        statement = premises[0].conclusion
        return isinstance(statement, MapSurjective) and isinstance(statement.map, TodaSuspensionMap)

    def conclude(premises):
        return ImageWholeStatement(premises[0].conclusion.map)

    return InferenceRule(
        name="EHP suspension surjectivity implies whole image",
        description="The image of a surjective suspension homomorphism equals its codomain.",
        premise_patterns=(PremisePattern(statement_type=MapSurjective),),
        match_guard=guard,
        conclusion_builder=conclude,
    )


def expand_ehp_whole_image(goal: object) -> tuple[GoalExpansion, ...]:
    """Build an unproved MapSurjective subgoal, keeping EHP ancestry mandatory."""
    if not isinstance(goal, ImageWholeStatement) or not isinstance(goal.map, TodaSuspensionMap):
        return ()
    return (GoalExpansion(ehp_surjective_implies_whole_image_rule(), (MapSurjective(goal.map),)),)
