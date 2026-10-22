"""Phase 168 R2-7(2): inspect the live registry without proof replay."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from proof import Relation
from toda_literature_statement_boundary import TodaFixedStatementComponent
from unified_statement_registry import AssertionOrigin

TARGETS = {
    "Proposition 5.3": "higher_eta_squared_group_relation",
    "Proposition 5.6": "higher_nu_group_relation",
}


def classify(value: object) -> str:
    if isinstance(value, TodaFixedStatementComponent):
        return "METADATA_ONLY"
    if isinstance(value, dict):
        return "SOURCE_ONLY"
    return "MATHEMATICAL_TYPED"


def audit(bridge=None) -> dict:
    if bridge is None:
        bridge = build_shared_typed_bridge()
    items = []
    for locator, target_key in TARGETS.items():
        relevant = []
        for assertion in bridge.registry._assertions.values():
            reference = bridge.registry.reference(assertion.reference_id)
            if reference.locator != locator:
                continue
            relevant.append({
                "assertion_id": assertion.assertion_id,
                "origin": assertion.origin.name,
                "content_type": type(assertion.content).__name__,
                "category": classify(assertion.content),
                "publication_position": reference.publication_position,
                "component_position": assertion.component_position,
            })
        targets = [a for a in bridge.registry._assertions.values()
                   if a.assertion_id.endswith(":" + target_key)
                   and bridge.registry.reference(a.reference_id).locator == locator
                   and a.origin is AssertionOrigin.FIXED_STATEMENT]
        if len(targets) != 1:
            raise ValueError(f"expected unique publication target: {locator}: {len(targets)}")
        target = targets[0]
        screened = screen_shared_proof_context(
            bridge, goal=target.content, citing_assertion_id=target.assertion_id,
            explicit_publication_target=True,
        )
        generated = []
        for link in screened.proof_links:
            claim = bridge.registry.assertion(link.assertion_id)
            ref = bridge.registry.reference(claim.reference_id)
            generated.append({
                "assertion_id": claim.assertion_id,
                "locator": ref.locator,
                "content_type": type(claim.content).__name__,
                "category": classify(claim.content),
                "is_target_content": claim.content == target.content,
            })
        items.append({
            "locator": locator,
            "registered": relevant,
            "registered_categories": dict(Counter(row["category"] for row in relevant)),
            "generated_given_count": len(generated),
            "generated_given_categories": dict(Counter(row["category"] for row in generated)),
            "same_proposition_generated": [row for row in generated if row["locator"] == locator],
            "self_conclusion_generated": any(row["is_target_content"] for row in generated),
            "mathematical_relations_registered": [row for row in relevant if row["content_type"] == Relation.__name__],
        })
    return {"phase": "168-R2-7-2", "production_code_modified": False, "targets": items}


def main() -> None:
    result = audit()
    target = Path(__file__).resolve().parent / "output"
    target.mkdir(exist_ok=True)
    outfile = target / "registry_source_audit.json"
    outfile.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for item in result["targets"]:
        print(json.dumps({key: value for key, value in item.items() if key not in ("registered", "same_proposition_generated", "mathematical_relations_registered")}, ensure_ascii=False, indent=2))
    print("JSON:", outfile)


if __name__ == "__main__":
    main()
