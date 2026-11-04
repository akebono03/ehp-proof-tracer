# Phase 173 final closeout — full changed units

既存コードへの変更はありません。追加するのは新規ディレクトリだけです。既存 Markdown 5文書は、以下のスクリプトで**それぞれの変更後全文**として出力します。

変更対象：`README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md`。

新規：`phase173_final_closeout_docs/docs_closeout.py` の全関数（`git`、`verify_repo`、`verify_report`、`transform_document`、`write_atomic`、`produce_full_documents`、`main`）、`run.ps1`、`tests/test_docs_closeout.py` の全テスト関数。新規ファイルの import は以下に全文を掲載します。

## `docs_closeout.py` — full source

```python
"""Phase 173 final-closeout documentation: five complete files, no proof edits.

Guard all tracked source documents against reviewed Git blobs before applying.
The sole proof/test evidence is the already-recorded R2 successful gate report.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


REVIEWED_HEAD = "25b1ee1f7c848356604061991db06265cfccb296"
AUDITED_ARCHIVE_HEAD = "9003ada8d9d723fbcbec67db55f4d4382ad45ea2"
REVIEWED_BLOBS = {
    "README.md": "109445340c559cfb2357d363c096cebbdb871168",
    "docs/design.md": "0491c27d8075829ba28151029eb19b119a293eff",
    "docs/development_log.md": "880dc8f9f2ff9408a9b4a61c7daa5d816955064c",
    "docs/roadmap.md": "d1d9661eb39674b156185bf61e74b8ee5fd9e101",
    "docs/proof_records.md": "eb310080fb85a265b474ed4a9c60ee91511cc6cf",
}
MARKER = "<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->"
CHECKPOINT = "<!-- PHASE173_R15R17_CHECKPOINT_20261104 -->"
EXPECTED_SUMMARY = "3546 passed in 80.58s (0:01:20)"

README_FINAL = r"""<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->

## Current status — Phase 173 formally closed (2026-11-05)

Phase 173 completed its reviewed proof-search and common-narrative integration
scope. The public route uses the verified Proof Tree, one ProofNarrativeModel,
one common Renderer, and a single source-backed Reference section. No
n/k-, generator-, or group-specific public narrative was introduced to
substitute for a mathematical proof. Typed equivalent pending group-structure
goals are grouped for display only; their underlying ProofSearchResult and
ProofSteps remain unchanged.

The checked public examples distinguish certified abstract structure from
completed named-generator proofs. For $\pi_{12}^{4}$ the abstract group is
$\mathbb Z/2$ but the named generator $\varepsilon_4$ is not proved (three
typed open goals, displayed together). For $\pi_{13}^{4}$ the abstract group
is $(\mathbb Z/2)^3$ but the named presentation remains incomplete (two typed
open goals, displayed together). The named proof for $\pi_8^5$ remains
incomplete without an abstract certificate; $\pi_8^4$ remains complete.
All four examples passed the Flask HTTP gate and were reviewed in browser-
copied text. A pixel-level MathJax/layout review was **not** independently
verified.

The first phase-end active `tests/` suite reported **3541 passed, 5 failed**:
three Phase 167 test modules still searched for a removed `証明` heading.
The five failures were test-contract mismatches in the Reference section
boundary, not demonstrated mathematical proof failures. The three tests
files were corrected to use the single canonical separator; the focused
regression passed **6 tests**. The corrective active-suite gate at Git HEAD
`25b1ee1f7c848356604061991db06265cfccb296` subsequently reported
**3546 passed in 80.58s (0:01:20)**, exit code 0, with reviewed source
blobs and preserved Git index.

The original four machine-generated files from the first failed test gate
were unavailable under the current Windows profile. Their preservation is
**not verifiable**; the initial failure remains recorded in the user-supplied
console log. The corrective PASS report is separate at
`%LOCALAPPDATA%/EHPProofTracerRecovery/phase173_final_gate_r2/phase173_full_test_report_r2.json`.
The closeout documentation adds no new theorems, new inference rules, or new
named-generator certificates. Future mathematical proof gaps belong to a later
phase.

"""

DESIGN_FINAL = r"""<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->

## Phase 173 正式終了 — 共通 Narrative の最終設計境界（2026-11-05）

**公開経路の責務：** Backward Search（逆向き証明探索）→ Verified Proof Tree（検証済み証明木）→ 単一の `ProofNarrativeModel`（証明文章モデル）→ 共通 Narrative Renderer（文章表示器）→ Flask Web とする。検証済み抽象群構造の祖先 ProofStep は同一 Model に統合し、Reference（根拠一覧）を一度だけ描画する。群の次元や生成元の名称による新しい Narrative 分岐は設けない。

**不変条件：** 証明木中の引用、`ProofSearchStatus`、`open_goals`、`diagnostics` を表示側で生成・変更しない。型付きの等価な未解決 Goal は表示上まとめても、内部ではすべて保持する。$\pi_{12}^{4}\cong\mathbb Z/2$ と $\pi_{12}^{4}=\mathbb Z/2\{\varepsilon_4\}$ は、前者の抽象群構造だけが検証済みである。$\pi_{13}^{4}\cong(\mathbb Z/2)^3$ と記名直和生成元の証明も同様に区別する。$\pi_8^5$ は未完成、$\pi_8^4$ は完成を維持した。

**テスト結果と境界：** R15R17 R3R5 の Flask HTTP 4例、ブラウザからの文字列確認4例、旧 Phase 167 Reference テスト3ファイルの修正後限定 pytest 6 PASS。Phase 173 最終 Gate 初回は **3541 PASS／5 FAIL**（旧 `証明` 見出しを探す5 assertion）。修正後の R2 最終 Gate は Git HEAD `25b1ee1f7c848356604061991db06265cfccb296` で **3546 PASS（80.58秒、終了コード0）**、Source Guard と Git index 保持 PASS。旧失敗の機械生成原本4ファイルは現在の Windows プロファイルから参照できず、**原本保存状態は未検証**。ブラウザの MathJax 画素レベル検証も未確認である。

この終了認定は共通表示の経路・テスト契約と個別の検証済み結果に限定する。任意の群の記名生成元証明、登録された文献命題の全真偽、一般的な数学的探索の完成は主張しない。将来 Phase で必要な数学的 Goal を別途扱う。
"""

DEVELOPMENT_FINAL = r"""<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->

## 2026-11-05 — Phase 173 正式終了：最終 Gate 失敗から修正後成功まで

Phase 173 は $n\ge3$ の探索状況を監査し、共通 Proof Narrative Model（証明文章モデル）・Reference・Renderer の公開経路を統合した。R15R17 では表示専用の型付き未解決 Goal 集約と、過去の旧表示契約に依存したテストの保守を行った。Flask HTTP の4ケース $(n,k)=(4,8),(4,9),(5,3),(4,4)$ は PASS。ユーザーによるブラウザ表示内容の確認も4ケースそろったが、MathJax の画素・レイアウトは独立検証していない。

**初回終了 Gate の失敗（2026-11-04）：** 現行アクティブ `tests/` の全体 pytest は `5 failed, 3541 passed in 34.43s`。失敗は `tests/test_phase167_r2_range_dedup.py` 2件、`tests/test_phase167_r2_shared_reference.py` 1件、`tests/test_phase167_r2_unified_reference.py` 2件の `StopIteration`。共通表示では Reference の末尾が `separator` になった一方、旧テストが `証明` 見出しを探していたためであり、証明アルゴリズムの誤りを示すものではなかった。

**R1修正：** 上記3テストファイルで Reference と証明本文の区切り検出だけを単一の `separator` に更新し、数学的な一般形・引用数の検査を保持。R1 DryRun／適用 PASS、限定 pytest **6 PASS**。既存本体は変更しない。

**R2再試験と失敗記録：** 別 Windows プロファイル `C:\Users\user` からは、初回失敗の `%LOCALAPPDATA%/EHPProofTracerRecovery/phase173_final_gate` に保存した機械生成原本4ファイルを参照できなかった。R2R1 は保存先指定を改善し、R2R2 は原本4件がすべて不在のときのみ明示的許可で再実行する。原本の `PRESERVED` 判定は **NOT_VERIFIABLE** を保持し、過去の失敗ログを成功に書き換えない。R2R2 の修正後 Gate 限定 pytest **27 PASS**。

**訂正後の最終 Gate：** `PHASE173_FINAL_R2_HEAD=25b1ee1f7c848356604061991db06265cfccb296`、`SOURCE_GUARD=PASS`、`PYTEST_EXIT=0`、`FULL_PYTEST=PASS`、`FULL_PYTEST_PASSED=3546`、`GATE=PASS`、`GIT_INDEX_PRESERVED=PASS`。pytest 表示は **3546 passed in 80.58s (0:01:20)**。別証拠として `%LOCALAPPDATA%/EHPProofTracerRecovery/phase173_final_gate_r2/phase173_full_test_report_r2.json` と stdout / stderr が存在する。ユーザー投稿の初回失敗ログと今回の成功ログは区別して保存する。

**Phase 173 正式終了：** 本最終5文書の更新・版照合後に終了とする。未完成の記名生成元 Goal や一般的推論機能を先取りせず、次 Phase へ持ち越す。過去の開発履歴は保持する。
"""

ROADMAP_FINAL = r"""<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->

## Phase 173 終了・次 Phase の境界（2026-11-05）

**Phase 173 は正式終了。** 最終訂正 Gate R2 は Git HEAD `25b1ee1f7c848356604061991db06265cfccb296` で、現行アクティブ `tests/` **3546 PASS（80.58秒、終了コード0）**、Source Guard PASS、Git index 保持 PASS を確認。初回 Gate は旧 Phase 167 Reference テストの不整合により **5 FAIL／3541 PASS** であり、修正3ファイルの限定 pytest **6 PASS** 後に訂正再実行した。旧失敗の機械生成原本は現在参照できず保存確認はできない。

共通 Narrative Renderer と単一 Reference の4対象 Web 表示は確認済み。ただしブラウザの MathJax レイアウト（画素）の独立検証は未了とする。抽象群構造が検証済みでも、記名生成元の Goal は未完成のまま保持する。

**次 Phase の候補：** 未解決の記名生成元証明、出典・型付き関係・必要な証明規則の監査から開始する。$\pi_{12}^{4}=\mathbb Z/2\{\varepsilon_4\}$、$\pi_{13}^{4}$ の記名直和分解、$\pi_8^5$ の生成元に関する Goal は本 Phase 173 で完成していない。特定の群のための例外的 Narrative 追加は行わず、必要なら Proof Search と型付き数学的推論を一般性・出典付きで拡張する。次 Phase の全体 pytest はその終了時にのみ実施する。
"""

PROOF_FINAL = r"""<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->

## 2026-11-05 — Phase 173 証明記録・未完成境界・終了 Gate

検証済み Proof Tree（証明木）から共通 Model・Narrative を生成する公開経路を監査した。$\pi_{12}^{4}$ は

$$
\pi_{12}^{4}\cong\mathbb Z/2
$$

という抽象群構造の検証済み ProofStep を持つが、$\varepsilon_4$ が生成元である記名表示は未証明である。型付き未解決 Goal は3件あり、表示上は同じ群構造の1行にまとめるだけで削除しない。$\pi_{13}^{4}$ でも

$$
\pi_{13}^{4}\cong(\mathbb Z/2)^3
$$

という抽象群の結論と、$\nu_4^3,\mu_4,\eta_4\varepsilon_5$ を用いる記名直和分解の完成証明は区別する（未解決 Goal 2件）。$\pi_8^5=\mathbb Z/8\{\nu_5\}$ は未完成で抽象群証明書もなく、$\pi_8^4$ は記名証明が完成している。これらの群について、Flask HTTP と公開文章の4ケースで状態・引用・未解決 Goal を確認した。DB の既知結果を未証明の前提から証明済みの結論に昇格させない。

R15R17 の一元化は数学的な新しい定理ではなく、既存の検証済み祖先・Reference を表示へ投影する処理である。旧 Reference 見出しを要求する Phase 167 の3ファイルのテスト修正後、限定 pytest 6 PASS。Phase 173 初回全体テストは5 FAIL・3541 PASS、訂正 R2 のアクティブ全体テストは **3546 PASS（80.58秒、終了コード0）**、Git HEAD `25b1ee1f7c848356604061991db06265cfccb296`、Source Guard PASS、Git index 保全 PASS。初回の機械生成失敗レポート原本4ファイルは確認できないため、保存状態は未検証と記録する。ブラウザ画素・MathJax 配置の検証も未確認である。

**Phase 173 正式終了の範囲：** これらの証明木・表示と活性テストの回帰に限る。記名生成元の未解決命題は解決しておらず、すべての $n,k$ や未採録の Toda 命題を一般に証明したとは主張しない。
"""

FINAL_BLOCKS = {
    "docs/design.md": DESIGN_FINAL,
    "docs/development_log.md": DEVELOPMENT_FINAL,
    "docs/roadmap.md": ROADMAP_FINAL,
    "docs/proof_records.md": PROOF_FINAL,
}


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result


def verify_repo(repo: Path) -> str:
    branch = git(repo, "branch", "--show-current").stdout.strip()
    if branch != "develop":
        raise RuntimeError("the closeout package requires the develop branch")
    root = Path(git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if root != repo.resolve():
        raise RuntimeError("extract this ZIP at the repository root")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    remote = git(repo, "rev-parse", "origin/develop").stdout.strip()
    for ref in ("HEAD", "origin/develop"):
        if git(repo, "merge-base", "--is-ancestor", REVIEWED_HEAD, ref,
               check=False).returncode != 0:
            raise RuntimeError(f"{ref} does not descend from reviewed HEAD")
    if git(repo, "merge-base", "--is-ancestor", "HEAD", "origin/develop",
           check=False).returncode != 0:
        raise RuntimeError("HEAD and origin/develop diverged")
    if git(repo, "diff", "--cached", "--quiet", check=False).returncode != 0:
        raise RuntimeError("staged modifications require separate review")
    changed = git(repo, "diff", "--name-only").stdout.splitlines()
    if changed:
        raise RuntimeError("tracked worktree changes require review: " + ", ".join(changed))
    for path, blob in REVIEWED_BLOBS.items():
        for ref in ("HEAD", "origin/develop"):
            actual = git(repo, "rev-parse", ref + ":" + path).stdout.strip()
            if actual != blob:
                raise RuntimeError("unreviewed document blob: " + ref + ":" + path)
        local = repo / path
        if not local.is_file():
            raise RuntimeError("missing document: " + path)
        if MARKER.encode("utf-8") in local.read_bytes():
            raise RuntimeError("Phase 173 closeout is already applied: " + path)
    print("PHASE173_CLOSEOUT_SOURCE_GUARD=PASS")
    return head


def verify_report(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise RuntimeError("successful R2 Gate report not found: " + str(path))
    raw = path.read_bytes()
    report = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(report, dict):
        raise RuntimeError("R2 report is not a JSON object")
    conditions = (
        report.get("phase") == 173,
        report.get("checkpoint") == "phase_end_corrective_r2",
        report.get("status") == "PASS",
        report.get("head") == REVIEWED_HEAD,
        report.get("pytest_exit_code") == 0,
        report.get("pytest_passed_count") == 3546,
        report.get("pytest_summary") == EXPECTED_SUMMARY,
        report.get("prior_failure_evidence_status") == "UNAVAILABLE_ORIGINAL_FILES",
        report.get("prior_failure_sha256") == {},
        report.get("browser_content_checked") == [[4, 8], [4, 9], [5, 3], [4, 4]],
        report.get("phase_formally_closed") is False,
    )
    if not all(conditions):
        raise RuntimeError("R2 report differs from the reviewed successful gate")
    stdout_path = Path(str(report.get("pytest_stdout", "")))
    if not stdout_path.is_file():
        raise RuntimeError("R2 stdout evidence is unavailable")
    stdout = stdout_path.read_text(encoding="utf-8", errors="replace")
    if EXPECTED_SUMMARY not in stdout or re.search(r"(?m)^5 failed", stdout):
        raise RuntimeError("R2 stdout does not match the successful full-suite summary")
    return {
        "report_sha256": hashlib.sha256(raw).hexdigest(),
        "stdout_sha256": hashlib.sha256(stdout_path.read_bytes()).hexdigest(),
        "head": report["head"],
        "status": report["status"],
        "summary": report["pytest_summary"],
        "prior_evidence_status": report["prior_failure_evidence_status"],
        "report_path": str(path.resolve()),
    }


def transform_document(path: str, original: bytes) -> bytes:
    if path not in REVIEWED_BLOBS:
        raise ValueError("unsupported document path")
    if MARKER.encode("utf-8") in original:
        raise ValueError("closeout already applied")
    if CHECKPOINT.encode("utf-8") not in original:
        raise ValueError("R15R17 checkpoint is missing")
    if path == "README.md":
        old_title = "## Current status — Phase 173 R15R17 checkpoint (2026-11-04)"
        if original.count(old_title.encode("utf-8")) != 1:
            raise ValueError("README's current checkpoint heading is missing")
        revised = original.replace(
            old_title.encode("utf-8"),
            b"## Historical checkpoint \xe2\x80\x94 Phase 173 R15R17 (2026-11-04)",
            1,
        )
        revised = revised.replace(
            CHECKPOINT.encode("utf-8"),
            README_FINAL.encode("utf-8") + CHECKPOINT.encode("utf-8"),
            1,
        )
    else:
        if not original.startswith(b"# EHP Proof Tracer"):
            raise ValueError("unreviewed document header")
        newline = b"\r\n" if original.endswith(b"\r\n") else b"\n"
        addition = FINAL_BLOCKS[path].encode("utf-8").replace(b"\n", newline)
        revised = original + newline + addition
        if not revised.startswith(original):
            raise ValueError("historical document content changed")
    if revised.count(MARKER.encode("utf-8")) != 1 or len(revised) <= len(original):
        raise ValueError("invalid full-file document transformation")
    return revised


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".phase173_closeout_", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        if path.is_file():
            os.chmod(tmp, path.stat().st_mode)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def produce_full_documents(repo: Path, package: Path, evidence: dict[str, object], apply: bool) -> None:
    head = verify_repo(repo)
    if head not in (str(evidence["head"]), AUDITED_ARCHIVE_HEAD):
        raise RuntimeError("current Git HEAD is not the reviewed R2 or audited archive HEAD")
    before_index = git(repo, "write-tree").stdout.strip()
    originals = {p: (repo / p).read_bytes() for p in REVIEWED_BLOBS}
    generated = {p: transform_document(p, raw) for p, raw in originals.items()}
    previews = package / "full_documents"
    if not apply:
        for path, data in generated.items():
            write_atomic(previews / path, data)
            print(f"PHASE173_CLOSEOUT_FULL_FILE={path} BYTES={len(data)}")
        print("PHASE173_CLOSEOUT_PRODUCTION_WRITES=NONE")
    else:
        backups = package / "original_backups"
        for path, data in originals.items():
            write_atomic(backups / path, data)
        for path, data in generated.items():
            write_atomic(previews / path, data)
        changed: list[str] = []
        try:
            for path, data in generated.items():
                write_atomic(repo / path, data)
                changed.append(path)
            for path, data in generated.items():
                if (repo / path).read_bytes() != data:
                    raise RuntimeError("post-write document mismatch: " + path)
            state = {
                "phase": 173,
                "closeout": "DOCUMENTED_AFTER_R2_GATE",
                "reviewed_head": head,
                "evidence": evidence,
                "files": {path: {
                    "original_sha256": hashlib.sha256(originals[path]).hexdigest(),
                    "final_sha256": hashlib.sha256(generated[path]).hexdigest(),
                } for path in REVIEWED_BLOBS},
            }
            write_atomic(package / "installed_state.json",
                         (json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        except BaseException:
            for path in changed:
                write_atomic(repo / path, originals[path])
            raise
        print("PHASE173_CLOSEOUT_DOCUMENTS_INSTALLED=PASS")
    if git(repo, "write-tree").stdout.strip() != before_index:
        raise RuntimeError("Git index was changed")
    print("PHASE173_CLOSEOUT_GIT_INDEX_PRESERVED=PASS")
    print("PHASE173_CLOSEOUT_FULL_OUTPUT=" + str(previews))
    print("PHASE173_CLOSEOUT_EVIDENCE_REPORT_SHA256=" + str(evidence["report_sha256"]))
    print("PHASE173_CLOSEOUT_FULL_PYTEST=NOT_RERUN")
    print("PHASE173_CLOSEOUT_MODE=" + ("APPLY" if apply else "DRY_RUN"))
    print("PHASE173_CLOSEOUT_GATE=PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 173 five-full-doc closeout")
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    evidence = verify_report(args.report.expanduser().resolve())
    produce_full_documents(args.repo.resolve(), args.package.resolve(), evidence, args.apply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `run.ps1` — full source

```powershell
param(
    [switch]$DryRun,
    [string]$ReportPath = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
if ([string]::IsNullOrWhiteSpace($ReportPath)) {
    $ReportPath = Join-Path $env:LOCALAPPDATA 'EHPProofTracerRecovery\phase173_final_gate_r2\phase173_full_test_report_r2.json'
}
Write-Output 'PHASE173_CLOSEOUT_SCOPE=FIVE_FULL_DOCUMENTS_ONLY'
Write-Output 'PHASE173_CLOSEOUT_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
Write-Output 'PHASE173_CLOSEOUT_FULL_PYTEST=False'
& git -C $Root fetch origin develop
if ($LASTEXITCODE -ne 0) { throw 'git fetch failed' }
Push-Location $Root
try {
    Write-Output '=== PHASE 173 FINAL DOCUMENT CONTRACT TESTS ==='
    & python -B -m pytest -q -p no:cacheprovider `
        phase173_final_closeout_docs/tests/test_docs_closeout.py
    if ($LASTEXITCODE -ne 0) { throw 'Phase 173 document contract tests failed' }
    $Arguments = @(
        '-B', '-m', 'phase173_final_closeout_docs.docs_closeout',
        '--repo', $Root, '--package', $Package, '--report', $ReportPath
    )
    if (-not $DryRun) { $Arguments += '--apply' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'Phase 173 full-document closeout failed' }
} finally {
    Pop-Location
}

```

## `tests/test_docs_closeout.py` — full source

```python
"""Phase 173 five-complete-document closeout, isolated from the real repository."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase173_final_closeout_docs.docs_closeout import (
    CHECKPOINT,
    EXPECTED_SUMMARY,
    FINAL_BLOCKS,
    MARKER,
    README_FINAL,
    REVIEWED_BLOBS,
    REVIEWED_HEAD,
    transform_document,
    verify_report,
)


def test_exactly_five_docs_selected() -> None:
    assert set(REVIEWED_BLOBS) == {
        'README.md', 'docs/design.md', 'docs/development_log.md',
        'docs/roadmap.md', 'docs/proof_records.md',
    }


def test_readme_complete_text_prepends_closeout_and_preserves_history() -> None:
    raw = (
        '# EHP Proof Tracer\n\n' + CHECKPOINT + '\n'
        '## Current status — Phase 173 R15R17 checkpoint (2026-11-04)\n'
        'Older checkpoint content.\n'
    ).encode('utf-8')
    result = transform_document('README.md', raw).decode('utf-8')
    assert result.count(MARKER) == 1
    assert 'Older checkpoint content.' in result
    assert '## Historical checkpoint — Phase 173 R15R17' in result
    assert '## Current status — Phase 173 formally closed' in result
    assert result.index(MARKER) < result.index(CHECKPOINT)
    assert result.endswith('Older checkpoint content.\n')


@pytest.mark.parametrize('path', tuple(FINAL_BLOCKS))
def test_four_japanese_docs_append_complete_copy(path: str) -> None:
    raw = ('# EHP Proof Tracer 記録\n\n先行記録。\n' + CHECKPOINT + '\n').encode('utf-8')
    result = transform_document(path, raw)
    assert result.startswith(raw)
    assert result.count(MARKER.encode('utf-8')) == 1
    assert b'\r\n' not in result
    assert '$\\pi' in result.decode('utf-8') or path == 'docs/development_log.md'


def test_windows_newlines_preserved() -> None:
    path = 'docs/design.md'
    raw = ('# EHP Proof Tracer 設計\r\n' + CHECKPOINT + '\r\n').encode('utf-8')
    result = transform_document(path, raw)
    assert result.startswith(raw)
    assert b'\r\n' in result[len(raw):]
    assert b'\n' not in result[len(raw):].replace(b'\r\n', b'')


def test_duplicate_closeout_rejected() -> None:
    raw = ('# EHP Proof Tracer\n' + CHECKPOINT + '\n' + MARKER).encode('utf-8')
    with pytest.raises(ValueError, match='already applied'):
        transform_document('docs/proof_records.md', raw)


def test_missing_checkpoint_rejected() -> None:
    with pytest.raises(ValueError, match='checkpoint'):
        transform_document('docs/design.md', b'# EHP Proof Tracer\n')


def test_unreviewed_target_rejected() -> None:
    with pytest.raises(ValueError, match='unsupported'):
        transform_document('docs/unreviewed.md', b'')


def make_report(tmp_path: Path) -> Path:
    stdout = tmp_path / 'active_suite_stdout_r2.txt'
    stdout.write_text('..................................... [100%]\n'
                      + EXPECTED_SUMMARY + '\n', encoding='utf-8')
    report = {
        'phase': 173,
        'checkpoint': 'phase_end_corrective_r2',
        'status': 'PASS',
        'head': REVIEWED_HEAD,
        'pytest_exit_code': 0,
        'pytest_passed_count': 3546,
        'pytest_summary': EXPECTED_SUMMARY,
        'prior_failure_evidence_status': 'UNAVAILABLE_ORIGINAL_FILES',
        'prior_failure_sha256': {},
        'browser_content_checked': [[4, 8], [4, 9], [5, 3], [4, 4]],
        'phase_formally_closed': False,
        'pytest_stdout': str(stdout),
    }
    report_path = tmp_path / 'phase173_full_test_report_r2.json'
    report_path.write_text(json.dumps(report), encoding='utf-8')
    return report_path


def test_valid_success_report_accepted(tmp_path: Path) -> None:
    output = verify_report(make_report(tmp_path))
    assert output['head'] == REVIEWED_HEAD
    assert output['summary'] == EXPECTED_SUMMARY
    assert output['prior_evidence_status'] == 'UNAVAILABLE_ORIGINAL_FILES'
    assert len(output['report_sha256']) == 64


def test_forged_full_suite_count_rejected(tmp_path: Path) -> None:
    path = make_report(tmp_path)
    content = json.loads(path.read_text(encoding='utf-8'))
    content['pytest_passed_count'] = 3545
    path.write_text(json.dumps(content), encoding='utf-8')
    with pytest.raises(RuntimeError, match='differs'):
        verify_report(path)


def test_missing_report_rejected(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match='not found'):
        verify_report(tmp_path / 'absent.json')


def test_missing_stdout_rejected(tmp_path: Path) -> None:
    path = make_report(tmp_path)
    stdout = tmp_path / 'active_suite_stdout_r2.txt'
    stdout.unlink()
    with pytest.raises(RuntimeError, match='stdout'):
        verify_report(path)


def test_original_failure_not_claimed_verified() -> None:
    assert 'not verifiable' in README_FINAL
    assert '未検証' in FINAL_BLOCKS['docs/design.md']
    assert 'NOT_VERIFIABLE' in FINAL_BLOCKS['docs/development_log.md']


def test_full_document_dry_run_and_apply_preserve_backups(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from types import SimpleNamespace
    from phase173_final_closeout_docs import docs_closeout as module

    repo = tmp_path / 'repo'
    package = repo / 'phase173_final_closeout_docs'
    package.mkdir(parents=True)
    originals = {}
    for path in REVIEWED_BLOBS:
        if path == 'README.md':
            content = (
                '# EHP Proof Tracer\n' + CHECKPOINT + '\n'
                '## Current status — Phase 173 R15R17 checkpoint (2026-11-04)\n'
                'Historical README prose.\n'
            ).encode('utf-8')
        else:
            content = ('# EHP Proof Tracer 記録\n' + CHECKPOINT + '\n'
                       '過去の記録を保持。\n').encode('utf-8')
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        originals[path] = content

    monkeypatch.setattr(module, 'verify_repo', lambda directory: REVIEWED_HEAD)
    monkeypatch.setattr(module, 'git', lambda *args, **kwargs: SimpleNamespace(stdout='stable-index\n'))
    evidence = {'head': REVIEWED_HEAD, 'report_sha256': 'a' * 64}

    module.produce_full_documents(repo, package, evidence, apply=False)
    for path, original in originals.items():
        assert (repo / path).read_bytes() == original
        preview = (package / 'full_documents' / path).read_bytes()
        assert MARKER.encode('utf-8') in preview

    module.produce_full_documents(repo, package, evidence, apply=True)
    for path, original in originals.items():
        assert (package / 'original_backups' / path).read_bytes() == original
        assert (repo / path).read_bytes() == (package / 'full_documents' / path).read_bytes()
        assert MARKER.encode('utf-8') in (repo / path).read_bytes()
    state = json.loads((package / 'installed_state.json').read_text('utf-8'))
    assert state['phase'] == 173
    assert set(state['files']) == set(REVIEWED_BLOBS)

```

