# Phase 171 R2B-R2 — Git ahead-only guard 修正（コード全文）

## 変更対象（先頭一覧）

- `phase171_r2b_prop56_source_dependency_audit/audit.py`：定数は変更なし。既存関数 `tracked_state()` 全体を置換。
- `phase171_r2b_prop56_source_dependency_audit/tests/test_audit.py`：`subprocess` の import を追加。既存テスト `test_git_guard_allows_only_reviewed_paths()` と `test_git_guard_rejects_unsynced_upstream()`（改名して `test_git_guard_rejects_diverged_upstream()`）を変更。`setup_temporary_git_repository()` を `test_git_guard_rejects_tracked_working_diff()` の後に追加。新規テスト4件を追加。
- `phase171_r2b_prop56_source_dependency_audit/README.md`：全文置換（英語）。
- `phase171_r2b_prop56_source_dependency_audit/監査仕様.md`：全文置換（日本語）。
- `run.ps1`、既存のアプリ・DB・数学ソース・Proof Search・Renderer・正式文書は変更なし。

今回の修正は Git 検査だけです。ローカルの `develop` が `origin/develop` の子孫で、先行コミットの変更先が許可済み監査用ディレクトリだけの場合に限り監査を続行します。逆向きの behind / diverged、追跡済み差分、既知の production blob 変更を許可しません。

## audit.py の import 全文（変更なし、監査用に掲載）

```python
"""Phase 171 R2B: inspect existing Proposition 5.6 source proof, never certify it."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback
```

## audit.py の置換関数 `tracked_state()` 全文

```python
def tracked_state(root: Path) -> dict:
    """Allow audit-only local commits ahead of origin; refuse unrelated changes.

    Both the reviewed baseline and origin/develop must be ancestors of HEAD.
    Differences from either anchor must be confined to reviewed audit paths.
    The working tree and pinned production Git blobs must remain unchanged.
    """
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    upstream_ref = "refs/remotes/origin/develop"
    upstream = git(root, "rev-parse", "--verify", upstream_ref)
    if branch != "develop":
        raise RuntimeError("expected develop branch")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked working tree is not clean")
    git(root, "merge-base", "--is-ancestor", BASELINE, "HEAD")
    try:
        git(root, "merge-base", "--is-ancestor", upstream_ref, "HEAD")
    except RuntimeError as exc:
        raise RuntimeError(
            "origin/develop is not an ancestor of local HEAD; "
            "refuse behind or diverged histories"
        ) from exc
    changed = git(root, "diff", "--name-only", "-z", BASELINE, "HEAD")
    paths = tuple(path for path in changed.split("\0") if path)
    local_changed = git(
        root, "diff", "--name-only", "-z", upstream_ref, "HEAD"
    )
    local_paths = tuple(path for path in local_changed.split("\0") if path)
    unreviewed = tuple(path for path in dict.fromkeys(paths + local_paths)
                       if not any(path.startswith(prefix)
                                  for prefix in REVIEWED_DIRECTORIES))
    if unreviewed:
        raise RuntimeError("unreviewed committed files: " + ", ".join(unreviewed))
    for path, digest in EXPECTED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path) != digest:
            raise RuntimeError("source blob has changed: " + path)
    diff = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"], cwd=root,
        capture_output=True, check=False,
    )
    if diff.returncode:
        raise RuntimeError("cannot calculate tracked binary diff")
    return {
        "branch": branch,
        "head": head,
        "origin_develop": upstream,
        "baseline": BASELINE,
        "reviewed_changes": paths,
        "local_ahead_audit_changes": local_paths,
        "tracked_diff_sha256": sha256(diff.stdout).hexdigest(),
    }
```

## tests/test_audit.py の import 全文

```python
"""Tests for source parsing, typed mismatch evidence and the Git safety boundary."""
from __future__ import annotations

from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest

from phase171_r2b_prop56_source_dependency_audit import audit
```

## tests/test_audit.py の全コード

新規テストの追加位置：既存の `test_git_guard_rejects_tracked_working_diff()` と `test_run_script_uses_python_module_launch()` の間（ヘルパーは同範囲の先頭）。各テスト関数は以下の全ファイルに含まれています。

```python
"""Tests for source parsing, typed mismatch evidence and the Git safety boundary."""
from __future__ import annotations

from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest

from phase171_r2b_prop56_source_dependency_audit import audit


def example_cases() -> list[dict]:
    cases = []
    for n, key in audit.CASES:
        cases.append({
            "n": n, "k": 3, "key": key,
            "goal_count": 1, "exact_equal": False,
            "differences": [{"path": "goal.rhs.generator.name", "kind": "value"}],
            "source_assertions": [{
                "assertion_id": "shared:0:boundary:Proposition 5.6:" + key,
                "origin": "fixed_statement", "proof_link_count": 0,
                "linked_step_count": 0,
            }],
        })
    return cases


def example_alignment() -> dict:
    return {
        "phase": "171 R2A", "mode": "READ_ONLY_TYPED_ALIGNMENT",
        "read_only": True, "source_head": audit.BASELINE,
        "cases": example_cases(),
    }


def example_source() -> str:
    return (
        "Header\n"
        r"\begin{proposition}\label{prop:5.6}" + "\n"
        r"\(\pi^{3}_{6}=\gen{\nu'}\cong \mathbb Z_{4}\)" + "\n"
        r"\(\pi^{4}_{7}=\gen{\nu_{4}}\oplus\gen{E\nu'}\)" + "\n"
        r"\(\pi^{n}_{n+3}=\gen{\nu_{n}}\cong\mathbb Z_8 (n\ge5)\)" + "\n"
        r"\end{proposition}" + "\n"
        r"\textbf{Proof.} (5.2), Prop 5.3, (4.4), (5.6)? "
        r"(4.8), (5.5), (4.5) \qed" + "\n"
        r"\paragraph*{iv). The next section}" + "\n"
    )


def test_validate_alignment_accepts_three_exact_gaps():
    cases = audit.validate_alignment(example_alignment())
    assert tuple(item["n"] for item in cases) == (3, 4, 5)


def test_validate_alignment_rejects_wrong_phase():
    report = example_alignment()
    report["phase"] = "171 R1D"
    with pytest.raises(ValueError, match="R2A"):
        audit.validate_alignment(report)


def test_validate_alignment_rejects_unverified_scope():
    report = example_alignment()
    report["read_only"] = False
    with pytest.raises(ValueError, match="read-only"):
        audit.validate_alignment(report)


def test_validate_alignment_rejects_wrong_source_head():
    report = example_alignment()
    report["source_head"] = "wrong"
    with pytest.raises(ValueError, match="commit"):
        audit.validate_alignment(report)


def test_validate_alignment_rejects_extra_case():
    report = example_alignment()
    report["cases"].append(dict(report["cases"][0]))
    with pytest.raises(ValueError, match="exactly three"):
        audit.validate_alignment(report)


def test_validate_alignment_rejects_proof_link():
    report = example_alignment()
    report["cases"][1]["source_assertions"][0]["proof_link_count"] = 1
    with pytest.raises(ValueError, match="proof-link"):
        audit.validate_alignment(report)


def test_validate_alignment_rejects_false_claim_of_equal_types():
    report = example_alignment()
    report["cases"][0]["exact_equal"] = True
    with pytest.raises(ValueError, match="already aligned"):
        audit.validate_alignment(report)


def test_source_sections_extracts_original_proposition_and_proof():
    result = audit.source_sections(example_source())
    assert r"\pi^{3}_{6}" in result["theorem"]
    assert r"\textbf{Proof.}" in result["proof"]
    assert result["theorem_start_line"] == 2
    assert result["has_question_marker"] is True
    assert "(5.2)" in result["references_in_proof"]
    assert "(4.5)" in result["references_in_proof"]


def test_source_sections_rejects_missing_proposition():
    with pytest.raises(ValueError, match="uniquely"):
        audit.source_sections("no proposition")


def test_source_sections_rejects_duplicate_proposition():
    with pytest.raises(ValueError, match="uniquely"):
        audit.source_sections(example_source() + example_source())


def test_source_sections_rejects_missing_theorem_marker():
    source = example_source().replace(r"\gen{\nu_{4}}", r"\gen{x}")
    with pytest.raises(ValueError, match="n=4"):
        audit.source_sections(source)


def test_source_sections_rejects_proof_without_qed():
    source = example_source().replace(r"\qed", "not yet")
    with pytest.raises(ValueError, match="incomplete"):
        audit.source_sections(source)


def test_source_sections_rejects_missing_next_section():
    source = example_source().replace(r"\paragraph*{iv).", "No section")
    with pytest.raises(ValueError, match="boundary"):
        audit.source_sections(source)


def test_classification_does_not_normalize_discrepant_symbols():
    case = example_cases()[0]
    case["differences"] = [
        {"path": "goal.rhs.generator.name", "kind": "value"},
        {"path": "goal.rhs.generator.source", "kind": "type"},
        {"path": "goal.rhs.generator.generator.family", "kind": "value"},
    ]
    item = audit.classify_case(case, audit.source_sections(example_source()))
    assert item["typed_difference_kinds"] == [
        "GENERATOR_DISPLAY_NAME", "GENERATOR_DOMAIN_CODOMAIN",
        "GENERATOR_SYMBOL_IDENTITY",
    ]
    assert item["blockers"] == ("TYPED_GOAL_MISMATCH", "NO_VERIFIED_PROOF_LINK")
    assert item["proof_link_count"] == 0


def test_classification_detects_iterated_suspension_type():
    case = example_cases()[1]
    case["differences"] = [{"path": "goal.rhs.summands[1].generator", "kind": "type"}]
    item = audit.classify_case(case, audit.source_sections(example_source()))
    assert item["typed_difference_kinds"] == ["GENERATOR_EXPRESSION_TYPE"]


def test_markdown_includes_original_text_and_boundary():
    source = audit.source_sections(example_source())
    items = [audit.classify_case(x, source) for x in example_cases()]
    output = audit.markdown_report({"cases": items, "source": source})
    assert "π_6^3" in output
    assert "π_7^4" in output
    assert "π_8^5" in output
    assert r"\begin{proposition}" in output
    assert "GIVEN" in output


def test_git_guard_allows_only_reviewed_paths(monkeypatch, tmp_path):
    expected = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "commit",
        ("rev-parse", "--verify", "refs/remotes/origin/develop"): "commit",
        ("status", "--porcelain", "--untracked-files=no"): "",
        ("merge-base", "--is-ancestor", audit.BASELINE, "HEAD"): "",
        ("merge-base", "--is-ancestor", "refs/remotes/origin/develop", "HEAD"): "",
        ("diff", "--name-only", "-z", audit.BASELINE, "HEAD"): "phase171_r1d_k3_three_gap_diagnostics/triage.py\0",
        ("diff", "--name-only", "-z", "refs/remotes/origin/develop", "HEAD"): "",
    }
    for path, blob in audit.EXPECTED_BLOBS.items():
        expected[("rev-parse", "HEAD:" + path)] = blob
    monkeypatch.setattr(audit, "git", lambda root, *args: expected[args])
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=b""))
    result = audit.tracked_state(tmp_path)
    assert result["head"] == "commit"
    assert result["reviewed_changes"] == ("phase171_r1d_k3_three_gap_diagnostics/triage.py",)


def test_git_guard_rejects_changed_production(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("status", "--porcelain", "--untracked-files=no"):
            return ""
        if args == ("diff", "--name-only", "-z", audit.BASELINE, "HEAD"):
            return "phase165_r52_r9_shared_math.py\0"
        return "commit"
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="unreviewed committed files"):
        audit.tracked_state(tmp_path)


def test_git_guard_rejects_diverged_upstream(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "local"
        if args == ("rev-parse", "--verify", "refs/remotes/origin/develop"):
            return "remote"
        if args == ("merge-base", "--is-ancestor", "refs/remotes/origin/develop", "HEAD"):
            raise RuntimeError("git reports remote not ancestor")
        return ""
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="not an ancestor"):
        audit.tracked_state(tmp_path)


def test_git_guard_rejects_tracked_working_diff(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "commit"
        if args == ("rev-parse", "--verify", "refs/remotes/origin/develop"):
            return "commit"
        return " M phase165_r52_r9_shared_math.py"
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="not clean"):
        audit.tracked_state(tmp_path)




def setup_temporary_git_repository(monkeypatch, tmp_path):
    """Build an isolated fixture with a tracking ref, not an application checkout."""
    def command(*arguments):
        finished = subprocess.run(
            ["git", *arguments], cwd=tmp_path, capture_output=True,
            text=True, check=True,
        )
        return finished.stdout.strip()

    command("init", "-q")
    command("config", "user.name", "Audit Test")
    command("config", "user.email", "audit@example.invalid")
    source = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    source.parent.mkdir(parents=True)
    source.write_text("reviewed source fixture\n", encoding="utf-8")
    command("add", "--", "sources/toda/Toda_05_2.tex")
    command("commit", "-q", "-m", "baseline")
    command("branch", "-M", "develop")
    base = command("rev-parse", "HEAD")
    command("update-ref", "refs/remotes/origin/develop", base)
    blob = command("rev-parse", "HEAD:sources/toda/Toda_05_2.tex")
    monkeypatch.setattr(audit, "BASELINE", base)
    monkeypatch.setattr(
        audit, "EXPECTED_BLOBS", {"sources/toda/Toda_05_2.tex": blob}
    )
    return command, base


def test_git_guard_accepts_audit_only_local_ahead_commit(monkeypatch, tmp_path):
    command, remote = setup_temporary_git_repository(monkeypatch, tmp_path)
    package = tmp_path / "phase171_r2a_prop56_alignment_audit"
    package.mkdir()
    (package / "README.md").write_text("audit only\n", encoding="utf-8")
    command("add", "--", "phase171_r2a_prop56_alignment_audit/README.md")
    command("commit", "-q", "-m", "local audit only")
    assert command("rev-parse", "HEAD") != remote
    state = audit.tracked_state(tmp_path)
    assert state["origin_develop"] == remote
    assert state["head"] == command("rev-parse", "HEAD")
    assert state["local_ahead_audit_changes"] == (
        "phase171_r2a_prop56_alignment_audit/README.md",
    )


def test_git_guard_rejects_ahead_unreviewed_source_commit(monkeypatch, tmp_path):
    command, remote = setup_temporary_git_repository(monkeypatch, tmp_path)
    package = tmp_path / "phase171_r2a_prop56_alignment_audit"
    package.mkdir()
    (package / "README.md").write_text("audit only\n", encoding="utf-8")
    source = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    source.write_text("unreviewed source edit\n", encoding="utf-8")
    command("add", "--", "phase171_r2a_prop56_alignment_audit/README.md", "sources/toda/Toda_05_2.tex")
    command("commit", "-q", "-m", "not audit only")
    assert command("rev-parse", "HEAD") != remote
    with pytest.raises(RuntimeError, match="unreviewed committed files"):
        audit.tracked_state(tmp_path)


def test_git_guard_rejects_remote_ahead_of_local(monkeypatch, tmp_path):
    command, base = setup_temporary_git_repository(monkeypatch, tmp_path)
    package = tmp_path / "phase171_r1d_k3_three_gap_diagnostics"
    package.mkdir()
    (package / "README.md").write_text("remote audit\n", encoding="utf-8")
    command("add", "--", "phase171_r1d_k3_three_gap_diagnostics/README.md")
    command("commit", "-q", "-m", "remote audited commit")
    remote = command("rev-parse", "HEAD")
    command("update-ref", "refs/remotes/origin/develop", remote)
    command("reset", "--hard", base)
    with pytest.raises(RuntimeError, match="not an ancestor"):
        audit.tracked_state(tmp_path)


def test_git_guard_rejects_ahead_commit_with_wrong_pinned_blob(monkeypatch, tmp_path):
    command, remote = setup_temporary_git_repository(monkeypatch, tmp_path)
    package = tmp_path / "phase171_r2a_prop56_alignment_audit"
    package.mkdir()
    (package / "README.md").write_text("audit only\n", encoding="utf-8")
    command("add", "--", "phase171_r2a_prop56_alignment_audit/README.md")
    command("commit", "-q", "-m", "local audit only")
    assert command("rev-parse", "HEAD") != remote
    monkeypatch.setattr(
        audit, "EXPECTED_BLOBS", {"sources/toda/Toda_05_2.tex": "different"}
    )
    with pytest.raises(RuntimeError, match="source blob has changed"):
        audit.tracked_state(tmp_path)

def test_run_script_uses_python_module_launch():
    script = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8")
    assert "phase171_r2b_prop56_source_dependency_audit.audit" in script
    assert "'--root'" in script
    assert "-m" in script


def test_blob_pin_covers_source_tex():
    assert "sources/toda/Toda_05_2.tex" in audit.EXPECTED_BLOBS
    assert "phase165_r52_r9_shared_math.py" in audit.EXPECTED_BLOBS
```

## run.ps1 全文（変更なし）

```powershell
param(
    [Parameter(Mandatory = $true)]
    [string] $ReportPath,
    [switch] $DryRun
)
$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path (Join-Path $packageRoot '..')).Path
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $repoRoot
try {
    python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider phase171_r2b_prop56_source_dependency_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R2B_FOCUSED_PYTEST_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R2B_FOCUSED_PYTEST=PASS'
    $arguments = @('-B', '-m', 'phase171_r2b_prop56_source_dependency_audit.audit', '--root', $repoRoot, '--report', $ReportPath)
    if ($DryRun.IsPresent) { $arguments += '--dry-run' }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R2B_AUDIT_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R2B=PASS'
}
finally {
    Pop-Location
}
```

## README.md 全文（英語）

````markdown
# Phase 171 R2B — Proposition 5.6 Source Dependency Audit

This is a read-only continuation of the completed R2A alignment audit. It does not change application source, database files, source assertions, proof steps, or registered theorem status.

## Purpose

The three unresolved registered 3-stem queries are (n,k)=(3,3), (4,3), and (5,3). R2A established that each database-typed goal differs structurally from the registered Proposition 5.6 candidate and that none of those candidate assertions has a proof link. R2B records these two blockers separately and extracts the original Proposition 5.6 statement and its proof from the checked-in `sources/toda/Toda_05_2.tex`. The proof text is preserved verbatim in an external audit report, and literal references appearing in the proof are inventoried.

This source presence is **not** certification of mathematical correctness or authorization of a GIVEN ProofStep. The source registration remains unverified and must be reviewed before implementing a proof transformation. This package makes no inference and does not attempt to equate `Suspension` with `IteratedSuspension` or alter generator identities.

## Windows PowerShell

Run from your repository root:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2B_R2.zip" -DestinationPath "." -Force
$Alignment = Join-Path $env:LOCALAPPDATA "EHPProofTracerRecovery\phase171_r2a_prop56_20261029_070818_650545\alignment.json"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2b_prop56_source_dependency_audit\run.ps1" -ReportPath $Alignment -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2b_prop56_source_dependency_audit\run.ps1" -ReportPath $Alignment
git status -sb
```

The runner uses `python -m` from the repository root to preserve import semantics and runs only package-focused pytest. Git must be on `develop`, with a clean tracked working tree. Both the reviewed baseline and `origin/develop` must be ancestors of local `HEAD`; therefore a local branch that is **ahead** only by reviewed Phase 171 audit commits is allowed, but a **behind** or diverged branch is rejected. All committed differences from the baseline and from `origin/develop` must be limited to the reviewed Phase 171 audit directories. Pinned production source Git blobs must remain unchanged. Untracked audit folders are allowed. Neither `git push` nor reset/checkout is required.

The full source proof and classification are saved as UTF-8 `dependency.json` and `dependency.md` under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2b_prop56_*`. This is an audit report, not a completed proof.

## Boundaries

Only files in this package are new. No runtime implementation or formal project document is modified. No full pytest is run before Phase 171 closeout. Subsequent implementation must independently verify cited premises, preserve chronology and the Proof Tree trust boundary, and rely on generic generator representation rather than label-specific normalization.
````

## 監査仕様.md 全文（日本語）

````markdown
# Phase 171 R2B 監査仕様

## 目的

R2A で確認された3件の型付き不一致と、3件の証明リンク欠落をそれぞれ独立した未解決事項として記録する。対象は3-stemの n=3,4,5 である。Proposition 5.6 の群構造を再登録しない。

## 監査入力

R2A の `alignment.json` と、リポジトリに収録されている `sources/toda/Toda_05_2.tex` を使用する。`alignment.json` は Phase 171 R2A の読み取り専用監査結果であり、n=3,4,5 の Goal が厳密一致しないこと、命題の ProofStep リンクが0件であることを検査する。

Git ブランチは `develop`、追跡済みファイルの未コミット変更は0件とする。基準コミット `715b00d67d4b3ff4b34bf87229842d14960ea6bb` と `origin/develop` がいずれもローカル `HEAD` の祖先であることを確認する。ローカル `HEAD` が `origin/develop` より監査用コミットだけ先行している状態（ahead）は許容するが、behind または diverged は拒否する。基準コミットおよび `origin/develop` からのコミット済み差分は、列挙済み Phase 171 監査ディレクトリのみに限定する。数学的ソース、DB、登録器、Proof Search などは既知の Git blob SHA に固定する。Git の push/reset/checkout は実施しない。

## 本文の取り扱い

Proposition 5.6 の主張部分と証明本文を、リポジトリ内の TeX から切り出して保存する。引用先は文字列として検出し、証明可能性や引用可能性を保証する情報には変換しない。原文中の `(5.6)?` はそのまま記録し、根拠が確認済みであるとは扱わない。

## 実装・完了条件

追加対象は `phase171_r2b_prop56_source_dependency_audit/` の新規ファイルのみ。限定 pytest、3群の診断、本文抽出、Git 追跡ファイル不変、外部監査レポートの保存を完了条件とする。3群が `SEARCH_COMPLETE` になったとは判定しない。

次段階では、出典の照合、生成元の同一性の型付き根拠、既存推論規則の適用条件を別々に検証する。`HyoujiGen.csv` のデータが使える場合は一般的な構造照合を優先し、ν の名前に固有な例外処理を増やさない。
````

## 検証・完了条件

限定 pytest：26件 PASS。今回追加・変更した対象だけで、全体 pytest は未実行。PowerShell 実行後に `PHASE171_R2B_DETAIL` 3件、`PHASE171_R2B_SOURCE_PROOF_FOUND=True`、`PHASE171_R2B_TRACKED_UNCHANGED=True`、`PHASE171_R2B_RESULT=PASS` が出ること。

## 次 Phase との境界

R2B は出典・依存命題の監査のみです。型付き Goal の正規化、Proposition 5.6 の検証済み ProofStep 作成、原典の出典昇格、Proof Tree の完成は行いません。
