"""Restore the reviewed active test inventory, preserving every removed byte."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '471d79109d3054b088c7f910372b5f4f6cd5efa1'
BASE = '90e8025c31841e522b3bb36f002ec44dfd4b89aa'
INTRO = 'a47b073f2d1f730e6037c0cb57aaee27852a5d86'
PINS = {
    'tests/hopf_rules.py': '362ae6d1cac9d95082a963ebedd243f0e2b2e810',
    'tests/tests/test_expression.py': 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    'tests/tests/test_hopf_rules.py': 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    'tests/tests/test_phase77_applicability_provenance.py': '339e176a8c23a6a946bb13fb342b78823177fa10',
}
CANONICAL = {
    'hopf_rules.py': '5c8c127d2decdbe03f2da0b218b8b29f7f3d7c91',
    'tests/test_hopf_rules.py': 'a6a1d06b753f25963511cd5b9b97654be670a287',
    'tests/test_expression.py': '620267360db91127b5f6d74b395e89e59424e04d',
    'tests/conftest.py': '304c7b40eb1041475fb6bc4519d3ef61fd3275e2',
}
FAIL_STDOUT = '41156466594bef2736fac8d1fe0f5ae43203e7c997a08d1ec5aca1cf40320b22'
FAIL_STDERR = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
COLLECT_COMMAND = ('-B','-m','pytest','-q','--tb=short','--disable-warnings','-p','no:cacheprovider','--collect-only','tests')


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True).stdout


def sha(raw):
    return sha256(raw).hexdigest()


def blob(raw):
    from hashlib import sha1
    return sha1(b'blob '+str(len(raw)).encode('ascii')+b'\0'+raw).hexdigest()


def same_blob(raw, expected):
    # Windows checkout can alter CRLF. Only accept an exact or EOL-equivalent blob.
    lf = raw.replace(b'\r\n',b'\n')
    return expected in {blob(raw), blob(lf), blob(lf.replace(b'\n',b'\r\n'))}


def paths_at(ref):
    return {os.fsdecode(p) for p in git('ls-tree','-r','--name-only','-z',ref,'--','tests').split(b'\0') if p and p.endswith(b'.py')}


def verify_inventory(base, current):
    added, removed = current-base, base-current
    if added != set(PINS) or removed:
        raise RuntimeError('UNREVIEWED_ACTIVE_PYTHON_INVENTORY: '+repr({'added':sorted(added),'removed':sorted(removed)}))
    return {'baseline_python_files':len(base),'current_python_files':len(current),'introduced':sorted(added),'removed':[]}


def archive_path(name):
    return ROOT / PACKAGE / 'archive' / (name+'.txt')


def evidence_root():
    return Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'


def failed_evidence():
    folder = evidence_root()/'phase176_closeout'
    names = ('attempt.json','report.json','full_pytest_stdout.txt','full_pytest_stderr.txt')
    raw = {n:(folder/n).read_bytes() for n in names}
    report = json.loads(raw['report.json'])
    attempt = json.loads(raw['attempt.json'])
    if (report.get('head') != HEAD or attempt.get('head') != HEAD
            or report.get('gate') != 'FAIL_PHASE176_CLOSEOUT'
            or report.get('phase176_formally_closed') is not False
            or report.get('full_pytest_exit') != 2
            or report.get('stdout_sha256') != FAIL_STDOUT or report.get('stderr_sha256') != FAIL_STDERR
            or sha(raw['full_pytest_stdout.txt']) != FAIL_STDOUT or sha(raw['full_pytest_stderr.txt']) != FAIL_STDERR
            or b"No module named 'test_phase77_lemma516_scaled_bracket_sum'" not in raw['full_pytest_stdout.txt']):
        raise RuntimeError('FIRST_FAILURE_EVIDENCE_MISMATCH')
    return {n:sha(v) for n,v in raw.items()}


def tracked_changes():
    return {os.fsdecode(p) for p in git('diff','--name-only','-z','HEAD').split(b'\0') if p}


def actual_python_paths():
    return {p.relative_to(ROOT).as_posix() for p in (ROOT/'tests').rglob('*.py') if p.is_file()}


def preflight():
    if Path(os.fsdecode(git('rev-parse','--show-toplevel').strip())).resolve()!=ROOT.resolve():
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch','--show-current').strip()!=b'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED')
    for ref in ('HEAD','origin/develop'):
        if git('rev-parse',ref).decode('ascii').strip()!=HEAD:
            raise RuntimeError('UNREVIEWED_HEAD:'+ref)
    if git('diff','--cached','--name-only'):
        raise RuntimeError('STAGED_CHANGES_REQUIRE_REVIEW')
    inventory = verify_inventory(paths_at(BASE),paths_at(HEAD))
    introduced = paths_at(INTRO)-paths_at(INTRO+'^')
    if introduced != set(PINS):
        raise RuntimeError('INTRODUCTION_DIFF_CHANGED:'+repr(sorted(introduced)))
    for name,pin in {**PINS,**CANONICAL}.items():
        if git('rev-parse',HEAD+':'+name).decode('ascii').strip()!=pin:
            raise RuntimeError('UNREVIEWED_BLOB:'+name)
    for name,pin in CANONICAL.items():
        if not same_blob((ROOT/name).read_bytes(),pin):
            raise RuntimeError('CANONICAL_FILE_CHANGED:'+name)
    states = set()
    for name,pin in PINS.items():
        source, saved = ROOT/name,archive_path(name)
        if source.is_file() and not saved.exists() and same_blob(source.read_bytes(),pin):
            states.add('before')
        elif not source.exists() and saved.is_file() and same_blob(saved.read_bytes(),pin):
            states.add('after')
        else:
            raise RuntimeError('UNREVIEWED_ARCHIVE_STATE:'+name)
    if len(states)!=1:
        raise RuntimeError('PARTIAL_ARCHIVE_STATE')
    stage, = states
    expected = set() if stage=='before' else set(PINS)
    if tracked_changes()!=expected:
        raise RuntimeError('UNEXPECTED_TRACKED_CHANGES:'+repr(sorted(tracked_changes())))
    actual = actual_python_paths()
    wanted = paths_at(BASE) | (set(PINS) if stage=='before' else set())
    if actual!=wanted:
        raise RuntimeError('UNTRACKED_OR_MISSING_TEST_PYTHON_FILES:'+repr({'extra':sorted(actual-wanted),'missing':sorted(wanted-actual)}))
    git('diff','--check')
    return {'head':HEAD,'phase175_baseline':BASE,'introduced_commit':INTRO,'stage':stage,
            'inventory':inventory,'first_failure_evidence':failed_evidence(),'full_pytest':'NOT_RUN'}


def archive_files():
    """Copy exact bytes first, then unlink only the reviewed active paths."""
    originals = {name:(ROOT/name).read_bytes() for name in PINS}
    created, removed = [], []
    try:
        for name,raw in originals.items():
            if not same_blob(raw,PINS[name]):
                raise RuntimeError('SOURCE_CHANGED:'+name)
            dest = archive_path(name)
            dest.parent.mkdir(parents=True,exist_ok=True)
            with dest.open('xb') as out:
                created.append(dest)
                out.write(raw)
            if dest.read_bytes()!=raw:
                raise RuntimeError('ARCHIVE_BYTES_CHANGED:'+name)
        for name,raw in originals.items():
            if (ROOT/name).read_bytes()!=raw:
                raise RuntimeError('CONCURRENT_SOURCE_CHANGE:'+name)
            (ROOT/name).unlink()
            removed.append(name)
    except BaseException:
        for name in reversed(removed):
            with (ROOT/name).open('xb') as out:
                out.write(originals[name])
        for dest in reversed(created):
            dest.unlink()
        raise
    return {name:{'archive':archive_path(name).relative_to(ROOT).as_posix(),'sha256':sha(raw),'bytes':len(raw)} for name,raw in originals.items()}


def parse_collection(stdout, code):
    if code!=0:
        raise RuntimeError('COLLECTION_NONZERO_EXIT:'+str(code))
    rows=[line.strip() for line in stdout.splitlines() if re.fullmatch(r'\d+ tests? collected in .+',line.strip())]
    if len(rows)!=1:
        raise RuntimeError('COLLECTION_SUMMARY_NOT_UNIQUE_OR_DESELECTED')
    count=int(rows[0].split()[0])
    if count!=3546:
        raise RuntimeError('COLLECTION_COUNT_DIFFERS_FROM_PHASE175:'+str(count))
    return count,rows[0]


def store(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def run(dry_run=False):
    snap=preflight()
    print('PHASE176_CLOSEOUT_R1_HEAD='+HEAD)
    print('PHASE176_CLOSEOUT_R1_STAGE='+snap['stage'])
    if dry_run:
        print('PHASE176_CLOSEOUT_R1_GATE=PASS_R1_READ_ONLY_DRYRUN')
        return 0
    folder=evidence_root()/PACKAGE
    folder.mkdir(parents=True,exist_ok=True)
    attempt=folder/'attempt.json'
    # A failed collection is evidence; do not overwrite it automatically.
    with attempt.open('x',encoding='utf-8') as out:
        json.dump({'started_utc':datetime.now(timezone.utc).isoformat(),'preflight':snap},out,ensure_ascii=False,indent=2)
    report={'gate':'FAIL_PHASE176_CLOSEOUT_R1','phase176_formally_closed':False,'full_pytest':'NOT_RUN','preflight':snap}
    try:
        if snap['stage']=='before':
            report['archives']=archive_files()
        else:
            report['archives']={n:{'archive':archive_path(n).relative_to(ROOT).as_posix(),'sha256':sha(archive_path(n).read_bytes()),'bytes':archive_path(n).stat().st_size} for n in PINS}
        repaired=preflight()
        if repaired['stage']!='after' or repaired['first_failure_evidence']!=snap['first_failure_evidence']:
            raise RuntimeError('REPAIRED_PREFLIGHT_MISMATCH')
        before=(git('diff','--binary','HEAD'),git('status','--porcelain','-z'))
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
        stdout,stderr=folder/'collect_stdout.txt',folder/'collect_stderr.txt'
        print('PHASE176_CLOSEOUT_R1_COLLECTION=STARTED_NO_TEST_EXECUTION',flush=True)
        with stdout.open('wb') as out,stderr.open('wb') as err:
            result=subprocess.run([sys.executable,*COLLECT_COMMAND],cwd=ROOT,env=env,stdout=out,stderr=err,check=False)
        report.update(collection_exit=result.returncode,stdout_sha256=sha(stdout.read_bytes()),stderr_sha256=sha(stderr.read_bytes()))
        text=stdout.read_text(encoding='utf-8',errors='replace')
        print('\n'.join(text.splitlines()[-12:]))
        count,summary=parse_collection(text,result.returncode)
        if before!=(git('diff','--binary','HEAD'),git('status','--porcelain','-z')) or preflight()!=repaired:
            raise RuntimeError('REPOSITORY_OR_EVIDENCE_CHANGED_DURING_COLLECTION')
        if any(sha(archive_path(n).read_bytes())!=v['sha256'] for n,v in report['archives'].items()):
            raise RuntimeError('ARCHIVE_CHANGED_DURING_COLLECTION')
        report.update(collection_count=count,summary=summary,baseline_inventory_restored=True,first_failure_preserved=True,
                      gate='PASS_PHASE176_CLOSEOUT_R1_ACTIVE_COLLECTION_RESTORED')
    except BaseException as exc:
        report['error']=repr(exc)
    store(folder/'report.json',report)
    for key in ('collection_exit','collection_count','summary','first_failure_preserved','full_pytest','phase176_formally_closed','error','gate'):
        if key in report:
            print('PHASE176_CLOSEOUT_R1_'+key.upper()+'='+json.dumps(report[key],ensure_ascii=False))
    print('REPORT='+str(folder/'report.json'))
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    return run(parser.parse_args().dry_run)


if __name__=='__main__':
    raise SystemExit(main())
