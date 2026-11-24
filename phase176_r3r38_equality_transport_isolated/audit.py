"""Read-only Phase 176 R3R38 source-screened local replay audit."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r38_equality_transport_isolated"
ROOT = Path(__file__).resolve().parent.parent


def source_guard() -> None:
    """Require exactly the already-reviewed public hooks and existing rules."""
    required = (
        "phase165_r52_r9_shared_math.py",
        "phase176_r3r34_composite_suspension_isolated/source.py",
        "phase176_r3r36_composite_right_hopf_isolated/source.py",
        "relation_rules.py",
        "hopf_rules.py",
    )
    for path in required:
        source = ROOT / path
        if not source.is_file():
            raise ValueError("MISSING_SOURCE:" + path)
        ast.parse(source.read_text(encoding="utf-8-sig"), filename=str(source))
    shared = (ROOT / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8-sig")
    anchors = (
        "options.extend(expand_composite_suspension_equality(goal))",
        "options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))",
    )
    if any(shared.count(anchor) != 1 for anchor in anchors):
        raise ValueError("R3R35_R3R37_PUBLIC_HOOKS_REQUIRED")


def probe() -> dict:
    """Replay sourced R3R35+R3R37 input proofs and six old transport rules."""
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
    from map_facts import EHP_H_MAP
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r34_composite_suspension_isolated.source import (
        composite_suspension_equality_input,
    )
    from phase176_r3r36_composite_right_hopf_isolated.source import (
        COMPOSITE_FORMULA_RULE_NAME,
        COMPOSITE_SUBSTITUTION_RULE_NAME,
    )
    from phase176_r3r38_equality_transport_isolated.source import (
        right_hopf_transport_inputs,
        replay_right_hopf_transport,
    )
    from proof import ProofRule, Relation, RelationType, find_inference_match, apply_inference_match
    from unified_statement_registry import AssertionOrigin

    nu_prime = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    beta = Composition(eta5, eta6)
    gamma = Composition(eta6, eta7)
    suspension_goal = Relation(Suspension(beta), gamma, RelationType.EQUALITY)
    goal = Relation(
        MapApplication(EHP_H_MAP, Composition(nu_prime, gamma)),
        Composition(eta5, gamma), RelationType.EQUALITY,
    )
    required = right_hopf_transport_inputs(goal, beta)
    if required is None or required[1] != suspension_goal:
        raise RuntimeError("TRANSPORT_TYPED_PREMISES_INVALID")
    substituted, _ = required
    formula = Relation(
        substituted.lhs,
        Composition(MapApplication(EHP_H_MAP, nu_prime), Suspension(beta)),
        RelationType.EQUALITY,
    )
    hopf_value = Relation(MapApplication(EHP_H_MAP, nu_prime), eta5,
                          RelationType.EQUALITY)

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    fixed_steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    available = tuple(step.conclusion for step in fixed_steps)
    if (available.count(TodaProp22RightFormula()) != 1
            or available.count(hopf_value) != 1):
        raise RuntimeError("SCREENED_SOURCES_NOT_UNIQUE")
    prop22_step = next(s for s in fixed_steps if s.conclusion == TodaProp22RightFormula())
    hopf_step = next(s for s in fixed_steps if s.conclusion == hopf_value)
    provider = shared_expansion_provider(screened, proof_target=roots[0])

    def choose(item, rule_name):
        matches = tuple(x for x in provider(item) if x.rule.name == rule_name)
        if len(matches) != 1:
            raise RuntimeError("PROVIDER_CANDIDATE_NOT_UNIQUE:" + rule_name)
        return matches[0]

    formula_candidate = choose(formula, COMPOSITE_FORMULA_RULE_NAME)
    substitution_candidate = choose(substituted, COMPOSITE_SUBSTITUTION_RULE_NAME)
    suspension_candidate = choose(
        suspension_goal, "proved composite suspension image yields typed element equality",
    )
    image_goal = composite_suspension_equality_input(suspension_goal)
    if (image_goal is None
            or formula_candidate.subgoals != (TodaProp22RightFormula(),)
            or substitution_candidate.subgoals != (formula, hopf_value)
            or suspension_candidate.subgoals != (image_goal,)):
        raise RuntimeError("PUBLIC_SUBGOALS_CHANGED")
    image_candidates = tuple(x for x in provider(image_goal) if not x.subgoals)
    if len(image_candidates) != 1:
        raise RuntimeError("IMAGE_LEAF_NOT_UNIQUE")

    def apply_one(candidate, steps, expected):
        match = find_inference_match(candidate.rule, steps)
        if match is None:
            raise RuntimeError("CANNOT_REPLAY:" + candidate.rule.name)
        step = apply_inference_match(match)
        if (step.rule is not ProofRule.INFERENCE or step.conclusion != expected
                or step.premises != steps):
            raise RuntimeError("REPLAY_OUTPUT_INVALID:" + candidate.rule.name)
        return step

    formula_step = apply_one(formula_candidate, (prop22_step,), formula)
    substituted_step = apply_one(substitution_candidate, (formula_step, hopf_step), substituted)
    image_step = apply_one(image_candidates[0], (), image_goal)
    suspension_step = apply_one(suspension_candidate, (image_step,), suspension_goal)
    transport = replay_right_hopf_transport(
        goal, beta, substituted_step, suspension_step,
    )
    if transport[-1].conclusion != goal or len(transport) != 6:
        raise RuntimeError("TRANSPORT_REPLAY_NOT_CONCLUDED")
    return {
        "gate": "PASS_R3R38_SOURCED_LOCAL_TRANSPORT_REPLAY_NOT_PUBLIC",
        "source_screened_prop22_count": available.count(TodaProp22RightFormula()),
        "source_screened_hopf_value_count": available.count(hopf_value),
        "r3r35_suspension_inference_replayed": True,
        "r3r37_hopf_substitution_replayed": True,
        "old_transport_inference_steps": len(transport),
        "old_transport_rule_names": [x.inference_rule.name for x in transport],
        "transport_to_eta_composite_local_replayed": True,
        "shared_provider_modified": False,
        "shared_dfs_source_order_gate_verified": False,
        "toda55_eta_cube_equivalence_proved": False,
        "hopf_image_goal_proved_in_shared_dfs": False,
        "root_group_proved": False,
        "new_given": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        source_guard()
        result = ({
            "gate": "PASS_R3R38_DRYRUN",
            "full_pytest": "NOT_RUN",
        } if args.dry_run else probe())
    except Exception as error:
        result = {
            "gate": "FAIL_R3R38",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    destination = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                   / "EHPProofTracerAudit" / PACKAGE / "report.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R38_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
