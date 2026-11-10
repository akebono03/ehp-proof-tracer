# R45R1 コード全文と追加位置

既存本番コード・関数・クラスの変更はありません。
既存の監査ファイル2件をそのまま置き換え、リポジトリ直下に修正用ディレクトリを1件追加します。

## 変更対象と位置

- `phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1`：全文置換。
- `phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py`：全文置換。新規テスト関数は `test_runner_performs_no_install_or_full_test_suite` の直後。
- `phase174_r3_r7_r45r1_pytest_importmode_fix/`：リポジトリ直下の新規追加ディレクトリ。`patch.py` の関数と import、`tests/test_patch.py` のテスト関数と import は以下が全文。

## 修正後 R45 run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r45_ehp_open_obligation_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R45 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R45_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r45_ehp_open_obligation_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R45 EHP frontier audit failed' }
    $Groups = @(
        @{Name='R45_STATIC'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py'},
        @{Name='R45_GUARD'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_source_guard.py'},
        @{Name='R45_FRONTIER'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_frontier.py'},
        @{Name='PROP42_SPECIALIZATION_REGRESSION'; Path='phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py'},
        @{Name='PROP42_CONSEQUENCE_REGRESSION'; Path='phase165_r12_r12_ehp_consequences/tests/test_phase165_r12_r12_ehp_consequences.py'},
        @{Name='R5_HOPF_REGRESSION'; Path='phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py'},
        @{Name='R37_DELTA_REGRESSION'; Path='phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R45_TEST_GROUP=' + $Group.Name)
        # The historical Prop42 test directories shadow same-named .py modules
        # under pytest importlib mode; prepend resolves the real module.
        $ImportMode = 'importlib'
        if ($Group.Name -in @('PROP42_SPECIALIZATION_REGRESSION', 'PROP42_CONSEQUENCE_REGRESSION')) {
            $ImportMode = 'prepend'
        }
        python -B -m pytest -q "--import-mode=$ImportMode" -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R45 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R45_RUN=PASS'
    Write-Output 'PHASE174_R3R7R45_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```

## 修正後 R45 tests/test_static.py（import と関数全文）

```python
"""R45 is a self-contained non-invasive audit-only ZIP."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r45_python_modules_are_complete_and_parse():
    targets = (
        "__init__.py", "source_guard.py", "audit.py",
        "tests/test_frontier.py", "tests/test_source_guard.py",
        "tests/test_static.py",
    )
    for filename in targets:
        source = (PACKAGE / filename).read_text(encoding="utf-8")
        tree = ast.parse(source)
        assert not any(
            isinstance(node, ast.Constant) and node.value is Ellipsis
            for node in ast.walk(tree)
        )


def test_runner_performs_no_install_or_full_test_suite():
    source = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in source
    assert "--dry-run" in source
    assert "$ImportMode = 'importlib'" in source
    assert "git reset" not in source
    assert "git clean" not in source
    assert "install.py" not in source
    assert "FULL_PYTEST=False" in source


def test_prop42_regressions_use_prepend_to_avoid_same_name_module_shadowing():
    source = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "$ImportMode = 'importlib'" in source
    assert "'PROP42_SPECIALIZATION_REGRESSION', 'PROP42_CONSEQUENCE_REGRESSION'" in source
    assert "$ImportMode = 'prepend'" in source
    assert '"--import-mode=$ImportMode"' in source
    assert "R45_FRONTIER" in source


def test_no_derived_theorem_is_installed_or_given():
    source = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "ProofStep(" not in source
    assert "ProofRule.GIVEN" in source
    assert "source_guard" in source
    assert "expand_provider=" not in source
    assert "expansion_provider=scoped" in source
```

## 新規 R45R1 patch.py

```python
"""Guarded, idempotent replacement of R45 runner and its static contract.

The production math modules, source references and R45 audit itself are not
modified. A dry run checks the reviewed checkout without writing any files.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import verify_checkout

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGETS = (
    "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py",
)


def normalized_sha256(data: bytes) -> str:
    """Compare exact reviewed content modulo whole-file Windows EOL conversion."""
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def target_fragments(relative_path: str) -> tuple[Path, Path]:
    prefix = "phase174_r3_r7_r45_ehp_open_obligation_audit/"
    if relative_path not in TARGETS or not relative_path.startswith(prefix):
        raise ValueError("Unreviewed patch destination")
    child = relative_path[len(prefix):]
    return PACKAGE / "baseline" / child, PACKAGE / "replacement" / child


def pending_replacements(root: Path = ROOT) -> tuple[tuple[Path, Path, str], ...]:
    """Refuse arbitrary edits; accept only baseline or the exact repaired file."""
    result = []
    for relative in TARGETS:
        original, replacement = target_fragments(relative)
        destination = root / relative
        if not all(x.is_file() for x in (original, replacement, destination)):
            raise RuntimeError("Missing reviewed file: " + relative)
        current = normalized_sha256(destination.read_bytes())
        before = normalized_sha256(original.read_bytes())
        after = normalized_sha256(replacement.read_bytes())
        if before == after:
            raise RuntimeError("Repair replacement unexpectedly unchanged: " + relative)
        if current not in (before, after):
            raise RuntimeError("Unreviewed existing R45 file: " + relative)
        result.append((destination, replacement, "ALREADY_REPAIRED" if current == after else "REPLACE"))
    return tuple(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    changes = pending_replacements()
    if not args.dry_run:
        for destination, replacement, mode in changes:
            if mode == "REPLACE":
                destination.write_bytes(replacement.read_bytes())
        if any(mode != "ALREADY_REPAIRED" for _, _, mode in pending_replacements()):
            raise RuntimeError("Patch verification failed")
    print("PHASE174_R3R7R45R1_SOURCE_GUARD=" + state["source_guard"])
    print("PHASE174_R3R7R45R1_REVIEWED_HEAD=" + state["local_head"])
    print("PHASE174_R3R7R45R1_TARGET_FILES=" + str(len(changes)))
    for destination, _, mode in changes:
        print("PHASE174_R3R7R45R1_TARGET=" + destination.relative_to(ROOT).as_posix() + ":" + mode)
    print("PHASE174_R3R7R45R1_PRODUCTION_FILES_CHANGED=0")
    print("PHASE174_R3R7R45R1_FULL_PYTEST=False")
    print("PHASE174_R3R7R45R1_GATE=" + (
        "PASS_R45R1_IMPORTMODE_DRYRUN" if args.dry_run else
        "PASS_R45R1_IMPORTMODE_REPAIR_APPLIED"
    ))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規 R45R1 run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r45r1_pytest_importmode_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R45R1 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R45R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r45r1_pytest_importmode_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R45R1 guarded patch failed' }
    powershell -NoProfile -ExecutionPolicy Bypass `
      -File '.\phase174_r3_r7_r45_ehp_open_obligation_audit\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R45 focused audit or regression tests failed' }
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
      'phase174_r3_r7_r45r1_pytest_importmode_fix/tests/test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R45R1 repair regression failed' }
    Write-Output 'PHASE174_R3R7R45R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R45R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```

## 新規 R45R1 tests/test_patch.py

```python
"""The R45R1 patch must not alter mathematical rules or unrelated files."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r45r1_pytest_importmode_fix.patch import (
    ROOT, TARGETS, normalized_sha256, pending_replacements, target_fragments,
)


def test_import_mode_repair_changes_only_two_reviewed_r45_files():
    assert TARGETS == (
        "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1",
        "phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py",
    )
    run_before, run_after = target_fragments(TARGETS[0])
    test_before, test_after = target_fragments(TARGETS[1])
    original = run_before.read_text(encoding="utf-8")
    revised = run_after.read_text(encoding="utf-8")
    assert "--import-mode=importlib" in original
    assert "$ImportMode = 'prepend'" not in original
    assert "$ImportMode = 'prepend'" in revised
    assert "'PROP42_SPECIALIZATION_REGRESSION', 'PROP42_CONSEQUENCE_REGRESSION'" in revised
    original_call = "        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path"
    revised_call = "\n".join((
        "        # The historical Prop42 test directories shadow same-named .py modules",
        "        # under pytest importlib mode; prepend resolves the real module.",
        "        $ImportMode = 'importlib'",
        "        if ($Group.Name -in @('PROP42_SPECIALIZATION_REGRESSION', 'PROP42_CONSEQUENCE_REGRESSION')) {",
        "            $ImportMode = 'prepend'",
        "        }",
        '        python -B -m pytest -q "--import-mode=$ImportMode" -p no:cacheprovider $Group.Path',
    ))
    assert revised.replace(revised_call, original_call) == original
    original_static = test_before.read_text(encoding="utf-8")
    revised_static = test_after.read_text(encoding="utf-8")
    start = revised_static.index("\n\ndef test_prop42_regressions_use_prepend_")
    end = revised_static.index("\n\ndef test_no_derived_theorem_is_installed_or_given", start)
    without_added_guard = revised_static[:start] + revised_static[end:]
    old_assertion = '    assert "--import-mode=importlib" in source'
    new_assertion = '    assert "$ImportMode = \'importlib\'" in source'
    assert without_added_guard.replace(new_assertion, old_assertion) == original_static


def test_repair_current_files_are_pinned_and_idempotent():
    changes = pending_replacements(ROOT)
    assert len(changes) == 2
    assert all(mode == "ALREADY_REPAIRED" for _, _, mode in changes)
    for dest, replacement, _ in changes:
        assert normalized_sha256(dest.read_bytes()) == normalized_sha256(replacement.read_bytes())


def test_repair_runner_has_dry_run_and_no_full_suite():
    script = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in script
    assert "patch --dry-run" in script
    assert "phase174_r3_r7_r45_ehp_open_obligation_audit\\run.ps1" in script
    assert "--import-mode=importlib" in script
    assert "git reset" not in script
    assert "git clean" not in script
    assert "FULL_PYTEST=False" in script
```
