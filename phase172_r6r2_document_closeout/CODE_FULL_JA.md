# Phase 172 R6R2 — 追加・置換対象コード全文

既存の Python コードは変更しない。実行時には現在の5文書を直接読み込み、過去の全文を保持した**置換後の全文**を `%LOCALAPPDATA%/EHPProofTracerRecovery/phase172_r6r2_document_closeout_*/full_documents/` に個別ファイルとして出力する。以下に新規コード、テスト、必要な import の全文を掲載する。

## `sections.py`（全文・新規追加位置：リポジトリ直下 `phase172_r6r2_document_closeout/sections.py`）

```python
"""Phase 172 closure narrative, strictly documentation only.

All supplied sections are full prose. The installer writes complete revised
file contents, retaining every prior byte except README's outdated status heading.
"""
from __future__ import annotations

MARKER = "<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->"

README_CURRENT = r"""<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->

## Current status — Phase 172 closed (2026-10-31)

Phase 172 is closed after presentation-only improvements to the verified public
proof of $\pi_6^3=\mathbb Z/4\{\nu'\}$. The common model-backed renderer now
suppresses redundant, certified suspension equalities, compresses a cited Hopf
image derivation, avoids a second display of the same Hopf surjectivity, and
renders admitted prior database results in readable Japanese while retaining
their internal database provenance and reference identities.

The proof itself is unchanged: the completed backward search still verifies
50 ProofSteps, 8 references, no open goals, and the `generic-complete-proof`
Web route. Regression checks passed for $\pi_3^2$, $\pi_4^3$, $\pi_5^3$,
$\pi_6^4$, and $\pi_6^3$. The Phase 172 R6 closeout gate passed ten focused
test groups, all five public-Web proof checks, and the active `tests/` full
suite **once**: `3546 passed in 107.52s (0:01:47)` (exit code 0). Local and
`origin/develop` heads matched at `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a`,
and tracked files were unchanged during that gate.

The two adopted `sphere.csv` prior results remain database assumptions, **not**
independently authenticated literature theorems; proposition numbers shown as
references are explicitly supplemental. This phase neither changes the
mathematical proof, introduces new GIVEN facts, nor certifies arbitrary other
homotopy groups. The next phase scope is not yet determined.

"""

DESIGN_ADDENDUM = r"""<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->

## Phase 172 — 表示専用射影と終了時の不変条件（2026-10-31）

Phase 172 は、Phase 171 で完成した $\pi_6^3=\mathbb Z/4\{\nu'\}$ の証明に対して、**検証済み Proof Tree を入力とする表示専用 Projection（射影処理）**を整備した。Backward Search（後向き証明探索）、Inference Rule（推論規則）、既存の `GIVEN`、群構造、文献出典の採用規則は変更していない。

- R1 は既存 Web Narrative（証明叙述）、Reference（引用）、50件の ProofStep（証明段階）を照合した監査である。
- R2 は引用済み `GeneratorSuspension`（生成元懸垂）から検証済みの直接等式と対称等式の重複表示を省く。`η_5` と `η₅` は印字名ではなく、`GeneratorSymbol`（型付き生成元識別子）・次元・始域・終域で対応を検証する。証明段階は残す。
- R3 は $H(\nu'\eta_6)=\eta_5^2$ に至る既証明の Hopf 導出の途中式を短縮し、Definition（定義）、Proposition 2.2、(5.3) の出典に対応する本文と最終等式を維持する。
- R4 は同じ型付き Hopf 写像の全射性を二度表示しない。後の全射性の推論依存と先行する検証済みの全射性を確認した場合だけ後者の重複行を抑制する。
- R5 は `ADOPTED_DATABASE_PRIOR` の出典を Web Reference 見出しに限って日本語化する。元の `DB prior: sphere.csv` locator と対応する ProofStep、Reference 番号、Trust Boundary（証明の検証境界）は保持する。`[参考: Proposition ...]` は独立の文献定理として採用したことを意味しない。

これらは型付きの根・祖先・Citation（引用対応）と表示順を検査し、欠損・不整合・未完成の証明では不正な圧縮を行わない **fail-closed（不確実な場合は変換しない）**方式である。特定の生成元名による新しい数学的例外や、新しい公理を追加しない。

R6 Closeout（終了監査）では、`develop` の `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a` に対し、限定 pytest 10セット、公開 Web 検証5群（$\pi_3^2,\pi_4^3,\pi_5^3,\pi_6^4,\pi_6^3$）がすべて PASS。$\pi_6^3$ の ProofStep 50件、Reference 8件、未解決 Goal 0、Web key `generic-complete-proof`、内部 DB 出典の不変を確認した。Phase 末尾の**現行アクティブ `tests/` 全体 pytest は1回のみ**実施し、`3546 passed in 107.52s (0:01:47)`、終了コード0。実行前後の追跡済みファイルの状態は一致した。

過去の「Phase 172 は候補・未実装」という記述は記録時点の履歴であり、本節が最新の正式状態である。次 Phase の内容はこの Phase 172 に含まれず、別途決定する。
"""

DEVELOPMENT_ADDENDUM = r"""<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->

## 2026-10-31 — Phase 172 正式終了（R1〜R6）

R1 `AUDIT_ONLY` では、Phase 171 完成済みの $\pi_6^3=\mathbb Z/4\{\nu'\}$ について、ProofStep 50件、Reference 8件、`complete`、`generic-complete-proof`、未解決 Goal 0を確認し、懸垂関係・Hopf 導出・全射性・`DB prior` 見出しの表示上の重複と内部表現を分類した。

R2 は $E(\eta_5)=\eta_6$ の派生等式と対称等式の重複を証明木から取り除かず、表示上だけ抑制した。最初の限定テストは `η_5`／`η₅` の印字名の差によって失敗し、R2R1 で同一の型付き生成元を構造的に比較する方式へ訂正。限定 pytest 5セット PASS。

R3R1 は Hopf 導出の出典と中間段階を監査した。R3R1R1 では、R2 がコミット済みの Renderer を監査 Gate が誤って拒否する問題を訂正した。R3 では $H(\nu'\eta_6)=\eta_5^2$ に至る既証明の途中式を整理した。R2 の歴史的な表示期待と衝突したテスト1件を R3R2 で修正し、R3 限定 pytest 5セット PASS。数学的推論・Proof Tree は変更していない。

R4 は Hopf 写像 $H:\pi_6^3\to\pi_6^5$ の全射性の重複表示を整理し、限定 pytest 6セット PASS。R5 は先行 `sphere.csv` DB 結果の Web Reference 見出しを日本語化し、内部 locator・引用番号・Trust Boundary を維持したまま限定 pytest 6セット PASS。R5 までの数学的な推論規則と既知の群構造は不変である。

R6 の Git HEAD は `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a`（`origin/develop` と一致）。Renderer は R5 コミット済み。内容検査・DryRun PASS、限定 pytest **10セットすべて PASS**、公開 Web の5群 $\pi_3^2,\pi_4^3,\pi_5^3,\pi_6^4,\pi_6^3$ がすべて PASS。Phase 終了 Gate の現行アクティブ `tests/` 全体 pytest を**1回**実行し、`3546 passed in 107.52s (0:01:47)`、終了コード0。追跡済みファイルの状態は実行前後で不変。最終結果は `PASS_PHASE172_R6_FULL_CLOSEOUT_GATE`。

終了証拠は `%LOCALAPPDATA%/EHPProofTracerRecovery/phase172_r6_20261031_144642_024616Z/closeout.json`、同 `full_active_pytest.log` と `pi_6_3_web_narrative.md` に保存されている。直前の DryRun は全体 pytest を実行していない。過去の途中失敗は修正済みであり、この正式終了記録は R6 の成功結果に基づく。

**Phase 172 正式終了。** 次 Phase の機能は先取りせず、別途計画する。本節は開発履歴への追記であり、過去の失敗・修正履歴を削除しない。
"""

ROADMAP_ADDENDUM = r"""<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->

## Phase 172 正式終了・次 Phase の境界（2026-10-31）

Phase 172 の R1〜R5 は、Phase 171 で完成した $\pi_6^3=\mathbb Z/4\{\nu'\}$ の Web 表示を、証明木と出典を不変にして改善した。懸垂等式の重複、Hopf 導出の過長表示、全射性の重複、`DB prior` の内部的見出しを整理済みである。R6 にて限定10セット・Web 5群の回帰検証が PASSし、現行アクティブ `tests/` 全体 pytest は**3,546 PASS（107.52秒、終了コード0）**である。`develop` の検証 HEAD は `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a`、追跡済みファイルの状態は不変。**Phase 172 は正式終了。**

次 Phase は未決定であり、Phase 172 の終了認定は未完成群の新規証明・一般化・未検証の文献内容には及ばない。新たな目標は、現行の登録結果・Proof Tree・必要な出典を個別に監査してから設定する。全体 pytest は次 Phase の終了 Gate まで再実行しない。

旧節の「Phase 172 — 候補（未実装）」は当時の計画の履歴であって、最新の状態は本節による。
"""

PROOF_ADDENDUM = r"""<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->

## 2026-10-31 — Phase 172 表示改善後の完成証明・保存記録

登録済み $\pi_6^3=\mathbb Z/4\{\nu'\}$ について、Phase 171 で確立した証明の数学的根拠を維持している。EHP の短完全列

$$
0\longrightarrow\pi_5^2\xrightarrow{E}\pi_6^3\xrightarrow{H}\pi_6^5\longrightarrow0
$$

と、両端の位数が2であることから $|\pi_6^3|=4$。さらに、単射性により $E(\eta_2^3)\ne0$、証明済みの $2\nu'=E(\eta_2^3)$ から $2\nu'\ne0$ となり、$\nu'$ の位数は4である。この数学的な Proof Tree は Phase 172 で変更していない。

表示整理では、型付きの $E(\eta_5)=\eta_6$ の重複二式を非表示化し、$H(\nu'\eta_6)=\eta_5^2$ の導出を既知の Proposition 2.2・(5.3)・Definition の引用を保って簡素化し、同じ Hopf 全射性の反復を抑制した。Reference 見出しの2件は `sphere.csv` に採録された先行群結果であり、内部 `ADOPTED_DATABASE_PRIOR` と `DB prior: sphere.csv` locator はそのまま維持する。参考の Proposition 番号を独立の出典証明として昇格させていない。

R6 終了監査は検証済み ProofStep **50件**、Reference **8件**、未解決 Goal **0件**、公開 Web `generic-complete-proof` を確認した。$\pi_3^2,\pi_4^3,\pi_5^3,\pi_6^4,\pi_6^3$ の Web 回帰はすべて PASS。限定 pytest 10セットが PASSし、Phase 末尾のアクティブ `tests/` 全体 pytest は `3546 passed in 107.52s (0:01:47)`、終了コード0である。終了証拠は `%LOCALAPPDATA%/EHPProofTracerRecovery/phase172_r6_20261031_144642_024616Z/closeout.json` と関連ログに保存した。Gate の実行 HEAD は `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a`。

Phase 172 は**表示品質の改善の認定**であり、新しい数学的定理の証明、任意のホモトピー群の完成、出典データベース全体の検証を意味しない。過去の Phase 171 数学的証明の記録は履歴として維持する。
"""

APPENDS = {
    "docs/design.md": DESIGN_ADDENDUM,
    "docs/development_log.md": DEVELOPMENT_ADDENDUM,
    "docs/roadmap.md": ROADMAP_ADDENDUM,
    "docs/proof_records.md": PROOF_ADDENDUM,
}


def make_revision(path: str, original: bytes) -> bytes:
    """Return a *complete* revised file; preserve historical bytes."""
    if not isinstance(original, bytes):
        raise TypeError("original document must be bytes")
    text = original.decode("utf-8-sig")
    if MARKER in text:
        raise ValueError("Phase 172 closeout already exists")
    newline = "\r\n" if original.count(b"\r\n") > original.count(b"\n") // 2 else "\n"
    if path == "README.md":
        anchor = b"<!-- PHASE171_FINAL_CLOSEOUT_20261031 -->"
        old_heading = "## Current status — Phase 171 closed (2026-10-31)".encode("utf-8")
        historical_heading = "## Historical closeout — Phase 171 (2026-10-31)".encode("utf-8")
        if original.count(anchor) != 1 or original.count(old_heading) != 1:
            raise ValueError("unreviewed README status structure")
        new_section = README_CURRENT.replace("\n", newline).encode("utf-8")
        return original.replace(anchor, new_section + anchor, 1).replace(
            old_heading, historical_heading, 1,
        )
    elif path in APPENDS:
        addition = APPENDS[path]
    else:
        raise ValueError("unreviewed documentation path")
    # Keep every original byte unchanged; append a complete closure record.
    ending = b"" if original.endswith((b"\n", b"\r")) else newline.encode()
    payload = addition.replace("\n", newline).encode("utf-8")
    return original + ending + newline.encode() + payload

```

## `install.py`（全文・新規追加位置：リポジトリ直下 `phase172_r6r2_document_closeout/install.py`）

```python
"""Phase 172 R6R2: five-document closeout using one already passed R6 gate.

This installer NEVER runs the full pytest suite and NEVER changes production
code. All five *complete* revised documents are saved before optional apply.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from .sections import APPENDS, MARKER, make_revision

ROOT = Path(__file__).resolve().parent.parent
REPORT_NAME = "phase172_r6_20261031_144642_024616Z"
REVIEWED_HEAD = "6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a"
DOC_BLOBS = {
    "README.md": "98fef702205b8a0aea416e6958557657520d7479",
    "docs/design.md": "b0f6e2c77aeb5817127ce2c38d390bfa3ff67433",
    "docs/development_log.md": "afb83495fbaef9dc28ccceb944b758cd9608232a",
    "docs/roadmap.md": "415e8af933c43da99ea0ae987ec7dd9ae1673398",
    "docs/proof_records.md": "1b39992cff566eb3bf7540ff32ede2b262f2056e",
}
REVIEWED_RENDERER_BLOB = "6bfd5e992f6c9ee9441920e10e63e0db4bece289"
TARGETS = ((2, 1), (3, 1), (3, 2), (4, 2), (3, 3))


def command(*args: str, timeout: int = 90) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", timeout=timeout,
        check=False,
    )


def checked(*args: str) -> str:
    process = command(*args)
    if process.returncode:
        raise RuntimeError("command failed: " + repr(args) + " " + process.stderr[-1200:])
    return process.stdout.strip()


def read_closeout_report(directory: Path) -> dict[str, object]:
    """Inspect immutable, *previously run* R6 evidence; do not repeat pytest."""
    path = directory / "closeout.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("result") != "PASS_PHASE172_R6_FULL_CLOSEOUT_GATE":
        raise RuntimeError("R6 closeout did not pass")
    if report.get("phase") != "172-R6" or report.get("tracked_unchanged") is not True:
        raise RuntimeError("R6 phase or tracked-state gate is invalid")
    state = report.get("state", {})
    if (state.get("head") != REVIEWED_HEAD
            or state.get("origin_develop") != REVIEWED_HEAD
            or state.get("renderer_state") != "R5_COMMITTED"):
        raise RuntimeError("R6 reviewed HEAD/renderer state differs")
    focused = report.get("focused", [])
    if (not isinstance(focused, list) or len(focused) != 10
            or {row.get("group") for row in focused} != set(range(1, 11))
            or any(row.get("exit_code") != 0 for row in focused)):
        raise RuntimeError("R6 focused test gate is incomplete")
    groups = report.get("public_groups", [])
    if (not isinstance(groups, list) or len(groups) != 5
            or {(row.get("n"), row.get("k")) for row in groups} != set(TARGETS)
            or any(row.get("web_key") != "generic-complete-proof"
                   or row.get("partial") is not False for row in groups)):
        raise RuntimeError("R6 Web gate is incomplete")
    pi63 = next(row for row in groups if (row["n"], row["k"]) == (3, 3))
    if (pi63.get("proof_steps") != 50 or pi63.get("reference_count") != 8
            or pi63.get("open_goals") != 0
            or pi63.get("internal_db_prior_references") != [2, 8]
            or pi63.get("presentation_gate") != "PASS"
            or pi63.get("trust_boundary") != "PASS"):
        raise RuntimeError("R6 pi63 proof/Reference gate is invalid")
    full = report.get("active_full_pytest", {})
    if (full.get("passed") != 3546 or full.get("exit_code") != 0):
        raise RuntimeError("R6 active suite PASS summary is invalid")
    log = (directory / "full_active_pytest.log").read_text(encoding="utf-8")
    if len(re.findall(r"\b3546 passed in 107\.52s", log)) != 1:
        raise RuntimeError("R6 full pytest evidence does not match the report")
    markdown = (directory / "pi_6_3_web_narrative.md").read_text(encoding="utf-8")
    for token in (
        "[R2] 先行データベース結果", "[R8] 先行データベース結果",
        r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.",
        r"\operatorname{ord}(\nu')=4", r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}",
    ):
        if token not in markdown:
            raise RuntimeError("R6 final Web evidence lacks " + token)
    if "DB prior: sphere.csv" in markdown.split("\n証明\n", 1)[0]:
        raise RuntimeError("R5 public locator improvement missing")
    return report


def preflight(directory: Path) -> dict[str, str]:
    if checked("git", "branch", "--show-current") != "develop":
        raise RuntimeError("the develop branch is required")
    head = checked("git", "rev-parse", "HEAD")
    if head != REVIEWED_HEAD:
        raise RuntimeError("unreviewed HEAD; expected R6 verified commit")
    remote = command("git", "ls-remote", "origin", "refs/heads/develop", timeout=35)
    if remote.returncode or not remote.stdout.strip():
        raise RuntimeError("origin/develop unavailable")
    if remote.stdout.split()[0] != head:
        raise RuntimeError("origin/develop differs from the reviewed HEAD")
    if checked("git", "status", "--porcelain", "-uno"):
        raise RuntimeError("unexpected existing tracked changes")
    if checked("git", "diff", "--cached", "--name-only"):
        raise RuntimeError("the Git index contains changes")
    for path, blob in DOC_BLOBS.items():
        if checked("git", "rev-parse", "HEAD:" + path) != blob:
            raise RuntimeError("reviewed document Git blob differs: " + path)
        if not (ROOT / path).is_file():
            raise RuntimeError("document is absent: " + path)
    if checked("git", "rev-parse", "HEAD:phase168_r3_5_model_renderer.py") != REVIEWED_RENDERER_BLOB:
        raise RuntimeError("Renderer is not the completed R5 implementation")
    read_closeout_report(directory)
    return {"branch": "develop", "head": head, "remote": head,
            "document_guard": "PASS", "r6_report": str(directory)}


def output_dir() -> Path:
    appdata = Path(os.environ.get("LOCALAPPDATA") or Path.home())
    parent = appdata / "EHPProofTracerRecovery"
    parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    directory = parent / ("phase172_r6r2_document_closeout_" + now)
    directory.mkdir(parents=True, exist_ok=False)
    return directory


def revised_documents() -> tuple[dict[str, bytes], dict[str, bytes]]:
    originals: dict[str, bytes] = {}
    updated: dict[str, bytes] = {}
    for path in DOC_BLOBS:
        original = (ROOT / path).read_bytes()
        revision = make_revision(path, original)
        if revision == original or MARKER.encode("utf-8") not in revision:
            raise RuntimeError("document generation did not add Phase 172 closure")
        originals[path] = original
        updated[path] = revision
    return originals, updated


def save_full_documents(output: Path, originals: dict[str, bytes], updated: dict[str, bytes]) -> None:
    """Write FIVE complete replacement files, not truncated diffs."""
    for path in DOC_BLOBS:
        destination = output / "full_documents" / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(updated[path])
        original = output / "backup_original" / path
        original.parent.mkdir(parents=True, exist_ok=True)
        original.write_bytes(originals[path])
        if destination.read_bytes() != updated[path]:
            raise RuntimeError("failed to verify complete document: " + path)


def run_focused_tests(output: Path) -> None:
    filename = output / "focused_pytest.log"
    process = command(sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
                      "-p", "no:cacheprovider",
                      "phase172_r6r2_document_closeout/tests/test_sections.py", timeout=120)
    filename.write_text(process.stdout + "\n" + process.stderr, encoding="utf-8")
    if process.returncode:
        raise RuntimeError("document-only focused pytest failed: " + process.stdout[-1200:])
    print("PHASE172_R6R2_DOCUMENT_TESTS=PASS", flush=True)


def restore(originals: dict[str, bytes]) -> None:
    for path, value in originals.items():
        (ROOT / path).write_bytes(value)


def apply_documents(originals: dict[str, bytes], updated: dict[str, bytes]) -> None:
    """Install reviewed full files, then check all five names and exact bytes."""
    try:
        for path, data in updated.items():
            destination = ROOT / path
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=destination.parent, delete=False,
                prefix=".phase172_r6r2_", suffix=".tmp",
            ) as stream:
                stream.write(data)
                temporary = Path(stream.name)
            try:
                os.replace(temporary, destination)
            finally:
                temporary.unlink(missing_ok=True)
        changed = set(checked("git", "diff", "--name-only").splitlines())
        if changed != set(DOC_BLOBS):
            raise RuntimeError("unexpected changed file set: " + repr(sorted(changed)))
        if command("git", "diff", "--check").returncode:
            raise RuntimeError("git diff --check failed")
        for path, data in updated.items():
            if (ROOT / path).read_bytes() != data:
                raise RuntimeError("complete document bytes differ: " + path)
    except BaseException:
        restore(originals)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report-dir", default=None)
    args = parser.parse_args()
    if args.dry_run == args.apply:
        parser.error("choose exactly one of --dry-run or --apply")
    base = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "EHPProofTracerRecovery"
    report_dir = Path(args.report_dir) if args.report_dir else base / REPORT_NAME
    state = preflight(report_dir)
    print("PHASE172_R6R2_BRANCH=" + state["branch"], flush=True)
    print("PHASE172_R6R2_HEAD=" + state["head"], flush=True)
    print("PHASE172_R6R2_R6_EVIDENCE=PASS", flush=True)
    print("PHASE172_R6R2_DOC_CONTENT_GUARD=PASS", flush=True)
    output = output_dir()
    originals, updated = revised_documents()
    save_full_documents(output, originals, updated)
    print("PHASE172_R6R2_FULL_DOCUMENTS=" + str(output / "full_documents"), flush=True)
    if args.dry_run:
        print("PHASE172_R6R2_DRY_RUN=PASS", flush=True)
        print("PHASE172_R6R2_SOURCE_CHANGES=0", flush=True)
        return 0
    run_focused_tests(output)
    apply_documents(originals, updated)
    record = {
        "phase": "172-R6R2", "result": "PASS_PHASE172_DOCUMENT_CLOSEOUT",
        "phase_end_gate": "PASS_PHASE172_R6_FULL_CLOSEOUT_GATE",
        "r6_head": REVIEWED_HEAD, "active_full_pytest": {"passed": 3546, "seconds": 107.52},
        "full_suite_executed_in_this_document_step": False,
        "documents": list(DOC_BLOBS),
        "full_documents": str(output / "full_documents"),
    }
    (output / "document_closeout.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE172_R6R2_DOCUMENTS=5", flush=True)
    print("PHASE172_R6R2_FULL_SUITE_EXECUTED=NO", flush=True)
    print("PHASE172_R6R2_RESULT=PASS_PHASE172_DOCUMENT_CLOSEOUT", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## `tests/test_sections.py`（全文・新規追加位置：リポジトリ直下 `phase172_r6r2_document_closeout/tests/test_sections.py`）

```python
"""Document-only regression checks; no full mathematical test suite."""
from __future__ import annotations

import pytest

from phase172_r6r2_document_closeout.sections import (
    APPENDS, DESIGN_ADDENDUM, DEVELOPMENT_ADDENDUM, MARKER,
    PROOF_ADDENDUM, README_CURRENT, ROADMAP_ADDENDUM, make_revision,
)
from phase172_r6r2_document_closeout.install import DOC_BLOBS


def test_complete_readme_revision_preserves_history_and_updates_current():
    old = (
        "# EHP Proof Tracer\n\nIntroduction.\n\n"
        "<!-- PHASE171_FINAL_CLOSEOUT_20261031 -->\n\n"
        "## Current status — Phase 171 closed (2026-10-31)\n"
        "Older text.\n"
    ).encode("utf-8")
    updated = make_revision("README.md", old)
    assert updated.startswith(b"# EHP Proof Tracer")
    assert b"Older text." in updated
    assert MARKER.encode() in updated
    assert b"3546 passed in 107.52s" in updated
    assert "Historical closeout" in updated.decode("utf-8")
    assert "Phase 172 closed" in updated.decode("utf-8")
    assert len(updated) > len(old)


def test_append_revisions_preserve_every_original_byte():
    original = "# 日本語の記録\r\n\r\n過去の段落\r\n".encode("utf-8")
    for path in APPENDS:
        updated = make_revision(path, original)
        assert updated.startswith(original)
        assert MARKER.encode("utf-8") in updated
        assert b"\r\n" in updated
        assert len(updated) > len(original)


def test_unfinished_or_duplicated_closeout_is_rejected():
    with pytest.raises(ValueError):
        make_revision("docs/roadmap.md", MARKER.encode("utf-8"))
    with pytest.raises(ValueError):
        make_revision("README.md", b"# Invalid README\n")
    with pytest.raises(ValueError):
        make_revision("docs/unknown.md", b"# Unknown\n")


def test_required_phase_boundaries_and_reference_trust_remain_explicit():
    assert "ADOPTED_DATABASE_PRIOR" in DESIGN_ADDENDUM
    assert "ADOPTED_DATABASE_PRIOR" in PROOF_ADDENDUM
    assert "independently authenticated" in README_CURRENT
    assert "全体 pytest を**1回**" in DEVELOPMENT_ADDENDUM
    assert "次 Phase は未決定" in ROADMAP_ADDENDUM


def test_exactly_five_reviewed_document_paths():
    assert set(DOC_BLOBS) == {"README.md", *APPENDS}
    assert len(DOC_BLOBS) == 5


def test_additional_document_text_is_utf8_and_not_abridged():
    for path, text in APPENDS.items():
        assert path.startswith("docs/")
        assert MARKER in text
        assert len(text.encode("utf-8")) > 500
        assert "Phase 172" in text
    assert "Phase 172" in README_CURRENT

```

## `run.ps1`（全文・新規追加位置：リポジトリ直下 `phase172_r6r2_document_closeout/run.ps1`）

```powershell
param(
    [switch]$DryRun,
    [switch]$Apply,
    [string]$ReportDir = ""
)
$ErrorActionPreference = 'Stop'
if ($DryRun -eq $Apply) {
    throw 'Select exactly one of -DryRun or -Apply'
}
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $params = @()
    if ($DryRun) {
        $params += '--dry-run'
    } else {
        $params += '--apply'
    }
    if ($ReportDir -ne '') {
        $params += '--report-dir'
        $params += $ReportDir
    }
    & python -B -m phase172_r6r2_document_closeout.install @params
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 document closeout failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

```

