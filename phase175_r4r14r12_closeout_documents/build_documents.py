"""Phase 175 R4R14R12: retain complete Markdown history and write full files.

Only the five named documentation files are updated. The repository is never
committed, reset, staged, or used for an automatic full pytest invocation.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

PACKAGE = "phase175_r4r14r12_closeout_documents"
REVIEWED_HEAD = "29a06166390c21a30d7a0bd4144597dd16eb2f56"
DOCUMENT_BLOBS = {
    "README.md": "05ead0862c7bb285d26d50a30bc0b0c464b16cf3",
    "docs/design.md": "d7e32354284f6a8ec51e8f2e2b73531ed2251e05",
    "docs/development_log.md": "f2d6c3e0b04f27a06ca201f7545f78b02756acb3",
    "docs/roadmap.md": "03a3665635b47f39a7db9bec9916d8f35b771dce",
    "docs/proof_records.md": "4d94b48965aab0ec5d248e4c499c866efc1597af",
}
MARKER = "PHASE175_R4R14R12_DOCS_20261119"

README_NOTE = """<!-- PHASE175_R4R14R12_DOCS_20261119 -->

## Current development status — Phase 175 closeout pending (2026-11-19)

Phase 175 has completed the six registered k=4 group proofs (sphere dimensions n=2 through n=7). The latest read-only R4R14R11 preflight observed `complete` and zero open goals for the three formerly unfinished groups `(n,k)=(3,4), (5,4), (6,4)`. This is evidence for these registered targets, **not** for all unstable homotopy groups or all published statements.

For `(6,4)`, the shared source-first search proves $\\pi_{10}^{6}=0$. The R4R14R10 audit verified the canonical 14-step proof tree, with four cited locators: Proposition 4.2 (4.4), (5.1), Proposition 5.8, and (5.9). The argument combines the cited $\\pi_{9}^{5}=\\mathbb Z/2\\{\\nu_5\\eta_8\\}$ with the independently inferred $E(\\nu_5\\eta_8)=0$, then applies surjectivity of $E$ from EHP exactness. The literature GIVEN remains distinct from the adopted DB GIVEN; no conclusion GIVEN or specialized narrative was added.

Focused evidence: R4R14R9R2 `44 passed, 4 deselected`; R4R14R10 `23 passed`; R4R14R11 `9 passed`. Four historically pinned Phase 174 Source Guard tests remain known failures on the modern HEAD; their failures have not been reclassified as passing. **The Phase 175 full pytest and final closeout gate have not run.** Historical Phase 174 closure below remains a separate, dated record.

"""
DESIGN_NOTE = """<!-- PHASE175_R4R14R12_DOCS_20261119 -->

## Phase 175 の現行設計境界（2026-11-19・終了文書準備）

k=4 の登録6群について、R4R14R11 時点の実探索で当初未完成だった `(n,k)=(3,4),(5,4),(6,4)` はいずれも `complete`、Open Goal 0 件となった。これは対象登録群の実測であり、任意のホモトピー群への一般化ではない。

R4R14R9 は、文献由来の `FIXED_STATEMENT` に対応するリンク済み `GIVEN` ProofStep と、別途 `INFERENCE` で証明された生成元の零像を前提として有限巡回群上の写像の零像を導く。文献出典の locator、position、Assertion Origin、元の ProofStep の一致を確認する。R40/R41 の DB 専用検証を緩めたり、DB GIVEN を文献 GIVEN に偽装したりしない。共有 Proof Search の First Successful Proof Search と一般規則の境界を維持する。

R4R14R10 は $\\pi_{10}^{6}=0$ の実探索で 14 ステップの Verified Proof Tree を確認した。EHP 完全性による $E$ の全射性、Proposition 5.8 の先行巡回群、Toda (5.9) による生成元の零像、`im E=0` から零群への推論は、すべて既存の共通 Renderer へ渡す。新しい専用 Narrative は追加していない。

Phase 174 の旧 Source Guard テスト4件は古い固定 HEAD／関数スナップショットに依存して現在の HEAD では失敗する。R4R14R9R2 はテストの削除・改変や条件緩和を行わず、現行限定テストから明示的に分離した。これらは PASS ではなく既知の未解決履歴として維持する。Phase 175 の全体 pytest および正式終了 Gate は未実施である。

"""
ROADMAP_NOTE = """<!-- PHASE175_R4R14R12_DOCS_20261119 -->

## Phase 175：R4R14R12 終了文書整備後の工程（2026-11-19）

登録された k=4 の6群について、R4R14R11 により当初未完成の3群 `(3,4),(5,4),(6,4)` もすべて `complete`／Open Goal 0 件であることが確認された。R4R14R10 は $\\pi_{10}^{6}=0$ の14ステップ・出典4件の証明木を監査済み。これは Phase 175 の数学的対象に関する到達点であり、Phase の正式終了ではない。

**終了前に残る義務：** (1) 旧 Phase 174 Source Guard 4件の歴史的な固定条件と現行 HEAD でのテスト運用を区別し、既知失敗を隠さない。(2) `.pytest_cache` の追跡差分がある場合は数学的コード変更と混同せず、ユーザーの変更を無断で破棄しない。(3) 主要5文書の全文出力・内容・Git 差分を確認する。(4) Phase 175 の末尾に限り全体 pytest を実行し、失敗時は証拠を保全する。(5) 最終 Gate で実測結果、Reference、出典の属性、変更ファイルを審査して正式 Closeout 可否を決める。

**次 Phase の境界：** k=4 の登録対象外の群、未完成の記名生成元 Goal、文献全件の独立数学検証、Phase 176 の新機能は今回先取りしない。Source-first、共通 Verified Proof Tree → ProofNarrativeModel → Renderer → Web、および First Successful Proof Search を維持する。

"""
LOG_NOTE = """<!-- PHASE175_R4R14R12_DOCS_20261119 -->

## 2026-11-19 — Phase 175 R4R14R9〜R4R14R12（終了文書準備）

- **R4R14R9：** 文献由来の先行巡回群 `FIXED_STATEMENT` を、出典属性とリンク済み ProofStep の厳密な一致によって認証し、別途証明された生成元の零像と組み合わせて `ImageZeroStatement(E)` を導く一般推論を共有探索に接続。R40/R41 の DB 専用検証条件は維持。新規結論 GIVEN、専用 Narrative は追加なし。
- **R4R14R9R1：** 複数テストディレクトリで同名の `test_rule.py` 等が衝突する pytest collection error を `--import-mode=importlib` で回避。
- **R4R14R9R2：** 旧 Source Guard 4件は現在の HEAD と歴史的固定値が異なるため失敗する。条件・テスト本文を変更せず今回の限定テストから明示的に分離。結果 `44 passed, 4 deselected`。この4件を PASS とは見なさない。
- **R4R14R10：** 実探索の $\\pi_{10}^{6}=0$ が `complete`、Open Goal 0 件、証明木14ステップと確認。出典 locator は `(5.1)`, `(5.9)`, `Proposition 4.2 (4.4)`, `Proposition 5.8`。文献 GIVEN と DB GIVEN の区別を証明木で監査。限定 pytest `23 passed`、新規 GIVEN 0。
- **R4R14R11：** Closeout Preflight の DryRun・本実行 PASS。旧未完成 k=4 群 `(3,4),(5,4),(6,4)` の実探索は全て `complete`、Open Goal 0 件。限定 pytest `9 passed`。Gate `PASS_R4R14R11_CLOSEOUT_PREFLIGHT_WITH_OPEN_POLICY`。確認 HEAD `28dcc4de13580a3f20faffa89353c11f897b1f8d`。旧 Source Guard 4件は未解決履歴として残存。
- **R4R14R12：** README と主要設計・履歴・ロードマップ・証明記録を、既存本文を保存した全文ファイルとして更新する文書工程。新規数学規則・GIVEN・共有 Provider・Renderer 変更なし。全体 pytest と Phase 最終 Gate はまだ実施していない。

この節は完了前の記録であり、Phase 175 の正式終了を宣言しない。
"""
PROOF_NOTE = """<!-- PHASE175_R4R14R12_DOCS_20261119 -->

## 2026-11-19 — Phase 175 k=4 の完成証明と出典の監査

登録6群のうち Phase 175 開始時点の未完成3群 `(n,k)=(3,4),(5,4),(6,4)` は、R4R14R11 実探索時点ですべて `complete`、Open Goal 0 件。旧3群の完成と合わせ、登録された k=4 の6群は完成状態と確認した。各群の具体的証明木について、全件が独立に文献全命題の真偽を証明したという認定ではない。

### $\\pi_{10}^{6}=0$（R4R14R10 監査）

出典4件：Proposition 4.2 (4.4)、Toda (5.1)、Proposition 5.8、Toda (5.9)。

$$
\\pi_{10}^{11}=0,\\qquad E:\\pi_9^5\\longrightarrow\\pi_{10}^{6}\\text{ は全射}.
$$

$$
\\pi_9^5=\\mathbb Z/2\\{\\nu_5\\eta_8\\},\\qquad
E(\\nu_5\\eta_8)=\\nu_6\\eta_9=0.
$$

生成元が零に写るので $\\operatorname{im}E=0$。一方 E は全射なので $\\pi_{10}^{6}=0$。この一般零像推論は文献由来 `GIVEN` と別途証明した `INFERENCE` を両方必要とする。R41 の DB 専用の ProofStep 検証を緩和しない。

実測 R4R14R10：`search_status=complete`、`open_goals=0`、Verified Proof Tree 14ステップ、4件の出典 locator、新規 GIVEN 0、限定 pytest `23 passed`。R4R14R11 でも `(6,4)` は `complete`／Open Goal 0 件を維持。

**検証境界：** 旧 Source Guard 4件の歴史的固定条件は未解決。Phase 175 の全体 pytest と最終 Gate は未実施であり、正式終了はまだ主張しない。
"""

NOTES = {
    "README.md": README_NOTE,
    "docs/design.md": DESIGN_NOTE,
    "docs/development_log.md": LOG_NOTE,
    "docs/roadmap.md": ROADMAP_NOTE,
    "docs/proof_records.md": PROOF_NOTE,
}


def call_git(root: Path, *args: str) -> str:
    result = subprocess.run(("git",) + args, cwd=root, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=False)
    if result.returncode:
        raise RuntimeError("GIT_ERROR: " + " ".join(args) + ": " + result.stderr.strip())
    return result.stdout.strip()


def insert_status(original: str, note: str) -> str:
    """Prepend after the top-level title; never delete a historical paragraph."""
    head, separator, tail = original.partition("\n")
    if not separator or not head.startswith("# "):
        raise ValueError("DOCUMENT_TITLE_MISSING")
    return head + "\n\n" + note + separator + tail


def render_full(path: str, original: str) -> str:
    """Maintain the complete original content and idempotent phase marker."""
    if MARKER in original:
        raise ValueError("ALREADY_UPDATED: " + path)
    note = NOTES[path]
    if path in ("README.md", "docs/design.md", "docs/roadmap.md"):
        return insert_status(original, note)
    return original.rstrip("\n") + "\n\n" + note


def preflight(root: Path) -> dict[str, object]:
    if Path(call_git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if call_git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    call_git(root, "merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD")
    if call_git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_CHANGES_REQUIRE_REVIEW")
    dirty = set(call_git(root, "diff", "--name-only").splitlines())
    if dirty.intersection(DOCUMENT_BLOBS):
        raise RuntimeError("EXISTING_DOCUMENT_EDITS_REQUIRE_REVIEW")
    for name, blob in DOCUMENT_BLOBS.items():
        if call_git(root, "rev-parse", "HEAD:" + name) != blob:
            raise RuntimeError("REVIEWED_DOCUMENT_HEAD_BLOB_DRIFT: " + name)
        if not (root / name).is_file():
            raise RuntimeError("DOCUMENT_MISSING: " + name)
    return {"head": call_git(root, "rev-parse", "HEAD"),
            "reviewed_base": REVIEWED_HEAD, "document_count": len(DOCUMENT_BLOBS),
            "dirty_other_files": sorted(dirty - set(DOCUMENT_BLOBS)),
            "historic_source_guard": "FOUR_KNOWN_FAILURES_NOT_RERUN"}


def execute(root: Path, *, dry_run: bool) -> dict[str, object]:
    metadata = preflight(root)
    originals = {name: (root / name).read_bytes() for name in DOCUMENT_BLOBS}
    new = {}
    for name, raw in originals.items():
        if not raw:
            raise RuntimeError("EMPTY_DOCUMENT: " + name)
        original = raw.decode("utf-8-sig")
        updated = render_full(name, original)
        if not updated.startswith(original.split("\n", 1)[0]):
            raise RuntimeError("TITLE_NOT_PRESERVED")
        if len(updated) <= len(original):
            raise RuntimeError("DOCUMENT_NOT_EXTENDED: " + name)
        new[name] = updated.encode("utf-8")
    meta = {"phase": "175_R4R14R12", "dry_run": dry_run,
            "gate": "PASS_R4R14R12_READ_ONLY_DRYRUN" if dry_run
            else "PASS_R4R14R12_FULL_DOCUMENT_FILES_WRITTEN",
            "preflight": metadata, "files": {}, "new_given": 0,
            "new_math_rules": 0, "full_pytest": "NOT_RUN",
            "phase_closed": False}
    for name in new:
        meta["files"][name] = {"before_bytes": len(originals[name]),
                                "after_bytes": len(new[name]), "full_file": True}
    if dry_run:
        return meta
    package = root / PACKAGE
    out = package / "output"
    if out.exists() and any(out.rglob("*.md")):
        raise RuntimeError("EXISTING_OUTPUT_REQUIRE_REVIEW")
    # Save the original entire files in the audit package before any modification.
    for name, data in originals.items():
        backup = package / "original" / name
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(data)
    for name, data in new.items():
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for name, data in new.items():
        (root / name).write_bytes(data)
    for name, data in new.items():
        if (root / name).read_bytes() != data or (out / name).read_bytes() != data:
            raise RuntimeError("OUTPUT_VERIFY_FAILED: " + name)
    return meta


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    report = {"phase": "175_R4R14R12", "gate": "FAIL_R4R14R12"}
    try:
        report = execute(root, dry_run=args.dry_run)
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    destination = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "EHP_Phase175_R4R14R12_documents.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("R4R14R12_GATE=" + str(report["gate"]))
    print("R4R14R12_REPORT=" + str(destination))
    if "error" in report:
        print("R4R14R12_ERROR=" + report["error"])
        return 1
    print("R4R14R12_DOCUMENT_COUNT=5")
    print("R4R14R12_FULL_PYTEST=NOT_RUN")
    print("R4R14R12_PHASE_CLOSED=FALSE")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
