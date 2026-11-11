def _project_composite_images(lines: list[str], model, scope: frozenset[int]) -> list[str]:
    """Condense three displayed premises only for a verified composite-zero step."""
    from expression import Zero
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase174_r3_r7_r7_composite_zero_audit.rule import (
        RULE_NAME, composite_zero_generator_inputs,
    )
    from proof import ProofRule
    from toda_proof_narrative_renderer import render_toda_expression_latex

    output = list(lines)
    for index in sorted(scope):
        zero_step = model.steps[index]
        zero_goal = zero_step.conclusion
        if (zero_step.rule is not ProofRule.INFERENCE
                or getattr(zero_step.inference_rule, "name", None) != RULE_NAME
                or not isinstance(zero_goal, GeneratorImage)
                or not isinstance(zero_goal.target_generator, Zero)
                or len(zero_step.premises) != 2):
            continue
        image_step, annihilator_step = zero_step.premises
        if (image_step.rule is not ProofRule.INFERENCE
                or annihilator_step.rule is not ProofRule.INFERENCE
                or _step_index(model, image_step, scope) is None
                or _step_index(model, annihilator_step, scope) is None
                or composite_zero_generator_inputs(
                    zero_goal, image_step.conclusion
                ) != (image_step.conclusion, annihilator_step.conclusion)):
            continue
        requirements = component_image_obligations(image_step.conclusion)
        if requirements is None or len(image_step.premises) != 2:
            continue
        component_steps = image_step.premises
        if (any(parent.rule is not ProofRule.INFERENCE
                or _step_index(model, parent, scope) is None
                for parent in component_steps)
                or tuple(parent.conclusion for parent in component_steps) != requirements):
            continue
        tags = _given_ancestor_tags(model, annihilator_step, scope)
        if len(tags) != 1:
            continue
        component_sentences = tuple(typed_sentence(parent.conclusion, parent)
                                    for parent in component_steps)
        annihilator_sentence = typed_sentence(annihilator_step.conclusion, annihilator_step)
        if (any(not isinstance(item, str) for item in component_sentences)
                or not isinstance(annihilator_sentence, str)):
            continue
        indices = tuple(_body_index(output, item) for item in component_sentences)
        related = _body_index(output, annihilator_sentence,
                              prefix=f"[R{tags[0]}]より, ")
        if (related is None or any(i is None for i in indices)
                or len(set(indices + (related,))) != 3):
            continue
        positions = sorted(indices + (related,))
        if (positions[0] != indices[0] or positions[1] != indices[1]
                or positions[2] != related
                or any(output[i] for i in range(positions[0], positions[2] + 1)
                       if i not in positions)):
            continue
        try:
            generator = render_toda_expression_latex(zero_goal.source_generator)
            composite = render_toda_expression_latex(image_step.conclusion.target_generator)
        except (TypeError, ValueError):
            continue
        if not generator or not composite or "\\" not in generator or "\\" not in composite:
            continue
        combined = (f"懸垂と合成の関係および [R{tags[0]}]より, "
                    f"$E({generator})={composite}=0$.")
        suffix = output[positions[2] + 1:]
        while suffix and suffix[0] == "":
            suffix.pop(0)
        output = output[:positions[0]] + [combined, ""] + suffix
    return output
