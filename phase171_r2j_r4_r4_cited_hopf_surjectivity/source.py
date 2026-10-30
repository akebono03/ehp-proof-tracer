"""Cyclic Hopf surjectivity from a proved codomain and cited generator image.

This is a generic typed inference rule. The caller is responsible for proving
that a GIVEN image is an actual earlier, screened literature assertion.
"""
from __future__ import annotations

from phase165_r14_r6_generic_iso import MapSurjective
from phase171_r2j_r2_cyclic_hopf_surjective.source import _valid_surjective_pair
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


def cited_hopf_cyclic_surjectivity_rule(
    goal: MapSurjective, group: Relation, image: Relation,
) -> InferenceRule:
    """A cited Hopf image hitting a *proved* cyclic generator is surjective.

    The group premise must be INFERENCE and the cited image must be a leaf
    GIVEN. This complements the existing rule for two INFERENCE premises,
    without altering its behavior or admitting arbitrary database results.
    """
    if not _valid_surjective_pair(goal, group, image):
        raise ValueError("Hopf map, cyclic codomain, and generator image do not match")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule is ProofRule.GIVEN
            and not premises[1].premises
            and premises[0].conclusion == group
            and premises[1].conclusion == image
            and _valid_surjective_pair(goal, group, image)
        )

    return InferenceRule(
        name="proved cyclic codomain and cited Hopf generator image imply surjectivity",
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=group,
            ),
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=image,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )
