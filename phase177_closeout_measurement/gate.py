"""Phase 177 read-only closeout measurement; never publish final documents."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '70d3ba540adebe96ada08728d045c1153e7e919a'
R18_HEAD = 'c4e6728aa1ae2b0e7e231bdd0f378df5a0a04faf'
TEST_BASE = '7b4e071b735d8c309c2155c04c96869e7e774bdb'
PINS = {
    'README.md': 'fa641728ebfe696a2999da865847997e3a1122b0',
    'docs/design.md': '54586fae5c8d03b8963f557e053b5df7540cc772',
    'docs/development_log.md': '8bc7dc8bdd31da4ea4349a090a8fdc8acbca4bf2',
    'docs/roadmap.md': 'adb524f837c5b20b3e54ffcdfa22cda25da4cd6a',
    'docs/proof_records.md': 'fdb2b72410027742da4a0416f7723f096339f0bc',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'tests/conftest.py': '304c7b40eb1041475fb6bc4519d3ef61fd3275e2',
    'phase176_closeout/gate.py': 'b6f055a144e0c1b053d01b2ed9ccd4ef7ea90f35',
    'phase176_r1_k5_source_first_audit/audit.py': 'b4d7b8a17119e7d60ea302b86b86c3ba2cdbc5c3',
    'phase177_r18_final_verified_proof_audit/audit.py': '704d5af7a98111e0365ad15fd1e2190891e23df5',
}
STATUSES = ('complete', 'partial', 'search_failed', 'not_searched')
MARKER = 'PHASE177_CLOSEOUT_WORKER_JSON='


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE177_CLOSEOUT_'+key+'='+str(value), flush=True)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def git_text(*args):
    return git(*args).decode('utf-8').strip()


def paths(raw):
    return {os.fsdecode(p) for p in raw.split(b'\0') if p}


def registered_pairs(csv_path):
    with csv_path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        require({'n','k'}.issubset(reader.fieldnames or ()), 'CSV_COLUMNS_MISSING')
        result = set()
        for row in reader:
            n, k = (row.get('n') or '').strip(), (row.get('k') or '').strip()
            if not n:
                continue
            n, k = int(n), int(k)
            if n >= 2 and k >= 0:
                result.add((n,k))
    return tuple(sorted(result, key=lambda p: (p[1] != 5, p[1], p[0])))


def preflight():
    from phase177_r18_final_verified_proof_audit import audit as r18
    from phase177_r2_cited_511_reuse_audit.audit import matches_blob
    from phase176_closeout.gate import ACTIVE_COMMAND, HISTORICAL
    from phase175_r4r14r11_closeout_preflight.audit import KNOWN_LEGACY_FAILURES
    require(Path(os.fsdecode(git('rev-parse','--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(git_text('branch','--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(git_text('rev-parse','HEAD') == git_text('rev-parse','origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:'+HEAD)
    require(not git('status','--porcelain','--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    git('diff','--check')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    git('merge-base','--is-ancestor',R18_HEAD,HEAD)
    changed = paths(git('diff','--name-only','-z',R18_HEAD,HEAD))
    prefix = 'phase177_r18_final_verified_proof_audit/'
    require(changed == {prefix+p for p in ('README.md','__init__.py','audit.py','run.ps1')}, 'R18_DIFF_CHANGED')
    pins = dict(PINS)
    pins.update(r18.PINS)
    for name, pin in pins.items():
        require(git_text('rev-parse','HEAD:'+name) == pin and matches_blob((ROOT/name).read_bytes(),pin), 'SOURCE_PIN_CHANGED:'+name)
    positions = r18.source_positions(ROOT)
    positions['toda:(5.11)'] = r18.verify_cited_511(ROOT)
    require(positions['toda:Proposition 2.5'] < positions['toda:(5.11)'], 'SOURCE_ORDER_INVALID')
    require(tuple(KNOWN_LEGACY_FAILURES) == HISTORICAL and len(HISTORICAL) == 4, 'HISTORICAL_SCOPE_CHANGED')
    require(all((ROOT/p.split('::')[0]).is_file() for p in HISTORICAL), 'HISTORICAL_FILES_MISSING')
    require(not git('diff','--name-only','-z',TEST_BASE,HEAD,'--','tests'), 'ACTIVE_TEST_TREE_CHANGED')
    tracked = paths(git('ls-tree','-r','--name-only','-z','HEAD','--','tests'))
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT/'tests').rglob('*.py') if p.is_file()}
    require(actual == {p for p in tracked if p.endswith('.py')}, 'ACTIVE_PYTHON_INVENTORY_CHANGED')
    pairs = registered_pairs(ROOT/'data/sphere.csv')
    require(len(pairs) == 831 and {p for p in pairs if p[1]==5} == {(n,5) for n in range(2,8)}, 'REGISTERED_DOMAIN_CHANGED')
    return {'head':HEAD,'r18_head':R18_HEAD,'test_baseline':TEST_BASE,'pins':pins,
            'source_positions':positions,'active_test_python_files':len(actual),
            'active_command':list(ACTIVE_COMMAND),'historical_tests':list(HISTORICAL),
            'historical_status':'FOUR_KNOWN_FAILURES_NOT_RERUN_NOT_PASSING',
            'pairs':list(pairs),'documents':{p:sha256((ROOT/p).read_bytes()).hexdigest() for p in PINS if p.endswith('.md')}}


def store(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str)+'\n',encoding='utf-8')


def observe(n, k):
    if k == 5:
        from phase176_r1_k5_source_first_audit.audit import observe as previous_observe
        row = previous_observe(n,k)
        require(row['web']['status'] == 'rendered', 'K5_WEB_FAILED:'+str(row['web']))
        return row
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    result = search_group_from_registered_goal(n=n,k=k)
    conclusion = result.conclusion
    roots = [s for s in result.proven_steps if conclusion is not None and s.conclusion == conclusion]
    target = conclusion.group if isinstance(conclusion,TodaPrimaryGroupZeroStatement) else getattr(conclusion,'lhs',None)
    if result.status is ProofSearchStatus.COMPLETE:
        require(not result.open_goals and conclusion is not None and target == TodaPrimaryGroup(n+k,n) and len(roots)==1, 'COMPLETE_PROOF_CONTRACT_VIOLATION')
    return {'n':n,'k':k,'status':result.status.value,'structure_status':result.structure_status.value,
            'open_goal_count':len(result.open_goals),'open_goals':[str(x) for x in result.open_goals],
            'reference_count':len(result.references),'proven_step_count':len(result.proven_steps),
            'root_step_count':len(roots),'conclusion':str(conclusion) if conclusion is not None else None,
            'diagnostics':list(result.diagnostics)}


def worker(n,k,timeout):
    env = dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
    try:
        p = subprocess.run([sys.executable,'-B','-m',PACKAGE+'.gate','--worker',str(n),str(k)],cwd=ROOT,
                           env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'n':n,'k':k,'status':'worker_timeout'}
    lines = [s[len(MARKER):] for s in p.stdout.splitlines() if s.startswith(MARKER)]
    if p.returncode or len(lines)!=1:
        return {'n':n,'k':k,'status':'worker_error','exit_code':p.returncode,'stderr':p.stderr[-8000:],'stdout':p.stdout[-2000:]}
    try:
        row = json.loads(lines[0])
        require((row['n'],row['k'])==(n,k) and row['status'] in STATUSES,'WORKER_CONTRACT_CHANGED')
        return row
    except Exception as exc:
        return {'n':n,'k':k,'status':'worker_error','error':repr(exc)}


def summarize(rows):
    counts = {s:sum(r['status']==s for r in rows) for s in STATUSES}
    counts['registered'] = len(rows)
    counts['incomplete'] = sum(counts[s] for s in STATUSES[1:])
    counts['unmeasured'] = len(rows)-sum(counts[s] for s in STATUSES)
    return counts


def run(dry_run, timeout):
    from phase176_closeout.gate import ACTIVE_COMMAND, parse_summary, checkout_state
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    attempt = folder/'attempt.json'
    report_path = folder/'report.json'
    report = {'gate':'FAIL_PHASE177_CLOSEOUT_MEASUREMENT','phase177_formally_closed':False,'full_pytest':'NOT_RUN'}
    started = False
    try:
        require(not attempt.exists() and not report_path.exists(),'EXISTING_ATTEMPT_REQUIRES_REVIEW')
        context = preflight()
        emit('HEAD',HEAD)
        emit('REGISTERED',len(context['pairs']))
        emit('K5_REGISTERED',6)
        if dry_run:
            emit('FULL_PYTEST','NOT_RUN')
            emit('GATE','PASS_READ_ONLY_DRYRUN')
            return 0
        before = checkout_state()
        folder.mkdir(parents=True,exist_ok=True)
        with attempt.open('x',encoding='utf-8') as out:
            started = True
            json.dump({'head':HEAD,'started_utc':datetime.now(timezone.utc).isoformat(),'command':[sys.executable,*ACTIVE_COMMAND]},out,indent=2)
        report['preflight'] = context
        from phase177_r18_final_verified_proof_audit.audit import observe as public_observe
        report['public_audit'] = public_observe(folder)
        a = report['public_audit']
        expected = {'status':'complete','web_key':'generic-complete-proof','open_goals':0,'root_ancestor_nodes':43,
                    'root_inferences':35,'root_given_leaves':8,'reference_count':8,'target_group_given':0,
                    'search_lookup_mode':'typed_reference','narrative_verified':True}
        require(all(a.get(k)==v for k,v in expected.items()) and len(a['db_prior_leaves'])==4,'R18_PUBLIC_INVARIANT_CHANGED')
        require(checkout_state()==before,'REPOSITORY_CHANGED_DURING_PUBLIC_AUDIT')
        store(report_path,report)
        stdout, stderr = folder/'full_pytest_stdout.txt',folder/'full_pytest_stderr.txt'
        emit('FULL_PYTEST','STARTED_ONE_PHASE_END_RUN')
        report['full_pytest']='STARTED'
        store(report_path,report)
        with stdout.open('xb') as out, stderr.open('xb') as err:
            proc = subprocess.run([sys.executable,*ACTIVE_COMMAND],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'),stdout=out,stderr=err)
        report.update(full_pytest_exit=proc.returncode,stdout_sha256=sha256(stdout.read_bytes()).hexdigest(),stderr_sha256=sha256(stderr.read_bytes()).hexdigest())
        print('\n'.join(stdout.read_text(encoding='utf-8',errors='replace').splitlines()[-12:]),flush=True)
        count, summary = parse_summary(stdout.read_text(encoding='utf-8',errors='replace'),proc.returncode)
        report.update(full_pytest='PASS',passed=count,summary=summary)
        store(report_path,report)
        require(checkout_state()==before,'REPOSITORY_CHANGED_DURING_FULL_PYTEST')
        rows = []
        report['groups'] = rows
        with (folder/'groups.jsonl').open('x',encoding='utf-8') as log:
            for index,(n,k) in enumerate(context['pairs'],1):
                row = worker(n,k,timeout)
                rows.append(row)
                log.write(json.dumps(row,ensure_ascii=False,default=str)+'\n')
                log.flush()
                emit('GROUP',f'{index}/{len(context["pairs"])} n={n} k={k} status={row["status"]} open={row.get("open_goal_count","UNKNOWN")}')
        k5 = [r for r in rows if r['k']==5]
        report['registered_summary'] = summarize(rows)
        report['k5_summary'] = summarize(k5)
        report['k5_groups'] = k5
        report['k5_remaining'] = [r for r in k5 if r['status'] in STATUSES[1:]]
        require(all(r['status']=='complete' for r in rows if r['k']==4),'PHASE175_REGRESSION')
        require(all(r['status']=='complete' for r in k5 if r['n'] in (3,5)),'PHASE176_OR_177_REGRESSION')
        require(report['registered_summary']['unmeasured']==0,'UNMEASURED_GROUPS_REQUIRE_REVIEW')
        require(checkout_state()==before,'REPOSITORY_CHANGED_DURING_GROUP_AUDIT')
        git('diff','--check')
        report['repository_unchanged']=True
        report['gate']='PASS_PHASE177_CLOSEOUT_MEASURED_DOCUMENTS_PENDING'
    except BaseException as exc:
        report.update(error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    if started:
        report['completed_utc']=datetime.now(timezone.utc).isoformat()
        store(report_path,report)
        emit('REPORT',report_path)
    for key in ('full_pytest','passed','summary','registered_summary','k5_summary','phase177_formally_closed','gate'):
        if key in report:
            emit(key.upper(),report[key])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--timeout',type=int,default=90)
    parser.add_argument('--worker',nargs=2,type=int)
    args = parser.parse_args()
    if args.worker is not None:
        print(MARKER+json.dumps(observe(*args.worker),ensure_ascii=False,default=str),flush=True)
        return 0
    require(args.timeout>0,'POSITIVE_TIMEOUT_REQUIRED')
    return run(args.dry_run,args.timeout)


if __name__ == '__main__':
    raise SystemExit(main())
