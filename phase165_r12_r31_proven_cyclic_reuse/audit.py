"""Read-only operational audit of shared Web search and cited diagonal specialization."""
from __future__ import annotations
import json
from pathlib import Path
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r57_r20_general_specialization import expand_cited_general_specialization
from expression import GeneratorSymbol, HomotopyElement
from proof import Relation


def main() -> None:
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=3, k=1)
    if len(candidates) != 1:
        raise RuntimeError("expected unique registered pi4^3 goal")
    goal = candidates[0]
    eta2 = HomotopyElement("η₂", 2, source=3, target=2, generator=GeneratorSymbol("η", 2))
    cyclic = CyclicStructureStatement(TodaPrimaryGroup(3, 2), eta2, None)
    shared = shared_expansion_provider(bridge, proof_target=goal)
    cyclic_options = shared(cyclic)
    expected_relation = Relation(cyclic.group, FreeCyclicGroup(eta2))
    matched = [x for x in cyclic_options if x.subgoals == (expected_relation,)]
    diagonal = Relation(
        TodaPrimaryGroup(5, 5),
        FreeCyclicGroup(HomotopyElement("ι_5", 5, generator=GeneratorSymbol("ι", 5))),
    )
    cited = tuple(
        link.step.conclusion for link in bridge.proof_links
        if link.step is not None and getattr(link.step.rule, "name", "") == "GIVEN"
    )
    specialization = expand_cited_general_specialization(diagonal, cited)
    inverse = Relation(diagonal.rhs, diagonal.lhs)
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    output = {
        "phase": "165 R12-R31",
        "source_cyclic_candidates": len(matched),
        "source_relation_subgoal": repr(expected_relation),
        "diagonal_forward_specializations": len(specialization),
        "diagonal_inverse_goal": repr(inverse),
        "diagonal_inverse_expansion_count": len(shared(inverse)),
        "web_search_status": result.status.value,
        "web_search_complete": result.conclusion is not None and not result.open_goals,
        "open_goals": [repr(x) for x in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "full_pytest_run": False,
    }
    path = Path(__file__).resolve().parent / "audit_result.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print("Audit saved:", path)


if __name__ == "__main__":
    main()
