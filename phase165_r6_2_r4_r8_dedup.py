"""Conservative equivalence for two generic cited scalar-specialization routes.

This equivalence is intentionally narrow: it never identifies independent proofs
merely because their conclusions are equal.
"""
from __future__ import annotations


SCALAR_SPECIALIZATION_ROUTES = frozenset((
    "Toda Proposition 5.1 generic higher-eta specialization",
    "generic cited typed scalar specialization",
))


def same_cited_scalar_specialization(left: object, right: object) -> bool:
    """Recognize the SAME cited step specialized to the SAME concrete goal.

    This is an alias of two implementations of scalar substitution, not a
    theorem that two arbitrary derivations with the same goal are equivalent.
    """
    from proof import ProofRule, ProofStep
    from phase165_r57_r20_general_specialization import specialize_typed_statement

    if not isinstance(left, ProofStep) or not isinstance(right, ProofStep):
        return False
    if left.rule is not ProofRule.INFERENCE or right.rule is not ProofRule.INFERENCE:
        return False
    if type(left.conclusion) is not type(right.conclusion) or left.conclusion != right.conclusion:
        return False
    if len(left.premises) != 1 or len(right.premises) != 1:
        return False
    cited_left, cited_right = left.premises[0], right.premises[0]
    if cited_left is not cited_right or not isinstance(cited_left, ProofStep):
        return False
    if cited_left.rule is not ProofRule.GIVEN or cited_left.premises != ():
        return False
    first_rule, second_rule = left.inference_rule, right.inference_rule
    if first_rule is None or second_rule is None:
        return False
    if frozenset((first_rule.name, second_rule.name)) != SCALAR_SPECIALIZATION_ROUTES:
        return False
    # Both routes must derive the goal by a checked typed scalar substitution.
    # A source is never constructed or silently promoted to a GIVEN.
    return specialize_typed_statement(cited_left.conclusion, left.conclusion) is not None


def append_unique_verified_derivation(options: list, candidate: object) -> None:
    """Keep distinct valid derivations; omit only verified duplicate routes."""
    if any(same_cited_scalar_specialization(old, candidate) for old in options):
        return
    options.append(candidate)
