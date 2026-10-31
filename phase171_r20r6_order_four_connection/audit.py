"""Read-only audit of the newly connected public order-four proposal."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from phase165_r52_r9_shared_math import shared_expansion_provider
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r7_nonzero_nu_order.audit import build_nonzero_nu_order_proof
from phase164_r8_proofstep_factory import derive_inference_proof_step
from proof import ProofRule, ProofStep, find_inference_matches_for_rule

PACKAGE = Path(__file__).resolve().parent


def analyze_step(name: str, proof: ProofStep, provider) -> dict:
    """Compare actual R4-R7 typed premises to independent public proposals."""
    if proof.rule is not ProofRule.INFERENCE or proof.inference_rule is None:
        raise RuntimeError("expected real inference for " + name)
    proposals = provider(proof.conclusion)
    if not isinstance(proposals, tuple):
        raise TypeError("public expansion provider did not return a tuple")
    expected = tuple(parent.conclusion for parent in proof.premises)
    certified = 0
    exact = 0
    for option in proposals:
        if option.rule.name != proof.inference_rule.name or option.subgoals != expected:
            continue
        exact += 1
        matches = find_inference_matches_for_rule(option.rule, proof.premises)
        if any(
            len(match.premises) == len(proof.premises)
            and all(left is right for left, right in zip(match.premises, proof.premises))
            and derive_inference_proof_step(match).conclusion == proof.conclusion
            for match in matches
        ):
            certified += 1
    return {
        "name": name,
        "conclusion_type": type(proof.conclusion).__name__,
        "expected_rule": proof.inference_rule.name,
        "proposals": len(proposals),
        "exact_proposals": exact,
        "certified_proposals": certified,
        "classification": "CERTIFIED_PUBLIC_PROPOSAL_PRESENT" if certified
            else "MISSING_MATCHING_PUBLIC_PROPOSAL" if not exact
            else "PUBLIC_RULE_DOES_NOT_CERTIFY_REAL_PARENTS",
    }


def audit() -> dict:
    screened, target, _ = _screened_context()
    nonzero, order_four, _, previous = build_nonzero_nu_order_proof()
    if previous["new_given_added"] != 0:
        raise RuntimeError("independent proof contains new GIVEN")
    provider = shared_expansion_provider(screened, proof_target=target)
    items = [
        analyze_step("nu_order_four", order_four, provider),
        analyze_step("double_nonzero", nonzero, provider),
        analyze_step("injected_eta_image_nonzero", nonzero.premises[1], provider),
        analyze_step("typed_double_equality", nonzero.premises[0], provider),
        analyze_step("middle_cardinality_four", order_four.premises[0], provider),
    ]
    if items[0]["classification"] != "CERTIFIED_PUBLIC_PROPOSAL_PRESENT":
        raise RuntimeError("public order-four proposal did not certify original parents")
    report = {
        "phase": "171-R20R6",
        "mode": "ORDER_FOUR_PUBLIC_CONNECTION_ONLY",
        "new_given_added": 0,
        "completed_proofs_imported_into_search": False,
        "public_complete_asserted": False,
        "steps": items,
        "missing_routes": [x["name"] for x in items if x["classification"] != "CERTIFIED_PUBLIC_PROPOSAL_PRESENT"],
        "full_pytest": False,
    }
    folder = PACKAGE / "output" / datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    folder.mkdir(parents=True, exist_ok=False)
    location = folder / "audit.json"
    location.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in items:
        print("PHASE171_R20R6_" + item["name"].upper() + "=" + item["classification"], flush=True)
    print("PHASE171_R20R6_MISSING_ROUTES=" + ",".join(report["missing_routes"]), flush=True)
    print("PHASE171_R20R6_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20R6_REPORT=" + str(location), flush=True)
    print("PHASE171_R20R6_RESULT=PASS_ORDER_FOUR_CONNECTED", flush=True)
    return report


def main() -> None:
    audit()


if __name__ == "__main__":
    main()
