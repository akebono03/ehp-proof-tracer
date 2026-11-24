"""Phase 176 R3R37: source-screened public candidate and local inference replay.

The report does not claim that the shared DFS citation/order gate was checked.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r37_composite_right_hopf_public"


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
    from map_facts import EHP_H_MAP
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase171_r2h_prop22_cited_hopf.source import (
        TodaProp22RightFormula, _formula_parts,
    )
    from phase176_r3r34_composite_suspension_isolated.source import (
        composite_suspension_equality_input,
    )
    from phase176_r3r36_composite_right_hopf_isolated.source import (
        COMPOSITE_FORMULA_RULE_NAME, COMPOSITE_SUBSTITUTION_RULE_NAME,
        composite_hopf_substitution_inputs,
    )
    from proof import ProofRule, Relation, RelationType, find_inference_match, apply_inference_match
    from unified_statement_registry import AssertionOrigin

    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    beta = Composition(eta5, eta6)
    suspended_beta = Suspension(beta)
    lhs = MapApplication(EHP_H_MAP, Composition(nu, suspended_beta))
    formula = Relation(
        lhs, Composition(MapApplication(EHP_H_MAP, nu), suspended_beta),
        RelationType.EQUALITY,
    )
    substituted = Relation(
        lhs, Composition(eta5, suspended_beta), RelationType.EQUALITY,
    )
    hopf = Relation(MapApplication(EHP_H_MAP, nu), eta5, RelationType.EQUALITY)

    if composite_hopf_substitution_inputs(substituted) != (formula, hopf):
        raise RuntimeError("R3R36_TYPED_SUBSTITUTION_CONTRACT_CHANGED")

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    source_steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    available = tuple(step.conclusion for step in source_steps)
    if available.count(TodaProp22RightFormula()) != 1 or available.count(hopf) != 1:
        raise RuntimeError("SCREENED_SOURCE_WITNESSES_NOT_UNIQUE")

    provider = shared_expansion_provider(screened, proof_target=roots[0])
    formula_candidates = tuple(
        item for item in provider(formula)
        if item.rule.name == COMPOSITE_FORMULA_RULE_NAME
    )
    substitution_candidates = tuple(
        item for item in provider(substituted)
        if item.rule.name == COMPOSITE_SUBSTITUTION_RULE_NAME
    )
    if (len(formula_candidates) != 1
            or formula_candidates[0].subgoals != (TodaProp22RightFormula(),)
            or len(substitution_candidates) != 1
            or substitution_candidates[0].subgoals != (formula, hopf)):
        raise RuntimeError("PUBLIC_COMPOSITE_HOPF_CANDIDATES_NOT_CONNECTED")

    universal = next(step for step in source_steps
                     if step.conclusion == TodaProp22RightFormula())
    source_hopf = next(step for step in source_steps
                       if step.conclusion == hopf)
    first_match = find_inference_match(formula_candidates[0].rule, (universal,))
    if first_match is None:
        raise RuntimeError("NO_FORMULA_INFERENCE_REPLAY")
    formula_step = apply_inference_match(first_match)
    second_match = find_inference_match(
        substitution_candidates[0].rule, (formula_step, source_hopf),
    )
    if second_match is None:
        raise RuntimeError("NO_HOPF_SUBSTITUTION_REPLAY")
    substituted_step = apply_inference_match(second_match)
    if (substituted_step.conclusion != substituted
            or substituted_step.rule is not ProofRule.INFERENCE
            or substituted_step.premises != (formula_step, source_hopf)):
        raise RuntimeError("INVALID_HOPF_REPLAY_CHAIN")

    # Regression: R3R35 stays visible and the historical single-factor path works.
    suspension_goal = Relation(
        Suspension(beta), Composition(eta6, eta7), RelationType.EQUALITY,
    )
    image = composite_suspension_equality_input(suspension_goal)
    if image is None:
        raise RuntimeError("R3R35_SUSPENSION_GOAL_TYPE_INVALID")
    suspension_candidates = tuple(
        item for item in provider(suspension_goal)
        if item.rule.name == "proved composite suspension image yields typed element equality"
    )
    if len(suspension_candidates) != 1 or suspension_candidates[0].subgoals != (image,):
        raise RuntimeError("R3R35_PUBLIC_BRANCH_LOST")
    single = Relation(
        MapApplication(EHP_H_MAP, Composition(nu, Suspension(eta5))),
        Composition(MapApplication(EHP_H_MAP, nu), Suspension(eta5)),
        RelationType.EQUALITY,
    )
    if _formula_parts(single) != (nu, eta5):
        raise RuntimeError("SINGLE_FACTOR_FORMULA_TYPE_INVALID")
    single_candidates = tuple(
        item for item in provider(single)
        if item.rule.name == "specialize cited Toda Proposition 2.2 right formula"
    )
    if len(single_candidates) != 1:
        raise RuntimeError("SINGLE_FACTOR_PROVIDER_REGRESSION")
    return {
        "gate": "PASS_R3R37_PUBLIC_COMPOSITE_HOPF_CONNECTED",
        "screened_prop22_count": available.count(TodaProp22RightFormula()),
        "screened_hopf_nu_prime_count": available.count(hopf),
        "public_formula_candidate_count": len(formula_candidates),
        "public_substitution_candidate_count": len(substitution_candidates),
        "public_substitution_subgoals": len(substitution_candidates[0].subgoals),
        "local_formula_replayed": formula_step.conclusion == formula,
        "local_substitution_replayed": substituted_step.conclusion == substituted,
        "r3r35_public_candidate_preserved": True,
        "legacy_single_factor_candidate_preserved": True,
        "source_screened_context_used": True,
        "shared_dfs_source_order_gate_verified": False,
        "transport_to_eta_cube_proved": False,
        "hopf_image_goal_proved": False,
        "root_group_proved": False,
        "new_given": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    try:
        result = probe()
    except Exception as error:
        result = {
            "gate": "FAIL_R3R37_PUBLIC_AUDIT",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / PACKAGE)
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / "public_report.json"
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for key, value in result.items():
        print("PHASE176_R3R37_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
