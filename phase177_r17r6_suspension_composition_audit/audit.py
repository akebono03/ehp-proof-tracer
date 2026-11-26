"""Read-only audit of the verified suspension-composition branch and its display."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import traceback

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob, snapshot
from phase177_r6_general_suspension_public.installer import normalize

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
BASE = 'b30678c9aca3188d0190bbf2b5e36fcdb2b24c16'
RENDERER = 'phase168_r3_5_model_renderer.py'
R5 = 'phase177_r17r5_duplicate_cited_equality'
PINS = {
    'phase168_r3_3_proof_narrative_model.py': '6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52',
    'phase168_r3_27_typed_statement_projection.py': 'fc19a65386b92ce096c3f4c55fc10622b19c3d65',
    'phase169_r10e5_composite_generator_image/rule.py': '01acace3eb273d47091421a61291ee54b51c369f',
    'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py': '48bae67c01b6a22a21ec2b9e90255c07b4e53696',
    'phase175_r4r3_two_summand_quotient/rule.py': 'b854491dff8b42817c5e1fe2771e4f2dc2c16713',
    'phase177_r17r3_rank_two_quotient_display/projection.py': 'b7ffda82255b0d3c6e7d37389515b376c902edc0',
    'phase177_r17r3_rank_two_quotient_display/tests/test_display.py': '9d3c1d32cb44fcc9210d2535ca7fbabd583e7278',
    'phase177_r17r4r2_prop25_equality_chain/projection.py': 'a5f35b71b053c603f540f9750b3af50101dde3ab',
    'phase176_r3r59r3_definitional_suspension_elision_isolated/projection.py': '1fe8211bc55ee4db825c3a20c3737153d2e7280f',
    'phase177_r2_cited_511_reuse_audit/audit.py': '220198dfc5ef1d7e9368f13837ba51d663c1f8d8',
    'phase168_r3_29_order_projection.py': 'b0eaf673fa0d36a31a6831b1297679b48453d8a8',
}
R5_SHA256 = {
    '__init__.py': '72ead7a3863a9c325bf168caddeaf915ef01208efd09d6b246e39fdc8cdba7d2',
    'installer.py': '5edb26c3216edba95fdf64b6308b2e7f385ec2a278ced7c1d34925308b19bc88',
    'projection.py': 'aa07b81869a2a4aa7ecea1e36af9d56da28250dc134eba2e43512d9a8f121e2a',
    'tests/test_display.py': '56b4bcb1bfcb96ca8152ce08ef8eafe02e20acd3c157db823d3694045a2e8195',
    'run.ps1': 'd4fb21d440486700dd696bfb735bd9e208d3bab006c6bf399befbd15d298a25f',
    'README.md': '1ecfe1844f845db0170b9a918fa6485e4df2acf82ad618eb1e040d096a079f03',
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(name, value):
    print('PHASE177_R17R6_'+name+'='+json.dumps(value, ensure_ascii=False), flush=True)


def preflight():
    require(Path(git('rev-parse','--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(git('branch','--show-current') == 'develop', 'WRONG_BRANCH')
    head = git('rev-parse','HEAD')
    require(head == git('rev-parse','origin/develop'), 'LOCAL_REMOTE_HEAD_MISMATCH')
    git('merge-base','--is-ancestor',BASE,head)
    allowed = {RENDERER} | {R5+'/'+name for name in R5_SHA256}
    require(not git('diff','--cached','--name-only'), 'STAGED_CHANGES_REFUSED')
    require(set(git('diff','--name-only',BASE,head).splitlines()) <= allowed,
            'UNREVIEWED_COMMITTED_CHANGES')
    require(set(git('diff','--name-only','HEAD').splitlines()) <= allowed,
            'UNREVIEWED_TRACKED_CHANGES')
    for path,pin in PINS.items():
        require(git('rev-parse','HEAD:'+path) == pin and matches_blob((ROOT/path).read_bytes(),pin),
                'DEPENDENCY_CHANGED:'+path)
    for name,digest in R5_SHA256.items():
        raw = (ROOT/R5/name).read_bytes()
        require(hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest() == digest,
                'R5_PACKAGE_CHANGED:'+name)
    from phase177_r17r5_duplicate_cited_equality.installer import proposed_source
    baseline = subprocess.check_output(['git','show',BASE+':'+RENDERER],cwd=ROOT)
    require(matches_blob(baseline,'c2557db64091344e48dc3c32b3bd2a93addb6a5c'), 'BASE_RENDERER_CHANGED')
    require(normalize((ROOT/RENDERER).read_bytes()) == proposed_source(normalize(baseline)),
            'R5_RENDERER_MISSING_OR_CHANGED')
    print('PHASE177_R17R6_HEAD='+head,flush=True)
    print('PHASE177_R17R6_R5_HOOK=VERIFIED',flush=True)
    return head


def rule_name(step):
    return step.inference_rule.name if step.inference_rule is not None else None


def observe(folder):
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase168_r3_29_order_projection import project_narrative_order
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase175_r4r3_two_summand_quotient.rule import RULE_NAME as QUOTIENT_RULE
    from phase177_r17r3_rank_two_quotient_display.projection import project_rank_two_quotient_reason
    from phase177_r17r4r1_prop25_suspension_elision.projection import replayed
    from phase177_r2_cited_511_reuse_audit.audit import capture
    from proof import ProofRule
    from web_group_proof_common import _group_proof_statement_latex

    invocation,result,calls,model,view = capture()
    require(model is not None and result.status is ProofSearchStatus.COMPLETE
            and model.status is ProofSearchStatus.COMPLETE and not result.open_goals
            and not model.open_goals and view.key == 'generic-complete-proof', 'ROOT_NOT_COMPLETE')
    require(result.target == TodaPrimaryGroup(10,5) and len(result.proven_steps) == len(model.steps) == 43
            and len(model.citations) == 8, 'REVIEWED_ROOT_CHANGED')
    steps = model.steps
    scope = root_ancestor_step_indices(steps,model.root_index)
    lookup = {id(step):i for i,step in enumerate(steps)}
    require(len(lookup) == len(steps), 'DUPLICATE_STEP_IDENTITIES')
    parents = {i:tuple(lookup.get(id(p)) for p in s.premises) for i,s in enumerate(steps)}
    require(all(p is not None for ps in parents.values() for p in ps), 'MISSING_PREMISE_IDENTITY')
    order = tuple(e.step_index for e in project_narrative_order(model))
    position = {i:k for k,i in enumerate(order)}
    quotient, = [i for i in scope if rule_name(steps[i]) == QUOTIENT_RULE]
    q = steps[quotient]
    require(len(q.premises) == 6 and replayed(q), 'QUOTIENT_NOT_REPLAYABLE')
    survivor = parents[quotient][-1]
    branch = root_ancestor_step_indices(steps,survivor)
    q_sentence = project_rank_two_quotient_reason(q.conclusion,q)
    require(q_sentence is not None, 'QUOTIENT_DISPLAY_MISSING')
    markdown = render_model_backed_narrative_markdown(result,model)
    require(markdown.count('\n証明\n') == 1, 'BODY_BOUNDARY_INVALID')
    body = markdown.split('\n証明\n',1)[1]
    body_lines = tuple(s for s in body.splitlines() if s.strip())
    citation_rows = [{'number':c.number,'label':c.reference.label,'locator':c.reference.locator,
                      'step_indices':list(c.step_indices),'assertion_ids':list(c.assertion_ids),
                      'reference_ids':list(c.reference_ids)} for c in model.citations]
    rows = []
    for i in sorted(scope):
        step = steps[i]
        latex,fallback = _group_proof_statement_latex(step.conclusion)
        sentence = typed_sentence(step.conclusion,step)
        direct = [line for line in body_lines if (latex and '$'+latex+'$' in line)
                  or (sentence and sentence in line)]
        consumers = sorted(j for j,ps in parents.items() if i in ps)
        obligations = component_image_obligations(step.conclusion)
        row = {'index':i,'rule':rule_name(step),'trust':step.rule.name,
               'premises':list(parents[i]),'consumers':consumers,
               'external_branch_consumers':[j for j in consumers if j not in branch and j != quotient],
               'citations':list(model.step_citation_numbers[i]),'position':position.get(i),
               'latex':latex,'fallback':fallback,'typed_sentence':sentence,
               'display_matches':direct,'statement':repr(step.conclusion),
               'component_obligations':None if obligations is None else [repr(x) for x in obligations],
               'component_premises_match':obligations is not None and tuple(p.conclusion for p in step.premises)==obligations}
        if i in branch or i == quotient:
            row['replayable'] = replayed(step) if step.rule is ProofRule.INFERENCE else None
            emit('NODE',{k:v for k,v in row.items() if k not in ('statement','component_obligations','fallback')})
        rows.append(row)
    sources = sorted(i for i in branch if steps[i].rule is ProofRule.GIVEN)
    emit('SURVIVOR_INDEX',survivor)
    emit('QUOTIENT_INDEX',quotient)
    emit('BRANCH_INDICES',sorted(branch))
    emit('SOURCE_INDICES',sources)
    emit('BRANCH_CITATIONS',sorted({n for i in branch for n in model.step_citation_numbers[i]}))
    emit('QUOTIENT_SENTENCE',q_sentence)
    emit('ROOT_STEPS',len(steps))
    emit('REFERENCE_COUNT',len(model.citations))
    for line in body_lines:
        emit('BODY_LINE',line)
    (folder/'narrative.md').write_text(markdown,encoding='utf-8')
    return {'root_steps':len(steps),'reference_count':len(model.citations),'root_index':model.root_index,
            'quotient_index':quotient,'survivor_index':survivor,'branch_indices':sorted(branch),
            'source_indices':sources,'citations':citation_rows,'nodes':rows,'body_lines':list(body_lines),
            'quotient_sentence':q_sentence}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    folder.mkdir(parents=True,exist_ok=True)
    report = {'phase':'177_R17R6','dry_run':args.dry_run,'gate':'FAIL_R17R6'}
    try:
        before = snapshot()
        report['head'] = preflight()
        if not args.dry_run:
            report['actual'] = observe(folder)
        require(snapshot() == before, 'REPOSITORY_CHANGED_DURING_AUDIT')
        report['gate'] = ('PASS_R17R6_READ_ONLY_DRYRUN' if args.dry_run
                          else 'PASS_R17R6_SUSPENSION_COMPOSITION_BOUNDARY_CAPTURED')
    except Exception as exc:
        report.update(error=repr(exc),traceback=traceback.format_exc())
        print('PHASE177_R17R6_ERROR='+repr(exc),flush=True)
    path = folder/('dryrun.json' if args.dry_run else 'suspension_composition.json')
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PHASE177_R17R6_REPORT='+str(path),flush=True)
    print('PHASE177_R17R6_NEW_MATH_RULES=0')
    print('PHASE177_R17R6_NEW_GIVEN=0')
    print('PHASE177_R17R6_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R17R6_GATE='+report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
