"""Phase 166 R3-R: read-only audit of actual shared-search proof ancestry."""
from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from pathlib import Path

from proof import ProofRule, ProofStep, Relation
from phase165_r14_r6_generic_iso import GeneratorImage


def ancestors(step: ProofStep) -> tuple[ProofStep, ...]:
    """Traverse actual ProofStep premises, detecting cycles by object identity."""
    found: list[ProofStep] = []
    visited: set[int] = set()
    active: set[int] = set()

    def walk(current: ProofStep) -> None:
        identity = id(current)
        if identity in active:
            raise ValueError("cycle in ProofStep premises")
        if identity in visited:
            return
        active.add(identity)
        for premise in current.premises:
            if not isinstance(premise, ProofStep):
                raise TypeError("non-ProofStep premise in proof ancestry")
            walk(premise)
        active.remove(identity)
        visited.add(identity)
        found.append(current)

    walk(step)
    return tuple(found)


def audit_relation_steps(steps: tuple[ProofStep, ...], bridge: object) -> dict:
    """Check image-to-relation ancestry; do not treat a matching GIVEN as derived."""
    linked: dict[int, list[str]] = {}
    for link in bridge.proof_links:
        if link.step is not None:
            linked.setdefault(id(link.step), []).append(link.assertion_id)
    image_reference_steps: dict[int, list[str]] = {}
    for link in bridge.proof_links:
        if link.step is None or not isinstance(link.step.conclusion, GeneratorImage):
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        label = repr(reference)
        image_reference_steps.setdefault(id(link.step), []).append(label)

    results: list[dict] = []
    seen: set[int] = set()
    for root in steps:
        if not isinstance(root, ProofStep):
            raise TypeError("result.proven_steps must contain ProofStep instances")
        for step in ancestors(root):
            if id(step) in seen or not isinstance(step.conclusion, Relation):
                continue
            seen.add(id(step))
            lineage = ancestors(step)
            image_nodes = [node for node in lineage[:-1] if isinstance(node.conclusion, GeneratorImage)]
            origin_ids = [identifier for node in image_nodes for identifier in linked.get(id(node), [])]
            origin_labels = [label for node in image_nodes for label in image_reference_steps.get(id(node), [])]
            relation_image = bool(image_nodes)
            results.append({
                "relation": repr(step.conclusion),
                "rule": step.rule.name,
                "inference_rule": getattr(step.inference_rule, "name", None),
                "immediate_generator_image_premise": any(isinstance(p.conclusion, GeneratorImage) for p in step.premises),
                "generator_image_ancestor": relation_image,
                "linked_image_assertion_ids": origin_ids,
                "linked_image_references": origin_labels,
                "registered_proposition_5_1_ancestor": any("5.1" in label for label in origin_labels),
                "independent_given_relation": step.rule is ProofRule.GIVEN,
            })
    candidates = [r for r in results if r["generator_image_ancestor"]]
    return {
        "relations_found": len(results),
        "relations_with_image_ancestor": len(candidates),
        "relation_evidence": results,
        "derived_image_relation_chain_verified": bool(candidates) and all(
            r["rule"] == "INFERENCE"
            and r["immediate_generator_image_premise"]
            and r["registered_proposition_5_1_ancestor"]
            for r in candidates
        ),
    }


def main() -> int:
    from homotopy_groups import FreeCyclicGroup
    from hopf_facts import ETA_2
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal

    root = Path(__file__).resolve().parent
    bridge = build_shared_typed_bridge()
    result = search_shared_group_goal(n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge)
    findings = audit_relation_steps(tuple(result.proven_steps), bridge)
    report = {
        "phase": "166 R3-R",
        "mode": "read_only",
        "goal": "pi_3^2",
        "search_status": getattr(result.status, "name", repr(result.status)),
        "proven_steps": len(result.proven_steps),
        **findings,
        "full_pytest_run": False,
    }
    report_path = root / "r3r_audit.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "relation_evidence"}, ensure_ascii=False, indent=2))
    print("REPORT:", report_path)
    return 0 if report["derived_image_relation_chain_verified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
