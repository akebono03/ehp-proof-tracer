"""Compare the isolated projection with the actual public, trusted narrative."""
from __future__ import annotations

import argparse
from dataclasses import replace
import difflib
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase165_r52_partial_proof import ProofSearchStatus
from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r56r3_public_cited_source_display.apply import planned_changes
from phase176_r3r57_composite_hopf_display_isolated.projection import project_composite_hopf_chain

PACKAGE = Path(__file__).resolve().parent.name


def preflight():
    if any(raw != changed for raw, changed in planned_changes().values()):
        raise RuntimeError('R56R3_NOT_APPLIED')


def capture():
    import phase168_r3_5_model_renderer as renderer
    original = renderer.render_model_backed_narrative_markdown
    captured = []

    def observed(result, model):
        before = baseline.snapshot(model)
        markdown = original(result, model)
        if before != baseline.snapshot(model):
            raise RuntimeError('MODEL_MUTATED')
        captured.append((result, model, markdown))
        return markdown

    with patch.object(renderer, 'render_model_backed_narrative_markdown', observed):
        report, actual, partial = baseline.observe()
    complete = [row for row in captured if row[0].status is ProofSearchStatus.COMPLETE]
    incomplete = [row for row in captured if row[0].status is not ProofSearchStatus.COMPLETE]
    if len(complete) != 1 or len(incomplete) != 1 or complete[0][2] != actual or incomplete[0][2] != partial:
        raise RuntimeError('UNEXPECTED_PUBLIC_CAPTURE')
    return report, complete[0], incomplete[0]


def artifact_folder():
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def observe():
    report, (result, model, actual), (_, partial_model, partial) = capture()
    snapshot = baseline.snapshot(model)
    shadow, plan = project_composite_hopf_chain(actual, model)
    folder = artifact_folder()
    for name, content in [('before.md', actual), ('shadow.md', shadow), ('partial.md', partial)]:
        (folder / name).write_text(content, encoding='utf-8')
    (folder / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (folder / 'narrative.diff').write_text(''.join(difflib.unified_diff(actual.splitlines(True), shadow.splitlines(True), fromfile='before', tofile='shadow')), encoding='utf-8')
    if plan.get('chain_indices') != list(range(14, 26)) or shadow == actual:
        raise RuntimeError('EXPECTED_CERTIFIED_CHAIN_NOT_PROJECTED')
    old = baseline.inspect_markdown(actual, report['steps'])
    new = baseline.inspect_markdown(shadow, report['steps'])
    if actual.split('\n証明\n',1)[0] != shadow.split('\n証明\n',1)[0]:
        raise RuntimeError('REFERENCE_SECTION_CHANGED')
    if (new['references_without_explicit_body_use'] or new['identities'] or new['repeated_equations']
            or new['reversed_equations'] or new['empty_reference_bodies'] != [1,4,5]):
        raise RuntimeError('DISPLAY_INVARIANT_CHANGED')
    if (report['proof_steps'], report['inference_steps'], report['given_steps']) != (62,51,11) or len(model.citations) != 10 or result.open_goals:
        raise RuntimeError('PROOF_INVARIANT_CHANGED')
    if project_composite_hopf_chain(shadow, model) != (shadow,{}) or project_composite_hopf_chain(partial, partial_model) != (partial,{}):
        raise RuntimeError('IDEMPOTENCE_OR_PARTIAL_GUARD_FAILED')
    missing = replace(model, citations=tuple(replace(c, assertion_ids=()) for c in model.citations))
    if project_composite_hopf_chain(actual, missing) != (actual,{}):
        raise RuntimeError('MISSING_SOURCE_GUARD_FAILED')
    if snapshot != baseline.snapshot(model):
        raise RuntimeError('MODEL_CHANGED')
    return {'gate':'PASS_R3R57_ISOLATED_COMPOSITE_HOPF_DISPLAY','status':result.status.value,
            'proof_steps':62,'inference_steps':51,'given_steps':11,'citation_count':10,'open_goals':[],
            'plan':plan,'body_rows_before':len(old['body_rows']),'body_rows_after':len(new['body_rows']),
            'reference_section_unchanged':True,'model_unchanged':True,'partial_render_unchanged':True,
            'production_changes':0,'new_math_rules':0,'new_given_registrations':0,
            'public_connection':'NOT_APPLIED','full_pytest':'NOT_RUN'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    preflight()
    if args.dry_run:
        print('PHASE176_R3R57_GATE=PASS_R3R57_DRYRUN')
        return 0
    git = baseline.prior.git
    before = (git('diff','--binary','HEAD'),git('status','--porcelain'))
    report = observe()
    if before != (git('diff','--binary','HEAD'),git('status','--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED')
    report['repository_unchanged'] = True
    path = artifact_folder() / 'report.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for key,value in report.items():
        if key != 'gate':
            print('PHASE176_R3R57_'+key.upper()+'='+json.dumps(value,ensure_ascii=False))
    print('REPORT='+str(path))
    print('PHASE176_R3R57_GATE='+report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
