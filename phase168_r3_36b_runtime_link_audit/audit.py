"""R3-36B runtime audit only. No repository writes."""
from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model


def describe(value: object) -> dict:
    return {
        "type": type(value).__name__,
        "repr": repr(value)[:3000],
    }


def inspect() -> dict:
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=4, k=1, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    steps = model.steps
    linked = []
    for i, step in enumerate(steps):
        matches = []
        for link in bridge.proof_links:
            if link.step is None or link.step != step:
                continue
            assertion = bridge.registry.assertion(link.assertion_id)
            reference = bridge.registry.reference(assertion.reference_id)
            matches.append({
                "assertion_id": assertion.assertion_id,
                "reference_id": assertion.reference_id,
                "locator": reference.locator,
                "origin": assertion.origin.value,
                "dependencies": list(assertion.dependencies),
                "registered_content": describe(assertion.content),
                "link_same_object": link.step is step,
            })
        ref_numbers = list(model.step_citation_numbers[i])
        linked.append({
            "step_index": i,
            "rule": step.rule.value,
            "conclusion": describe(step.conclusion),
            "inference_reference": (
                str(step.inference_rule.literature_reference)
                if step.inference_rule is not None
                and step.inference_rule.literature_reference is not None
                else None
            ),
            "citation_numbers": ref_numbers,
            "matches": matches,
        })
    citations = []
    for citation in model.citations:
        entries = []
        for assertion_id in citation.assertion_ids:
            assertion = bridge.registry.assertion(assertion_id)
            entries.append({
                "assertion_id": assertion_id,
                "reference_id": assertion.reference_id,
                "origin": assertion.origin.value,
                "dependencies": list(assertion.dependencies),
                "content": describe(assertion.content),
            })
        citations.append({
            "number": citation.number,
            "locator": citation.reference.locator or citation.reference.label,
            "step_indices": list(citation.step_indices),
            "assertion_ids": list(citation.assertion_ids),
            "reference_ids": list(citation.reference_ids),
            "assertions": entries,
            "inference_only": not citation.assertion_ids,
        })
    return {
        "mode": "AUDIT_ONLY",
        "group": "pi_5^4",
        "status": result.status.value,
        "step_count": len(steps),
        "bridge_link_count": len(bridge.proof_links),
        "citations": citations,
        "steps": linked,
        "notes": [
            "A reference heading alone does not certify registered statement content.",
            "ProofStep comparison uses value equality; no name-based matching.",
            "The report is observational and does not modify repository code.",
        ],
    }


def main() -> None:
    report = inspect()
    output = Path(__file__).resolve().parent / "output" / "audit.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("AUDIT_ONLY: no repository files modified")
    print("STATUS:", report["status"], "STEPS:", report["step_count"])
    for c in report["citations"]:
        print(f'[R{c["number"]}] {c["locator"]}: '
              f'assertions={len(c["assertion_ids"])} '
              f'inference_only={c["inference_only"]} '
              f'steps={c["step_indices"]}')
    print("REPORT:", output)


if __name__ == "__main__":
    main()
