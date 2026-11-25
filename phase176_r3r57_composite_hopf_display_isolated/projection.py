"""Compress a verified composite-right Hopf equality chain, presentation only."""
from __future__ import annotations

from expression import Composition, MapApplication
from map_facts import EHP_H_MAP
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, root_ancestor_step_indices
from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence
from phase176_r3r34_composite_suspension_isolated.source import composite_suspension_equality_input
from phase176_r3r36_composite_right_hopf_isolated.source import (
    COMPOSITE_FORMULA_RULE_NAME, COMPOSITE_SUBSTITUTION_RULE_NAME,
    composite_right_formula_parts, composite_hopf_substitution_inputs,
)
from phase176_r3r55_equality_display_isolated.projection import (
    equality, is_composition_transport, is_symmetry, is_transitivity,
)
from phase176_r3r56_cited_source_display_isolated.projection import (
    PROP_ASSERTION, PROP_REFERENCE, TodaProp22RightFormula, source_citation,
)
from proof import ProofRule
from web_group_proof_common import _group_proof_statement_latex


def inferred(step, name, arity):
    return (step.rule is ProofRule.INFERENCE and step.inference_rule is not None
            and step.inference_rule.name == name and len(step.premises) == arity)


def match_chain(model, scope, final_index):
    """Recognize the exact ordinary premise edges, never a textual proof pattern."""
    final = model.steps[final_index]
    if not inferred(final, 'equality transitivity', 2):
        return None
    intermediate, right = final.premises
    if not (inferred(intermediate, 'equality transitivity', 2)
            and inferred(right, 'equality preserved under left composition', 1)):
        return None
    reverse, substitution = intermediate.premises
    suspension, = right.premises
    if not (inferred(reverse, 'equality symmetry', 1)
            and inferred(substitution, COMPOSITE_SUBSTITUTION_RULE_NAME, 2)
            and inferred(suspension, 'proved composite suspension image yields typed element equality', 1)):
        return None
    forward, = reverse.premises
    formula, hopf = substitution.premises
    image, = suspension.premises
    if not (inferred(forward, 'EHP H preserves equality', 1)
            and inferred(formula, COMPOSITE_FORMULA_RULE_NAME, 1)
            and hopf.rule is ProofRule.GIVEN and not hopf.premises
            and image.rule is ProofRule.INFERENCE and image.inference_rule is not None):
        return None
    alpha, = forward.premises
    prop, = formula.premises
    if not (inferred(alpha, 'equality preserved under left composition', 1)
            and alpha.premises[0] is suspension):
        return None
    ordered = (image, suspension, alpha, forward, reverse, prop, formula, hopf,
               substitution, intermediate, right, final)
    lookup = {id(s): i for i, s in enumerate(model.steps)}
    indices = tuple(lookup.get(id(s)) for s in ordered)
    if len(set(indices)) != len(ordered) or any(i not in scope for i in indices):
        return None
    if final_index == model.root_index:
        return None
    c = lambda s: s.conclusion
    if not (composite_suspension_equality_input(c(suspension)) == c(image)
            and composite_right_formula_parts(c(formula)) is not None
            and composite_hopf_substitution_inputs(c(substitution)) == (c(formula), c(hopf))
            and is_composition_transport(c(alpha), c(suspension))
            and is_composition_transport(c(right), c(suspension))
            and equality(c(forward)) and equality(c(alpha))
            and c(forward).lhs == MapApplication(EHP_H_MAP, c(alpha).lhs)
            and c(forward).rhs == MapApplication(EHP_H_MAP, c(alpha).rhs)
            and is_symmetry(c(reverse), c(forward))
            and is_transitivity(c(intermediate), c(reverse), c(substitution))
            and is_transitivity(c(final), c(intermediate), c(right))):
        return None
    # No other proof branch may depend on any equation hidden by this summary.
    # The independent suspension image and final conclusion are retained.
    hidden = set(indices[1:5] + indices[6:11])
    if any(model.step_citation_numbers[i] for i in hidden - {indices[7]}):
        return None
    if model.step_citation_numbers[final_index] or model.step_citation_numbers[indices[0]]:
        return None
    for j in scope - set(indices):
        if any(lookup.get(id(p)) in hidden for p in model.steps[j].premises):
            return None
    citation = source_citation(model, scope, indices[5], TodaProp22RightFormula(),
                               PROP_ASSERTION, PROP_REFERENCE, 'Proposition 2.2')
    nums = model.step_citation_numbers[indices[7]]
    if citation is None or len(nums) != 1 or nums[0] == citation.number:
        return None
    hopf_cites = [x for x in model.citations if x.number == nums[0] and indices[7] in x.step_indices]
    if len(hopf_cites) != 1:
        return None
    return ordered, indices, (citation.number, nums[0])


def relation_terms(step):
    if not equality(step.conclusion):
        return None
    tex, fallback = _group_proof_statement_latex(step.conclusion)
    if fallback is not None or not tex or tex.count('=') != 1:
        return None
    parts = tuple(part.strip() for part in tex.split('='))
    return parts if all(parts) else None


def project_composite_hopf_chain(markdown, model):
    """Return (markdown, plan); fail closed for ambiguous, absent or partial views."""
    if (not isinstance(model, ProofNarrativeModel) or model.status is not ProofSearchStatus.COMPLETE
            or model.open_goals or model.root_index is None
            or len(model.steps) != len(model.step_citation_numbers)):
        return markdown, {}
    try:
        scope = root_ancestor_step_indices(model.steps, model.root_index)
    except ValueError:
        return markdown, {}
    lines = markdown.splitlines()
    if lines.count('証明') != 1:
        return markdown, {}
    boundary = lines.index('証明')
    body = [(i, line) for i, line in enumerate(lines) if i > boundary and line.strip()]
    candidates = []
    for final_index in sorted(scope):
        matched = match_chain(model, scope, final_index)
        if matched is None:
            continue
        steps, indices, (prop, hopf) = matched
        image, suspension, alpha, forward, reverse, source, formula, given, substitution, intermediate, right, final = steps
        # All five links are established by real typed equations. Rendering is
        # used only after the premise edges and citations have been verified.
        edges = [relation_terms(s) for s in (reverse, formula, substitution, right)]
        if any(edge is None for edge in edges):
            continue
        rev, form, sub, last = edges
        if rev[1] != form[0] or form[0] != sub[0] or sub[1] != last[0]:
            continue
        final_terms = relation_terms(final)
        if final_terms != (rev[0], last[1]):
            continue
        terms = (rev[0], rev[1], form[1], sub[1], last[1])
        if len(set(terms)) != len(terms):
            continue
        sentences = [_rendered_sentence(s) for s in (image, suspension, alpha, forward, formula,
                                                       given, substitution, intermediate, right, final)]
        if any(s is None for s in sentences):
            continue
        sentences[4] = f'[R{prop}]より, ' + sentences[4]
        sentences[5] = f'[R{hopf}]より, ' + sentences[5]
        # Require a single contiguous sequence of exactly the actual displayed
        # sentences (blank Markdown separators allowed). Reverse was hidden by
        # the prior equality projection; it must not also be visible.
        if any(line == _rendered_sentence(reverse) for _, line in body):
            continue
        if any(sum(line == s for _, line in body) != 1 for s in sentences):
            continue
        starts = [j for j in range(len(body) - len(sentences) + 1)
                  if [line for _, line in body[j:j+len(sentences)]] == sentences]
        if len(starts) != 1:
            continue
        start = starts[0]
        first, end = body[start][0], body[start+len(sentences)-1][0]
        summary = f'[R{prop}], [R{hopf}]を用いて, $' + '='.join(terms) + '$.'
        candidates.append((first, end, sentences[0], summary, indices))
    if len(candidates) != 1:
        return markdown, {}
    first, end, witness, summary, indices = candidates[0]
    output = lines[:first] + [witness, '', summary] + lines[end+1:]
    result = '\n'.join(output) + ('\n' if markdown.endswith('\n') else '')
    return result, {'chain_indices': list(indices), 'summary': summary,
                    'retained_witness': witness, 'replaced_visible_lines': 9}
