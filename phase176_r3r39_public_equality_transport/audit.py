"""Source-screened public DFS audit; fail closed when any step is missing."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import sys
import tempfile

from phase176_r3r39_public_equality_transport.apply import ROOT, TARGET, updated_source

PACKAGE = "phase176_r3r39_public_equality_transport"


def source_guard(require_patch: bool) -> None:
    for filename in (
        "phase165_r52_r9_shared_math.py",
        "phase176_r3r38_equality_transport_isolated/source.py",
        "phase176_r3r34_composite_suspension_isolated/source.py",
        "phase176_r3r36_composite_right_hopf_isolated/source.py",
        "relation_rules.py",
        "hopf_rules.py",
    ):
        path = ROOT / filename
        if not path.is_file():
            raise ValueError("MISSING_SOURCE:" + filename)
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=filename)
    current = TARGET.read_text(encoding="utf-8-sig")
    proposed = updated_source(current)
    if require_patch and proposed != current:
        raise ValueError("PUBLIC_PATCH_NOT_APPLIED")
    if require_patch and current.count("options.extend(public_right_hopf_transport(goal))") != 1:
        raise ValueError("PUBLIC_DISPATCH_NOT_UNIQUE")


def probe() -> dict:
    """Run real shared DFS over the screened root context, not fake inputs."""
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from map_facts import EHP_H_MAP
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r39_public_equality_transport.source import (
        right_hopf_transport_backward_plan,
    )
    from proof import ProofRule, Relation, RelationType
    from unified_statement_registry import AssertionOrigin

    nu_prime = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = Composition(eta6, eta7)
    goal = Relation(
        MapApplication(EHP_H_MAP, Composition(nu_prime, gamma)),
        Composition(eta5, gamma), RelationType.EQUALITY,
    )

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )
    available = tuple(step.conclusion for step in steps)
    if len(right_hopf_transport_backward_plan(goal, available)) != 6:
        raise RuntimeError("SOURCE_FIRST_TRANSPORT_PLAN_MISSING")
    if available.count(TodaProp22RightFormula()) != 1:
        raise RuntimeError("PROPOSITION_22_CITATION_MISSING")

    provider = shared_expansion_provider(screened, proof_target=roots[0])
    root_options = provider(goal)
    plan = right_hopf_transport_backward_plan(goal, available)
    if not any(option.rule.name == "equality transitivity"
               and option.subgoals == plan[-1][1].subgoals
               for option in root_options):
        raise RuntimeError("SHARED_ROOT_EXPANSION_MISSING")
    events: list[tuple[str, object]] = []
    ids = tuple(screened.registry._assertions)
    if not ids:
        raise RuntimeError("EMPTY_SCREENED_REGISTRY")

    inferred = reconstruct_registered_goal(
        goal,
        screened,
        ids[0],
        provider,
        lookup_mode="typed_reference",
        progress_observer=lambda kind, target, _step: events.append((kind, target)),
    )
    if inferred.conclusion != goal or inferred.rule is not ProofRule.INFERENCE:
        raise RuntimeError("SHARED_DFS_DID_NOT_PROVE_HOPF_TRANSPORT")

    visited: list = []
    def visit(step):
        for child in step.premises:
            visit(child)
        visited.append(step)
    visit(inferred)
    transport_names = [
        "equality preserved under left composition",
        "EHP H preserves equality",
        "equality symmetry",
        "equality preserved under left composition",
        "equality transitivity",
        "equality transitivity",
    ]
    for target, expansion in plan:
        step = next((item for item in reversed(visited)
                     if item.conclusion == target), None)
        if (step is None or step.rule is not ProofRule.INFERENCE
                or step.inference_rule.name != expansion.rule.name
                or tuple(child.conclusion for child in step.premises) != expansion.subgoals):
            raise RuntimeError("SIX_STEP_PROOF_TREE_MISMATCH:" + expansion.rule.name)
    if not any(kind == "proved" and target == goal for kind, target in events):
        raise RuntimeError("DFS_PROGRESS_NOT_RECORDED")
    if not any(step.conclusion == TodaProp22RightFormula()
               and step.rule is ProofRule.GIVEN for step in visited):
        raise RuntimeError("PROPOSITION_22_PROVENANCE_MISSING")

    return {
        "gate": "PASS_R3R39_PUBLIC_SOURCED_DFS_SIX_EXISTING_STEPS",
        "registered_root_candidates": len(roots),
        "cited_prop22_count": available.count(TodaProp22RightFormula()),
        "six_old_rules_in_shared_proof_tree": transport_names,
        "shared_dfs_intermediate_hopf_transport_proved": True,
        "screened_context_used": True,
        "root_order_gate_retained": True,
        "toda55_quadruple_connection_proved": False,
        "root_hopf_image_goal_proved": False,
        "group_structure_proved": False,
        "new_given": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        source_guard(require_patch=not args.dry_run)
        result = ({"gate": "PASS_R3R39_DRYRUN", "full_pytest": "NOT_RUN"}
                  if args.dry_run else probe())
    except Exception as error:
        result = {
            "gate": "FAIL_R3R39",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    destination = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                   / "EHPProofTracerAudit" / PACKAGE / "report.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R39_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
