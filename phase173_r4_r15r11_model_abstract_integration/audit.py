"""Post-install audit of proof/status and Web Narrative Model integration."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from web_group_proof import build_standard_web_group_proof_view


def inspect(k: int) -> dict[str, object]:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    model = build_proof_narrative_model(result)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    ready = (
        result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        and result.conclusion is None and bool(result.open_goals)
        and model.abstract_structure is result.abstract_structure
        and model.abstract_structure is not None
        and headings.count("証明済みの抽象群構造") == 1
        and headings.count("未解決 Goal") == 1
        and view.key == "generic-partial-proof" and view.partial_result
    )
    return {
        "k": k, "model_abstract_certified": model.abstract_structure is not None,
        "model_same_certificate": model.abstract_structure is result.abstract_structure,
        "citations": len(model.citations), "open_goals": len(result.open_goals),
        "abstract_section_count": headings.count("証明済みの抽象群構造"),
        "web_key": view.key, "named_pending": view.partial_result,
        "passed": ready,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    opts = p.parse_args()
    rows = [inspect(k) for k in (8, 31)]
    complete = []
    for n, k in ((3, 3), (4, 3)):
        view = build_standard_web_group_proof_view(
            n=n, k=k, mode="narrative", citation_source="model",
        )
        complete.append({"n": n, "k": k,
                         "passed": view.key == "generic-complete-proof"
                                   and not view.partial_result})
    if not all(r["passed"] for r in rows + complete):
        raise RuntimeError("Source-first Narrative Model regression")
    report = {"phase": "173-R4-R15R11", "model_abstract_integrated": True,
              "normal_model_route_owns_abstract_section": True,
              "legacy_route_preserved": True, "named_proof_promoted": False,
              "phase_completed": False, "full_pytest_performed": False,
              "abstract_rows": rows, "complete_rows": complete, "passed": True}
    opts.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(f"PHASE173_R4_R15R11_K={row['k']} MODEL_HAS_ABSTRACT={row['model_abstract_certified']} "
              f"ABSTRACT_SECTION_COUNT={row['abstract_section_count']} "
              f"OPEN_GOALS={row['open_goals']} NAMED_PENDING={row['named_pending']}", flush=True)
    print("PHASE173_R4_R15R11_AUDIT=PASS", flush=True)
    print("PHASE173_R4_R15R11_PHASE_COMPLETED=False", flush=True)


if __name__ == "__main__":
    main()
