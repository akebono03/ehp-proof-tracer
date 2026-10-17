"""Check the actual R12-R14/15/18/21 proofs, never substitute synthetic leaves."""
from __future__ import annotations

import json
from pathlib import Path

from expression import Multiple
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap, FiniteCyclicGroup
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r12_r14_kernel_closure import prove_kernel_in_screened_context
from phase165_r12_r15_toda51 import prove_surjectivity_in_screened_context
from phase165_r12_r16_bridges import (
    concrete_cyclic_kernel_as_multiple_rule, derive_from_certified_proof,
    suspension_surjectivity_as_generic_surjectivity_rule,
)
from phase165_r12_r18_evidence_reuse import extract_completed_root
from phase165_r12_r19_generator_connection import expand_generator_presentation
from phase165_r12_r21_eta_generator_chain import proof_has_cited_eta_general_ancestor
from phase165_r12_r22_quotient_closure import close_quotient_from_verified_steps, proof_ancestors
from phase165_r12_r2_quotient_rules import HomomorphismPresentationStatement
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal, RegisteredGoalUnresolved
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
)
from proof import ProofRule, Relation, RelationType
from toda_rules import toda_eta_family_definition_statement


def perform_audit() -> dict:
    source = TodaPrimaryGroup(3, 2)
    target = TodaPrimaryGroup(4, 3)
    mapping = TodaSuspensionMap(source, target)
    eta2 = toda_eta_family_definition_statement(2).element
    eta3 = toda_eta_family_definition_statement(3).element
    report = {
        "phase": "165 R12-R22", "pi32_root_proven": False,
        "kernel_proven": False, "surjectivity_proven": False,
        "presentation_proven": False, "source_structure_inferred": False,
        "first_isomorphism_derived": False, "final_relation_derived": False,
        "all_four_proof_ancestors": False, "eta_general_ancestor": False,
        "pi43_proof_certified": False, "status": "UNRESOLVED",
        "full_pytest_run": False,
    }
    try:
        bridge = build_shared_typed_bridge()
        citing = next(iter(bridge.registry._assertions))
        goal = Relation(target, FiniteCyclicGroup(2, eta3), relation_type=RelationType.EQUALITY)
        proof_target = Relation(target, object(), relation_type=RelationType.EQUALITY)

        pi32_goal = Relation(source, FreeCyclicGroup(eta2), relation_type=RelationType.EQUALITY)
        partial = search_shared_group_goal(n=2, k=1, group_structure=pi32_goal.rhs, bridge=bridge)
        pi32_evidence = extract_completed_root(partial, pi32_goal)
        if pi32_evidence.proof is None:
            report["blocker"] = "pi32: " + str(pi32_evidence.reason)
            return report
        source_root = pi32_evidence.proof
        report["pi32_root_proven"] = True

        kernel = prove_kernel_in_screened_context(
            SuspensionKernelFreeCyclicStatement(mapping, FreeCyclicGroup(Multiple(2, eta2))),
            bridge, citing_assertion_id=citing, proof_target=proof_target,
        )
        if kernel.proof is None or kernel.status != "CERTIFIED":
            report["blocker"] = "kernel: " + str(kernel.blocker)
            return report
        kstep = derive_from_certified_proof(concrete_cyclic_kernel_as_multiple_rule(), kernel.proof)
        report["kernel_proven"] = True

        onto = prove_surjectivity_in_screened_context(
            MapSurjective(mapping), bridge, citing_assertion_id=citing, proof_target=proof_target,
        )
        if onto.proof is None or onto.status != "CERTIFIED":
            report["blocker"] = "surjectivity: " + str(onto.blocker)
            return report
        sstep = derive_from_certified_proof(suspension_surjectivity_as_generic_surjectivity_rule(), onto.proof)
        report["surjectivity_proven"] = True

        pgoal = HomomorphismPresentationStatement(mapping, source, target, eta2, eta3)
        provider = shared_expansion_provider(bridge, extra_providers=(expand_generator_presentation,))
        pstep = reconstruct_registered_goal(
            pgoal, bridge, citing_assertion_id=citing,
            expansion_provider=provider, lookup_mode="typed_reference",
        )
        if pstep.conclusion != pgoal or pstep.rule is not ProofRule.INFERENCE:
            report["blocker"] = "presentation proof is not matching inference"
            return report
        report["eta_general_ancestor"] = proof_has_cited_eta_general_ancestor(pstep)
        if not report["eta_general_ancestor"]:
            report["blocker"] = "presentation missing cited eta definition"
            return report
        report["presentation_proven"] = True

        closure = close_quotient_from_verified_steps(pstep, kstep, sstep, source_root)
        if closure.proof is None:
            report["blocker"] = "quotient: " + str(closure.blocker)
            return report
        report["source_structure_inferred"] = True
        report["first_isomorphism_derived"] = len(closure.intermediate_steps) >= 1
        report["all_four_proof_ancestors"] = proof_ancestors(
            closure.proof, (pstep, kernel.proof, onto.proof, source_root)
        )
        report["final_relation_derived"] = (
            closure.proof.conclusion == goal and closure.proof.rule is ProofRule.INFERENCE
        )
        report["pi43_proof_certified"] = (
            report["all_four_proof_ancestors"] and report["final_relation_derived"]
        )
        report["status"] = "PI43_QUOTIENT_PROOF_CERTIFIED" if report["pi43_proof_certified"] else "FINAL_ROOT_OR_ANCESTRY_MISMATCH"
    except (RegisteredGoalUnresolved, ValueError, TypeError) as exc:
        report["blocker"] = type(exc).__name__ + ": " + str(exc)
    return report


def main() -> None:
    result = perform_audit()
    path = Path(__file__).with_name("audit_result.json")
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("Audit saved:", path)
    if not result["pi43_proof_certified"]:
        raise SystemExit("R12-R22 remains unresolved; no proof was certified")


if __name__ == "__main__":
    main()
