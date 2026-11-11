# Phase 174 R72 — 全文コードと新規ファイル

新規作成ファイルは `phase174_r3_r7_r72_closeout_preflight/` 以下に配置する。既存コード・既存テスト・正式主要5文書は一切書き換えない。新規クラスはなく、以下に全 import とすべての新規関数を省略なしで示す。新規関数は `audit.py` と `tests/test_audit.py` の各ファイルに記載順で追加する。対象は Phase 174 の Closeout 前監査のみであり、全体 pytest は実行しない。

## `audit.py`

```python
"""Phase 174 R72: read-only closeout preflight and partial-proof boundary audit.

R71 evidence is checked as a prior result, not presented as a fresh test run.
Two actual incomplete public searches verify that R70/R70R1 did not upgrade
named-generator proof statuses. No repo source or main document is written.
"""
from __future__ import annotations

import argparse
from hashlib import sha1
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from phase174_r3_r7_r71_common_narrative_regression.audit import (
    PINS as R71_PINS,
    REVIEWED_REMOTE_HEAD,
    source_guard as r71_source_guard,
)


PACKAGE = "phase174_r3_r7_r72_closeout_preflight"
R71_PACKAGE = "phase174_r3_r7_r71_common_narrative_regression"
R71_AUDIT_BLOB = "cdf68bc499395c115526d783ffcdb9b180c50a28"
MERGED_R71_HEAD = "b66099598177d74e979492f1d04a916e6f0821a8"
ALLOWED_LOCAL_HEADS = (REVIEWED_REMOTE_HEAD, MERGED_R71_HEAD)
EXPECTED_REFERENCES = {
    (3, 3): 8,
    (4, 3): 4,
    (4, 4): 4,
    (4, 5): 4,
    (4, 7): 4,
    (5, 3): 7,
    (6, 5): 7,
    (7, 5): 3,
}
INCOMPLETE_CASES = ((4, 8), (4, 31))
DOCUMENTS = (
    "README.md",
    "docs/design.md",
    "docs/development_log.md",
    "docs/roadmap.md",
    "docs/proof_records.md",
)


def git_blob_sha(raw: bytes) -> str:
    """Calculate a Git blob SHA-1 for exact bytes."""
    return sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()


def check_prior_package(root: Path) -> None:
    """Verify the R71 audit script matches the version that produced its evidence."""
    path = root / R71_PACKAGE / "audit.py"
    raw = path.read_bytes()
    lf = raw.replace(b"\r\n", b"\n")
    if b"\r" in lf:
        raise RuntimeError("R72_R71_MIXED_LINE_ENDINGS")
    choices = (raw, lf, lf.replace(b"\n", b"\r\n"))
    if R71_AUDIT_BLOB not in {git_blob_sha(content) for content in choices}:
        raise RuntimeError("R72_R71_AUDIT_SOURCE_CHANGED")


def git_head(root: Path, branch: str = "HEAD") -> str:
    """Read an existing Git ref; never fetch or change repository state."""
    result = subprocess.run(
        ["git", "rev-parse", "--verify", branch], cwd=root,
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("R72_GIT_REF_UNAVAILABLE: " + branch)
    return result.stdout.strip()


def tracked_changes(root: Path) -> tuple[str, ...]:
    """Require no changes in existing tracked files or the staging index."""
    observed: list[str] = []
    for argv in (("git", "diff", "--name-only"),
                 ("git", "diff", "--cached", "--name-only")):
        result = subprocess.run(
            list(argv), cwd=root, capture_output=True, text=True, check=False,
        )
        if result.returncode:
            raise RuntimeError("R72_GIT_DIFF_UNAVAILABLE")
        observed.extend(path for path in result.stdout.splitlines() if path)
    if observed:
        raise RuntimeError("R72_TRACKED_CHANGES_PRESENT: " + ", ".join(observed))
    return ()


def validate_r71_report(data: dict[str, object], head: str) -> list[dict[str, object]]:
    """Validate R71 evidence structurally; this is not independent mathematics."""
    if not isinstance(data, dict) or data.get("phase") != "174-R71":
        raise RuntimeError("R72_R71_REPORT_PHASE_MISMATCH")
    if head not in ALLOWED_LOCAL_HEADS:
        raise RuntimeError("R72_HEAD_REVIEW_REQUIRED: " + head)
    if (data.get("reviewed_remote_head") != REVIEWED_REMOTE_HEAD
            or data.get("local_head") != REVIEWED_REMOTE_HEAD):
        # The R71 evidence is historical: its genuine run occurred at
        # 01c5246a, before GitHub merged its audit-only directory.
        raise RuntimeError("R72_R71_REPORT_HEAD_MISMATCH")
    if (data.get("production_changes") != []
            or data.get("new_given") != 0
            or data.get("new_mathematical_rules") != 0
            or data.get("whole_test_suite_executed") is not False
            or data.get("full_sentence_semantics_certified") is not False):
        raise RuntimeError("R72_R71_REPORT_SCOPE_CHANGED")
    checked = data.get("source_files_checked")
    if checked != list(R71_PINS):
        raise RuntimeError("R72_R71_SOURCE_SCOPE_CHANGED")
    items = data.get("public_samples")
    if not isinstance(items, list) or len(items) != len(EXPECTED_REFERENCES):
        raise RuntimeError("R72_R71_SAMPLE_COUNT_CHANGED")
    seen: set[tuple[int, int]] = set()
    for item in items:
        if not isinstance(item, dict):
            raise RuntimeError("R72_R71_SAMPLE_NOT_OBJECT")
        n, k = item.get("n"), item.get("k")
        if type(n) is not int or type(k) is not int:
            raise RuntimeError("R72_R71_SAMPLE_BAD_DIMENSION")
        pair = (n, k)
        if pair not in EXPECTED_REFERENCES or pair in seen:
            raise RuntimeError("R72_R71_SAMPLE_UNEXPECTED_OR_DUPLICATED")
        seen.add(pair)
        if (item.get("group") != f"pi_{n+k}^{n}"
                or item.get("status") != "COMPLETE"
                or item.get("verified_root") is not True
                or type(item.get("step_count")) is not int
                or item["step_count"] < 1
                or item.get("reference_count") != EXPECTED_REFERENCES[pair]
                or not isinstance(item.get("markdown_sha256"), str)
                or re.fullmatch(r"[0-9a-f]{64}", item["markdown_sha256"]) is None):
            raise RuntimeError("R72_R71_SAMPLE_CONTRACT_CHANGED")
    if seen != set(EXPECTED_REFERENCES):
        raise RuntimeError("R72_R71_SAMPLES_MISSING")
    return items


def document_readiness(root: Path) -> list[dict[str, object]]:
    """Record five canonical documents needing a Phase 174 full-file closeout.

    This function does not write any document or rewrite historical sections.
    """
    output: list[dict[str, object]] = []
    for name in DOCUMENTS:
        path = root / name
        raw = path.read_bytes()
        content = raw.decode("utf-8-sig")
        if not content.lstrip().startswith("# EHP Proof Tracer"):
            raise RuntimeError("R72_DOCUMENT_HEADER_CHANGED: " + name)
        if "PHASE173_FINAL_CLOSEOUT_20261105" not in content:
            raise RuntimeError("R72_PHASE173_HISTORY_MISSING: " + name)
        output.append({
            "path": name,
            "git_blob_sha": git_blob_sha(raw),
            "phase173_final_record_present": True,
            "phase174_final_record_present": "PHASE174_FINAL_CLOSEOUT" in content,
            "closeout_full_file_update_required": "PHASE174_FINAL_CLOSEOUT" not in content,
        })
    return output


def inspect_partial_public() -> list[dict[str, object]]:
    """Check two actual, still-incomplete typed goals and their Web narratives."""
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r70_verified_narrative_projection.projection import (
        project_verified_general_narrative,
    )
    from web_group_proof import build_standard_web_group_proof_view

    results: list[dict[str, object]] = []
    for n, k in INCOMPLETE_CASES:
        goal = exact_prior_database_result(n, k)
        if goal is None:
            raise RuntimeError(f"R72_NO_REGISTERED_GOAL: n={n},k={k}")
        result = search_group_from_registered_goal(n=n, k=k, goal=goal)
        if (result.status not in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
                or result.conclusion is not None or not result.open_goals):
            raise RuntimeError(f"R72_NAMED_GOAL_PROMOTED: n={n},k={k}")
        model = build_proof_narrative_model(result)
        if (model.root_index is not None
                or model.status is not result.status
                or model.open_goals != result.open_goals
                or model.diagnostics != result.diagnostics
                or model.abstract_structure is not result.abstract_structure):
            raise RuntimeError(f"R72_PARTIAL_MODEL_CHANGED: n={n},k={k}")
        original = ["## 証明対象", "", "## 未解決 Goal"]
        if project_verified_general_narrative(original, model) is not original:
            raise RuntimeError("R72_R70_CHANGED_INCOMPLETE_NARRATIVE")
        markdown = render_model_backed_narrative_markdown(result, model)
        if (markdown.count("## 使用する結果") != 1
                or markdown.count("## 未解決 Goal") != 1
                or "未解決 Goal は証明済みの結論ではありません。" not in markdown
                or markdown.rstrip().endswith("□")):
            raise RuntimeError(f"R72_PARTIAL_RENDERING_CHANGED: n={n},k={k}")
        web = build_standard_web_group_proof_view(
            n=n, k=k, goal=goal, mode="narrative", citation_source="model",
        )
        headings = [line.prefix for line in web.rendered_lines if line.kind == "heading"]
        if (web.key != "generic-partial-proof" or not web.partial_result
                or headings.count("使用する結果") != 1
                or headings.count("未解決 Goal") != 1):
            raise RuntimeError(f"R72_PARTIAL_WEB_REGRESSION: n={n},k={k}")
        results.append({
            "group": f"pi_{n+k}^{n}",
            "status": result.status.name,
            "named_goal_incomplete": True,
            "open_goal_count": len(result.open_goals),
            "abstract_certificate_present": result.abstract_structure is not None,
            "web_key": web.key,
            "model_root_index": None,
        })
    return results


def main() -> int:
    """Run R72 without altering Git, production files, or canonical documents."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    pins = r71_source_guard(root)
    check_prior_package(root)
    head = git_head(root)
    remote = git_head(root, "origin/develop")
    if head not in ALLOWED_LOCAL_HEADS or remote != head:
        raise RuntimeError("R72_HEAD_REVIEW_REQUIRED: " + head + " vs " + remote)
    tracked_changes(root)
    docs = document_readiness(root)
    print("PHASE174_R72_SOURCE_GUARD=PASS")
    print("PHASE174_R72_SOURCE_PINS=" + str(len(pins) + 1))
    print("PHASE174_R72_R71_MERGED_HEAD=" + MERGED_R71_HEAD)
    print("PHASE174_R72_LOCAL_HEAD=" + head)
    print("PHASE174_R72_ORIGIN_DEVELOP=" + remote)
    print("PHASE174_R72_TRACKED_CHANGES=0")
    print("PHASE174_R72_PRODUCTION_CHANGES=0")
    if args.dry_run:
        print("PHASE174_R72_GATE=PASS_R72_READ_ONLY_DRYRUN")
        print("(END)")
        return 0

    prior_path = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
                  / "EHPProofTracerAudit" / R71_PACKAGE / "report.json")
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    completed = validate_r71_report(prior, head)
    partial = inspect_partial_public()
    missing_docs = [item["path"] for item in docs if item["closeout_full_file_update_required"]]
    record = {
        "phase": "174-R72", "local_head": head,
        "origin_develop": remote, "source_guard_pins": len(pins) + 1,
        "r71_report_path": str(prior_path),
        "r71_complete_case_count": len(completed),
        "r71_focused_pytest_passed": 81,
        "r71_focused_pytest_is_user_reported": True,
        "r71_complete_results_are_prior_evidence": True,
        "incomplete_public_cases": partial,
        "canonical_documents": docs,
        "missing_phase174_closeout_records": missing_docs,
        "production_changes": [], "new_given": 0, "new_mathematical_rules": 0,
        "whole_test_suite_executed": False,
        "full_sentence_semantics_certified": False,
        "phase174_closed": False,
        "next_gate": "Phase 174 full-document outputs and one phase-end active-suite pytest",
    }
    target = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
              / "EHPProofTracerAudit" / PACKAGE / "report.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print("PHASE174_R72_R71_EVIDENCE_COMPLETE_CASES=" + str(len(completed)))
    for item in partial:
        print("PHASE174_R72_INCOMPLETE_CASE=" + item["group"] + ":PASS:" + item["status"])
    print("PHASE174_R72_MISSING_FINAL_DOC_RECORDS=" + str(len(missing_docs)))
    for name in missing_docs:
        print("PHASE174_R72_CLOSEOUT_DOCUMENT_PENDING=" + name)
    print("PHASE174_R72_NEW_GIVEN=0")
    print("PHASE174_R72_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R72_FULL_PYTEST_EXECUTED=False")
    print("PHASE174_R72_PHASE_CLOSED=False")
    print("PHASE174_R72_REPORT=" + str(target))
    print("PHASE174_R72_GATE=PASS_R72_PREFLIGHT_GAPS_IDENTIFIED")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_audit.py`

```python
"""R72 focused tests for prior evidence, document gaps, and fail-closed checks."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from phase174_r3_r7_r71_common_narrative_regression.audit import (
    PINS as R71_PINS,
    REVIEWED_REMOTE_HEAD,
)
from phase174_r3_r7_r72_closeout_preflight.audit import (
    ALLOWED_LOCAL_HEADS,
    MERGED_R71_HEAD,
    DOCUMENTS,
    EXPECTED_REFERENCES,
    INCOMPLETE_CASES,
    check_prior_package,
    document_readiness,
    git_blob_sha,
    validate_r71_report,
)


def fixture_prior() -> dict[str, object]:
    """Build a small simulated R71 report; no source search is bypassed."""
    return {
        "phase": "174-R71",
        "reviewed_remote_head": REVIEWED_REMOTE_HEAD,
        "local_head": REVIEWED_REMOTE_HEAD,
        "source_files_checked": list(R71_PINS),
        "production_changes": [],
        "new_given": 0,
        "new_mathematical_rules": 0,
        "whole_test_suite_executed": False,
        "full_sentence_semantics_certified": False,
        "public_samples": [
            {"n": n, "k": k, "group": f"pi_{n+k}^{n}",
             "status": "COMPLETE", "verified_root": True,
             "step_count": 5, "reference_count": refs,
             "markdown_sha256": "a" * 64}
            for (n, k), refs in EXPECTED_REFERENCES.items()
        ],
    }


def test_r71_evidence_accepts_exact_completed_case_contract() -> None:
    report = fixture_prior()
    result = validate_r71_report(report, REVIEWED_REMOTE_HEAD)
    assert len(result) == 8
    assert [item["reference_count"] for item in result] == list(EXPECTED_REFERENCES.values())


def test_r71_evidence_survives_audit_only_r71_merge() -> None:
    result = validate_r71_report(fixture_prior(), MERGED_R71_HEAD)
    assert len(result) == len(EXPECTED_REFERENCES)
    assert ALLOWED_LOCAL_HEADS == (REVIEWED_REMOTE_HEAD, MERGED_R71_HEAD)


def test_r71_evidence_rejects_duplicate_complete_case() -> None:
    report = fixture_prior()
    report["public_samples"][1] = deepcopy(report["public_samples"][0])
    with pytest.raises(RuntimeError, match="R72_R71_SAMPLE_UNEXPECTED_OR_DUPLICATED"):
        validate_r71_report(report, REVIEWED_REMOTE_HEAD)


def test_r71_evidence_rejects_promoted_or_unverified_case() -> None:
    report = fixture_prior()
    report["public_samples"][0]["verified_root"] = False
    with pytest.raises(RuntimeError, match="R72_R71_SAMPLE_CONTRACT_CHANGED"):
        validate_r71_report(report, REVIEWED_REMOTE_HEAD)


def test_r71_evidence_rejects_changed_reference_count() -> None:
    report = fixture_prior()
    report["public_samples"][0]["reference_count"] = 99
    with pytest.raises(RuntimeError, match="R72_R71_SAMPLE_CONTRACT_CHANGED"):
        validate_r71_report(report, REVIEWED_REMOTE_HEAD)


def test_r71_evidence_rejects_full_test_or_sentence_certification_claim() -> None:
    report = fixture_prior()
    report["whole_test_suite_executed"] = True
    with pytest.raises(RuntimeError, match="R72_R71_REPORT_SCOPE_CHANGED"):
        validate_r71_report(report, REVIEWED_REMOTE_HEAD)
    report = fixture_prior()
    report["full_sentence_semantics_certified"] = True
    with pytest.raises(RuntimeError, match="R72_R71_REPORT_SCOPE_CHANGED"):
        validate_r71_report(report, REVIEWED_REMOTE_HEAD)


def test_r71_evidence_rejects_different_head() -> None:
    with pytest.raises(RuntimeError, match="R72_HEAD_REVIEW_REQUIRED"):
        validate_r71_report(fixture_prior(), "a" * 40)


def test_prior_r71_report_head_cannot_be_rewritten_to_merge_head() -> None:
    report = fixture_prior()
    report["local_head"] = MERGED_R71_HEAD
    with pytest.raises(RuntimeError, match="R72_R71_REPORT_HEAD_MISMATCH"):
        validate_r71_report(report, MERGED_R71_HEAD)


def test_document_gap_detection_does_not_mutate_files(tmp_path: Path) -> None:
    original = {}
    for path in DOCUMENTS:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        text = "# EHP Proof Tracer\n\n<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->\n"
        target.write_text(text, encoding="utf-8")
        original[path] = target.read_bytes()
    report = document_readiness(tmp_path)
    assert len(report) == 5
    assert all(item["closeout_full_file_update_required"] for item in report)
    assert all((tmp_path / path).read_bytes() == raw for path, raw in original.items())


def test_document_gap_can_be_cleared_by_an_actual_closeout_marker(tmp_path: Path) -> None:
    for path in DOCUMENTS:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "# EHP Proof Tracer\n<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->\n"
            "<!-- PHASE174_FINAL_CLOSEOUT_20261111 -->\n", encoding="utf-8",
        )
    assert all(not item["closeout_full_file_update_required"]
               for item in document_readiness(tmp_path))


def test_document_history_missing_fails_closed(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# EHP Proof Tracer\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R72_PHASE173_HISTORY_MISSING"):
        document_readiness(tmp_path)


def test_r71_prior_audit_script_is_source_pinned() -> None:
    root = Path(__file__).resolve().parents[2]
    check_prior_package(root)


def test_git_blob_fingerprint_and_partial_sample_contract() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
    assert INCOMPLETE_CASES == ((4, 8), (4, 31))
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$env:PYTHONDONTWRITEBYTECODE = '1'
$package = 'phase174_r3_r7_r72_closeout_preflight'

python -m "$package.audit" --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R72 source/head/document preflight failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R72_GATE=PASS_R72_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib `
    "$package/tests/test_audit.py" `
    'phase174_r3_r7_r71_common_narrative_regression/tests/test_audit.py' `
    'phase174_r3_r7_r70r1_assoc_chain_display_fix/tests/test_install.py' `
    'phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py'
if ($LASTEXITCODE -ne 0) { throw 'R72 focused pytest failed' }

python -m "$package.audit"
if ($LASTEXITCODE -ne 0) { throw 'R72 prior-evidence or partial public preflight failed' }

Write-Output 'PHASE174_R72_GATE=PASS_R72_FOCUSED_AND_PREFLIGHT'
Write-Output '(END)'
```

## `__init__.py`

```python
"""Phase 174 R72 read-only pre-closeout verification package."""
```

## `README.md`

```markdown
# Phase 174 R72 — Read-only Closeout Preflight

R72 records closeout prerequisites after the successful R71 regression audit. This package does not close Phase 174 and does not mutate production code, the five canonical documents, the Git index, or the proof registry.

The preflight checks the previously generated R71 report (eight completed public cases and citation counts), checks that the audited source code and the prior R71 audit script are unchanged, and rechecks two genuinely incomplete named-generator public cases: `n=4,k=8` and `n=4,k=31`. R70's completion-only projection must leave both partial models untouched.

The five canonical documents are inspected for a Phase 174 final-closeout record. Missing records are reported as pending work, not silently written. The full active pytest suite is reserved for the phase-end final gate, not R72. The 81 passed focused tests are user-reported R71 evidence, not a new R72 run.

## Commands

From the project repository root on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r72_closeout_preflight\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r72_closeout_preflight\run.ps1"
```

The pinned source boundary allows either the original R71 run HEAD (`01c5246a`) or the audit-only merged R71 HEAD (`b6609959`), provided local HEAD and `origin/develop` match. The R71 report must still attest to its original `01c5246a` run. If `origin/develop`, previously reviewed sources, or tracked files have changed beyond that reviewed boundary, review the differences rather than overriding the safety gate. The final output `PASS_R72_FOCUSED_AND_PREFLIGHT` is **not** a Phase 174 closeout result.
```

## `AUDIT_NOTES_JA.md`

```markdown
# Phase 174 R72 — Closeout Preflight（正式終了前監査）

## 1. 位置づけ

Phase 174 R71 は、ユーザー実行結果として限定 pytest 81 PASS、完成8群の実探索・共通 Renderer 回帰 PASS、Reference 件数 `8,4,4,4,4,7,7,3`、既存実装変更0件だった。R71 レポートは `%LOCALAPPDATA%/EHPProofTracerAudit/phase174_r3_r7_r71_common_narrative_regression/report.json` にある。本 R72 はその保存証拠を再検査するが、81件の pytest を改めて実行したという主張はしない。

## 2. 監査対象

- `akebono03/ehp-proof-tracer` の `develop`。R71 実行時 HEAD `01c5246a011b43e10ed85699a6048f117562a748` と R71 監査ディレクトリのみを追加した merge HEAD `b66099598177d74e979492f1d04a916e6f0821a8` を監査済みの同一実装系列として許可する。R71 レポート内の実行 HEAD は旧 SHA のまま固定する。
- R71 が固定した既存ファイル9件と、R71 の `audit.py` 本文1件の Git blob SHA。
- R71 の保存 JSON の completed 8群、引用件数、Verified root、renderer 出力 digest、評価範囲の否定条件。
- 未完成の記名 Goal：$(n,k)=(4,8)$ の $\pi_{12}^{4}$、$(4,31)$ の $\pi_{35}^{4}$。Typed Backward Search・単一 ProofNarrativeModel・共通 Renderer・Web の `generic-partial-proof` が一致すること。
- 主要5文書 `README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md`。Phase 173 の過去記録の保持と Phase 174 正式終了節の有無。

## 3. 制約

- Source-first、First Successful Proof Search、唯一性検査なし。
- 新しい GIVEN・数学的推論規則・群専用 Narrative は0件。
- 既存実装、既存テスト、5つの主要文書に変更を加えない。
- `git diff` と `git diff --cached` の既存追跡済み差分は不可。新しい R71/R72 監査ディレクトリは未追跡のままでよい。
- 全体 pytest は実施しない。次の正式 Closeout Gate で Phase 174 の最後に1回だけ行う。
- `PHASE174_R72_GATE=PASS_R72_FOCUSED_AND_PREFLIGHT` は監査工程の成功であり、Phase 174 の正式終了を意味しない。

## 4. 完了前の明示的残件

1. 5文書について現在状態に一致する Phase 174 の正式 Closeout 内容を作成する。更新する際はそれぞれ**全文ファイル**を出力する。README は英語、他4文書は日本語。`development_log.md` と `proof_records.md` は原則追記し、過去の履歴と最新の状態を区別する。
2. R72 で確認できない全 ProofStep／文章の数学的意味を網羅的に証明したとは記載しない。
3. 新文書の内容・Git の変更と必要な限定テストを点検する。
4. Phase 174 最後の Gate で、現行アクティブ `tests/` の全体 pytest を1回のみ実施する。
5. 完全な数学的真理の保証やすべての $(n,k)$ の完成は認定の対象外とする。

## 5. 実行条件

- Python / pytest が使える Windows PowerShell でプロジェクトルートから実行する。
- R71 の本実行を同じ Windows ユーザーで完了済みであること。
- `origin/develop` と `HEAD` が一致し、いずれも監査済みの2つの SHA のどちらかであり、既存追跡ファイルに差分がないこと。`git fetch` は実行せず、第三の SHA は監査・再ピン留めが必要。

R72 は `report.json` を `%LOCALAPPDATA%/EHPProofTracerAudit/phase174_r3_r7_r72_closeout_preflight/` に出力する。
```

