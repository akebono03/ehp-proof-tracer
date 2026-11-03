"""Check the canonical Web Group proof projection without completing named goals."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.install import preflight
from web_group_proof import build_standard_web_group_proof_view


def inspect_public(k: int) -> dict[str, object]:
    """Inspect both canonical search and model-backed shared Web projection."""
    goal = exact_prior_database_result(4, k)
    if goal is None:
        raise RuntimeError("Expected exact registered group target")
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    has_abstract = result.abstract_structure is not None
    headings = tuple(line.prefix for line in view.rendered_lines if line.kind == "heading")
    theorem_math = tuple(line.statement_latex or "" for line in view.rendered_lines)
    printed = (
        "証明済みの抽象群構造" in headings
        and any(rf"\pi_{{{k+4}}}^{{4}}" in latex and r"\cong" in latex
                for latex in theorem_math)
    )
    named_pending = bool(
        result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        and result.conclusion is None and result.open_goals
        and view.key == "generic-partial-proof" and view.partial_result
    )
    return {
        "k": k,
        "group": f"pi_{k+4}^4",
        "abstract_attached": has_abstract,
        "abstract_rendered": printed,
        "named_search_status": result.status.value,
        "named_open_goals": len(result.open_goals),
        "web_key": view.key,
        "web_partial": view.partial_result,
        "public_named_complete": not named_pending,
        "passed": has_abstract and printed and named_pending,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    preflight(args.root)
    rows = [inspect_public(k) for k in (8, 31)]
    if not all(row["passed"] for row in rows):
        raise RuntimeError("Canonical Web abstract evidence not rendered or named status changed")
    report = {
        "phase": "173-R4-R15R9",
        "mode": "COMMON_WEB_ABSTRACT_EVIDENCE_PROJECTION",
        "observations": rows,
        "named_complete_promoted": False,
        "specialized_narrative_added": False,
        "full_pytest_performed": False,
        "passed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    for row in rows:
        print("PHASE173_R4_R15R9_K=" + str(row["k"])
              + " ABSTRACT_RENDERED=" + str(row["abstract_rendered"])
              + " NAMED_PENDING=" + str(not row["public_named_complete"]), flush=True)
    print("PHASE173_R4_R15R9_K31_PUBLIC_ABSTRACT_RENDERED=PASS", flush=True)
    print("PHASE173_R4_R15R9_WEB_NAMED_COMPLETE=False", flush=True)
    print("PHASE173_R4_R15R9_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R9_AUDIT=PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
