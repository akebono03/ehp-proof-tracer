"""Display only source clauses and source tags already backed by a verified tree."""
from __future__ import annotations

import re

from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, root_ancestor_step_indices
from phase171_r2h_prop22_cited_hopf.source import (
    ASSERTION_ID as PROP_ASSERTION, REFERENCE_ID as PROP_REFERENCE, TodaProp22RightFormula,
)
from phase175_r3r9_lemma57_explicit_public.source import (
    ASSERTION_ID as ZERO_ASSERTION, REFERENCE_ID as ZERO_REFERENCE,
    PARTICULAR_CLAUSE, TodaLemma57ExplicitNuPrimeZero,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition, StableFamilyMemberDefinition,
)
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    ASSERTION_ID as QUAD_ASSERTION, REFERENCE_ID as QUAD_REFERENCE,
    Toda55UniversalQuadrupleStatement, quadruple_inputs,
)
from phase176_r3r36_composite_right_hopf_isolated.source import composite_right_formula_parts
from proof import ProofRule
from web_group_proof_common import _group_proof_statement_latex


def matches_registered_id(value: str, expected: str) -> bool:
    """Accept exact original ID or the shared bridge's numbered namespace."""
    return value == expected or re.fullmatch(r'shared:[0-9]+:' + re.escape(expected), value) is not None


def source_citation(model, scope, index, statement, assertion_id, reference_id, locator):
    """Require the actual cited source leaf, matching registry IDs and locator."""
    if index not in scope:
        return None
    step = model.steps[index]
    if (step.rule is not ProofRule.GIVEN or step.premises
            or type(step.conclusion) is not type(statement) or step.conclusion != statement):
        return None
    matches = [c for c in model.citations
               if c.reference.locator == locator and index in c.step_indices
               and c.number in model.step_citation_numbers[index]
               and any(matches_registered_id(a, assertion_id) for a in c.assertion_ids)
               and any(matches_registered_id(r, reference_id) for r in c.reference_ids)]
    return matches[0] if len(matches) == 1 else None


def insert_reference_clause(lines, citation, clause):
    """Append a missing clause within its own reference block, not the proof."""
    boundary = lines.index('証明')
    header = f'**[R{citation.number}] {citation.reference.locator}.**'
    matches = [i for i, line in enumerate(lines[:boundary]) if line == header]
    if len(matches) != 1:
        return
    start = matches[0]
    end = next((i for i in range(start + 1, boundary)
                if re.match(r'^\*\*\[R\d+\]', lines[i])), boundary)
    if clause in lines[start + 1:end]:
        return
    lines[end:end] = [clause, '']


def tag_exact_sentence(lines, old, new):
    """Edit one already emitted sentence only; refuse ambiguous or absent anchors."""
    boundary = lines.index('証明')
    matches = [i for i in range(boundary + 1, len(lines)) if lines[i] == old]
    if len(matches) == 1:
        lines[matches[0]] = new


def unique_rendered_relation(model, scope, index):
    """A source tag must not be assigned through an ambiguous rendered relation."""
    latex, fallback = _group_proof_statement_latex(model.steps[index].conclusion)
    if latex is None or fallback is not None:
        return None
    matches = [j for j in scope
               if _group_proof_statement_latex(model.steps[j].conclusion) == (latex, None)]
    return latex if matches == [index] else None


def project_cited_sources(markdown: str, model: ProofNarrativeModel) -> str:
    """No proof search, new premises or citation numbers; incomplete views unchanged."""
    if (not isinstance(model, ProofNarrativeModel) or model.status is not ProofSearchStatus.COMPLETE
            or model.open_goals or model.root_index is None
            or len(model.steps) != len(model.step_citation_numbers)):
        return markdown
    lines = markdown.splitlines()
    if lines.count('証明') != 1:
        return markdown
    try:
        scope = root_ancestor_step_indices(model.steps, model.root_index)
    except ValueError:
        return markdown
    indices = {id(s): i for i, s in enumerate(model.steps)}
    if len(indices) != len(model.steps):
        return markdown
    for i in sorted(scope):
        step = model.steps[i]
        zero = source_citation(model, scope, i, TodaLemma57ExplicitNuPrimeZero(),
                               ZERO_ASSERTION, ZERO_REFERENCE, 'Lemma 5.7')
        if zero is not None:
            insert_reference_clause(lines, zero, '$' + PARTICULAR_CLAUSE.replace(r'\circ', '') + '$.')
        quad = source_citation(model, scope, i, Toda55UniversalQuadrupleStatement(),
                               QUAD_ASSERTION, QUAD_REFERENCE, '(5.5)')
        if quad is not None:
            insert_reference_clause(lines, quad, r'$n\ge 5$ に対し, $4\nu_n=\eta_n^3$.')
        if step.rule is not ProofRule.INFERENCE or step.inference_rule is None:
            continue
        parents = step.premises
        if len(parents) == 1 and composite_right_formula_parts(step.conclusion) is not None:
            prop = source_citation(model, scope, indices.get(id(parents[0])), TodaProp22RightFormula(),
                                   PROP_ASSERTION, PROP_REFERENCE, 'Proposition 2.2')
            if prop is not None:
                latex = unique_rendered_relation(model, scope, i)
                if latex is not None:
                    sentence = f'${latex}$.'
                    tag_exact_sentence(lines, sentence, f'[R{prop.number}]より, ' + sentence)
        if len(parents) != 3:
            continue
        inputs = quadruple_inputs(step.conclusion)
        if inputs is None or tuple(p.conclusion for p in parents) != inputs:
            continue
        member, given, eta = parents
        if (member.rule is not ProofRule.INFERENCE or len(member.premises) != 1
                or type(member.conclusion) is not StableFamilyMemberDefinition
                or eta.rule is not ProofRule.GIVEN):
            continue
        family = member.conclusion.source
        if type(family) is not CitedStableFamilyDefinition:
            continue
        definition = source_citation(model, scope, indices.get(id(member.premises[0])), family,
            f'adopted:assertion:toda5:stable_family:{family.family_id}',
            f'adopted:reference:toda5:stable_family:{family.family_id}',
            'Chapter V, ν-family definition (after Lemma 5.5)')
        quad = source_citation(model, scope, indices.get(id(given)), Toda55UniversalQuadrupleStatement(),
                               QUAD_ASSERTION, QUAD_REFERENCE, '(5.5)')
        if definition is None or quad is None or quad.number not in model.step_citation_numbers[i]:
            continue
        latex = unique_rendered_relation(model, scope, i)
        if latex is not None:
            sentence = f'${latex}$.'
            tag_exact_sentence(lines, f'[R{quad.number}]を用いて, ' + sentence,
                               f'[R{definition.number}], [R{quad.number}]を用いて, ' + sentence)
    if lines == markdown.splitlines():
        return markdown
    return '\n'.join(lines) + ('\n' if markdown.endswith('\n') else '')
