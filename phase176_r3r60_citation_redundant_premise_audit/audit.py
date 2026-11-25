"""Read-only audit of direct formula citation and redundant cited zero premise."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import tempfile

from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase175_r3r9_lemma57_explicit_public import rule as lemma_rule, source as lemma_source
from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence
from phase176_r3r10_right_zero_transport_isolated import rule as transport
from phase176_r3r27r1_toda55_quadruple_isolated import source as quad
from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r56_cited_source_display_isolated.projection import source_citation
from phase176_r3r57_composite_hopf_display_isolated.audit import capture
from phase176_r3r59r4_public_definitional_suspension_elision.apply import planned_changes
from proof import ProofRule, find_inference_matches_for_rule

PACKAGE = Path(__file__).resolve().parent.name
ROOT = Path(__file__).resolve().parents[1]
PINS = {
    'phase175_r3r9_lemma57_explicit_public/rule.py': '7dc500d1ad3125378f7b13be26ca619c69cd46b0',
    'phase175_r3r9_lemma57_explicit_public/source.py': '0dbd07c4dbca7e3b3fcbbabf94126e111e21b1ab',
    'phase175_r3r11_cited_hopf_narrative/projection.py': '76eb3c474dc7c7f7f8b97629adfaf69b87a8c5b0',
    'phase176_r3r10_right_zero_transport_isolated/rule.py': '261501eec8358c0777fba089f1251e56b333bf21',
    'phase176_r3r27r1_toda55_quadruple_isolated/source.py': '3e174ff8ffb656f069e1318591785bb7697c7736',
}
TAG = re.compile(r'\[R(\d+)\]')


def preflight():
    if any(raw != new for raw, new in planned_changes().values()):
        raise RuntimeError('R59R4_NOT_APPLIED')
    for path, sha in PINS.items():
        if not pinned(normalize((ROOT / path).read_bytes())[0], sha):
            raise RuntimeError('UNREVIEWED_SOURCE:' + path)
    return baseline.prior.git('rev-parse', 'HEAD').decode('ascii').strip()


def juxtaposition(sentence):
    return sentence.replace(r'\circ ', '').replace(r'\circ', '')


def row_for(rows, sentence):
    hits = [row for row in rows if row['text'] == sentence]
    return hits[0] if len(hits) == 1 else None


def usage_after(rows, removed, replacements):
    """Text-only diagnostic, never a proof of source dependency."""
    return sorted({int(n) for row in rows if row['text'] not in removed
                   for n in TAG.findall(replacements.get(row['text'], row['text']))})


def inspect_candidates(model, diagnostics):
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    steps = model.steps
    lookup = {id(s): i for i, s in enumerate(steps)}
    if len(lookup) != len(steps):
        raise RuntimeError('AMBIGUOUS_STEP_IDENTITY')
    parents = {i: tuple(lookup.get(id(p)) for p in steps[i].premises) for i in scope}
    if any(p not in scope or p >= i for i, ps in parents.items() for p in ps):
        raise RuntimeError('INVALID_PREMISE_EDGE')
    rows, refs = diagnostics['body_rows'], diagnostics['references']

    def inferred(i, name, arity):
        step = steps[i]
        return (step.rule is ProofRule.INFERENCE and step.inference_rule is not None
                and step.inference_rule.name == name and len(parents[i]) == arity
                and bool(find_inference_matches_for_rule(step.inference_rule, step.premises)))

    zeros, quads = [], []
    for i in sorted(scope):
        if inferred(i, lemma_rule.RULE_NAME, 1) and lemma_rule.exact_lemma57_zero_image_goal(steps[i].conclusion):
            leaf, = parents[i]
            cite = source_citation(model, scope, leaf, lemma_source.TodaLemma57ExplicitNuPrimeZero(),
                                   lemma_source.ASSERTION_ID, lemma_source.REFERENCE_ID, 'Lemma 5.7')
            if cite is None:
                continue
            n = cite.number
            base = _rendered_sentence(steps[i])
            if base is None:
                continue
            quoted = '$' + juxtaposition(lemma_source.PARTICULAR_CLAUSE) + '$.'
            if quoted not in refs[n]['body']:
                continue
            old = f'[R{n}]より, ' + juxtaposition(base)
            old_row = row_for(rows, old)
            users = sorted(j for j, ps in parents.items() if i in ps)
            if old_row is None or len(users) != 1 or model.step_citation_numbers[i]:
                continue
            j, = users
            if not inferred(j, transport.RULE_NAME, 1) or parents[j] != (i,):
                continue
            if transport.right_zero_transport_inputs(steps[j].conclusion, steps[i].conclusion) != (steps[i].conclusion,):
                continue
            text = _rendered_sentence(steps[j])
            if text is None:
                continue
            retained = f'[R{n}]より, ' + text
            retained_row = row_for(rows, retained)
            if retained_row is None or retained_row['line'] <= old_row['line']:
                continue
            zeros.append({'source_index':leaf,'reference':n,'base_index':i,'consumer_index':j,
                          'base_direct_users':users,'consumer_direct_users':sorted(k for k, ps in parents.items() if j in ps),
                          'source_clause':quoted,'remove':old,'replace':retained,
                          'candidate':f'[R{n}]より, ' + juxtaposition(text)})
        if not inferred(i, quad.RULE_NAME, 3):
            continue
        inputs = quad.quadruple_inputs(steps[i].conclusion)
        if inputs is None or tuple(p.conclusion for p in steps[i].premises) != inputs:
            continue
        member, leaf, eta = parents[i]
        cite = source_citation(model, scope, leaf, quad.Toda55UniversalQuadrupleStatement(),
                               quad.ASSERTION_ID, quad.REFERENCE_ID, '(5.5)')
        if cite is None or cite.number not in model.step_citation_numbers[i]:
            continue
        ancestry = root_ancestor_step_indices(steps, i)
        numbers = {n for j in ancestry if steps[j].rule is ProofRule.GIVEN for n in model.step_citation_numbers[j]}
        if len(numbers) != 3 or cite.number not in numbers:
            continue
        text = _rendered_sentence(steps[i])
        if text is None:
            continue
        old = ', '.join(f'[R{n}]' for n in sorted(numbers)) + 'を用いて, ' + text
        if row_for(rows, old) is None:
            continue
        quads.append({'step_index':i,'premises':[member,leaf,eta], 'reference':cite.number,
                      'all_ancestor_citations':sorted(numbers),'auxiliary_citations':sorted(numbers-{cite.number}),
                      'source_body':refs[cite.number]['body'],'replace':old,
                      'candidate':f'[R{cite.number}]より, ' + text})
    findings = {'zero_candidates':zeros,'quadruple_candidates':quads,'blockers':[]}
    if len(zeros) != 1 or len(quads) != 1:
        findings['blockers'].append('EXPECTED_UNIQUE_TYPED_CANDIDATES_NOT_FOUND')
        return findings
    z, q = zeros[0], quads[0]
    removed = [z['remove']]
    replacements = {z['replace']:z['candidate'], q['replace']:q['candidate']}
    used = usage_after(rows, removed, replacements)
    unused = sorted(set(refs)-set(used))
    findings.update(candidate_body_rows=len(rows)-1, candidate_body_citations=used,
                    reference_headers_without_body_use=unused,
                    auxiliary_reference_headers=[refs[n]['header'] for n in unused],
                    other_uses={str(n):refs[n]['uses'] for n in q['auxiliary_citations']},
                    proposed_body_removals=removed, proposed_body_replacements=replacements,
                    reference_list_policy='REVIEW_REQUIRED_NO_REMOVAL_OR_RENUMBERING')
    return findings


def observe():
    report, (result, model, actual), (partial_result, partial_model, partial) = capture()
    snap = baseline.snapshot(model)
    diagnostics = baseline.inspect_markdown(actual, report['steps'])
    if ((report['proof_steps'], report['inference_steps'], report['given_steps']) != (62,51,11)
            or len(model.citations) != 10 or result.open_goals or result.status.value != 'complete'
            or report['web_key'] != 'generic-complete-proof' or len(diagnostics['body_rows']) != 19
            or diagnostics['references_without_explicit_body_use']):
        raise RuntimeError('R59R4_BASELINE_CHANGED')
    findings = inspect_candidates(model, diagnostics)
    import phase168_r3_5_model_renderer as renderer
    if (renderer.render_model_backed_narrative_markdown(result, model) != actual
            or renderer.render_model_backed_narrative_markdown(partial_result, partial_model) != partial
            or baseline.snapshot(model) != snap):
        raise RuntimeError('MODEL_OR_RENDER_CHANGED')
    return {'gate':'PASS_R3R60_CITATION_REDUNDANT_PREMISE_AUDIT', 'status':result.status.value,
            'proof_steps':62,'inference_steps':51,'given_steps':11,'citation_count':10,
            'open_goals':[], 'body_rows':19, 'findings':findings,
            'frontier':'TYPED_CANDIDATES_CONFIRMED' if not findings['blockers'] else 'DEPENDENCY_REVIEW_REQUIRED',
            'production_changes':0,'new_math_rules':0,'new_given_registrations':0,
            'model_unchanged':True,'partial_render_unchanged':True,'public_connection':'NOT_CHANGED',
            'full_pytest':'NOT_RUN'}, actual, partial, report['steps']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    head = preflight()
    print('PHASE176_R3R60_HEAD='+head)
    if args.dry_run:
        print('PHASE176_R3R60_GATE=PASS_R3R60_DRYRUN')
        return 0
    git = baseline.prior.git
    before = (git('diff','--binary','HEAD'),git('status','--porcelain'))
    report, actual, partial, steps = observe()
    if before != (git('diff','--binary','HEAD'),git('status','--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
    report.update(head=head, repository_unchanged=True)
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True,exist_ok=True)
    for name, content in [('actual_narrative.md',actual),('partial.md',partial)]:
        (folder/name).write_text(content,encoding='utf-8')
    for name,data in [('report.json',report),('steps.json',steps)]:
        (folder/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for key,value in report.items():
        if key != 'gate':
            print('PHASE176_R3R60_'+key.upper()+'='+json.dumps(value,ensure_ascii=False))
    print('REPORT='+str(folder/'report.json'))
    print('PHASE176_R3R60_GATE='+report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
