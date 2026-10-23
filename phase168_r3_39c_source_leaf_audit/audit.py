"""Read-only diagnostic of (5.1) direct GIVEN leaves and universal sources."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
from phase165_r57_r20_general_specialization import specialize_typed_statement
from proof import ProofRule


def audit(root: Path) -> dict:
    tex = root / "phase165_r14_r39_toda51.tex"
    direct = build_adopted_typed_reference_registry(tex)
    shared = build_shared_typed_bridge()
    result = {"direct": [], "general": [], "unmatched_direct": [], "notes": []}
    candidates = []
    for assertion in shared.registry._assertions.values():
        ref = shared.registry.reference(assertion.reference_id)
        if ref.locator != "(5.1)":
            continue
        linked = any(link.assertion_id == assertion.assertion_id and link.step is not None
                     and link.step.rule is ProofRule.GIVEN for link in shared.proof_links)
        candidates.append((assertion, linked))
    direct_contents = tuple(link.step.conclusion for link in direct.proof_links if link.step is not None)
    for assertion, linked in candidates:
        item = {"assertion_id": assertion.assertion_id,
                "type": type(assertion.content).__name__,
                "linked_given": linked,
                "direct_legacy": any(assertion.content == content for content in direct_contents),
                "statement": repr(assertion.content)}
        if item["direct_legacy"]:
            item["symbolic_source_matches"] = [
                other.assertion_id for other, other_linked in candidates
                if other_linked and other.assertion_id != assertion.assertion_id
                and specialize_typed_statement(other.content, assertion.content) is not None
            ]
            result["direct"].append(item)
            if not item["symbolic_source_matches"]:
                result["unmatched_direct"].append(item["assertion_id"])
        else:
            result["general"].append(item)
    result["notes"] = [
        "A direct source leaf with no symbolic_source_matches must not be removed.",
        "Symbolic matching alone does not prove that a replacement proof search succeeds.",
        "Source publication ordering and actual Proof Tree ancestry must be retained.",
        "No repository files were modified by this audit.",
    ]
    return result


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    report = audit(root)
    out = Path(__file__).resolve().parent / "output"
    out.mkdir(exist_ok=True)
    destination = out / "source_leaf_audit.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("DIRECT_SOURCE_LEAVES", len(report["direct"]))
    print("REGISTERED_OTHER_51_ASSERTIONS", len(report["general"]))
    print("UNMATCHED_DIRECT", len(report["unmatched_direct"]))
    for item in report["direct"]:
        print("DIRECT", item["assertion_id"], "MATCHES", item["symbolic_source_matches"])
    print("REPORT", destination)
    print("AUDIT_ONLY: no repository code modified")


if __name__ == "__main__":
    main()
