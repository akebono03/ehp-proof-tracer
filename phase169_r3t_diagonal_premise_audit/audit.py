"""Read-only audit: cited Toda (5.1) diagonal evidence for Delta injectivity."""
from __future__ import annotations

import json
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r5_ehp_connection import expand_cited_ehp_terminal_goal
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r57_r20_general_specialization import (
    expand_cited_general_specialization,
    specialize_typed_statement,
)
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule, Relation, RelationType
from toda_rules import TodaDeltaInjectiveStatement

ROOT = Path(__file__).resolve().parent


def diagonal_pi55_goal() -> Relation:
    """Create a GOAL, not a source fact; Toda (5.1) must prove this."""
    return Relation(
        TodaPrimaryGroup(5, 5),
        FreeCyclicGroup(
            HomotopyElement(
                name="ι_5",
                dimension=5,
                generator=GeneratorSymbol(family="ι", index=5),
            )
        ),
        relation_type=RelationType.EQUALITY,
    )


def audit() -> dict:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(goals) != 1:
        raise AssertionError("Expected one registered pi5^3 group goal")
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if not citing:
        raise AssertionError("Missing pi5^3 citing assertion")
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise AssertionError("Canonical screened context not available")
    screened = contexts[0]
    from unified_statement_registry import AssertionOrigin
    given_links = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
            is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion
            == screened.registry.assertion(link.assertion_id).content
    )
    available = tuple(link.step.conclusion for link in given_links)
    diagonal = diagonal_pi55_goal()
    matches = tuple(
        (link.assertion_id, link.step.conclusion)
        for link in given_links
        if specialize_typed_statement(link.step.conclusion, diagonal) is not None
    )
    proposals = expand_cited_general_specialization(diagonal, available)
    delta = TodaDeltaInjectiveStatement(
        map=TodaDeltaMap(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2)),
    )
    old_proposals = expand_cited_ehp_terminal_goal(delta, available)
    old_delta_prerequisites = [
        [type(subgoal).__name__ for subgoal in proposal.subgoals]
        for proposal in old_proposals
    ]
    derived_status = "not-attempted"
    derived_premises = []
    derived_source_locators = []
    if matches:
        provider = shared_expansion_provider(screened, proof_target=target)
        try:
            proof = reconstruct_registered_goal(
                diagonal, screened, citing, provider,
                lookup_mode="typed_reference_publication",
            )
        except Exception as exc:
            derived_status = "unresolved: " + type(exc).__name__ + ": " + str(exc)
        else:
            derived_status = "inference" if proof.rule is ProofRule.INFERENCE else proof.rule.value
            derived_premises = [type(p.conclusion).__name__ for p in proof.premises]
            derived_source_locators = sorted({
                p.inference_rule.literature_reference.locator
                for p in proof.premises
                if p.inference_rule is not None
                and p.inference_rule.literature_reference is not None
            })
    record = {
        "phase": "169-R3T",
        "mode": "AUDIT_ONLY",
        "target": "pi5^3",
        "proof_status": result.status.value,
        "screened_given_count": len(given_links),
        "diagonal_goal": repr(diagonal),
        "cited_diagonal_schema_matches": len(matches),
        "matched_citing_assertions": [identifier for identifier, _ in matches],
        "general_specialization_options": len(proposals),
        "diagonal_proof_result": derived_status,
        "diagonal_proof_premise_types": derived_premises,
        "diagonal_proof_source_locators": derived_source_locators,
        "current_delta_injectivity_subgoal_types": old_delta_prerequisites,
        "old_delta_contains_pi55_premise": any(
            any(isinstance(subgoal, Relation) and subgoal == diagonal
                for subgoal in option.subgoals)
            for option in old_proposals
        ),
        "production_files_modified": False,
        "full_suite_run": False,
    }
    output = ROOT / "output" / "r3t_diagonal_premise.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for key in (
        "proof_status", "screened_given_count", "cited_diagonal_schema_matches",
        "matched_citing_assertions", "general_specialization_options",
        "diagonal_proof_result", "diagonal_proof_source_locators",
        "current_delta_injectivity_subgoal_types", "old_delta_contains_pi55_premise",
    ):
        print("R3T_" + key.upper() + "=" + repr(record[key]))
    print("R3T_AUDIT_ONLY=True")
    print("R3T_FULL_PYTEST_RUN=False")
    print("R3T_REPORT=" + str(output))
    return record


if __name__ == "__main__":
    audit()
