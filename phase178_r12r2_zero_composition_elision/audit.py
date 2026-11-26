"""Audit actual R12R2 renderer output against the unchanged verified tree."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

from phase178_r12r2_zero_composition_elision.installer import ROOT, TARGET, full_review_source, gt, preflight, require

PACKAGE = Path(__file__).parent.name
TESTS = (
    PACKAGE + '/tests/test_projection.py',
    'phase178_r12r1_suspension_composition_display/tests/test_projection.py',
    'phase178_r12_suspension_composition_audit/tests/test_audit.py',
    'phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py',
    'phase177_r17r6r1_suspension_composition_display/tests/test_display.py',
    'phase178_r11_hopf_zero_reason_display/tests/test_sentence_layout_audit.py',
)


def emit(key, value):
    print('PHASE178_R12R2_' + key + '=' + str(value), flush=True)


def inspect_actual(folder):
    import phase168_r3_5_model_renderer as renderer
    from phase178_r11_hopf_zero_reason_display.audit import inspect_actual as inspect_r11
    from phase178_r12_suspension_composition_audit.audit import inspect_model
    from phase178_r12r1_suspension_composition_display import projection as notation
    from phase178_r12r2_zero_composition_elision import projection

    real = renderer.render_model_backed_narrative_markdown
    original_projection = projection.project_zero_composition_elision
    calls, plans = [], []

    def observed(result, model):
        markdown = real(result, model)
        calls.append((result, model, markdown))
        return markdown

    def observed_projection(before, lines, model, protected):
        output, plan = original_projection(before, lines, model, protected)
        plans.append((list(before), list(lines), output, plan))
        return output, plan

    with patch.object(renderer, 'render_model_backed_narrative_markdown', observed), patch.object(projection, 'project_zero_composition_elision', observed_projection):
        summary = inspect_r11(folder)
    require(len(calls) == len(plans) == 1, 'RENDER_CAPTURE_MISSING_OR_AMBIGUOUS')
    result, model, after = calls[0]
    raw, normalized, output, plan = plans[0]
    before = '\n'.join(normalized).rstrip() + '\n'
    (folder / 'narrative_before.md').write_text(before, encoding='utf-8')
    (folder / 'narrative.md').write_text(after, encoding='utf-8')
    (folder / 'display_elisions.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    require(plan.get('retained_index') == 8 and plan.get('duplicate_index') == 16 and plan.get('consumer_index') == 17 and plan.get('base_index') == 7, 'AUDITED_TYPED_BRANCH_NOT_MATCHED')
    require(plan.get('base_display_absorbed') is True and len(plan['removed_positions']) == 2, 'EXPECTED_REFERENCE_AND_DUPLICATE_ELISION_NOT_APPLIED')
    require(after == '\n'.join(output).rstrip() + '\n', 'ACTUAL_WEB_OUTPUT_DIFFERS')
    before_model = (model.steps, model.citations, model.step_citation_numbers, model.root_index, model.open_goals)
    with patch.object(projection, 'project_zero_composition_elision', lambda before, lines, model, protected: (lines, {})):
        baseline = real(result, model)
        with patch.object(notation, 'project_zero_suspension_composition', lambda lines, model, protected: lines):
            raw_markdown = real(result, model)
    rows, candidates, edits, preview = inspect_model(model, raw_markdown)
    require(not candidates and len(edits) == 3 and preview == baseline == before, 'R12R1_BASELINE_CHANGED')
    require(before_model == (model.steps, model.citations, model.step_citation_numbers, model.root_index, model.open_goals), 'MODEL_CHANGED')
    boundary = normalized.index('証明')
    expected = list(normalized)
    for p in sorted(plan['removed_positions'], reverse=True):
        del expected[p:p + 2]
    require(output == expected and output[:boundary + 1] == normalized[:boundary + 1], 'UNEXPECTED_DISPLAY_CHANGE')
    first = r"[R4]より, $E(\eta_{2}\nu'\eta_{6})=0$."
    second = r"[R4]より, $E(\eta_{2}\nu'\eta_{6}^{2})=0$."
    base = r"[R4]より, $E(\eta_{2}\nu')=0$."
    body = output[boundary + 1:]
    require(body.count(first) == body.count(second) == 1 and body.index(first) < body.index(second) and base not in body, 'REQUESTED_BODY_DISPLAY_NOT_FOUND')
    emit('ROOT_STATUS', summary['status'])
    emit('ROOT_STEPS', summary['proven_step_count'])
    emit('ROOT_OPEN_GOALS', summary['open_goal_count'])
    emit('REFERENCES', len(model.citations))
    emit('TRUST_STATUS', summary['trust_status'])
    emit('TARGET_GIVEN_COUNT', summary['target_given_count'])
    emit('DUPLICATE_BODY_ELISIONS', 1)
    emit('REFERENCE_BODY_ELISIONS', 1)
    emit('PROOF_STEPS_REMOVED', 0)
    emit('DISPLAY_PLAN', json.dumps(plan, ensure_ascii=False))
    return dict(summary, display_plan=plan, proof_steps_removed=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_R12R2', 'dry_run': args.dry_run, 'new_math_rules': 0, 'new_given': 0, 'full_pytest': 'NOT_RUN'}
    original = None
    changed = False
    try:
        head, current, updated, source = preflight()
        report['head'] = head
        emit('HEAD', head)
        (folder / 'FUNCTION_AND_IMPORTS_FULL.py.txt').write_text(full_review_source(source), encoding='utf-8')
        (folder / 'FILE_FULL.py.txt').write_text(source, encoding='utf-8')
        emit('FULL_CODE', folder / 'FUNCTION_AND_IMPORTS_FULL.py.txt')
        if args.dry_run:
            report['gate'] = 'PASS_R12R2_READ_ONLY_DRYRUN'
        else:
            if current != updated:
                original = current
                (folder / 'renderer.before').write_bytes(current)
                changed = True
                (ROOT / TARGET).write_bytes(updated)
            report['audit'] = inspect_actual(folder)
            command = [sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--import-mode=importlib', *TESTS]
            report['focused_command'] = command
            subprocess.run(command, cwd=ROOT, check=True)
            check_head, check_current, check_updated, _ = preflight()
            require(check_head == head and check_current == check_updated == updated, 'POST_INSTALL_INTEGRITY_FAILED')
            gt('diff', '--check')
            report['gate'] = 'PASS_R12R2_ZERO_COMPOSITION_ELISION'
    except Exception as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
        if changed and original is not None:
            (ROOT / TARGET).write_bytes(original)
            report['renderer_restored'] = True
        emit('ERROR', repr(exc))
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    emit('REPORT', folder / 'report.json')
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
