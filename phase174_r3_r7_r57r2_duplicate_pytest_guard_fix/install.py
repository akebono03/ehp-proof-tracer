"""Fix R57's accidentally duplicated pytest parametrization, preserving its guards.

Only the R56 test and R57's reviewed test-patch text + SHA are changed.
The established R57 proof rules and shared narrative implementation remain untouched.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TEST_NAME = 'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py'
INSTALL_NAME = 'phase174_r3_r7_r57_narrative_source_cleanup/install.py'
TARGET_TEST = ROOT / TEST_NAME
TARGET_INSTALL = ROOT / INSTALL_NAME
REVIEWED_BASE = '0a5be29a4458cdffaa8a7ad4ad31c2e91f6941f9'

BEFORE_TEST_SHA = '05133a242e6dfdf28c3c6a813634299a8b77b01ab1ae9f1bf702e90a553c44d1'
AFTER_TEST_SHA = '8dbc5a52f3c4c57ca2b3f5cc8750112fb86cc4ca4fa9a521fbbb74aa29e48fab'
BEFORE_INSTALL_SHA = '6a4df3c77edd7a0abd902d28782d12a63ebb6bd69f8c7d03e8efff601cd1e32e'
AFTER_INSTALL_SHA = '5cea9f784ba727d177fcbfdf07c5a10329825d2a33cbac8eb37a7d1c726af11b'

DOUBLE_PARAM = """@pytest.mark.parametrize("n", (4, 6, 8, 10))
@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_generator_relation_alone_proves_delta_surjectivity"""
SINGLE_PARAM = """@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_generator_relation_alone_proves_delta_surjectivity"""

OLD_INSTALL_SHA_ROW = "    'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py': '" + BEFORE_TEST_SHA + "',"
NEW_INSTALL_SHA_ROW = "    'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py': '" + AFTER_TEST_SHA + "',"
OLD_INSTALL_TEST_TEXT = """NEW_TEST1=\'\'\'@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_generator_relation_alone_proves_delta_surjectivity"""
NEW_INSTALL_TEST_TEXT = """NEW_TEST1=\'\'\'def test_generator_relation_alone_proves_delta_surjectivity"""


def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def normalize(data: bytes) -> tuple[str, bytes, str]:
    """Preserve UTF-8 BOM and CRLF/LF while rejecting mixed or CR-only EOL."""
    bom = b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b''
    payload = data[len(bom):]
    if b'\r' in payload.replace(b'\r\n', b''):
        raise RuntimeError('unexpected CR-only line ending')
    if b'\r\n' in payload and b'\n' in payload.replace(b'\r\n', b''):
        raise RuntimeError('mixed LF/CRLF line endings')
    return payload.decode('utf-8').replace('\r\n', '\n'), bom, ('\r\n' if b'\r\n' in payload else '\n')


def replace_exactly_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise RuntimeError('unreviewed or ambiguous R57R2 anchor: ' + label + ' count=' + str(count))
    return source.replace(old, new, 1)


def corrected_test(source: str) -> str:
    """Remove the redundant marker without changing the complete test function."""
    revised = replace_exactly_once(source, DOUBLE_PARAM, SINGLE_PARAM, 'duplicate n parametrization')
    tree = ast.parse(revised, filename=TEST_NAME)
    named = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == 'test_generator_relation_alone_proves_delta_surjectivity']
    if len(named) != 1 or len(named[0].decorator_list) != 1:
        raise RuntimeError('surjectivity test must have exactly one parametrization')
    if sha256_text(revised) != AFTER_TEST_SHA:
        raise RuntimeError('revised test SHA-256 differs from reviewed result')
    return revised


def corrected_installer(source: str) -> str:
    """Update both the patch template and its expected output hash."""
    after = replace_exactly_once(source, OLD_INSTALL_SHA_ROW, NEW_INSTALL_SHA_ROW,
                                 'R57 test hash pin')
    after = replace_exactly_once(after, OLD_INSTALL_TEST_TEXT, NEW_INSTALL_TEST_TEXT,
                                 'R57 test replacement template')
    ast.parse(after, filename=INSTALL_NAME)
    if sha256_text(after) != AFTER_INSTALL_SHA:
        raise RuntimeError('revised installer SHA-256 differs from reviewed result')
    return after


def _read_target(path: Path) -> tuple[bytes, str, bytes, str]:
    raw = path.read_bytes()
    content, bom, eol = normalize(raw)
    return raw, content, bom, eol


def _git(*args: str) -> tuple[int, str]:
    result = subprocess.run(('git',) + args, cwd=ROOT, capture_output=True)
    return result.returncode, result.stdout.decode('utf-8', errors='replace').strip()


def _check_repo() -> None:
    status, branch = _git('branch', '--show-current')
    if status != 0 or branch != 'develop':
        raise RuntimeError('develop branch required')
    status, git_root = _git('rev-parse', '--show-toplevel')
    if status or Path(git_root).resolve() != ROOT.resolve():
        raise RuntimeError('extract directly into the repository root')
    status, staged = _git('diff', '--cached', '--name-only')
    if status or staged:
        raise RuntimeError('staged changes need separate review')
    status, _ = _git('merge-base', '--is-ancestor', REVIEWED_BASE, 'HEAD')
    if status != 0:
        raise RuntimeError('HEAD is not a descendant of the reviewed R56 base')


def _check_r57_review(installer_source: str) -> None:
    """Execute R57's existing strict review without running its installer.

    This still checks its three committed Git blob pins, local R56 rule/test,
    branch and staged files. No mathematical source gate is bypassed.
    """
    namespace = {'__name__': '_r57r2_readonly_review', '__file__': str(TARGET_INSTALL)}
    exec(compile(installer_source, str(TARGET_INSTALL), 'exec'), namespace)
    states = namespace['review'](True)
    if not states or any(before != after for before, after, _ in states.values()):
        raise RuntimeError('R57 did not finish installing its reviewed patch')


def review() -> tuple[tuple[Path, bytes, bytes], ...]:
    _check_repo()
    if not TARGET_TEST.is_file() or not TARGET_INSTALL.is_file():
        raise RuntimeError('R56 test and R57 installer are required')
    raw_test, test_source, test_bom, test_eol = _read_target(TARGET_TEST)
    raw_inst, installer_source, inst_bom, inst_eol = _read_target(TARGET_INSTALL)
    test_sha, inst_sha = sha256_text(test_source), sha256_text(installer_source)
    if (test_sha, inst_sha) == (BEFORE_TEST_SHA, BEFORE_INSTALL_SHA):
        # Validate the already installed R57 before making any additional edits.
        _check_r57_review(installer_source)
        revised_test = corrected_test(test_source)
        revised_inst = corrected_installer(installer_source)
        # The corrected R57 installer must now generate the identical revised
        # test from the reviewed original R56 test, with one marker only.
        original_test = (PACKAGE / 'fixtures' / 'R56_TEST_ORIGINAL.py.txt').read_text(encoding='utf-8')
        checked = {'__name__': '_r57r2_corrected_review', '__file__': str(TARGET_INSTALL)}
        exec(compile(revised_inst, str(TARGET_INSTALL), 'exec'), checked)
        if checked['patch_test'](original_test) != revised_test:
            raise RuntimeError('corrected R57 installer is not reproducible')
    elif (test_sha, inst_sha) == (AFTER_TEST_SHA, AFTER_INSTALL_SHA):
        revised_test, revised_inst = test_source, installer_source
        _check_r57_review(installer_source)
    else:
        raise RuntimeError('unreviewed or partially patched R57R2 sources: test=' + test_sha + ' installer=' + inst_sha)
    return (
        (TARGET_TEST, raw_test, test_bom + revised_test.replace('\n', test_eol).encode('utf-8')),
        (TARGET_INSTALL, raw_inst, inst_bom + revised_inst.replace('\n', inst_eol).encode('utf-8')),
    )


def _atomic_replace(path: Path, before: bytes, after: bytes) -> None:
    if before == after:
        return
    fd, temp = tempfile.mkstemp(prefix='.r57r2_', suffix='.tmp', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as file:
            file.write(after)
        if path.read_bytes() != before:
            raise RuntimeError('file modified during R57R2 install: ' + str(path))
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def run(dry_run: bool) -> None:
    changes = review()
    print('PHASE174_R57R2_SOURCE_GUARD=PASS')
    print('PHASE174_R57R2_DUPLICATE_PARAMETRIZATION_IDENTIFIED=True')
    print('PHASE174_R57R2_NEW_GIVEN=0')
    print('PHASE174_R57R2_NEW_MATH_RULES=0')
    print('PHASE174_R57R2_CHANGED_TARGETS=2')
    if dry_run:
        print('PHASE174_R57R2_GATE=PASS_PREFLIGHT_ONLY')
        print('(END)')
        return
    for path, before, after in changes:
        _atomic_replace(path, before, after)
    for path, _, after in changes:
        if path.read_bytes() != after:
            raise RuntimeError('failed to apply reviewed correction: ' + str(path))
    review()
    print('PHASE174_R57R2_GATE=PASS_R57R2_TEST_DECORATOR_AND_HASH_CORRECTED')
    print('(END)')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    run(args.dry_run)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
