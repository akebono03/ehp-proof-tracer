# R13R8R3 コード全文

## 既存コードの変更

`phase168_r3_37c_reference_projection.py` の `_verified_source_sentence` 関数全文を置換。既存ファイルのモジュール import に変更なし。

```python
def _verified_source_sentence(statement: object) -> str | None:
    """Render only a uniquely verified, canonical typed source statement."""
    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource

    if type(statement) is TodaLemma54TypedSource and statement == TodaLemma54TypedSource():
        return (
            r"$\nu_4\in\pi_7^4$, "
            r"$H(\nu_4)=\iota_7$ および "
            r"$2E\nu_4=E^2\nu'$."
        )

    from phase175_r4r12r10r1_cited_511_public.source import (
        CitedToda511, canonical_511, verify_cited_511,
    )
    if type(statement) is CitedToda511:
        if statement != CitedToda511(canonical_511()):
            return None
        verify_cited_511()
        return r"$\Delta(\eta_9)=E\nu'\eta_7$."

    from phase175_r4r10_cited_58_prop25_public.source import (
        CitedToda58SignedDelta, canonical_toda58, source_positions,
    )
    if type(statement) is CitedToda58SignedDelta:
        if statement != CitedToda58SignedDelta(canonical_toda58()):
            return None
        source_positions()
        return r"$\Delta(\iota_9)=\pm(2\nu_4-E\nu')$."
    return None

```

## 新規ファイル：installer.py

追加位置：`phase175_r4r12r13r8r3_verified_reference_body/installer.py`

```python
"""Install only the full verified reference-body function; preserve file EOL."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess

PACKAGE = "phase175_r4r12r13r8r3_verified_reference_body"
TARGET = "phase168_r3_37c_reference_projection.py"
EXPECTED_GIT_BLOB = "3800dc72a2e09808f15b8ee78ae76d4d39c2eede"
FUNCTION = "_verified_source_sentence"


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if result.returncode:
        raise RuntimeError("GIT_FAILED: " + result.stderr)
    return result.stdout.strip()


def updated_bytes(original: bytes, replacement: str) -> bytes:
    if not isinstance(original, bytes) or not isinstance(replacement, str):
        raise TypeError("expected bytes and replacement string")
    normalized = original.replace(b"\r\n", b"\n")
    text = normalized.decode("utf-8")
    tree = ast.parse(text)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == FUNCTION]
    if len(matches) != 1:
        raise RuntimeError("FUNCTION_NOT_UNIQUE")
    node = matches[0]
    lines = text.splitlines(keepends=True)
    replace_text = replacement.rstrip("\n") + "\n"
    updated = "".join(lines[:node.lineno-1]) + replace_text + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    if original.count(b"\r\n") and original.count(b"\n") == original.count(b"\r\n"):
        updated = updated.replace("\n", "\r\n")
    return updated.encode("utf-8")


def run(root: Path, dry_run: bool) -> None:
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("BRANCH_MISMATCH")
    file = root / TARGET
    if git(root, "hash-object", TARGET) != EXPECTED_GIT_BLOB:
        raise RuntimeError("SOURCE_BLOB_MISMATCH_NO_WRITE")
    if git(root, "diff", "--name-only", "--", TARGET):
        raise RuntimeError("TRACKED_TARGET_DIRTY_NO_WRITE")
    source = file.read_bytes()
    replacement = (root / PACKAGE / "verified_function_FULL.py").read_text(encoding="utf-8")
    candidate = updated_bytes(source, replacement)
    if candidate == source:
        print("PHASE175_R13R8R3_PATCH_STATUS=ALREADY_APPLIED")
        return
    if dry_run:
        print("PHASE175_R13R8R3_PATCH_STATUS=DRYRUN_VERIFIED")
        return
    file.write_bytes(candidate)
    print("PHASE175_R13R8R3_PATCH_STATUS=INSTALLED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    main()

```

## 新規ファイル：run.ps1

追加位置：`phase175_r4r12r13r8r3_verified_reference_body/run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r12r13r8r3_verified_reference_body'
if ($DryRun) {
    & python -B (Join-Path $package 'installer.py') --root $repo --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R13R8R3 guarded DryRun failed' }
    Write-Output 'PHASE175_R13R8R3_GATE=DRYRUN_PASS'
    exit 0
}
& python -B (Join-Path $package 'installer.py') --root $repo
if ($LASTEXITCODE -ne 0) { throw 'R13R8R3 patch failed' }
& python -B -m pytest -q -p no:cacheprovider (Join-Path (Join-Path $package 'tests') 'test_verified_reference.py')
if ($LASTEXITCODE -ne 0) { throw 'R13R8R3 focused tests failed' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'Git diff whitespace check failed' }
Write-Output 'PHASE175_R13R8R3_GATE=REFERENCE_BODIES_TESTED_PREFIX_NOT_YET_AUDITED'

```

## 新規ファイル：tests/test_verified_reference.py

追加位置：`phase175_r4r12r13r8r3_verified_reference_body/tests/test_verified_reference.py`

```python
"""Focused typed-reference projection tests, including negative guards."""
from __future__ import annotations

from dataclasses import replace

from phase168_r3_37c_reference_projection import _verified_source_sentence
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
from phase175_r4r10_cited_58_prop25_public.source import CitedToda58SignedDelta, canonical_toda58


def test_verified_cited_511_reference_body() -> None:
    actual = _verified_source_sentence(CitedToda511(canonical_511()))
    assert actual == r"$\Delta(\eta_9)=E\nu'\eta_7$."


def test_verified_cited_58_reference_body_keeps_sign() -> None:
    actual = _verified_source_sentence(CitedToda58SignedDelta(canonical_toda58()))
    assert actual == r"$\Delta(\iota_9)=\pm(2\nu_4-E\nu')$."


def test_wrong_typed_reference_never_projects() -> None:
    assert _verified_source_sentence(replace(CitedToda511(canonical_511()), locator="(5.8)")) is None
    assert _verified_source_sentence(replace(CitedToda58SignedDelta(canonical_toda58()), locator="(5.11)")) is None


def test_web_complete_references_are_populated() -> None:
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase165_r52_partial_proof import ProofSearchStatus

    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(n=5, k=4, bridge=bridge, context_sink=contexts.append)
    assert result.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(result, contexts[-1])
    refs = {c.reference.locator: c for c in model.citations if c.reference.locator in ("(5.11)", "(5.8)")}
    assert set(refs) == {"(5.11)", "(5.8)"}
    assert refs["(5.11)"].statement_bodies == (r"$\Delta(\eta_9)=E\nu'\eta_7$.",)
    assert refs["(5.8)"].statement_bodies == (r"$\Delta(\iota_9)=\pm(2\nu_4-E\nu')$.",)

```
