"""R3-36C read-only comparison of USED GIVEN and registered provenance."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from proof import ProofRule


def compact(value: object) -> dict:
    return {"type": type(value).__name__, "repr": repr(value)[:2500]}


def inspect() -> dict:
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=4, k=1, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    out = []
    for index, step in enumerate(result.proven_steps):
        if step.rule is not ProofRule.GIVEN:
            continue
        inference_ref = None
        if step.inference_rule is not None:
            inference_ref = step.inference_rule.literature_reference
        locator = None if inference_ref is None else (inference_ref.locator or inference_ref.label)
        matches = []
        for link in bridge.proof_links:
            if link.step is None:
                continue
            relation = (
                "exact" if link.step == step else
                "same_conclusion" if link.step.conclusion == step.conclusion else
                "different"
            )
            if relation == "different":
                continue
            assertion = bridge.registry.assertion(link.assertion_id)
            ref = bridge.registry.reference(assertion.reference_id)
            matches.append({
                "kind": relation,
                "assertion_id": assertion.assertion_id,
                "origin": assertion.origin.value,
                "dependencies": list(assertion.dependencies),
                "locator": ref.locator,
                "statement": compact(assertion.content),
                "linked_rule": link.step.rule.value,
                "link_matches_conclusion": link.step.conclusion == step.conclusion,
            })
        candidates = []
        for assertion in bridge.registry._assertions.values():
            if assertion.content != step.conclusion:
                continue
            ref = bridge.registry.reference(assertion.reference_id)
            candidates.append({
                "assertion_id": assertion.assertion_id,
                "origin": assertion.origin.value,
                "dependencies": list(assertion.dependencies),
                "locator": ref.locator,
                "publication_position": ref.publication_position,
                "component_position": assertion.component_position,
            })
        out.append({
            "step_index": index,
            "citation_numbers": list(model.step_citation_numbers[index]),
            "locator": locator,
            "conclusion": compact(step.conclusion),
            "links_same_step_or_conclusion": matches,
            "registered_exact_content": candidates,
        })
    return {
        "mode": "AUDIT_ONLY",
        "status": result.status.value,
        "target": "pi_5^4",
        "given_steps": out,
        "bridge_links": len(bridge.proof_links),
        "all_registry_assertions": len(bridge.registry._assertions),
    }


def main() -> None:
    report = inspect()
    path = Path(__file__).resolve().parent / "output" / "audit.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("AUDIT_ONLY: no repository files modified")
    for step in report["given_steps"]:
        print(f'STEP {step["step_index"]}: {step["locator"]}, '
              f'exact-content-assertions={len(step["registered_exact_content"])}, '
              f'matching-links={len(step["links_same_step_or_conclusion"])}')
        for a in step["registered_exact_content"]:
            print(f'  {a["origin"]}: {a["assertion_id"]} '
                  f'dependencies={a["dependencies"]}')
    print("REPORT:", path)


if __name__ == "__main__":
    main()
