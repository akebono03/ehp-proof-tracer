"""Prefer the existing screened (5.12) candidate; audit the actual proof."""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
import argparse

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).parent.name
BASE = 'bbb603e2829d3b12c0428efb95d25108bb8c2d8c'
TARGET = 'phase165_r52_r9_shared_math.py'
TARGET_BLOB = '78f7cbb9e3b00231457014f31ed400ef884f063f'
PREVIOUS = 'phase178_r17r1_finite_cyclic_quotient_public/'
PREVIOUS_ANCHOR = '    extra_providers = tuple(extra_providers) + (build_cited_512_provider(bridge),)\n'
PREVIOUS_INSERT = """    # Phase 178 R17R1: expose the unchanged finite cyclic quotient rule.
    from phase178_r17r1_finite_cyclic_quotient_public.provider import build_public_finite_cyclic_quotient_provider
    extra_providers = tuple(extra_providers) + (
        build_public_finite_cyclic_quotient_provider(bridge=bridge, proof_target=proof_target),
    )
"""
SOURCE_ANCHOR = '        return retain_ordered_root_expansions(proof_target, goal, merged)\n'
SOURCE_INSERT = """        # Phase 178 R17R2: prefer already screened direct citation readings.
        from phase178_r15_toda512_isolated.provider import RULE_NAME as cited_512_rule_name
        preferred = tuple(o for o in merged if o.rule.name == cited_512_rule_name)
        if preferred:
            merged = preferred + tuple(o for o in merged if o.rule.name != cited_512_rule_name)
"""
TESTS = (
    PACKAGE + '/tests/test_installer.py', PACKAGE + '/tests/test_priority.py',
    PREVIOUS + 'tests/test_public.py',
    'phase178_r15r2_toda512_public/tests/test_public.py',
    'phase178_r16r2_toda513_public/tests/test_public.py',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def normalize(data):
    return data.decode('utf-8-sig').replace('\r\n', '\n')


def digest(data):
    return hashlib.sha256(normalize(data).encode('utf-8')).hexdigest()


def proposed_source(source):
    require(source.count(SOURCE_ANCHOR) == 1, 'MISSING_OR_AMBIGUOUS_ANCHOR')
    require(SOURCE_INSERT not in source, 'ALREADY_CONNECTED_SOURCE')
    source = source.replace(SOURCE_ANCHOR, SOURCE_INSERT + SOURCE_ANCHOR, 1)
    ast.parse(source)
    return source


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def gt(*args):
    return git(*args).decode('utf-8').strip()


def emit(key, value):
    print('PHASE178_R17R2_' + key + '=' + str(value), flush=True)


def preflight():
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    head = gt('rev-parse', 'HEAD')
    require(gt('branch', '--show-current') == 'develop' and head == gt('rev-parse', 'origin/develop'), 'BRANCH_OR_HEAD_MISMATCH')
    require(gt('merge-base', BASE, head) == BASE, 'REVIEWED_ANCESTRY_REQUIRED')
    require(not gt('diff', '--cached', '--name-only'), 'STAGED_CHANGES_REFUSED')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    require(gt('rev-parse', BASE + ':' + TARGET) == TARGET_BLOB, 'BASE_BLOB_CHANGED')
    pins = json.loads((Path(__file__).parent / 'reviewed_r17r1_hashes.json').read_text(encoding='utf-8'))
    changed = set(gt('diff', '--name-only', BASE, head).splitlines())
    require(changed <= set(pins) | {TARGET}, 'UNREVIEWED_COMMITTED_CHANGE:' + repr(sorted(changed - set(pins) - {TARGET})))
    for path, expected in pins.items():
        require((ROOT / path).is_file() and digest((ROOT / path).read_bytes()) == expected, 'R17R1_PACKAGE_CHANGED:' + path)
        if path in changed:
            require(digest(git('show', head + ':' + path)) == expected, 'R17R1_COMMITTED_CONTENT_CHANGED:' + path)
    base = normalize(git('show', BASE + ':' + TARGET))
    require(base.count(PREVIOUS_ANCHOR) == 1, 'R17R1_ANCHOR_CHANGED')
    connected = base.replace(PREVIOUS_ANCHOR, PREVIOUS_ANCHOR + PREVIOUS_INSERT, 1)
    proposed = proposed_source(connected)
    require(normalize(git('show', head + ':' + TARGET)) in (base, connected), 'UNREVIEWED_COMMITTED_TARGET')
    path = ROOT / TARGET
    original = path.read_bytes()
    require(normalize(original) in (connected, proposed), 'UNREVIEWED_TARGET_CONTENT')
    dirty = set(gt('diff', '--name-only', 'HEAD').splitlines())
    require(dirty <= {TARGET}, 'UNRELATED_TRACKED_CHANGE:' + repr(sorted(dirty - {TARGET})))
    require(all((ROOT / t).is_file() for t in TESTS), 'FOCUSED_TEST_MISSING')
    gt('diff', '--check')
    return head, original, proposed, normalize(original) == proposed


def write_proposal(path, original, proposed):
    newline = '\r\n' if b'\r\n' in original else '\n'
    encoding = 'utf-8-sig' if original.startswith(b'\xef\xbb\xbf') else 'utf-8'
    path.write_bytes(proposed.replace('\n', newline).encode(encoding))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    folder_base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder_base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=folder_base))
    report = {'gate': 'FAIL_R17R2', 'dry_run': args.dry_run, 'full_pytest': 'NOT_RUN', 'new_math_rules': 0}
    original = None
    installed = False
    path = ROOT / TARGET
    try:
        head, original, proposed, already = preflight()
        report.update(head=head, already_installed=already)
        emit('HEAD', head)
        emit('R17R1_PACKAGE', 'VERIFIED')
        # Keep the entire proposed module and the full replacement function outside the repository.
        (folder / TARGET).write_text(proposed, encoding='utf-8')
        lines = proposed.splitlines(keepends=True)
        names = {'shared_expansion_provider'}
        for node in ast.parse(proposed).body:
            if isinstance(node, ast.FunctionDef) and node.name in names:
                (folder / (node.name + '.py')).write_text(''.join(lines[node.lineno-1:node.end_lineno]), encoding='utf-8')
        emit('REPLACEMENT_FILE', folder / TARGET)
        if args.dry_run:
            report['gate'] = 'PASS_R17R2_READ_ONLY_DRYRUN'
        else:
            if not already:
                installed = True
                write_proposal(path, original, proposed)
            command = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '-p', 'no:cacheprovider', '--import-mode=importlib', *TESTS]
            report['focused_command'] = command
            subprocess.run(command, cwd=ROOT, check=True)
            new_head, _, _, is_proposed = preflight()
            require(new_head == head and is_proposed, 'POST_INSTALL_INTEGRITY_FAILED')
            command = [sys.executable, '-B', '-m', PACKAGE + '.audit', '--folder', str(folder)]
            subprocess.run(command, cwd=ROOT, check=True, timeout=180)
            report['proof_audit'] = json.loads((folder / 'proof_audit.json').read_text(encoding='utf-8'))
            report['gate'] = 'PASS_R17R2_CITED_512_PRIORITY'
    except Exception as exc:
        if installed and original is not None:
            path.write_bytes(original)
            report['rolled_back'] = True
        report.update(error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    emit('REPORT', folder / 'report.json')
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
