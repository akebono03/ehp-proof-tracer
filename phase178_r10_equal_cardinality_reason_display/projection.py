"""Explain the actual finite-cardinality injectivity premises, not ancestors."""
from phase165_r14_r6_generic_iso import MapInjective
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase178_r8_finite_group_surjective_injective_isolated.rule import (
    RULE_NAME, expand_finite_surjective_injective,
)
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def project_equal_cardinality_reason(statement, step):
    """Return a sentence only for the replayed R8 rule and its exact premises."""
    if (type(statement) is not MapInjective or not isinstance(step, ProofStep)
            or step.rule is not ProofRule.INFERENCE or step.conclusion != statement
            or step.inference_rule is None or step.inference_rule.name != RULE_NAME
            or len(step.premises) != 3):
        return None
    if any(not isinstance(p, ProofStep) or p.rule is not ProofRule.INFERENCE
           for p in step.premises):
        return None
    first = step.premises[0].conclusion
    if type(first) is not FiniteGroupCardinality:
        return None
    options = expand_finite_surjective_injective(statement, first.order)
    if len(options) != 1 or options[0].subgoals != tuple(p.conclusion for p in step.premises):
        return None
    # Check both the original inference and the current canonical R8 guard.
    for rule in (step.inference_rule, options[0].rule):
        if not any(
            len(match.premises) == len(step.premises)
            and all(a is b for a, b in zip(match.premises, step.premises))
            and type(derived.conclusion) is type(statement)
            and derived.conclusion == statement
            for match in find_inference_matches_for_rule(rule, step.premises)
            for derived in (apply_inference_match(match),)
        ):
            return None
    from phase168_r3_27_typed_statement_projection import group_tex, map_symbol_tex
    source = group_tex(statement.map.source_group)
    target = group_tex(statement.map.target_group)
    symbol = map_symbol_tex(statement.map)
    if not all((source, target, symbol)):
        return None
    return (rf"$|{source}|=|{target}|={first.order}$ であり, ${symbol}$ は全射なので, "
            rf"${symbol}: {source}\to {target}$ は単射.")
