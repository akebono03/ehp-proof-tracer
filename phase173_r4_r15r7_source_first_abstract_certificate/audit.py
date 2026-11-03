"""Validate source-first abstract certificates, not named-group Web completion."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import verified_db_step
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from proof import ProofRule


def inspect_k(k: int, bridge: object) -> dict[str, object]:
    """Inspect actual checked root and premise ancestry under one shared bridge."""
    result = search_source_first_abstract(k=k, bridge=bridge)
    if result is None:
        return {
            "k": k,
            "abstract_certified": False,
            "named_generator_shape_matched": False,
            "public_group_complete": False,
            "reason": "SOURCE_FIRST_ABSTRACT_PROOF_UNRESOLVED",
        }
    root = result.root_step
    premises = root.premises
    valid = (
        root.rule is ProofRule.INFERENCE
        and root.conclusion == result.conclusion
        and len(premises) == 4
        and root.inference_rule is not None
        and root.inference_rule.match_guard(premises, ())
        and premises[0].rule is ProofRule.GIVEN
        and verified_db_step(
            premises[1], proof_target=result.proof_target,
            bridge=result.source_context,
        )
        and verified_db_step(
            premises[2], proof_target=result.proof_target,
            bridge=result.source_context,
        )
        and premises[3].rule is ProofRule.INFERENCE
        and len(premises[3].premises) == 1
        and premises[3].premises[0].rule is ProofRule.GIVEN
        and result.public_group_complete is False
    )
    return {
        "k": k,
        "abstract_certified": bool(valid),
        "invariant_summands": [list(x) for x in result.conclusion.invariant_summands],
        "premise_count": len(premises),
        "hopf_inferred": premises[3].rule is ProofRule.INFERENCE,
        "prior_db_reverified": bool(valid),
        "named_generator_shape_matched": result.named_generator_shape_matched,
        "public_group_complete": result.public_group_complete,
        "source_context_links": len(result.source_context.proof_links),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "data" / "sphere.csv").is_file():
        raise RuntimeError("Expected repository root")
    bridge = build_shared_typed_bridge()
    rows = [inspect_k(k, bridge) for k in (4, 7, 8, 31)]
    report = {
        "phase": "173-R4-R15R7",
        "mode": "SOURCE_FIRST_ABSTRACT_CERTIFICATE_SEPARATE_FROM_NAMED_WEB_GROUP",
        "rows": rows,
        "public_route_changed": False,
        "new_given": 0,
        "named_generator_equalities_added": 0,
        "full_pytest_performed": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    for row in rows:
        print(
            "PHASE173_R4_R15R7_K=" + str(row["k"])
            + " ABSTRACT_CERTIFIED=" + str(row["abstract_certified"])
            + " NAMED_SHAPE=" + str(row["named_generator_shape_matched"])
            + " PUBLIC_COMPLETE=" + str(row["public_group_complete"]),
            flush=True,
        )
    k31 = rows[-1]
    passed = (
        all(row["abstract_certified"] for row in rows)
        and k31.get("invariant_summands") == [["finite", 2]] * 8
        and k31["named_generator_shape_matched"] is False
        and k31["public_group_complete"] is False
    )
    print("PHASE173_R4_R15R7_K31_SOURCE_FIRST_ABSTRACT=" + ("PASS" if passed else "FAIL"), flush=True)
    print("PHASE173_R4_R15R7_PUBLIC_COMPLETION=False", flush=True)
    print("PHASE173_R4_R15R7_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R7_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
