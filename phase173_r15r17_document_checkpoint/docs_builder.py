"""Phase 173 R15R17 documentation checkpoint: full-file generation with strict guards.

Only verified R15R17 results are recorded. Browser visualization and phase-end
full pytest remain pending; existing historical text is preserved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


REVIEWED_BASE = "80e51d4c22f80e597e48a2f899eecac8ded8595d"
DOCUMENT_BLOBS = {
    "README.md": "1dac05e0f7310771009d307d8f535c6de3632a45",
    "docs/design.md": "43cc766ce00e4867f43ea656b2bfccbdc0730e45",
    "docs/development_log.md": "a7c35c69785124c7748c3dd31e1a96d8e72a2ca7",
    "docs/roadmap.md": "7bbdff53070bc60fb49ec41b209e1a568c868fc9",
    "docs/proof_records.md": "10256a08c44626fd82ad9764703dceeed729e87c",
}
MARKER = "<!-- PHASE173_R15R17_CHECKPOINT_20261104 -->"

README_BLOCK = """<!-- PHASE173_R15R17_CHECKPOINT_20261104 -->

## Current status — Phase 173 R15R17 checkpoint (2026-11-04)

Phase 173 is in progress, **not formally closed**. The public incomplete-proof
path now incorporates the actual certified abstract proof ancestry into one
`ProofNarrativeModel` and one common Narrative renderer. A single Reference
section retains the source-backed evidence; a separately rendered abstract-tree
appendix is not emitted on the model-backed Web path. This is presentation
integration, not a new mathematical inference.

For the reviewed targets, the verified abstract structure is not promoted to a
completed named-generator proof. In particular, the source-backed abstract
structure $\\pi_{12}^{4}\\cong\\mathbb Z/2$ does not establish the named
presentation $\\pi_{12}^{4}=\\mathbb Z/2\\{\\varepsilon_4\\}$. Typed pending
goals remain in the search result even when equivalent group presentations are
combined into a single display entry. The partial status of $\\pi_{13}^{4}$
and $\\pi_8^5$ is retained; $\\pi_8^4$ remains a completed proof.

On 2026-11-04, the R15R17 R3R4 focused historical-test contract run reported
**92 passed**. R3R5 exercised actual Flask-generated HTTP output for four cases
($n,k$ = (4,8), (4,9), (5,3), (4,4)); **4 HTTP tests passed**, with one Reference
section per case, no redundant abstract sidecar, and the correct named-proof
status. The HTML parser contract reported **4 passed**. These are separate,
limited test runs; they do **not** constitute the phase-end full suite.

**Still pending:** manual visual review of MathJax/layout in a browser,
Phase 173 documentation closeout, and the phase-end active `tests/` full pytest
(which is run once, at the end of the phase). No Phase 173 full-suite result
has been claimed here.

"""

DESIGN_BLOCK = """<!-- PHASE173_R15R17_CHECKPOINT_20261104 -->

## Phase 173 R15R17 — 証明表示の単一 Model 統合と未完成状態の境界（2026-11-04、終了前）

Phase 173 は継続中であり、本節は R15R17 の HTTP 監査までの確認結果である。公開経路では、型付き Backward Search（逆向き探索）結果と別に Certified Abstract Structure（検証済み抽象群構造）が存在する場合、実際の検証済み ProofStep の祖先を **同一の `ProofNarrativeModel`** に取り込む。Reference（引用文献）を一か所に投影し、共通 Narrative Renderer（文章表示器）で一度だけ描画する。個別 $(n,k)$、生成元名または群名に対応した Narrative 分岐は追加しない。

検証済みの抽象群結論と記名生成元による群構造の完成証明は異なる。例えば $\\pi_{12}^{4}\\cong\\mathbb Z/2$ の抽象群構造が導けても、$\\varepsilon_4$ を生成元とする構造表示まで完成したとはみなさない。`PartialProofResult` の `status`、`conclusion`、`open_goals`、`diagnostics` は変更しない。`model.steps` には検証済みの抽象群祖先を表示用に追加するが、探索の `proven_steps` は不変とする。

内部の `CyclicStructureStatement`、順向きの `Relation`、逆向きの `Relation` は異なる Goal（未解決目標）として保持する。型付き群構造の一致を確認できる場合だけ公開表示を集約する。文字列の等値だけを証明上の等値とみなさない。参照先を持つ GIVEN（与件）で数式表示不能な内部型は本文へ生の Python 型名として出さず、その ProofStep と Citation の対応を維持する。

R3R4 は旧来の別 Section を要求する**公開 Web テスト契約**を統一後の経路に整えた。独立した legacy（互換経路）や補助 API の契約を一律に廃止していない。R3R5 の Flask HTTP 検査では、$(n,k)=(4,8),(4,9),(5,3),(4,4)$ の4件が 200 を返し、Reference は各1か所、model-backed 経路の旧抽象群 sidecar（追記部）は不在、証明状態は内部の検証済み状態と一致した。

**未確認：** ブラウザでの数式・レイアウトの目視確認、Phase 173 末尾のアクティブ `tests/` 全体 pytest、Phase 173 正式終了。旧 Phase の記録を改変しない。本節は新たな数学定理の証明や任意の群の証明完成を意味しない。
"""

DEVELOPMENT_BLOCK = """<!-- PHASE173_R15R17_CHECKPOINT_20261104 -->

## 2026-11-04 — Phase 173 R15R17：共通 Narrative 統合・表示・HTTP 監査（終了前）

R1 は `ProofNarrativeModel` に検索済み ProofStep と別途検証済みの抽象群証明木を統合した。元の探索結果や未解決 Goal は変更せず、単一の Reference と Renderer を公開 Web に接続した。Windows 実行で DryRun PASS、限定 pytest **19 PASS**。R2 は公開本文に残る表示不能な内部型名だけを抑制し、引用と証明木を保持した（限定 pytest **17 PASS**）。

R3 は Goal と旧テスト契約を監査し、`CyclicStructureStatement` と方向の違う `Relation` を別々の型付き未解決 Goal と確認した。監査用限定 pytest は **14 PASS**、実測4ケース、歴史的契約候補31か所。R3R3 は型付き意味が一致した Goal を**表示上だけ集約**した（限定 pytest **24 PASS**）。R3R4 は独立 API テストを維持しつつ公開 Web に関する旧 Section の期待値を修正し、テスト10ファイルの限定 pytest **92 PASS**。R3R5 は Flask `test_client` による HTTP 出力の4ケースで **4 PASS**、HTML parser の契約テスト **4 PASS**、Reference 各1か所、旧 sidecar なし、抽象群証明・記名証明の未完成区別維持を確認した。

R3R5 の実行ログは `R15R17R3R5_SOURCE_GUARD=PASS`、`R15R17R3R5_HTTP_GATE=PASS`、`R15R17R3R5_GIT_INDEX_PRESERVED=PASS`、`R15R17R3R5_AUDIT_COMPLETE=PASS`。引き継ぎ DryRun は `PHASE173_R15R17_HTTP_GATE=PASS_REPORTED_BY_USER_2026-11-04`、Git HEAD `80e51d4c22f80e597e48a2f899eecac8ded8595d`、本体書込みなし。これらの PASS 件数は**異なる限定スイート**であり合計を全体テスト件数として扱わない。

**残作業：** ブラウザ目視、文書の正式 Closeout 更新、Phase 173 末尾の一度だけのアクティブ `tests/` 全体 pytest。現時点で Phase 173 終了は宣言しない。旧ログは削除せず追記する。
"""

ROADMAP_BLOCK = """<!-- PHASE173_R15R17_CHECKPOINT_20261104 -->

## Phase 173 — R15R17 HTTP Gate 通過後の終了前計画（2026-11-04）

**現在の段階：** R15R17 の共通 Proof Narrative Model（証明文章モデル）・Reference（引用）・Renderer（表示器）統合、型付き Goal の表示集約、歴史的公開 Web テストの整合化は実装・限定テスト済み。Flask HTTP の4対象 $(n,k)=(4,8),(4,9),(5,3),(4,4)$ は監査 PASS。Phase 173 自体は未終了。

残る依存は (1) 実ブラウザにおける MathJax 数式と画面構成の目視確認、(2) 本チェックポイント記録のレビューと最終文書更新、(3) Phase 末尾で一度だけ行うアクティブ `tests/` の全体 pytest、(4) Git 差分・監査結果・未完成範囲の確認による正式 Closeout である。

**次 Phase との境界：** 記名生成元を含む $pi_{12}^{4}$ や $pi_{13}^{4}$ の未解決 Goal を証明完了にする新規数学規則、任意の $n,k$ への証明一般化、既存の Legacy API の一括削除は本 R15R17 の表示・監査作業には含めない。新しい ProofStep をでっち上げてステータスを昇格させない。
""".replace("\x01pi", "\\pi")

PROOF_BLOCK = """<!-- PHASE173_R15R17_CHECKPOINT_20261104 -->

## 2026-11-04 — Phase 173 R15R17：抽象群の検証済み結論と記名 Goal の区別

型付き Backward Search（逆向き探索）による命題 $\\pi_{12}^{4}=\\mathbb Z/2\\{\\varepsilon_4\\}$ は未完成である。他方、出典付きの実際の検証済み ProofStep により抽象群構造

$$
\\pi_{12}^{4}\\cong\\mathbb Z/2
$$

は証拠を持つ。これらを同一の完成証明と取り違えない。R15R17 の Narrative Model（文章モデル）は抽象群の ProofStep の祖先を一つの証明表示に含めるが、記名 Goal の `search_failed`、`conclusion=None`、`open_goals` を維持する。

$pi_{13}^{4}$ でも検証済みの抽象群構造と記名生成元の未完成を区別する。$pi_8^5$ は抽象群証明書を持たない未完成例、$pi_8^4$ は完成例として表示状態が保持された。今回追加したのは表示統合・引用の一元化・型付き Goal の表示集約とテスト契約であり、独立の数学的推論や文献上の新しい定理ではない。

R3R5 の Flask HTTP 監査は 4ケースで各 Reference 1か所、追加 sidecar なし、抽象群証明書の有無と記名群の完成・未完成の区別を確認した（4 HTTP PASS）。原典の数学的真理の全面確認、ブラウザ上の数式描画の目視検査、Phase 173 の全体 pytest は含まない。全体テストと正式 Closeout は Phase 末尾に実施する。
""".replace("\x01pi", "\\pi")

APPENDS = {
    "docs/design.md": DESIGN_BLOCK,
    "docs/development_log.md": DEVELOPMENT_BLOCK,
    "docs/roadmap.md": ROADMAP_BLOCK,
    "docs/proof_records.md": PROOF_BLOCK,
}


def apply_document_update(path: str, original: bytes) -> bytes:
    """Generate the complete Markdown file, preserving every historical byte."""
    if path not in DOCUMENT_BLOBS:
        raise ValueError("unreviewed document path")
    marker = MARKER.encode("utf-8")
    if marker in original:
        raise ValueError("checkpoint already applied or a duplicate marker exists")
    if path == "README.md":
        anchor = b"<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->"
        if original.count(anchor) != 1:
            raise ValueError("unreviewed README anchor")
        historical_title = b"## Current status \xe2\x80\x94 Phase 172 closed (2026-10-31)"
        if original.count(historical_title) != 1:
            raise ValueError("unreviewed Phase 172 heading")
        updated = original.replace(anchor, README_BLOCK.encode("utf-8") + anchor, 1)
        updated = updated.replace(
            historical_title,
            b"## Historical closeout \xe2\x80\x94 Phase 172 (2026-10-31)",
            1,
        )
    else:
        if not original.startswith(b"# EHP Proof Tracer"):
            raise ValueError(f"unreviewed document title: {path}")
        newline = b"\r\n" if original.endswith(b"\r\n") else b"\n"
        block = APPENDS[path].encode("utf-8").replace(b"\n", newline)
        updated = original + newline + block
    if updated.count(marker) != 1:
        raise ValueError("missing or duplicate checkpoint marker")
    if len(updated) <= len(original):
        raise ValueError("checkpoint must retain all historical content")
    return updated


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    process = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if check and process.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {process.stderr.strip()}")
    return process


def verify_repository(repo: Path) -> None:
    if git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() != "develop":
        raise RuntimeError("expected develop branch")
    actual_repo = Path(git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if actual_repo != repo.resolve():
        raise RuntimeError("ZIP must be extracted at the repository root")
    for ref in ("HEAD", "origin/develop"):
        if git(repo, "merge-base", "--is-ancestor", REVIEWED_BASE, ref, check=False).returncode:
            raise RuntimeError(f"{ref} is not a descendant of the reviewed Phase 173 HEAD")
    if git(repo, "merge-base", "--is-ancestor", "HEAD", "origin/develop", check=False).returncode:
        raise RuntimeError("local HEAD diverged from origin/develop")
    for path, expected in DOCUMENT_BLOBS.items():
        if git(repo, "diff", "--quiet", "HEAD", "--", path, check=False).returncode:
            raise RuntimeError(f"local document has unreviewed changes: {path}")
        if git(repo, "diff", "--cached", "--quiet", "--", path, check=False).returncode:
            raise RuntimeError(f"staged document has unreviewed changes: {path}")
        actual = git(repo, "rev-parse", f"HEAD:{path}").stdout.strip()
        if actual != expected:
            raise RuntimeError(f"document content changed on GitHub, needs rereview: {path}")
        if not (repo / path).is_file():
            raise RuntimeError(f"missing tracked document: {path}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".phase173_doc_", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        if path.exists():
            os.chmod(temporary, path.stat().st_mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)


def generate_files(repo: Path, package: Path, apply: bool) -> None:
    """Write all five full-file previews; on apply, replace verified tracked docs."""
    verify_repository(repo)
    preview_dir = package / "full_documents"
    preview_dir.mkdir(parents=True, exist_ok=True)
    documents = {}
    originals = {}
    for path in DOCUMENT_BLOBS:
        original = (repo / path).read_bytes()
        generated = apply_document_update(path, original)
        originals[path] = original
        documents[path] = generated
        atomic_write(preview_dir / path, generated)
        print(f"PHASE173_DOC_FULL_FILE={path} ORIGINAL_BYTES={len(original)} COMPLETE_BYTES={len(generated)}")
    status_before = git(repo, "diff", "--cached", "--name-status").stdout
    if apply:
        backup_dir = package / "original_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        for path, content in originals.items():
            atomic_write(backup_dir / path, content)
        try:
            for path, content in documents.items():
                atomic_write(repo / path, content)
            for path, content in documents.items():
                if (repo / path).read_bytes() != content:
                    raise RuntimeError(f"document post-write mismatch: {path}")
        except BaseException:
            for path, content in originals.items():
                atomic_write(repo / path, content)
            raise
        (package / "installed_state.json").write_text(json.dumps({
            "reviewed_base": REVIEWED_BASE,
            "paths": {path: {"before": sha256(originals[path]),
                             "after": sha256(documents[path])}
                      for path in DOCUMENT_BLOBS},
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if git(repo, "diff", "--cached", "--name-status").stdout != status_before:
        raise RuntimeError("Git index changed during documentation generation")
    print("PHASE173_R15R17_DOCS_GIT_INDEX_PRESERVED=PASS")
    print("PHASE173_R15R17_DOCS_FULL_OUTPUT=phase173_r15r17_document_checkpoint/full_documents/")
    print(f"PHASE173_R15R17_DOCS_{'INSTALL' if apply else 'DRY_RUN'}=PASS")
    if not apply:
        print("PHASE173_R15R17_DOCS_PRODUCTION_WRITES=NONE")
    print("PHASE173_R15R17_PHASE_END_FULL_PYTEST=NOT_RUN")
    print("PHASE173_R15R17_BROWSER_VISUAL_VERIFIED=UNCONFIRMED")


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 173 R15R17 full-file docs checkpoint")
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    generate_files(args.repo.resolve(), args.package.resolve(), args.apply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
