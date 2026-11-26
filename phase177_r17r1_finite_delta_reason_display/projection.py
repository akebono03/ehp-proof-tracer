"""Presentation only: explain the actual R14 order and injectivity premises."""
from proof import ProofRule, ProofStep
from phase177_r14_finite_cyclic_delta_injective_isolated.rule import (
    ORDER_RULE, INJECTIVE_RULE, summand_order_inputs, finite_delta_injective_inputs,
)
from toda_human_readable_renderer import render_toda_public_group_generator_latex


def project_finite_delta_reason(statement, step):
    if (not isinstance(step, ProofStep) or step.rule is not ProofRule.INFERENCE
            or step.conclusion != statement or step.inference_rule is None):
        return None
    from phase168_r3_27_typed_statement_projection import group_tex
    name = step.inference_rule.name
    parents = step.premises
    if name == ORDER_RULE and len(parents) == 1:
        if (parents[0].rule not in (ProofRule.GIVEN, ProofRule.INFERENCE)
                or summand_order_inputs(statement, parents[0].conclusion) is None):
            return None
        try:
            element = render_toda_public_group_generator_latex(statement.element)
        except (TypeError, ValueError):
            return None
        if not element:
            return None
        return rf"直和成分の生成元なので, $\operatorname{{ord}}({element})={statement.order}$."
    if name == INJECTIVE_RULE and len(parents) == 3:
        if (parents[0].rule not in (ProofRule.GIVEN, ProofRule.INFERENCE)
                or any(p.rule is not ProofRule.INFERENCE for p in parents[1:])
                or finite_delta_injective_inputs(statement, *(p.conclusion for p in parents)) is None):
            return None
        source = group_tex(statement.map.source_group)
        target = group_tex(statement.map.target_group)
        try:
            a = render_toda_public_group_generator_latex(parents[1].conclusion.source_generator)
            b = render_toda_public_group_generator_latex(parents[1].conclusion.target_generator)
        except (TypeError, ValueError):
            return None
        if not all((source, target, a, b)):
            return None
        m = parents[2].conclusion.order
        return (rf"始域は位数 ${m}$ の巡回群で, $\Delta({a})={b}$ の位数も ${m}$ なので, "
                rf"$\Delta:{source}\to {target}$ は単射.")
    return None



def project_concise_delta_display(model, order, suppressed):
    """Keep the certified order step; elide only redundant complete-proof prose."""
    from phase168_r3_27_typed_statement_projection import group_tex
    from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality

    hidden = set()
    sentences = {}
    positions = {index: pos for pos, index in enumerate(order)}
    identities = {id(step): index for index, step in enumerate(model.steps)}

    def earlier_visible(step, index):
        parent = identities.get(id(step))
        return (parent in positions and parent not in suppressed and parent not in hidden
                and positions[parent] < positions[index])

    for index in order:
        step = model.steps[index]
        if (index in suppressed or step.inference_rule is None
                or step.inference_rule.name != INJECTIVE_RULE
                or project_finite_delta_reason(step.conclusion, step) is None):
            continue
        domain, image, witness = step.premises
        if (witness.inference_rule is None or witness.inference_rule.name != ORDER_RULE
                or project_finite_delta_reason(witness.conclusion, witness) is None):
            continue
        witness_index = identities.get(id(witness))
        if (witness_index == model.root_index or not earlier_visible(witness,index)
                or model.step_citation_numbers[witness_index]
                or sum(any(parent is witness or parent == witness for parent in candidate.premises)
                       for candidate in model.steps) != 1):
            continue
        if not earlier_visible(domain,index) or not earlier_visible(witness.premises[0],index):
            continue
        # The GeneratorImage itself may be intentionally hidden by the shared
        # renderer. Require its actual equality premise to occur before this step.
        equality = delta_image_equality(image.conclusion)
        if equality is None or not any(
            type(parent.conclusion) is type(equality) and parent.conclusion == equality
            and earlier_visible(parent,index) for parent in image.premises
        ):
            continue
        source = group_tex(step.conclusion.map.source_group)
        target = group_tex(step.conclusion.map.target_group)
        if source is None or target is None:
            continue
        hidden.add(witness_index)
        sentences[index] = rf"よって, $\Delta:{source}\to {target}$ は単射."
    return frozenset(hidden), sentences
