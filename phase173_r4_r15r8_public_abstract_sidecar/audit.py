"""Source-first abstract evidence in public result model, without named completion."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_partial_proof import (
    GroupStructureStatus,
    ProofSearchStatus,
    make_partial_proof_result,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r8_public_abstract_sidecar.attach import (
    attach_certified_abstract_structure,
)
from phase173_r4_r15r8_public_abstract_sidecar.install import preflight


def inspect_k(k: int, bridge: object) -> dict[str, object]:
    """Check the canonical result type carries evidence without named promotion.

    This is a result-model audit; it does not claim the unrelated group search
    has successfully generated any named generator equality or Web display.
    """
    target = exact_prior_database_result(4, k)
    named = make_partial_proof_result(
        n=4, k=k, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=(target,), diagnostics=("記名生成元の証明は未解決",),
    )
    enriched = attach_certified_abstract_structure(
        named, n=4, k=k, goal=target, bridge=bridge,
    )
    evidence = enriched.abstract_structure
    passed = bool(
        evidence is not None
        and evidence.group == enriched.target
        and enriched.status is ProofSearchStatus.SEARCH_FAILED
        and enriched.structure_status is GroupStructureStatus.UNKNOWN
        and enriched.conclusion is None
        and enriched.open_goals == (target,)
        and enriched.diagnostics == named.diagnostics
        and evidence.proof_step.inference_rule.match_guard(
            evidence.proof_step.premises, (),
        )
    )
    return {
        "k": k,
        "abstract_certified": passed,
        "invariant_summands": (
            [list(term) for term in evidence.invariant_summands]
            if evidence is not None else []
        ),
        "named_status_unchanged": enriched.status == named.status,
        "open_goals_unchanged": enriched.open_goals == named.open_goals,
        "named_conclusion_promoted": enriched.conclusion is not None,
        "named_generator_proved": False,
        "web_complete": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    preflight(root)
    shared = build_shared_typed_bridge()
    rows = [inspect_k(k, shared) for k in (4, 7, 8, 31)]
    # Run the real registered public selector once, not just a fabricated
    # presentation object. A name-labelled target remains incomplete.
    registered_target = exact_prior_database_result(4, 31)
    real_public = search_group_from_registered_goal(
        n=4, k=31, goal=registered_target, bridge=shared,
    )
    public_path_passed = bool(
        real_public.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        and real_public.abstract_structure is not None
        and real_public.conclusion is None
        and real_public.open_goals
        and real_public.structure_status is GroupStructureStatus.UNKNOWN
        and real_public.abstract_structure.invariant_summands == (("finite", 2),) * 8
    )
    passed = bool(
        public_path_passed
        and all(row["abstract_certified"] for row in rows)
        and rows[-1]["invariant_summands"] == [["finite", 2]] * 8
        and all(row["named_status_unchanged"] and row["open_goals_unchanged"]
                and row["named_conclusion_promoted"] is False for row in rows)
    )
    report = {
        "phase": "173-R4-R15R8",
        "mode": "CANONICAL_PUBLIC_PARTIAL_RESULT_ABSTRACT_SIDECAR",
        "rows": rows,
        "public_selector_checked": True,
        "public_selector_abstract_attached": public_path_passed,
        "public_selector_named_status": real_public.status.value,
        "public_selector_open_goals": len(real_public.open_goals),
        "public_web_renderer_changed": False,
        "named_group_public_complete": False,
        "full_pytest_performed": False,
        "passed": passed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for row in rows:
        print("PHASE173_R4_R15R8_K=" + str(row["k"])
              + " ABSTRACT_ATTACHED=" + str(row["abstract_certified"])
              + " NAMED_STATUS_UNCHANGED=" + str(row["named_status_unchanged"]),
              flush=True)
    print("PHASE173_R4_R15R8_K31_REAL_PUBLIC_SELECTOR="
          + ("PASS" if public_path_passed else "FAIL"), flush=True)
    print("PHASE173_R4_R15R8_K31_PUBLIC_RESULT_ABSTRACT="
          + ("PASS" if passed else "FAIL"), flush=True)
    print("PHASE173_R4_R15R8_WEB_COMPLETE=False", flush=True)
    print("PHASE173_R4_R15R8_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R8_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
