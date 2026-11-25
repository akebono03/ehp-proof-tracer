"""Observe the actual trusted Web render and compare on the identical model."""
from __future__ import annotations

from dataclasses import replace
import difflib
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r57_composite_hopf_display_isolated import audit as isolated, projection
from phase176_r3r57r1_public_composite_hopf_display.apply import planned_changes

PACKAGE = Path(__file__).resolve().parent.name


def artifact_folder():
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def observe():
    project = projection.project_composite_hopf_chain
    calls = []

    def observed(markdown, model):
        before = baseline.snapshot(model)
        output, plan = project(markdown, model)
        if before != baseline.snapshot(model):
            raise RuntimeError('MODEL_CHANGED_IN_PUBLIC_HOOK')
        calls.append((markdown, model, output, plan))
        return output, plan

    with patch.object(projection, 'project_composite_hopf_chain', observed):
        report, (result, model, actual), (partial_result, partial_model, partial) = isolated.capture()
    if len(calls) != 1 or calls[0][1] is not model:
        raise RuntimeError('PUBLIC_HOOK_NOT_OBSERVED')
    before, _, output, plan = calls[0]
    before = before.rstrip() + '\n'
    if output.rstrip() + '\n' != actual:
        raise RuntimeError('WEB_DIFFERS_FROM_HOOK')
    folder = artifact_folder()
    for name, text in [('before.md', before), ('actual_narrative.md', actual), ('partial.md', partial)]:
        (folder / name).write_text(text, encoding='utf-8')
    (folder / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (folder / 'narrative.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True), actual.splitlines(True), fromfile='before', tofile='public')), encoding='utf-8')
    snapshot = baseline.snapshot(model)
    if (plan.get('chain_indices') != list(range(14, 26)) or plan.get('replaced_visible_lines') != 9
            or before == actual or project(before, model) != (actual, plan)
            or project(actual, model) != (actual, {})):
        raise RuntimeError('PUBLIC_DIFFERS_FROM_VERIFIED_ISOLATED_PROJECTION')
    import phase168_r3_5_model_renderer as renderer
    with patch.object(projection, 'project_composite_hopf_chain', lambda markdown, model: (markdown, {})):
        if renderer.render_model_backed_narrative_markdown(result, model) != before:
            raise RuntimeError('DISABLED_HOOK_BASELINE_MISMATCH')
        if renderer.render_model_backed_narrative_markdown(partial_result, partial_model) != partial:
            raise RuntimeError('PARTIAL_RENDER_CHANGED')
    if project(partial, partial_model) != (partial, {}):
        raise RuntimeError('PARTIAL_PROJECTION_CHANGED')
    missing = replace(model, citations=tuple(replace(c, assertion_ids=()) for c in model.citations))
    if project(before, missing) != (before, {}):
        raise RuntimeError('MISSING_SOURCE_GUARD_FAILED')
    old = baseline.inspect_markdown(before, report['steps'])
    new = baseline.inspect_markdown(actual, report['steps'])
    if before.split('\n証明\n', 1)[0] != actual.split('\n証明\n', 1)[0]:
        raise RuntimeError('REFERENCE_SECTION_CHANGED')
    if (new['references_without_explicit_body_use'] or new['identities'] or new['repeated_equations']
            or new['reversed_equations'] or new['empty_reference_bodies'] != [1,4,5]
            or (len(old['body_rows']), len(new['body_rows'])) != (26,18)
            or actual.count(plan['summary']) != 1 or actual.count(plan['retained_witness']) != 1
            or (report['proof_steps'], report['inference_steps'], report['given_steps']) != (62,51,11)
            or len(model.citations) != 10 or result.open_goals or baseline.snapshot(model) != snapshot):
        raise RuntimeError('PUBLIC_INVARIANT_CHANGED')
    return {'gate':'PASS_R3R57R1_PUBLIC_COMPOSITE_HOPF_DISPLAY_CONNECTED',
            'status':result.status.value, 'web_key':report['web_key'], 'proof_steps':62,
            'inference_steps':51, 'given_steps':11, 'citation_count':10, 'open_goals':[],
            'plan':plan, 'body_rows_before':26, 'body_rows_after':18,
            'reference_section_unchanged':True, 'references_without_explicit_body_use':[],
            'model_unchanged':True, 'partial_render_unchanged':True,
            'public_connection':'APPLIED', 'new_math_rules':0, 'new_given_registrations':0,
            'full_pytest':'NOT_RUN'}


def main():
    if any(raw != changed for raw, changed in planned_changes().values()):
        raise RuntimeError('R57R1_NOT_APPLIED')
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
            print('PHASE176_R3R57R1_'+key.upper()+'='+json.dumps(value,ensure_ascii=False))
    print('REPORT='+str(path))
    print('PHASE176_R3R57R1_GATE='+report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
