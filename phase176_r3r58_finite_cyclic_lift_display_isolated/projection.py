"""Explain an already certified finite cyclic Hopf lift, without adding proof steps."""
from __future__ import annotations

from math import gcd

from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, root_ancestor_step_indices
from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import (
    RULE_NAME, finite_cyclic_subgroup_lift_inputs,
)
from phase176_r3r50_strict_nu_prime_connection.notation import (
    RULE_NAME as ALIAS_RULE_NAME, alias_hopf_input,
)
from phase176_r3r55_equality_display_isolated.projection import is_finite_cyclic_conversion
from phase176_r3r57_composite_hopf_display_isolated.projection import relation_terms
from proof import ProofRule, find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement


def match_lift(model):
    """Require the actual five-premise root lift and its existing rule guard."""
    if (not isinstance(model, ProofNarrativeModel)
            or model.status is not ProofSearchStatus.COMPLETE or model.open_goals
            or type(model.root_index) is not int
            or len(model.steps) != len(model.step_citation_numbers)):
        return None
    try:
        scope = root_ancestor_step_indices(model.steps, model.root_index)
    except ValueError:
        return None
    root = model.steps[model.root_index]
    if (root.rule is not ProofRule.INFERENCE or root.inference_rule is None
            or root.inference_rule.name != 'finite cyclic structure gives group relation'
            or len(root.premises) != 1):
        return None
    lift, = root.premises
    if (lift.rule is not ProofRule.INFERENCE or lift.inference_rule is None
            or lift.inference_rule.name != RULE_NAME or len(lift.premises) != 5
            or not is_finite_cyclic_conversion(lift.conclusion, root.conclusion)):
        return None
    injective, exact, codomain, kernel, image = lift.premises
    lookup = {id(step): i for i, step in enumerate(model.steps)}
    ordered = (*lift.premises, lift, root)
    indices = tuple(lookup.get(id(step)) for step in ordered)
    if (len(lookup) != len(model.steps) or len(set(indices)) != len(ordered)
            or any(i not in scope for i in indices)):
        return None
    if any(s.rule is not ProofRule.INFERENCE or s.inference_rule is None
           for s in (injective, exact, kernel, image)):
        return None
    values = tuple(s.conclusion for s in lift.premises)
    if finite_cyclic_subgroup_lift_inputs(lift.conclusion, *values[1:]) != values:
        return None
    # Reuse the actual guarded rule (including the verified DB-prior guard).
    # This checks a match only; it does not construct or search for a ProofStep.
    if not find_inference_matches_for_rule(lift.inference_rule, lift.premises):
        return None
    if (exact.inference_rule.name != 'EHP exactness implies image equals kernel'
            or len(exact.premises) != 1):
        return None
    window, = exact.premises
    window_index = lookup.get(id(window))
    if (window_index not in scope or window.rule is not ProofRule.INFERENCE
            or window.conclusion != TodaProp42ExactnessStatement(exact.conclusion.window)):
        return None
    try:
        ancestors = root_ancestor_step_indices(model.steps, window_index)
    except ValueError:
        return None
    source_numbers = set()
    for i in ancestors:
        step = model.steps[i]
        if (step.rule is ProofRule.GIVEN and not step.premises
                and type(step.conclusion) is TodaProp42GeneralExactnessStatement):
            source_numbers.update(c.number for c in model.citations
                                  if i in c.step_indices and c.number in model.step_citation_numbers[i])
    if len(source_numbers) != 1:
        return None
    # The final typed image may use the already verified strict notation
    # transport. Require its exact premise, not an equal-looking string.
    visible_image = image
    if image.inference_rule.name == ALIAS_RULE_NAME:
        if len(image.premises) != 1:
            return None
        visible_image, = image.premises
        if (lookup.get(id(visible_image)) not in scope
                or visible_image.rule is not ProofRule.INFERENCE
                or alias_hopf_input(image.conclusion, visible_image.conclusion)
                != visible_image.conclusion):
            return None
    if any(model.step_citation_numbers[i] for i in (indices[5], indices[6])):
        return None
    return ordered, indices, visible_image, next(iter(source_numbers))


def project_finite_cyclic_lift(markdown, model):
    """Insert only the missing justification immediately before the unique root."""
    matched = match_lift(model)
    if matched is None:
        return markdown, {}
    steps, indices, visible_image, exactness_number = matched
    injective, exact, codomain, kernel, image, lift, root = steps
    lines = markdown.splitlines()
    if lines.count('証明') != 1:
        return markdown, {}
    boundary = lines.index('証明')
    body = [(i, line) for i, line in enumerate(lines) if i > boundary and line.strip()]
    texts = [_rendered_sentence(s) for s in (injective, codomain, kernel, visible_image, root)]
    if any(s is None for s in texts):
        return markdown, {}
    # Require the five displayed facts, allowing the existing citations on
    # the codomain statement. No matching by bare generator text.
    codomain_numbers = model.step_citation_numbers[indices[2]]
    if codomain.rule is ProofRule.GIVEN:
        if not codomain_numbers or any(not any(c.number == n and indices[2] in c.step_indices
                                             for c in model.citations) for n in codomain_numbers):
            return markdown, {}
        texts[1] = ', '.join(f'[R{n}]' for n in codomain_numbers) + 'より, ' + texts[1]
    elif codomain.rule is not ProofRule.INFERENCE or codomain_numbers:
        return markdown, {}
    texts[4] = '以上より, ' + texts[4]
    anchors = [[i for i, line in body if line == text] for text in texts]
    if any(len(items) != 1 for items in anchors):
        return markdown, {}
    positions = tuple(items[0] for items in anchors)
    if positions != tuple(sorted(set(positions))) or any(
            line.strip() for line in lines[positions[3]+1:positions[4]]):
        return markdown, {}
    terms = relation_terms(visible_image)
    if terms is None or relation_terms(image) != terms:
        return markdown, {}
    m, q, order = codomain.conclusion.rhs.order, kernel.conclusion.multiple, lift.conclusion.order
    if order != m // gcd(m, q):
        return markdown, {}
    multiple = terms[1]
    reasons = (
        rf'完全性より, $\operatorname{{Im}} H=\ker\Delta=\langle {multiple}\rangle$.',
        rf'この部分群の位数は $\operatorname{{ord}}({multiple})=\frac{{{m}}}{{\gcd({m},{q})}}={order}$.',
        rf'$H$ は単射であり, 直前に求めた像がこの部分群を生成するので, その原像が位数 ${order}$ の生成元となる.',
    )
    if any(reason in lines for reason in reasons):
        return markdown, {}
    output = lines[:positions[4]] + [part for reason in reasons for part in (reason, '')] + lines[positions[4]:]
    projected = '\n'.join(output) + ('\n' if markdown.endswith('\n') else '')
    return projected, {'lift_index': indices[5], 'root_index': indices[6],
                       'premise_indices': list(indices[:5]), 'exactness_reference': exactness_number,
                       'codomain_order': m, 'kernel_multiple': q, 'subgroup_order': order,
                       'added_sentences': list(reasons)}
