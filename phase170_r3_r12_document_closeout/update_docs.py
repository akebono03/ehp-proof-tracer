"""Phase 170 R3-R12: preserve and emit five complete current documents.

Read reviewed worktree files after checking HEAD/blobs and Phase 170 evidence.
Write complete updated files to output/, then optionally apply atomically.
Never synthesize or replace historical text and never run repository-wide pytest.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess

# The successful Phase 170 pytest gate ran at this commit.
# A later commit may only ADD files in the three reviewed audit packages.
GATE_HEAD = "84db682e179203dcbddc1c2c88bc3ccbb31a830f"
EXPECTED_HEAD = GATE_HEAD  # Stable provenance expected in the saved closeout evidence.
ALLOWED_NEW_AUDIT_PREFIXES = (
    "phase170_r3_r11_active_suite_closeout/",
    "phase170_r3_r11r1_committed_audit_head/",
    "phase170_r3_r11r2_unicode_git_path_fix/",
)
AUDITED_HEAD = "08382968b5359d6c956b48acec333f127014d4c8"
BRANCH = "develop"
DOC_BLOBS = {
    "README.md": "89b637a35134583fa58132d6ffc31519bee5bfff",
    "docs/design.md": "fb729605aa7ea67ef3586524af3f964965139ba8",
    "docs/development_log.md": "8dfbedc8d64b342833f390810399a3ebf988c554",
    "docs/roadmap.md": "ae9cbe4feb34c013312fe311fbcaf0ddf2534b81",
    "docs/proof_records.md": "74daf33c383c57f1727a171b83ae51ca92528cb0",
}
MARKER = "<!-- PHASE170_FINAL_DOCUMENT_CLOSEOUT_20261029 -->"
README_INSERT_BEFORE = "<!-- PHASE169_FINAL_CLOSEOUT_20261028 -->"

README_SECTION = r"""<!-- PHASE170_FINAL_DOCUMENT_CLOSEOUT_20261029 -->

## Current status — Phase 170 closed (2026-10-29)

Phase 170 completed its reviewed **explicit $n=2$ database domain**, covering all 33 stems $1\le k\le 33$ (groups $\pi_{k+2}^{2}$). A fresh, independent R3-R10R1 audit ran ordinary typed proof search and the public, trust-gated narrative Web route for each stem. The results were **33/33 `COMPLETE_AND_WEB_VERIFIED`**, with no unresolved goals in the audited outcomes and no domain gaps. The audit left tracked files unchanged.

The proof search uses the separately screened earlier group structure for $\pi_{k+2}^{3}$ and the typed Toda (5.2) composition isomorphism $\eta_2\circ -:\pi_m^3\cong\pi_m^2$ in its applicable domain. For $\pi_{14}^{2}$, the previously unfinished generator correspondence additionally uses the cited equation $\varepsilon_3\circ\nu_{11}=\nu'\circ\bar\nu_6$ from the checked adopted Chapter VII transcription of Toda (7.12). It is a separate, replayable proof premise, not an equality inferred from generator names or database display text. Its source position is defined relative to the adopted transcription, **not independently certified against the original printed edition**.

Phase-end verification on Windows on 2026-10-29 reported **3,546 passed in 34.94s**, exit code 0, for `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests`. The Phase 170 R3-R11 final report was `FULL_SUITE_PASS`, with the previously verified 33/33 domain report accepted and `tracked_unchanged=True`. The active `tests/` suite is not the full collection of archived or retired historical tests.

These results do **not** certify every homotopy group, every $n\ge3$ target, every original Toda statement, or arbitrary user-defined inference rules. The existing Proof Tree, citation-screening, Narrative Model, and Web trust boundaries remain in effect. Further work should select remaining registered goals based on actual incomplete searches and independently checkable sources.

"""

DESIGN_SECTION = r"""<!-- PHASE170_FINAL_DOCUMENT_CLOSEOUT_20261029 -->

## Phase 170 — $n=2$ の登録済み33件に対する型付き輸送と証明検証（2026-10-29）

### 本番探索の数学的根拠と責務

Phase 170 は、登録済み DB の $n=2$、$1\le k\le33$ を対象とし、$m=k+2$ で先行する $\pi_m^3$ の型付き群構造と Toda (5.2) の $\eta_2\circ-:\pi_m^3\xrightarrow{\cong}\pi_m^2$ を組み合わせる Backward Search（逆向き証明探索）経路を拡張した。巡回群および直和群の構造と生成元の対応は型付き演算により検査し、DB の表示文字列や生成元名の一致のみでは推論を採用しない。DB の群構造が Goal（証明目標）として与えられたことを、その Goal の証明済み GIVEN（既知の前提）とみなさない。

特に $\pi_{14}^{2}$ では先行する $\pi_{14}^{3}$ の直和分解に現れる $\varepsilon_3\circ\nu_{11}$ と目標の $\nu'\circ\bar\nu_6$ が文字列として異なる。Toda (7.12) の型付き等式 $\varepsilon_3\circ\nu_{11}=\nu'\circ\bar\nu_6$ を出典付きの**独立した第3前提**として Proof Tree に加え、同じ生成元であるとの無根拠な仮定を拒否する。Toda (5.2)、先行群構造、Toda (7.12) の各根拠は既存の探索・引用採用・検証境界を通る。

Toda (7.12) の引用は `sources/toda/Toda_07_2.tex` の採用済み TeX 転写を厳密に照合し、`HyoujiGen.csv` の生成元 ID から型付き等式を構築する。文献の掲載位置はこの転写データ内の順序であり、Toda 原著の刊行版の位置や記述が独立に校訂・認証されたことは意味しない。転写が一致しない場合は fail-closed（安全側で拒否）とする。

### 標準 Web 経路と監査範囲

公開経路は従来どおり、登録された型付き Goal → Backward Search → 検証済み Proof Tree → Proof Narrative Model → 共通 Renderer → Web とする。`phase170_r3_r8_n2_exhaustive_audit/audit.py` の独立 Worker によって各 $k=1,\ldots,33$ を再探索し、`generic-complete-proof`、`partial_result=False`、`open_goals=0`、検証済みステップと描画行の存在を確認した。R3-R10R1 の全33件で `COMPLETE_AND_WEB_VERIFIED`、未完了0件、既存追跡ファイルの変更なしだった。

Phase 170 の終了 Gate では、同じ33件の監査レポートを個々の Worker 行まで検査したうえで、現行アクティブ `tests/` の pytest **3,546 PASS**（2026-10-29、34.94秒、終了コード0）、`FULL_SUITE_PASS`、`tracked_unchanged=True` を確認した。監査パッケージの追加による Git HEAD の変更は、数学的な本体ファイルの変更と区別して検証した。ここで「全体テスト」と呼ぶのは現行 `tests/` であり、退避された歴史的テストを含む無制限の全ファイル収集ではない。

### 認定しない範囲

登録済み $n=2$ の33件以外の Goal、全ての $n\ge3$、すべての stem、Toda 原著の全命題の数学的真理、任意の外部 `InferenceRule` は認定対象外である。旧 Renderer や個別生成元名に依存した例外的な証明を復活させず、既存 API と Trust Boundary を維持する。
"""

DEV_SECTION = r"""<!-- PHASE170_FINAL_DOCUMENT_CLOSEOUT_20261029 -->

## 2026-10-29 — Phase 170 終了（登録済み $n=2$ 群の証明完成・全体テスト）

### 実装と失敗原因の監査履歴

R3-R7 では Toda (5.2) の $\eta_2\circ -$ による $\pi_m^3$ から $\pi_m^2$ への型付き輸送を実装し、巡回群と直和群の構造を先行する出典・DB Goal と区別した。R3-R8 の初期全件監査で $n=2$、$k=1,\ldots,33$ の32件が完成したが、$k=12$ は当初 Worker の Windows `cp932` 出力エラーによって失敗と記録された。R3-R8R2 で UTF-8 を固定して再評価した結果、$\pi_{14}^{2}$ の数学的 Goal が未完成であることが明らかになった。

R3-R9 は Toda (7.12) にある $\varepsilon_3\circ\nu_{11}=\nu'\circ\bar\nu_6$ を、型付きで引用された独立した等式前提として導入した。初回の照合は TeX 転写の空白・`\ov{\nu}` 表記に一致せず失敗したため、R3-R9R2 で採用済み `sources/toda/Toda_07_2.tex` の実際の式と一致させた。限定 pytest **46 PASS**、追加テスト **12 PASS**、$\pi_{14}^{2}$ は `complete`、`open_goals=0`、`proven_steps=4`、Web `generic-complete-proof` を確認した。転写の出典資格と、原著刊行版における独立校訂は区別する。

R3-R10R1 の fresh audit（過去の32件を流用しない全件再探索）では、$k=1$ から33まで **33/33 `COMPLETE_AND_WEB_VERIFIED`**、`DOMAIN_GAPS=0`、追跡済み変更なし。限定契約テストは **19 PASS**。監査時 Git HEAD は `08382968b5359d6c956b48acec333f127014d4c8`、その後の HEAD `84db682e179203dcbddc1c2c88bc3ccbb31a830f` までの差分は監査パッケージの追加だけだった。日本語ファイル名が `core.quotePath` により八進数表示された問題は、監査用 Git コマンドの UTF-8 パス取得に限定して修正した。

### 終了 Gate と証拠

R3-R11R2 の終了実行では、33件すべてを含む監査レポートを再照合した後、`python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests` を**Phase 170 の終了時に1回**実行した。結果は **3546 passed in 34.94s**、終了コード0、`PHASE170_R3R11_RESULT=FULL_SUITE_PASS`、`PHASE170_R3R11_TRACKED_UNCHANGED=True`。DryRun も PASS。報告ファイルは Windows の `%LOCALAPPDATA%/EHPProofTracerRecovery/phase170_r3_r11_active_closeout_20261029_051330_057437/closeout.json`、全33件のレポートは同 `phase170_r3_r10_n2_33_20261029_045006_272086/audit.json`。詳細は元の JSON と Worker ログを参照し、文書更新で元の証拠を改変しない。

### Phase 境界

完成認定は登録済み $n=2,1\le k\le33$ の探索と Web 公開経路の監査結果に限る。すべてのホモトピー群、未登録の高次群、すべての Toda 原典の正しさを証明したものではない。Phase 171 以降は未完成の実在する Goal と、型付き命題・出典・生成元情報の不足を個別に調査してから最小限の変更を選ぶ。
"""

ROADMAP_SECTION = r"""<!-- PHASE170_FINAL_DOCUMENT_CLOSEOUT_20261029 -->

## Phase 170 — 正式終了（2026-10-29）

Phase 170 は、Phase 169 の次工程として、登録 DB に明示された $n=2$、$1\le k\le33$ の33群における Backward Search（逆向き証明探索）と Web Trust Boundary（信頼境界）を全件監査した。Toda (5.2) に基づく型付き $\eta_2\circ-$ 輸送を利用し、唯一残った $\pi_{14}^{2}$ の生成元表示差異を Toda (7.12) の出典付き等式で解消した。

**最終結果：** R3-R10R1 の fresh audit **33/33 `COMPLETE_AND_WEB_VERIFIED`**、未完成0件。R3-R11R2 の Phase 末尾の現行アクティブ `tests/` 全体 pytest **3,546 PASS**（34.94秒、終了コード0）、Git 追跡済みファイル不変。これは登録済み $n=2$ の有限範囲だけの認定であり、任意の $(n,k)$ の証明完成とは異なる。

### Phase 171 以降 — 現時点の調査方針（未実装）

1. $n\ge3$ や現在の監査範囲外で、DB に明示された Goal を実際に探索し、未完成の Proof Tree・open goals・出典資格を先に確定する。
2. `HyoujiGen.csv`、`sphere.csv`、Toda の採用済み転写の関係を、表示文字列ではなく型付き関係と引用可能な命題によって検証する。
3. 必要な数学的根拠の不足が確認された対象に限り、既存の共通 Backward Search と Trust Boundary を再利用した最小限の修正を計画する。
4. 全登録群の完成・原著全命題の数学的認証・旧 Definition の一括削除・生成元 family 別の個別実装を先取りしない。全体 pytest は次 Phase の末尾だけに実施する。

以前の節にある「Phase 170 の範囲は未確定」は Phase 169 終了時の計画記録であり、本節を Phase 170 の確定済み結果として参照する。
"""

PROOF_SECTION = r"""<!-- PHASE170_FINAL_DOCUMENT_CLOSEOUT_20261029 -->

## 2026-10-29 — Phase 170：$n=2$ 登録済み33群の完成証明・出典記録

### 対象と検証方式

`data/sphere.csv` に登録された $n=2$、$1\le k\le33$ の33件（$\pi_{k+2}^{2}$）について、R3-R10R1 の独立 Worker を使い、型付き Backward Search と公開 Web の検証済み Narrative を毎件再生成した。**33/33 `COMPLETE_AND_WEB_VERIFIED`、`open_goals=0`、Web `generic-complete-proof`、`partial_result=False`、未完成0件**。過去の32件の監査結果を結合して得た数ではない。

### 代表的な新規完成対象：$\pi_{14}^{2}$

先行する登録済み群構造は次のとおり。

$$
\pi_{14}^{3}\cong
\mathbb Z/4\{\mu'\}
\oplus\mathbb Z/2\{\varepsilon_3\circ\nu_{11}\}
\oplus\mathbb Z/2\{\nu'\circ\varepsilon_6\}.
$$

目標の DB 表示は次のとおり。

$$
\pi_{14}^{2}\cong
\mathbb Z/4\{\eta_2\circ\mu'\}
\oplus\mathbb Z/2\{\eta_2\circ\nu'\circ\bar\nu_6\}
\oplus\mathbb Z/2\{\eta_2\circ\nu'\circ\varepsilon_6\}.
$$

Toda (5.2) の $\eta_2\circ-:\pi_{14}^{3}\xrightarrow{\cong}\pi_{14}^{2}$ は群の輸送を与えるが、それだけでは $\varepsilon_3\circ\nu_{11}$ と $\nu'\circ\bar\nu_6$ の表示の差を正当化できない。Toda (7.12) に記された

$$
\varepsilon_3\circ\nu_{11}=\nu'\circ\bar\nu_6
$$

を引用付きの型付き等式前提として別に採用し、先行群構造・Toda (5.2)・Toda (7.12) を用いる Proof Tree を完成した。R3-R9R2 では探索 `complete`、`open_goals=0`、`proven_steps=4`、Web 完成表示を確認し、元の限定テスト46件・追加12件が PASS した。

Toda (7.12) の根拠は `sources/toda/Toda_07_2.tex` の**採用済み転写**と `data/HyoujiGen.csv` の型付き生成元 ID との照合である。TeX 上の表記 `\ov{\nu}_6`、式番号の周辺構文、改行を一致させており、元の刊行版を独立に照合したとの主張はしない。与えられた命題の採録と、その命題から結論への型付き推論を区別する。

### 終了監査記録と認定範囲

33件 fresh audit：`%LOCALAPPDATA%/EHPProofTracerRecovery/phase170_r3_r10_n2_33_20261029_045006_272086/audit.json`。Phase 終了テスト：`%LOCALAPPDATA%/EHPProofTracerRecovery/phase170_r3_r11_active_closeout_20261029_051330_057437/closeout.json`。終了時の現行 `tests/` は **3546 PASS、0 FAIL、0 ERROR、34.94秒、終了コード0**、追跡済みファイル不変。退避済みの歴史的テストは含まない。

**検証境界：** 全33件の search/Web 完成表示とその根拠を確認した記録であり、任意のホモトピー群・全ての書誌原典・生成元名の暗黙の等式・任意の外部推論規則の正しさを包括的に認証するものではない。
"""

SECTIONS = {
    "README.md": README_SECTION,
    "docs/design.md": DESIGN_SECTION,
    "docs/development_log.md": DEV_SECTION,
    "docs/roadmap.md": ROADMAP_SECTION,
    "docs/proof_records.md": PROOF_SECTION,
}


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(
            "git " + " ".join(args) + " failed: "
            + proc.stderr.decode("utf-8", errors="replace").strip()
        )
    return proc.stdout.decode("utf-8", errors="replace").strip()


def preflight(root: Path, *, check_remote: bool = True) -> dict:
    """Require the reviewed Gate HEAD or an audit-only descendant thereof."""
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != BRANCH:
        raise RuntimeError(f"unreviewed branch: {branch}")
    # Fail closed on divergent history, but accept the same successful Gate
    # with later audit-package additions. Never accept math/data/test edits.
    git(root, "merge-base", "--is-ancestor", GATE_HEAD, "HEAD")
    delta = git(root, "-c", "core.quotePath=false", "diff", "--name-status", GATE_HEAD, "HEAD", "--")
    for entry in delta.splitlines():
        status, delimiter, path = entry.partition("\t")
        if (delimiter != "\t" or status != "A"
                or not path.startswith(ALLOWED_NEW_AUDIT_PREFIXES)):
            raise RuntimeError(f"non-audit change after Phase 170 pytest Gate: {entry}")
    if check_remote:
        remote = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not remote or remote.split()[0] != head:
            raise RuntimeError("origin/develop differs from local reviewed commit")
    if git(root, "diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes present; refusing document update")
    if git(root, "diff", "--name-only", "HEAD", "--"):
        raise RuntimeError("pre-existing tracked changes; refusing document update")
    for relative, blob in DOC_BLOBS.items():
        if git(root, "rev-parse", f"HEAD:{relative}") != blob:
            raise RuntimeError(f"unreviewed documentation blob: {relative}")
        if not (root / relative).is_file():
            raise RuntimeError(f"missing document: {relative}")
    return {"head": head, "branch": branch, "gate_head": GATE_HEAD,
            "reviewed_audit_additions": delta.splitlines(), "blobs": dict(DOC_BLOBS)}


def validate_evidence(domain: dict, closeout: dict, domain_path: Path) -> None:
    if (domain.get("phase") != "170 R3-R10"
            or domain.get("mode") != "AUDIT_ONLY_FRESH_33"
            or domain.get("dry_run") is not False
            or domain.get("result") != "DOMAIN_ALL_VERIFIED"
            or domain.get("domain") != list(range(1, 34))
            or domain.get("domain_checked") != 33
            or domain.get("domain_complete") != 33
            or domain.get("domain_gaps") != 0
            or domain.get("tracked_unchanged") is not True):
        raise RuntimeError("unverified Phase 170 fresh-domain report")
    old_pre = domain.get("preflight")
    if not isinstance(old_pre, dict) or old_pre.get("head") != AUDITED_HEAD:
        raise RuntimeError("domain report not from the reviewed audited HEAD")
    rows = domain.get("rows")
    if not isinstance(rows, list) or len(rows) != 33:
        raise RuntimeError("domain report is missing worker rows")
    for k, row in enumerate(rows, 1):
        if not isinstance(row, dict) or not (
            row.get("k") == k and row.get("n") == 2
            and row.get("group_dimension") == k + 2
            and row.get("target_typed") is True
            and row.get("source_precedes") is True
            and row.get("search_status") == "complete"
            and row.get("search_complete") is True
            and type(row.get("open_goals")) is int and row["open_goals"] == 0
            and type(row.get("proven_steps")) is int and row["proven_steps"] > 0
            and row.get("result") == "COMPLETE_AND_WEB_VERIFIED"
            and row.get("audit_result") == "COMPLETE_AND_WEB_VERIFIED"
            and row.get("web_key") == "generic-complete-proof"
            and row.get("web_partial") is False
            and type(row.get("web_steps")) is int and row["web_steps"] > 0
            and type(row.get("web_lines")) is int and row["web_lines"] > 0
            and row.get("web_error") is None
        ):
            raise RuntimeError(f"worker evidence incomplete: k={k}")
    if (closeout.get("phase") != "170 R3-R11"
            or closeout.get("mode") != "PHASE_END_ACTIVE_SUITE"
            or closeout.get("dry_run") is not False
            or closeout.get("full_pytest") is not True
            or closeout.get("pytest_exit") != 0
            or closeout.get("result") != "FULL_SUITE_PASS"
            or closeout.get("tracked_unchanged") is not True
            or closeout.get("domain_checked") != 33
            or closeout.get("domain_complete") != 33
            or closeout.get("domain_gaps") != 0
            or closeout.get("domain_report_sha256") != sha256(domain_path.read_bytes()).hexdigest()
            or closeout.get("preflight", {}).get("head") != EXPECTED_HEAD):
        raise RuntimeError("unverified Phase 170 final active-suite report")
    if not re.fullmatch(r"3546 passed in 34\.94s", closeout.get("pytest_summary", "")):
        raise RuntimeError("unexpected final pytest summary")
    active_command = closeout.get("active_command", [])
    expected_command = ["python", "-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings", "-p", "no:cacheprovider", "tests"]
    if active_command != expected_command:
        raise RuntimeError("active test selection is not the reviewed tests/ command")


def load_evidence(recovery: Path) -> tuple[Path, Path, dict, dict]:
    domain_path = (recovery / "phase170_r3_r10_n2_33_20261029_045006_272086" / "audit.json")
    closeout_path = (recovery / "phase170_r3_r11_active_closeout_20261029_051330_057437" / "closeout.json")
    domain = json.loads(domain_path.read_text(encoding="utf-8-sig"))
    closeout = json.loads(closeout_path.read_text(encoding="utf-8-sig"))
    validate_evidence(domain, closeout, domain_path)
    return domain_path, closeout_path, domain, closeout


def append_section(original: bytes, relative: str) -> bytes:
    if relative not in SECTIONS:
        raise KeyError(relative)
    if original.startswith(b"\xef\xbb\xbf"):
        prefix, body = b"\xef\xbb\xbf", original[3:]
    else:
        prefix, body = b"", original
    contents = body.decode("utf-8")
    if MARKER in contents:
        raise RuntimeError(f"Phase 170 marker already exists in {relative}; refusing duplicate update")
    newline = "\r\n" if contents.count("\r\n") > contents.count("\n") - contents.count("\r\n") else "\n"
    added = SECTIONS[relative].strip("\n").replace("\n", newline)
    if relative == "README.md":
        if contents.count(README_INSERT_BEFORE) != 1:
            raise RuntimeError("README Phase 169 insertion point missing or ambiguous")
        contents = contents.replace(README_INSERT_BEFORE, added + newline + newline + README_INSERT_BEFORE, 1)
    else:
        contents = contents + ("" if contents.endswith(("\n", "\r")) else newline) + newline + added + newline
    changed = prefix + contents.encode("utf-8")
    if not changed.startswith(original) and relative != "README.md":
        raise AssertionError("historical document prefix must be preserved byte-for-byte")
    if relative == "README.md":
        old_rest = original[len(prefix):].decode("utf-8")
        new_rest = changed[len(prefix):].decode("utf-8")
        if new_rest.replace(added + newline + newline, "", 1) != old_rest:
            raise AssertionError("README historical text unexpectedly modified")
    return changed


def atomically_write(path: Path, contents: bytes) -> None:
    temporary = path.with_name(path.name + ".phase170.tmp")
    try:
        temporary.write_bytes(contents)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def build_docs(root: Path, output_root: Path, recovery: Path, *, apply: bool) -> dict:
    before = preflight(root)
    domain_path, closeout_path, _, _ = load_evidence(recovery)
    output_root.mkdir(parents=True, exist_ok=True)
    originals: dict[str, bytes] = {}
    new_files: dict[str, bytes] = {}
    for relative in DOC_BLOBS:
        original = (root / relative).read_bytes()
        new = append_section(original, relative)
        if new == original or MARKER.encode("ascii") not in new:
            raise RuntimeError(f"document did not change correctly: {relative}")
        originals[relative] = original
        new_files[relative] = new
    for relative, data in new_files.items():
        dest = output_root / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        atomically_write(dest, data)
    report = {
        "phase": "170 R3-R12", "apply": apply, "head": before["head"],
        "domain_report": str(domain_path), "domain_report_sha256": sha256(domain_path.read_bytes()).hexdigest(),
        "closeout_report": str(closeout_path), "closeout_report_sha256": sha256(closeout_path.read_bytes()).hexdigest(),
        "documents": {key: {"before_bytes": len(originals[key]), "after_bytes": len(new_files[key]),
                            "sha256": sha256(new_files[key]).hexdigest()}
                      for key in DOC_BLOBS},
        "full_pytest_rerun": False,
    }
    if apply:
        backup_root = recovery / ("phase170_r3_r12_docs_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        backup_root.mkdir(parents=True, exist_ok=False)
        for relative, original in originals.items():
            backup = backup_root / "before" / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            atomically_write(backup, original)
        applied: list[str] = []
        try:
            for relative, data in new_files.items():
                atomically_write(root / relative, data)
                applied.append(relative)
            staged = git(root, "diff", "--cached", "--name-only", "--")
            changed = set(git(root, "diff", "--name-only", "HEAD", "--").splitlines())
            if staged or changed != set(DOC_BLOBS):
                raise RuntimeError(f"unexpected post-apply git changes: {staged!r}, {changed!r}")
            for relative, data in new_files.items():
                if (root / relative).read_bytes() != data:
                    raise RuntimeError(f"document verification failed: {relative}")
            report["backup_root"] = str(backup_root)
            report["result"] = "FIVE_DOCUMENTS_APPLIED"
        except BaseException:
            for relative in applied:
                atomically_write(root / relative, originals[relative])
            raise
    else:
        if preflight(root, check_remote=False) != before:
            raise RuntimeError("dry-run altered reviewed tracked state")
        report["result"] = "FIVE_FULL_DOCUMENTS_PREPARED"
    (output_root / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    try:
        report = build_docs(args.root.resolve(), args.output.resolve(), recovery, apply=args.apply)
        for name, row in report["documents"].items():
            print(f"PHASE170_R3R12_FULL_DOCUMENT={name} BYTES={row['after_bytes']}", flush=True)
        print(f"PHASE170_R3R12_REPORT={args.output.resolve() / 'report.json'}", flush=True)
        print(f"PHASE170_R3R12_RESULT={report['result']}", flush=True)
        return 0
    except Exception as exc:
        print(f"PHASE170_R3R12_REFUSED={type(exc).__name__}: {exc}", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
