"""Append R19 candidates after existing ordering; export full code and audit."""
import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '7390660dc6eda0364d93a29cc255d670c51c4871'
TARGET = 'phase165_r52_r9_shared_math.py'
PREVIOUS = 'phase178_r19_finite_cyclic_suspension_transport_isolated/'
OLD_TEST = PREVIOUS + 'tests/test_provider.py'
PREFIX = 'PHASE178_R19R1_'
PINS = {
    TARGET: '5b23a40f62069c00ae30bee6ed670d66f8a3daf9',
    OLD_TEST: 'f79a3e80bb513b8c55e0bfe7760576a191f42698',
    PREVIOUS + 'provider.py': 'c20a6c2d8466cd30adee8bb92ed61283c6c6fe9d',
    'phase165_r12_r24_web_search_connection.py': '71d0c6c365a46e833a2bfe304c771d2e010178ca',
    'phase165_r57_r11_proof_order_gate.py': '1ad9dfe8bb3da061cbee0dbd7a11c196f3f50604',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase176_r3r48_cited_finite_delta_kernel/rule.py': '86cc4a468ffd4601337bbef589a37fa46b449263',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase178_r18_n6_source_first_audit/audit.py': 'd9577c8d77c73e21e112a37f56942ecc7adbfdfe',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'phase178_r17r3_common_renderer/tests/test_display.py': '934fcdec3976b45e7e9570a780a47adca6837cca',
    'phase169_r3b_finite_cyclic_suspension/tests/test_phase169_r3b_finite_cyclic_suspension.py': 'f1f6c5169107677c94c183aeb4ef49794dc4a174',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
}
LEGACY = 'phase169_r3b_finite_cyclic_suspension/tests/test_phase169_r3b_finite_cyclic_suspension.py'
TESTS = (
    PACKAGE + '/tests', OLD_TEST,
    LEGACY + '::test_expansion_contains_three_unproved_typed_premises',
    LEGACY + '::test_inference_derives_only_from_all_three_verified_premises',
    LEGACY + '::test_wrong_isomorphism_or_generator_image_rejected',
    LEGACY + '::test_missing_or_ambiguous_registered_source_retains_previous_route',
    LEGACY + '::test_other_stems_are_unchanged',
    'phase178_r17r3_common_renderer/tests/test_display.py',
)
BUILD_ANCHOR = '    shared_provider_registry = build_shared_expansion_provider_registry(\n'
BUILD_INSERT = '''    # Phase 178 R19R1: reuse the independently tested finite cyclic transport provider.
    from phase178_r19_finite_cyclic_suspension_transport_isolated.provider import (
        build_finite_cyclic_suspension_transport_provider,
    )
    finite_cyclic_transport = build_finite_cyclic_suspension_transport_provider(
        bridge=bridge, proof_target=proof_target,
    )
'''
RETURN_ANCHOR = '        return retain_ordered_root_expansions(proof_target, goal, merged)\n'
RETURN_INSERT = '''        # Append only new obligations; preserve all existing candidate priorities.
        for option in finite_cyclic_transport(goal):
            if not any(old.rule.name == option.rule.name and old.subgoals == option.subgoals
                       for old in merged):
                merged += (option,)
'''
TEST_EDITS = (
    ('def test_real_n6_candidate_not_publicly_installed():',
     'def test_real_n6_candidate_matches_public_wiring():'),
    ('    assert all(o.rule.name != RULE for o in public)\n',
     '    assert sum(o.rule.name == RULE and o.subgoals == expected for o in public) == 1\n'),
    ("    print('PHASE178_R19_PUBLIC_PROVIDER_UNCHANGED=VERIFIED')",
     "    print('PHASE178_R19R1_PUBLIC_PROVIDER_MATCH=VERIFIED')"),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def replace_once(text, old, new):
    require(text.count(old) == 1, 'MISSING_OR_AMBIGUOUS_ANCHOR:' + old)
    return text.replace(old, new, 1)


def proposed_source(text):
    require(BUILD_INSERT not in text and RETURN_INSERT not in text, 'ALREADY_CONNECTED_SOURCE')
    text = replace_once(text, BUILD_ANCHOR, BUILD_INSERT + BUILD_ANCHOR)
    text = replace_once(text, RETURN_ANCHOR, RETURN_INSERT + RETURN_ANCHOR)
    ast.parse(text)
    return text


def proposed_test(text):
    for old, new in TEST_EDITS:
        text = replace_once(text, old, new)
    ast.parse(text)
    return text


def normalized(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def encode_like(text, raw):
    rest = raw.replace(b'\r\n', b'')
    require(b'\r' not in rest and not (b'\r\n' in raw and b'\n' in rest), 'MIXED_EOL')
    return text.replace('\n', '\r\n' if b'\r\n' in raw else '\n').encode(
        'utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8')


def preflight(r1):
    gt = r1.git_text
    require(Path(os.fsdecode(r1.git('rev-parse', '--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    head = gt('rev-parse', 'HEAD')
    require(head == gt('rev-parse', 'origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not gt('diff', '--cached', '--name-only'), 'STAGED_CHANGES_PRESENT')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    changes = {}
    writers = {TARGET: proposed_source, OLD_TEST: proposed_test}
    require(set(gt('diff', '--name-only', 'HEAD').splitlines()) <= set(writers), 'UNRELATED_TRACKED_CHANGES')
    for path, pin in PINS.items():
        require(gt('rev-parse', 'HEAD:' + path) == pin, 'PIN_CHANGED:' + path)
        file = ROOT / path
        if path not in writers:
            require(r1.blob_matches(file, pin), 'WORKTREE_PIN_CHANGED:' + path)
            continue
        base = normalized(r1.git('show', HEAD + ':' + path))
        updated = writers[path](base)
        raw = file.read_bytes()
        require(normalized(raw) in (base, updated), 'UNREVIEWED_WORKTREE:' + path)
        changes[path] = (raw, encode_like(updated, raw), updated)
    for node in TESTS:
        require((ROOT / node.split('::', 1)[0]).exists(), 'TEST_MISSING:' + node)
    r1.git('diff', '--check')
    return head, changes


def export_code(folder, changes):
    for path, (raw, updated, text) in changes.items():
        name = path.replace('/', '__')
        (folder / (name + '.full.txt')).write_text(text, encoding='utf-8')
        (folder / (name + '.before')).write_bytes(raw)
        if path == TARGET:
            lines = text.splitlines(keepends=True)
            func, = [n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef)
                     and n.name == 'shared_expansion_provider']
            (folder / 'shared_expansion_provider.full.py.txt').write_text(
                ''.join(lines[func.lineno-1:func.end_lineno]), encoding='utf-8')


def audit_public(r1, folder, report):
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase178_r19_finite_cyclic_suspension_transport_isolated.provider import suspension_transport_inputs
    from phase178_r18_n6_source_first_audit.audit import summarize
    rows = []
    report['groups'] = rows
    # These four targets were complete before this wiring change.
    for n in (2, 3, 4, 5, 6):
        summary = r1.worker(n, 6, folder, 180)
        rows.append(summary)
        require('detail' in summary, 'WORKER_FAILED:' + repr(summary))
        require(summary['web_error'] is None and summary['complete_invariants_hold']
                and summary['target_given_count'] == 0, 'PUBLIC_TRUST_FAILURE:' + repr(summary))
        detail = json.loads(Path(summary['detail']).read_text(encoding='utf-8'))
        emit('GROUP', json.dumps({k: summary[k] for k in ('n','k','status','proven_step_count','open_goal_count','trust_status','target_given_count','web_key')}, ensure_ascii=False))
        if n < 6:
            require(summary['status'] == 'complete' and summary['trust_status'] == 'VERIFIED'
                    and summary['open_goal_count'] == 0 and summary['web_key'] == 'generic-complete-proof',
                    'COMPLETED_GROUP_REGRESSION:' + str(n))
            continue
        report['n6_analysis'] = summarize(summary, detail)
        root, lower = exact_prior_database_result(6,6), exact_prior_database_result(5,6)
        required = suspension_transport_inputs(root, lower)
        require(required is not None, 'R19_OBLIGATION_MISSING')
        calls = detail['provider_calls']
        root_calls = [c for c in calls if c['goal'] == r1.statement(root)]
        expected = [r1.statement(g) for g in required]
        require(any(o['rule'] == 'finite cyclic presentation transported by proved suspension isomorphism'
                    and o['subgoals'] == expected for c in root_calls for o in c['options']),
                'TRANSPORT_NOT_IN_ACTUAL_SEARCH')
        iso_calls = [c for c in calls if c['goal'] == r1.statement(required[1])]
        require(bool(iso_calls), 'SUSPENSION_ISOMORPHISM_NOT_REACHED')
        report['iso_calls'] = iso_calls
        emit('N6_TRANSPORT_REACHED', 'VERIFIED')
        emit('N6_ISOMORPHISM_VISITS', len(iso_calls))
        emit('N6_ISOMORPHISM_CANDIDATE_COUNTS', [len(c['options']) for c in iso_calls])
        for item in report['n6_analysis']['frontier']:
            emit('FRONTIER', json.dumps(item, ensure_ascii=False))
        for line in detail['web']['rendered_lines']:
            print(line)
    emit('COMPLETED_K6_REGRESSION', '4/4_VERIFIED')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    from phase178_r1_k6_source_first_audit import audit as r1
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate':'FAIL_R19R1','dry_run':args.dry_run,'new_math_rules':0,'new_given':0,'full_pytest':'NOT_RUN'}
    written = []
    try:
        head, changes = preflight(r1)
        report['head'] = head
        emit('HEAD', head)
        export_code(folder, changes)
        emit('FULL_CODE', folder)
        if args.dry_run:
            report['gate'] = 'PASS_R19R1_DRYRUN'
        else:
            for path,(raw,updated,text) in changes.items():
                require((ROOT/path).read_bytes() == raw, 'WORKTREE_CHANGED:' + path)
            for path,(raw,updated,text) in changes.items():
                if raw != updated:
                    written.append((path,raw,updated))
                    (ROOT/path).write_bytes(updated)
            command = [sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command'] = command
            subprocess.run(command,cwd=ROOT,check=True)
            before = r1.snapshot()
            audit_public(r1,folder,report)
            require(r1.snapshot() == before, 'REPOSITORY_CHANGED_DURING_AUDIT')
            _, after = preflight(r1)
            require(all(raw == updated for raw,updated,text in after.values()), 'POST_INSTALL_INTEGRITY_FAILED')
            report['gate'] = 'PASS_R19R1_FINITE_CYCLIC_TRANSPORT_PUBLIC'
    except Exception as exc:
        for path,raw,updated in reversed(written):
            if (ROOT/path).read_bytes() == updated:
                (ROOT/path).write_bytes(raw)
        report.update(error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    emit('REPORT',folder/'report.json')
    emit('NEW_MATH_RULES',0)
    emit('NEW_GIVEN',0)
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
