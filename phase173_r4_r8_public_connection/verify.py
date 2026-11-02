"""Verify normal Group query, source provenance, and Web narrative for three groups."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import verified_db_step
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from proof import ProofRule, ProofStep
from web_group_proof import build_standard_web_group_proof_view


ROOT_RULE = "Toda Proposition 4.4 source-first n=4 typed direct-sum transport"


def _ancestry(step: ProofStep) -> tuple[ProofStep, ...]:
    seen: set[int] = set()
    result: list[ProofStep] = []

    def visit(current: ProofStep) -> None:
        if id(current) in seen:
            return
        seen.add(id(current))
        result.append(current)
        for premise in current.premises:
            visit(premise)

    visit(step)
    return tuple(result)


def inspect_public() -> tuple[dict, ...]:
    """Never equate an isolated root or a successful pytest with a Web proof."""
    rows = []
    for dimension in (8, 9, 10):
        stem = dimension - 4
        contexts = []
        result = search_group_from_registered_goal(n=4, k=stem, context_sink=contexts.append)
        complete = result.status is ProofSearchStatus.COMPLETE
        roots = tuple(
            step for step in result.proven_steps
            if step.rule is ProofRule.INFERENCE
            and step.inference_rule is not None
            and step.inference_rule.name == ROOT_RULE
            and step.conclusion == result.conclusion
        )
        checked = _ancestry(roots[0]) if len(roots) == 1 else ()
        source_certified = bool(
            complete and len(contexts) == 1 and len(roots) == 1
            and len(roots[0].premises) == 4
            and roots[0].premises[0].rule is ProofRule.GIVEN
            and verified_db_step(roots[0].premises[1], proof_target=result.conclusion, bridge=contexts[0])
            and verified_db_step(roots[0].premises[2], proof_target=result.conclusion, bridge=contexts[0])
            and roots[0].premises[3].rule is ProofRule.INFERENCE
            and roots[0].premises[3].conclusion == canonical_hopf_relation()
            and any(step.rule is ProofRule.GIVEN
                    and type(step.conclusion) is TodaLemma54TypedSource
                    for step in checked)
            and not result.open_goals
        )
        # The canonical Web trust boundary may still reject a complete search.
        view = build_standard_web_group_proof_view(
            n=4, k=stem, max_depth=2, mode="narrative", citation_source="model",
        )
        web_complete = bool(
            view.key == "generic-complete-proof"
            and not view.partial_result and view.steps and view.rendered_lines
        )
        row = {
            "group": f"pi_{dimension}^4", "n": 4, "k": stem,
            "public_status": result.status.value,
            "public_complete": complete,
            "root_count": len(roots),
            "source_certified": source_certified,
            "public_open_goals": len(result.open_goals),
            "public_proven_steps": len(result.proven_steps),
            "web_complete": web_complete,
            "web_key": view.key,
            "web_lines": len(view.rendered_lines),
            "diagnostics": [str(item)[:1200] for item in result.diagnostics[:5]],
        }
        rows.append(row)
        print(
            "PHASE173_R4_R8_" + row["group"]
            + " STATUS=" + row["public_status"]
            + " ROOT_CERTIFIED=" + str(row["source_certified"])
            + " OPEN=" + str(row["public_open_goals"])
            + " WEB_COMPLETE=" + str(row["web_complete"])
            + " WEB_KEY=" + str(row["web_key"])
            + " STEPS=" + str(row["public_proven_steps"]),
            flush=True,
        )
    return tuple(rows)


def main() -> int:
    rows = inspect_public()
    success = len(rows) == 3 and all(
        row["public_complete"] and row["source_certified"]
        and row["public_open_goals"] == 0
        and row["web_complete"] and row["web_key"] == "generic-complete-proof"
        for row in rows
    )
    output = Path(__file__).resolve().parent / "verification_result.json"
    output.write_text(json.dumps({
        "phase": "173 R4-R8", "mode": "PUBLIC_CONNECTOR_VERIFICATION",
        "results": rows, "all_three_public_certified": success,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R8_ALL_PUBLIC_CERTIFIED=" + str(success), flush=True)
    print("PHASE173_R4_R8_REPORT=" + str(output), flush=True)
    return 0 if success else 2


if __name__ == "__main__":
    raise SystemExit(main())
