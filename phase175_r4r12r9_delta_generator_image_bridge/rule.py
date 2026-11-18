"""Generic typed bridge: a proved map equality implies a generator image.

No Toda equation, DB fact, group conclusion or GIVEN is introduced.
"""
from __future__ import annotations

from expression import MapApplication
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


RULE_NAME = "proved typed Delta equality implies generator image"


def delta_image_equality(goal: object) -> Relation | None:
    """Form the precise equality required by a typed Delta GeneratorImage."""
    if not isinstance(goal, GeneratorImage) or not isinstance(goal.map, TodaDeltaMap):
        return None
    source = typed_endpoints(goal.source_generator)
    target = typed_endpoints(goal.target_generator)
    if (source is None or target is None
            or source[1] < 3 or source[1] % 2 != 1
            or source[0] < source[1] or source[0] < 3
            or source[1] != 2 * target[1] + 1
            or source[0] != target[0] + 2
            or goal.map.source_group != TodaPrimaryGroup(*source)
            or goal.map.target_group != TodaPrimaryGroup(*target)):
        return None
    return Relation(
        lhs=MapApplication(EHP_DELTA_MAP, goal.source_generator),
        rhs=goal.target_generator,
        relation_type=RelationType.EQUALITY,
    )


def expand_proved_delta_equality_image(goal: object) -> tuple[GoalExpansion, ...]:
    """Use a verified INFERENCE equality, never a guessed printed generator."""
    equality = delta_image_equality(goal)
    if equality is None:
        return ()

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == equality
            and delta_image_equality(goal) == equality
        )

    rule = InferenceRule(
        name=RULE_NAME,
        description=(
            "An independently inferred and dimension-checked Delta(g)=h "
            "supplies the typed GeneratorImage(Delta,g,h). "
            "A signed relation or a DB generator label is insufficient."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.INFERENCE,
            statement_type=Relation,
            relation_type=RelationType.EQUALITY,
            statement_pattern=equality,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    )
    return (GoalExpansion(rule, (equality,)),)
