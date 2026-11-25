"""Elide only certified definitional witnesses absorbed by a displayed proof."""
from __future__ import annotations

import re

from expression import Suspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r20_eta_definition import (
    ASSERTION_ID, REFERENCE_ID, TodaEtaFamilyGeneralDefinition,
)
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, root_ancestor_step_indices
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase169_r10eq_r1_universal_stable_definition.definition import is_defined_stable_image
from phase171_r20r13_eta_sentence_layout.projection import verified_eta_display_sentences
from phase172_r2_suspension_relation_display.projection import same_typed_generator
from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence
from phase176_r3r27r1_toda55_quadruple_isolated.source import quadruple_inputs
from phase176_r3r55_equality_display_isolated.projection import (
    equality, is_composition_transport, is_symmetry, is_transitivity, looks_identical,
)
from phase176_r3r56_cited_source_display_isolated.projection import source_citation
from phase176_r3r57_composite_hopf_display_isolated import projection as hopf
from proof import ProofRule
from toda_rules import TodaEtaFamilyDefinitionStatement, toda_eta_family_definition_statement

TAG = re.compile(r'\[R(\d+)\]')


def alias_branch(model, scope, index, leaf, parents):
    """Return actual notation-transport nodes and suspension witnesses, or None.

    Every leaf is a typed, cited consecutive eta suspension. Rendered identity
    is a secondary guard, not evidence of equality.
    """
    steps = model.steps
    def uncited(i, name, arity):
        return (i in scope and not model.step_citation_numbers[i]
                and hopf.inferred(steps[i], name, arity))

    def witness(i):
        if not uncited(i, 'consecutive cited eta definitions imply generator suspension', 2):
            return False
        value = steps[i].conclusion
        if type(value) is not GeneratorSuspension or type(value.map) is not TodaSuspensionMap:
            return False
        a, b = parents[i]
        for j in (a, b):
            d = steps[j].conclusion
            if (not uncited(j, 'specialize cited eta-family general definition', 1)
                    or parents[j] != (leaf,) or type(d) is not TodaEtaFamilyDefinitionStatement
                    or type(d.index) is not int or d.index < 2
                    or d != toda_eta_family_definition_statement(d.index)):
                return False
        x, y = steps[a].conclusion, steps[b].conclusion
        return (y.index == x.index + 1
                and value.map == TodaSuspensionMap(
                    TodaPrimaryGroup(x.index + 1, x.index),
                    TodaPrimaryGroup(y.index + 1, y.index))
                and same_typed_generator(value.source_generator, x.element)
                and same_typed_generator(value.target_generator, y.element)
                and typed_sentence(value, steps[i]) is not None)

    def bridge(i, w):
        if not uncited(i, 'proved consecutive eta suspension yields element equality', 1):
            return False
        r, g = steps[i].conclusion, steps[w].conclusion
        return (parents[i] == (w,) and equality(r) and type(r.lhs) is Suspension
                and same_typed_generator(r.lhs.expression, g.source_generator)
                and same_typed_generator(r.rhs, g.target_generator))

    active = set()
    def visit(i):
        if (i in active or i not in scope or steps[i].rule is not ProofRule.INFERENCE
                or model.step_citation_numbers[i] or not looks_identical(steps[i].conclusion)):
            return None
        active.add(i)
        try:
            r, ps = steps[i].conclusion, parents[i]
            if uncited(i, 'equality transitivity', 2):
                a, b = ps
                if not is_transitivity(r, steps[a].conclusion, steps[b].conclusion):
                    return None
                if (same_typed_generator(r.lhs, r.rhs)
                        and uncited(a, 'equality symmetry', 1)
                        and len(parents[b]) == 1):
                    p, = parents[a]
                    w, = parents[b]
                    if (witness(w) and bridge(p, w) and bridge(b, w)
                            and is_symmetry(steps[a].conclusion, steps[p].conclusion)):
                        return {i, a, b, p, w}, {w}
                x, y = visit(a), visit(b)
                if x is not None and y is not None:
                    return x[0] | y[0] | {i}, x[1] | y[1]
            elif (uncited(i, 'equality preserved under left composition', 1)
                  or uncited(i, 'equality preserved under right composition', 1)):
                p, = ps
                if is_composition_transport(r, steps[p].conclusion):
                    child = visit(p)
                    if child is not None:
                        return child[0] | {i}, child[1]
            return None
        finally:
            active.remove(i)
    return visit(index)


def source_prefix(line, numbers):
    """Only extend a recognized citation prefix, preserving the exact math."""
    match = re.fullmatch(r'(\[R\d+\](?:, \[R\d+\])*)(を用いて, |より, )(\$.*\$\.)', line)
    if match is None:
        return None
    old = {int(x) for x in TAG.findall(match[1])}
    if not old or not old.issubset(numbers):
        return None
    return ', '.join(f'[R{n}]' for n in sorted(numbers)) + 'を用いて, ' + match[3]


def project_definitional_suspension_elision(markdown, model):
    """Return (unchanged or projected Markdown, audit plan); no proof changes."""
    if (not isinstance(model, ProofNarrativeModel) or model.status is not ProofSearchStatus.COMPLETE
            or model.open_goals or type(model.root_index) is not int
            or len(model.steps) != len(model.step_citation_numbers)):
        return markdown, {}
    try:
        scope = root_ancestor_step_indices(model.steps, model.root_index)
    except ValueError:
        return markdown, {}
    steps = model.steps
    lookup = {id(s): i for i, s in enumerate(steps)}
    parents = {i: tuple(lookup.get(id(p)) for p in steps[i].premises) for i in scope}
    if len(lookup) != len(steps) or any(p not in scope or p >= i for i, ps in parents.items() for p in ps):
        return markdown, {}
    lines = markdown.splitlines()
    if lines.count('証明') != 1:
        return markdown, {}
    boundary = lines.index('証明')
    body = [(i, s) for i, s in enumerate(lines) if i > boundary and s.strip()]
    def unique(s):
        hits = [i for i, line in body if line == s]
        return hits[0] if len(hits) == 1 else None
    sources = []
    for i in scope:
        if type(steps[i].conclusion) is TodaEtaFamilyGeneralDefinition:
            cite = source_citation(model, scope, i, TodaEtaFamilyGeneralDefinition(),
                                   ASSERTION_ID, REFERENCE_ID, 'Chapter V, i)')
            if cite is not None:
                sources.append((i, cite.number))
    if len(sources) != 1:
        return markdown, {}
    leaf, number = sources[0]
    allowed = verified_eta_display_sentences(model)
    candidates = []
    for final in sorted(scope):
        match = hopf.match_chain(model, scope, final)
        if match is None:
            continue
        chain, indices, nums = match
        image = indices[0]
        if (not hopf.inferred(steps[image], 'stable representative definitional suspension', 0)
                or not is_defined_stable_image(steps[image].conclusion)
                or model.step_citation_numbers[image]
                or any(j not in indices and image in ps for j, ps in parents.items())):
            continue
        # Reconstruct R57's exact summary from the same typed equations.
        edges = [hopf.relation_terms(chain[k]) for k in (4, 6, 8, 10)]
        if any(edge is None for edge in edges):
            continue
        rev, form, sub, last = edges
        if rev[1] != form[0] or form[0] != sub[0] or sub[1] != last[0]:
            continue
        if hopf.relation_terms(chain[-1]) != (rev[0], last[1]):
            continue
        terms = (rev[0], rev[1], form[1], sub[1], last[1])
        if len(set(terms)) != len(terms) or number in nums:
            continue
        witness = _rendered_sentence(steps[image])
        summary = ', '.join(f'[R{n}]' for n in nums) + 'を用いて, $' + '='.join(terms) + '$.'
        wi, si = unique(witness), unique(summary)
        if wi is None or si is None or wi >= si or any(s.strip() for s in lines[wi+1:si]):
            continue
        for joined in sorted(scope):
            if (not hopf.inferred(steps[joined], 'equality transitivity', 2)
                    or model.step_citation_numbers[joined] or parents[joined][0] != final
                    or joined == model.root_index):
                continue
            alias = parents[joined][1]
            if (not is_transitivity(steps[joined].conclusion, steps[final].conclusion, steps[alias].conclusion)
                    or hopf.relation_terms(steps[joined]) != hopf.relation_terms(steps[final])):
                continue
            matched = alias_branch(model, scope, alias, leaf, parents)
            if matched is None:
                continue
            nodes, witnesses = matched
            if (nodes.intersection(indices) or not witnesses
                    or any(j not in nodes | {joined} and nodes.intersection(ps) for j, ps in parents.items())
                    or any(j != joined and final in ps for j, ps in parents.items())):
                continue
            tag = f'[R{number}]より, '
            sentences = [typed_sentence(steps[w].conclusion, steps[w]) for w in sorted(witnesses)]
            if any(s is None or tag+s not in allowed for s in sentences):
                continue
            merged = tag + '$' + r',\quad '.join(allowed[tag+s][1] for s in sentences) + '$.'
            mi = unique(merged)
            if mi is None or mi <= si or any(s.strip() for s in lines[si+1:mi]):
                continue
            # No independent alias equation may still be visible.
            if any(_rendered_sentence(steps[j]) in {s for _, s in body} for j in nodes-witnesses):
                continue
            for consumer in sorted(scope):
                if (not hopf.inferred(steps[consumer], 'equality transitivity', 2)
                        or parents[consumer][0] != joined):
                    continue
                reverse = parents[consumer][1]
                if not hopf.inferred(steps[reverse], 'equality symmetry', 1):
                    continue
                q, = parents[reverse]
                quad = steps[q]
                inputs = quadruple_inputs(quad.conclusion)
                if (inputs is None or not hopf.inferred(quad, 'specialize cited Toda (5.5) quadruple nu-family identity', 3)
                        or tuple(p.conclusion for p in quad.premises) != inputs
                        or parents[q][2] != leaf
                        or not is_symmetry(steps[reverse].conclusion, quad.conclusion)
                        or not is_transitivity(steps[consumer].conclusion, steps[joined].conclusion, steps[reverse].conclusion)):
                    continue
                q_sources = root_ancestor_step_indices(steps, q)
                q_nums = {n for j in q_sources if steps[j].rule is ProofRule.GIVEN for n in model.step_citation_numbers[j]}
                if number not in q_nums or len(q_nums) != 3:
                    continue
                qtext = _rendered_sentence(quad)
                if qtext is None:
                    continue
                qline = ', '.join(f'[R{n}]' for n in sorted(q_nums-{number})) + 'を用いて, ' + qtext
                qi = unique(qline)
                if qi is None or qi <= mi or any(s.strip() for s in lines[mi+1:qi]):
                    continue
                new_summary = source_prefix(summary, set(nums)|{number})
                new_quad = source_prefix(qline, q_nums)
                if new_summary is None or new_quad is None:
                    continue
                candidates.append((wi, si, mi, qi, new_summary, new_quad, {
                    'chain_indices': list(indices), 'joined_index': joined,
                    'alias_index': alias, 'alias_nodes': sorted(nodes),
                    'witness_indices': sorted(witnesses), 'source_index': leaf,
                    'source_reference': number, 'quadruple_index': q,
                    'consumer_index': consumer, 'removed_sentences': [witness, merged],
                    'replacements': {summary: new_summary, qline: new_quad},
                }))
    if len(candidates) != 1:
        return markdown, {}
    wi, si, mi, qi, new_summary, new_quad, plan = candidates[0]
    output = list(lines)
    for i, replacement in sorted(((wi, None), (si, new_summary), (mi, None), (qi, new_quad)), reverse=True):
        if replacement is not None:
            output[i] = replacement
        else:
            del output[i]
            if i < len(output) and not output[i]:
                del output[i]
    projected = '\n'.join(output) + ('\n' if markdown.endswith('\n') else '')
    return projected, plan
