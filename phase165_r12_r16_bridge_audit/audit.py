"""R12-R16: check two actual antecedent derivations without inventing other facts."""
from __future__ import annotations

import json
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r12_r14_kernel_closure import prove_kernel_in_screened_context
from phase165_r12_r15_toda51 import prove_surjectivity_in_screened_context
from phase165_r12_r16_bridges import (
    concrete_cyclic_kernel_as_multiple_rule,
    derive_from_certified_proof,
    suspension_surjectivity_as_generic_surjectivity_rule,
)
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from proof import Relation, RelationType, ProofRule


def main() -> None:
    source = TodaPrimaryGroup(3, 2)
    target = TodaPrimaryGroup(4, 3)
    suspension = TodaSuspensionMap(source, target)
    eta2 = HomotopyElement("η₂", dimension=2, source=3, target=2,
                           generator=GeneratorSymbol("η", 2))
    bridge = build_shared_typed_bridge()
    citation = next(iter(bridge.registry._assertions))
    proof_target = Relation(target, object(), relation_type=RelationType.EQUALITY)
    kernel = prove_kernel_in_screened_context(
        SuspensionKernelFreeCyclicStatement(
            suspension, FreeCyclicGroup(Multiple(coefficient=2, expression=eta2)),
        ), bridge, citing_assertion_id=citation, proof_target=proof_target,
    )
    surj = prove_surjectivity_in_screened_context(
        MapSurjective(suspension), bridge,
        citing_assertion_id=citation, proof_target=proof_target,
    )
    output = {
        "phase": "165 R12-R16",
        "kernel_source_status": kernel.status,
        "surjectivity_source_status": surj.status,
        "kernel_conversion": "NOT_ATTEMPTED",
        "surjectivity_conversion": "NOT_ATTEMPTED",
        "pi43_proof_certified": False,
        "remaining_premises": [
            "certified homomorphism presentation with generator image",
            "certified infinite cyclic structure of source group",
            "first-isomorphism and quotient inference chain",
            "final group relation proof and provenance",
        ],
        "full_pytest_run": False,
    }
    if kernel.status == "CERTIFIED" and kernel.proof is not None:
        step = derive_from_certified_proof(concrete_cyclic_kernel_as_multiple_rule(), kernel.proof)
        output["kernel_conversion"] = "INFERENCE" if step.rule is ProofRule.INFERENCE and step.premises == (kernel.proof,) else "INVALID"
        output["kernel_multiple"] = getattr(step.conclusion, "multiple", None)
    if surj.status == "CERTIFIED" and surj.proof is not None:
        step = derive_from_certified_proof(suspension_surjectivity_as_generic_surjectivity_rule(), surj.proof)
        output["surjectivity_conversion"] = "INFERENCE" if step.rule is ProofRule.INFERENCE and step.premises == (surj.proof,) else "INVALID"
    output["status"] = "BRIDGE_READY_PENDING_PROOF_PREMISES" if output["kernel_conversion"] == output["surjectivity_conversion"] == "INFERENCE" else "BLOCKED"
    destination = Path(__file__).resolve().parent / "audit_result.json"
    destination.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if output["status"] == "BLOCKED":
        raise SystemExit("R12-R16 antecedent proof bridges are blocked; audit_result.json saved")


if __name__ == "__main__":
    main()
