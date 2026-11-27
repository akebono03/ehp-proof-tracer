"""Read-only public frontier audit and isolated finite cyclic quotient tests."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).parent.name
BASE = '2d2ba0baf0fc9fd1a8f7fbb2c1c86a0e3523696b'
TARGET = 'phase165_r52_r9_shared_math.py'
TARGET_BLOB = 'ff667e53c17568d607b81f6362338b33591351db'
ANCHOR = '        sources = sources + (build_cited_512_source(),)\n'
INSERT = '''    # Phase 178 R16R2: append the reviewed, positioned Toda (5.13) images.
    if default_sources:
        from phase178_r16_toda513_isolated.source import build_cited_513_source
        sources = sources + (build_cited_513_source(),)
'''
PINS = {
    'phase165_r12_r2_quotient_rules.py': '2b3e8e0449382e9245ee22f08501e9cede0a5b59',
    'phase165_r12_r26_map_candidates.py': 'b57e4efe80d70cf67906882cbc93c047311e10e9',
    'phase165_r12_r5_structure_bridge.py': '4067bf1b2cc4114359c2d1a104d17ba874122060',
    'phase175_r4r3_two_summand_quotient/rule.py': 'b854491dff8b42817c5e1fe2771e4f2dc2c16713',
    'phase175_r4r12_public_two_summand_quotient/provider.py': '1b34fe0d2707a51af7acc52eaa7d38209e90dfa2',
    'phase176_r3r48_cited_finite_delta_kernel/rule.py': '86cc4a468ffd4601337bbef589a37fa46b449263',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase169_r10e5_composite_generator_image/rule.py': '01acace3eb273d47091421a61291ee54b51c369f',
    'phase165_r12_r11_prop42_unified.py': '79752ec035244677ff6a54debff312e87a76fbf2',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase178_r16_toda513_isolated/source.py': '73300491e27c4d4298e07d8b0bd9c6653328b609',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'phase178_r14_n5_source_first_audit/audit.py': '36aeaee42f124e549c464a71829eee020fb1ed73',
    'phase175_r4r3_two_summand_quotient/tests/test_rule.py': '558651492f5af5ea330973dd2105f5f563d94281',
    'phase175_r4r12_public_two_summand_quotient/tests/test_provider.py': '21ba2c5c785c3d2704f2253bfa132a090e514d7a',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py': 'bd37cb05011ed0d9413bdd7f7335a116d29dae33',
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
}
TESTS = (
    PACKAGE+'/tests/test_audit_contract.py', PACKAGE+'/tests/test_rule.py',
    'phase175_r4r3_two_summand_quotient/tests/test_rule.py',
    'phase175_r4r12_public_two_summand_quotient/tests/test_provider.py',
    'phase178_r16r2_toda513_public/tests/test_public.py',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def normalize(raw):
    return raw.decode('utf-8-sig').replace('\r\n','\n')


def digest(raw):
    return hashlib.sha256(normalize(raw).encode('utf-8')).hexdigest()


def reviewed_production(base):
    require(base.count(ANCHOR)==1 and INSERT not in base,'BASE_ANCHOR_CHANGED')
    return base.replace(ANCHOR,ANCHOR+INSERT,1)


def emit(key,value):
    print('PHASE178_R17_'+key+'='+str(value),flush=True)


def preflight(r1):
    gt = r1.git_text
    head = gt('rev-parse','HEAD')
    require(Path(gt('rev-parse','--show-toplevel')).resolve()==ROOT,'WRONG_ROOT')
    require(gt('branch','--show-current')=='develop' and head==gt('rev-parse','origin/develop'),'BRANCH_OR_HEAD_MISMATCH')
    require(gt('merge-base',BASE,head)==BASE,'REVIEWED_ANCESTRY_REQUIRED')
    require(not gt('diff','--cached','--name-only'),'STAGED_CHANGES_REFUSED')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(),'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    require(gt('rev-parse',BASE+':'+TARGET)==TARGET_BLOB,'BASE_BLOB_CHANGED')
    pins=json.loads((Path(__file__).parent/'reviewed_r16r2_hashes.json').read_text(encoding='utf-8'))
    changed=set(gt('diff','--name-only',BASE,head).splitlines())
    require(changed <= set(pins)|{TARGET},'UNREVIEWED_COMMIT_CHANGE:'+repr(sorted(changed-set(pins)-{TARGET})))
    require(set(gt('diff','--name-only','HEAD').splitlines()) <= {TARGET},'UNRELATED_TRACKED_CHANGE')
    expected=reviewed_production(normalize(r1.git('show',BASE+':'+TARGET)))
    require(normalize((ROOT/TARGET).read_bytes())==expected,'R16R2_PUBLIC_CONNECTION_REQUIRED')
    if TARGET in changed:
        require(normalize(r1.git('show',head+':'+TARGET))==expected,'COMMITTED_PUBLIC_CONNECTION_CHANGED')
    for path,pin in pins.items():
        require((ROOT/path).is_file() and digest((ROOT/path).read_bytes())==pin,'R16R2_PACKAGE_CHANGED:'+path)
        if path in changed:
            require(digest(r1.git('show',head+':'+path))==pin,'COMMITTED_R16R2_PACKAGE_CHANGED:'+path)
    for path,pin in PINS.items():
        require(gt('rev-parse',head+':'+path)==pin and r1.blob_matches(ROOT/path,pin),'PIN_CHANGED:'+path)
    require(all((ROOT/p).is_file() for p in TESTS),'FOCUSED_TEST_MISSING')
    gt('diff','--check')
    return head


def inspect_obligations():
    """Inspect actual data and screened candidates; no proof is injected."""
    from homotopy_groups import FiniteCyclicGroup, TodaSuspensionMap
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result, admitted_db_step
    from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
    from phase178_r16_toda513_isolated.source import canonical_513
    from phase178_r15_toda512_isolated.source import canonical_512
    from phase178_r17_finite_cyclic_quotient_isolated.rule import expand_finite_cyclic_quotient
    from proof import Relation
    root=exact_prior_database_result(5,6)
    middle=exact_prior_database_result(4,6)
    source=exact_prior_database_result(9,3)
    require(all(type(x) is Relation and type(x.rhs) is FiniteCyclicGroup for x in (root,middle,source)),'PRIOR_OR_TARGET_PRESENTATION_MISSING')
    require((root.rhs.order,middle.rhs.order,source.rhs.order)==(2,8,8),'PRESENTATION_ORDER_CHANGED')
    goal=CyclicStructureStatement(root.lhs,root.rhs.generator,root.rhs.order)
    bridge=prefer_universal_prop42_derivation(screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root))
    signed=canonical_513()[0]
    require(len(linked_cited_steps(bridge,signed))==1,'SCREENED_513_MISSING')
    require(len(linked_cited_steps(bridge,canonical_512(4)))==1,'SCREENED_512_MISSING')
    suspension=GeneratorImage(TodaSuspensionMap(middle.lhs,root.lhs),middle.rhs.generator,root.rhs.generator)
    provider=shared_expansion_provider(bridge,proof_target=root)
    original=provider(goal)
    candidate=expand_finite_cyclic_quotient(goal,middle,source,signed,suspension,bridge=bridge)
    result={'root':repr(root),'middle':repr(middle),'source':repr(source),'signed':repr(signed),
            'existing_root_candidate_names':[o.rule.name for o in original],
            'isolated_candidate_count':len(candidate), 'obligations':[]}
    if candidate:
        for statement in candidate[0].subgoals:
            result['obligations'].append({'goal':repr(statement),
                'screened_given_count':len(linked_cited_steps(bridge,statement)),
                'admitted_db_prior':admitted_db_step(statement,proof_target=root,bridge=bridge) is not None,
                'provider_rules':[o.rule.name for o in provider(statement)]})
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dry-run',action='store_true')
    p.add_argument('--timeout',type=int,default=180)
    args=p.parse_args()
    base=Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder=Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report={'gate':'FAIL_R17','dry_run':args.dry_run,'full_pytest':'NOT_RUN','public_changes':0,'new_given':0}
    try:
        from phase178_r1_k6_source_first_audit import audit as r1
        from phase178_r14_n5_source_first_audit.audit import summarize
        require(args.timeout>0,'POSITIVE_TIMEOUT_REQUIRED')
        before=r1.snapshot()
        head=preflight(r1)
        report['head']=head
        emit('HEAD',head)
        emit('R16R2_PUBLIC_CONNECTION','VERIFIED')
        if args.dry_run:
            report['gate']='PASS_R17_READ_ONLY_DRYRUN'
        else:
            summary=r1.worker(5,6,folder,args.timeout)
            report['public_summary']=summary
            require('detail' in summary,'PUBLIC_SEARCH_WORKER_FAILED:'+repr(summary))
            detail=json.loads(Path(summary['detail']).read_text(encoding='utf-8'))
            report['public_analysis']=summarize(summary,detail)
            for key in ('status','proven_step_count','open_goal_count','reference_count','trust_status','target_given_count','web_key'):
                emit('PUBLIC_'+key.upper(),summary[key])
            for item in report['public_analysis']['frontier']:
                emit('FRONTIER',json.dumps(item,ensure_ascii=False))
            result=inspect_obligations()
            report['isolated_candidate_audit']=result
            emit('EXISTING_CYCLIC_CANDIDATES',json.dumps(result['existing_root_candidate_names'],ensure_ascii=False))
            emit('ISOLATED_CANDIDATE_COUNT',result['isolated_candidate_count'])
            for item in result['obligations']:
                emit('OBLIGATION',json.dumps(item,ensure_ascii=False))
            command=[sys.executable,'-B','-m','pytest','-q','-s','-p','no:cacheprovider','--import-mode=importlib',*TESTS]
            report['focused_command']=command
            subprocess.run(command,cwd=ROOT,check=True)
            require(result['isolated_candidate_count']==1,'ACTUAL_TYPED_INPUTS_NEED_REVIEW')
            report['gate']='PASS_R17_FINITE_CYCLIC_QUOTIENT_ISOLATED'
        require(r1.snapshot()==before,'REPOSITORY_CHANGED_DURING_AUDIT')
    except Exception as exc:
        report.update(gate='FAIL_R17',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    emit('REPORT',folder/'report.json')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__=='__main__':
    raise SystemExit(main())
