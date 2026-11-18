# Phase 175 R4R12R5R2 — 置換・実行コード全文

## installer.py（全文）

```python
"""Narrow, fail-closed R4R3 rank-two endpoint adaptation.

The original production file must match its reviewed Git blob exactly, except
for LF/CRLF conversion, or match this patch's own output for repeatability.
"""
from __future__ import annotations

import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess
import tempfile

TARGET = Path('phase175_r4r3_two_summand_quotient/rule.py')
BASE_BLOB = '0fdb4c5efa1f2e66470a0735f58f781aafe18d44'
EXPECTED_HEAD = '9203e1a8c077320a58214bda40d9bfeb17704f58'
ORIGINAL_IMPORT = 'from phase169_r10e5_composite_generator_image.rule import _endpoints\n'
NEW_IMPORT = 'from expression import Composition, HomotopyElement, IteratedSuspension\n' + ORIGINAL_IMPORT
ORIGINAL_CHECK = '''    if (_endpoints(first) != (middle.group_dimension, middle.sphere_dimension)
            or _endpoints(second) != (middle.group_dimension, middle.sphere_dimension)
            or _endpoints(delta_image.source_generator)
            != (source.group_dimension, source.sphere_dimension)
            or _endpoints(goal.generator)
            != (target.group_dimension, target.sphere_dimension)):
'''
NEW_CHECK = ORIGINAL_CHECK.replace('_endpoints(', '_rank_two_endpoints(')
HELPER = '''def _rank_two_endpoints(element: object) -> tuple[int, int] | None:
    """Typed endpoints for rank-two generators, including iterated suspension.

    The inner map must itself have valid endpoints. A suspension exponent must
    be a nonnegative exact int, not a bool, symbolic value or negative integer.
    Names alone never certify an expression's endpoints.
    """
    if isinstance(element, IteratedSuspension):
        exponent = element.exponent
        if type(exponent) is not int or exponent < 0:
            return None
        inner = _rank_two_endpoints(element.expression)
        if inner is None:
            return None
        return inner[0] + exponent, inner[1] + exponent
    if isinstance(element, Composition):
        left = _rank_two_endpoints(element.left)
        right = _rank_two_endpoints(element.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    return _endpoints(element)


'''


def git(root: Path, *args: str) -> str:
    p = subprocess.run(['git', *args], cwd=root, text=True, capture_output=True,
                       encoding='utf-8', errors='replace', check=False)
    if p.returncode:
        raise RuntimeError('R4R12R5_GIT_ERROR: ' + ' '.join(args) + ': ' + p.stderr.strip())
    return p.stdout.strip()


def blob(data: bytes) -> str:
    return sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def render(original: str) -> tuple[str, str, str]:
    """Return whole module and full modified helper / function for inspection."""
    ast.parse(original)
    normalized = original.replace('\r\n', '\n')
    if blob(normalized.encode('utf-8')) != BASE_BLOB:
        # Idempotent re-entry is verified by exactly undoing this patch.
        reverted = normalized.replace(HELPER, '', 1).replace(NEW_CHECK, ORIGINAL_CHECK, 1).replace(NEW_IMPORT, ORIGINAL_IMPORT, 1)
        if (normalized.count(HELPER) != 1 or normalized.count(NEW_CHECK) != 1
                or normalized.count(NEW_IMPORT) != 1 or blob(reverted.encode('utf-8')) != BASE_BLOB):
            raise RuntimeError('R4R12R5_UNREVIEWED_SOURCE')
        new = normalized
    else:
        if (normalized.count(ORIGINAL_IMPORT) != 1 or normalized.count(ORIGINAL_CHECK) != 1
                or normalized.count('def two_summand_quotient_inputs(') != 1):
            raise RuntimeError('R4R12R5_ANCHOR_MISMATCH')
        new = normalized.replace(ORIGINAL_IMPORT, NEW_IMPORT, 1)
        new = new.replace('def two_summand_quotient_inputs(', HELPER + 'def two_summand_quotient_inputs(', 1)
        new = new.replace(ORIGINAL_CHECK, NEW_CHECK, 1)
    tree = ast.parse(new)
    full = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ('_rank_two_endpoints', 'two_summand_quotient_inputs'):
            lines = new.splitlines(keepends=True)
            full.append(''.join(lines[node.lineno-1:node.end_lineno]))
    if len(full) != 2:
        raise RuntimeError('R4R12R5_FUNCTION_EXPORT_MISSING')
    return new, full[0], full[1]


def plan(root: Path):
    if git(root, 'branch', '--show-current') != 'develop':
        raise RuntimeError('R4R12R5_WRONG_BRANCH')
    if git(root, 'rev-parse', 'HEAD') != EXPECTED_HEAD:
        raise RuntimeError('R4R12R5_UNREVIEWED_HEAD: ' + git(root, 'rev-parse', 'HEAD'))
    if git(root, 'rev-parse', 'HEAD:' + str(TARGET).replace('\\','/')) != BASE_BLOB:
        raise RuntimeError('R4R12R5_UNREVIEWED_COMMITTED_RULE')
    changed = set(git(root, 'diff', '--name-only').splitlines() + git(root, 'diff', '--cached', '--name-only').splitlines())
    allowed = {TARGET.as_posix(), '.pytest_cache/v/cache/nodeids'}
    if changed - allowed:
        raise RuntimeError('R4R12R5_UNREVIEWED_TRACKED_CHANGE: ' + repr(sorted(changed-allowed)))
    path = root/TARGET
    before = path.read_bytes()
    source = before.replace(b'\r\n',b'\n').decode('utf-8')
    new, helper, function = render(source)
    after = new.encode('utf-8')
    if b'\r\n' in before:
        after = after.replace(b'\n',b'\r\n')
    return path,before,after,helper,function


def install(root: Path, *, dry_run: bool, output: Path):
    target,before,after,helper,function = plan(root)
    output.mkdir(parents=True,exist_ok=True)
    (output/'_rank_two_endpoints_FULL.py').write_text(helper,encoding='utf-8')
    (output/'two_summand_quotient_inputs_FULL.py').write_text(function,encoding='utf-8')
    (output/'rule_FULL_AFTER.py').write_bytes(after)
    if before != after and not dry_run:
        fd,temp = tempfile.mkstemp(prefix='r4r12r5_',suffix='.py',dir=target.parent)
        try:
            with os.fdopen(fd,'wb') as stream: stream.write(after)
            os.replace(temp,target)
        finally:
            if os.path.exists(temp):os.unlink(temp)
    return {'patch_required':before!=after,'patch_applied':before!=after and not dry_run,
            'full_functions_exported':True,'after_blob':blob(after.replace(b'\r\n',b'\n'))}

```

## tests/test_installer.py（全文）

```python
"""Pure installer contract tests, no repository mutations."""
from __future__ import annotations

from phase175_r4r12r5_iterated_suspension_endpoints import installer


def test_expected_committed_source_pin_and_narrow_patch() -> None:
    assert len(installer.BASE_BLOB)==40
    assert len(installer.EXPECTED_HEAD)==40
    assert installer.ORIGINAL_CHECK.count('_endpoints(')==4
    assert installer.NEW_CHECK.count('_rank_two_endpoints(')==4
    assert 'IteratedSuspension' in installer.HELPER


def test_helper_rejects_untyped_suspension_exponents() -> None:
    assert 'type(exponent) is not int or exponent < 0' in installer.HELPER
    assert 'left[0] != right[1]' in installer.HELPER


def test_reviewed_head_pin_matches_current_develop() -> None:
    assert installer.EXPECTED_HEAD == "9203e1a8c077320a58214bda40d9bfeb17704f58"

```

## run.ps1（全文）

```powershell
param([switch]$DryRun)
$ErrorActionPreference='Stop'
$root=(Resolve-Path '.').Path
python -m pytest -q phase175_r4r12r5_iterated_suspension_endpoints/tests/test_installer.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R5 installer tests failed' }
$argsList=@('--root',$root)
if ($DryRun) { $argsList+= '--dry-run' }
python -m phase175_r4r12r5_iterated_suspension_endpoints.audit @argsList
if ($LASTEXITCODE -ne 0) { throw 'R4R12R5 audit failed' }
if (-not $DryRun) {
    python -m pytest -q phase175_r4r12r5_iterated_suspension_endpoints/tests/test_endpoints.py phase175_r4r3_two_summand_quotient/tests/test_rule.py phase175_r4r12_public_two_summand_quotient/tests/test_provider.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R12R5 focused integration tests failed' }
}

```
