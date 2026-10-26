"""Actual R3I provenance and citation audit; never asserts a future complete proof."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r5_ehp_connection import (
    expand_cited_ehp_terminal_goal, expand_registered_ehp_terminal_goal,
)
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3h_source_registry import ASSERTION_ID
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step
from toda_rules import TodaDeltaInjectiveStatement, TodaHopfInvariantSurjectiveStatement

PACKAGE = Path(__file__).resolve().parent


def validate_completed_proof_tree(root: ProofStep, screened, citing: str) -> dict:
    """Replay every inference and identify each GIVEN as an earlier screened source.

    This is an independent tree audit, not a proof leaf or a search shortcut.
    """
    if not isinstance(root, ProofStep):
        raise TypeError("root must be a ProofStep")
    visited: set[int] = set()
    visiting: set[int] = set()
    givens = []
    inferences = []
    citations = set()
    terminal_rules = set()

    def walk(step: ProofStep) -> None:
        key = id(step)
        if key in visiting:
            raise AssertionError("cycle in completed proof tree")
        if key in visited:
            return
        if not isinstance(step, ProofStep):
            raise AssertionError("non-ProofStep in completed proof tree")
        visiting.add(key)
        try:
            if step.rule is ProofRule.GIVEN:
                if step.premises:
                    raise AssertionError("GIVEN with fabricated proof ancestry")
                matches = tuple(link for link in screened.proof_links
                                if link.step is not None and link.step == step
                                and precedes_citing_assertion(screened, link.assertion_id, citing))
                if not matches:
                    raise AssertionError("GIVEN lacks an exact prior screened reference")
                givens.append(step)
                citations.update(link.assertion_id for link in matches)
            elif step.rule is ProofRule.INFERENCE:
                if step.inference_rule is None or not step.premises:
                    raise AssertionError("inference lacks rule or premises")
                for ancestor in step.premises:
                    walk(ancestor)
                matches = tuple(match for match in find_inference_matches_for_rule(
                    step.inference_rule, tuple(step.premises))
                    if tuple(match.premises) == tuple(step.premises))
                if len(matches) != 1:
                    raise AssertionError("stored inference not accepted by its rule")
                replayed = derive_inference_proof_step(matches[0])
                if replayed.conclusion != step.conclusion or replayed.rule is not ProofRule.INFERENCE:
                    raise AssertionError("stored inference conclusion not replayable")
                inferences.append(step)
                if step.inference_rule.name.startswith("cited prior sources:"):
                    terminal_rules.add(step.inference_rule.name)
            else:
                raise AssertionError("unknown proof step rule")
            visited.add(key)
        finally:
            visiting.remove(key)

    walk(root)
    if root.rule is not ProofRule.INFERENCE or not givens or not inferences:
        raise AssertionError("missing derived root or valid ancestors")
    if len(terminal_rules) != 2:
        raise AssertionError("both sourced EHP terminal derivations must be ancestors")
    return {
        "given_count": len(givens),
        "inference_count": len(inferences),
        "node_count": len(visited),
        "cited_assertion_ids": sorted(citations),
        "terminal_rule_names": sorted(terminal_rules),
        "all_givens_prior": True,
        "all_inferences_replayed": True,
        "cyclic_or_unregistered_leaf": False,
    }


def audit() -> int:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(goals) != 1:
        raise AssertionError("pi5^3 must have a unique database goal")
    goal = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    if not citing:
        raise AssertionError("typed citing assertion missing")
    source_id = "shared:8:" + ASSERTION_ID
    if not precedes_citing_assertion(bridge, source_id, citing):
        raise AssertionError("(5.3) is not earlier than Proposition 5.3")
    contexts = []
    upper = search_group_from_registered_goal(n=3, k=2, bridge=bridge, context_sink=contexts.append)
    lower = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    if lower.status is not ProofSearchStatus.COMPLETE:
        raise AssertionError("pi4^2 lower completed proof regressed")
    if len(contexts) != 1:
        raise AssertionError("actual upper proof context missing")
    screened = contexts[0]
    source_proofs = tuple(
        link.step for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    screened_hopf = tuple(link for link in screened.proof_links
                            if link.assertion_id == source_id and link.step is not None)
    if len(screened_hopf) != 1 or screened_hopf[0].step.rule is not ProofRule.GIVEN:
        raise AssertionError("(5.3) was not screened as a source GIVEN")
    provider = shared_expansion_provider(screened, proof_target=goal)
    terminals = (
        TodaHopfInvariantSurjectiveStatement(
            TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)),
        ),
        TodaDeltaInjectiveStatement(
            TodaDeltaMap(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2)),
        ),
    )
    terminal_records = []
    for terminal in terminals:
        available = tuple(step.conclusion for step in source_proofs)
        old, = expand_registered_ehp_terminal_goal(terminal, available)
        adapted, = expand_cited_ehp_terminal_goal(terminal, available)
        if (not all(p.proof_rule is ProofRule.INFERENCE for p in old.rule.premise_patterns)
                or not all(p.proof_rule is ProofRule.GIVEN for p in adapted.rule.premise_patterns)
                or adapted.rule.match_guard.__code__ is not old.rule.match_guard.__code__
                or adapted.rule.conclusion_builder.__code__ is not old.rule.conclusion_builder.__code__):
            raise AssertionError("historical EHP guard or mathematical conclusion changed")
        result = reconstruct_registered_goal(
            terminal, screened, citing, provider,
            lookup_mode="typed_reference_publication",
        )
        if result.rule is not ProofRule.INFERENCE or result.conclusion != terminal:
            raise AssertionError("terminal goal not derived by genuine inference")
        if (result.inference_rule is None
                or not result.inference_rule.name.startswith("cited prior sources:")
                or len(result.premises) != len(adapted.subgoals)
                or not all(p.rule is ProofRule.GIVEN and not p.premises for p in result.premises)
                or tuple(p.conclusion for p in result.premises) != adapted.subgoals):
            raise AssertionError("EHP citation premises were not preserved")
        terminal_records.append({
            "goal": type(terminal).__name__,
            "proof_rule": result.rule.value,
            "premise_rules": [p.rule.value for p in result.premises],
            "mathematical_rule_guard_reused": True,
            "historical_rule_unchanged": True,
            "inference_rule": result.inference_rule.name,
        })
    # R3I2: a successful upper search is a claim that requires a closed,
    # citation-checked proof tree, not merely a COMPLETE status flag.
    if upper.status is not ProofSearchStatus.COMPLETE or upper.conclusion != goal:
        raise AssertionError("pi5^3 was not completed by the screened search")
    root = reconstruct_registered_goal(
        goal, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    if root.conclusion != goal:
        raise AssertionError("completed root does not match the database goal")
    closure = validate_completed_proof_tree(root, screened, citing)
    report = {
        "phase": "169-R3I2", "lower_status": lower.status.value,
        "upper_status": upper.status.value, "upper_proven_steps": len(upper.proven_steps),
        "upper_complete": True,
        "root_verified": root.conclusion == goal,
        "proof_tree_closure": closure,
        "citing_assertion": citing, "hopf_source_assertion": source_id,
        "hopf_source_prior": True, "hopf_source_rule": ProofRule.GIVEN.value,
        "terminal_results": terminal_records,
        "unjustified_given_added": 0,
        "historical_rules_modified": False,
        "full_suite_run": False,
    }
    out = PACKAGE / "output" / "cited_ehp_inference_closure.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for key in ("lower_status", "upper_status", "upper_proven_steps", "hopf_source_prior"):
        print(key.upper() + "=" + repr(report[key]))
    for row in terminal_records:
        print("TERMINAL=" + row["goal"] + " DERIVED=inference PREMISES=" + repr(row["premise_rules"]))
    print("FULL_SUITE_RUN=False")
    print("REPORT=" + str(out))
    print("R3I_TERMINAL_CITATIONS_DERIVED=True")
    print("R3I2_CLOSED_PROOF_TREE_VERIFIED=True")
    print("R3I2_TREE_NODES=" + str(closure["node_count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(audit())
