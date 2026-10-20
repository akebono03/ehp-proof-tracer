"""Phase 166 R3: read-only inspection of the production registry's order fields."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from phase165_r9_production_wiring import discover_goal_search_inputs
from unified_statement_registry import AssertionOrigin


def collect() -> dict:
    inputs = discover_goal_search_inputs()
    bridge = inputs.bridge
    rows = []
    for assertion in bridge.registry._assertions.values():
        reference = bridge.registry.reference(assertion.reference_id)
        locator = reference.locator
        if locator not in ("(5.1)", "Proposition 5.1", "Proposition 4.2", "Proposition 4.2 (4.4)") and not any(
            phrase in assertion.assertion_id.lower() for phrase in ("pi3_2", "pi_3_2", "pi2_1", "pi_2_1", "eta2_hopf")
        ):
            continue
        linked = tuple(link for link in bridge.proof_links if link.assertion_id == assertion.assertion_id)
        rows.append({
            "assertion_id": assertion.assertion_id,
            "origin": assertion.origin.value,
            "reference_id": assertion.reference_id,
            "locator": locator,
            "source_id": reference.source_id,
            "publication_position": reference.publication_position,
            "component_position": assertion.component_position,
            "available_after_position": assertion.available_after_position,
            "content_type": type(assertion.content).__name__,
            "proof_link_count": len(linked),
            "proof_step_types": [type(link.step).__name__ if link.step is not None else None for link in linked],
        })
    return {
        "audit": "Phase 166 R3 read-only ordering inventory",
        "all_assertions": len(bridge.registry._assertions),
        "all_proof_links": len(bridge.proof_links),
        "origin_counts": dict(Counter(a.origin.value for a in bridge.registry._assertions.values())),
        "all_fixed_with_publication_position": sum(
            a.origin is AssertionOrigin.FIXED_STATEMENT
            and bridge.registry.reference(a.reference_id).publication_position is not None
            for a in bridge.registry._assertions.values()
        ),
        "all_fixed_with_available_after_position": sum(
            a.origin is AssertionOrigin.FIXED_STATEMENT and a.available_after_position is not None
            for a in bridge.registry._assertions.values()
        ),
        "selected_assertions": rows,
        "note": "Observation only; no ordering positions are inferred and no citation eligibility is granted.",
    }


def main() -> None:
    result = collect()
    output = Path(__file__).resolve().parent / "results" / "order_inventory.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "all_assertions": result["all_assertions"],
        "all_proof_links": result["all_proof_links"],
        "fixed_with_publication_position": result["all_fixed_with_publication_position"],
        "fixed_with_available_after_position": result["all_fixed_with_available_after_position"],
        "selected_count": len(result["selected_assertions"]),
        "report": str(output),
        "production_modified": False,
        "full_pytest_run": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
