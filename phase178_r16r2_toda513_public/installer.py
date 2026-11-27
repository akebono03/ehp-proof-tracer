"""Exact-anchor, reviewed-base wiring; no change to mathematical rules."""
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
BASE = '2d48756c9ccc227c8a80a465c99e070b661a8ce2'
TARGET = 'phase165_r52_r9_shared_math.py'
TARGET_BLOB = 'ff667e53c17568d607b81f6362338b33591351db'
PREVIOUS = 'phase178_r16_toda513_isolated/'
SOURCE_ANCHOR = '        sources = sources + (build_cited_512_source(),)\n'
SOURCE_INSERT = """    # Phase 178 R16R2: append the reviewed, positioned Toda (5.13) images.
    if default_sources:
        from phase178_r16_toda513_isolated.source import build_cited_513_source
        sources = sources + (build_cited_513_source(),)
"""
TESTS = (
    PACKAGE + '/tests/test_installer.py',
    PACKAGE + '/tests/test_public.py',
    PREVIOUS + 'tests/test_source_contract.py',
    PREVIOUS + 'tests/test_registration.py',
    'phase178_r15r2_toda512_public/tests/test_public.py',
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
    source = source.replace(SOURCE_ANCHOR, SOURCE_ANCHOR + SOURCE_INSERT, 1)
    ast.parse(source)
    return source


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def gt(*args):
    return git(*args).decode('utf-8').strip()


def emit(key, value):
    print('PHASE178_R16R2_' + key + '=' + str(value), flush=True)


def preflight():
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    head = gt('rev-parse', 'HEAD')
    require(gt('branch', '--show-current') == 'develop' and head == gt('rev-parse', 'origin/develop'), 'BRANCH_OR_HEAD_MISMATCH')
    require(gt('merge-base', BASE, head) == BASE, 'REVIEWED_ANCESTRY_REQUIRED')
    require(not gt('diff', '--cached', '--name-only'), 'STAGED_CHANGES_REFUSED')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    require(gt('rev-parse', BASE + ':' + TARGET) == TARGET_BLOB, 'BASE_BLOB_CHANGED')
    pins = json.loads((Path(__file__).parent / 'reviewed_r16_hashes.json').read_text(encoding='utf-8'))
    changed = set(gt('diff', '--name-only', BASE, head).splitlines())
    require(changed <= set(pins), 'UNREVIEWED_COMMITTED_CHANGE:' + repr(sorted(changed - set(pins))))
    for path, expected in pins.items():
        require((ROOT / path).is_file() and digest((ROOT / path).read_bytes()) == expected, 'R16_PACKAGE_CHANGED:' + path)
        if path in changed:
            require(digest(git('show', head + ':' + path)) == expected, 'R16_COMMITTED_CONTENT_CHANGED:' + path)
    base = normalize(git('show', BASE + ':' + TARGET))
    proposed = proposed_source(base)
    path = ROOT / TARGET
    original = path.read_bytes()
    require(normalize(original) in (base, proposed), 'UNREVIEWED_TARGET_CONTENT')
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
    report = {'gate': 'FAIL_R16R2', 'dry_run': args.dry_run, 'full_pytest': 'NOT_RUN', 'new_math_rules': 0}
    original = None
    installed = False
    path = ROOT / TARGET
    try:
        head, original, proposed, already = preflight()
        report.update(head=head, already_installed=already)
        emit('HEAD', head)
        emit('R16_PACKAGE', 'VERIFIED')
        # Keep the entire proposed module and the full replacement function outside the repository.
        (folder / TARGET).write_text(proposed, encoding='utf-8')
        lines = proposed.splitlines(keepends=True)
        names = {'build_shared_typed_bridge'}
        for node in ast.parse(proposed).body:
            if isinstance(node, ast.FunctionDef) and node.name in names:
                (folder / (node.name + '.py')).write_text(''.join(lines[node.lineno-1:node.end_lineno]), encoding='utf-8')
        emit('REPLACEMENT_FILE', folder / TARGET)
        if args.dry_run:
            report['gate'] = 'PASS_R16R2_READ_ONLY_DRYRUN'
        else:
            if not already:
                installed = True
                write_proposal(path, original, proposed)
            command = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '-p', 'no:cacheprovider', '--import-mode=importlib', *TESTS]
            report['focused_command'] = command
            subprocess.run(command, cwd=ROOT, check=True)
            new_head, _, _, is_proposed = preflight()
            require(new_head == head and is_proposed, 'POST_INSTALL_INTEGRITY_FAILED')
            report['gate'] = 'PASS_R16R2_TODA513_PUBLIC'
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
