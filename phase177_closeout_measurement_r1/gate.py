"""Recover interrupted measurement without rerunning full pytest or stable groups."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

PACKAGE = 'phase177_closeout_measurement_r1'
HEAD = '70d3ba540adebe96ada08728d045c1153e7e919a'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE177_CLOSEOUT_R1_'+key+'='+str(value), flush=True)


def split_scope(pairs, is_stable):
    active, stable, future = [], [], []
    for n, k in pairs:
        if is_stable(n, k):
            stable.append((n,k))
        elif k <= 5:
            active.append((n,k))
        else:
            future.append((n,k))
    return tuple(active), tuple(stable), tuple(future)


def read_rows(path, pairs, embedded):
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    require(rows == embedded, 'ORIGINAL_REPORT_AND_JSONL_DISAGREE')
    actual = [(r['n'],r['k']) for r in rows]
    require(actual == list(pairs[:len(rows)]) and len(set(actual)) == len(actual), 'INVALID_ORIGINAL_PREFIX')
    return {(r['n'],r['k']):r for r in rows}


def valid_complete(row):
    return (row.get('status') == 'complete' and row.get('open_goal_count') == 0
            and row.get('open_goals') == [] and row.get('root_step_count') == 1
            and row.get('conclusion') is not None)


def load_evidence(old, context):
    from phase176_closeout.gate import parse_summary, ACTIVE_COMMAND
    names = ('attempt.json','report.json','full_pytest_stdout.txt','full_pytest_stderr.txt',
             'groups.jsonl','root_proof_tree.json','narrative.md')
    hashes = {name:sha256((old/name).read_bytes()).hexdigest() for name in names}
    attempt = json.loads((old/'attempt.json').read_text(encoding='utf-8'))
    report = json.loads((old/'report.json').read_text(encoding='utf-8'))
    require(attempt['head'] == HEAD and attempt['command'][1:] == list(ACTIVE_COMMAND), 'OLD_TEST_COMMAND_CHANGED')
    require(report.get('gate') == 'FAIL_PHASE177_CLOSEOUT_MEASUREMENT' and report.get('error') == 'KeyboardInterrupt()', 'NOT_REVIEWED_INTERRUPTION')
    require(report['full_pytest'] == 'PASS' and report['full_pytest_exit'] == 0, 'OLD_FULL_PYTEST_NOT_PASS')
    require(report['stdout_sha256'] == hashes['full_pytest_stdout.txt'] and report['stderr_sha256'] == hashes['full_pytest_stderr.txt'], 'OLD_LOG_HASH_MISMATCH')
    count, summary = parse_summary((old/'full_pytest_stdout.txt').read_text(encoding='utf-8',errors='replace'),0)
    require(count == report['passed'] == 3546 and summary == report['summary'] == '3546 passed in 40.59s', 'OLD_TEST_SUMMARY_MISMATCH')
    # JSON-normalize tuples in the current preflight to compare with saved JSON.
    require(report['preflight'] == json.loads(json.dumps(context,default=str)), 'OLD_PREFLIGHT_MISMATCH')
    a = report['public_audit']
    expected = {'status':'complete','web_key':'generic-complete-proof','open_goals':0,
                'root_ancestor_nodes':43,'root_inferences':35,'root_given_leaves':8,
                'reference_count':8,'target_group_given':0,'search_lookup_mode':'typed_reference','narrative_verified':True}
    require(all(a.get(k)==v for k,v in expected.items()) and len(a['db_prior_leaves'])==4, 'OLD_PUBLIC_AUDIT_CHANGED')
    rows = read_rows(old/'groups.jsonl',context['pairs'],report['groups'])
    require(len(rows)==75 and all(valid_complete(r) for r in rows.values()), 'OLD_OBSERVED_PREFIX_CHANGED')
    k5 = [rows[(n,5)] for n in range(2,8)]
    require(all(r.get('web',{}).get('status')=='rendered' for r in k5), 'OLD_K5_WEB_NOT_RENDERED')
    return report, rows, hashes


def run(dry_run, timeout):
    from phase177_closeout_measurement import gate as original
    from phase176_closeout.gate import checkout_state
    from homotopy_groups import TodaPrimaryGroup
    from stable_rules import is_in_toda_stable_range
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'
    old = base/'phase177_closeout_measurement'
    out = base/PACKAGE
    report = {'gate':'FAIL_PHASE177_CLOSEOUT_R1','phase177_formally_closed':False,'full_pytest_this_run':'NOT_RUN'}
    started = False
    try:
        require(not (out/'report.json').exists() and not (out/'attempt.json').exists(), 'R1_EXISTING_ATTEMPT_REQUIRES_REVIEW')
        context = original.preflight()
        require(original.git_text('rev-parse','HEAD:stable_rules.py') == '1c226f40f658670271a6bcff7076a60515d6eeee', 'STABLE_RULE_PIN_CHANGED')
        active, stable, future = split_scope(context['pairs'],lambda n,k:is_in_toda_stable_range(TodaPrimaryGroup(n+k,n)))
        require((len(active),len(stable),len(future))==(15,313,503),'SCOPE_COUNTS_CHANGED')
        previous, saved, hashes = load_evidence(old, context)
        remaining = [p for p in active if p not in saved]
        require(len(remaining)==7,'UNEXPECTED_REMAINING_SCOPE')
        for key,value in [('HEAD',HEAD),('CSV_REGISTERED',831),('ACTIVE_UNSTABLE',len(active)),('STABLE_EXCLUDED',len(stable)),('FUTURE_UNSTABLE_EXCLUDED',len(future)),('ACTIVE_REUSED',len(active)-len(remaining)),('ACTIVE_TO_SEARCH',remaining),('FULL_PYTEST','PASS_REUSED'),('FULL_PYTEST_THIS_RUN','NOT_RUN')]:
            emit(key,value)
        if dry_run:
            emit('GATE','PASS_R1_READ_ONLY_DRYRUN')
            return 0
        before = checkout_state()
        out.mkdir(parents=True,exist_ok=True)
        with (out/'attempt.json').open('x',encoding='utf-8') as stream:
            started = True
            json.dump({'head':HEAD,'old_evidence_hashes':hashes,'remaining':remaining},stream,indent=2)
        report.update(preflight=context,head=HEAD,source_report=str(old/'report.json'),source_hashes=hashes,
                      full_pytest='PASS',full_pytest_exit=0,passed=previous['passed'],summary=previous['summary'],
                      stdout_sha256=previous['stdout_sha256'],stderr_sha256=previous['stderr_sha256'],
                      public_audit=previous['public_audit'],scope={'active_unstable':active,'stable_excluded_count':len(stable),
                      'future_unstable_excluded_count':len(future),'csv_registered_count':831},groups=[])
        with (out/'groups.jsonl').open('x',encoding='utf-8') as stream:
            for n,k in active:
                reused = (n,k) in saved
                row = dict(saved[(n,k)] if reused else original.worker(n,k,timeout))
                row['measurement_origin'] = 'original_interrupted_run' if reused else 'r1_new_search'
                report['groups'].append(row)
                stream.write(json.dumps(row,ensure_ascii=False,default=str)+'\n')
                stream.flush()
                emit('GROUP',f'n={n} k={k} status={row["status"]} origin={row["measurement_origin"]}')
                require(valid_complete(row),'ACTIVE_UNSTABLE_NOT_COMPLETE:'+str((n,k)))
        report['active_unstable_summary'] = original.summarize(report['groups'])
        report['k5_groups'] = [saved[(n,5)] for n in range(2,8)]
        report['k5_summary'] = original.summarize(report['k5_groups'])
        report['k5_remaining'] = []
        report['stable_new_searches'] = 0
        report['future_unstable_new_searches'] = 0
        require(checkout_state()==before,'REPOSITORY_CHANGED_DURING_RECOVERY')
        require(all(sha256((old/name).read_bytes()).hexdigest()==digest for name,digest in hashes.items()),'ORIGINAL_EVIDENCE_CHANGED')
        original.git('diff','--check')
        report['repository_unchanged']=True
        report['gate']='PASS_PHASE177_CLOSEOUT_SCOPED_MEASUREMENT_DOCUMENTS_PENDING'
    except BaseException as exc:
        report.update(error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    if started:
        (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
        emit('REPORT',out/'report.json')
    for key in ('full_pytest','full_pytest_this_run','passed','summary','active_unstable_summary','k5_summary','phase177_formally_closed','gate'):
        if key in report:
            emit(key.upper(),report[key])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--timeout',type=int,default=90)
    args = parser.parse_args()
    require(args.timeout>0,'POSITIVE_TIMEOUT_REQUIRED')
    return run(args.dry_run,args.timeout)


if __name__ == '__main__':
    raise SystemExit(main())
