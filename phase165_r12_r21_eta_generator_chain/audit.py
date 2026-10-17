"""Read actual canonical backwards proof steps; never certify missing ancestry."""
from __future__ import annotations
import json
from pathlib import Path
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r2_quotient_rules import HomomorphismPresentationStatement
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import reconstruct_registered_goal, RegisteredGoalUnresolved
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r12_r21_eta_generator_chain import proof_has_cited_eta_general_ancestor
from phase165_r12_r19_generator_connection import expand_generator_presentation
from toda_rules import toda_eta_family_definition_statement
from proof import ProofRule


def main() -> None:
    a = toda_eta_family_definition_statement(2).element
    b = toda_eta_family_definition_statement(3).element
    mapping = TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3))
    goals = (GeneratorSuspension(mapping, a, b), GeneratorImage(mapping, a, b),
             HomomorphismPresentationStatement(mapping, mapping.source_group, mapping.target_group, a, b))
    bridge = build_shared_typed_bridge()
    citing = next(iter(bridge.registry._assertions))
    def extra(goal):
        return expand_generator_presentation(goal)
    provider = shared_expansion_provider(bridge, extra_providers=(extra,))
    result = {"phase": "165 R12-R21", "generator_suspension_certified": False,
              "generator_image_certified": False, "homomorphism_presentation_certified": False,
              "eta_general_ancestor_for_all": False, "pi43_proof_certified": False,
              "full_pytest_run": False, "status": "UNRESOLVED"}
    proof_results = []
    for goal in goals:
        try:
            step = reconstruct_registered_goal(goal, bridge, citing_assertion_id=citing,
                expansion_provider=provider, lookup_mode="typed_reference")
            accepted = (step.conclusion == goal and step.rule is ProofRule.INFERENCE
                        and proof_has_cited_eta_general_ancestor(step))
            proof_results.append(accepted)
            if not accepted:
                result["blocker"] = "invalid root or missing cited ancestor: " + type(goal).__name__
                break
        except (RegisteredGoalUnresolved, ValueError) as exc:
            result["blocker"] = type(goal).__name__ + ": " + str(exc)
            proof_results.append(False)
            break
    keys = ("generator_suspension_certified", "generator_image_certified", "homomorphism_presentation_certified")
    for key, value in zip(keys, proof_results):
        result[key] = value
    result["eta_general_ancestor_for_all"] = len(proof_results) == 3 and all(proof_results)
    if result["eta_general_ancestor_for_all"]:
        result["status"] = "GENERATOR_PRESENTATION_CERTIFIED_QUOTIENT_PENDING"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    (Path(__file__).resolve().parent / "audit_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    if result["status"] != "GENERATOR_PRESENTATION_CERTIFIED_QUOTIENT_PENDING":
        raise SystemExit("R12-R21 certification unresolved; inspect audit_result.json")


if __name__ == "__main__":
    main()
