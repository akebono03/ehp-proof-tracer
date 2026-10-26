"""Infer suspension injectivity in Hopf dimension four from cited Toda Prop. 4.4.

The paragraph immediately preceding Proposition 4.4 in the adopted Toda
source supplies the n=4 Hopf fibration. The proposition's conditional
statement then provides suspension injectivity for all relevant i. This
module handles ONLY the n=4 case; it does not bypass Toda (4.5)'s stable
range, infer surjectivity, or establish a target group presentation.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule


def _is_hopf_four_suspension(goal: object) -> bool:
    if not isinstance(goal, MapInjective):
        return False
    mapping = goal.map
    if not isinstance(mapping, TodaSuspensionMap):
        return False
    source, target = mapping.source_group, mapping.target_group
    if not isinstance(source, TodaPrimaryGroup) or not isinstance(target, TodaPrimaryGroup):
        return False
    i = source.group_dimension
    return (
        type(i) is int
        and i >= 3
        and source.sphere_dimension == 3
        and target == TodaPrimaryGroup(i + 1, 4)
    )


def prop44_hopf_four_injectivity_rule(goal: MapInjective) -> InferenceRule:
    """Require the cited full Prop. 4.4, not an assumed concrete map fact."""
    if not _is_hopf_four_suspension(goal):
        raise ValueError("goal must be an n=4 Hopf-dimension suspension injectivity")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and type(premises[0].conclusion) is TodaProp44UniversalStatement
            and premises[0].conclusion == TodaProp44UniversalStatement()
            and _is_hopf_four_suspension(goal)
        )

    return InferenceRule(
        name="Toda Proposition 4.4 Hopf dimension-four suspension injectivity",
        description=(
            "For n=4 a Hopf invariant one map exists by the preceding "
            "Hopf-fibration statement; Proposition 4.4 implies E is injective."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaProp44UniversalStatement,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4",
            locator="Proposition 4.4",
        ),
    )


def expand_cited_prop44_injectivity(
    goal: object, available: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Expand only from the unique citation-screened Prop. 4.4 claim."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not _is_hopf_four_suspension(goal):
        return ()
    cited = tuple(
        claim
        for claim in available
        if type(claim) is TodaProp44UniversalStatement
        and claim == TodaProp44UniversalStatement()
    )
    if len(cited) != 1:
        return ()
    return (GoalExpansion(prop44_hopf_four_injectivity_rule(goal), cited),)
