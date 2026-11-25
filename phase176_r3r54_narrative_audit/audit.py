"""Collect real narrative and typed ancestry; do not change proof or rendering."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import tempfile
from unittest.mock import patch

from phase176_r3r53_common_kernel_renderer import audit as prior
from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
PINS = {
    'phase168_r3_12_body_binding.py': 'ad8797c141216e410e81bafae284507f7797c3e4',
    'phase171_r20r13_eta_sentence_layout/projection.py': '5deaa8886f36ec967d52b9fcd603d135ae290b39',
    'phase172_r3_hopf_chain_display/projection.py': '3af8879b75dfcc45e67f02aa8fc94a31373e123b',
    'phase175_r3r11_cited_hopf_narrative/projection.py': 'a9ecbffc4b89c2da84bc523fd9388b44d476fb26',
    'phase176_r3r27r1_toda55_quadruple_isolated/source.py': '3e174ff8ffb656f069e1318591785bb7697c7736',
    'phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/rule.py': 'a2021644163c56cf20ff1899190f3f0330bd8275',
    'phase176_r3r53_common_kernel_renderer/audit.py': '1f6bf584e4b24066937be87f65f3649d54bf1d16',
}
MATH = re.compile(r'\$([^$\n]+)\$')
TAG = re.compile(r'\[R(\d+)\]')
HEADER = re.compile(r'^\*\*\[R(\d+)\] .+\*\*$')


def preflight():
    from phase176_r3r53r1_historical_kernel_test.apply import planned_changes
    head = prior.preflight()
    old, new = planned_changes()
    if old != new:
        raise RuntimeError('R3R53R1_NOT_APPLIED')
    for path, sha in PINS.items():
        text, _ = normalize((ROOT / path).read_bytes())
        if not pinned(text, sha):
            raise RuntimeError('UNREVIEWED_SOURCE:' + path)
    return head


def equations(text):
    """Only literal single-equality math spans; no semantic normalization."""
    values = []
    for value in MATH.findall(text):
        if value.count('=') != 1:
            continue
        left, right = (part.strip() for part in value.split('='))
        if left and right:
            values.append((left, right))
    return values


def inspect_markdown(markdown, step_rows):
    """Return candidate display matches, not asserted proof-step ownership."""
    lines = markdown.splitlines()
    if lines.count('証明') != 1:
        raise ValueError('EXPECTED_ONE_PROOF_BOUNDARY')
    boundary = lines.index('証明')
    refs = {}
    current = None
    for i, line in enumerate(lines[:boundary]):
        header = HEADER.fullmatch(line)
        if header:
            current = int(header.group(1))
            if current in refs:
                raise ValueError('DUPLICATE_REFERENCE_HEADER')
            refs[current] = {'header': line, 'line': i + 1, 'body': [], 'uses': []}
        elif current is not None and line.strip():
            refs[current]['body'].append(line)
    rows = []
    for i in range(boundary + 1, len(lines)):
        line = lines[i]
        if not line.strip():
            continue
        tags = [int(n) for n in TAG.findall(line)]
        for n in tags:
            if n not in refs:
                raise ValueError('UNKNOWN_BODY_REFERENCE:' + str(n))
            refs[n]['uses'].append(i + 1)
        spans = MATH.findall(line)
        candidates = [row['index'] for row in step_rows
                      if row['latex'] is not None and row['latex'] in spans]
        rows.append({'line': i + 1, 'text': line, 'citations': tags,
                     'equations': equations(line), 'candidate_step_indices': candidates})
    occurrences = {}
    for row in rows:
        for left, right in row['equations']:
            occurrences.setdefault((left, right), []).append(row['line'])
    identities = [{'equation': list(pair), 'lines': nums}
                  for pair, nums in occurrences.items() if pair[0] == pair[1]]
    repeats = [{'equation': list(pair), 'lines': nums}
               for pair, nums in occurrences.items() if len(nums) > 1]
    reversed_pairs = [{'equation': list(pair), 'lines': nums,
                       'reverse_lines': occurrences[pair[::-1]]}
                      for pair, nums in occurrences.items()
                      if pair[0] < pair[1] and pair[::-1] in occurrences]
    return {'references': refs, 'body_rows': rows, 'identities': identities,
            'repeated_equations': repeats, 'reversed_equations': reversed_pairs,
            'empty_reference_bodies': [n for n, r in refs.items() if not r['body']],
            'references_without_explicit_body_use': [n for n, r in refs.items() if not r['uses']]}


def snapshot(model):
    return (tuple((id(s), repr(s.conclusion), s.rule.value,
                   tuple(id(p) for p in s.premises)) for s in model.steps),
            repr(model.citations), model.step_citation_numbers, model.root_index)


def collect_steps(result, model):
    from phase168_r3_12_body_binding import build_narrative_body_lines
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from proof import ProofRule

    body = {r.step_index: r for r in build_narrative_body_lines(result, model)}
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    by_id = {id(step): i for i, step in enumerate(model.steps)}
    if len(by_id) != len(model.steps):
        raise RuntimeError('AMBIGUOUS_MODEL_STEP_IDENTITY')
    rows = []
    for i in sorted(scope):
        step = model.steps[i]
        ancestry = root_ancestor_step_indices(model.steps, i) | {i}
        source_indices = [j for j in sorted(ancestry) if model.steps[j].rule is ProofRule.GIVEN]
        rows.append({'index': i, 'type': type(step.conclusion).__name__,
                     'rule': step.rule.value, 'inference': getattr(step.inference_rule, 'name', None),
                     'conclusion': repr(step.conclusion),
                     'premises': [by_id[id(p)] for p in step.premises],
                     'latex': body[i].statement_latex if i in body else None,
                     'typed_sentence': typed_sentence(step.conclusion, step),
                     'direct_citations': list(model.step_citation_numbers[i]),
                     'given_ancestor_indices': source_indices,
                     'given_ancestor_citations': sorted({n for j in source_indices for n in model.step_citation_numbers[j]})})
    return rows


def observe():
    import phase168_r3_5_model_renderer as renderer
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import RULE_NAME

    captures = []
    original = renderer.render_model_backed_narrative_markdown

    def observed(result, model):
        before = snapshot(model)
        markdown = original(result, model)
        if before != snapshot(model):
            raise RuntimeError('MODEL_CHANGED_DURING_RENDER')
        if result.status is ProofSearchStatus.COMPLETE:
            rows = collect_steps(result, model)
            if before != snapshot(model):
                raise RuntimeError('MODEL_CHANGED_DURING_AUDIT')
            captures.append((result, model, markdown, rows))
        return markdown

    # Prior audit itself calls through the real Web entry, trust boundary and
    # common renderer; its checks are retained, including the accepted prefix.
    with patch.object(renderer, 'render_model_backed_narrative_markdown', observed):
        baseline, markdown, partial = prior.observe()
    if len(captures) != 1:
        raise RuntimeError('EXPECTED_ONE_COMPLETE_RENDER')
    result, model, actual, rows = captures[0]
    if actual != markdown or len(rows) != 62 or result.open_goals:
        raise RuntimeError('COMPLETE_BASELINE_CHANGED')
    diagnostics = inspect_markdown(markdown, rows)
    if set(diagnostics['references']) != {c.number for c in model.citations}:
        raise RuntimeError('REFERENCE_HEADER_SET_MISMATCH')
    lifts = [row for row in rows if row['inference'] == RULE_NAME]
    if len(lifts) != 1 or len(lifts[0]['premises']) != 5:
        raise RuntimeError('LIFT_WITNESSES_MISSING')
    lookup = {row['index']: row for row in rows}
    report = {'gate': 'PASS_R3R54_NARRATIVE_BASELINE_AUDITED',
              'status': result.status.value, 'open_goals': [], 'web_key': baseline['web_key'],
              'proof_steps': len(rows), 'inference_steps': baseline['trust_inference_count'],
              'given_steps': baseline['trust_given_count'], 'root_index': model.root_index,
              'model_unchanged': True, 'kernel_renderer_verified': baseline['common_kernel_renderer_used'],
              'citations': baseline['citation_rows'], 'diagnostics': diagnostics,
              'lift': lifts[0], 'lift_premises': [lookup[i] for i in lifts[0]['premises']],
              'steps': rows, 'new_math_rules': 0, 'new_given_registrations': 0,
              'production_changes': 0, 'full_pytest': 'NOT_RUN'}
    return report, markdown, partial


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    head = preflight()
    print('PHASE176_R3R54_HEAD=' + head)
    if args.dry_run:
        print('PHASE176_R3R54_GATE=PASS_R3R54_DRYRUN')
        return 0
    before = (prior.git('diff', '--binary', 'HEAD'), prior.git('status', '--porcelain'))
    report, markdown, partial = observe()
    after = (prior.git('diff', '--binary', 'HEAD'), prior.git('status', '--porcelain'))
    if before != after:
        raise RuntimeError('AUDIT_CHANGED_REPOSITORY')
    report.update(head=head, repository_unchanged=True)
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (folder / 'actual_narrative.md').write_text(markdown, encoding='utf-8')
    (folder / 'partial_prefix_narrative.md').write_text(partial, encoding='utf-8')
    for name in ('status', 'open_goals', 'proof_steps', 'inference_steps', 'given_steps', 'model_unchanged', 'repository_unchanged', 'full_pytest'):
        print('PHASE176_R3R54_' + name.upper() + '=' + json.dumps(report[name], ensure_ascii=False))
    for name in ('identities', 'repeated_equations', 'reversed_equations', 'empty_reference_bodies', 'references_without_explicit_body_use'):
        print('PHASE176_R3R54_' + name.upper() + '=' + json.dumps(report['diagnostics'][name], ensure_ascii=False))
    print('PHASE176_R3R54_LIFT_PREMISES=' + json.dumps([{k: row[k] for k in ('index', 'type', 'latex', 'direct_citations')} for row in report['lift_premises']], ensure_ascii=False))
    print('REPORT=' + str(folder / 'report.json'))
    print('NARRATIVE=' + str(folder / 'actual_narrative.md'))
    print('PHASE176_R3R54_GATE=' + report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
