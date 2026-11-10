# R56R1 修正コード全文

## 変更対象（先に列挙）

- `phase174_r3_r7_r56_cyclic_generator_bridge/audit.py`：`main()` 全体。import の変更はありません。
- `phase174_r3_r7_r56r1_audit_path_fix/install.py`：新規ファイル、すべての関数を全文掲載。
- `phase174_r3_r7_r56r1_audit_path_fix/tests/test_audit_path.py`：新規テストファイル、すべての関数を全文掲載。
- `phase174_r3_r7_r56r1_audit_path_fix/run.ps1`：新規 PowerShell 実行スクリプト全文。

### 変更後 `audit.py` の import 全文（変更なし）

```python
"""Real source-first Group query audit for the two general R56 inferences."""

from __future__ import annotations



import argparse

import json

import os

from pathlib import Path

import tempfile



from phase174_r3_r7_r56_cyclic_generator_bridge.install import review
```

### 変更後の `audit.py` の `main()` 全文

```python
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = review()
    data = None if args.dry_run else inspect_public()
    report = {
        "phase": "174-R3-R7-R56",
        "local_head": state["local_head"],
        "source_guard": state["source_guard"],
        "inspection": data,
        "gate": "PASS_PREFLIGHT_ONLY" if args.dry_run else data["gate"],
    }
    destination = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    destination /= Path("EHPProofTracerAudit") / "phase174_r3_r7_r56"
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / ("preflight.json" if args.dry_run else "public_proofs.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R56_SOURCE_GUARD=" + str(report["source_guard"]))
    if data is not None:
        for key, value in data.items():
            if key != "gate":
                print("PHASE174_R56_" + key.upper() + "=" + str(value))
    print("PHASE174_R56_REPORT=" + str(output))
    print("PHASE174_R56_GATE=" + str(report["gate"]))
    print("(END)")
    return 0

```

変更後の `audit.py` 全文は同じ ZIP 内の `audit_FULL_AFTER.py` に格納しています。これは確認用ファイルであり、Python 実行経路には読み込まれません。

## 新規 `install.py` 全文

```python
"""Fail-closed correction of the R56 audit report directory Path expression.

Only the untracked R56 audit module is changed. All proof rules, proof search,
registered sources, and common rendering code are retained exactly.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_FILE = ROOT / "phase174_r3_r7_r56_cyclic_generator_bridge" / "audit.py"
BASELINE_SHA256 = "240e88a7a404f0ecc5640fe1b3155fd55e6ac2c148f2c5760986afaa6d5940e3"
PATCHED_SHA256 = "e4c37f2ec99847682a2df52dfdf295ea6b2a3a18d2c01e482ddfc61d9a4124f5"
OLD_LINE = '    destination /= "EHPProofTracerAudit" / "phase174_r3_r7_r56"'
NEW_LINE = '    destination /= Path("EHPProofTracerAudit") / "phase174_r3_r7_r56"'


def _read_lf(raw: bytes) -> tuple[str, str]:
    """Allow LF or uniform CRLF, but reject mixed, partial, and BOM edits."""
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw.replace(b"\r\n", b""):
        raise RuntimeError("unreviewed encoding or CR-only line ending in R56 audit")
    if b"\r\n" in raw and raw.count(b"\n") != raw.count(b"\r\n"):
        raise RuntimeError("mixed line endings in R56 audit")
    style = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), style


def _sha(normalized_text: str) -> str:
    return hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()


def patch_source(source: str) -> str:
    """Replace only the verified invalid Path expression, never audit logic."""
    if source.count(OLD_LINE) != 1 or NEW_LINE in source:
        raise RuntimeError("R56 audit Path patch anchor is absent or ambiguous")
    updated = source.replace(OLD_LINE, NEW_LINE, 1)
    ast.parse(updated, filename=str(AUDIT_FILE))
    if _sha(source) != BASELINE_SHA256 or _sha(updated) != PATCHED_SHA256:
        raise RuntimeError("R56 audit content differs from reviewed ZIP baseline")
    return updated


def review() -> dict[str, object]:
    """Reuse R56 production Source Guard and verify the full original audit."""
    from phase174_r3_r7_r56_cyclic_generator_bridge.install import review as review_r56

    base = review_r56()
    if base["source_guard"] != "PASS":
        raise RuntimeError("R56 production Source Guard did not pass")
    if not AUDIT_FILE.is_file():
        raise RuntimeError("R56 audit module not found")
    raw = AUDIT_FILE.read_bytes()
    old, style = _read_lf(raw)
    current = _sha(old)
    if current == BASELINE_SHA256:
        updated = patch_source(old)
    elif current == PATCHED_SHA256:
        updated = old
        if updated.count(NEW_LINE) != 1 or OLD_LINE in updated:
            raise RuntimeError("R56 patched audit structure is invalid")
        ast.parse(updated, filename=str(AUDIT_FILE))
    else:
        raise RuntimeError("R56 audit was edited outside reviewed baseline; refusing overwrite")
    return {
        "local_head": base["local_head"],
        "source_guard": "PASS",
        "audit_source_sha256": current,
        "changed": current != PATCHED_SHA256,
        "raw": raw,
        "replacement": updated.replace("\n", style).encode("utf-8"),
    }


def install(dry_run: bool) -> dict[str, object]:
    state = review()
    if not dry_run and state["changed"]:
        AUDIT_FILE.write_bytes(state["replacement"])
        if _sha(_read_lf(AUDIT_FILE.read_bytes())[0]) != PATCHED_SHA256:
            raise RuntimeError("R56 audit post-install file check failed")
    return {
        "local_head": state["local_head"],
        "source_guard": state["source_guard"],
        "audit_source_sha256": state["audit_source_sha256"],
        "changed": state["changed"],
        "gate": ("PASS_R56R1_PREFLIGHT_ONLY" if dry_run
                 else "PASS_R56R1_AUDIT_REPORT_PATH_PATCHED"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = install(args.dry_run)
    for key, value in state.items():
        print("PHASE174_R56R1_" + key.upper() + "=" + str(value))
    print("PHASE174_R56R1_NEW_GIVEN=0")
    print("PHASE174_R56R1_NEW_MATH_RULES=0")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## 新規 `tests/test_audit_path.py` 全文

```python
"""Focused R56R1 audit Path regression without fabricated mathematical proofs."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

import pytest

from phase174_r3_r7_r56r1_audit_path_fix.install import (
    BASELINE_SHA256,
    PATCHED_SHA256,
    OLD_LINE,
    NEW_LINE,
    _read_lf,
    _sha,
    patch_source,
)


PACKAGE = Path(__file__).resolve().parents[1]
BASELINE_FILE = PACKAGE / "audit_FULL_AFTER.py"


def test_exact_r56_original_zip_hash_and_one_line_patch() -> None:
    corrected = BASELINE_FILE.read_text(encoding="utf-8")
    original = corrected.replace(NEW_LINE, OLD_LINE)
    assert corrected.count(NEW_LINE) == 1
    assert _sha(original) == BASELINE_SHA256
    assert _sha(corrected) == PATCHED_SHA256
    assert patch_source(original) == corrected
    ast.parse(corrected)


def test_fails_closed_for_missing_or_tampered_original() -> None:
    corrected = BASELINE_FILE.read_text(encoding="utf-8")
    original = corrected.replace(NEW_LINE, OLD_LINE)
    with pytest.raises(RuntimeError):
        patch_source(corrected)
    with pytest.raises(RuntimeError):
        patch_source(original.replace(OLD_LINE, "    destination = 'tampered'"))
    with pytest.raises(RuntimeError):
        patch_source(original.replace("import argparse", "import random"))


def test_uniform_crlf_is_accepted_without_normalizing_git_blob_hash() -> None:
    corrected = BASELINE_FILE.read_text(encoding="utf-8")
    crlf = corrected.replace("\n", "\r\n").encode("utf-8")
    normalized, eol = _read_lf(crlf)
    assert eol == "\r\n"
    assert normalized == corrected
    assert hashlib.sha256(crlf).hexdigest() != PATCHED_SHA256
    with pytest.raises(RuntimeError):
        _read_lf(b"first\r\nsecond\n")


@pytest.mark.parametrize("dry_run", (False, True))
def test_actual_audit_main_writes_report_after_completed_inspection(
    dry_run: bool, monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    source = BASELINE_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "main"]
    assert len(nodes) == 1
    isolated = ast.Module(body=nodes, type_ignores=[])
    inspection_calls = []

    def fake_review() -> dict[str, object]:
        return {"local_head": "test-only-head", "source_guard": "PASS"}

    def fake_inspect() -> dict[str, object]:
        inspection_calls.append(True)
        return {"gate": "PASS_R56_TWO_GENERAL_RULES_SOURCE_FIRST_PUBLIC",
                "pi11_6_complete": True, "pi12_7_complete": True}

    scope = {
        "argparse": argparse,
        "json": json,
        "os": os,
        "Path": Path,
        "tempfile": tempfile,
        "review": fake_review,
        "inspect_public": fake_inspect,
    }
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["audit"] + (["--dry-run"] if dry_run else []))
    exec(compile(isolated, str(BASELINE_FILE), "exec"), scope)
    assert scope["main"]() == 0
    report = (tmp_path / "EHPProofTracerAudit" / "phase174_r3_r7_r56"
              / ("preflight.json" if dry_run else "public_proofs.json"))
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["source_guard"] == "PASS"
    assert data["inspection"] is None if dry_run else data["inspection"]["pi11_6_complete"]
    assert len(inspection_calls) == (0 if dry_run else 1)

```

## 新規 `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r56r1_audit_path_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R56R1 guarded audit correction DryRun failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R56R1_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }

    python -B -m phase174_r3_r7_r56r1_audit_path_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R56R1 audit correction failed' }

    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider '.\phase174_r3_r7_r56r1_audit_path_fix\tests\test_audit_path.py'
    if ($LASTEXITCODE -ne 0) { throw 'R56R1 focused report-path tests failed' }

    python -B -m phase174_r3_r7_r56_cyclic_generator_bridge.audit
    if ($LASTEXITCODE -ne 0) { throw 'R56 public proof certification failed after report-path fix' }

    Write-Output 'PHASE174_R56R1_FOCUSED_TESTS=PASS'
    Write-Output 'PHASE174_R56R1_FULL_PYTEST=False'
    Write-Output 'PHASE174_R56R1_GATE=PASS_R56R1_REPORT_PATH_AND_R56_PUBLIC_AUDIT'
    Write-Output '(END)'
} finally {
    Pop-Location
}

```
