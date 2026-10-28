"""R10ET-R6B: read existing R6 pi_10^8 evidence without changing the project."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

PHASE_DIRECTORY = "phase169_r10et_r6_residual_definition_dependency_audit"
TARGET = "pi_10^8"


def existing_report(root: Path, specified: Path | None) -> Path:
    """Choose a preexisting R6 report, preferring the user's exact run."""
    if specified is not None:
        candidate = specified.resolve()
        if not candidate.is_file() or candidate.name != "audit.json":
            raise ValueError(f"R6 audit.json not found at {candidate}")
        return candidate
    audit_root = root / PHASE_DIRECTORY / "output"
    candidates = sorted(
        audit_root.glob("*/audit.json"),
        key=lambda path: (path.stat().st_mtime_ns, str(path)),
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(f"no existing R6 report found in {audit_root}")
    return candidates[0]


def diagnostic_lines(
    report: dict[str, Any], trace: dict[str, Any] | None,
) -> list[str]:
    """Print factual, case-specific results; never waive the prior R6 failure."""
    cases = report.get("cases")
    if not isinstance(cases, list):
        raise ValueError("R6 report has no case list")
    matches = [row for row in cases if row.get("case") == TARGET]
    if len(matches) != 1:
        raise ValueError(f"expected one {TARGET} report row, found {len(matches)}")
    row = matches[0]
    problems = row.get("problems")
    if not isinstance(problems, list):
        raise ValueError("R6 report has no per-case reasons")
    lines = [
        f"R10ET_R6B_CASE={TARGET}",
        f"R10ET_R6B_R6_REQUIRED_PASS={report.get('required_pass')}",
        f"R10ET_R6B_R6_PROBES_PASS={report.get('probes_pass')}",
        f"R10ET_R6B_TRUST={row.get('trust')}",
        f"R10ET_R6B_STATUS={row.get('status')}",
        f"R10ET_R6B_ELIGIBLE={row.get('eligible_image_steps')}",
        f"R10ET_R6B_CANONICAL={row.get('canonical_image_steps')}",
        f"R10ET_R6B_REMAINING={row.get('remaining_eligible_cited_steps')}",
        f"R10ET_R6B_NONELIGIBLE={row.get('noneligible_image_steps')}",
        f"R10ET_R6B_ROOT_ANCESTRY_STEPS={row.get('root_ancestry_steps')}",
        f"R10ET_R6B_PROBLEM_COUNT={len(problems)}",
    ]
    for index, problem in enumerate(problems, start=1):
        lines.append(f"R10ET_R6B_PROBLEM_{index}={problem}")
    for index, locator in enumerate(row.get("reference_locators", []), start=1):
        lines.append(f"R10ET_R6B_REFERENCE_{index}={locator}")
    for index, support in enumerate(row.get("root_support", []), start=1):
        lines.append(
            f"R10ET_R6B_ROOT_SUPPORT_{index}_CITATIONS="
            f"{support.get('citation_numbers', [])}"
        )
        lines.append(f"R10ET_R6B_ROOT_SUPPORT_{index}_TYPE={support.get('type')}")
    if trace is None:
        lines.append("R10ET_R6B_TRACE=NOT_FOUND")
    else:
        lines.append("R10ET_R6B_TRACE=FOUND")
        lines.append(f"R10ET_R6B_ROOT_INDEX={trace.get('root_index')}")
        lines.append(f"R10ET_R6B_ROOT_PREMISES={trace.get('root_premises')}")
        for citation in trace.get("references", []):
            no = citation.get("number")
            lines.extend((
                f"R10ET_R6B_CITATION_{no}_LOCATOR={citation.get('locator')}",
                f"R10ET_R6B_CITATION_{no}_ROOT={citation.get('reachable_from_root')}",
                f"R10ET_R6B_CITATION_{no}_GIVEN={citation.get('directly_attributed_to_given')}",
                f"R10ET_R6B_CITATION_{no}_HEADING={citation.get('reference_heading_displayed')}",
                f"R10ET_R6B_CITATION_{no}_BODY={citation.get('body_marker_displayed')}",
            ))
        images = trace.get("images", [])
        lines.append(f"R10ET_R6B_IMAGE_COUNT={len(images)}")
        for image in images:
            eligible = image.get("eligible_for_common_definition")
            canonical = image.get("actual_canonical_common_definition")
            if (eligible != canonical or image.get("given_ancestor_citation_numbers")
                    or not canonical):
                i = image.get("index")
                lines.extend((
                    f"R10ET_R6B_IMAGE_{i}_ELIGIBLE={eligible}",
                    f"R10ET_R6B_IMAGE_{i}_CANONICAL={canonical}",
                    f"R10ET_R6B_IMAGE_{i}_RULE={image.get('inference_rule')}",
                    f"R10ET_R6B_IMAGE_{i}_CITATIONS={image.get('given_ancestor_citation_numbers')}",
                    f"R10ET_R6B_IMAGE_{i}_ROOT_ANCESTOR={image.get('root_ancestor')}",
                ))
    lines.append("R10ET_R6B_VERDICT=" + ("REVIEW_REQUIRED" if problems else "PASS"))
    lines.append("R10ET_R6B_AUDIT_ONLY_COMPLETE=PASS")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        path = existing_report(root, args.report)
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("phase") != "169 R10ET-R6" or data.get("mode") != "AUDIT_ONLY":
            raise ValueError("not an R10ET-R6 read-only report")
        trace_path = path.parent / "pi10_8" / "proof_steps.json"
        trace = (json.loads(trace_path.read_text(encoding="utf-8"))
                 if trace_path.is_file() else None)
        print(f"R10ET_R6B_SOURCE={path}")
        for line in diagnostic_lines(data, trace):
            print(line)
        return 0
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"R10ET_R6B_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
