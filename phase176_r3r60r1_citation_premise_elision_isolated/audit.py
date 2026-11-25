"""Verify the isolated projection on the actual public, trusted proof model."""
from __future__ import annotations

import argparse
from dataclasses import replace
import difflib
import json
import os
from pathlib import Path
import tempfile

from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence
from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r57_composite_hopf_display_isolated.audit import capture
from phase176_r3r58_finite_cyclic_lift_display_isolated.projection import match_lift
from phase176_r3r60_citation_redundant_premise_audit import audit as prior
from phase176_r3r60r1_citation_premise_elision_isolated.projection import (
    TAG, parse_display, project_citation_premise_elision,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
PINS = {
    'phase176_r3r60_citation_redundant_premise_audit/audit.py':'4a7bf735f1e556c798aea8a5137304536ccca4c5',
    'phase171_r20r13_eta_sentence_layout/projection.py':'2b82ba6dfe4c34d71d84743dbe46de311d89ec8a',
    'phase176_r3r56_cited_source_display_isolated/projection.py':'b61d4c7065db97b54efac529e2d9f709b840e01e',
    'phase169_r10d2_general_family_definition/family_citation.py':'b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8',
}


def preflight():
    head = prior.preflight()
    for path,sha in PINS.items():
        if not pinned(normalize((ROOT/path).read_bytes())[0],sha):
            raise RuntimeError('UNREVIEWED_SOURCE:'+path)
    return head


def artifact_folder():
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    folder.mkdir(parents=True,exist_ok=True)
    return folder


def observe():
    report,(result,model,actual),(partial_result,partial_model,partial) = capture()
    snap = baseline.snapshot(model)
    old = baseline.inspect_markdown(actual,report['steps'])
    findings = prior.inspect_candidates(model,old)
    if findings['blockers']:
        raise RuntimeError('R60_CANDIDATES_CHANGED')
    projected,plan = project_citation_premise_elision(actual,model)
    folder = artifact_folder()
    for name,content in [('before.md',actual),('shadow.md',projected),('partial.md',partial)]:
        (folder/name).write_text(content,encoding='utf-8')
    (folder/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (folder/'narrative.diff').write_text(''.join(difflib.unified_diff(actual.splitlines(True),projected.splitlines(True),fromfile='before',tofile='shadow')),encoding='utf-8')
    expected_map = {**{i:i for i in range(1,9)},10:9}
    if (plan.get('zero_source_index'),plan.get('zero_base_index'),plan.get('zero_consumer_index'),
            plan.get('quadruple_index'),plan.get('formula_source_index'),plan.get('member_index'),
            plan.get('family_source_index'),plan.get('removed_reference'),plan.get('display_number_map')) != (1,2,3,56,55,54,53,9,expected_map):
        raise RuntimeError('EXPECTED_CERTIFIED_ELISION_NOT_PROJECTED')
    if (plan['removed_sentences'] != findings['proposed_body_removals']
            or plan['replacements'] != findings['proposed_body_replacements']):
        raise RuntimeError('R60_BODY_CANDIDATES_CHANGED')
    new = baseline.inspect_markdown(projected,report['steps'])
    def remap(s):
        return TAG.sub(lambda m:f'[R{expected_map[int(m[1])]}]',s)
    expected = [remap(plan['replacements'].get(row['text'],row['text']))
                for row in old['body_rows'] if row['text'] not in plan['removed_sentences']]
    if expected != [row['text'] for row in new['body_rows']]:
        raise RuntimeError('UNEXPECTED_BODY_CHANGE')
    before_lines,_,before_blocks = parse_display(actual)
    after_lines,_,after_blocks = parse_display(projected)
    for original,display in expected_map.items():
        a,b = before_blocks[original]
        c,d = after_blocks[display]
        if [remap(s) for s in before_lines[a:b]] != after_lines[c:d]:
            raise RuntimeError('RETAINED_REFERENCE_BLOCK_CHANGED')
    root = '以上より, '+_rendered_sentence(model.steps[model.root_index])
    if ((len(old['body_rows']),len(new['body_rows'])) != (19,18)
            or list(old['references']) != list(range(1,11))
            or list(new['references']) != list(range(1,10))
            or new['references_without_explicit_body_use'] or new['identities']
            or new['repeated_equations'] or new['reversed_equations']
            or new['empty_reference_bodies'] != [1,4,5] or projected.count(root) != 1
            or (report['proof_steps'],report['inference_steps'],report['given_steps']) != (62,51,11)
            or len(model.citations) != 10 or result.open_goals or result.status.value != 'complete'
            or report['web_key'] != 'generic-complete-proof' or match_lift(model) is None):
        raise RuntimeError('DISPLAY_OR_PROOF_INVARIANT_CHANGED')
    if (project_citation_premise_elision(projected,model) != (projected,{})
            or project_citation_premise_elision(partial,partial_model) != (partial,{})
            or project_citation_premise_elision(actual,replace(model,citations=())) != (actual,{})):
        raise RuntimeError('NEGATIVE_OR_IDEMPOTENCE_GUARD_FAILED')
    import phase168_r3_5_model_renderer as renderer
    if (renderer.render_model_backed_narrative_markdown(result,model) != actual
            or renderer.render_model_backed_narrative_markdown(partial_result,partial_model) != partial
            or baseline.snapshot(model) != snap):
        raise RuntimeError('MODEL_OR_PUBLIC_RENDER_CHANGED')
    return {'gate':'PASS_R3R60R1_ISOLATED_CITATION_PREMISE_ELISION',
            'status':result.status.value,'web_key':report['web_key'],
            'proof_steps':62,'inference_steps':51,'given_steps':11,'citation_count':10,
            'open_goals':[],'plan':plan,'body_rows_before':19,'body_rows_after':18,
            'display_reference_count_before':10,'display_reference_count_after':9,
            'retained_reference_blocks_unchanged_except_display_numbers':True,
            'references_without_explicit_body_use':[], 'root_display_count':1,
            'model_unchanged':True,'partial_render_unchanged':True,
            'production_changes':0,'new_math_rules':0,'new_given_registrations':0,
            'public_connection':'NOT_APPLIED','full_pytest':'NOT_RUN'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    head = preflight()
    print('PHASE176_R3R60R1_HEAD='+head)
    if args.dry_run:
        print('PHASE176_R3R60R1_GATE=PASS_R3R60R1_DRYRUN')
        return 0
    git = baseline.prior.git
    before = (git('diff','--binary','HEAD'),git('status','--porcelain'))
    report = observe()
    if before != (git('diff','--binary','HEAD'),git('status','--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
    report.update(head=head,repository_unchanged=True)
    path = artifact_folder()/'report.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for key,value in report.items():
        if key != 'gate':
            print('PHASE176_R3R60R1_'+key.upper()+'='+json.dumps(value,ensure_ascii=False))
    print('REPORT='+str(path))
    print('PHASE176_R3R60R1_GATE='+report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
