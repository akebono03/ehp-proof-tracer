"""Phase 169 documentation closeout; reviewed full-file transformation only.

Does not invoke the full pytest suite, change production code, stage or commit files.
Generates complete copies of all five documents and backups outside the Git repo.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import traceback

sys.dont_write_bytecode = True

REPO_NAME = "akebono03/ehp-proof-tracer"
BASELINE_HEAD = "6e5d6bbed186dd4da706b54c308f94041a32e6d7"
REVIEWED_REMOTE_HEAD = "1e881f45b2f3f3ecbb1052750c9d7a7b5bf95712"
DOC_BLOBS = {
    "README.md": "c2c2c9236fdee03686518d05fa0ca7367b044a3b",
    "docs/design.md": "39f859dfe8a0ee208509efcb4dae7dc126812993",
    "docs/development_log.md": "9a68123a59d6acb2845ffc376aabc164a0102b45",
    "docs/roadmap.md": "0f5314a479a3549e99844ff8e0a94a4cf117023c",
    "docs/proof_records.md": "a993629e7ad2d4883f2c0d3e272eef47dcf29b9a",
}
SOURCE_BLOBS = {
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase168_r3_5_model_renderer.py": "4b4478ccbc20a4264be86e61b7a2c72f69b1e5b0",
    "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py": "daad1b7b246c4b005bd529637f82e64ce85a9cfe",
    "phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py": "f0664c1e28793f5a3ab341b17eb5e7ded0724436",
    "phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py": "9038d656aac21311a5272e4d62551cce435037c3",
    "phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py": "65f65b5bacdbec9cc4257b2c96140720568097a3",
    "phase169_r10et_r6_residual_definition_dependency_audit/audit.py": "ae883ad6ec24382dfc4bac26790a4a2b7e8fa54e",
}
DOC_MARKER = "<!-- PHASE169_FINAL_CLOSEOUT_20261028 -->"
REPORT_DIR_PREFIX = "phase169_closeout_r1_"
R6_EVIDENCE = "phase169_r10et_r6_residual_definition_dependency_audit/output/20261028_174644_215/audit.json"
R6_BLOB = "e00cb348d59679919189fab761025e0be9ca05dc"

README_CLOSE = r"""## Current status — Phase 169 closed (2026-10-28)

**Phase 169 is closed for its reviewed scope, not for all homotopy groups.** The completed work covers the 2-stem production path, theorem-based stable transport, direct-sum and composite-generator projection, shared generator-image Definition, root-reachable completed-proof references, and the relevant trust boundaries. The existing `HyoujiGen.csv` information continues to be used without adding generator-family-specific Definition implementations.

The independent R10ET R6D audit passed **19/19** scoped cases (16 required and 3 probes), with zero residual dependency on individual Definitions where the shared typed Definition was eligible. For $\\pi_{10}^{8}$, the search retains nine `ProofStep` objects; the completed narrative and references include only the eight steps reachable from the selected root, citing the used `sphere.csv (n=4,k=2)` DB premise and Toda (4.5). Partial-proof visibility is unchanged.

The final end-of-phase test run on **2026-10-28** passed **67 focused Phase 169/168 regression tests** and **3,546 active `tests/` tests**, with zero failed tests, zero errors, exit code 0, and preserved Git index. The closeout helper itself passed eight tests. Full-suite command: `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests`. The active suite retains the Phase 155 historical audit-only deselection boundary; archived tests are not silently counted as passes.

These results certify the stated implementation and test scope only. They do **not** establish complete proofs for arbitrary $\\pi_{n+k}^{n}$, certify the mathematical truth of every registered Toda or database statement, remove legacy individual Definitions, or prove that every stem is supported. The next phase is to audit remaining mathematical proof gaps and data coverage before selecting any new implementation work.

"""
DESIGN_CLOSE = r"""
<!-- PHASE169_FINAL_CLOSEOUT_20261028 -->

## Phase 169 終了時の設計境界（2026-10-28）

Phase 169 の正式な終了対象は、R10ET までにレビューした型付き逆向き探索、生成元像の共通 Definition、安定懸垂輸送、巡回群・直和群・合成生成元の証明表示、および完成証明の root 祖先に限定した本文・Reference の射影である。R10ET 文書区切りに記した「全体 pytest は未実施」はその時点の記録であり、本節の最終テストによって更新された。

共通 Definition は、安定範囲に適合する `GeneratorImage` の正規 `INFERENCE` を本番探索で優先する。既存の群構造 DB prior、Toda (4.5) による同型、生成元関係などの数学的前提を置き換えない。`HyoujiGen.csv` の型付き生成元データとの整合を保ち、特定の family 名に依存する新規規則を追加しない。

完全証明では、検証済み Proof Tree の root から到達できる ProofStep だけを Proof Narrative Model / Reference に射影する。Proof Tree 全体を削除せず、未完成証明の出力を変更しない。標準 Web の検証器を経ず、任意に与えられた Model を正式な証明と認証しない。Origin Observation も認証の代替とはしない。

最終テスト Gate は、関連回帰 **67 PASS**、現行アクティブ `tests/` **3546 PASS**、FAIL 0、ERROR 0、終了コード0、Git index 保全 PASS。Gate 自身の限定テスト **8 PASS**。実行コマンドは `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests`。`tests/conftest.py` の Phase 155 audit-only nodeid 除外を維持し、退避した歴史的テストを無制限に収集していない。

**認定境界：** この合格は Phase 169 で対象にしたコード・証明表示・有限個の回帰の終了判定であり、任意の stem や全登録群の自動証明、文献上の全命題の独立した形式認証を意味しない。残存する数学的・DB 上の未達事項は次 Phase の監査で確定する。既存 API、Trust Boundary、退避テストの扱いを変更しない。
"""
ROADMAP_CLOSE = r"""
<!-- PHASE169_FINAL_CLOSEOUT_20261028 -->

## Phase 169 — 正式終了（2026-10-28）

**状態：Phase 169 完了（検証済み対象範囲に限定）。** R10ET R5D の共通 Definition 本番優先、R6C の root 到達可能な引用、R6D の独立した19件監査、主要文書の R10ET Closeout R3A 整合性監査を完了した。終了時 Gate では関連回帰 **67 PASS**、アクティブな `tests/` **3546 PASS**、FAIL 0、ERROR 0、終了コード0、Git index 保全を確認した。事前の Gate 補助テストは **8 PASS**。古い Phase 169 計画に記載された「未実施」は過去時点の記述とし、この節を現在の終了状態とする。

終了条件は (1) 対象実装と限定監査の完了、(2) R10ET 文書5件と本体の整合性確認、(3) Phase 169 終了時の関連回帰と全アクティブテストの PASS、(4) Proof Tree・引用・Trust Boundary の回帰維持、(5) 本節および設計・開発ログ・証明記録の正式更新である。今回、テストまでの (1)〜(4) が既に PASS したことを前提に (5) を記録する。

### 次 Phase — 数学的残件・DB 適用範囲の監査（計画のみ）

次 Phase は、2-stem の低次群（$\\pi_4^2$、$\\pi_5^3$、$\\pi_6^4$）から、最新の Proof Tree・Reference・完了状態と登録 DB の根拠を再確認する。続いて他の stem の不完全な Goal、未採用の Toda 命題、`HyoujiGen.csv` と群構造・関係式 DB の整合、共通 Definition の非適用条件を監査する。未確認の対象が実際に不足している場合に限り、新 Phase で最小実装を計画する。

**先取りしない事項：** 全 stem の自動完成、旧 Definition 台帳の一括削除、Generator family 別の例外実装、新しい数学的認証機構、退避テストの一括復活。Phase 170 の実装範囲は未確定とする。
"""
LOG_CLOSE = r"""
<!-- PHASE169_FINAL_CLOSEOUT_20261028 -->

## 2026-10-28 — Phase 169 最終 Closeout（終了時テスト Gate・文書記録）

R10ET R5D〜R6D の実装と限定監査、R10ET Closeout R2A の主要文書5件全文更新、Closeout R3A の整合性検査を前提に、Phase 169 の終了時最終 Gate を Windows PowerShell から実行した。R3A は文書5/5、本体ソース8/8、R6対象19/19、Git index 保全を PASS とした。R10ET を再実装せず、終了判定のみ追加した。

### 終了時テスト（新規実行の記録）

- 実行日：2026-10-28（JST）。
- Gate 補助限定 pytest：**8 passed in 2.36s**（ユーザー実行ログ）。
- 関連回帰：**67 passed in 21.86s**、終了コード0。対象は Gate に明記された Phase 169 の10テストファイル（Phase 168 P19 回帰を含む）。
- 現行アクティブテスト：**3546 passed in 34.95s**、FAIL 0、ERROR 0、終了コード0。
- 全体テストコマンド：`python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests`。
- `tests/conftest.py` の Phase 155 audit-only nodeid 選別を維持し、歴史的退避テストは追加収集しない。`PYTHONDONTWRITEBYTECODE=1` と cacheprovider 無効化を使用した。
- Git index：実行前後の保全確認 `True`。Gate 判定：`PHASE169_CLOSEOUT_R1_TEST_GATE_PASS=True`、`TEST_GATE_PASS_PENDING_PHASE169_CLOSEOUT_DOCUMENTATION`。
- 最終 Gate 証拠は `%LOCALAPPDATA%\EHPProofTracerRecovery\phase169_closeout_r1_20261028_193510_755227\report.json` に保存された。本文書の文書更新 Gate はその JSON を読み直し、同じ回数と終了コードを検証している。

### 正式終了判断

**Phase 169 は、上記テストと R10ET の既存監査で検証済みの実装範囲について終了と判定する。** 記録更新は証明探索の新機能・命題登録・既存 API 変更を伴わない。対象外 Goal の partial を complete と扱わず、19件の監査から任意の stem の数学的証明完成を主張しない。

次 Phase では、未完成の数学的対象と群構造・関係式・生成元 DB の登録状況を現行コードから監査し、必要最小限の変更だけを新たな Phase の責務として定める。旧方式の無条件再導入・文献命題の真偽の自動認証・未検証の一般化は実施しない。
"""
PROOF_CLOSE = r"""
<!-- PHASE169_FINAL_CLOSEOUT_20261028 -->

## 2026-10-28 — Phase 169 終了時の証明・引用整合性記録

Phase 169 の終了は、既存の文献根拠に基づく型付き Proof Tree、共通 Definition による生成元像の推論、安定輸送・直和群・複合生成元の表示、および Reference が実際に使用した祖先に限られることの検証結果である。新しい数学的定理の証明を追加した記録ではない。

R10ET R6D の必須16群と追加3群は **19/19 PASS**、Trust PASS、共通 Definition の適用可能範囲で旧個別 Definition への残存引用依存0件だった。$\\pi_{10}^{8}$ は検索済み9 ProofStep を保持し、結論から到達可能な8ステップを完成証明に表示した。使用 Reference は `sphere.csv (n=4,k=2)` と Toda `(4.5)` であり、未使用の `sphere.csv (n=7,k=2)` を引用しない。部分証明表示は変更していない。

Phase 終了時の関連回帰 **67 PASS**、アクティブな `tests/` **3546 PASS**（いずれも終了コード0、FAIL 0、ERROR 0）、Git index 保全 PASS を記録した。既存の Phase 168 固定基準（$\\pi_3^2$、$\\pi_4^3$、$\\pi_5^4$）と Trust Boundary を維持するテストを含む。ただし現行の全テストの成功が、登録されていない命題や未検証の全ホモトピー群の完成証明を意味するものではない。

**未認定領域：** 任意の $(n,k)$、すべての Toda 記述の数学的真理、任意の利用者定義推論、すべての DB 生成元関係。これらは必要な出典と型付き導出を次 Phase の監査で特定する。
"""


def git(root: Path, *args: str) -> str:
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    cp = subprocess.run(["git", "-c", "core.longpaths=true", "-C", str(root), *args],
                        capture_output=True, check=False, timeout=60, env=env)
    if cp.returncode:
        raise RuntimeError(f"git {args!r}: " + cp.stderr.decode("utf-8", "replace"))
    return cp.stdout.decode("utf-8", "replace").strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def inspect_report(recovery: Path, root: Path) -> tuple[Path, dict]:
    """Accept a successful R1 Gate from any reviewed ancestor commit.

    R1 may have run before audit-only packages were committed. Its HEAD must be
    between BASELINE_HEAD and REVIEWED_REMOTE_HEAD on the same ancestry path.
    All previous success, scope, command and log-presence checks remain in force.
    """
    paths = sorted(recovery.glob(REPORT_DIR_PREFIX + "*/report.json"), reverse=True)
    if not paths:
        raise RuntimeError(
            "No R1 Gate report.json found under "
            + str(recovery / (REPORT_DIR_PREFIX + "*"))
            + "; do not rerun full pytest just to create a report"
        )
    rejected: list[str] = []
    for path in paths:
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            rejected.append(path.name + ": invalid or unreadable JSON: " + str(exc))
            continue
        if not isinstance(report, dict):
            rejected.append(str(path) + ": JSON root is not an object")
            continue
        focused, active = report.get("focused"), report.get("active_full")
        if not isinstance(focused, dict) or not isinstance(active, dict):
            rejected.append(str(path) + ": missing focused / active_full results")
            continue
        valid = (
            report.get("mode") == "PHASE169_END_OF_PHASE_TEST"
            and report.get("phase169_test_gate_pass") is True
            and report.get("git_index_preserved") is True
            and report.get("phase169_certified") is False
            and report.get("decision") == "TEST_GATE_PASS_PENDING_PHASE169_CLOSEOUT_DOCUMENTATION"
            and report.get("reviewed_files") == 13
            and report.get("r6_cases") == 19
            and focused.get("passed_count") == 67 and focused.get("exit_code") == 0
            and active.get("passed_count") == 3546 and active.get("exit_code") == 0
            and isinstance(focused.get("command"), list)
            and len(focused["command"]) >= 10
            and isinstance(active.get("command"), list)
            and active["command"][-1:] == ["tests"]
            and active["command"][1:8] == [
                "-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings", "-p"
            ]
            and "no:cacheprovider" in active["command"]
        )
        if not valid:
            rejected.append(str(path) + ": R1 Gate results or command differ from reviewed contract")
            continue
        if not all(isinstance(x.get("log"), str) and Path(x["log"]).is_file()
                   for x in (focused, active)):
            rejected.append(str(path) + ": focused or active pytest log missing")
            continue
        head = report.get("head")
        if not (isinstance(head, str) and len(head) == 40
                and all(character in "0123456789abcdef" for character in head)):
            rejected.append(str(path) + ": malformed Gate Git HEAD")
            continue
        try:
            in_reviewed_history = (
                git(root, "merge-base", BASELINE_HEAD, head) == BASELINE_HEAD
                and git(root, "merge-base", head, REVIEWED_REMOTE_HEAD) == head
            )
        except RuntimeError:
            in_reviewed_history = False
        if not in_reviewed_history:
            rejected.append(str(path) + ": Gate HEAD is outside reviewed commit ancestry: " + head)
            continue
        print("PHASE169_CLOSEOUT_R3B_R1_REPORT_HEAD=" + head, flush=True)
        print("PHASE169_CLOSEOUT_R3B_R1_REPORT_PATH=" + str(path), flush=True)
        return path, report
    details = "\n".join(rejected[:10])
    raise RuntimeError(
        "No verified successful Phase 169 R1 Gate report found among "
        + str(len(paths)) + " candidate(s). Rejections:\n" + details
    )


def edit_documents(docs: dict[str, str]) -> dict[str, str]:
    for path, content in docs.items():
        if DOC_MARKER in content:
            raise RuntimeError("Closeout marker already exists; refuse double application: " + path)
    readme = docs["README.md"]
    first = "## Current status — Phase 169 R10ET complete; Phase 169 remains open (2026-10-28)"
    next_section = "## Current status — Phase 168 closed (2026-10-25)"
    if readme.count(first) != 1 or readme.count(next_section) != 1:
        raise RuntimeError("README phase boundary changed")
    a, b = readme.index(first), readme.index(next_section)
    if b <= a:
        raise RuntimeError("Unexpected README section order")
    readme = readme[:a] + README_CLOSE.replace("$\\\\", "$\\") + readme[b:]
    readme = readme.replace("## Current status — Phase 169 closed", DOC_MARKER + "\n\n## Current status — Phase 169 closed", 1)
    old_command = "python -m pytest tests -q --tb=short"
    new_command = "python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests"
    if readme.count(old_command) != 1:
        raise RuntimeError("README test example changed")
    readme = readme.replace(old_command, new_command, 1)

    roadmap = docs["docs/roadmap.md"]
    old_status = "**現状：Phase 169 進行中。**"
    if roadmap.count(old_status) != 1:
        raise RuntimeError("Roadmap Phase169 status changed")
    roadmap = roadmap.replace(old_status, "**R10ET 時点の状況：Phase 169 進行中（終了前の履歴）。**", 1)
    old_next = "### 次の実施順序"
    if roadmap.count(old_next) < 1:
        raise RuntimeError("Roadmap R10ET plan heading missing")
    pos = roadmap.rfind(old_next)
    roadmap = roadmap[:pos] + roadmap[pos:].replace(old_next, "### R10ET 時点の次工程（終了時に実施済み）", 1)

    output = {
        "README.md": readme,
        "docs/design.md": docs["docs/design.md"].rstrip("\n") + "\n" + DESIGN_CLOSE.replace("$\\\\", "$\\"),
        "docs/development_log.md": docs["docs/development_log.md"].rstrip("\n") + "\n" + LOG_CLOSE.replace("$\\\\", "$\\"),
        "docs/roadmap.md": roadmap.rstrip("\n") + "\n" + ROADMAP_CLOSE.replace("$\\\\", "$\\"),
        "docs/proof_records.md": docs["docs/proof_records.md"].rstrip("\n") + "\n" + PROOF_CLOSE.replace("$\\\\", "$\\"),
    }
    assert set(output) == set(docs)
    for path, content in output.items():
        if content.count(DOC_MARKER) != 1:
            raise RuntimeError("Closeout marker must occur once: " + path)
        if content == docs[path]:
            raise RuntimeError("Document was not updated: " + path)
    return output


def inspect_environment(root: Path) -> tuple[str, str]:
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Not on develop")
    if git(root, "diff", "--name-only") or git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Tracked edits exist; refuse to overwrite")
    head = git(root, "rev-parse", "HEAD")
    if head not in (BASELINE_HEAD, REVIEWED_REMOTE_HEAD):
        raise RuntimeError("Unknown local HEAD; re-audit new commits before applying documentation: " + head)
    remote_line = git(root, "ls-remote", "origin", "refs/heads/develop")
    remote_head = remote_line.split("\t")[0]
    if remote_head != REVIEWED_REMOTE_HEAD:
        raise RuntimeError("Remote develop changed since review: " + remote_head)
    origin_tracking = git(root, "rev-parse", "refs/remotes/origin/develop")
    if origin_tracking not in (BASELINE_HEAD, REVIEWED_REMOTE_HEAD):
        raise RuntimeError("Unexpected origin/develop ref: " + origin_tracking)
    for path, expected in {**DOC_BLOBS, **SOURCE_BLOBS, R6_EVIDENCE: R6_BLOB}.items():
        full = root / path
        if not full.is_file() or git(root, "hash-object", "--path=" + path, path) != expected:
            raise RuntimeError("Reviewed local file differs: " + path)
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("Reviewed committed file differs: " + path)
    return head, origin_tracking


def apply_documentation(root: Path, do_apply: bool) -> int:
    recovery_env = os.environ.get("LOCALAPPDATA")
    if not recovery_env:
        raise RuntimeError("LOCALAPPDATA is required")
    recovery = Path(recovery_env) / "EHPProofTracerRecovery"
    if root == recovery or root in recovery.parents or recovery in root.parents:
        raise RuntimeError("External recovery must be outside checkout")
    head, origin_tracking = inspect_environment(root)
    report_path, report = inspect_report(recovery, root)
    original_bytes = {p: (root / p).read_bytes() for p in DOC_BLOBS}
    original_texts = {p: b.decode("utf-8") for p, b in original_bytes.items()}
    revised = edit_documents(original_texts)
    work = recovery / ("phase169_closeout_r3_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    before_dir, full_dir = work / "before_full", work / "after_full"
    before_dir.mkdir(parents=True, exist_ok=False)
    full_dir.mkdir(parents=True, exist_ok=False)
    for path, raw in original_bytes.items():
        before, after = before_dir / path, full_dir / path
        before.parent.mkdir(parents=True, exist_ok=True)
        after.parent.mkdir(parents=True, exist_ok=True)
        before.write_bytes(raw)
        after.write_bytes(revised[path].encode("utf-8"))
    metadata = {
        "mode": "PHASE169_FINAL_DOCUMENTATION", "repository": REPO_NAME,
        "local_head_before": head, "origin_develop_before": origin_tracking,
        "reviewed_remote_head": REVIEWED_REMOTE_HEAD, "test_report": str(report_path),
        "test_report_head": report["head"], "focused_pass": 67, "active_full_pass": 3546,
        "files": {p: {"old_blob": DOC_BLOBS[p], "new_sha256": hashlib.sha256(revised[p].encode("utf-8")).hexdigest()} for p in DOC_BLOBS},
        "applied": False, "index_preserved": None,
        "remote_ahead_of_local": head != REVIEWED_REMOTE_HEAD,
    }
    manifest = work / "manifest.json"
    manifest.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE169_CLOSEOUT_R3_FULL_DOCUMENTS=" + str(full_dir), flush=True)
    print("PHASE169_CLOSEOUT_R3_BACKUP_DOCUMENTS=" + str(before_dir), flush=True)
    print("PHASE169_CLOSEOUT_R3_R1_REPORT=" + str(report_path), flush=True)
    if not do_apply:
        print("PHASE169_CLOSEOUT_R3_DECISION=PREPARED_NOT_APPLIED", flush=True)
        print("PHASE169_CLOSEOUT_R3_MANIFEST=" + str(manifest), flush=True)
        return 0
    index_path_string = git(root, "rev-parse", "--git-path", "index")
    index_path = Path(index_path_string)
    if not index_path.is_absolute():
        index_path = root / index_path
    index_original = index_path.read_bytes()
    updated: list[str] = []
    try:
        for path, raw in original_bytes.items():
            if (root / path).read_bytes() != raw:
                raise RuntimeError("Source changed during update: " + path)
        for path in DOC_BLOBS:
            target = root / path
            fd, temp_path = tempfile.mkstemp(prefix=".phase169_r3_", dir=target.parent)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(revised[path].encode("utf-8"))
                    stream.flush()
                    os.fsync(stream.fileno())
                shutil.copymode(target, temp_path)
                os.replace(temp_path, target)
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            updated.append(path)
        if index_path.read_bytes() != index_original:
            raise RuntimeError("Git index changed")
        changed = set(git(root, "diff", "--name-only").splitlines())
        if changed != set(DOC_BLOBS) or git(root, "diff", "--cached", "--name-only"):
            raise RuntimeError("Unexpected tracked diff after update: " + str(changed))
        metadata["applied"] = True
        metadata["index_preserved"] = True
        manifest.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE169_CLOSEOUT_R3_DOCUMENTS=5/5_WRITTEN", flush=True)
        print("PHASE169_CLOSEOUT_R3_GIT_INDEX_PRESERVED=True", flush=True)
        print("PHASE169_CLOSEOUT_R3_REMOTE_AHEAD_OF_LOCAL=" + str(head != REVIEWED_REMOTE_HEAD), flush=True)
        print("PHASE169_CLOSEOUT_R3_DECISION=PHASE169_CLOSED_LOCAL_DOCS_PENDING_GIT_COMMIT", flush=True)
        print("PHASE169_CLOSEOUT_R3_MANIFEST=" + str(manifest), flush=True)
        return 0
    except BaseException:
        for path in reversed(updated):
            (root / path).write_bytes(original_bytes[path])
        metadata["rolled_back"] = True
        manifest.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    try:
        return apply_documentation(args.repo.resolve(), not args.prepare_only)
    except BaseException:
        print("PHASE169_CLOSEOUT_R3_ERROR=" + traceback.format_exc(), flush=True)
        print("PHASE169_CLOSEOUT_R3_EXIT=1", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
