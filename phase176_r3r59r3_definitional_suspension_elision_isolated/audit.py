"""Compare an isolated projection with the actual trusted complete Web view."""
from __future__ import annotations

import argparse
from dataclasses import replace
import difflib
import json
import os
from pathlib import Path
import tempfile

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r57_composite_hopf_display_isolated.audit import capture
from phase176_r3r58_finite_cyclic_lift_display_isolated.projection import match_lift
from phase176_r3r59_final_narrative_audit.audit import preflight as prior_preflight
from phase176_r3r59r3_definitional_suspension_elision_isolated.projection import project_definitional_suspension_elision
from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence

PACKAGE = Path(__file__).resolve().parent.name
ROOT = Path(__file__).resolve().parents[1]
PINS = {
    'phase171_r20r13_eta_sentence_layout/projection.py': '71351ba0072f9bb60f74eb8dffb5f21f4724e549',
    'phase172_r2_suspension_relation_display/projection.py': 'bba6280a36ca1c094be1b2a65d94ba0d2582c7a1',
    'phase176_r3r55_equality_display_isolated/projection.py': 'f2bedfc04f96f27a771fbdebaa282fd9c2c9a075',
    'phase169_r10eq_r1_universal_stable_definition/definition.py': '0c74d121419b6755e947a367d7de465d81193174',
    'phase176_r3r59_final_narrative_audit/audit.py': 'b1d997c691721a6ee2cbf3a750056667dfac9c5a',
}


def preflight():
    head = prior_preflight()
    for path, sha in PINS.items():
        if not pinned(normalize((ROOT / path).read_bytes())[0], sha):
            raise RuntimeError('UNREVIEWED_SOURCE:' + path)
    return head


def artifact_folder():
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def observe():
    report, (result, model, actual), (_, partial_model, partial) = capture()
    original = baseline.snapshot(model)
    projected, plan = project_definitional_suspension_elision(actual, model)
    folder = artifact_folder()
    for name, content in [('before.md', actual), ('shadow.md', projected), ('partial.md', partial)]:
        (folder / name).write_text(content, encoding='utf-8')
    (folder / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (folder / 'narrative.diff').write_text(''.join(difflib.unified_diff(actual.splitlines(True), projected.splitlines(True), fromfile='before', tofile='shadow')), encoding='utf-8')
    if (plan.get('chain_indices'), plan.get('joined_index'), plan.get('alias_index'),
            plan.get('witness_indices'), plan.get('source_index'), plan.get('source_reference'),
            plan.get('quadruple_index'), plan.get('consumer_index')) != (list(range(14,26)),52,51,[29,36,43],26,8,56,58):
        raise RuntimeError('EXPECTED_CERTIFIED_ELISION_NOT_PROJECTED')
    old = baseline.inspect_markdown(actual, report['steps'])
    new = baseline.inspect_markdown(projected, report['steps'])
    root = '以上より, ' + _rendered_sentence(model.steps[model.root_index])
    if (actual.split('\n証明\n',1)[0] != projected.split('\n証明\n',1)[0]
            or new['references_without_explicit_body_use'] or new['identities']
            or new['repeated_equations'] or new['reversed_equations']
            or new['empty_reference_bodies'] != [1,4,5]
            or (len(old['body_rows']),len(new['body_rows'])) != (21,19)
            or projected.count(root) != 1
            or (report['proof_steps'],report['inference_steps'],report['given_steps']) != (62,51,11)
            or len(model.citations) != 10 or result.open_goals
            or report['web_key'] != 'generic-complete-proof'):
        raise RuntimeError('DISPLAY_OR_PROOF_INVARIANT_CHANGED')
    # Only the two removals and two citation-prefix replacements are allowed.
    expected = [row['text'] for row in old['body_rows'] if row['text'] not in plan['removed_sentences']]
    expected = [plan['replacements'].get(line,line) for line in expected]
    if expected != [row['text'] for row in new['body_rows']] or len(plan['replacements']) != 2:
        raise RuntimeError('UNEXPECTED_BODY_EDIT')
    if (project_definitional_suspension_elision(projected, model) != (projected,{})
            or project_definitional_suspension_elision(partial, partial_model) != (partial,{})
            or project_definitional_suspension_elision(actual, replace(model, citations=())) != (actual,{})):
        raise RuntimeError('IDEMPOTENCE_OR_NEGATIVE_GUARD_FAILED')
    if match_lift(model) is None or original != baseline.snapshot(model):
        raise RuntimeError('MODEL_OR_LIFT_CHANGED')
    return {'gate':'PASS_R3R59R3_ISOLATED_DEFINITIONAL_SUSPENSION_ELISION',
            'status':result.status.value, 'web_key':report['web_key'], 'proof_steps':62,
            'inference_steps':51, 'given_steps':11, 'citation_count':10, 'open_goals':[],
            'plan':plan, 'body_rows_before':21, 'body_rows_after':19,
            'reference_section_unchanged':True, 'references_without_explicit_body_use':[],
            'model_unchanged':True, 'partial_render_unchanged':True, 'root_display_count':1,
            'production_changes':0, 'new_math_rules':0, 'new_given_registrations':0,
            'public_connection':'NOT_APPLIED', 'full_pytest':'NOT_RUN'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    head = preflight()
    print('PHASE176_R3R59R3_HEAD=' + head)
    if args.dry_run:
        print('PHASE176_R3R59R3_GATE=PASS_R3R59R3_DRYRUN')
        return 0
    git = baseline.prior.git
    before = (git('diff','--binary','HEAD'),git('status','--porcelain'))
    report = observe()
    if before != (git('diff','--binary','HEAD'),git('status','--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
    report.update(head=head, repository_unchanged=True)
    path = artifact_folder() / 'report.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for key,value in report.items():
        if key != 'gate':
            print('PHASE176_R3R59R3_'+key.upper()+'='+json.dumps(value,ensure_ascii=False))
    print('REPORT='+str(path))
    print('PHASE176_R3R59R3_GATE='+report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
