"""Report which real certified antecedents are ready; do not invent the others."""
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
from proof import ProofRule, Relation, RelationType


def main() -> None:
    source = TodaPrimaryGroup(3, 2)
    target = TodaPrimaryGroup(4, 3)
    mapping = TodaSuspensionMap(source, target)
    eta2 = HomotopyElement("η₂", dimension=2, source=3, target=2,
                           generator=GeneratorSymbol("η", 2))
    bridge = build_shared_typed_bridge()
    citation = next(iter(bridge.registry._assertions))
    proof_target = Relation(target, object(), relation_type=RelationType.EQUALITY)
    kernel = prove_kernel_in_screened_context(
        SuspensionKernelFreeCyclicStatement(
            mapping, FreeCyclicGroup(Multiple(coefficient=2, expression=eta2)),
        ), bridge, citing_assertion_id=citation, proof_target=proof_target,
    )
    surj = prove_surjectivity_in_screened_context(
        MapSurjective(mapping), bridge,
        citing_assertion_id=citation, proof_target=proof_target,
    )
    ready = kernel.status == "CERTIFIED" and surj.status == "CERTIFIED"
    conversions = False
    if ready:
        kp = derive_from_certified_proof(concrete_cyclic_kernel_as_multiple_rule(), kernel.proof)
        sp = derive_from_certified_proof(suspension_surjectivity_as_generic_surjectivity_rule(), surj.proof)
        conversions = kp.rule is ProofRule.INFERENCE and sp.rule is ProofRule.INFERENCE
    report = {
        "phase": "165 R12-R17",
        "kernel_source_status": kernel.status,
        "surjectivity_source_status": surj.status,
        "converted_antecedents_ready": conversions,
        "generic_quotient_chain_available": True,
        "homomorphism_presentation_proof": "NOT_VERIFIED",
        "infinite_cyclic_source_proof": "NOT_VERIFIED",
        "pi43_proof_certified": False,
        "status": "UNRESOLVED_PENDING_TWO_PROVEN_PREMISES" if conversions else "BLOCKED_ANTECEDENTS",
        "full_pytest_run": False,
    }
    path = Path(__file__).with_name("audit_result.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", path)
    if not conversions:
        raise SystemExit("Existing certified antecedents could not be reconstructed")


if __name__ == "__main__":
    main()
