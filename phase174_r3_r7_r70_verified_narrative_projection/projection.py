"""Source-bound, general explanation of existing completed ProofStep chains.

Never add a ProofStep, GIVEN, or inference. A displayed intermediate implication
of a verified four-premise EHP root is prose, not an independent new proof step.
Any missing, ambiguous or unrelated witness leaves original lines untouched.
"""
from __future__ import annotations


def _step_index(model, step, scope: frozenset[int]) -> int | None:
    """Resolve a real ancestor by unique identity, else unique value."""
    identities = tuple(i for i in scope if model.steps[i] is step)
    if len(identities) == 1:
        return identities[0]
    if identities:
        return None
    values = tuple(i for i in scope if model.steps[i] == step)
    return values[0] if len(values) == 1 else None


def _body_index(lines: list[str], sentence: str, *, prefix: str | None = None) -> int | None:
    """Match one whole existing proof line, never a Reference paragraph."""
    headings = [i for i, line in enumerate(lines) if line == "証明"]
    if len(headings) != 1 or not sentence:
        return None
    start = headings[0] + 1
    found = [i for i in range(start, len(lines))
             if (lines[i] == sentence or lines[i].endswith(sentence))
             and (prefix is None or lines[i].startswith(prefix))]
    return found[0] if len(found) == 1 else None


def _given_ancestor_tags(model, step, scope: frozenset[int]) -> tuple[int, ...]:
    """Collect only actually used registered GIVEN citations, not names."""
    from proof import ProofRule
    seen: set[int] = set()
    pending = [step]
    numbers: set[int] = set()
    while pending:
        current = pending.pop()
        index = _step_index(model, current, scope)
        if index is None:
            return ()
        if index in seen:
            continue
        seen.add(index)
        if current.rule is ProofRule.GIVEN:
            numbers.update(model.step_citation_numbers[index])
        pending.extend(current.premises)
    return tuple(sorted(numbers))


def _project_composite_images(lines: list[str], model, scope: frozenset[int]) -> list[str]:
    """Condense three displayed premises only for a verified composite-zero step."""
    from expression import Zero
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import (
        RULE_NAME as ASSOCIATIVITY_RULE_NAME,
        generator_image_associativity_inputs,
    )
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
        # A verified image may first be rebracketed by the generic
        # associativity rule. Trace that one certified INFERENCE edge before
        # checking the existing two-component suspension rule. R9 changes
        # parentheses, not the image, generator, or source citations.
        component_image_step = image_step
        if len(image_step.premises) == 1:
            right_step = image_step.premises[0]
            expected_right = generator_image_associativity_inputs(
                image_step.conclusion,
            )
            if (image_step.inference_rule is None
                    or image_step.inference_rule.name != ASSOCIATIVITY_RULE_NAME
                    or right_step.rule is not ProofRule.INFERENCE
                    or _step_index(model, right_step, scope) is None
                    or expected_right != (right_step.conclusion,)):
                continue
            component_image_step = right_step
        requirements = component_image_obligations(
            component_image_step.conclusion,
        )
        if (requirements is None
                or len(component_image_step.premises) != 2):
            continue
        component_steps = component_image_step.premises
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


def _project_delta_consequence(lines: list[str], model,
                               scope: frozenset[int]) -> list[str]:
    """Use よって only when an exact one-premise cyclic presentation precedes Delta."""
    from homotopy_groups import TodaDeltaMap
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase168_r3_27_typed_statement_projection import group_tex, typed_sentence
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import (
        SURJECTIVE_RULE_NAME, delta_surjectivity_generator_inputs,
    )
    from proof import ProofRule, Relation

    output = list(lines)
    for index in sorted(scope):
        step = model.steps[index]
        goal = step.conclusion
        if (step.rule is not ProofRule.INFERENCE
                or getattr(step.inference_rule, "name", None) != SURJECTIVE_RULE_NAME
                or not isinstance(goal, MapSurjective)
                or not isinstance(goal.map, TodaDeltaMap)
                or len(step.premises) != 1):
            continue
        prior = step.premises[0]
        prior_idx = _step_index(model, prior, scope)
        expected = delta_surjectivity_generator_inputs(goal)
        if (prior_idx is None or expected != (prior.conclusion,)
                or prior.rule not in (ProofRule.INFERENCE, ProofRule.GIVEN)
                or not isinstance(prior.conclusion, Relation)):
            continue
        sentence = typed_sentence(goal, step)
        if not isinstance(sentence, str):
            continue
        tags = model.step_citation_numbers[prior_idx]
        if len(tags) != 1:
            continue
        delta_idx = _body_index(output, sentence, prefix=f"[R{tags[0]}]より, ")
        if delta_idx is None:
            continue
        group_name = group_tex(prior.conclusion.lhs)
        if group_name is None:
            continue
        prior_matches = [i for i in range(delta_idx)
                         if output[i].startswith(f"[R{tags[0]}]より, ")
                         and group_name in output[i]]
        if len(prior_matches) != 1:
            continue
        output[delta_idx] = "よって, " + sentence
    return output


def _project_zero_root_explanation(lines: list[str], model,
                                   scope: frozenset[int]) -> list[str]:
    """Explain the existing EHP root's four-premise implication, without new steps."""
    from homotopy_groups import TodaHopfInvariantMap, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import MapInjective
    from phase168_r3_27_typed_statement_projection import group_tex, typed_sentence
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME, ehp_zero_inputs
    from proof import ProofRule

    if model.root_index not in scope:
        return list(lines)
    root = model.steps[model.root_index]
    required = ehp_zero_inputs(root.conclusion)
    if (root.rule is not ProofRule.INFERENCE
            or getattr(root.inference_rule, "name", None) != RULE_NAME
            or required is None
            or len(required) != 4
            or len(root.premises) != 4
            or any(parent.rule is not ProofRule.INFERENCE
                   or parent.conclusion != expected
                   or _step_index(model, parent, scope) is None
                   for parent, expected in zip(root.premises, required))):
        return list(lines)
    delta_window = required[1].window
    hopf_window = required[2].window
    e = TodaSuspensionMap(delta_window.middle_term, delta_window.target_term)
    h = TodaHopfInvariantMap(hopf_window.middle_term, hopf_window.target_term)
    if (e.target_group != h.source_group
            or delta_window.target_term != hopf_window.middle_term):
        return list(lines)
    if any(model.steps[i].rule is ProofRule.INFERENCE
           and model.steps[i].conclusion in (ImageZeroStatement(e), MapInjective(h))
           for i in scope):
        # Do not repeat separately certified intermediate ProofSteps.
        return list(lines)
    delta_sentence = typed_sentence(required[0], root.premises[0])
    if not isinstance(delta_sentence, str):
        return list(lines)
    index = _body_index(lines, delta_sentence)
    if index is None:
        return list(lines)
    source, middle = group_tex(e.source_group), group_tex(e.target_group)
    middle_h, terminal = group_tex(h.source_group), group_tex(h.target_group)
    if any(value is None for value in (source, middle, middle_h, terminal)):
        return list(lines)
    # These are explicitly the two elementary consequences of the verified
    # four-premise zero-root rule, NOT additional independent ProofSteps.
    first = (rf"完全性と $\Delta$ の全射性より, "
             rf"$E:{source}\to {middle}$ は零写像.")
    second = (rf"さらに完全性より, $\ker H=\operatorname{{Im}}E=0$ なので, "
              rf"$H:{middle_h}\to {terminal}$ は単射.")
    output = list(lines)
    output[index + 1:index + 1] = ["", first, "", second]
    return output


def project_verified_general_narrative(lines: list[str], model) -> list[str]:
    """General, fail-closed completion-only prose improvements from a verified root."""
    if not isinstance(lines, list) or model.root_index is None:
        return lines
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    changed = _project_composite_images(lines, model, scope)
    changed = _project_delta_consequence(changed, model, scope)
    changed = _project_zero_root_explanation(changed, model, scope)
    return changed
