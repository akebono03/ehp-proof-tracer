# R43R2 コード全文

既存の変更対象は `phase174_r3_r7_r43r1_r3_sha_pin_fix/install.py` の `verify_checkout()` 全体のみ。新規 R43R2 の `repair.py`、`run.ps1`、`tests/test_guard.py` は同梱ファイルそのものが全文です。省略箇所はありません。

## 変更後の import 全文

```python
"""Fail-closed repair of a single R43 source SHA literal. No production edits."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PREVIOUS_DIR = ROOT / "phase174_r3_r7_r43_public_ehp_map_property_wiring"
TARGET = PREVIOUS_DIR / "source_guard.py"
EXPECTED_HEAD = "f5b6899b124d435c224870476b2448454f77b1b5"
REVIEWED_EHP_SOURCE_PATH = "phase174_r3_r7_r3_ehp_zero_rule/rule.py"
REVIEWED_EHP_SOURCE_BLOB = "8834cbefbfca5bcca18dc01f072c9738a05f7bdc"
WRONG_SHA = "8834cbefbfca18dc01f072c9738a05f7bdc"
CORRECT_SHA = REVIEWED_EHP_SOURCE_BLOB
PREVIOUS_PINS = {'install.py': '07591182c401643835b910be1c9f6f95aa0c084b871e1f4815c2c879925a0756', 'audit.py': 'c62bd6869f52d30b4fc764dad2884c061cc1cb6d0524fda4bd8895e770b5e0f2', 'run.ps1': '0ea5ce8b3282ad44a6d21199b51a41fe9b59e23cfb8dabc8106711b04e3f24ad', 'tests/test_guard.py': 'ad40a7e7f2a1623db18b9736a9ef55b8dc03f7ad3eb3abd172b1a75ded7e6839', 'tests/test_public.py': '1078a24393b48e998fb37b883b05232342c4d0fe0df9423f0905158b12fff2f5', 'tests/test_static.py': '0645503867844300715d8fea16b4ad3f5d3cb920760d5689685399be92f7774b'}


```

## 変更後の verify_checkout() 全文

```python
def verify_checkout() -> dict[str, object]:
    """Refuse changed Git lineage, tracked edits, or unreviewed R43 package."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R43R1 into the Git repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R43R1 requires develop")
    local = git("rev-parse", "HEAD")
    remote_rows = git("ls-remote", "origin", "refs/heads/develop").split()
    remote = remote_rows[0] if remote_rows else ""
    if local != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError("Unreviewed HEAD; do not change files")
    # R43R2: allow only the exactly reviewed R43 provider installation.
    # Every other tracked change, and any staged change, still fails closed.
    staged = tuple(git("diff", "--cached", "--name-only").splitlines())
    modified = tuple(git("diff", "--name-only").splitlines())
    if staged:
        raise RuntimeError("Staged changes require independent review: " + repr(staged))
    reviewed_target = "phase165_r52_r9_shared_math.py"
    if modified and modified != (reviewed_target,):
        raise RuntimeError("Unreviewed tracked changes; no files modified: " + repr(modified))
    if modified:
        # Exact bytes, not only a path whitelist. No reset or discarded work.
        from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
            expected_replacement,
        )
        baseline_output = subprocess.run(
            ("git", "show", "HEAD:" + reviewed_target),
            cwd=ROOT, check=True, capture_output=True,
        ).stdout
        expected = expected_replacement(baseline_output)
        actual = normalize((ROOT / reviewed_target).read_bytes())
        if actual != expected:
            raise RuntimeError(
                "Reviewed R43 target has a different modification; no files modified: "
                + reviewed_target
            )
    for relative, expected in PREVIOUS_PINS.items():
        item = PREVIOUS_DIR / relative
        if not item.is_file() or sha256(item.read_bytes()) != expected:
            raise RuntimeError("Existing R43 file changed: " + relative)
    if not reviewed_source_blob((ROOT / REVIEWED_EHP_SOURCE_PATH).read_bytes()):
        raise RuntimeError("The actual historical EHP source has changed")
    baseline, replacement = replacement_contract()
    if not TARGET.is_file():
        raise RuntimeError("Original R43 source_guard.py is absent")
    current = normalize(TARGET.read_bytes())
    if current == baseline:
        mode = "BASELINE"
    elif current == replacement:
        mode = "PATCHED"
    else:
        raise RuntimeError("R43 source_guard.py differs from both reviewed versions")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "old_sha_length": len(WRONG_SHA),
        "correct_sha_length": len(CORRECT_SHA),
        "correct_sha": CORRECT_SHA,
        "r43_source_guard_mode": mode,
        "production_files_changed": 0,
        "target_files": 1,
        "full_pytest": False,
    }
```

## 変更後 install.py 全文

```python
"""Fail-closed repair of a single R43 source SHA literal. No production edits."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PREVIOUS_DIR = ROOT / "phase174_r3_r7_r43_public_ehp_map_property_wiring"
TARGET = PREVIOUS_DIR / "source_guard.py"
EXPECTED_HEAD = "f5b6899b124d435c224870476b2448454f77b1b5"
REVIEWED_EHP_SOURCE_PATH = "phase174_r3_r7_r3_ehp_zero_rule/rule.py"
REVIEWED_EHP_SOURCE_BLOB = "8834cbefbfca5bcca18dc01f072c9738a05f7bdc"
WRONG_SHA = "8834cbefbfca18dc01f072c9738a05f7bdc"
CORRECT_SHA = REVIEWED_EHP_SOURCE_BLOB
PREVIOUS_PINS = {'install.py': '07591182c401643835b910be1c9f6f95aa0c084b871e1f4815c2c879925a0756', 'audit.py': 'c62bd6869f52d30b4fc764dad2884c061cc1cb6d0524fda4bd8895e770b5e0f2', 'run.ps1': '0ea5ce8b3282ad44a6d21199b51a41fe9b59e23cfb8dabc8106711b04e3f24ad', 'tests/test_guard.py': 'ad40a7e7f2a1623db18b9736a9ef55b8dc03f7ad3eb3abd172b1a75ded7e6839', 'tests/test_public.py': '1078a24393b48e998fb37b883b05232342c4d0fe0df9423f0905158b12fff2f5', 'tests/test_static.py': '0645503867844300715d8fea16b4ad3f5d3cb920760d5689685399be92f7774b'}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True,
        text=True, capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def normalize(content: bytes) -> bytes:
    return content.replace(b"\r\n", b"\n")


def sha256(content: bytes) -> str:
    return hashlib.sha256(normalize(content)).hexdigest()


def git_blob(content: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(content)).encode("ascii") + b"\0" + content,
    ).hexdigest()


def reviewed_source_blob(content: bytes) -> bool:
    canonical = normalize(content)
    return len(REVIEWED_EHP_SOURCE_BLOB) == 40 and REVIEWED_EHP_SOURCE_BLOB in (
        git_blob(content), git_blob(canonical),
        git_blob(canonical.replace(b"\n", b"\r\n")),
    )


def replacement_contract() -> tuple[bytes, bytes]:
    """Require literally one inserted five-character SHA segment."""
    baseline = normalize((PACKAGE / "baseline" / "source_guard.py").read_bytes())
    replacement = normalize((PACKAGE / "replacement" / "source_guard.py").read_bytes())
    old = ("\"" + WRONG_SHA + "\"").encode("ascii")
    new = ("\"" + CORRECT_SHA + "\"").encode("ascii")
    if (len(WRONG_SHA) != 35 or len(CORRECT_SHA) != 40
            or baseline.count(old) != 1
            or replacement != baseline.replace(old, new, 1)
            or baseline == replacement):
        raise RuntimeError("R43R1 change is not exactly the reviewed SHA correction")
    return baseline, replacement


def verify_checkout() -> dict[str, object]:
    """Refuse changed Git lineage, tracked edits, or unreviewed R43 package."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R43R1 into the Git repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R43R1 requires develop")
    local = git("rev-parse", "HEAD")
    remote_rows = git("ls-remote", "origin", "refs/heads/develop").split()
    remote = remote_rows[0] if remote_rows else ""
    if local != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError("Unreviewed HEAD; do not change files")
    # R43R2: allow only the exactly reviewed R43 provider installation.
    # Every other tracked change, and any staged change, still fails closed.
    staged = tuple(git("diff", "--cached", "--name-only").splitlines())
    modified = tuple(git("diff", "--name-only").splitlines())
    if staged:
        raise RuntimeError("Staged changes require independent review: " + repr(staged))
    reviewed_target = "phase165_r52_r9_shared_math.py"
    if modified and modified != (reviewed_target,):
        raise RuntimeError("Unreviewed tracked changes; no files modified: " + repr(modified))
    if modified:
        # Exact bytes, not only a path whitelist. No reset or discarded work.
        from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
            expected_replacement,
        )
        baseline_output = subprocess.run(
            ("git", "show", "HEAD:" + reviewed_target),
            cwd=ROOT, check=True, capture_output=True,
        ).stdout
        expected = expected_replacement(baseline_output)
        actual = normalize((ROOT / reviewed_target).read_bytes())
        if actual != expected:
            raise RuntimeError(
                "Reviewed R43 target has a different modification; no files modified: "
                + reviewed_target
            )
    for relative, expected in PREVIOUS_PINS.items():
        item = PREVIOUS_DIR / relative
        if not item.is_file() or sha256(item.read_bytes()) != expected:
            raise RuntimeError("Existing R43 file changed: " + relative)
    if not reviewed_source_blob((ROOT / REVIEWED_EHP_SOURCE_PATH).read_bytes()):
        raise RuntimeError("The actual historical EHP source has changed")
    baseline, replacement = replacement_contract()
    if not TARGET.is_file():
        raise RuntimeError("Original R43 source_guard.py is absent")
    current = normalize(TARGET.read_bytes())
    if current == baseline:
        mode = "BASELINE"
    elif current == replacement:
        mode = "PATCHED"
    else:
        raise RuntimeError("R43 source_guard.py differs from both reviewed versions")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "old_sha_length": len(WRONG_SHA),
        "correct_sha_length": len(CORRECT_SHA),
        "correct_sha": CORRECT_SHA,
        "r43_source_guard_mode": mode,
        "production_files_changed": 0,
        "target_files": 1,
        "full_pytest": False,
    }


def install(*, dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if dry_run:
        state["mode"] = "DRYRUN"
        state["corrected_preview"] = True
        return state
    if state["r43_source_guard_mode"] == "BASELINE":
        _baseline, replacement = replacement_contract()
        old = TARGET.read_bytes()
        data = replacement.replace(b"\n", b"\r\n") if b"\r\n" in old else replacement
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=TARGET.parent, prefix="r43r1_", suffix=".tmp",
                delete=False,
            ) as stream:
                temp_path = stream.name
                stream.write(data)
            os.replace(temp_path, TARGET)
        finally:
            if temp_path is not None and os.path.exists(temp_path):
                os.unlink(temp_path)
    checked = verify_checkout()
    if checked["r43_source_guard_mode"] != "PATCHED":
        raise RuntimeError("R43R1 correction did not persist")
    checked["mode"] = "INSTALLED"
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = install(dry_run=args.dry_run)
    prefix = "PHASE174_R3R7R43R1_"
    for key, value in result.items():
        print(prefix + key.upper() + "=" + str(value))
    print(prefix + "GATE=PASS_R43R1_REVIEWED_R3_SHA_PIN_REPAIRED")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規 repair.py 全文

```python
"""R43R2: apply an exact fail-closed allowance for a reviewed R43 change."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PREVIOUS = ROOT / "phase174_r3_r7_r43r1_r3_sha_pin_fix"
R43 = ROOT / "phase174_r3_r7_r43_public_ehp_map_property_wiring"
TARGET = PREVIOUS / "install.py"
EXPECTED_HEAD = "f5b6899b124d435c224870476b2448454f77b1b5"
PUBLIC_TARGET = "phase165_r52_r9_shared_math.py"
ORIGINAL_INSTALL_SHA256 = "dbf35b58f5a23747cec9f9da401cf00f58f157bd83ef508d280804c6934f63ba"
REVIEWED_R43_GUARD_SHA256 = "6b030ba62b36dea14f08b8823974c485853f9101652a26236b12710b80d43c8a"
CORRECTED_R43_GUARD_SHA256 = "52bda02f8f63c217bb7b90fb11fc2d58a4e852a0645c460322872faa3685543c"


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def normalized(content: bytes) -> bytes:
    return content.replace(b"\r\n", b"\n")


def sha256(content: bytes) -> str:
    return hashlib.sha256(normalized(content)).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Only one exactly reviewed R43 target edit is an approved exception."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R43R2 at the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R43R2 requires develop")
    local = git("rev-parse", "HEAD")
    remote_data = git("ls-remote", "origin", "refs/heads/develop").split()
    remote = remote_data[0] if remote_data else ""
    if local != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError(
            "Unreviewed Git HEAD; local=" + local + "; remote=" + remote
        )
    staged = tuple(git("diff", "--cached", "--name-only").splitlines())
    changed = tuple(git("diff", "--name-only").splitlines())
    if staged:
        raise RuntimeError("Staged changes require review: " + repr(staged))
    if changed and changed != (PUBLIC_TARGET,):
        raise RuntimeError("Unreviewed tracked changes: " + repr(changed))
    guard = R43 / "source_guard.py"
    if (not guard.is_file()
            or sha256(guard.read_bytes()) not in (
                REVIEWED_R43_GUARD_SHA256, CORRECTED_R43_GUARD_SHA256,
            )):
        raise RuntimeError("R43 Source Guard differs from both reviewed versions")
    if changed:
        from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
            expected_replacement,
        )
        baseline = subprocess.run(
            ("git", "show", "HEAD:" + PUBLIC_TARGET),
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
        expected = expected_replacement(baseline)
        target = ROOT / PUBLIC_TARGET
        if not target.is_file() or normalized(target.read_bytes()) != expected:
            raise RuntimeError("R43 target differs from the exact reviewed patch")
    base, replacement = reviewed_contract()
    if not TARGET.is_file():
        raise RuntimeError("Prior R43R1 installer is absent")
    actual = normalized(TARGET.read_bytes())
    if actual == base:
        mode = "BASELINE"
    elif actual == replacement:
        mode = "PATCHED"
    else:
        raise RuntimeError("Prior R43R1 installer changed outside reviewed function")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "tracked_paths": list(changed),
        "staged_paths": list(staged),
        "reviewed_r43_target_state": "EXACT_INSTALLED" if changed else "CLEAN",
        "r43r1_installer_state": mode,
        "production_files_changed_by_r43r2": 0,
        "full_pytest": False,
    }


def reviewed_contract() -> tuple[bytes, bytes]:
    """Only replace the complete verify_checkout function, not the other code."""
    base = normalized((PACKAGE / "baseline" / "install.py").read_bytes())
    new = normalized((PACKAGE / "replacement" / "install.py").read_bytes())
    if sha256(base) != ORIGINAL_INSTALL_SHA256 or base == new:
        raise RuntimeError("Reviewed R43R1 baseline installer does not match")
    import ast
    old_tree = ast.parse(base.decode("utf-8"))
    new_tree = ast.parse(new.decode("utf-8"))
    def function_map(tree):
        return {node.name: ast.dump(node) for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    old_fns, new_fns = function_map(old_tree), function_map(new_tree)
    if (set(old_fns) != set(new_fns)
            or any(old_fns[key] != new_fns[key] for key in old_fns
                   if key != "verify_checkout")
            or old_fns["verify_checkout"] == new_fns["verify_checkout"]):
        raise RuntimeError("Unexpected changes outside full verify_checkout")
    expected_guard = b'    if git("diff", "--cached", "--name-only") or git("diff", "--name-only"):'
    if base.count(expected_guard) != 1 or expected_guard in new:
        raise RuntimeError("Guard replacement is not the exact reviewed change")
    for literal in (
        b'if staged:',
        b'if modified and modified != (reviewed_target,):',
        b'if actual != expected:',
        b'raise RuntimeError(',
    ):
        if literal not in new:
            raise RuntimeError("Safety constraint missing in replacement installer")
    return base, new


def install(*, dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if dry_run:
        state["mode"] = "DRYRUN"
        return state
    if state["r43r1_installer_state"] == "BASELINE":
        _base, replacement = reviewed_contract()
        original = TARGET.read_bytes()
        selected = replacement.replace(b"\n", b"\r\n") if b"\r\n" in original else replacement
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=TARGET.parent, prefix="r43r2_", suffix=".tmp", delete=False,
            ) as stream:
                temporary = stream.name
                stream.write(selected)
            os.replace(temporary, TARGET)
        finally:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)
    checked = verify_checkout()
    if checked["r43r1_installer_state"] != "PATCHED":
        raise RuntimeError("R43R2 guarded installer correction was not installed")
    checked["mode"] = "INSTALLED"
    return checked


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    result = install(dry_run=args.dry_run)
    prefix = "PHASE174_R3R7R43R2_"
    for key, value in result.items():
        print(prefix + key.upper() + "=" + str(value))
    print(prefix + "GATE=PASS_R43R2_REVIEWED_TRACKED_CHANGE_GUARD_CORRECTED")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規テスト全文

```python
"""R43R2 exact edited-function and fail-closed contract tests."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r43r2_reviewed_tracked_change_guard.repair import (
    reviewed_contract,
)

ROOT = Path(__file__).resolve().parents[1]


def test_only_verify_checkout_changed():
    original, edited = reviewed_contract()
    before = ast.parse(original.decode("utf-8"))
    after = ast.parse(edited.decode("utf-8"))
    old = {node.name: ast.dump(node) for node in before.body
           if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    new = {node.name: ast.dump(node) for node in after.body
           if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    assert old.keys() == new.keys()
    assert old["verify_checkout"] != new["verify_checkout"]
    for name in old:
        if name != "verify_checkout":
            assert old[name] == new[name]


def test_staged_changes_are_never_admitted():
    _, edited = reviewed_contract()
    code = edited.decode("utf-8")
    assert 'git("diff", "--cached", "--name-only")' in code
    assert "if staged:" in code
    assert "Staged changes require independent review" in code


def test_only_exact_r43_public_target_is_whitelisted():
    _, edited = reviewed_contract()
    code = edited.decode("utf-8")
    assert 'reviewed_target = "phase165_r52_r9_shared_math.py"' in code
    assert "modified != (reviewed_target,)" in code
    assert "expected_replacement(baseline_output)" in code
    assert "if actual != expected:" in code
    assert "Unreviewed tracked changes; no files modified" in code


def test_source_pins_and_r43r1_contract_unchanged():
    original, edited = reviewed_contract()
    for literal in (
        b"REVIEWED_EHP_SOURCE_BLOB",
        b"PREVIOUS_PINS",
        b"reviewed_source_blob",
        b"replacement_contract",
        b"EXPECTED_HEAD",
    ):
        assert literal in original and literal in edited


def test_run_always_runs_prior_guard_and_focused_tests():
    run = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in run
    assert "R43R1 DryRun failed" in run
    assert "R43R1/R43 audit failed" in run
    assert "pytest -q --import-mode=importlib" in run
    assert "git reset" not in run
    assert "git clean" not in run
    assert "FULL_PYTEST=False" in run


def test_repair_does_not_touch_production_or_fabricate_source():
    code = (ROOT / "repair.py").read_text(encoding="utf-8")
    assert 'TARGET = PREVIOUS / "install.py"' in code
    assert "os.replace(temporary, TARGET)" in code
    assert "R43 target differs from the exact reviewed patch" in code
    assert "Staged changes require review" in code
    assert "Unreviewed tracked changes" in code
```

## 実行 PowerShell 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r43r2_reviewed_tracked_change_guard.repair --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R43R2 Source Guard failed: review tracked paths; no reset was made' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R43R2_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r43r2_reviewed_tracked_change_guard.repair
    if ($LASTEXITCODE -ne 0) { throw 'R43R2 repair failed' }
    Write-Output 'PHASE174_R3R7R43R2_TEST_GROUP=PATCH_CONTRACT'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r43r2_reviewed_tracked_change_guard/tests/test_guard.py
    if ($LASTEXITCODE -ne 0) { throw 'R43R2 patch-contract pytest failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r43r1_r3_sha_pin_fix\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R43R1 DryRun failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r43r1_r3_sha_pin_fix\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R43R1/R43 audit failed' }
    Write-Output 'PHASE174_R3R7R43R2_RUN=PASS'
    Write-Output 'PHASE174_R3R7R43R2_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```
