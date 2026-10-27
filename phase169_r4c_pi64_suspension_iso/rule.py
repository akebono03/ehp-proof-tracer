"""Connect independently proved injectivity and surjectivity to the pi6_4 E-isomorphism.

The two inputs must be genuine INFERENCE ProofSteps. Neither the source group
presentation nor an isomorphism is supplied as a GIVEN by this module.
"""
from __future__ import annotations

from homotopy_groups import (
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule


_PI64_E = TodaSuspensionMap(
    source_group=TodaPrimaryGroup(5, 3),
    target_group=TodaPrimaryGroup(6, 4),
)


def pi64_suspension_isomorphism_rule(goal: TodaSuspensionIsomorphismStatement) -> InferenceRule:
    """Infer only E: pi5_3 -> pi6_4 from two separately proved map properties."""
    if type(goal) is not TodaSuspensionIsomorphismStatement or goal.map != _PI64_E:
        raise ValueError("R4C requires the concrete pi5_3 to pi6_4 suspension map")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule is ProofRule.INFERENCE
            and type(premises[0].conclusion) is MapInjective
            and type(premises[1].conclusion) is MapSurjective
            and premises[0].conclusion.map == _PI64_E
            and premises[1].conclusion.map == _PI64_E
        )

    return InferenceRule(
        name="pi6_4 suspension isomorphism from proved injectivity and surjectivity",
        description=(
            "Compose independently derived Toda Proposition 4.4 injection and "
            "Proposition 4.2 / (5.1) EHP surjection for pi5_3 to pi6_4."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapInjective),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapSurjective),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_pi64_suspension_isomorphism(goal: object) -> tuple[GoalExpansion, ...]:
    """Offer the missing typed link, without manufacturing proofs or references."""
    if type(goal) is not TodaSuspensionIsomorphismStatement or goal.map != _PI64_E:
        return ()
    return (
        GoalExpansion(
            pi64_suspension_isomorphism_rule(goal),
            (MapInjective(_PI64_E), MapSurjective(_PI64_E)),
        ),
    )
