# Phase 171 R2A-R3 — Module execution path 修正（コード全文）

## 変更対象

- `phase171_r2a_prop56_alignment_audit/run.ps1`：PowerShell スクリプト全体を置換。`python -B -m phase171_r2a_prop56_alignment_audit.audit` で実行する。
- `phase171_r2a_prop56_alignment_audit/tests/test_audit.py`：既存24件維持、新規3件の回帰テストを末尾に追加（新規追加位置：既存の最終テスト関数の直後）。import に `os`, `subprocess`, `sys` を追加。
- `phase171_r2a_prop56_alignment_audit/README.md`：全文置換。
- `phase171_r2a_prop56_alignment_audit/監査仕様.md`：全文置換。

変更しないもの：`audit.py` 全体、既存 production、DB、既存の数理・出典検証規則。

## PowerShell 全文 — `run.ps1`

```powershell
param(
    [Parameter(Mandatory = $true)][string]$ReportPath,
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $RepoRoot
try {
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider '.\phase171_r2a_prop56_alignment_audit\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2A_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R2A_FOCUSED_PYTEST=PASS'
    $Arguments = @('-B', '-m', 'phase171_r2a_prop56_alignment_audit.audit', '--root', $RepoRoot, '--report', $ReportPath)
    if ($DryRun) { $Arguments += '--dry-run' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R2A_AUDIT_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R2A=PASS'
}
finally {
    Pop-Location
}

```

## Python テスト全文 — `tests/test_audit.py`（変更後の import を含む）

```python
"""Pure, focused regressions for read-only alignment audit helpers."""
from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

from phase171_r2a_prop56_alignment_audit.audit import (
    CASES,
    REVIEWED_AUDIT_DIRECTORIES,
    SOURCE_AUDIT_HEAD,
    git_state,
    inspect_case,
    short,
    typed_differences,
    validate_r1c_report,
)


@dataclass(frozen=True)
class Symbol:
    family: str
    index: int | None


@dataclass(frozen=True)
class Group:
    symbol: object
    order: int


def sample_report():
    ns = [2, 3, 4, 5, 6, 7] + list(range(9, 60, 2))
    assert len(ns) == 32
    rows = []
    for n in ns:
        rows.append({"n": n, "k": 3,
                     "result": "PROOF_UNFINISHED" if n in (3, 4, 5) else "COMPLETE_AND_WEB_VERIFIED",
                     "search_status": "search_failed" if n in (3, 4, 5) else "complete",
                     "proven_steps": 0 if n in (3, 4, 5) else 5})
    return {"phase": "171 R1C", "stem": 3, "dry_run": False,
            "result": "AUDIT_COMPLETE_WITH_GAPS", "tracked_unchanged": True,
            "preflight": {"head": "715b00d67d4b3ff4b34bf87229842d14960ea6bb"},
            "domain": [{"n": n, "k": 3} for n in ns], "rows": rows,
            "domain_checked": 32, "domain_complete": 29, "domain_gaps": 3,
            "worker_failures": 0}


def test_reviewed_audit_directories_are_narrowly_scoped():
    assert SOURCE_AUDIT_HEAD == "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
    assert REVIEWED_AUDIT_DIRECTORIES == (
        "phase171_r1_n3_registered_audit/",
        "phase171_r1c_k3_registered_audit/",
        "phase171_r1d_k3_three_gap_diagnostics/",
        "phase171_r2a_prop56_alignment_audit/",
    )


def test_exact_three_cases_only():
    assert CASES == ((3, "pi6_3_group_relation"),
                     (4, "pi7_4_group_relation"),
                     (5, "pi8_5_group_relation"))


def test_validate_r1c_accepts_expected_gaps():
    assert [row["n"] for row in validate_r1c_report(sample_report())] == [3, 4, 5]


@pytest.mark.parametrize("name,value", [
    ("stem", 2), ("dry_run", True), ("result", "DRY_RUN_PASS"),
    ("tracked_unchanged", False), ("worker_failures", 1),
    ("domain_complete", 28),
])
def test_validate_r1c_rejects_corrupted_metadata(name, value):
    report = sample_report()
    report[name] = value
    with pytest.raises(ValueError):
        validate_r1c_report(report)


def test_validate_r1c_rejects_duplicate_coordinates():
    report = sample_report()
    report["domain"][4]["n"] = 5
    with pytest.raises(ValueError):
        validate_r1c_report(report)


def test_validate_r1c_rejects_fabricated_complete():
    report = sample_report()
    report["rows"][1]["result"] = "COMPLETE_AND_WEB_VERIFIED"
    with pytest.raises(ValueError):
        validate_r1c_report(report)


def test_typed_differences_captures_nested_field_mismatch():
    a = Group(Symbol("\\nu'", None), 4)
    b = Group(Symbol("ν", 3), 4)
    diffs = typed_differences(a, b)
    assert {d["path"] for d in diffs} == {"goal.symbol.family", "goal.symbol.index"}
    assert all(d["kind"] in ("type", "value") for d in diffs)


def test_typed_differences_exact_match_is_empty():
    group = Group(Symbol("ν", 5), 8)
    assert typed_differences(group, group) == []


def test_typed_differences_refuses_type_alias():
    assert typed_differences(Group(Symbol("ν", 5), 8), ["ν", 5]) == [
        {"path": "goal", "kind": "type", "left": "Group", "right": "list"}
    ]


def test_typed_differences_records_sequence_length():
    assert typed_differences((1, 2), (1,)) == [
        {"path": "goal.length", "kind": "length", "left": 2, "right": 1}
    ]


def test_short_truncates_only_when_needed():
    assert short("ab", 10) == "'ab'"
    assert short("abcdefghij", 7).endswith(" [truncated]")


def test_inspect_case_reports_unverified_source_without_promotion():
    source = Group(Symbol("ν", 3), 4)
    target = Group(Symbol("\\nu'", None), 4)
    evidence = SimpleNamespace(statement=source, source_description="SOURCE_UNVERIFIED")
    assertion = SimpleNamespace(content=source, origin=SimpleNamespace(value="boundary"))
    bridge = SimpleNamespace(
        registry=SimpleNamespace(_assertions={
            "shared:0:boundary:Proposition 5.6:pi6_3_group_relation": assertion,
        }), proof_links=(),
    )
    case = inspect_case(
        bridge, {"pi6_3_group_relation": evidence}, 3, "pi6_3_group_relation",
        selector=lambda _bridge, *, n, k: (target,),
    )
    assert not case["exact_equal"]
    assert case["source_assertions"][0]["proof_link_count"] == 0
    assert len(case["differences"]) == 2


def _temporary_reviewed_git_repo(tmp_path: Path, monkeypatch):
    """Build a real miniature Git history with a matching remote tracking ref."""
    import subprocess
    import phase171_r2a_prop56_alignment_audit.audit as module

    def command(*arguments):
        outcome = subprocess.run(
            ["git", *arguments], cwd=tmp_path, capture_output=True,
            text=True, encoding="utf-8", check=True,
        )
        return outcome.stdout.strip()

    command("init", "-q")
    command("config", "user.email", "audit@example.invalid")
    command("config", "user.name", "Audit Test")
    command("branch", "-M", "develop")
    for path in module.EXPECTED_BLOBS:
        file_path = tmp_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("reviewed production source\n", encoding="utf-8")
    command("add", "--", ".")
    command("commit", "-qm", "reviewed baseline")
    baseline = command("rev-parse", "HEAD")
    monkeypatch.setattr(module, "SOURCE_AUDIT_HEAD", baseline)
    monkeypatch.setattr(module, "EXPECTED_BLOBS", {
        path: command("rev-parse", "HEAD:" + path)
        for path in module.EXPECTED_BLOBS
    })
    command("update-ref", "refs/remotes/origin/develop", baseline)
    return command


def test_git_state_accepts_audit_only_descendant(tmp_path, monkeypatch):
    command = _temporary_reviewed_git_repo(tmp_path, monkeypatch)
    directory = tmp_path / "phase171_r1d_k3_three_gap_diagnostics"
    directory.mkdir()
    (directory / "triage.py").write_text("read-only\n", encoding="utf-8")
    command("add", "--", "phase171_r1d_k3_three_gap_diagnostics")
    command("commit", "-qm", "add R1D audit only")
    command("update-ref", "refs/remotes/origin/develop", command("rev-parse", "HEAD"))

    state = git_state(tmp_path)
    assert state["branch"] == "develop"
    assert state["head"] == state["origin_develop"]
    assert state["committed_audit_changes"] == (
        "phase171_r1d_k3_three_gap_diagnostics/triage.py",
    )


def test_git_state_rejects_committed_production_change(tmp_path, monkeypatch):
    command = _temporary_reviewed_git_repo(tmp_path, monkeypatch)
    (tmp_path / "other_production.py").write_text("modified\n", encoding="utf-8")
    command("add", "--", "other_production.py")
    command("commit", "-qm", "unexpected production change")
    command("update-ref", "refs/remotes/origin/develop", command("rev-parse", "HEAD"))
    with pytest.raises(RuntimeError, match="unreviewed committed paths"):
        git_state(tmp_path)


def test_git_state_rejects_mismatched_origin_develop(tmp_path, monkeypatch):
    command = _temporary_reviewed_git_repo(tmp_path, monkeypatch)
    directory = tmp_path / "phase171_r1d_k3_three_gap_diagnostics"
    directory.mkdir()
    (directory / "README.md").write_text("audit\n", encoding="utf-8")
    command("add", "--", "phase171_r1d_k3_three_gap_diagnostics")
    command("commit", "-qm", "local audit commit")
    with pytest.raises(RuntimeError, match="unexpected HEAD/upstream"):
        git_state(tmp_path)


def test_git_state_rejects_uncommitted_tracked_edits(tmp_path, monkeypatch):
    _temporary_reviewed_git_repo(tmp_path, monkeypatch)
    (tmp_path / "web_group_proof.py").write_text("local change\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="tracked files changed"):
        git_state(tmp_path)


def test_git_state_rejects_modified_reviewed_source_blob(tmp_path, monkeypatch):
    command = _temporary_reviewed_git_repo(tmp_path, monkeypatch)
    # Re-checking the pinned blobs also guards a change to a critical file.
    module_path = tmp_path / "web_group_proof.py"
    module_path.write_text("different committed source\n", encoding="utf-8")
    command("add", "--", "web_group_proof.py")
    command("commit", "-qm", "unexpected source change")
    command("update-ref", "refs/remotes/origin/develop", command("rev-parse", "HEAD"))
    with pytest.raises(RuntimeError, match="unreviewed committed paths"):
        git_state(tmp_path)


def test_git_state_rejects_missing_reviewed_baseline(tmp_path, monkeypatch):
    _temporary_reviewed_git_repo(tmp_path, monkeypatch)
    import phase171_r2a_prop56_alignment_audit.audit as module
    monkeypatch.setattr(module, "SOURCE_AUDIT_HEAD", "f" * 40)
    with pytest.raises(RuntimeError, match="merge-base"):
        git_state(tmp_path)


def test_git_state_ignores_untracked_audit_output(tmp_path, monkeypatch):
    _temporary_reviewed_git_repo(tmp_path, monkeypatch)
    (tmp_path / "untracked_logs").mkdir()
    (tmp_path / "untracked_logs" / "readme.txt").write_text("audit output\n", encoding="utf-8")
    state = git_state(tmp_path)
    assert state["committed_audit_changes"] == ()


def test_powershell_invokes_audit_as_repo_root_module():
    """Regression: script-path execution cannot import sibling repository modules."""
    package_dir = Path(__file__).resolve().parents[1]
    script = (package_dir / "run.ps1").read_text(encoding="utf-8")
    assert "Push-Location $RepoRoot" in script
    assert "'-B', '-m', 'phase171_r2a_prop56_alignment_audit.audit'" in script
    assert "'.\\phase171_r2a_prop56_alignment_audit\\audit.py'" not in script


def test_repository_root_module_entrypoint_runs_in_subprocess():
    """Check the actual module entrypoint from outside the pytest import process."""
    root = Path(__file__).resolve().parents[2]
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "phase171_r2a_prop56_alignment_audit.audit", "--help"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "--report" in proc.stdout and "--root" in proc.stdout


def test_module_launch_can_import_repository_root_sibling(tmp_path):
    """Replicate the user's script-path import failure without using production modules."""
    package = tmp_path / "mini_audit"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "runner.py").write_text(
        "from sibling_at_repository_root import READY\nprint(READY)\n", encoding="utf-8"
    )
    (tmp_path / "sibling_at_repository_root.py").write_text(
        "READY = 'ROOT_IMPORT_OK'\n", encoding="utf-8"
    )
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    module_launch = subprocess.run(
        [sys.executable, "-B", "-m", "mini_audit.runner"], cwd=tmp_path,
        capture_output=True, text=True, check=False, env=environment,
    )
    assert module_launch.returncode == 0, module_launch.stderr
    assert module_launch.stdout.strip() == "ROOT_IMPORT_OK"
    path_launch = subprocess.run(
        [sys.executable, "-B", str(package / "runner.py")], cwd=tmp_path,
        capture_output=True, text=True, check=False, env=environment,
    )
    assert path_launch.returncode != 0
    assert "No module named 'sibling_at_repository_root'" in path_launch.stderr

```

## README.md 全文

# Phase 171 R2A — Read-only Proposition 5.6 alignment audit

This package compares the **actual typed** `sphere.csv`-derived group proof goals for `n=3,4,5; k=3` with the existing typed Toda Proposition 5.6 *candidates* in `phase165_r6_explicit_literature_inputs.py`. It inspects the matching assertions and linked proof steps in the shared registry. **It does not prove, register, adopt, or edit any mathematical statement.** A `SOURCE_UNVERIFIED` candidate is not an admissible proof leaf.

Preflight requires `develop` to match `origin/develop`, a clean tracked tree, and a history descending from the reviewed `715b00d6` baseline. Every committed path since that baseline must be inside the explicitly reviewed Phase 171 R1, R1C, R1D, or R2A audit directories; otherwise the audit refuses to proceed. The pinned production code/data blobs remain mandatory. In particular, the verified `912322af` R1D-only commit is accepted without hardcoding new commit IDs. The source R1C `audit.json` is validated against the complete 32-group result (29 complete and the three known gaps). Untracked Phase 171 audit folders do not prevent inspection.

Unzip the archive at the root of `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`, then run:

```powershell
$Audit = Join-Path $env:LOCALAPPDATA "EHPProofTracerRecovery\phase171_r1c_k3_20261029_061130_694213\audit.json"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2a_prop56_alignment_audit\run.ps1" -ReportPath $Audit -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2a_prop56_alignment_audit\run.ps1" -ReportPath $Audit
git status -sb
```

The PowerShell runner launches `python -B -m phase171_r2a_prop56_alignment_audit.audit` from the repository root, instead of executing `audit.py` by path. This preserves root-level module discovery for `phase165_r52_r9_shared_math.py` and other project imports. The DryRun mode does not exercise these imports, so the regression tests cover the module entrypoint and sibling-import behavior.

`alignment.json` and `alignment.md` are written only under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2a_prop56_*`. Send the `PHASE171_R2A_DETAIL` lines or the report to evaluate differences and source-link status before choosing the first mathematical implementation. Focused tests only; the full suite remains Phase-final.


## 監査仕様.md 全文

# Phase 171 R2A — 命題候補と型付き Goal の照合

## 現時点の証拠

Phase 171 R1C は $k=3$ の登録済み32群中29群の完成と Web 検証を記録した。R1D は $\pi_6^3$、$\pi_7^4$、$\pi_8^5$ において、登録済み Goal が存在するにもかかわらず、証明ステップが0で「一意の導出が見つからない」と記録した。

GitHub `develop` の `phase165_r6_explicit_literature_inputs.py` は Proposition 5.6 の候補を登録する。一方、`phase163_r4_r11_literature_registration.py` はこれを `SOURCE_UNVERIFIED`、`PROOF_ANCESTRY_NOT_CHECKED` として取り扱い、`proof_links` を増やさない。引用候補と検証済み数学的前提を混同しない。

## 今回の境界

- `phase171_r2a_prop56_alignment_audit/audit.py` と限定テストだけを追加する。
- 3群の DB Goal と Proposition 5.6 の候補について、クラス・フィールドの厳密一致と候補の ProofStep リンクを観測する。
- 生成元表記の相違を自動正規化しない。生成元系列名で例外を作らない。
- 文献を新規引用済みの数学的事実にしない。Proof Tree を捏造しない。
- `README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` は変更しない。
- 全体 pytest は Phase 171 の最後だけ実行する。

## 次段階

型付き差分とリンクの観測結果を確認してから、原典照合・共通の型付き生成元照合・不足推論規則のうち、どれが必要かを決定する。現在の未完成群を完成とみなさない。


## R2A-R2 HEAD 検査更新

Git HEAD を個別の固定値列挙では判定しない。`715b00d6` を祖先とし、そこから現行 HEAD までに変更されたパスが Phase 171 の R1、R1C、R1D、R2A の監査専用ディレクトリ内に限られることを確認する。`develop` と `origin/develop` の一致、tracked clean、既存の本体コードと `sphere.csv` の blob SHA-1 固定を維持する。基準報告 `audit.json` の HEAD と数学的照合の処理は変更しない。

## R2A-R3 実行経路の修正

PowerShell の `run.ps1` はリポジトリ直下から `python -B -m phase171_r2a_prop56_alignment_audit.audit` で起動する。ファイルパス実行では Python の import 起点が監査ディレクトリとなり、通常監査の `phase165_r52_r9_shared_math` import が失敗する。`-m` に切り替えることで、既存の数学的処理・出典検証・Git preflight を変更せずに解消する。DryRun だけでは検出できないため、subprocess による module entrypoint と sibling import の回帰テストを追加した。


## テスト・完了条件・Phase 境界

`python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider phase171_r2a_prop56_alignment_audit/tests/test_audit.py`：27 PASS。`run.ps1` の DryRun と通常監査が PASS し、`PHASE171_R2A_DETAIL` 3件、`PHASE171_R2A_TRACKED_UNCHANGED=True` が確認できれば R2A-R3 完了。次の R2B は命題・DB Goal の不一致と証明リンクを分析する段階で、今回は実装しない。Phase 最後以外は全体 pytest をしない。
