"""Read-only Phase 178 measurement: active scope, historical R4C, full active suite."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = 'c3e873b8c5fe5b69c895a48d0c55bad759b7f107'
R4C = 'phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py'
ACTIVE_COMMAND = ('-B', '-m', 'pytest', '-q', '--tb=short', '--disable-warnings', '-p', 'no:cacheprovider', 'tests')
FOCUSED = (
    PACKAGE + '/tests/test_gate.py',
    R4C,
    'phase178_r29_final_6stem_audit/tests/test_audit.py',
    'phase178_r13_final_verified_proof_audit/tests/test_audit.py',
    'phase178_r12r2_zero_composition_elision/tests/test_projection.py',
    'phase178_r17r3_common_renderer/tests/test_display.py',
    'phase178_r23_common_renderer_elision/tests/test_display.py',
    'phase178_r26_n7_final_verified_proof_audit/tests/test_audit.py',
    'phase178_r27_stable_boundary_source_first_audit/tests/test_audit.py',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
    'phase178_r20f1_historical_guard_audit/tests/test_audit.py',
    'phase178_r30_historical_guard_final_audit/tests/test_audit.py',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
    'phase178_r20r1_suspension_isomorphism_bridge_public/tests/test_public.py',
)
DOCUMENTS = ('README.md', 'docs/design.md', 'docs/development_log.md', 'docs/roadmap.md', 'docs/proof_records.md')
PINS = {
    'README.md': '6d5d7e460ef320f0e1547d53b68754c1d2768794',
    'docs/design.md': 'aca84843720abca116f91274a9dfda4992f9c49a',
    'docs/development_log.md': '8b101a22a4a54d3a1d4563fc7749fb7743e0f427',
    'docs/proof_records.md': 'dbb18ad4c790731ce5eccefb63e237357d683816',
    'docs/roadmap.md': '11aff787afccee2ca9cbe7b9127efea521ee70cd',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'stable_rules.py': '1c226f40f658670271a6bcff7076a60515d6eeee',
    'tests/conftest.py': '304c7b40eb1041475fb6bc4519d3ef61fd3275e2',
    'tests/phase155_audit_only_nodeids.txt': 'e65284e1e108d4ce0c81b9f1cd1e41140238dc8f',
    R4C: 'b428cc4d5752a098fa3ca8f936b1fe29803e7125',
    'phase176_closeout/gate.py': 'b6f055a144e0c1b053d01b2ed9ccd4ef7ea90f35',
    'phase177_closeout_measurement/gate.py': '452220f322e09335dbafa3a4d379d92a1c75b487',
    'phase177_closeout_measurement_r1/gate.py': '6ea4e3325810bab9e9316d0a63405b2d867f3514',
    'phase178_r27_stable_boundary_source_first_audit/audit.py': 'f25e20b54115e9a66e23b1d29de6d4e1728272ca',
    'phase178_r29_final_6stem_audit/audit.py': '07d0df26eee37239807657d9d7f2b0500b55668d',
}
EXPECTED = tuple((n, k) for k in range(1, 7) for n in range(2, k + 2))
EXPECTED_K6 = {2: (3, 2, 1, 2), 3: (20, 5, 15, 5), 4: (6, 4, 2, 4),
               5: (18, 6, 12, 6), 6: (18, 5, 13, 5), 7: (18, 5, 13, 5)}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_CLOSEOUT_' + key + '=' + str(value), flush=True)


def store(path, data):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')
    temp.replace(path)


def split_scope(pairs, is_stable):
    pairs = tuple(pairs)
    require(len(pairs) == len(set(pairs)), 'DUPLICATE_COORDINATES')
    active, stable, future = [], [], []
    for n, k in pairs:
        if is_stable(n, k):
            stable.append((n, k))
        elif k <= 6:
            active.append((n, k))
        else:
            future.append((n, k))
    return tuple(sorted(active, key=lambda p: (p[1], p[0]))), tuple(stable), tuple(future)


def validate_scope(active, stable, future):
    require(tuple(active) == EXPECTED, 'ACTIVE_SCOPE_CHANGED')
    require((len(active), len(stable), len(future)) == (21, 313, 497), 'REGISTERED_SCOPE_CHANGED')


def validate_prior(n, k, row):
    require((row.get('n'), row.get('k')) == (n, k), 'WRONG_PRIOR_COORDINATES')
    require(row.get('status') == 'complete' and row.get('open_goal_count') == 0
            and row.get('open_goals') == [] and row.get('root_step_count') == 1
            and row.get('conclusion') is not None, 'PRIOR_GROUP_NOT_COMPLETE:' + repr((n, k)))
    if k == 5:
        require(row.get('web', {}).get('status') == 'rendered'
                and row.get('complete_invariants_hold') is True, 'K5_PUBLIC_CONTRACT_CHANGED')


def validate_k6(n, row):
    summary = row['summary']
    require((summary['n'], summary['k']) == (n, 6), 'WRONG_K6_COORDINATES')
    require(summary['status'] == 'complete' and summary['trust_status'] == 'VERIFIED'
            and summary['open_goal_count'] == 0 and summary['target_given_count'] == 0
            and summary['web_key'] == 'generic-complete-proof'
            and summary['complete_invariants_hold'] is True and summary['web_error'] is None
            and row['citation_audit'] == 'VERIFIED', 'K6_PUBLIC_CONTRACT_CHANGED')
    actual = (summary['proven_step_count'], row['given_count'], row['inference_count'], row['model_citation_count'])
    require(actual == EXPECTED_K6[n] and row['root_ancestor_count'] == actual[0], 'R29_STATISTICS_CHANGED')
    require(len(row['model_citations']) == actual[3] and row['citation_headings'] == list(range(1, actual[3]+1)),
            'R29_CITATION_STATISTICS_CHANGED')


def inspect_junit(path, exit_code, minimum, *, expected_count=None):
    require(exit_code == 0, 'PYTEST_NONZERO_EXIT:' + str(exit_code))
    cases = list(ET.parse(path).getroot().iter('testcase'))
    require(len(cases) >= minimum, 'PYTEST_COUNT_BELOW_BASELINE')
    require(not any(c.find(tag) is not None for c in cases for tag in ('failure', 'error', 'skipped')),
            'PYTEST_NONPASS_CASE')
    if expected_count is not None:
        require(len(cases) == expected_count, 'PYTEST_XML_COUNT_MISMATCH')
    return len(cases)


def preflight():
    from phase178_r1_k6_source_first_audit import audit as r1
    from phase177_closeout_measurement import gate as previous
    from phase176_closeout.gate import ACTIVE_COMMAND as previous_command, HISTORICAL
    from phase175_r4r14r11_closeout_preflight.audit import KNOWN_LEGACY_FAILURES
    from homotopy_groups import TodaPrimaryGroup
    from stable_rules import is_in_toda_stable_range
    gt = r1.git_text
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(gt('rev-parse', 'HEAD') == gt('rev-parse', 'origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not r1.git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    r1.git('diff', '--check')
    for path, blob in PINS.items():
        require(gt('rev-parse', 'HEAD:' + path) == blob and r1.blob_matches(ROOT/path, blob), 'SOURCE_PIN_CHANGED:' + path)
    require(tuple(previous_command) == ACTIVE_COMMAND, 'ACTIVE_COMMAND_CHANGED')
    require(tuple(KNOWN_LEGACY_FAILURES) == HISTORICAL and len(HISTORICAL) == 4, 'HISTORICAL_SCOPE_CHANGED')
    require(all((ROOT / p.split('::')[0]).is_file() for p in HISTORICAL), 'HISTORICAL_TEST_MISSING')
    require(all((ROOT/p).is_file() for p in FOCUSED), 'FOCUSED_TEST_MISSING')
    tracked = {os.fsdecode(p) for p in r1.git('ls-tree', '-r', '--name-only', '-z', 'HEAD', '--', 'tests').split(b'\0') if p.endswith(b'.py')}
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT/'tests').rglob('*.py') if p.is_file()}
    require(actual == tracked and len(actual) == 242, 'ACTIVE_TEST_INVENTORY_CHANGED')
    pairs = previous.registered_pairs(ROOT/'data/sphere.csv')
    stable_pred = lambda n, k: is_in_toda_stable_range(TodaPrimaryGroup(n+k, n))
    active, stable, future = split_scope(pairs, stable_pred)
    validate_scope(active, stable, future)
    require((8,6) in stable, 'STABLE_BOUNDARY_CHANGED')
    return {'head': HEAD, 'pins': PINS, 'documents': {p: sha256((ROOT/p).read_bytes()).hexdigest() for p in DOCUMENTS},
            'active_test_python_files': len(actual), 'active_command': list(ACTIVE_COMMAND),
            'focused_tests': list(FOCUSED), 'historical_tests': list(HISTORICAL),
            'historical_status': 'FOUR_KNOWN_FAILURES_NOT_RERUN_NOT_PASSING',
            'scope': {'active_unstable': list(map(list, active)), 'stable_excluded_count': len(stable),
                      'future_unstable_excluded_count': len(future), 'csv_registered_count': len(pairs)}}


def measure_group(n, k, folder, timeout):
    if k != 6:
        from phase177_closeout_measurement import gate as previous
        row = previous.worker(n, k, timeout)
        validate_prior(n, k, row)
        return row
    from phase178_r29_final_6stem_audit import audit as r29
    command = [sys.executable, '-B', '-m', r29.PACKAGE + '.audit', '--worker', str(n), '--folder', str(folder)]
    subprocess.run(command, cwd=ROOT, check=True, timeout=timeout)
    audit = json.loads((folder/f'n{n}_audit.json').read_text(encoding='utf-8'))
    r29.validate_summary(n, audit['summary'])
    validate_k6(n, audit)
    return {'n': n, 'k': k, 'status': 'complete', 'open_goal_count': 0, 'open_goals': [],
            'root_step_count': 1, 'conclusion': audit['conclusion'], 'proven_step_count': audit['summary']['proven_step_count'],
            'reference_count': audit['summary']['reference_count'], 'model_citation_count': audit['model_citation_count'],
            'given_count': audit['given_count'], 'inference_count': audit['inference_count'],
            'trust_status': audit['summary']['trust_status'], 'target_given_count': 0, 'web_key': audit['summary']['web_key'],
            'public_audit': audit}


def run_pytest(folder, label, args):
    xml = folder/(label+'.xml')
    stdout = folder/(label+'_stdout.txt')
    stderr = folder/(label+'_stderr.txt')
    command = [sys.executable, *args, '--junitxml='+str(xml)]
    emit(label.upper(), 'STARTED')
    with stdout.open('xb') as out, stderr.open('xb') as err:
        proc = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err)
    output = stdout.read_text(encoding='utf-8', errors='replace')
    print('\n'.join(output.splitlines()[-25:]), flush=True)
    if stderr.stat().st_size:
        print(stderr.read_text(encoding='utf-8', errors='replace')[-4000:], flush=True)
    return {'command': command, 'exit_code': proc.returncode, 'stdout_sha256': sha256(stdout.read_bytes()).hexdigest(),
            'stderr_sha256': sha256(stderr.read_bytes()).hexdigest(), 'xml_sha256': sha256(xml.read_bytes()).hexdigest() if xml.is_file() else None}, xml, output


def run(dry_run, timeout):
    from phase178_r1_k6_source_first_audit import audit as r1
    from phase177_closeout_measurement import gate as previous
    from phase178_r29_final_6stem_audit import audit as r29
    from phase176_closeout.gate import parse_summary
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report_path = folder/'report.json'
    report = {'gate': 'FAIL_PHASE178_CLOSEOUT_MEASUREMENT', 'head': HEAD, 'dry_run': dry_run,
              'phase178_formally_closed': False, 'full_pytest': 'NOT_RUN', 'groups': [],
              'started_utc': datetime.now(timezone.utc).isoformat()}
    try:
        require(timeout > 0, 'INVALID_TIMEOUT')
        context = preflight()
        report['preflight'] = context
        report['scope'] = context['scope']
        before = r1.snapshot()
        emit('HEAD', HEAD)
        for key in ('csv_registered_count', 'stable_excluded_count', 'future_unstable_excluded_count'):
            emit(key.upper(), context['scope'][key])
        emit('ACTIVE_UNSTABLE', len(EXPECTED))
        emit('LEGACY_SOURCE_GUARDS', context['historical_status'])
        if dry_run:
            report['gate'] = 'PASS_PHASE178_CLOSEOUT_DRYRUN'
        else:
            store(report_path, report)
            with (folder/'groups.jsonl').open('x', encoding='utf-8') as stream:
                for n, k in EXPECTED:
                    row = measure_group(n, k, folder, timeout)
                    report['groups'].append(row)
                    stream.write(json.dumps(row, ensure_ascii=False, default=str)+'\n')
                    stream.flush()
                    store(report_path, report)
                    emit('GROUP', f'n={n} k={k} status={row["status"]} open={row["open_goal_count"]} steps={row["proven_step_count"]}')
            report['active_unstable_summary'] = previous.summarize(report['groups'])
            k6 = [row for row in report['groups'] if row['k'] == 6]
            report['k6_groups'] = k6
            report['k6_summary'] = previous.summarize(k6)
            require(report['active_unstable_summary']['complete'] == 21 and report['k6_summary']['complete'] == 6, 'ACTIVE_SCOPE_NOT_COMPLETE')
            totals = {key: sum(row[key] for row in k6) for key in ('proven_step_count', 'given_count', 'inference_count', 'model_citation_count', 'target_given_count', 'open_goal_count')}
            require(totals == {'proven_step_count':83,'given_count':27,'inference_count':56,'model_citation_count':27,'target_given_count':0,'open_goal_count':0}, 'R29_TOTALS_CHANGED')
            report['k6_totals'] = totals
            emit('K6_TOTALS', json.dumps(totals))
            boundary_path = folder/'stable_boundary.json'
            subprocess.run([sys.executable, '-B', '-m', 'phase178_r27_stable_boundary_source_first_audit.audit', '--worker', str(boundary_path)], cwd=ROOT, check=True, timeout=timeout)
            boundary = json.loads(boundary_path.read_text(encoding='utf-8'))
            r29.validate_boundary(boundary)
            report['stable_boundary'] = boundary
            report['stable_boundary_status'] = 'DEFERRED_PHASE179_PARTIAL'
            emit('STABLE_BOUNDARY', report['stable_boundary_status'])
            emit('STABLE_BOUNDARY_OPEN_GOALS', boundary['open_goal_count'])
            require(r1.snapshot() == before, 'WORKTREE_CHANGED_DURING_GROUP_AUDIT')
            store(report_path, report)
            focused, xml, output = run_pytest(folder, 'focused', ('-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*FOCUSED))
            report['focused'] = focused
            focused['passed'] = inspect_junit(xml, focused['exit_code'], 47)
            cases = list(ET.parse(xml).getroot().iter('testcase'))
            legacy = [c for c in cases if c.get('classname','').endswith('test_r4c_pi64_suspension_iso')]
            require(len(legacy) == 6 and 'PHASE178_R30R1_HISTORICAL_REPLAY=VERIFIED' in output
                    and 'PHASE178_R30R1_PRIOR_SOURCES=VERIFIED' in output, 'R4C_NOT_REVERIFIED')
            report['historical_guard'] = 'RESOLVED_6_OF_6_PASS'
            emit('HISTORICAL_GUARD', report['historical_guard'])
            emit('FOCUSED_PASSED', focused['passed'])
            require(r1.snapshot() == before, 'WORKTREE_CHANGED_DURING_FOCUSED_TESTS')
            report['full_pytest'] = 'STARTED'
            store(report_path, report)
            full, xml, output = run_pytest(folder, 'full_pytest', ACTIVE_COMMAND)
            report['full_pytest_evidence'] = full
            report['full_pytest'] = 'FAILED_OR_UNVERIFIED'
            report['full_pytest_exit'] = full['exit_code']
            store(report_path, report)
            count, summary = parse_summary(output, full['exit_code'])
            inspect_junit(xml, full['exit_code'], 3546, expected_count=count)
            report.update(full_pytest='PASS', full_pytest_exit=0, passed=count, summary=summary,
                          stdout_sha256=full['stdout_sha256'], stderr_sha256=full['stderr_sha256'])
            store(report_path, report)
            require(r1.snapshot() == before and preflight() == context, 'WORKTREE_CHANGED_DURING_CLOSEOUT')
            report['repository_unchanged'] = True
            report['gate'] = 'PASS_PHASE178_CLOSEOUT_MEASURED_DOCUMENTS_PENDING'
        require(r1.snapshot() == before, 'REPOSITORY_CHANGED_DURING_MEASUREMENT')
    except BaseException as exc:
        report.update(gate='FAIL_PHASE178_CLOSEOUT_MEASUREMENT', error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    store(report_path, report)
    for key in ('active_unstable_summary', 'k6_summary', 'full_pytest', 'passed', 'summary', 'phase178_formally_closed', 'gate'):
        if key in report:
            emit(key.upper(), report[key])
    emit('REPORT', report_path)
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--timeout', type=int, default=180)
    args = parser.parse_args()
    return run(args.dry_run, args.timeout)


if __name__ == '__main__':
    raise SystemExit(main())
