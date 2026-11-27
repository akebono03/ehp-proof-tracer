"""Validate the pinned measurement and publish five full Markdown documents."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import traceback
import xml.etree.ElementTree as ET
import zipfile

from .documents import DOCUMENTS, MARKER, render_full, sections

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '2f15ad21e68c6a3f8d8ac6e16a9c1f26b2b29f7a'
MEASURED_HEAD = 'c3e873b8c5fe5b69c895a48d0c55bad759b7f107'
MEASUREMENT = 'phase178_closeout_measurement'
ATTEMPT = 'attempt_jwjqk6a6'
MEASUREMENT_BLOBS = {
    MEASUREMENT + '/__init__.py': 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    MEASUREMENT + '/gate.py': '73501226d26ebf58f72938716bbd8aeb8e87ee0a',
    MEASUREMENT + '/run.ps1': '7fdcba0a2dd7bb7482a3805942f587cc90266924',
    MEASUREMENT + '/tests/test_gate.py': 'bf0fe7379fc13399b2c92bdd4eff3ce3ff210d18',
}
MEASUREMENT_GATE = 'PASS_PHASE178_CLOSEOUT_MEASURED_DOCUMENTS_PENDING'
EXPECTED_STEPS = (18, 3, 27, 3, 60, 7, 3, 25, 6, 24, 3, 62, 6, 43, 23,
                  3, 20, 6, 18, 18, 18)
EXPECTED_TOTALS = {'proven_step_count':83,'given_count':27,'inference_count':56,
                   'model_citation_count':27,'target_given_count':0,'open_goal_count':0}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_FINAL_' + key + '=' + str(value), flush=True)


def digest(raw):
    return sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def gt(*args):
    return os.fsdecode(git(*args)).strip()


def paths(raw):
    return {os.fsdecode(p) for p in raw.split(b'\0') if p}


def checked_json(raw):
    return json.loads(raw.decode('utf-8'))


def validate_headline(report):
    expected = dict(gate=MEASUREMENT_GATE, head=MEASURED_HEAD, dry_run=False,
                    phase178_formally_closed=False, full_pytest='PASS', full_pytest_exit=0,
                    passed=3546, summary='3546 passed in 54.95s', repository_unchanged=True,
                    historical_guard='RESOLVED_6_OF_6_PASS',
                    stable_boundary_status='DEFERRED_PHASE179_PARTIAL', k6_totals=EXPECTED_TOTALS)
    for key, value in expected.items():
        require(key in report and report[key] == value, 'MEASUREMENT_CONTRACT_CHANGED:' + key)
    require(report['focused']['passed'] == 189 and report['focused']['exit_code'] == 0,
            'FOCUSED_MEASUREMENT_CHANGED')
    require('error' not in report and 'traceback' not in report, 'MEASUREMENT_HAS_ERROR')


def validate_narrative(n, text, count):
    require(text.rstrip().endswith('□'), 'NARRATIVE_END_MISSING:' + str(n))
    numbers = [int(x) for x in re.findall(r'^\*\*\[R(\d+)\] ', text, re.MULTILINE)]
    require(numbers == list(range(1, count + 1)), 'NARRATIVE_CITATION_HEADINGS_CHANGED:' + str(n))
    require(MARKER not in text, 'NARRATIVE_CONTAINS_CLOSEOUT_MARKER')


def preflight():
    from phase178_r1_k6_source_first_audit import audit as r1
    from phase178_closeout_measurement import gate as m
    from phase177_closeout_measurement import gate as previous
    from phase176_closeout.gate import ACTIVE_COMMAND, HISTORICAL
    from phase175_r4r14r11_closeout_preflight.audit import KNOWN_LEGACY_FAILURES
    from homotopy_groups import TodaPrimaryGroup
    from stable_rules import is_in_toda_stable_range
    require(Path(gt('rev-parse','--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch','--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(gt('rev-parse','HEAD') == gt('rev-parse','origin/develop') == HEAD,
            'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not git('status','--porcelain','--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    git('diff','--check')
    git('merge-base','--is-ancestor', MEASURED_HEAD, HEAD)
    require(paths(git('diff','--name-only','-z', MEASURED_HEAD, HEAD)) == set(MEASUREMENT_BLOBS),
            'POST_MEASUREMENT_DIFF_CHANGED')
    require(m.HEAD == MEASURED_HEAD and tuple(m.ACTIVE_COMMAND) == ACTIVE_COMMAND,
            'MEASUREMENT_COMMAND_CHANGED')
    for path, blob in dict(m.PINS, **MEASUREMENT_BLOBS).items():
        require(gt('rev-parse','HEAD:'+path) == blob and r1.blob_matches(ROOT/path,blob),
                'PIN_CHANGED:'+path)
    require(tuple(KNOWN_LEGACY_FAILURES) == HISTORICAL and len(HISTORICAL) == 4,
            'HISTORICAL_SCOPE_CHANGED')
    require(all((ROOT/p.split('::')[0]).is_file() for p in HISTORICAL), 'HISTORICAL_FILE_MISSING')
    require(all((ROOT/p).is_file() for p in m.FOCUSED), 'FOCUSED_FILE_MISSING')
    tracked = {os.fsdecode(p) for p in git('ls-tree','-r','--name-only','-z','HEAD','--','tests').split(b'\0') if p.endswith(b'.py')}
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT/'tests').rglob('*.py') if p.is_file()}
    require(actual == tracked and len(actual) == 242, 'ACTIVE_TEST_INVENTORY_CHANGED')
    pairs = previous.registered_pairs(ROOT/'data/sphere.csv')
    active, stable, future = m.split_scope(pairs,lambda n,k:is_in_toda_stable_range(TodaPrimaryGroup(n+k,n)))
    m.validate_scope(active,stable,future)
    require((8,6) in stable,'STABLE_BOUNDARY_CHANGED')
    return {'head':MEASURED_HEAD,'pins':m.PINS,
            'documents':{p:digest((ROOT/p).read_bytes()) for p in DOCUMENTS},
            'active_test_python_files':len(actual),'active_command':list(ACTIVE_COMMAND),
            'focused_tests':list(m.FOCUSED),'historical_tests':list(HISTORICAL),
            'historical_status':'FOUR_KNOWN_FAILURES_NOT_RERUN_NOT_PASSING',
            'scope':{'active_unstable':list(map(list,active)), 'stable_excluded_count':len(stable),
                     'future_unstable_excluded_count':len(future),'csv_registered_count':len(pairs)}}


def verify_evidence(folder, context):
    from phase178_closeout_measurement import gate as m
    from phase177_closeout_measurement import gate as previous
    from phase176_closeout.gate import parse_summary
    from phase178_r29_final_6stem_audit import audit as r29
    evidence = {}

    def read(name):
        raw = (folder/name).read_bytes()
        evidence[name] = digest(raw)
        return raw

    report = checked_json(read('report.json'))
    validate_headline(report)
    require(report['preflight'] == context and report['scope'] == context['scope'],
            'MEASUREMENT_PREFLIGHT_MISMATCH')
    for label, key, args, count in (
        ('full_pytest', 'full_pytest_evidence', list(m.ACTIVE_COMMAND), 3546),
        ('focused', 'focused', ['-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*m.FOCUSED], 189),
    ):
        record = report[key]
        require(record['exit_code'] == 0, 'NONZERO_PYTEST_EXIT:' + label)
        command = record['command']
        require(command[1:-1] == args and command[-1].startswith('--junitxml=') and
                Path(command[-1].split('=',1)[1]).resolve() == (folder/(label+'.xml')).resolve(),
                'PYTEST_COMMAND_MISMATCH:' + label)
        for suffix, field in (('_stdout.txt','stdout_sha256'),('_stderr.txt','stderr_sha256'),('.xml','xml_sha256')):
            name = label+suffix
            read(name)
            require(evidence[name] == record[field], 'EVIDENCE_HASH_MISMATCH:'+name)
        xml_path = folder/(label+'.xml')
        m.inspect_junit(xml_path, record['exit_code'], count, expected_count=count)
        output = (folder/(label+'_stdout.txt')).read_text(encoding='utf-8',errors='replace')
        if label == 'full_pytest':
            measured_count, measured_summary = parse_summary(output, record['exit_code'])
            require((measured_count,measured_summary) == (report['passed'],report['summary']), 'FULL_SUMMARY_MISMATCH')
            require(report['stdout_sha256']==record['stdout_sha256'] and report['stderr_sha256']==record['stderr_sha256'], 'FULL_LOG_HASH_MISMATCH')
        else:
            cases = list(ET.parse(xml_path).getroot().iter('testcase'))
            legacy = [c for c in cases if c.get('classname','').endswith('test_r4c_pi64_suspension_iso')]
            require(len(legacy)==6 and 'PHASE178_R30R1_HISTORICAL_REPLAY=VERIFIED' in output
                    and 'PHASE178_R30R1_PRIOR_SOURCES=VERIFIED' in output,
                    'R4C_EVIDENCE_MISMATCH')
    rows = [json.loads(line) for line in read('groups.jsonl').decode('utf-8').splitlines() if line.strip()]
    require(rows == report['groups'] and [(r['n'],r['k']) for r in rows] == list(m.EXPECTED), 'GROUP_ROWS_MISMATCH')
    require(tuple(r['proven_step_count'] for r in rows) == EXPECTED_STEPS, 'GROUP_STEP_COUNTS_CHANGED')
    k6 = [r for r in rows if r['k']==6]
    require(k6 == report['k6_groups'], 'K6_ROWS_MISMATCH')
    for key, group_rows, count in (('active_unstable_summary',rows,21),('k6_summary',k6,6)):
        require(report[key] == previous.summarize(group_rows) == dict(complete=count,partial=0,search_failed=0,
                    not_searched=0,registered=count,incomplete=0,unmeasured=0), 'GROUP_SUMMARY_MISMATCH:'+key)
    narratives = {}
    for row in rows:
        n,k = row['n'],row['k']
        if k!=6:
            m.validate_prior(n,k,row)
            continue
        audit = checked_json(read(f'n{n}_audit.json'))
        require(audit == row['public_audit'], 'AUDIT_REPORT_MISMATCH:'+str(n))
        r29.validate_summary(n,audit['summary'])
        m.validate_k6(n,audit)
        expected_row = {'n':n,'k':k,'status':'complete','open_goal_count':0,'open_goals':[],
                        'root_step_count':1,'conclusion':audit['conclusion'],
                        'proven_step_count':audit['summary']['proven_step_count'],
                        'reference_count':audit['summary']['reference_count'],
                        'model_citation_count':audit['model_citation_count'],'given_count':audit['given_count'],
                        'inference_count':audit['inference_count'],'trust_status':'VERIFIED',
                        'target_given_count':0,'web_key':'generic-complete-proof','public_audit':audit}
        require(row == expected_row, 'K6_PUBLIC_ROW_MISMATCH:'+str(n))
        detail_name = f'n{n}_k6.json'
        require(Path(audit['summary']['detail']).resolve() == (folder/detail_name).resolve(), 'DETAIL_PATH_MISMATCH')
        detail = checked_json(read(detail_name))
        require(evidence[detail_name] == audit['summary']['detail_sha256'], 'DETAIL_HASH_MISMATCH')
        require(detail['conclusion'] == audit['conclusion'] and detail['trust_status']=='VERIFIED'
                and detail['target_given_count']==0 and not detail['open_goals'], 'DETAIL_CONTRACT_CHANGED')
        text = read(f'n{n}_narrative.md').decode('utf-8')
        validate_narrative(n,text,audit['model_citation_count'])
        narratives[n] = text
    totals = {key:sum(r[key] for r in k6) for key in EXPECTED_TOTALS}
    require(totals == report['k6_totals'] == EXPECTED_TOTALS, 'K6_TOTAL_MISMATCH')
    boundary = checked_json(read('stable_boundary.json'))
    require(boundary == report['stable_boundary'] and boundary['open_goal_count']==8,'BOUNDARY_EVIDENCE_MISMATCH')
    r29.validate_boundary(boundary)
    return report,evidence,narratives


def prepare_documents(report, evidence, narratives, context, out):
    additions = sections(report,evidence['report.json'],narratives)
    require(set(additions)==set(DOCUMENTS),'DOCUMENT_SET_CHANGED')
    originals, updated = {}, {}
    for name in DOCUMENTS:
        raw = (ROOT/name).read_bytes()
        require(digest(raw)==context['documents'][name],'DOCUMENT_BASELINE_CHANGED:'+name)
        require(b'PHASE177_FINAL_CLOSEOUT_20261126' in raw, 'PRIOR_CLOSEOUT_MARKER_MISSING:'+name)
        originals[name] = raw
        updated[name] = render_full(name,raw,additions[name])
        require(updated[name].count(MARKER.encode())==1 and updated[name]!=raw,'INVALID_DOCUMENT_OUTPUT:'+name)
        for part,content in (('original_full',raw),('final_full',updated[name])):
            target = out/part/name
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(content)
            require(target.read_bytes()==content,'DOCUMENT_OUTPUT_WRITE_FAILED:'+name)
    archive = out/'EHP_Phase178_Closeout_Final_Documents.zip'
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for name in DOCUMENTS:
            z.writestr(name,updated[name])
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None and set(z.namelist())==set(DOCUMENTS),'DOCUMENT_ZIP_INVALID')
        require(all(z.read(name)==updated[name] for name in DOCUMENTS),'DOCUMENT_ZIP_CONTENT_MISMATCH')
    return originals,updated,archive


def run(dry_run):
    from phase178_closeout_measurement import gate as m
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'
    source = base/MEASUREMENT/ATTEMPT
    base_out = base/PACKAGE
    base_out.mkdir(parents=True,exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix='attempt_',dir=base_out))
    result = dict(gate='FAIL_PHASE178_CLOSEOUT_FINAL',phase178_formally_closed=False,
                  dry_run=dry_run,full_pytest_this_run='NOT_RUN',new_group_searches=0)
    originals, written = {}, []
    try:
        context = preflight()
        before_untracked = git('ls-files','--others','--exclude-standard','-z')
        report,evidence,narratives = verify_evidence(source,context)
        emit('HEAD',HEAD)
        emit('MEASURED_HEAD',MEASURED_HEAD)
        emit('MEASUREMENT_EVIDENCE','VERIFIED')
        emit('FULL_PYTEST','PASS_REUSED: '+report['summary'])
        emit('FOCUSED_PASSED',report['focused']['passed'])
        emit('ACTIVE_COMPLETE','21/21')
        emit('K6_COMPLETE','6/6')
        emit('HISTORICAL_GUARD',report['historical_guard'])
        emit('LEGACY_SOURCE_GUARDS',context['historical_status'])
        emit('STABLE_BOUNDARY',report['stable_boundary_status'])
        originals,updated,archive = prepare_documents(report,evidence,narratives,context,out)
        require(all(digest((source/name).read_bytes())==value for name,value in evidence.items()), 'MEASUREMENT_EVIDENCE_CHANGED')
        require(preflight()==context,'BASELINE_CHANGED_DURING_DOCUMENT_GENERATION')
        result.update(head=HEAD,measured_head=MEASURED_HEAD,measurement_report=str(source/'report.json'),
                      measurement_hashes=evidence,full_pytest='PASS_REUSED',passed=report['passed'],summary=report['summary'],
                      focused_passed=report['focused']['passed'],active_unstable_summary=report['active_unstable_summary'],
                      k6_summary=report['k6_summary'],k6_totals=report['k6_totals'],scope=report['scope'],
                      historical_guard=report['historical_guard'],legacy_source_guards=context['historical_status'],
                      stable_boundary_status=report['stable_boundary_status'],stable_boundary_open_goals=8,
                      documents={name:{'original_sha256':digest(originals[name]),'final_sha256':digest(updated[name]),
                                       'final_bytes':len(updated[name])} for name in DOCUMENTS},
                      documents_zip=str(archive),documents_zip_sha256=digest(archive.read_bytes()))
        if dry_run:
            require(not git('diff','--name-only','HEAD'),'DRYRUN_CHANGED_TRACKED_FILES')
            result['gate']='PASS_PHASE178_CLOSEOUT_FINAL_DRYRUN'
        else:
            for name in DOCUMENTS:
                target = ROOT/name
                require(target.read_bytes()==originals[name], 'DOCUMENT_CHANGED_BEFORE_WRITE:'+name)
                written.append(name)
                target.write_bytes(updated[name])
                require(target.read_bytes()==updated[name],'DOCUMENT_WRITE_FAILED:'+name)
            require(paths(git('diff','--name-only','-z','HEAD'))==set(DOCUMENTS),'UNEXPECTED_TRACKED_DIFF')
            require(not git('diff','--cached','--name-only'),'UNEXPECTED_STAGED_DIFF')
            git('diff','--check')
            require(gt('rev-parse','HEAD')==gt('rev-parse','origin/develop')==HEAD,'HEAD_CHANGED_DURING_FINAL')
            require(all(digest((source/name).read_bytes())==value for name,value in evidence.items()), 'MEASUREMENT_EVIDENCE_CHANGED')
            result.update(gate='PASS_PHASE178_CLOSEOUT_FINAL',phase178_formally_closed=True)
        require(git('ls-files','--others','--exclude-standard','-z')==before_untracked,'UNTRACKED_INVENTORY_CHANGED')
        m.store(out/'report.json',result)
    except BaseException as exc:
        rollback_errors = []
        for name in reversed(written):
            try:
                (ROOT/name).write_bytes(originals[name])
                require((ROOT/name).read_bytes()==originals[name],'ROLLBACK_MISMATCH:'+name)
            except Exception as rollback_exc:
                rollback_errors.append(repr(rollback_exc))
        result.update(gate='FAIL_PHASE178_CLOSEOUT_FINAL',phase178_formally_closed=False,
                      error=repr(exc),traceback=traceback.format_exc(),rollback_errors=rollback_errors)
        emit('ERROR',repr(exc))
        m.store(out/'report.json',result)
    emit('REPORT',out/'report.json')
    if result.get('documents_zip'):
        emit('FULL_DOCUMENTS_ZIP',result['documents_zip'])
        emit('FULL_DOCUMENTS_DIRECTORY',out/'final_full')
    emit('FULL_PYTEST_THIS_RUN','NOT_RUN')
    emit('NEW_GROUP_SEARCHES',0)
    emit('PHASE178_FORMALLY_CLOSED',result['phase178_formally_closed'])
    emit('GATE',result['gate'])
    return 0 if result['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    return run(args.dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
