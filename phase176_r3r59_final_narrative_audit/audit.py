"""Inspect real proof dependencies before any eta display change."""
from __future__ import annotations

import argparse
import difflib
import json
import os
from pathlib import Path
import re
import tempfile
from unittest.mock import patch

from phase165_r12_r20_eta_definition import (
    ASSERTION_ID, REFERENCE_ID, TodaEtaFamilyGeneralDefinition,
)
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase171_r20r13_eta_sentence_layout.projection import verified_eta_display_sentences
from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence
from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r56_cited_source_display_isolated.projection import source_citation
from phase176_r3r57_composite_hopf_display_isolated import projection as hopf
from phase176_r3r58r1_public_finite_cyclic_lift_display import apply as prior_apply, audit as prior
from phase176_r3r27r1_toda55_quadruple_isolated.source import quadruple_inputs
from proof import ProofRule

PACKAGE = Path(__file__).resolve().parent.name
ROOT = Path(__file__).resolve().parents[1]
PINS = {
    'phase165_r12_r20_eta_definition.py': '9d7058607c102c47265a192735180cac36321910',
    'phase176_r3r57_composite_hopf_display_isolated/projection.py': '2f54ed18b2729070b64f3b0613cc62a6f5f9dcf9',
    'phase176_r3r54_narrative_audit/audit.py': 'df62b1231e905ac66721be3b499644e8f11ba9f2',
    'phase176_r3r56_cited_source_display_isolated/projection.py': 'b61d4c7065db97b54efac529e2d9f709b840e01e',
}
TAG = re.compile(r'\[R(\d+)\]')


def preflight():
    if any(raw != new for raw, new in prior_apply.planned_changes().values()):
        raise RuntimeError('R58R1_NOT_APPLIED')
    for path, sha in PINS.items():
        if not pinned(normalize((ROOT / path).read_bytes())[0], sha):
            raise RuntimeError('UNREVIEWED_SOURCE:' + path)
    return baseline.prior.git('rev-parse', 'HEAD').decode('ascii').strip()


def unique_body_line(markdown, sentence):
    lines = markdown.splitlines()
    if lines.count('証明') != 1 or not sentence:
        return None
    boundary = lines.index('証明')
    found = [i for i in range(boundary + 1, len(lines)) if lines[i] == sentence]
    return found[0] if len(found) == 1 else None


def add_source_tag(line, number):
    """Audit preview only: require the existing exact citation prefix."""
    match = re.fullmatch(r'(\[R\d+\](?:, \[R\d+\])*)(を用いて, |より, )(\$.*\$\.)', line)
    if match is None:
        return None
    numbers = sorted({int(x) for x in TAG.findall(match[1])} | {number})
    return ', '.join(f'[R{n}]' for n in numbers) + 'を用いて, ' + match[3]


def preview(markdown, removed, replacements):
    """Exact unique body anchors only; never touch the reference section."""
    anchors = list(removed) + list(replacements)
    if len(set(anchors)) != len(anchors) or not anchors:
        return None
    positions = {s: unique_body_line(markdown, s) for s in anchors}
    if any(i is None for i in positions.values()):
        return None
    lines = markdown.splitlines()
    for s, i in sorted(positions.items(), key=lambda row: row[1], reverse=True):
        if s in replacements:
            lines[i] = replacements[s]
        else:
            del lines[i]
            if i < len(lines) and lines[i] == '':
                del lines[i]
    return '\n'.join(lines) + ('\n' if markdown.endswith('\n') else '')


def inspect_eta(model, actual, chain_plan):
    """Identify actual eta leaf, exact visible rows and their certified consumers."""
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    ancestors = {i: root_ancestor_step_indices(model.steps, i) for i in scope}
    eta_leaves = []
    for i in sorted(scope):
        step = model.steps[i]
        if type(step.conclusion) is TodaEtaFamilyGeneralDefinition:
            cite = source_citation(model, scope, i, TodaEtaFamilyGeneralDefinition(),
                                   ASSERTION_ID, REFERENCE_ID, 'Chapter V, i)')
            if cite is not None:
                eta_leaves.append((i, cite.number))
    findings = {'eta_sources': [{'step': i, 'reference': n} for i, n in eta_leaves],
                'chain_indices': chain_plan['chain_indices'], 'candidate_rows': [],
                'consumers': [], 'blockers': []}
    if len(eta_leaves) != 1:
        findings['blockers'].append('ETA_SOURCE_NOT_UNIQUE_OR_NOT_BOUND')
        return findings, None
    leaf, number = eta_leaves[0]
    final = chain_plan['chain_indices'][-1]
    match = hopf.match_chain(model, scope, final)
    if match is None or list(match[1]) != chain_plan['chain_indices']:
        raise RuntimeError('CHAIN_PLAN_NOT_REPLAYED')
    witness = chain_plan['retained_witness']
    summary = chain_plan['summary']
    image = match[1][0]
    if witness != _rendered_sentence(model.steps[image]):
        raise RuntimeError('WITNESS_NOT_TYPED_RENDERING')
    candidates = [(witness, [image])]
    # Match the actual merged line against the existing typed eta renderer.
    allowed = verified_eta_display_sentences(model)
    tag = f'[R{number}]より, '
    body = actual.split('\n証明\n', 1)[1].splitlines()
    for line in body:
        if not line.startswith(tag + '$') or not line.endswith('$.'):
            continue
        parts = line[len(tag)+1:-2].split(r',\quad ')
        if len(parts) < 2 or not all(tag + '$' + p + '$.' in allowed for p in parts):
            continue
        owners = []
        for part in parts:
            indices = [i for i in sorted(scope)
                       if model.steps[i].rule is ProofRule.INFERENCE
                       and leaf in ancestors[i]
                       and typed_sentence(model.steps[i].conclusion, model.steps[i]) == '$' + part + '$.']
            owners.append(indices)
        if any(len(indices) != 1 for indices in owners):
            findings['blockers'].append('ETA_MEMBER_OWNER_NOT_UNIQUE')
            continue
        candidates.append((line, [indices[0] for indices in owners]))
    consumers = [(summary, final)]
    for i in sorted(scope):
        step = model.steps[i]
        inputs = quadruple_inputs(step.conclusion)
        if (inputs is None or step.rule is not ProofRule.INFERENCE
                or tuple(p.conclusion for p in step.premises) != inputs):
            continue
        rendered = _rendered_sentence(step)
        if rendered is None:
            continue
        visible = [line for line in body if line.endswith(rendered) and TAG.match(line)]
        if len(visible) == 1:
            consumers.append((visible[0], i))
    for line, i in consumers:
        findings['consumers'].append({'line': line, 'step': i, 'eta_source_is_ancestor': leaf in ancestors[i]})
    used_consumers = set()
    for line, owners in candidates:
        rows = []
        for i in owners:
            targets = [j for _, j in consumers if i in ancestors[j] and i != j and leaf in ancestors[j]]
            rows.append({'step': i, 'rule': model.steps[i].inference_rule.name,
                         'eta_source_is_ancestor': leaf in ancestors[i],
                         'consumer_steps': targets,
                         'direct_users': [j for j in sorted(scope) if any(p is model.steps[i] for p in model.steps[j].premises)],
                         'direct_citations': list(model.step_citation_numbers[i])})
            if leaf not in ancestors[i] or not targets:
                findings['blockers'].append('ETA_DEPENDENCY_NOT_COVERED:' + str(i))
            used_consumers.update(targets)
        findings['candidate_rows'].append({'line': line, 'owners': rows})
    if len(candidates) != 2:
        findings['blockers'].append('EXPECTED_TWO_DISPLAY_ROWS_NOT_IDENTIFIED')
    if findings['blockers']:
        return findings, None
    replacements = {}
    for line, i in consumers:
        if i in used_consumers:
            changed = add_source_tag(line, number)
            if changed is None:
                findings['blockers'].append('CONSUMER_PREFIX_UNRECOGNIZED')
                return findings, None
            replacements[line] = changed
    if not replacements:
        findings['blockers'].append('NO_CERTIFIED_CONSUMER')
        return findings, None
    shadow = preview(actual, [line for line, _ in candidates], replacements)
    if shadow is None:
        findings['blockers'].append('DISPLAY_ANCHOR_NOT_UNIQUE')
        return findings, None
    findings['preview_replacements'] = replacements
    return findings, shadow


def observe():
    """Reuse R58R1 public audit and observe R57's actual hook on the same model."""
    captured, chains = [], []
    capture = prior.capture
    project = hopf.project_composite_hopf_chain

    def observed_capture():
        result = capture()
        captured.append(result)
        return result

    def observed_chain(markdown, model):
        output, plan = project(markdown, model)
        if plan:
            chains.append((model, plan))
        return output, plan

    with patch.object(prior, 'capture', observed_capture), patch.object(hopf, 'project_composite_hopf_chain', observed_chain):
        checked = prior.observe()
    if len(captured) != 1 or not chains:
        raise RuntimeError('PUBLIC_CAPTURE_MISSING')
    report, (result, model, actual), (_, partial_model, partial) = captured[0]
    same = [plan for owner, plan in chains if owner is model]
    if not same or any(plan != same[0] for plan in same):
        raise RuntimeError('HOPF_PLAN_CHANGED')
    snap = baseline.snapshot(model)
    findings, shadow = inspect_eta(model, actual, same[0])
    old = baseline.inspect_markdown(actual, report['steps'])
    if len(old['body_rows']) != 21 or checked['root_display_count'] != 1:
        raise RuntimeError('R58R1_BASELINE_CHANGED')
    new = None
    if shadow is not None:
        new = baseline.inspect_markdown(shadow, report['steps'])
        root = '以上より, ' + _rendered_sentence(model.steps[model.root_index])
        if (len(new['body_rows']) != 19 or new['references_without_explicit_body_use']
                or new['identities'] or new['repeated_equations'] or new['reversed_equations']
                or actual.split('\n証明\n', 1)[0] != shadow.split('\n証明\n', 1)[0]
                or shadow.count(root) != 1
                or any(shadow.count(s) != 1 for s in checked['plan']['added_sentences'])):
            findings['blockers'].append('PREVIEW_INVARIANT_FAILED')
            shadow = None
            new = None
    if snap != baseline.snapshot(model):
        raise RuntimeError('MODEL_MUTATED')
    zero_rows = [row for row in old['body_rows'] if r'\circ' in row['text']]
    for row in zero_rows:
        owners = [i for i in range(len(model.steps))
                  if (text := _rendered_sentence(model.steps[i])) is not None and row['text'].endswith(text)]
        row['typed_rendering_candidates'] = [report['steps'][i] for i in owners]
    outcome = {'gate': 'PASS_R3R59_FINAL_NARRATIVE_AUDIT',
               'status': result.status.value, 'web_key': report['web_key'],
               'proof_steps': report['proof_steps'], 'inference_steps': report['inference_steps'],
               'given_steps': report['given_steps'], 'citation_count': len(model.citations),
               'open_goals': [], 'body_rows': 21, 'preview_body_rows': len(new['body_rows']) if new else None,
               'eta_frontier': 'PREVIEW_AVAILABLE' if shadow is not None else 'DEPENDENCY_REVIEW_REQUIRED',
               'eta_findings': findings, 'composition_notation_findings': zero_rows,
               'model_unchanged': True, 'partial_render_unchanged': checked['partial_render_unchanged'],
               'production_changes': 0, 'new_math_rules': 0, 'new_given_registrations': 0,
               'public_connection': 'NOT_CHANGED', 'full_pytest': 'NOT_RUN'}
    return outcome, actual, shadow, partial, report['steps']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    head = preflight()
    print('PHASE176_R3R59_HEAD=' + head)
    if args.dry_run:
        print('PHASE176_R3R59_GATE=PASS_R3R59_DRYRUN')
        return 0
    git = baseline.prior.git
    before = (git('diff', '--binary', 'HEAD'), git('status', '--porcelain'))
    report, actual, shadow, partial, steps = observe()
    if before != (git('diff', '--binary', 'HEAD'), git('status', '--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
    report.update(head=head, repository_unchanged=True)
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    for name, content in [('actual_narrative.md', actual), ('partial.md', partial)]:
        (folder / name).write_text(content, encoding='utf-8')
    for name, data in [('report.json', report), ('steps.json', steps)]:
        (folder / name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for name in ('preview.md', 'narrative.diff'):
        (folder / name).unlink(missing_ok=True)
    if shadow is not None:
        (folder / 'preview.md').write_text(shadow, encoding='utf-8')
        (folder / 'narrative.diff').write_text(''.join(difflib.unified_diff(actual.splitlines(True), shadow.splitlines(True), fromfile='actual', tofile='preview')), encoding='utf-8')
    for key, value in report.items():
        if key not in ('gate', 'composition_notation_findings'):
            print('PHASE176_R3R59_' + key.upper() + '=' + json.dumps(value, ensure_ascii=False))
    print('REPORT=' + str(folder / 'report.json'))
    print('STEPS=' + str(folder / 'steps.json'))
    print('PHASE176_R3R59_GATE=' + report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
