"""Audit an isolated display projection against the actual trusted public proof."""
from __future__ import annotations

import argparse
from dataclasses import replace
import difflib
import json
import os
from pathlib import Path
import tempfile

from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r57_composite_hopf_display_isolated.audit import capture
from phase176_r3r57r1_public_composite_hopf_display.apply import planned_changes
from phase176_r3r58_finite_cyclic_lift_display_isolated.projection import project_finite_cyclic_lift

PACKAGE = Path(__file__).resolve().parent.name


def preflight():
    if any(raw != changed for raw, changed in planned_changes().values()):
        raise RuntimeError('R57R1_NOT_APPLIED')


def artifact_folder():
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def observe():
    report, (result, model, actual), (_, partial_model, partial) = capture()
    snapshot = baseline.snapshot(model)
    projected, plan = project_finite_cyclic_lift(actual, model)
    folder = artifact_folder()
    for name, content in [('before.md', actual), ('shadow.md', projected), ('partial.md', partial)]:
        (folder / name).write_text(content, encoding='utf-8')
    (folder / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (folder / 'narrative.diff').write_text(''.join(difflib.unified_diff(actual.splitlines(True), projected.splitlines(True), fromfile='before', tofile='shadow')), encoding='utf-8')
    if (plan.get('lift_index'), plan.get('root_index'), plan.get('premise_indices'), plan.get('subgroup_order')) != (60,61,[7,9,10,13,59],2):
        raise RuntimeError('EXPECTED_CERTIFIED_LIFT_NOT_PROJECTED')
    old = baseline.inspect_markdown(actual, report['steps'])
    new = baseline.inspect_markdown(projected, report['steps'])
    if (actual.split('\n証明\n',1)[0] != projected.split('\n証明\n',1)[0]
            or new['references_without_explicit_body_use'] or new['identities']
            or new['repeated_equations'] or new['reversed_equations']
            or new['empty_reference_bodies'] != [1,4,5]
            or (len(old['body_rows']),len(new['body_rows'])) != (18,21)):
        raise RuntimeError('DISPLAY_INVARIANT_CHANGED')
    if any(projected.count(s) != 1 for s in plan['added_sentences']):
        raise RuntimeError('REASON_MISSING_OR_REPEATED')
    if (report['proof_steps'],report['inference_steps'],report['given_steps']) != (62,51,11) or len(model.citations) != 10 or result.open_goals:
        raise RuntimeError('PROOF_INVARIANT_CHANGED')
    if (project_finite_cyclic_lift(projected, model) != (projected,{})
            or project_finite_cyclic_lift(partial, partial_model) != (partial,{})):
        raise RuntimeError('IDEMPOTENCE_OR_PARTIAL_GUARD_FAILED')
    if project_finite_cyclic_lift(actual, replace(model, citations=())) != (actual,{}):
        raise RuntimeError('MISSING_CITATION_GUARD_FAILED')
    if snapshot != baseline.snapshot(model):
        raise RuntimeError('MODEL_CHANGED')
    return {'gate':'PASS_R3R58_ISOLATED_FINITE_CYCLIC_LIFT_DISPLAY', 'status':result.status.value,
            'web_key':report['web_key'], 'proof_steps':62,'inference_steps':51,'given_steps':11,
            'citation_count':10,'open_goals':[], 'plan':plan,'body_rows_before':18,'body_rows_after':21,
            'reference_section_unchanged':True,'model_unchanged':True,'partial_render_unchanged':True,
            'production_changes':0,'new_math_rules':0,'new_given_registrations':0,
            'public_connection':'NOT_APPLIED','full_pytest':'NOT_RUN'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    preflight()
    if args.dry_run:
        print('PHASE176_R3R58_GATE=PASS_R3R58_DRYRUN')
        return 0
    git = baseline.prior.git
    before = (git('diff','--binary','HEAD'),git('status','--porcelain'))
    report = observe()
    if before != (git('diff','--binary','HEAD'),git('status','--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
    report['repository_unchanged'] = True
    path = artifact_folder() / 'report.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for key,value in report.items():
        if key != 'gate':
            print('PHASE176_R3R58_'+key.upper()+'='+json.dumps(value,ensure_ascii=False))
    print('REPORT='+str(path))
    print('PHASE176_R3R58_GATE='+report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
