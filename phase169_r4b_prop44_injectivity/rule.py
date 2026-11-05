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
    """Apply conditional Proposition 4.4 to a proved Lemma 5.4 Hopf witness."""
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
    )
    from proof import Relation, RelationType

    if not _is_hopf_four_suspension(goal):
        raise ValueError("goal must be an n=4 suspension injectivity")
    hopf = canonical_hopf_relation()
    proposition = TodaProp44UniversalStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == proposition
            and premises[1].rule is ProofRule.INFERENCE
            and premises[1].conclusion == hopf
            and len(premises[1].premises) == 1
            and premises[1].premises[0].rule is ProofRule.GIVEN
            and type(premises[1].premises[0].conclusion) is TodaLemma54TypedSource
            and premises[1].premises[0].conclusion == TodaLemma54TypedSource()
            and _is_hopf_four_suspension(goal)
        )

    return InferenceRule(
        name="Toda Proposition 4.4 using separately proved Hopf invariant",
        description=(
            "Proposition 4.4 is conditional; independently prove H(nu_4)=iota_7 "
            "from the earlier, screened Lemma 5.4 before specializing it."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaProp44UniversalStatement,
                statement_pattern=proposition,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=hopf,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )


def expand_cited_prop44_injectivity(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose the conditional theorem only when Lemma 5.4 is source-screened."""
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
    )

    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not _is_hopf_four_suspension(goal):
        return ()
    proposition = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    if available.count(proposition) != 1 or available.count(lemma) != 1:
        return ()
    return (GoalExpansion(
        prop44_hopf_four_injectivity_rule(goal),
        (proposition, canonical_hopf_relation()),
    ),)
