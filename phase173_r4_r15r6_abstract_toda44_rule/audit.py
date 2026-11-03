"""Report k-unbounded abstract roots, without promoting named/public proof."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
    canonical_abstract_result,
    expand_abstract_toda44,
)


def inspect_k(k: int) -> dict[str, object]:
    """Read registered group and abstract proposal for any permitted k."""
    if type(k) is not int or k < 3:
        raise ValueError("k must be an integer >= 3")
    goal = exact_prior_database_result(4, k)
    statement = canonical_abstract_result(goal)
    sources = (TodaProp44UniversalStatement(), TodaLemma54TypedSource())
    expansions = (
        expand_abstract_toda44(statement, sources, proof_target=goal)
        if statement is not None else ()
    )
    return {
        "k": k,
        "group": f"pi_{k + 4}^4",
        "registered_target": goal is not None,
        "abstract_result": statement is not None,
        "invariant_summands": (
            [list(item) for item in statement.invariant_summands]
            if statement is not None else []
        ),
        "source_screened_rule_proposals": len(expansions),
        "strict_named_generator_guard": (
            checked_general_inputs(goal) is not None if goal is not None else False
        ),
        "theorem_citation_screening_performed_here": False,
        "proof_step_replayed_in_this_audit": False,
        "new_given_created": False,
        "public_completion": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not (args.root / "data" / "sphere.csv").is_file():
        raise RuntimeError("Expected repository root")
    rows = [inspect_k(k) for k in (3, 4, 7, 8, 31)]
    report = {
        "phase": "173-R4-R15R6",
        "mode": "ABSTRACT_TODA44_TYPED_ROOT_NOT_PUBLIC_PROOF",
        "rows": rows,
        "new_named_generator_equalities": 0,
        "new_given": 0,
        "public_completion": False,
        "full_pytest_performed": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(
            "PHASE173_R4_R15R6_K=" + str(row["k"])
            + " ABSTRACT=" + str(row["abstract_result"])
            + " ROOT_CANDIDATE=" + str(row["source_screened_rule_proposals"])
            + " NAMED_GUARD=" + str(row["strict_named_generator_guard"]),
            flush=True,
        )
    k31 = rows[-1]
    passed = (
        k31["abstract_result"] is True
        and k31["source_screened_rule_proposals"] == 1
        and k31["invariant_summands"] == [["finite", 2]] * 8
        and k31["strict_named_generator_guard"] is False
        and k31["public_completion"] is False
    )
    print("PHASE173_R4_R15R6_K31_ABSTRACT_RULE=" + ("PASS" if passed else "FAIL"), flush=True)
    print("PHASE173_R4_R15R6_PUBLIC_COMPLETION=False", flush=True)
    print("PHASE173_R4_R15R6_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R6_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
