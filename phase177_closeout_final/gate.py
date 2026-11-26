"""Verify saved Phase 177 measurements and publish five complete documents."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
import time
import traceback
import zipfile

from .documents import DOCUMENTS, MARKER, render_full, sections

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'phase177_closeout_final'
HEAD = '70d3ba540adebe96ada08728d045c1153e7e919a'
REVIEWED_PACKAGE_HEAD = 'a8d61bf5cf0953a33d8b0985f78ebb75fd62ad3c'
PASS = 'PASS_PHASE177_ACTIVE_SCOPE_CLOSED_WITH_HISTORICAL_GUARD_OPEN'
R1_PASS = 'PASS_PHASE177_CLOSEOUT_SCOPED_MEASUREMENT_DOCUMENTS_PENDING'
SCRIPT_PINS = {
    'phase177_closeout_measurement/gate.py': 'b50c6cc8f1745f57f948d15935c831e34ff38eef2aadf7cf6ecfc17fb8ca2670',
    'phase177_closeout_measurement_r1/gate.py': 'bb7823970491a6586d44978655ce78303bf5682b5722bdc434a51d3dca7cc6f5',
}
PACKAGE_COMMIT_PINS = {'phase177_closeout_measurement/README.md': '9a0f78247e35f9ba6eb586b8946171bb3e7941dc', 'phase177_closeout_measurement/__init__.py': '13f6b169fe3987b0b95aa5012c6f32250366eaf3', 'phase177_closeout_measurement/gate.py': '452220f322e09335dbafa3a4d379d92a1c75b487', 'phase177_closeout_measurement/run.ps1': 'c0b1053d5b35648dc7c604007ed3bcf12adcfc00', 'phase177_closeout_measurement_r1/README.md': '491c470e4012546069fee21e88ab49f899ce9c51', 'phase177_closeout_measurement_r1/__init__.py': '8b209d7a664cf77d3d0f9964350dd480750f871c', 'phase177_closeout_measurement_r1/gate.py': '6ea4e3325810bab9e9316d0a63405b2d867f3514', 'phase177_closeout_measurement_r1/run.ps1': '35abb532fd7cdcca57d3ea9faf5aad6ce4391e7a'}
DOC_PINS = {
    'README.md': 'fa641728ebfe696a2999da865847997e3a1122b0',
    'docs/design.md': '54586fae5c8d03b8963f557e053b5df7540cc772',
    'docs/development_log.md': '8bc7dc8bdd31da4ea4349a090a8fdc8acbca4bf2',
    'docs/roadmap.md': 'adb524f837c5b20b3e54ffcdfa22cda25da4cd6a',
    'docs/proof_records.md': 'fdb2b72410027742da4a0416f7723f096339f0bc',
}
EXPECTED_ACTIVE = {(n,k) for k in range(1,6) for n in range(2,k+2)}
EXPECTED_REMAINING = [(2,3),(3,3),(4,3),(2,4),(3,4),(4,4),(5,4)]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE177_CLOSEOUT_FINAL_'+key+'='+str(value), flush=True)


def digest(raw):
    return sha256(raw).hexdigest()


def evidence_dir():
    return Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'


def verify_scripts():
    for name, expected in SCRIPT_PINS.items():
        require(digest((ROOT/name).read_bytes().replace(b'\r\n',b'\n')) == expected, 'MEASUREMENT_SCRIPT_CHANGED:'+name)


def verify_reviewed_head(git, gt, matches_blob):
    current = gt('rev-parse','HEAD')
    require(current == gt('rev-parse','origin/develop'), 'LOCAL_REMOTE_HEAD_MISMATCH')
    require(current in (HEAD, REVIEWED_PACKAGE_HEAD), 'REVIEWED_HEAD_REQUIRED')
    if current == REVIEWED_PACKAGE_HEAD:
        git('merge-base','--is-ancestor',HEAD,current)
        changed = git('diff','--name-status','--no-renames',HEAD,current).decode('utf-8').splitlines()
        require(set(changed) == {'A\t'+name for name in PACKAGE_COMMIT_PINS}, 'PACKAGE_COMMIT_SCOPE_CHANGED')
        for name, pin in PACKAGE_COMMIT_PINS.items():
            require(gt('rev-parse',current+':'+name)==pin and matches_blob((ROOT/name).read_bytes(),pin),
                    'PACKAGE_COMMIT_PIN_CHANGED:'+name)
    return current


def verify_checkout(context):
    from phase177_closeout_measurement import gate as original
    from phase177_r18_final_verified_proof_audit import audit as r18
    from phase177_r2_cited_511_reuse_audit.audit import matches_blob
    from phase176_closeout.gate import ACTIVE_COMMAND, HISTORICAL
    from phase175_r4r14r11_closeout_preflight.audit import KNOWN_LEGACY_FAILURES
    git, gt = original.git, original.git_text
    require(Path(os.fsdecode(git('rev-parse','--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch','--show-current') == 'develop', 'DEVELOP_REQUIRED')
    current_head = verify_reviewed_head(git, gt, matches_blob)
    require(not git('diff','--cached','--name-only'), 'STAGED_CHANGES_REQUIRE_REVIEW')
    changed = original.paths(git('diff','--name-only','-z','HEAD'))
    require(changed <= set(DOCUMENTS), 'UNREVIEWED_TRACKED_CHANGES:'+repr(sorted(changed)))
    git('diff','--check')
    expected_pins = dict(original.PINS)
    expected_pins.update(r18.PINS)
    require(context['head'] == HEAD and context['pins'] == expected_pins, 'SAVED_SOURCE_PINS_CHANGED')
    require({p:expected_pins[p] for p in DOCUMENTS} == DOC_PINS, 'DOCUMENT_PINS_CHANGED')
    for name, pin in expected_pins.items():
        require(gt('rev-parse','HEAD:'+name)==pin, 'GIT_PIN_CHANGED:'+name)
        if name not in DOCUMENTS:
            require(matches_blob((ROOT/name).read_bytes(),pin), 'WORKTREE_PIN_CHANGED:'+name)
    require(gt('rev-parse','HEAD:stable_rules.py')=='1c226f40f658670271a6bcff7076a60515d6eeee' and matches_blob((ROOT/'stable_rules.py').read_bytes(),'1c226f40f658670271a6bcff7076a60515d6eeee'), 'STABLE_RULE_CHANGED')
    positions = r18.source_positions(ROOT)
    positions['toda:(5.11)'] = r18.verify_cited_511(ROOT)
    require(json.loads(json.dumps(positions,default=str)) == context['source_positions'], 'SOURCE_POSITIONS_CHANGED')
    require(tuple(KNOWN_LEGACY_FAILURES)==HISTORICAL==tuple(context['historical_tests']) and len(HISTORICAL)==4, 'HISTORICAL_SCOPE_CHANGED')
    require(all((ROOT/p.split('::')[0]).is_file() for p in HISTORICAL), 'HISTORICAL_FILE_MISSING')
    require(context['historical_status']=='FOUR_KNOWN_FAILURES_NOT_RERUN_NOT_PASSING', 'HISTORICAL_STATUS_CHANGED')
    require(tuple(context['active_command'])==ACTIVE_COMMAND, 'ACTIVE_COMMAND_CHANGED')
    require(context['test_baseline']==original.TEST_BASE and not git('diff','--name-only','-z',original.TEST_BASE,HEAD,'--','tests'), 'ACTIVE_TEST_TREE_CHANGED')
    tracked = original.paths(git('ls-tree','-r','--name-only','-z','HEAD','--','tests'))
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT/'tests').rglob('*.py') if p.is_file()}
    require(actual=={p for p in tracked if p.endswith('.py')} and len(actual)==context['active_test_python_files'], 'ACTIVE_TEST_INVENTORY_CHANGED')
    pairs = original.registered_pairs(ROOT/'data/sphere.csv')
    require(list(map(list,pairs))==context['pairs'], 'REGISTERED_DOMAIN_CHANGED')
    if not changed and current_head == HEAD:
        require(json.loads(json.dumps(original.preflight(),default=str))==context, 'LIVE_PREFLIGHT_MISMATCH')
    require(context['r18_head']==original.R18_HEAD, 'SAVED_R18_HEAD_CHANGED')
    if not changed:
        require(all(digest((ROOT/name).read_bytes())==context['documents'][name] for name in DOCUMENTS), 'DOCUMENT_BASELINE_CHANGED')
    return changed


def verify_evidence(base):
    from phase177_closeout_measurement import gate as original
    from phase177_closeout_measurement_r1 import gate as r1
    from stable_rules import is_in_toda_stable_range
    from homotopy_groups import TodaPrimaryGroup
    old, recovery = base/'phase177_closeout_measurement', base/'phase177_closeout_measurement_r1'
    files = {name:(recovery/name).read_bytes() for name in ('attempt.json','report.json','groups.jsonl')}
    hashes = {name:digest(raw) for name,raw in files.items()}
    report, attempt = json.loads(files['report.json']), json.loads(files['attempt.json'])
    expected = {'gate':R1_PASS,'head':HEAD,'phase177_formally_closed':False,'full_pytest_this_run':'NOT_RUN',
                'full_pytest':'PASS','full_pytest_exit':0,'passed':3546,'summary':'3546 passed in 40.59s',
                'stable_new_searches':0,'future_unstable_new_searches':0,'repository_unchanged':True,'k5_remaining':[]}
    require(all(report.get(k)==v for k,v in expected.items()), 'R1_REPORT_MISMATCH')
    context = report['preflight']
    verify_checkout(context)
    live_context = dict(context, pairs=list(map(tuple,context['pairs'])))
    previous, saved, old_hashes = r1.load_evidence(old,live_context)
    require(report['source_hashes']==attempt['old_evidence_hashes']==old_hashes and attempt['head']==HEAD, 'ORIGINAL_EVIDENCE_HASH_MISMATCH')
    for key in ('passed','summary','stdout_sha256','stderr_sha256','public_audit'):
        require(report[key]==previous[key], 'R1_ORIGINAL_RESULT_MISMATCH:'+key)
    pairs = tuple(map(tuple,context['pairs']))
    active, stable, future = r1.split_scope(pairs,lambda n,k:is_in_toda_stable_range(TodaPrimaryGroup(n+k,n)))
    require(set(active)==EXPECTED_ACTIVE and (len(active),len(stable),len(future))==(15,313,503), 'ACTIVE_SCOPE_CHANGED')
    require(report['scope']=={'active_unstable':list(map(list,active)),'stable_excluded_count':313,'future_unstable_excluded_count':503,'csv_registered_count':831}, 'R1_SCOPE_MISMATCH')
    remaining = [p for p in active if p not in saved]
    require(remaining==EXPECTED_REMAINING and attempt['remaining']==list(map(list,remaining)), 'R1_REMAINING_MISMATCH')
    rows = [json.loads(line) for line in files['groups.jsonl'].decode('utf-8').splitlines() if line.strip()]
    require(rows==report['groups'] and [(r['n'],r['k']) for r in rows]==list(active), 'R1_GROUP_ROWS_MISMATCH')
    for row in rows:
        p = row['n'],row['k']
        require(r1.valid_complete(row), 'ACTIVE_NOT_COMPLETE:'+repr(p))
        if p in saved:
            require(row==dict(saved[p],measurement_origin='original_interrupted_run'), 'REUSED_ROW_MISMATCH:'+repr(p))
        else:
            require(row['measurement_origin']=='r1_new_search', 'NEW_ROW_ORIGIN_MISMATCH:'+repr(p))
    k5 = [saved[(n,5)] for n in range(2,8)]
    require(report['k5_groups']==k5 and all(r1.valid_complete(r) and r['web']['status']=='rendered' for r in k5), 'K5_GROUP_MISMATCH')
    for name, measured, count in [('active_unstable_summary',rows,15),('k5_summary',k5,6)]:
        require(report[name]==original.summarize(measured)=={'complete':count,'partial':0,'search_failed':0,'not_searched':0,'registered':count,'incomplete':0,'unmeasured':0}, 'SUMMARY_MISMATCH:'+name)
    return report, {'original':old_hashes,'r1':hashes}


def document_plan(report, hashes, final_root):
    from phase177_closeout_measurement import gate as original
    from phase177_r2_cited_511_reuse_audit.audit import matches_blob
    additions = sections(report,hashes['r1']['report.json'])
    plan = {}
    for name in DOCUMENTS:
        current = (ROOT/name).read_bytes()
        committed = original.git('show',HEAD+':'+name)
        lf = committed.replace(b'\r\n',b'\n')
        candidates = [current,committed,lf,lf.replace(b'\n',b'\r\n')]
        candidates += [p.read_bytes() for p in sorted(final_root.glob('attempt_*/original_full/'+name)) if p.is_file()]
        baseline = next((raw for raw in candidates if digest(raw)==report['preflight']['documents'][name] and matches_blob(raw,DOC_PINS[name])),None)
        require(baseline is not None,'ORIGINAL_DOCUMENT_NOT_RECOVERABLE:'+name)
        final = render_full(name,baseline,additions[name])
        require(current in (baseline,final),'UNREVIEWED_DOCUMENT_CONTENT:'+name)
        require(final.count(MARKER.encode())==1,'DOCUMENT_MARKER_MISMATCH:'+name)
        if name != 'README.md':
            require('不安定'.encode('utf-8') not in final, 'TERMINOLOGY_NOT_NORMALIZED:'+name)
        plan[name] = {'original':baseline,'current':current,'final':final,'state':'FINAL' if current==final else 'ORIGINAL'}
    return plan


def write_bundle(folder, plan):
    for name,row in plan.items():
        for kind,key in [('original_full','original'),('final_full','final')]:
            path = folder/kind/name
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('xb') as stream:
                stream.write(row[key])
            require(path.read_bytes()==row[key],'DOCUMENT_OUTPUT_MISMATCH:'+name)
    archive = folder/'EHP_Phase177_Final_Five_Full_Documents.zip'
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as zf:
        for name,row in plan.items():
            zf.writestr(name,row['final'])
    with zipfile.ZipFile(archive) as zf:
        require(zf.testzip() is None and set(zf.namelist())==set(plan) and all(zf.read(n)==r['final'] for n,r in plan.items()),'FULL_ZIP_MISMATCH')
    return archive


def replace_document(target, expected, updated):
    require(target.read_bytes()==expected,'CONCURRENT_DOCUMENT_CHANGE:'+str(target))
    if expected==updated:
        return
    fd, name = tempfile.mkstemp(prefix=target.name+'.phase177-',dir=target.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(updated)
            stream.flush()
            os.fsync(stream.fileno())
        for i in range(3):
            require(target.read_bytes()==expected,'CONCURRENT_DOCUMENT_CHANGE:'+str(target))
            try:
                os.replace(temp,target)
                break
            except PermissionError:
                if i==2:
                    raise
                time.sleep(0.25)
        require(target.read_bytes()==updated,'APPLIED_DOCUMENT_MISMATCH:'+str(target))
    finally:
        if temp.exists():
            temp.unlink()


def run(dry_run=False):
    base = evidence_dir()
    final_root = base/PACKAGE
    folder = None
    result = {'gate':'FAIL_PHASE177_CLOSEOUT_FINAL','phase177_formally_closed':False,'full_pytest_this_run':'NOT_RUN','new_group_searches':0}
    try:
        require(not (final_root/'final_report.json').exists(),'FINAL_REPORT_ALREADY_EXISTS')
        verify_scripts()
        from phase177_closeout_measurement import gate as original
        report, hashes = verify_evidence(base)
        plan = document_plan(report,hashes,final_root)
        emit('HEAD',original.git_text('rev-parse','HEAD'))
        emit('MEASURED_HEAD',HEAD)
        emit('FULL_PYTEST','PASS_REUSED: '+report['summary'])
        emit('FULL_PYTEST_THIS_RUN','NOT_RUN')
        emit('NEW_GROUP_SEARCHES',0)
        emit('ACTIVE_UNSTABLE','15/15 complete')
        emit('K5','6/6 complete')
        emit('DOCUMENT_STATES',{n:r['state'] for n,r in plan.items()})
        if dry_run:
            emit('GATE','PASS_FINAL_READ_ONLY_DRYRUN')
            return 0
        final_root.mkdir(parents=True,exist_ok=True)
        folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=final_root))
        original.store(folder/'attempt.json',{'head':HEAD,'evidence_hashes':hashes,'document_states':{n:r['state'] for n,r in plan.items()},'started_utc':datetime.now(timezone.utc).isoformat()})
        result.update(head=HEAD,checkout_head=original.git_text('rev-parse','HEAD'),passed=report['passed'],summary=report['summary'],full_pytest_exit=0,
                      stdout_sha256=report['stdout_sha256'],stderr_sha256=report['stderr_sha256'],
                      historical_status=report['preflight']['historical_status'],historical_tests=report['preflight']['historical_tests'],
                      active_unstable_summary=report['active_unstable_summary'],k5_summary=report['k5_summary'],scope=report['scope'],public_audit=report['public_audit'],evidence_hashes=hashes)
        archive = write_bundle(folder,plan)
        result['archive'] = str(archive)
        emit('FULL_DOCUMENT_ZIP',archive)
        require(verify_evidence(base)[1]==hashes,'EVIDENCE_CHANGED_BEFORE_APPLY')
        # Each replacement is atomic; a subsequent attempt can recognize only
        # the exact original or exact generated bytes. No unsafe rollback.
        for name,row in plan.items():
            replace_document(ROOT/name,row['current'],row['final'])
            emit('DOCUMENT_APPLIED',name)
        require(verify_evidence(base)[1]==hashes,'EVIDENCE_CHANGED_AFTER_APPLY')
        require(verify_checkout(report['preflight'])==set(DOCUMENTS),'FINAL_TRACKED_DIFF_MISMATCH')
        require(all((ROOT/n).read_bytes()==r['final'] for n,r in plan.items()),'FINAL_DOCUMENT_BYTES_CHANGED')
        result['documents'] = [{'path':n,'before_sha256':digest(r['original']),'after_sha256':digest(r['final']),'full_bytes':len(r['final'])} for n,r in plan.items()]
        result.update(gate=PASS,phase177_formally_closed=True)
    except BaseException as exc:
        result.update(error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    if folder is not None:
        result['completed_utc']=datetime.now(timezone.utc).isoformat()
        original.store(folder/'report.json',result)
        if result['phase177_formally_closed']:
            with (final_root/'final_report.json').open('x',encoding='utf-8') as stream:
                json.dump(result,stream,ensure_ascii=False,indent=2,default=str)
        emit('REPORT',folder/'report.json')
    emit('PHASE177_FORMALLY_CLOSED',result['phase177_formally_closed'])
    emit('GATE',result['gate'])
    return 0 if result['phase177_formally_closed'] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    return run(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
