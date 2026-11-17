"""Phase 175 R4R3: review an isolated generic EHP two-summand quotient rule.

The previous R4 observation must exist and remain unchanged. Nothing in this
module edits production code, creates GIVENs, or runs the whole test suite.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

from phase175_r4_pi95_audit.audit import git, preflight
from phase175_r4r3_two_summand_quotient.rule import RULE_NAME


PACKAGE = "phase175_r4r3_two_summand_quotient"
REVIEWED_R4_GATE = "PASS_R4_PI95_FRONTIER_RECORDED_NOT_COMPLETE"
R4_REPORT_FOLDER = "phase175_r4_pi95_audit"
DRY_GATE = "PASS_R4R3_ISOLATED_RULE_DRYRUN"
FINAL_GATE = "PASS_R4R3_ISOLATED_RULE_NOT_PUBLIC"
REVIEWED_R4_REPORT_HEAD = "c77a26fdebe0eead67f1f7dad3a469aa446b134f"
REVIEWED_R4_COMMIT = "20622a303b8c4558fe297eed070b43ca2f322831"
REVIEWED_R4_COMMIT_CHANGES = {
    ".pytest_cache/v/cache/nodeids": "M",
    "phase175_r4_pi95_audit/AUDIT_PLAN_JA.md": "A",
    "phase175_r4_pi95_audit/CODE_FULL_JA.md": "A",
    "phase175_r4_pi95_audit/README.md": "A",
    "phase175_r4_pi95_audit/TEST_RESULTS_JA.md": "A",
    "phase175_r4_pi95_audit/__init__.py": "A",
    "phase175_r4_pi95_audit/audit.py": "A",
    "phase175_r4_pi95_audit/run.ps1": "A",
    "phase175_r4_pi95_audit/tests/test_audit.py": "A",
}


def r4_report_path(explicit: Path | None = None) -> Path:
    """Choose the last successful full R4 observation, never a DryRun."""
    if explicit is not None:
        path = explicit.resolve()
        if not path.is_file():
            raise RuntimeError("R4R3_R4_REPORT_NOT_FOUND: " + str(path))
        return path
    root = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    report_root = root / "EHPProofTracerAudit" / R4_REPORT_FOLDER
    choices = sorted(report_root.glob("*/report.json"), reverse=True)
    for path in choices:
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            continue
        if result.get("gate") == REVIEWED_R4_GATE:
            return path
    raise RuntimeError("R4R3_NO_PASSED_R4_REAL_REPORT")


def validate_r4_lineage(root: Path, report_head: object, current_head: object) -> dict[str, object]:
    """Accept only an unchanged HEAD or the exact reviewed R4 audit commit.

    The R4 real report was recorded just before its audit-only package was
    committed. The reviewed commit adds no mathematical/production sources;
    its only changed pre-existing file is pytest's nodeids cache. Do not
    accept an arbitrary descendant or a change to the R4 audit after that
    commit. Actual Git objects, parentage and file statuses are checked.
    """
    if not isinstance(report_head, str) or not isinstance(current_head, str):
        raise RuntimeError("R4R3_R4_HEAD_OR_PINS_CHANGED")
    if report_head == current_head:
        return {
            "report_head": report_head,
            "current_head": current_head,
            "status": "SAME_HEAD",
            "reviewed_changes": [],
        }
    if (report_head, current_head) != (
        REVIEWED_R4_REPORT_HEAD, REVIEWED_R4_COMMIT,
    ):
        raise RuntimeError("R4R3_R4_UNREVIEWED_HEAD_TRANSITION")
    _, actual_head = git(root, "rev-parse", "HEAD")
    if actual_head != current_head:
        raise RuntimeError("R4R3_R4_CURRENT_HEAD_MISMATCH")
    _, actual_parent = git(root, "rev-parse", current_head + "^1")
    if actual_parent != report_head:
        raise RuntimeError("R4R3_R4_UNREVIEWED_PARENT")
    _, changed = git(
        root, "diff", "--name-status", "--no-renames",
        report_head, current_head,
    )
    actual_changes: dict[str, str] = {}
    for line in changed.splitlines():
        fields = line.split("\t")
        if len(fields) != 2 or fields[0] not in {"A", "M"}:
            raise RuntimeError("R4R3_R4_UNREVIEWED_COMMIT_DIFF")
        status, path = fields
        if path in actual_changes:
            raise RuntimeError("R4R3_R4_UNREVIEWED_COMMIT_DIFF")
        actual_changes[path] = status
    if actual_changes != REVIEWED_R4_COMMIT_CHANGES:
        raise RuntimeError("R4R3_R4_UNREVIEWED_COMMIT_DIFF")
    return {
        "report_head": report_head,
        "current_head": current_head,
        "status": "REVIEWED_R4_AUDIT_ONLY_COMMIT",
        "reviewed_changes": sorted(actual_changes),
    }


def validate_r4_report(report: object, current_head: str) -> dict[str, object]:
    """Never infer target proof or trust from an unchecked prior report."""
    if not isinstance(report, dict):
        raise RuntimeError("R4R3_REPORT_NOT_OBJECT")
    if (report.get("phase") != "175-R4"
            or report.get("mode") != "READ_ONLY_AUDIT"
            or report.get("dry_run") is not False
            or report.get("gate") != REVIEWED_R4_GATE
            or report.get("new_given") != 0
            or report.get("new_mathematical_rules") != 0
            or report.get("full_pytest_executed") is not False
            or report.get("production_changes") != []):
        raise RuntimeError("R4R3_R4_GATE_OR_POLICY_MISMATCH")

    r4_preflight = report.get("preflight")
    if (not isinstance(r4_preflight, dict)
            or r4_preflight.get("head") != current_head
            or r4_preflight.get("pinned_source_count") != 18):
        raise RuntimeError("R4R3_R4_HEAD_OR_PINS_CHANGED")

    observed = report.get("observations")
    rows = report.get("actual_rows")
    source = report.get("source")
    if (not isinstance(observed, dict)
            or observed.get("target_group") != "pi_9^5"
            or observed.get("prior_group") != "pi_8^4"
            or observed.get("open_goals_count") != 3
            or observed.get("target_status") != "INCOMPLETE_AND_WEB_CONFIRMED"
            or observed.get("prior_status") != "COMPLETE_AND_WEB_VERIFIED"
            or observed.get("proof_complete") is not False
            or not isinstance(observed.get("open_goals"), list)
            or len(observed["open_goals"]) != 3
            or not isinstance(rows, dict)
            or not isinstance(rows.get("target"), dict)
            or rows["target"].get("search_proven_count") != 0
            or not isinstance(rows.get("prior_pi84"), dict)
            or rows["prior_pi84"].get("trust_verified") is not True
            or not isinstance(source, dict)
            or source.get("prior_pi84_printed") is not True
            or source.get("source_proposition25") is not True
            or source.get("source_ehp_delta_eta9") is not True
            or source.get("source_ehp_delta_iota9") is not True
            or source.get("source_pi95_quotient") is not True
            or source.get("source_is_derived_goal_proof") is not False):
        raise RuntimeError("R4R3_R4_OPEN_GOAL_OR_SOURCE_EVIDENCE_CHANGED")

    return {
        "target_group": observed["target_group"],
        "prior_group": observed["prior_group"],
        "open_goals_count": observed["open_goals_count"],
        "target_proven_steps": rows["target"]["search_proven_count"],
        "prior_verified": rows["prior_pi84"]["trust_verified"],
        "source_prop25_seen": source["source_proposition25"],
        "proof_complete": False,
    }


def make_report_path() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    path = root / "EHPProofTracerAudit" / PACKAGE / stamp
    path.mkdir(parents=True, exist_ok=False)
    return path


def run(root: Path, dry_run: bool, r4_report: Path | None = None) -> int:
    output = make_report_path()
    result: dict[str, object] = {
        "phase": "175-R4R3",
        "mode": "ISOLATED_GENERIC_INFERENCE",
        "gate": "FAIL_R4R3_ISOLATED_RULE",
        "dry_run": dry_run,
        "production_changes": [],
        "new_given": 0,
        "new_mathematical_rules": 1,
        "rule_connected_to_public": False,
        "complete_proof": False,
        "full_pytest_executed": False,
    }
    try:
        examined = preflight(root)
        result["preflight"] = examined
        report_file = r4_report_path(r4_report)
        loaded = json.loads(report_file.read_text(encoding="utf-8"))
        result["r4_report"] = str(report_file)
        r4_preflight = loaded.get("preflight") if isinstance(loaded, dict) else None
        r4_head = r4_preflight.get("head") if isinstance(r4_preflight, dict) else None
        lineage = validate_r4_lineage(root, r4_head, examined["head"])
        result["r4_lineage"] = lineage
        result["r4_observation"] = validate_r4_report(loaded, lineage["report_head"])
        result["mathematical_rule"] = RULE_NAME
        result["unproven_public_premises"] = [
            "verified pi_8^4 direct-sum presentation in the search context",
            "proved pi_10^9 = (Z/2){eta_9} presentation",
            "inferred Delta(eta_9) is a chosen pi_8^4 summand generator",
            "inferred Proposition 4.2 Delta-to-E exactness window",
            "inferred E:pi_8^4 -> pi_9^5 surjective",
            "inferred E(nu_4 eta_7) = nu_5 eta_8",
        ]
        result["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
        result["traceback"] = traceback.format_exc()[-4000:]

    (output / "report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    report_md = "\n".join([
        "# Phase 175 R4R3 — 一般商群推論の隔離監査", "",
        "Gate: `" + str(result["gate"]) + "`", "",
        "新規 GIVEN: 0。新規一般推論規則: 1。", "",
        "対象群の完成証明・公開 Proof Tree・Narrative は変更しない。", "",
        "R4 report: `" + str(result.get("r4_report", "UNVERIFIED")) + "`", "",
        "## 必要な証明義務", "",
        *["- " + x for x in result.get("unproven_public_premises", [])],
        "", "次段階で、実際に検証された前提と出典を公開 Provider へ接続する。", "",
    ])
    (output / "report.md").write_text(report_md, encoding="utf-8")
    print("PHASE175_R4R3_HEAD=" + str(result.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R3_PINNED_SOURCES=" + str(result.get("preflight", {}).get("pinned_source_count", 0)))
    print("PHASE175_R4R3_NEW_GIVEN=0")
    print("PHASE175_R4R3_NEW_GENERAL_RULES=1")
    print("PHASE175_R4R3_PUBLIC_PROOF=NOT_COMPLETE")
    print("PHASE175_R4R3_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R3_REPORT=" + str(output / "report.json"))
    print("PHASE175_R4R3_GATE=" + str(result["gate"]))
    if "error" in result:
        print("PHASE175_R4R3_ERROR=" + str(result["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4-report", type=Path, default=None)
    options = parser.parse_args(argv)
    return run(options.root.resolve(), options.dry_run, options.r4_report)


if __name__ == "__main__":
    sys.exit(main())
