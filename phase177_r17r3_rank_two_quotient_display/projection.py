"""Display the already certified rank-two EHP quotient inference."""
from proof import ProofRule, ProofStep
from phase175_r4r3_two_summand_quotient.rule import RULE_NAME, two_summand_quotient_inputs
from toda_human_readable_renderer import render_toda_public_group_generator_latex


def project_rank_two_quotient_reason(statement, step):
    """Describe only the exact six premises; never create a ProofStep."""
    if (not isinstance(step, ProofStep) or step.rule is not ProofRule.INFERENCE
            or step.conclusion != statement or step.inference_rule is None
            or step.inference_rule.name != RULE_NAME or len(step.premises) != 6):
        return None
    parents = step.premises
    if (any(p.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE) for p in parents[:2])
            or any(p.rule is not ProofRule.INFERENCE for p in parents[2:])):
        return None
    values = tuple(p.conclusion for p in parents)
    middle, domain, delta, exact, surj, image = values
    if two_summand_quotient_inputs(statement, middle, domain, delta, image) != values:
        return None
    from phase168_r3_27_typed_statement_projection import group_tex
    try:
        killed = render_toda_public_group_generator_latex(delta.target_generator)
        survivor = render_toda_public_group_generator_latex(image.source_generator)
        target_generator = render_toda_public_group_generator_latex(image.target_generator)
    except (TypeError, ValueError):
        return None
    a, b = group_tex(middle.lhs), group_tex(statement.group)
    if not all((killed, survivor, target_generator, a, b)):
        return None
    return (
        rf"完全性より, $\ker E=\operatorname{{Im}}\Delta=\mathbb{{Z}}/2\{{{killed}\}}$. "
        rf"また, $E({survivor})={target_generator}$. "
        rf"$E$ は全射なので, 準同型定理より ${b}\cong {a}/\ker E$."
    )
