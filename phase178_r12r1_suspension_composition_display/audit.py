"""Compare the installed renderer to the exact R12 preview on the same model."""
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

from phase178_r12r1_suspension_composition_display.installer import (
    ROOT, TARGET, full_review_source, gt, preflight, require,
)

PACKAGE = Path(__file__).parent.name
TESTS = (
    PACKAGE + '/tests/test_projection.py',
    'phase178_r12_suspension_composition_audit/tests/test_audit.py',
    'phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py',
    'phase177_r17r6r1_suspension_composition_display/tests/test_display.py',
    'phase178_r11_hopf_zero_reason_display/tests/test_sentence_layout_audit.py',
)


def emit(key, value):
    print('PHASE178_R12R1_' + key + '=' + str(value), flush=True)


def inspect_actual(folder):
    import phase168_r3_5_model_renderer as renderer
    from phase178_r11_hopf_zero_reason_display.audit import inspect_actual as inspect_r11
    from phase178_r12_suspension_composition_audit.audit import inspect_model
    from phase178_r12r1_suspension_composition_display import projection

    real = renderer.render_model_backed_narrative_markdown
    calls = []

    def observed(result, model):
        markdown = real(result, model)
        calls.append((result, model, markdown))
        return markdown

    with patch.object(renderer, 'render_model_backed_narrative_markdown', observed):
        summary = inspect_r11(folder)
    require(len(calls) == 1, 'RENDER_CAPTURE_MISSING_OR_AMBIGUOUS')
    result, model, after = calls[0]
    before_model = (model.steps, model.citations, model.step_citation_numbers, model.root_index, model.open_goals)
    with patch.object(projection, 'project_zero_suspension_composition', lambda lines, model, protected: lines):
        before = real(result, model)
    rows, candidates, edits, preview = inspect_model(model, before)
    require(not candidates and len(edits) == 3, 'R12_PREVIEW_CONTRACT_CHANGED')
    (folder / 'narrative_before.md').write_text(before, encoding='utf-8')
    (folder / 'notation_preview.md').write_text(preview, encoding='utf-8')
    (folder / 'narrative.md').write_text(after, encoding='utf-8')
    (folder / 'display_edits.json').write_text(json.dumps(edits, ensure_ascii=False, indent=2), encoding='utf-8')
    require(after == preview, 'ACTUAL_RENDERER_DIFFERS_FROM_R12_PREVIEW')
    require(before_model == (model.steps, model.citations, model.step_citation_numbers, model.root_index, model.open_goals), 'MODEL_CHANGED')
    require(len(after.splitlines()) == len(before.splitlines()), 'BODY_LINE_COUNT_CHANGED')
    for edit in edits:
        emit('NOTATION_EDIT', json.dumps(edit, ensure_ascii=False))
    emit('ROOT_STATUS', summary['status'])
    emit('ROOT_STEPS', summary['proven_step_count'])
    emit('ROOT_OPEN_GOALS', summary['open_goal_count'])
    emit('REFERENCES', len(model.citations))
    emit('TRUST_STATUS', summary['trust_status'])
    emit('TARGET_GIVEN_COUNT', summary['target_given_count'])
    emit('NOTATION_EDITS', len(edits))
    emit('ELIDED_STEPS', 0)
    return dict(summary, edits=edits, elided_steps=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_R12R1', 'dry_run': args.dry_run, 'new_math_rules': 0, 'new_given': 0, 'full_pytest': 'NOT_RUN'}
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
            report['gate'] = 'PASS_R12R1_READ_ONLY_DRYRUN'
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
            report['gate'] = 'PASS_R12R1_SUSPENSION_COMPOSITION_DISPLAY'
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
