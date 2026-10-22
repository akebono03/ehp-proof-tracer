"""Read-only audit of typed input availability for Proposition 5.3/5.6."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r9_production_wiring import discover_goal_search_inputs
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from toda_literature_statement_boundary import TodaFixedStatementComponent
from unified_statement_registry import AssertionOrigin

TARGETS = {
    "Proposition 5.3": (
        "pi4_2_group_relation", "pi5_3_group_relation",
        "pi6_4_group_relation", "higher_eta_squared_group_relation",
    ),
    "Proposition 5.6": (
        "pi5_2_group_relation", "pi6_3_group_relation",
        "pi7_4_group_relation", "pi8_5_group_relation", "higher_nu_group_relation",
    ),
}


def category(assertion):
    if assertion.origin is AssertionOrigin.SOURCE_ARCHIVE:
        return "SOURCE_ARCHIVE"
    if isinstance(assertion.content, TodaFixedStatementComponent):
        return "METADATA_ONLY"
    return "MATHEMATICAL_TYPED"


def inspect_bridge(bridge):
    entries = {}
    for assertion in bridge.registry._assertions.values():
        ref = bridge.registry.reference(assertion.reference_id)
        locator = getattr(ref, "locator", None)
        if locator not in TARGETS:
            continue
        content = assertion.content
        key = getattr(content, "component_key", None)
        if key is None and assertion.assertion_id.startswith("shared:0:boundary:"):
            key = assertion.assertion_id.split(":")[-1]
        entries.setdefault(locator, []).append({
            "assertion_id": assertion.assertion_id,
            "key": key,
            "category": category(assertion),
            "content_type": type(content).__name__,
            "publication_position": ref.publication_position,
            "component_position": assertion.component_position,
        })
    return entries


def audit():
    base = discover_goal_search_inputs().bridge
    shared = build_shared_typed_bridge()
    base_rows = inspect_bridge(base)
    shared_rows = inspect_bridge(shared)
    results = {}
    for locator, keys in TARGETS.items():
        rows = shared_rows.get(locator, [])
        typed = [r for r in rows if r["category"] == "MATHEMATICAL_TYPED"]
        metadata = [r for r in rows if r["category"] == "METADATA_ONLY"]
        results[locator] = {
            "expected_component_keys": list(keys),
            "base_boundary_count": len([r for r in base_rows.get(locator, []) if r["category"] == "METADATA_ONLY"]),
            "shared_metadata_count": len(metadata),
            "shared_math_typed_count": len(typed),
            "typed_component_keys": [r["key"] for r in typed],
            "unregistered_component_keys": [key for key in keys if key not in [r["key"] for r in typed]],
            "entries": rows,
        }
    return {
        "audit": "phase168-r2-7-3-preflight",
        "production_code_modified": False,
        "registrar_prop53_requires": "exactly eight LiteratureComponentInput across Proposition 5.1 and 5.3",
        "registrar_prop56_requires": "exactly five LiteratureAssertionInput",
        "legacy_proof_conclusions_reused": False,
        "targets": results,
    }


def main():
    result = audit()
    out = Path(__file__).resolve().parent / "output" / "registration_preflight.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for locator, row in result["targets"].items():
        print(locator, "metadata", row["shared_metadata_count"], "typed", row["shared_math_typed_count"], "missing", len(row["unregistered_component_keys"]))
    print("JSON:", out)


if __name__ == "__main__":
    main()
