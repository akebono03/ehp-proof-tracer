"""Actual end-to-end R12-R20 proof audit."""
from __future__ import annotations
import json
from pathlib import Path
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r3_recursive_search import reconstruct_registered_goal, RegisteredGoalUnresolved
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from toda_rules import toda_eta_family_definition_statement
from proof import ProofRule

def main() -> None:
    bridge = build_shared_typed_bridge()
    refs = [x for x in bridge.proof_links if x.step is not None and isinstance(x.step.conclusion, TodaEtaFamilyGeneralDefinition)]
    goal = toda_eta_family_definition_statement(3)
    report = {"phase":"165 R12-R20", "general_fixed_link_count":len(refs), "eta3_specialization_certified":False,
              "eta3_proof_ancestor_cited":False, "generator_image_certified":False, "pi43_proof_certified":False, "full_pytest_run":False}
    if len(refs)==1:
        citing = next(iter(bridge.registry._assertions))
        try:
            result = reconstruct_registered_goal(goal, bridge, citing_assertion_id=citing,
                expansion_provider=shared_expansion_provider(bridge), lookup_mode="typed_reference")
            report["eta3_specialization_certified"] = (result.conclusion==goal and result.rule is ProofRule.INFERENCE)
            report["eta3_proof_ancestor_cited"] = any(parent is refs[0].step for parent in result.premises)
        except RegisteredGoalUnresolved as error:
            report["blocker"] = str(error)
    report["status"] = "ETA3_DEFINITION_CERTIFIED" if report["eta3_specialization_certified"] and report["eta3_proof_ancestor_cited"] else "UNRESOLVED"
    output = Path(__file__).resolve().parent / "audit_result.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] != "ETA3_DEFINITION_CERTIFIED":
        raise SystemExit("R12-R20 definition certification failed")

if __name__ == "__main__":
    main()
