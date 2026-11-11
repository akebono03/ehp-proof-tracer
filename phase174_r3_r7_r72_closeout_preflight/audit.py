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
