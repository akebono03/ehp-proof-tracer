"""R57R3: repair one outdated proof-matcher test and R57's reproducibility pin.

R57 switched Delta surjectivity to one required group-structure premise.
Unrelated available proof facts must not become a required premise or block
that inference. This package changes no mathematical rule or renderer.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
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

BEFORE_TEST_SHA = '8dbc5a52f3c4c57ca2b3f5cc8750112fb86cc4ca4fa9a521fbbb74aa29e48fab'
AFTER_TEST_SHA = 'b13d03c5877d9b24d40a6c2e11d65120465f699b89f9719cde68586522c7b719'
BEFORE_INSTALL_SHA = '5cea9f784ba727d177fcbfdf07c5a10329825d2a33cbac8eb37a7d1c726af11b'
AFTER_INSTALL_SHA = '637e073aea7afb2232c219e200df83561651ae59720139c6ebb8d5833d2de00b'
TEST_FUNCTION = 'test_missing_or_wrong_group_generator_blocks_surjectivity'

TEST_REPLACEMENT = '''def test_missing_or_wrong_group_generator_blocks_surjectivity() -> None:
    theorem = typed_specialization(6)
    goal = MapSurjective(theorem.delta)
    relation, = delta_surjectivity_generator_inputs(goal)
    wrong = Relation(relation.lhs, FreeCyclicGroup(
        replace(relation.rhs.generator, name="Delta of wrong identity")
    ))
    rule = delta_surjectivity_from_generator_rule(goal)
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(rule, (_test_step(wrong),)) == ()
    assert find_inference_matches_for_rule(rule, (_test_step(theorem),)) == ()
    valid_relation = _test_step(relation)
    unrelated_theorem = _test_step(theorem)
    matches = find_inference_matches_for_rule(
        rule, (valid_relation, unrelated_theorem)
    )
    assert len(matches) == 1
    assert matches[0].premises == (valid_relation,)
    derived = apply_inference_match(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == (valid_relation,)
'''


def sha256_text(source: str) -> str:
    return hashlib.sha256(source.encode('utf-8')).hexdigest()


def _normalize(data: bytes) -> tuple[str, bytes, str]:
    bom = b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b''
    payload = data[len(bom):]
    if b'\r' in payload.replace(b'\r\n', b''):
        raise RuntimeError('CR-only line endings are not reviewed')
    if b'\r\n' in payload and b'\n' in payload.replace(b'\r\n', b''):
        raise RuntimeError('mixed EOL is not reviewed')
    return payload.decode('utf-8').replace('\r\n', '\n'), bom, ('\r\n' if b'\r\n' in payload else '\n')


def _read(path: Path) -> tuple[bytes, str, bytes, str]:
    raw = path.read_bytes()
    content, bom, eol = _normalize(raw)
    return raw, content, bom, eol


def _one(source: str, before: str, after: str, label: str) -> str:
    if source.count(before) != 1:
        raise RuntimeError('unreviewed or ambiguous R57R3 anchor ' + label)
    return source.replace(before, after, 1)


def _replace_function(source: str, name: str, replacement: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1 or matches[0].decorator_list:
        raise RuntimeError('unreviewed test function or decorators: ' + name)
    node = matches[0]
    lines = source.splitlines(keepends=True)
    return ''.join(lines[:node.lineno - 1]) + replacement.rstrip() + '\n\n' + ''.join(lines[node.end_lineno:]).lstrip('\n')


def corrected_test(source: str) -> str:
    after = _replace_function(source, TEST_FUNCTION, TEST_REPLACEMENT)
    if sha256_text(after) != AFTER_TEST_SHA:
        raise RuntimeError('R57R3 corrected test does not match reviewed SHA-256')
    return after


def corrected_installer(source: str) -> str:
    start = "NEW_TEST3='''def " + TEST_FUNCTION
    marker = "'''\n\ndef patch_rule"
    if source.count(start) != 1:
        raise RuntimeError('R57 installer NEW_TEST3 anchor missing or ambiguous')
    first = source.index(start)
    last = source.find(marker, first)
    if last < 0:
        raise RuntimeError('R57 installer test template end missing')
    old_literal = source[first:last + 3]
    new_literal = "NEW_TEST3='''" + TEST_REPLACEMENT.rstrip() + "\n'''"
    after = _one(source, old_literal, new_literal, 'NEW_TEST3')
    old_pin = "    '" + TEST_NAME + "': '" + BEFORE_TEST_SHA + "',"
    new_pin = "    '" + TEST_NAME + "': '" + AFTER_TEST_SHA + "',"
    after = _one(after, old_pin, new_pin, 'AFTER_SHA256 R56 test')
    ast.parse(after, filename=INSTALL_NAME)
    if sha256_text(after) != AFTER_INSTALL_SHA:
        raise RuntimeError('R57R3 corrected installer does not match reviewed SHA-256')
    return after


def _git(*args: str) -> tuple[int, str]:
    result = subprocess.run(('git',) + args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode, result.stdout.decode('utf-8', 'replace').strip()


def _check_repo() -> None:
    code, branch = _git('branch', '--show-current')
    if code or branch != 'develop':
        raise RuntimeError('develop branch required')
    code, top = _git('rev-parse', '--show-toplevel')
    if code or Path(top).resolve() != ROOT.resolve():
        raise RuntimeError('extract R57R3 directly into the repository root')
    code, staged = _git('diff', '--cached', '--name-only')
    if code or staged:
        raise RuntimeError('staged files require independent review')
    code, _ = _git('merge-base', '--is-ancestor', REVIEWED_BASE, 'HEAD')
    if code:
        raise RuntimeError('HEAD is not a descendant of reviewed R56 base')


def _check_r57_review(source: str) -> None:
    """Use the R57 verified blob and local-patch guards, without writing."""
    namespace = {'__name__': '_r57r3_guard_review', '__file__': str(TARGET_INSTALL)}
    exec(compile(source, str(TARGET_INSTALL), 'exec'), namespace)
    states = namespace['review'](True)
    if not states or any(before != after for before, after, _ in states.values()):
        raise RuntimeError('R57 reviewed patches are missing or partially applied')


def _check_regeneration(source: str, expected: str) -> None:
    original = (PACKAGE / 'fixtures' / 'R56_TEST_ORIGINAL.py.txt').read_text(encoding='utf-8')
    namespace = {'__name__': '_r57r3_generation_review', '__file__': str(TARGET_INSTALL)}
    exec(compile(source, str(TARGET_INSTALL), 'exec'), namespace)
    if namespace['patch_test'](original) != expected:
        raise RuntimeError('R57 corrected installer cannot reproduce the reviewed test')
    if namespace['AFTER_SHA256'][namespace['R56_TEST']] != AFTER_TEST_SHA:
        raise RuntimeError('R57 corrected installer has a mismatched test hash')


def review() -> tuple[tuple[Path, bytes, bytes], ...]:
    _check_repo()
    if not TARGET_TEST.is_file() or not TARGET_INSTALL.is_file():
        raise RuntimeError('R56 test and R57 installer are required')
    raw_test, test_source, test_bom, test_eol = _read(TARGET_TEST)
    raw_inst, install_source, install_bom, install_eol = _read(TARGET_INSTALL)
    observed = (sha256_text(test_source), sha256_text(install_source))
    if observed == (BEFORE_TEST_SHA, BEFORE_INSTALL_SHA):
        _check_r57_review(install_source)
        revised_test = corrected_test(test_source)
        revised_installer = corrected_installer(install_source)
    elif observed == (AFTER_TEST_SHA, AFTER_INSTALL_SHA):
        revised_test, revised_installer = test_source, install_source
        _check_r57_review(install_source)
    else:
        raise RuntimeError('unreviewed or partially patched R57R3 source: ' + repr(observed))
    _check_regeneration(revised_installer, revised_test)
    return (
        (TARGET_TEST, raw_test, test_bom + revised_test.replace('\n', test_eol).encode('utf-8')),
        (TARGET_INSTALL, raw_inst, install_bom + revised_installer.replace('\n', install_eol).encode('utf-8')),
    )


def _atomic_write(path: Path, before: bytes, after: bytes) -> None:
    if before == after:
        return
    fd, temp = tempfile.mkstemp(prefix='.r57r3_', suffix='.tmp', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(after)
        if path.read_bytes() != before:
            raise RuntimeError('R57R3 target modified during install: ' + str(path))
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def run(dry_run: bool) -> None:
    changes = review()
    print('PHASE174_R57R3_SOURCE_GUARD=PASS')
    print('PHASE174_R57R3_NEW_GIVEN=0')
    print('PHASE174_R57R3_NEW_MATH_RULES=0')
    print('PHASE174_R57R3_CHANGED_TARGETS=2')
    if dry_run:
        print('PHASE174_R57R3_GATE=PASS_PREFLIGHT_ONLY')
        print('(END)')
        return
    for path, before, after in changes:
        _atomic_write(path, before, after)
    if any(path.read_bytes() != after for path, _, after in changes):
        raise RuntimeError('R57R3 final target bytes do not match the review')
    review()
    print('PHASE174_R57R3_GATE=PASS_R57R3_TEST_CONTRACT_AND_INSTALLER_PIN')
    print('(END)')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    opts = parser.parse_args()
    run(opts.dry_run)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
