"""Summarize the existing Phase 173 R3 audit report; never run proof search."""
from __future__ import annotations

import json
import os
from pathlib import Path

EXPECTED_HEAD = "10f77860a5631d363d606e76b8c1f12ee6c500d5"
TARGETS = ((4, 3), (5, 3))


def default_report_path() -> Path:
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        raise RuntimeError("LOCALAPPDATA is not available")
    return (
        Path(local_appdata)
        / "EHPProofTracerRecovery"
        / "phase173_r3_manual"
        / "audit.json"
    )


def load_report(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"R3 audit.json not found: {path}")
    report = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(report, dict):
        raise ValueError("R3 report must be an object")
    if report.get("head") != EXPECTED_HEAD:
        raise ValueError("R3 report was created from a different source HEAD")
    if report.get("mode") != "AUDIT_ONLY":
        raise ValueError("R3 report is not marked AUDIT_ONLY")
    rows = report.get("rows")
    if not isinstance(rows, list) or len(rows) != len(TARGETS):
        raise ValueError("Expected exactly two R3 report rows")
    if tuple((row.get("n"), row.get("k")) for row in rows) != TARGETS:
        raise ValueError("Unexpected R3 target coordinates")
    for row in rows:
        roots = row.get("roots")
        if not isinstance(roots, list):
            raise ValueError("Root list is missing")
        if row.get("root_candidate_count") != len(roots):
            raise ValueError("Root candidates are incomplete or truncated")
        if row.get("target_direct_given_count") != 0:
            raise ValueError("Target is incorrectly available as a direct GIVEN")
        if not isinstance(row.get("prior_sources"), list):
            raise ValueError("Prior source listing is missing")
        for root in roots:
            if not isinstance(root.get("rule"), str) or not isinstance(root.get("children"), list):
                raise ValueError("Malformed root/children record")
    return report


def format_report(report: dict) -> str:
    output = ["PHASE173_R3_FRONTIER_READOUT=AUDIT_ONLY"]
    for row in report["rows"]:
        output.append(
            f"TARGET pi_{row['n'] + row['k']}^{row['n']} "
            f"locator={row.get('source_locator')} "
            f"given={row.get('screened_given_count')} "
            f"roots={len(row['roots'])}"
        )
        for position, root in enumerate(row["roots"], start=1):
            output.append(f"  ROOT {position}: {root['rule']}")
            for child_index, child in enumerate(root["children"], start=1):
                count = child.get("child_proposal_count", "NOT_PROBED_DUPLICATE")
                direct = child.get("exact_screened_given", "NOT_PROBED_DUPLICATE")
                output.append(
                    f"    SUBGOAL {child_index}: {child.get('type')} "
                    f"proposals={count} exact_given={direct}"
                )
                for rule in child.get("child_proposal_rules", []):
                    output.append(f"      RULE: {rule}")
                if "child_probe_error" in child:
                    output.append(f"      PROBE_ERROR: {child['child_probe_error']}")
                output.append(f"      TARGET_REPR: {child.get('repr', '')}")
        for source in row["prior_sources"]:
            output.append(
                f"  PRIOR n={source.get('n')} k={source.get('k')} "
                f"eligible={source.get('eligible')} "
                f"stable_source={source.get('stable_source')} "
                f"reason={source.get('reason')}"
            )
    output.append("PHASE173_R3_FRONTIER_READOUT=PASS")
    output.append("OBSERVATION_IS_NOT_A_PROOF=True")
    return "\n".join(output)


def main() -> int:
    print(format_report(load_report(default_report_path())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
