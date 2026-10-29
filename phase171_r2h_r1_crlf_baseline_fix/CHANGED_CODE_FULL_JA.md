# Phase 171 R2H-R1 — 変更コード全文と安全な実行手順

## 変更対象と変更範囲

- 既存 `phase171_r2h_prop22_cited_hopf/install.py`：`status()` 関数全体のみ。import 部変更なし。
- 既存 `phase171_r2h_prop22_cited_hopf/tests/test_install.py`：末尾に `_make_reviewed_git_fixture()` および5件のテストを追加。import 部は元の全文を保持。既存6件は変更なし。
- 新規 `phase171_r2h_r1_crlf_baseline_fix/` 以下：安全な修復処理、テスト、PowerShell、文書。
- 数学の production ファイル、R2G の同一性実装、Proposition 2.2 の出典・推論規則、正式 docs は今回一切変更しない。

修復後の旧 R2H ランナーが、その元の設計に従って `phase165_r52_r9_shared_math.py` の2関数を変更する。保存済みの Git HEAD の blob SHA と CRLF/LF 以外の内容一致を必須とする。


## 変更後：phase171_r2h_prop22_cited_hopf/install.py（全文）

```python
"""Guarded, idempotent R2H integration; no reset, checkout, or overwrite of edits."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha1
from pathlib import Path
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
BASE_BLOB_SHA = "97bd75c575200ff799e10c5d1f646bc804136580"
ANCHOR_SOURCE = "        sources = sources + (build_adopted_toda53_double_reference(production),)"
INSERT_SOURCE = (
    "        from phase171_r2h_prop22_cited_hopf.source import (\n"
    "            build_cited_prop22_right_reference,\n"
    "        )\n"
    "        sources = sources + (build_cited_prop22_right_reference(production),)"
)
ANCHOR_PROVIDER = "        options.extend(expand_hopf_image_relation(goal, tuple(available)))"
INSERT_PROVIDER = (
    "        from phase171_r2h_prop22_cited_hopf.source import (\n"
    "            expand_cited_prop22_right_formula,\n"
    "        )\n"
    "        options.extend(expand_cited_prop22_right_formula(goal, tuple(available)))"
)


def git(*arguments: str) -> str:
    process = subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("git inspection failed: " + process.stderr)
    return process.stdout.strip()


def git_blob(data: bytes) -> str:
    normalized = data.replace(b"\r\n", b"\n")
    return sha1(b"blob " + str(len(normalized)).encode() + b"\0" + normalized).hexdigest()


def patch_source(source: str) -> str:
    """Insert only the R2H source and expansion connections in existing functions."""
    eol = "\r\n" if "\r\n" in source else "\n"
    normalized = source.replace("\r\n", "\n")
    if (normalized.count(ANCHOR_SOURCE) != 1
            or normalized.count(ANCHOR_PROVIDER) != 1):
        raise ValueError("shared integration anchors changed or are ambiguous")
    for addition in (INSERT_SOURCE, INSERT_PROVIDER):
        if addition in normalized:
            raise ValueError("partial or duplicate R2H integration")
    normalized = normalized.replace(ANCHOR_SOURCE, ANCHOR_SOURCE + "\n" + INSERT_SOURCE)
    normalized = normalized.replace(ANCHOR_PROVIDER, ANCHOR_PROVIDER + "\n" + INSERT_PROVIDER)
    return normalized.replace("\n", eol)


def status() -> tuple[str, bytes, bytes]:
    """Allow only the reviewed HEAD file or its exact two-connection patch.

    The Git blob SHA covers original bytes.  CRLF versus LF conversion in a
    checkout must not be confused with an unreviewed source modification.
    """
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R2H must run on develop")
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    head_blob = git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py")
    if head_blob != BASE_BLOB_SHA:
        raise RuntimeError("HEAD shared_math blob differs from reviewed baseline")
    baseline_process = subprocess.run(
        ["git", "show", "HEAD:phase165_r52_r9_shared_math.py"],
        cwd=ROOT, capture_output=True, check=True,
    )
    baseline_bytes = baseline_process.stdout
    if sha1(b"blob " + str(len(baseline_bytes)).encode() + b"\0" + baseline_bytes).hexdigest() != BASE_BLOB_SHA:
        raise RuntimeError("Git HEAD shared_math blob content is inconsistent")

    current = TARGET.read_bytes()
    baseline_text = baseline_bytes.decode("utf-8")
    current_text = current.decode("utf-8")
    normalize = lambda value: value.replace("\r\n", "\n")
    if normalize(current_text) == normalize(baseline_text):
        updated = patch_source(current_text).encode("utf-8")
        return "NEEDS_PATCH", current, updated
    expected = patch_source(baseline_text)
    if normalize(current_text) == normalize(expected):
        return "ALREADY_APPLIED", current, current
    raise RuntimeError("shared_math contains unreviewed changes; refusing to overwrite")


def full_functions(source: str) -> dict[str, str]:
    """Extract the full post-change functions, never truncated diffs."""
    import ast
    tree = ast.parse(source)
    result = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in (
            "build_shared_typed_bridge", "shared_expansion_provider",
        ):
            result[node.name] = ast.get_source_segment(source, node)
    if set(result) != {"build_shared_typed_bridge", "shared_expansion_provider"}:
        raise ValueError("expected full shared functions missing")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "apply"))
    args = parser.parse_args()
    stage, before, after = status()
    print("PHASE171_R2H_PREFLIGHT=" + stage, flush=True)
    if args.mode == "check":
        print("PHASE171_R2H_RESULT=PASS_CHECK", flush=True)
        return 0
    if stage == "NEEDS_PATCH":
        dest_root = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
        dest = dest_root / ("phase171_r2h_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        dest.mkdir(parents=True, exist_ok=False)
        backup = dest / TARGET.name
        shutil.copy2(TARGET, backup)
        print("PHASE171_R2H_BACKUP=" + str(dest), flush=True)
        if TARGET.read_bytes() != before:
            raise RuntimeError("shared file changed during R2H preflight")
        TARGET.write_bytes(after)
        print("PHASE171_R2H_PATCHED=" + str(TARGET.relative_to(ROOT)), flush=True)
    checked = TARGET.read_text(encoding="utf-8")
    pieces = full_functions(checked)
    output = ROOT / "phase171_r2h_prop22_cited_hopf" / "output"
    output.mkdir(parents=True, exist_ok=True)
    for name, code in pieces.items():
        (output / (name + "_FULL.py")).write_text(code + "\n", encoding="utf-8")
    print("PHASE171_R2H_FUNCTIONS_FULL=" + str(output), flush=True)
    print("PHASE171_R2H_RESULT=PASS_APPLY", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 変更後：phase171_r2h_prop22_cited_hopf/tests/test_install.py（全文）

```python
"""Pure tests for the guarded R2H installer (without production modules)."""
from __future__ import annotations

from hashlib import sha1

import pytest

from phase171_r2h_prop22_cited_hopf.install import (
    ANCHOR_PROVIDER, ANCHOR_SOURCE, INSERT_PROVIDER, INSERT_SOURCE,
    full_functions, git_blob, patch_source,
)


BASE = ("def build_shared_typed_bridge():\n"
        "    if True:\n" + ANCHOR_SOURCE + "\n"
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n" + ANCHOR_PROVIDER + "\n")


def test_r2h_inserts_exactly_two_connections():
    patched = patch_source(BASE)
    assert patched.count(INSERT_SOURCE) == 1
    assert patched.count(INSERT_PROVIDER) == 1
    assert patched.index(ANCHOR_SOURCE) < patched.index(INSERT_SOURCE)


def test_r2h_preserves_crlf():
    patched = patch_source(BASE.replace("\n", "\r\n"))
    assert "\r\n" in patched
    assert patched.replace("\r\n", "\n") == patch_source(BASE)


def test_r2h_fails_closed_for_ambiguous_source_anchor():
    with pytest.raises(ValueError, match="anchors"):
        patch_source(BASE + ANCHOR_SOURCE)


def test_r2h_fails_closed_for_partial_integration():
    with pytest.raises(ValueError, match="partial"):
        patch_source(BASE.replace(ANCHOR_SOURCE, ANCHOR_SOURCE + "\n" + INSERT_SOURCE))


def test_r2h_extracts_two_whole_functions():
    functions = full_functions(patch_source(BASE))
    assert set(functions) == {"build_shared_typed_bridge", "shared_expansion_provider"}
    assert INSERT_SOURCE in functions["build_shared_typed_bridge"]
    assert INSERT_PROVIDER in functions["shared_expansion_provider"]


def test_git_blob_matches_standard_blob_calculation():
    data = b"hello\n"
    expected = sha1(b"blob 6\0hello\n").hexdigest()
    assert git_blob(data) == expected
    assert git_blob(b"hello\r\n") == expected

def _make_reviewed_git_fixture(tmp_path, monkeypatch, *, line_ending="\r\n"):
    """Create a real isolated Git repo, never touching the project worktree."""
    import subprocess
    from pathlib import Path

    import phase171_r2h_prop22_cited_hopf.install as installer

    def command(*args):
        output = subprocess.run(
            ["git", *args], cwd=tmp_path, capture_output=True,
            check=True, text=True, encoding="utf-8",
        )
        return output.stdout.strip()

    command("init", "-q")
    command("config", "user.email", "phase171@example.invalid")
    command("config", "user.name", "Phase171 Test")
    command("branch", "-M", "develop")
    target = tmp_path / "phase165_r52_r9_shared_math.py"
    committed_text = BASE.replace("\n", line_ending)
    target.write_bytes(committed_text.encode("utf-8"))
    command("add", "--", target.name)
    command("commit", "-qm", "reviewed baseline")
    monkeypatch.setattr(installer, "ROOT", tmp_path)
    monkeypatch.setattr(installer, "TARGET", target)
    monkeypatch.setattr(
        installer, "BASE_BLOB_SHA",
        command("rev-parse", "HEAD:" + target.name),
    )
    return installer, target, committed_text, command


def test_status_accepts_unchanged_crlf_git_blob(tmp_path, monkeypatch):
    installer, target, original, command = _make_reviewed_git_fixture(
        tmp_path, monkeypatch,
    )
    stage, before, after = installer.status()
    assert stage == "NEEDS_PATCH"
    assert before == original.encode("utf-8")
    assert after.decode("utf-8") == installer.patch_source(original)
    assert target.read_bytes() == before
    assert command("status", "--porcelain") == ""


def test_status_accepts_lf_worktree_from_crlf_commit(tmp_path, monkeypatch):
    installer, target, original, _ = _make_reviewed_git_fixture(
        tmp_path, monkeypatch,
    )
    # Reproduce a checkout whose text uses different line endings from Git.
    target.write_bytes(original.replace("\r\n", "\n").encode("utf-8"))
    stage, before, after = installer.status()
    assert stage == "NEEDS_PATCH"
    assert b"\r\n" not in after
    assert after != before


def test_status_recognizes_exact_patch_on_crlf_baseline(tmp_path, monkeypatch):
    installer, target, original, _ = _make_reviewed_git_fixture(
        tmp_path, monkeypatch,
    )
    target.write_bytes(installer.patch_source(original).encode("utf-8"))
    stage, before, after = installer.status()
    assert stage == "ALREADY_APPLIED"
    assert before == after == target.read_bytes()


def test_status_rejects_unreviewed_worktree_content(tmp_path, monkeypatch):
    installer, target, original, _ = _make_reviewed_git_fixture(
        tmp_path, monkeypatch,
    )
    edited = original.replace("def shared_expansion_provider():", "def intruder():")
    target.write_bytes(edited.encode("utf-8"))
    with pytest.raises(RuntimeError, match="unreviewed changes"):
        installer.status()
    assert target.read_bytes() == edited.encode("utf-8")


def test_status_rejects_unreviewed_committed_blob(tmp_path, monkeypatch):
    installer, target, original, command = _make_reviewed_git_fixture(
        tmp_path, monkeypatch,
    )
    target.write_bytes((original + "# new change\r\n").encode("utf-8"))
    command("add", "--", target.name)
    command("commit", "-qm", "unreviewed production change")
    with pytest.raises(RuntimeError, match="reviewed baseline"):
        installer.status()
```

## 新規：phase171_r2h_r1_crlf_baseline_fix/repair.py

```python
"""Guarded repair of the R2H installer's CRLF/LF preflight comparison.

This repairs only files from the previously distributed R2H folder. It does
not modify tracked application source, Git history, or unrelated worktrees.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
FILES = (
    (
        "phase171_r2h_prop22_cited_hopf/install.py",
        "install_FULL.py",
        "0d370f801fb9528cd3a05f522d32a8803bbe8822874ccfe34afd5a48f6c8c8b6",
        "988ae78111f85f179eb4bf1104e786ab3e4dc0bacbb5080e6a22e14910a65ec4",
    ),
    (
        "phase171_r2h_prop22_cited_hopf/tests/test_install.py",
        "test_install_FULL.py",
        "c9826bf3d94a34e9be55115ee05877c3d26cfebdb37db681e5c8210e7b4fe058",
        "b14049db4c23886a70df1195adc992bcbc10afc732250f6488acd3e825df5508",
    ),
)


def inspect() -> tuple[tuple[str, Path, bytes, bytes], ...]:
    """Return only independently hash-validated, recognized file states."""
    verified = []
    for relative, payload, original_sha, patched_sha in FILES:
        target = ROOT / relative
        replacement = PACKAGE / payload
        if not target.is_file() or not replacement.is_file():
            raise FileNotFoundError(relative + " or " + payload)
        current = target.read_bytes()
        new_data = replacement.read_bytes()
        if sha256(new_data).hexdigest() != patched_sha:
            raise RuntimeError("repair payload hash mismatch: " + relative)
        actual = sha256(current).hexdigest()
        if actual == original_sha:
            state = "NEEDS_REPAIR"
        elif actual == patched_sha:
            state = "ALREADY_REPAIRED"
        else:
            raise RuntimeError("unreviewed R2H installer content: " + relative)
        verified.append((state, target, current, new_data))
    return tuple(verified)


def run(mode: str) -> int:
    """Read-only check or backed-up, strictly scoped replacement."""
    if mode not in ("check", "apply"):
        raise ValueError("mode must be check or apply")
    items = inspect()
    for state, target, _, _ in items:
        print("PHASE171_R2H_R1_PREFLIGHT=" + str(target.relative_to(ROOT)) + ":" + state, flush=True)
    if mode == "check":
        print("PHASE171_R2H_R1_RESULT=PASS_CHECK", flush=True)
        return 0
    pending = tuple(item for item in items if item[0] == "NEEDS_REPAIR")
    if pending:
        root = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
        backup_root = root / ("phase171_r2h_r1_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        backup_root.mkdir(parents=True, exist_ok=False)
        for _, target, original, _ in pending:
            destination = backup_root / target.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, destination)
            if destination.read_bytes() != original:
                raise RuntimeError("backup verification failed: " + str(target))
        print("PHASE171_R2H_R1_BACKUP=" + str(backup_root), flush=True)
        for _, target, original, new_data in pending:
            if target.read_bytes() != original:
                raise RuntimeError("installer file changed after backup: " + str(target))
            target.write_bytes(new_data)
            if target.read_bytes() != new_data:
                raise RuntimeError("installer repair write verification failed: " + str(target))
            print("PHASE171_R2H_R1_PATCHED=" + str(target.relative_to(ROOT)), flush=True)
    checked = inspect()
    if any(state != "ALREADY_REPAIRED" for state, _, _, _ in checked):
        raise RuntimeError("R2H installer repair did not reach the expected state")
    print("PHASE171_R2H_R1_RESULT=PASS_APPLY", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "apply"))
    args = parser.parse_args()
    try:
        return run(args.mode)
    except (RuntimeError, ValueError, OSError) as exc:
        print("PHASE171_R2H_R1_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    sys.exit(main())
```

## 新規：phase171_r2h_r1_crlf_baseline_fix/run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $RepoRoot
try {
    & python -B -m phase171_r2h_r1_crlf_baseline_fix.repair check
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_R1_PREFLIGHT_FAILED' }
    if ($DryRun.IsPresent) {
        Write-Host 'PHASE171_R2H_R1_RESULT=PASS_DRY_RUN'
        return
    }
    & python -B -m phase171_r2h_r1_crlf_baseline_fix.repair apply
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_R1_REPAIR_FAILED' }
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider 'phase171_r2h_r1_crlf_baseline_fix/tests/test_repair.py'
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_R1_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R2H_R1_FOCUSED_PYTEST=PASS'
    & powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r2h_prop22_cited_hopf\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_R1_REPAIRED_PREFLIGHT_FAILED' }
    & powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r2h_prop22_cited_hopf\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_R1_ORIGINAL_RUN_FAILED' }
    Write-Host 'PHASE171_R2H_R1_RESULT=PASS'
}
finally { Pop-Location }
```

## 新規：phase171_r2h_r1_crlf_baseline_fix/tests/test_repair.py

```python
"""Focused guards for the non-destructive R2H R1 package repair."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from phase171_r2h_r1_crlf_baseline_fix import repair


def _test_installation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    fixture_files = {
        "install.py": "baseline_install.py.txt",
        "test_install.py": "baseline_test_install.py.txt",
    }
    for relative, _, original_hash, _ in repair.FILES:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        source = Path(__file__).resolve().parents[1] / fixture_files[target.name]
        payload = source.read_bytes()
        assert sha256(payload).hexdigest() == original_hash
        target.write_bytes(payload)



def test_read_only_check_keeps_original_bytes(tmp_path: Path, monkeypatch) -> None:
    _test_installation(tmp_path, monkeypatch)
    before = [(tmp_path / path).read_bytes() for path, _, _, _ in repair.FILES]
    assert repair.run("check") == 0
    assert before == [(tmp_path / path).read_bytes() for path, _, _, _ in repair.FILES]


def test_guarded_repair_creates_backup_and_is_idempotent(tmp_path: Path, monkeypatch) -> None:
    _test_installation(tmp_path, monkeypatch)
    recovery = tmp_path / "recovery"
    monkeypatch.setenv("LOCALAPPDATA", str(recovery))
    assert repair.run("apply") == 0
    for relative, _, _, patched_hash in repair.FILES:
        assert sha256((tmp_path / relative).read_bytes()).hexdigest() == patched_hash
    assert len(list((recovery / "EHPProofTracerRecovery").glob("phase171_r2h_r1_*"))) == 1
    assert repair.run("apply") == 0
    assert len(list((recovery / "EHPProofTracerRecovery").glob("phase171_r2h_r1_*"))) == 1


def test_rejects_modified_installer_without_writing(tmp_path: Path, monkeypatch) -> None:
    _test_installation(tmp_path, monkeypatch)
    path = tmp_path / repair.FILES[0][0]
    path.write_bytes(path.read_bytes() + b"\n# unreviewed\n")
    before = path.read_bytes()
    with pytest.raises(RuntimeError, match="unreviewed"):
        repair.inspect()
    assert path.read_bytes() == before


def test_rejects_unrecognized_payload_hash(tmp_path: Path, monkeypatch) -> None:
    _test_installation(tmp_path, monkeypatch)
    original = repair.FILES
    item = original[0]
    monkeypatch.setattr(repair, "FILES", ((item[0], item[1], item[2], "0" * 64),))
    with pytest.raises(RuntimeError, match="payload hash"):
        repair.inspect()
```

## 新規：README.md（全文・英語）

```markdown
# Phase 171 R2H-R1 — CRLF-aware installer preflight repair

This narrowly scoped repair fixes a false "unreviewed changes" rejection in the previously distributed Phase 171 R2H installer. The reviewed Git blob `phase165_r52_r9_shared_math.py` contains CRLF line endings, while the old installer normalized CRLF to LF **before comparing its hash with the original Git blob SHA**. Unmodified files were therefore rejected.

The repaired `status()` method verifies the precise committed Git blob SHA, reads the HEAD blob bytes, and compares checkout text after *only* CRLF/LF normalization. Both a legitimate unmodified checkout and the **exactly** expected R2H patch are accepted; arbitrary file edits and unexpected committed baselines are still rejected. The existing R2H package's mathematical code, citation verification, inference rules, and tests apart from the installer's specific regression tests remain unchanged.

## Scope

The guarded repair changes only:

- `phase171_r2h_prop22_cited_hopf/install.py`: complete `status()` function, with unchanged imports and other functions.
- `phase171_r2h_prop22_cited_hopf/tests/test_install.py`: five additional complete regression tests and one test fixture, appended after existing tests. Existing tests and imports are preserved.

This repair package also provides `repair.py`, `run.ps1`, self-contained baseline fixtures, and its own focused tests. No repository-wide test suite or history-changing Git command is used.

## Execute from the repository root in PowerShell

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2H_R1_CRLF_FIX.zip" -DestinationPath "."
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2h_r1_crlf_baseline_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2h_r1_crlf_baseline_fix\run.ps1"
git status -sb
git diff --stat
```

The DryRun is strictly read-only. The real run first verifies exact SHA-256 hashes of the original R2H installer/test, saves copies under `%LOCALAPPDATA%\EHPProofTracerRecovery`, and applies the repair. It then runs repair-focused pytest, the original R2H DryRun, and the original R2H runner with its focused pytest and mathematical proof audit.

R2H succeeds only if the previous package's cited Proposition 2.2 two-inference Proof Tree passes. It does **not** establish the group structure of `pi_6^3`, and it does not use an unrelated Proposition 5.6 result as a given.
```

## 新規：監査仕様.md（全文・日本語）

```markdown
# Phase 171 R2H-R1 — 改行差によるインストーラー誤判定の修復

## 事実と原因

現行の GitHub `develop` にある `phase165_r52_r9_shared_math.py` の Git blob SHA は `97bd75c575200ff799e10c5d1f646bc804136580` で、公開ファイルに CRLF 改行が含まれる。旧 `status()` は作業ファイルをハッシュ計算前に LF に置き換え、Git が計算する生バイト列の SHA と比較した。そのため、未変更の HEAD に対しても `shared_math contains unreviewed changes` と誤判定した。

## 変更対象

- 旧 R2H フォルダの `install.py` 内の `status()` 全体を置換。既存 import・その他の関数は変更しない。
- 旧 R2H フォルダの `tests/test_install.py` 末尾に隔離した Git リポジトリの試験用関数と、CRLF 未変更・LF ワークツリー・適用済み・未知の変更・未知の HEAD を検証する5テストを追加。既存テストと import は維持する。
- 新規修復パッケージに `repair.py`、`run.ps1`、限定テスト、元ファイルの内容を固定した試験フィクスチャを同梱する。

## 保護条件

`repair.py` は修正前と修正後の SHA-256 を厳密に区別し、それ以外なら停止する。追跡対象のアプリケーションファイルはこの段階では変更しない。バックアップはリポジトリ外に保存する。修正後の R2H `status()` は Git HEAD の blob ID と実際の `git show` 出力との整合性を検証し、改行コード以外の変更を認めない。Git checkout/reset は実施しない。

## テスト

修正前の追加テストは CRLF 関連2件が失敗。修正後の旧 R2H インストーラー単体テスト11件と修復処理単体テスト4件が PASS。実際のアプリケーションを用いる限定 pytest と出典付き推論監査は、利用者の PowerShell 実行で確認する。全体 pytest は Phase 171 終了時のみ実行する。

## 完了条件と次段階

`PHASE171_R2H_R1_RESULT=PASS` に加え、元の R2H が `PHASE171_R2H_RESULT=PASS` を表示し、Proposition 2.2 と (5.3) に基づく2段の `INFERENCE` が成立すること。π₆³ の群構造・位数・生成性は未証明のまま保持し、以後の Phase 171 で扱う。
```

## 実行 pytest と Phase 境界

修復処理の限定テスト：`python -B -m pytest -q -p no:cacheprovider phase171_r2h_r1_crlf_baseline_fix/tests/test_repair.py`。元 R2H は `run.ps1` の限定テストと出典付き Proof Tree 監査を実行する。全体 pytest は Phase 171 終了時のみ。

π₆³ の位数4、生成性、η₆=Eη₅ の置換、EHP 拡張の完成証明は次段階に残す。
