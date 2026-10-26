"""R3Z final live narrative audit; no proof or source changes."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown


def examine():
    bridge = build_shared_typed_bridge()
    contexts = []
    proof = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if proof.status is not ProofSearchStatus.COMPLETE or len(contexts) != 1:
        raise AssertionError("pi5^3 is no longer complete")
    model = build_linked_proof_narrative_model(proof, contexts[0])
    markdown = render_model_backed_narrative_markdown(proof, model)
    sections = markdown.split("\n証明\n", 1)
    if len(sections) != 2:
        raise AssertionError("Narrative missing proof section")
    reference, body = sections
    general_in_reference = r"\pi_{n+1}^{n}" in reference
    general_in_body = r"\pi_{n+1}^{n}" in body
    concrete_in_body = r"\pi_{6}^{5}" in body
    if not general_in_reference or general_in_body or not concrete_in_body:
        raise AssertionError("General higher-eta clause not projected correctly")
    locators = tuple(c.reference.locator for c in model.citations)
    if not all(name in locators for name in ("Proposition 5.1", "(5.1)", "(5.3)")):
        raise AssertionError("Proof references changed")
    return {
        "phase": "169-R3Z", "proof_status": proof.status.value,
        "step_count": len(model.steps), "reference_count": len(model.citations),
        "general_eta_reference_only": True, "concrete_pi65_in_body": True,
        "references": locators, "full_pytest_run": False,
    }


def main():
    report = examine()
    output = Path(__file__).resolve().parent / "output" / "audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n",encoding="utf8")
    for key,value in report.items():
        print("R3Z_" + key.upper() + "=" + repr(value))
    print("R3Z_REPORT=" + str(output))


if __name__ == "__main__":
    main()
