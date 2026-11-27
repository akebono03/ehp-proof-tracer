"""Read-only Source-first audit for the single Phase 178 n=5, k=6 target."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).parent.name
BASE = '694c674d73f8a360bf65c6bba3e4aafd9749ba99'
PREFIX = 'PHASE178_R14_'
PINS = {
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'phase165_r52_r9_shared_math.py': '4556e76736a3d5624632900ee9c4ab45599ffb0f',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
    'phase178_r12r2_zero_composition_elision/projection.py': '07fb67b22cfc1d3dd80f5de9390e10dbba353b53',
    'phase175_r4r10_cited_58_prop25_public/tests/test_provider.py': '7777efc5024f429b4881314c909036ec637ac1e8',
    'phase175_r4r12r13r3_public_delta_e_bridge/tests/test_provider.py': 'f568b9591f3af50c524693f998183fd157ffcdb3',
    'phase177_r15_finite_cyclic_delta_injective_public/tests/test_public.py': '8f6d2419933f3748a40749cbbdc3c65f4228fa24',
    'phase178_r9_finite_group_surjective_injective_public/tests/test_provider.py': '46b5daa6f7b9ddb96cda1991104c53848a5777e8',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py': 'bd37cb05011ed0d9413bdd7f7335a116d29dae33',
}
TESTS = (
    PACKAGE+'/tests/test_audit.py',
    'phase175_r4r10_cited_58_prop25_public/tests/test_provider.py',
    'phase175_r4r12r13r3_public_delta_e_bridge/tests/test_provider.py',
    'phase177_r15_finite_cyclic_delta_injective_public/tests/test_public.py',
    'phase178_r9_finite_group_surjective_injective_public/tests/test_provider.py',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
)
ANCHORS = (r'\begin{equation}\label{eq:5.12}', r'\begin{proposition}\label{prop:5.11}', r'\begin{equation}\label{eq:5.13}')


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def emit(key, value):
    print(PREFIX+key+'='+str(value), flush=True)


def source_evidence(source):
    """Check unique adopted-source anchors, order, and the literal clauses."""
    require(all(source.count(a)==1 for a in ANCHORS), 'SOURCE_ANCHOR_MISSING_OR_AMBIGUOUS')
    positions = [source.index(a) for a in ANCHORS]
    require(positions == sorted(positions), 'SOURCE_ORDER_CHANGED')
    eq12 = source.split(ANCHORS[0],1)[1].split(r'\end{equation}',1)[0]
    prop = source.split(ANCHORS[1],1)[1].split(r'\end{proposition}',1)[0]
    eq13 = source.split(ANCHORS[2],1)[1].split(r'\end{equation}',1)[0]
    require(all(x in eq12 for x in (r'\pi^{2n+1}_{n+7}',r'\pi^{n}_{n+5}','n=4,5,6','単射')), 'EQ512_CHANGED')
    require(all(x in prop for x in (r'\pi^{3}_{9}=0',r'\pi^{4}_{10}=\mathbb Z_8',r'\pi^{n}_{n+6}=\mathbb Z_2')), 'PROP511_CHANGED')
    require(r'\Delta(\nu_9)=\pm\,2(\nu_4^{2})' in eq13,'EQ513_FIRST_CHANGED')
    return {'anchor_lines':{a:source[:p].count('\n')+1 for a,p in zip(ANCHORS,positions)},
            'eq512':eq12.strip(),'proposition511':prop.strip(),'eq513':eq13.strip()}


def summarize(summary, detail):
    """Classify observed root/frontier, without treating a candidate as proof."""
    require((summary.get('n'),summary.get('k'))==(5,6),'WRONG_TARGET')
    status = summary['status']
    require(status in ('complete','partial','search_failed','not_searched'),'UNMEASURED_TARGET')
    require(summary['web_error'] is None and summary['web_key'] is not None,'WEB_GAP')
    require(summary['target_given_count']==0,'TARGET_GIVEN_FOUND')
    require(summary['complete_invariants_hold'],'TRUST_CONTRACT_FAILED')
    require(len(detail['open_goals'])==summary['open_goal_count'],'OPEN_GOAL_COUNT_CHANGED')
    if status=='complete':
        require(summary['trust_status']=='VERIFIED' and summary['open_goal_count']==0 and summary['web_key']=='generic-complete-proof','COMPLETE_NOT_VERIFIED')
    frontier = []
    for item in detail['frontier']:
        frontier.append({'goal':item['goal'],'state':item['state'],
                         'rules':list(dict.fromkeys(o['rule'] for batch in item['observed_expansions'] for o in batch['options']))})
    return {'root_complete':status=='complete','frontier':frontier,
            'provider_call_count':len(detail['provider_calls']),
            'screened_source_inventory':detail['screened_source_inventory'],
            'search_context':detail['search_context']}


def preflight(r1):
    require(Path(os.fsdecode(r1.git('rev-parse','--show-toplevel').strip())).resolve()==ROOT,'WRONG_ROOT')
    require(r1.git_text('branch','--show-current')=='develop','DEVELOP_REQUIRED')
    head = r1.git_text('rev-parse','HEAD')
    require(head==r1.git_text('rev-parse','origin/develop'),'HEAD_ORIGIN_MISMATCH')
    require(r1.git_text('merge-base',BASE,head)==BASE,'REVIEWED_BASE_REQUIRED')
    changed = r1.git_text('diff','--name-only',BASE,head).splitlines()
    require(all(p.startswith('phase178_r13_final_verified_proof_audit/') for p in changed),'UNREVIEWED_COMMIT_CHANGE:'+repr(changed))
    require(not r1.git('status','--porcelain','--untracked-files=no'),'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(),'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path,pin in PINS.items():
        require(r1.git_text('rev-parse','HEAD:'+path)==pin and r1.blob_matches(ROOT/path,pin),'PIN_CHANGED:'+path)
    for path in TESTS:
        require((ROOT/path).is_file(),'FOCUSED_TEST_MISSING:'+path)
    r1.git('diff','--check')
    return head,source_evidence((ROOT/'sources/toda/Toda_05_2.tex').read_text(encoding='utf-8-sig'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--timeout',type=int,default=180)
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report = {'gate':'FAIL_R14','dry_run':args.dry_run,'new_rules':0,'new_given':0,'full_pytest':'NOT_RUN'}
    try:
        from phase178_r1_k6_source_first_audit import audit as r1
        require(args.timeout>0,'POSITIVE_TIMEOUT_REQUIRED')
        before = r1.snapshot()
        head,evidence = preflight(r1)
        report.update(head=head,source_evidence=evidence)
        emit('HEAD',head)
        emit('SOURCE_ORDER','VERIFIED_ADOPTED_TRANSCRIPTION')
        if args.dry_run:
            report['gate']='PASS_R14_READ_ONLY_DRYRUN'
        else:
            summary = r1.worker(5,6,folder,args.timeout)
            report['summary']=summary
            require('detail' in summary,'SEARCH_WORKER_FAILED:'+repr(summary))
            detail = json.loads(Path(summary['detail']).read_text(encoding='utf-8'))
            analysis = summarize(summary,detail)
            report['analysis']=analysis
            for key in ('status','proven_step_count','open_goal_count','reference_count','trust_status','target_given_count','web_key'):
                emit(key.upper(),summary[key])
            for item in analysis['frontier']:
                emit('FRONTIER',json.dumps(item,ensure_ascii=False))
            emit('PROVIDER_CALL_COUNT',analysis['provider_call_count'])
            command=[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib',*TESTS]
            report['focused_command']=command
            subprocess.run(command,cwd=ROOT,check=True)
            report['gate']='PASS_R14_N5_SOURCE_FIRST_AUDIT'
        require(r1.snapshot()==before,'REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged']=True
    except Exception as exc:
        report.update(gate='FAIL_R14',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    emit('REPORT',folder/'report.json')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__=='__main__':
    raise SystemExit(main())
