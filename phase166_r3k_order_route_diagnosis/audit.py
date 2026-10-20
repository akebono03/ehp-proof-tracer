"""Read-only Phase 166 R3-K registry-to-search order diagnostics."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_prop51_claim_order import pi4_3_goal
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from proof import ProofRule


def inspect() -> dict:
    bridge = build_shared_typed_bridge()
    registry = bridge.registry
    refs = registry._references
    assertions = registry._assertions
    all_links = {link.assertion_id for link in bridge.proof_links}
    targets = {}
    for n, k in ((2, 1), (3, 1), (4, 1)):
        candidates = registered_group_goal_candidates(bridge, n=n, k=k)
        matches = [a for a in assertions.values() if a.content in candidates and a.component_position is not None]
        targets[f"pi_{n+k}^{n}"] = {
            "candidate_count": len(candidates),
            "matches": [{
                "assertion_id": a.assertion_id,
                "reference_id": a.reference_id,
                "component_position": a.component_position,
                "reference_publication_position": refs[a.reference_id].publication_position,
                "has_preexisting_link": a.assertion_id in all_links,
            } for a in matches],
        }
    target = next((a for a in assertions.values() if a.content == pi4_3_goal() and a.component_position == 4), None)
    selected = {}
    if target is not None:
        screened = screen_shared_proof_context(
            bridge, goal=target.content, citing_assertion_id=target.assertion_id,
            explicit_publication_target=True,
        )
        ids = {link.assertion_id for link in screened.proof_links}
        selected = {
            "target": target.assertion_id,
            "selected_count": len(ids),
            "selected_references": sorted({registry.reference(assertions[i].reference_id).locator for i in ids}),
            "selected_prop51_components": [
                {"assertion_id": a.assertion_id, "position": a.component_position}
                for a in assertions.values()
                if a.assertion_id in ids and refs[a.reference_id].locator == "Proposition 5.1"
            ],
            "all_selected_are_given": all(link.step is not None and link.step.rule is ProofRule.GIVEN for link in screened.proof_links),
        }
    refs_summary = []
    for ref in refs.values():
        if ref.locator in {"(5.1)", "(4.5)", "Proposition 5.1"}:
            members = [a for a in assertions.values() if a.reference_id == ref.reference_id]
            refs_summary.append({
                "reference_id": ref.reference_id,
                "locator": ref.locator,
                "publication_position": ref.publication_position,
                "assertions": [{
                    "assertion_id": a.assertion_id,
                    "component_position": a.component_position,
                    "type": type(a.content).__name__,
                    "has_preexisting_link": a.assertion_id in all_links,
                } for a in members],
            })
    return {
        "phase": "166-R3K",
        "read_only": True,
        "full_pytest_run": False,
        "targets": targets,
        "references": refs_summary,
        "pi43_explicit_order_selection": selected,
    }


if __name__ == "__main__":
    result = inspect()
    path = Path.cwd() / "phase166_r3k_order_route_diagnosis_results.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    print("AUDIT SAVED:", path)
