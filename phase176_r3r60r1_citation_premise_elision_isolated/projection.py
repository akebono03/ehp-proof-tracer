"""Presentation-only direct formula citation and cited premise elision.

Apply only to complete, already trusted models. All original ProofSteps,
registry links and NarrativeCitation numbers remain unchanged. Display numbers
are local to this final Markdown projection, never used as proof evidence.
"""
from __future__ import annotations

import re

from phase165_r12_r20_eta_definition import (
    ASSERTION_ID as ETA_ASSERTION, REFERENCE_ID as ETA_REFERENCE,
    TodaEtaFamilyGeneralDefinition,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, root_ancestor_step_indices
from phase169_r10d2_general_family_definition.family_citation import canonical_member
from phase174_r3_r6_r3_common_narrative.projection import display_cited_nu_family_locator
from phase175_r3r9_lemma57_explicit_public import rule as lemma_rule, source as lemma_source
from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence
from phase176_r3r10_right_zero_transport_isolated import rule as transport
from phase176_r3r27r1_toda55_quadruple_isolated import source as quad
from phase176_r3r56_cited_source_display_isolated.projection import source_citation
from proof import ProofRule, find_inference_matches_for_rule

TAG = re.compile(r'\[R(\d+)\]')
HEADER = re.compile(r'^\*\*\[R(\d+)\] .+\*\*$')


def parse_display(markdown):
    """Return complete-body boundary and exact ordered reference blocks."""
    lines = markdown.splitlines()
    if lines.count('証明') != 1:
        return None
    boundary = lines.index('証明')
    starts = [(i, int(m[1])) for i, line in enumerate(lines[:boundary])
              if (m := HEADER.fullmatch(line)) is not None]
    numbers = [n for _, n in starts]
    if not starts or numbers != list(range(1, len(numbers)+1)):
        return None
    blocks = {n:(i, starts[k+1][0] if k+1 < len(starts) else boundary)
              for k,(i,n) in enumerate(starts)}
    if any(TAG.search(line) for line in lines[:starts[0][0]]):
        return None
    for start,end in blocks.values():
        if len(TAG.findall(lines[start])) != 1 or any(TAG.search(line) for line in lines[start+1:end]):
            return None
    if any(int(n) not in blocks for line in lines[boundary+1:] for n in TAG.findall(line)):
        return None
    return lines,boundary,blocks


def rewrite_display(markdown, removed, replacements, drop):
    """Exact body anchors, one authorized reference block, one-pass tag mapping.

    This helper is textual only: callers must first prove the typed eligibility
    of every edit and of the dropped reference. Return None on ambiguity.
    """
    parsed = parse_display(markdown)
    if parsed is None:
        return None
    lines,boundary,blocks = parsed
    anchors = list(removed)+list(replacements)
    if (not anchors or len(set(anchors)) != len(anchors) or drop not in blocks
            or any(not s for s in anchors)):
        return None
    for s in anchors:
        if lines[boundary+1:].count(s) != 1:
            return None
    body = list(lines[boundary+1:])
    for i in range(len(body)-1,-1,-1):
        s = body[i]
        if s in removed:
            del body[i]
            if i < len(body) and not body[i]:
                del body[i]
        elif s in replacements:
            body[i] = replacements[s]
    # Every retained source must still have a body citation, and the only
    # unused source must be precisely the certified auxiliary definition.
    used = {int(n) for s in body for n in TAG.findall(s)}
    if used != set(blocks)-{drop}:
        return None
    mapping = {n:i for i,n in enumerate((n for n in blocks if n != drop),1)}
    start,end = blocks[drop]
    prefix = lines[:start]+lines[end:boundary+1]
    # Restrict replacement to actual [R<number>] tokens. Never edit formula
    # indices, source locators, source bodies, or the model's citation objects.
    def remap(line):
        return TAG.sub(lambda m: f'[R{mapping[int(m[1])]}]',line)
    output = '\n'.join(remap(s) for s in prefix+body)
    if markdown.endswith('\n'):
        output += '\n'
    return output,mapping


def project_citation_premise_elision(markdown, model):
    """Return (Markdown, plan) or exact unchanged input on any missing guard."""
    if (not isinstance(model, ProofNarrativeModel) or model.status is not ProofSearchStatus.COMPLETE
            or model.open_goals or type(model.root_index) is not int
            or len(model.steps) != len(model.step_citation_numbers)):
        return markdown,{}
    parsed = parse_display(markdown)
    if parsed is None:
        return markdown,{}
    lines,boundary,blocks = parsed
    citations = {c.number:c for c in model.citations}
    if len(citations) != len(model.citations) or set(citations) != set(blocks):
        return markdown,{}
    try:
        scope = root_ancestor_step_indices(model.steps,model.root_index)
    except ValueError:
        return markdown,{}
    steps = model.steps
    lookup = {id(s):i for i,s in enumerate(steps)}
    if len(lookup) != len(steps):
        return markdown,{}
    parents = {i:tuple(lookup.get(id(p)) for p in steps[i].premises) for i in scope}
    if any(p not in scope or p >= i for i,ps in parents.items() for p in ps):
        return markdown,{}
    def users(i):
        return {j for j,ps in parents.items() if i in ps}
    def inferred(i,name,arity):
        step = steps[i]
        return (step.rule is ProofRule.INFERENCE and step.inference_rule is not None
                and step.inference_rule.name == name and len(parents[i]) == arity
                and bool(find_inference_matches_for_rule(step.inference_rule,step.premises)))
    def source_body(n):
        start,end = blocks[n]
        return tuple(s for s in lines[start+1:end] if s.strip())
    def unique(s):
        hits = [i for i in range(boundary+1,len(lines)) if lines[i] == s]
        return hits[0] if len(hits) == 1 else None
    def juxtapose(s):
        return s.replace(r'\circ ', '').replace(r'\circ', '')
    zeros,quads = [],[]
    for i in sorted(scope):
        if (i != model.root_index and inferred(i,lemma_rule.RULE_NAME,1)
                and not model.step_citation_numbers[i]
                and lemma_rule.exact_lemma57_zero_image_goal(steps[i].conclusion)):
            leaf, = parents[i]
            cite = source_citation(model,scope,leaf,lemma_source.TodaLemma57ExplicitNuPrimeZero(),
                                   lemma_source.ASSERTION_ID,lemma_source.REFERENCE_ID,'Lemma 5.7')
            if cite is not None and cite.number in blocks and len(users(i)) == 1:
                n = cite.number
                j, = users(i)
                quoted = '$'+juxtapose(lemma_source.PARTICULAR_CLAUSE)+'$.'
                if (quoted in source_body(n) and j != model.root_index
                        and not model.step_citation_numbers[j]
                        and inferred(j,transport.RULE_NAME,1) and parents[j] == (i,)
                        and transport.right_zero_transport_inputs(steps[j].conclusion,steps[i].conclusion) == (steps[i].conclusion,)):
                    base,text = _rendered_sentence(steps[i]),_rendered_sentence(steps[j])
                    if base is not None and text is not None and r'\circ' in text:
                        tag = f'[R{n}]より, '
                        old,retained = tag+juxtapose(base),tag+text
                        a,b = unique(old),unique(retained)
                        if a is not None and b is not None and a < b and not any(s.strip() for s in lines[a+1:b]):
                            zeros.append((old,retained,tag+juxtapose(text),leaf,i,j,n))
        if i == model.root_index or not inferred(i,quad.RULE_NAME,3):
            continue
        inputs = quad.quadruple_inputs(steps[i].conclusion)
        if inputs is None or tuple(p.conclusion for p in steps[i].premises) != inputs:
            continue
        member,leaf,eta = parents[i]
        if not inferred(member,'specialize cited stable-family definition',1):
            continue
        family_leaf, = parents[member]
        definition = steps[member].conclusion
        family = definition.source
        if canonical_member(family,definition.index) != definition:
            continue
        formula = source_citation(model,scope,leaf,quad.Toda55UniversalQuadrupleStatement(),
                                  quad.ASSERTION_ID,quad.REFERENCE_ID,'(5.5)')
        eta_cite = source_citation(model,scope,eta,TodaEtaFamilyGeneralDefinition(),
                                    ETA_ASSERTION,ETA_REFERENCE,'Chapter V, i)')
        family_cite = source_citation(model,scope,family_leaf,family,
            f'adopted:assertion:toda5:stable_family:{family.family_id}',
            f'adopted:reference:toda5:stable_family:{family.family_id}',
            'Chapter V, ν-family definition (after Lemma 5.5)')
        if any(c is None for c in (formula,eta_cite,family_cite)):
            continue
        n,e,f = formula.number,eta_cite.number,family_cite.number
        if len({n,e,f}) != 3 or not {n,e,f}.issubset(blocks):
            continue
        ancestry = root_ancestor_step_indices(steps,i)
        numbers = {k for j in ancestry if steps[j].rule is ProofRule.GIVEN for k in model.step_citation_numbers[j]}
        if numbers != {n,e,f} or set(model.step_citation_numbers[i]) != {n}:
            continue
        # The auxiliary family reference must have no other proof use or
        # attached claim. Check the actual source block, not the locator alone.
        if (users(family_leaf) != {member} or users(member) != {i}
                or set(family_cite.step_indices) != {family_leaf}
                or any(f in nums for j,nums in enumerate(model.step_citation_numbers) if j != family_leaf)
                or len(family_cite.assertion_ids) != 1 or len(family_cite.reference_ids) != 1):
            continue
        locator = display_cited_nu_family_locator(family_cite,model)
        start,_ = blocks[f]
        if (locator is None or lines[start] != f'**[R{f}] {locator}.**'
                or not family_cite.statement_bodies
                or source_body(f) != tuple(family_cite.statement_bodies)
                or r'$n\ge 5$ に対し, $4\nu_n=\eta_n^3$.' not in source_body(n)):
            continue
        text = _rendered_sentence(steps[i])
        if text is None:
            continue
        old = ', '.join(f'[R{k}]' for k in sorted(numbers))+'を用いて, '+text
        if unique(old) is None:
            continue
        quads.append((old,f'[R{n}]より, '+text,i,leaf,member,family_leaf,n,e,f))
    if len(zeros) != 1 or len(quads) != 1:
        return markdown,{}
    old,retained,new,zero_leaf,base,consumer,zero_ref = zeros[0]
    qold,qnew,qindex,qleaf,member,family_leaf,formula_ref,eta_ref,drop = quads[0]
    if drop in (zero_ref,formula_ref,eta_ref):
        return markdown,{}
    replacements = {retained:new,qold:qnew}
    changed = rewrite_display(markdown,[old],replacements,drop)
    if changed is None:
        return markdown,{}
    output,mapping = changed
    return output,{
        'zero_source_index':zero_leaf,'zero_base_index':base,'zero_consumer_index':consumer,
        'quadruple_index':qindex,'formula_source_index':qleaf,'member_index':member,
        'family_source_index':family_leaf,'removed_reference':drop,
        'display_number_map':mapping,'removed_sentences':[old],'replacements':replacements,
    }
