"""Verify the public hook against the independent projection on the same tree."""
from __future__ import annotations

from dataclasses import replace
import difflib
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r57_composite_hopf_display_isolated.audit import capture
from phase176_r3r58_finite_cyclic_lift_display_isolated import projection
from phase176_r3r58r1_public_finite_cyclic_lift_display.apply import planned_changes

PACKAGE = Path(__file__).resolve().parent.name


def artifact_folder():
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def observe():
    project = projection.project_finite_cyclic_lift
    calls = []

    def observed(markdown, model):
        original = baseline.snapshot(model)
        output, plan = project(markdown, model)
        if original != baseline.snapshot(model):
            raise RuntimeError('MODEL_CHANGED_IN_PUBLIC_HOOK')
        calls.append((markdown, model, output, plan))
        return output, plan

    with patch.object(projection, 'project_finite_cyclic_lift', observed):
        report, (result, model, actual), (partial_result, partial_model, partial) = capture()
    if len(calls) != 1 or calls[0][1] is not model:
        raise RuntimeError('PUBLIC_HOOK_NOT_OBSERVED')
    hook_input, _, output, plan = calls[0]
    before = hook_input.rstrip() + '\n'
    if output.rstrip() + '\n' != actual:
        raise RuntimeError('WEB_DIFFERS_FROM_HOOK')
    snap = baseline.snapshot(model)
    if (plan.get('lift_index'), plan.get('root_index'), plan.get('premise_indices'),
            plan.get('exactness_reference'), plan.get('codomain_order'),
            plan.get('kernel_multiple'), plan.get('subgroup_order')) != (60,61,[7,9,10,13,59],3,8,4,2):
        raise RuntimeError('EXPECTED_CERTIFIED_LIFT_NOT_PROJECTED')
    if before == actual or project(before, model) != (actual, plan):
        raise RuntimeError('PUBLIC_DIFFERS_FROM_ISOLATED_PROJECTION')
    reasons = plan['added_sentences']
    if len(reasons) != 3 or any(actual.count(reason) != 1 for reason in reasons):
        raise RuntimeError('REASON_MISSING_OR_REPEATED')
    from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence
    root = '以上より, ' + _rendered_sentence(model.steps[model.root_index])
    if actual.count(root) != 1 or actual.replace(''.join(reason + '\n\n' for reason in reasons), '', 1) != before:
        raise RuntimeError('NOT_EXACTLY_THREE_INSERTIONS_BEFORE_ROOT')
    if ''.join(reason + '\n\n' for reason in reasons) + root not in actual:
        raise RuntimeError('REASONS_NOT_IMMEDIATELY_BEFORE_ROOT')
    import phase168_r3_5_model_renderer as renderer
    with patch.object(projection, 'project_finite_cyclic_lift', lambda markdown, model: (markdown, {})):
        if renderer.render_model_backed_narrative_markdown(result, model) != before:
            raise RuntimeError('DISABLED_HOOK_BASELINE_MISMATCH')
        if renderer.render_model_backed_narrative_markdown(partial_result, partial_model) != partial:
            raise RuntimeError('PARTIAL_RENDER_CHANGED')
    if (project(actual, model) != (actual, {}) or project(partial, partial_model) != (partial, {})
            or project(before, replace(model, citations=())) != (before, {})):
        raise RuntimeError('IDEMPOTENCE_OR_NEGATIVE_GUARD_FAILED')
    old = baseline.inspect_markdown(before, report['steps'])
    new = baseline.inspect_markdown(actual, report['steps'])
    if (before.split('\n証明\n', 1)[0] != actual.split('\n証明\n', 1)[0]
            or new['references_without_explicit_body_use'] or new['identities']
            or new['repeated_equations'] or new['reversed_equations']
            or new['empty_reference_bodies'] != [1,4,5]
            or (len(old['body_rows']), len(new['body_rows'])) != (18,21)
            or (report['proof_steps'], report['inference_steps'], report['given_steps']) != (62,51,11)
            or len(model.citations) != 10 or result.open_goals or baseline.snapshot(model) != snap
            or result.status.value != 'complete' or report['web_key'] != 'generic-complete-proof'):
        raise RuntimeError('PUBLIC_INVARIANT_CHANGED')
    folder = artifact_folder()
    for name, content in [('before.md', before), ('actual_narrative.md', actual), ('partial.md', partial)]:
        (folder / name).write_text(content, encoding='utf-8')
    (folder / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (folder / 'narrative.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True), actual.splitlines(True), fromfile='before', tofile='public')), encoding='utf-8')
    return {'gate':'PASS_R3R58R1_PUBLIC_FINITE_CYCLIC_LIFT_DISPLAY_CONNECTED',
            'status':result.status.value, 'web_key':report['web_key'], 'proof_steps':62,
            'inference_steps':51, 'given_steps':11, 'citation_count':10, 'open_goals':[],
            'plan':plan, 'body_rows_before':18, 'body_rows_after':21,
            'reference_section_unchanged':True, 'references_without_explicit_body_use':[],
            'model_unchanged':True, 'partial_render_unchanged':True,
            'root_display_count':1, 'public_connection':'APPLIED',
            'new_math_rules':0, 'new_given_registrations':0, 'full_pytest':'NOT_RUN'}


def main():
    if any(raw != new for raw, new in planned_changes().values()):
        raise RuntimeError('R58R1_NOT_APPLIED')
    git = baseline.prior.git
    before = (git('diff','--binary','HEAD'),git('status','--porcelain'))
    report = observe()
    if before != (git('diff','--binary','HEAD'),git('status','--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
    report['repository_unchanged_during_audit'] = True
    path = artifact_folder() / 'report.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for key, value in report.items():
        if key != 'gate':
            print('PHASE176_R3R58R1_'+key.upper()+'='+json.dumps(value, ensure_ascii=False))
    print('REPORT='+str(path))
    print('PHASE176_R3R58R1_GATE='+report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
