"""Run an isolated candidate against the very same verified Web proof model."""
from __future__ import annotations

import argparse
import ast
from types import SimpleNamespace
import difflib
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r55_equality_display_isolated.projection import project_redundant_equalities

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
RENDERER = ROOT / 'phase168_r3_5_model_renderer.py'
PINS = {
    'phase168_r3_5_model_renderer.py': 'f77616cf4ccc734954754e6e5d3a8d8b550dfef1',
    'phase172_r2_suspension_relation_display/projection.py': 'bba6280a36ca1c094be1b2a65d94ba0d2582c7a1',
    'phase176_r3r50_strict_nu_prime_connection/notation.py': '2ed8c8b3ee8324ad7f37a61371e8b7323f2bd85c',
    'phase174_r3_r6_r3_common_narrative/projection.py': '82bafa9794d8273875fc90f968f2fa8ecbc7b233',
    'phase165_r12_r2_quotient_rules.py': '2b3e8e0449382e9245ee22f08501e9cede0a5b59',
}
ANCHOR = '    for index in order:\n        if order_summary is not None and index == model.root_index:\n'
INSERT = '''    if not incomplete:
        protected_equalities = set()
        if order_summary is not None:
            protected_equalities.update(order)
        if direct_sum_display is not None:
            protected_equalities.add(direct_sum_display.root_index)
        if stable_chain_display is not None:
            protected_equalities.add(stable_chain_display.root_index)
        if hopf_display is not None:
            protected_equalities.update((hopf_display.formula_index, hopf_display.image_index))
        suppressed_body_indices.update(_r55_observe_projection(
            model, order, suppressed_body_indices, protected_equalities,
        ))
'''
# Expected indices are regression checks for the uploaded R54 evidence only.
# The projection itself contains no dimensions, indices or expected formulas.
EXPECTED = {18, 33, 34, 40, 41, 47, 48, 49, 50, 51, 52, 57, 59, 60}


def candidate_function_source():
    raw, _ = normalize(RENDERER.read_bytes())
    if not pinned(raw, PINS[RENDERER.name]) or raw.count(ANCHOR) != 1:
        raise RuntimeError('UNREVIEWED_RENDERER_OR_ANCHOR')
    changed = raw.replace(ANCHOR, INSERT + ANCHOR, 1)
    nodes = [node for node in ast.parse(changed).body
             if isinstance(node, ast.FunctionDef)
             and node.name == 'render_model_backed_narrative_markdown']
    if len(nodes) != 1 or INSERT.rstrip() not in ast.get_source_segment(changed, nodes[0]):
        raise RuntimeError('SHADOW_INSERT_OUTSIDE_RENDER_FUNCTION')
    return changed, nodes[0]


def preflight():
    head = baseline.preflight()
    for path, sha in PINS.items():
        text, _ = normalize((ROOT / path).read_bytes())
        if not pinned(text, sha):
            raise RuntimeError('UNREVIEWED_SOURCE:' + path)
    candidate_function_source()
    return head


def shadow_renderer():
    import phase168_r3_5_model_renderer as renderer

    source, node = candidate_function_source()
    records = []

    def observed(model, order, hidden, protected):
        plan = project_redundant_equalities(model, order, hidden, protected)
        records.append({'planned': plan, 'order': list(order),
                        'previously_hidden': sorted(hidden), 'protected': sorted(protected)})
        return plan

    # The production module and its global function are not changed.
    namespace = dict(vars(renderer))
    namespace['_r55_observe_projection'] = observed
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<R3R55 shadow renderer>', 'exec'), namespace)
    return namespace[node.name], records, ast.get_source_segment(source, node)


def compare_display(before, after, rows):
    old = baseline.inspect_markdown(before, rows)
    new = baseline.inspect_markdown(after, rows)
    if before.split('\n証明\n', 1)[0] != after.split('\n証明\n', 1)[0]:
        raise RuntimeError('REFERENCE_SECTION_CHANGED')
    old_uses = {n for n, row in old['references'].items() if row['uses']}
    new_uses = {n for n, row in new['references'].items() if row['uses']}
    if old_uses != new_uses:
        raise RuntimeError('EXPLICIT_REFERENCE_USE_CHANGED')
    if new['identities'] or new['repeated_equations'] or new['reversed_equations']:
        raise RuntimeError('EXPECTED_EQUALITY_CLEANUP_INCOMPLETE')
    if not after.rstrip().endswith('□'):
        raise RuntimeError('ROOT_END_MARKER_MISSING')
    return old, new


def observe():
    import phase168_r3_5_model_renderer as renderer
    from phase165_r52_partial_proof import ProofSearchStatus

    captures = []
    original = renderer.render_model_backed_narrative_markdown

    def capture(result, model):
        markdown = original(result, model)
        captures.append((result, model, markdown))
        return markdown

    # R54/R53 still run their public search and trust checks unchanged.
    with patch.object(renderer, 'render_model_backed_narrative_markdown', capture):
        report, before, partial = baseline.observe()
    complete = [(r,m,t) for r,m,t in captures if r.status is ProofSearchStatus.COMPLETE]
    incomplete = [(r,m,t) for r,m,t in captures if r.status is not ProofSearchStatus.COMPLETE]
    if len(complete) != 1 or len(incomplete) != 1:
        raise RuntimeError('UNEXPECTED_BASELINE_CAPTURE_COUNT')
    result, model, text = complete[0]
    if text != before or incomplete[0][2] != partial:
        raise RuntimeError('BASELINE_CAPTURE_MISMATCH')
    snapshot = baseline.snapshot(model)
    shadow, plans, source = shadow_renderer()
    after = shadow(result, model)
    if baseline.snapshot(model) != snapshot or result.open_goals:
        raise RuntimeError('MODEL_CHANGED')
    if len(plans) != 1:
        raise RuntimeError('EXPECTED_ONE_SHADOW_PLAN')
    plan = plans[0]['planned']
    # Save evidence even if the proposed general conditions did not cover all findings.
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'before.md').write_text(before, encoding='utf-8')
    (folder / 'shadow.md').write_text(after, encoding='utf-8')
    (folder / 'shadow_renderer_FULL.py.txt').write_text(source + '\n', encoding='utf-8')
    (folder / 'plan.json').write_text(json.dumps(plans[0], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (folder / 'narrative.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='before', tofile='shadow')), encoding='utf-8')
    print('PHASE176_R3R55_PLANNED=' + json.dumps(plan, ensure_ascii=False), flush=True)
    print('ARTIFACTS=' + str(folder), flush=True)
    if set(plan) != EXPECTED:
        raise RuntimeError('UNEXPECTED_PLAN: missing=' + str(sorted(EXPECTED - set(plan))) + ', extra=' + str(sorted(set(plan) - EXPECTED)))
    order = tuple(plans[0]['order'])
    prior_hidden = set(plans[0]['previously_hidden'])
    protected = set(plans[0]['protected'])
    if {18, 59, 60}.intersection(project_redundant_equalities(
            model, order, prior_hidden, protected | {18, 59, 60})):
        raise RuntimeError('PROTECTED_STEP_SUPPRESSED')
    if 33 in project_redundant_equalities(model, order, prior_hidden | {29}, protected):
        raise RuntimeError('HIDDEN_WITNESS_USED')
    cited = list(model.step_citation_numbers)
    cited[18] = (6,)
    cited_fixture = SimpleNamespace(status=model.status, open_goals=model.open_goals,
                                    steps=model.steps, root_index=model.root_index,
                                    step_citation_numbers=tuple(cited))
    if 18 in project_redundant_equalities(cited_fixture, order, prior_hidden, protected):
        raise RuntimeError('CITED_STEP_SUPPRESSED')
    if baseline.snapshot(model) != snapshot:
        raise RuntimeError('MODEL_CHANGED_DURING_NEGATIVE_CHECKS')
    old, new = compare_display(before, after, report['steps'])
    by_index = {row['index']: row for row in report['steps']}
    body = after.split('\n証明\n', 1)[1]
    for i in (0, 10, 11, 12, 13, 17, 20, 21, 25, 56, 58, 61):
        latex = by_index[i]['latex']
        if latex is None or latex not in body:
            raise RuntimeError('RETAINED_WITNESS_MISSING:' + str(i))
    for i in (29, 36, 43):
        math = by_index[i]['typed_sentence'].split('$')[1]
        if math not in body:
            raise RuntimeError('CITED_SUSPENSION_WITNESS_MISSING:' + str(i))
    r, m, t = incomplete[0]
    partial_snapshot = baseline.snapshot(m)
    if shadow(r, m) != t or len(plans) != 1 or baseline.snapshot(m) != partial_snapshot:
        raise RuntimeError('PARTIAL_RENDER_CHANGED')
    summary = {'gate': 'PASS_R3R55_ISOLATED_EQUALITY_PROJECTION', 'status': result.status.value,
               'proof_steps': report['proof_steps'], 'inference_steps': report['inference_steps'],
               'given_steps': report['given_steps'], 'open_goals': [], 'citation_count': len(model.citations),
               'suppressed_indices': sorted(plan), 'reasons': plan,
               'identities_before': sum(len(x['lines']) for x in old['identities']),
               'identities_after': len(new['identities']),
               'repeated_equations_after': new['repeated_equations'],
               'reversed_equations_after': new['reversed_equations'],
               'reference_section_unchanged': True, 'explicit_reference_use_set_unchanged': True,
               'model_unchanged': True, 'partial_render_unchanged': True,
               'negative_projection_guards_passed': True, 'production_changes': 0, 'new_math_rules': 0, 'new_given_registrations': 0,
               'public_connection': 'NOT_APPLIED', 'full_pytest': 'NOT_RUN'}
    return summary, folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    head = preflight()
    print('PHASE176_R3R55_HEAD=' + head)
    if args.dry_run:
        print('PHASE176_R3R55_GATE=PASS_R3R55_DRYRUN')
        return 0
    before = (baseline.prior.git('diff', '--binary', 'HEAD'), baseline.prior.git('status', '--porcelain'))
    report, folder = observe()
    after = (baseline.prior.git('diff', '--binary', 'HEAD'), baseline.prior.git('status', '--porcelain'))
    if before != after:
        raise RuntimeError('REPOSITORY_CHANGED')
    report.update(head=head, repository_unchanged=True)
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for k,v in report.items():
        if k != 'gate':
            print('PHASE176_R3R55_' + k.upper() + '=' + json.dumps(v, ensure_ascii=False))
    print('REPORT=' + str(folder / 'report.json'))
    print('PHASE176_R3R55_GATE=' + report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
