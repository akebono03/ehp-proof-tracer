"""Display the two exactness implications of the existing combined rule."""
from phase165_r14_r6_generic_iso import MapSurjective
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import (
    E_RULE_NAME, expand_e_surjective_from_delta_injective,
)
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def project_hopf_zero_reason(statement, step):
    """Explain a combined inference without adding a Hopf-zero ProofStep."""
    if (type(statement) is not MapSurjective
            or not isinstance(step, ProofStep)
            or step.rule is not ProofRule.INFERENCE
            or step.conclusion != statement or step.inference_rule is None
            or step.inference_rule.name != E_RULE_NAME
            or len(step.premises) != 3
            or any(not isinstance(p, ProofStep) or p.rule is not ProofRule.INFERENCE
                   for p in step.premises)):
        return None
    options = expand_e_surjective_from_delta_injective(statement)
    if (len(options) != 1
            or options[0].subgoals != tuple(p.conclusion for p in step.premises)):
        return None
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
    from phase168_r3_27_typed_statement_projection import group_tex
    source = group_tex(statement.map.source_group)
    target = group_tex(statement.map.target_group)
    if not source or not target:
        return None
    return (rf"完全性より, $\operatorname{{Im}}H=\ker\Delta=0$ なので, "
            rf"$H$ は零写像. よって, $\operatorname{{Im}}E=\ker H={target}$ となり, "
            rf"$E: {source}\to {target}$ は全射.")
