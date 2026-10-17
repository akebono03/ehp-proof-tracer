"""Read-only scope gate for R12-R34-R4; does not claim runtime ancestry."""
from __future__ import annotations

import inspect
import json
from pathlib import Path

from phase165_r14_r16_foundational_suspension import instantiate_foundational_identity_suspension
from phase165_r14_r17_foundational_proofstep import derive_foundational_suspension_step
from toda_group_proof_narrative_contribution_renderer import (
    suppress_toda_group_proof_narrative_reference_internal_body,
    order_toda_group_proof_narrative_short_exact_support,
)


def audit() -> dict[str, object]:
    step = derive_foundational_suspension_step(
        instantiate_foundational_identity_suspension(1).statement
    )
    if step is None or step.foundational_reference is None:
        raise AssertionError("Foundational proof step has no source identity")
    suppress_source = inspect.getsource(suppress_toda_group_proof_narrative_reference_internal_body)
    ordering_source = inspect.getsource(order_toda_group_proof_narrative_short_exact_support)
    return {
        "phase": "165 R12-R34-R4 scope gate",
        "status": "EXISTING_SHARED_RENDERER_SCANNED_RUNTIME_PI43_ANCESTRY_UNVERIFIED",
        "generator_suspension": "E(ι₁)=ι₂",
        "foundational_reference": step.foundational_reference.key,
        "existing_reference_internal_suppression": "_toda_group_proof_narrative_reference_internal_step_ids" in suppress_source,
        "existing_exact_support_orderer": "_generic_short_exact_sequence_latex" in ordering_source,
        "existing_suppression_uses_step_identity": "id(" in suppress_source,
        "pi43_actual_tree_inspected": False,
        "pi32_boundary_certified": False,
        "renderer_modified": False,
        "full_pytest_run": False,
        "remaining": ["Inspect actual pi43 presentation proof graph", "Find generic prior-proof frontier", "Amend shared renderer with targeted tests", "Verify reference content and sequencing"],
    }


def main() -> None:
    result = audit()
    out = Path(__file__).resolve().parent / "audit_result.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("Audit saved:", out)


if __name__ == "__main__":
    main()
