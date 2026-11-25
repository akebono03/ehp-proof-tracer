"""Verify the actual public hook and distinguish display from model citations."""
from __future__ import annotations

from dataclasses import replace
import difflib
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase165_r52_partial_proof import ProofSearchStatus
from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence
from phase176_r3r53_common_kernel_renderer import audit as kernel
from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r58_finite_cyclic_lift_display_isolated.projection import match_lift
from phase176_r3r60_citation_redundant_premise_audit import audit as prior
from phase176_r3r60r1_citation_premise_elision_isolated import projection
from phase176_r3r60r1_citation_premise_elision_isolated.projection import TAG, parse_display
from phase176_r3r60r2_public_citation_premise_elision.apply import planned_changes

PACKAGE = Path(__file__).resolve().parent.name


def capture_public():
    """Observe actual renderer and public adapter, without R54's old count assertion."""
    import phase168_r3_5_model_renderer as renderer
    import phase165_r52_r3_web_adapter as adapter
    original = renderer.render_model_backed_narrative_markdown
    project = projection.project_citation_premise_elision
    original_adapter = adapter.build_partial_web_group_proof_view
    renders, calls, views = [], [], []

    def observed_render(result, model):
        snap = baseline.snapshot(model)
        markdown = original(result, model)
        if snap != baseline.snapshot(model):
            raise RuntimeError('MODEL_MUTATED_IN_RENDERER')
        renders.append((result, model, markdown))
        return markdown

    def observed_project(markdown, model):
        snap = baseline.snapshot(model)
        output, plan = project(markdown, model)
        if snap != baseline.snapshot(model):
            raise RuntimeError('MODEL_MUTATED_IN_PROJECTION')
        calls.append((markdown, model, output, plan))
        return output, plan

    def observed_adapter(result, **kwargs):
        view = original_adapter(result, **kwargs)
        views.append((result, kwargs.get('narrative_model'), view))
        return view

    with patch.object(renderer, 'render_model_backed_narrative_markdown', observed_render), patch.object(
            projection, 'project_citation_premise_elision', observed_project), patch.object(
            adapter, 'build_partial_web_group_proof_view', observed_adapter):
        report, actual, partial = kernel.observe()
    complete = [row for row in renders if row[0].status is ProofSearchStatus.COMPLETE]
    incomplete = [row for row in renders if row[0].status is not ProofSearchStatus.COMPLETE]
    if len(complete) != 1 or len(incomplete) != 1 or len(calls) != 1 or len(views) != 1:
        raise RuntimeError('UNEXPECTED_PUBLIC_CALL_COUNTS')
    result, model, rendered = complete[0]
    hook_input, owner, output, plan = calls[0]
    view_result, view_model, view = views[0]
    if (rendered != actual or incomplete[0][2] != partial or owner is not model
            or view_result is not result or view_model is not model
            or view.key != 'generic-complete-proof'
            or output.rstrip() + '\n' != actual
            or view.rendered_lines != adapter._build_group_proof_rendered_lines(actual)):
        raise RuntimeError('PUBLIC_HOOK_OR_ADAPTER_MISMATCH')
    report.update(proof_steps=report['root_tree_steps'], inference_steps=report['trust_inference_count'],
                  given_steps=report['trust_given_count'], steps=baseline.collect_steps(result, model))
    return report, complete[0], incomplete[0], hook_input.rstrip() + '\n', plan


def artifact_folder():
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    folder.mkdir(parents=True,exist_ok=True)
    return folder


def observe():
    report,(result,model,actual),(partial_result,partial_model,partial),before,hook_plan = capture_public()
    snap = baseline.snapshot(model)
    old = baseline.inspect_markdown(before,report['steps'])
    findings = prior.inspect_candidates(model,old)
    if findings['blockers']:
        raise RuntimeError('R60_CANDIDATES_CHANGED')
    project = projection.project_citation_premise_elision
    projected,plan = project(before,model)
    if projected != actual or plan != hook_plan or actual == before:
        raise RuntimeError('PUBLIC_DIFFERS_FROM_ISOLATED_PROJECTION')
    folder = artifact_folder()
    for name,content in [('before.md',before),('actual_narrative.md',actual),('partial.md',partial)]:
        (folder/name).write_text(content,encoding='utf-8')
    (folder/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (folder/'narrative.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),actual.splitlines(True),fromfile='before',tofile='public')),encoding='utf-8')
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
    before_lines,_,before_blocks = parse_display(before)
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
    if (project(projected,model) != (projected,{})
            or project(partial,partial_model) != (partial,{})
            or project(before,replace(model,citations=())) != (before,{})):
        raise RuntimeError('NEGATIVE_OR_IDEMPOTENCE_GUARD_FAILED')
    import phase168_r3_5_model_renderer as renderer
    with patch.object(projection, 'project_citation_premise_elision', lambda markdown, model: (markdown, {})):
        if (renderer.render_model_backed_narrative_markdown(result,model) != before
                or renderer.render_model_backed_narrative_markdown(partial_result,partial_model) != partial):
            raise RuntimeError('DISABLED_HOOK_BASELINE_OR_PARTIAL_CHANGED')
    if baseline.snapshot(model) != snap:
        raise RuntimeError('MODEL_CHANGED')
    return {'gate':'PASS_R3R60R2_PUBLIC_CITATION_PREMISE_ELISION_CONNECTED',
            'status':result.status.value,'web_key':report['web_key'],
            'proof_steps':62,'inference_steps':51,'given_steps':11,'citation_count':10,
            'open_goals':[],'plan':plan,'body_rows_before':19,'body_rows_after':18,
            'display_reference_count_before':10,'display_reference_count_after':9,
            'retained_reference_blocks_unchanged_except_display_numbers':True,
            'references_without_explicit_body_use':[], 'root_display_count':1,
            'model_unchanged':True,'partial_render_unchanged':True,
            'production_changes':1,'public_adapter_verified':True,'new_math_rules':0,'new_given_registrations':0,
            'public_connection':'APPLIED','full_pytest':'NOT_RUN'}


def main():
    if any(raw != new for raw,new in planned_changes().values()):
        raise RuntimeError('R60R2_NOT_APPLIED')
    git = kernel.git
    before = (git('diff','--binary','HEAD'),git('status','--porcelain'))
    report = observe()
    if before != (git('diff','--binary','HEAD'),git('status','--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
    report.update(head=git('rev-parse','HEAD').decode('ascii').strip(),repository_unchanged_during_audit=True)
    path = artifact_folder()/'report.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for key,value in report.items():
        if key != 'gate':
            print('PHASE176_R3R60R2_'+key.upper()+'='+json.dumps(value,ensure_ascii=False))
    print('REPORT='+str(path))
    print('PHASE176_R3R60R2_GATE='+report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
