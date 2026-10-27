"""R10EF audit-only: capture real competing one-stem derivations and provenance.

The production append routine and proof search run unchanged. A mocked
module-level call merely observes the candidates after delegating to the
original. Neither a candidate nor its conclusion is promoted to a proof.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from phase169_r10ef_one_stem_duplicate_trace.trace import (
    forward_and_observe,
    pairwise_kept_indices,
)

OUTPUT = Path(__file__).resolve().parent / "output"
CASES = ((4, 1), (5, 1))


def _short(value: object, limit: int = 1200) -> str:
    rendered = repr(value)
    return rendered if len(rendered) <= limit else rendered[:limit] + " [truncated]"


def describe_step(step: object, screened: object) -> dict:
    """Summarize actual cited ancestors without interpreting rule names as facts."""
    from proof import ProofRule

    seen: set[int] = set()
    leaves: list[dict] = []
    pending = [step]
    while pending:
        ancestor = pending.pop()
        if id(ancestor) in seen:
            continue
        seen.add(id(ancestor))
        if ancestor.rule is ProofRule.GIVEN:
            reference = getattr(getattr(ancestor, "inference_rule", None),
                                "literature_reference", None)
            links = [
                item.assertion_id for item in screened.proof_links
                if item.step is ancestor or (item.step is not None and item.step == ancestor)
            ]
            leaves.append({
                "type": type(ancestor.conclusion).__name__,
                "conclusion": _short(ancestor.conclusion, 700),
                "assertion_ids": list(dict.fromkeys(links)),
                "locator": getattr(reference, "locator", None),
                "note": _short(getattr(ancestor, "note", None), 220),
            })
        pending.extend(ancestor.premises)
    return {
        "rule": step.rule.value,
        "rule_name_observational_only": getattr(step.inference_rule, "name", None),
        "conclusion_type": type(step.conclusion).__name__,
        "conclusion_repr": _short(step.conclusion, 900),
        "premise_count": len(step.premises),
        "premise_types": [type(parent.conclusion).__name__ for parent in step.premises],
        "premise_rule_names_observational_only": [
            getattr(parent.inference_rule, "name", None) for parent in step.premises
        ],
        "given_ancestors": leaves,
    }


def _comparison(left: object, right: object) -> dict:
    """Report existing equivalence checks; do not collapse either candidate."""
    from phase165_r12_r33_proof_tree_dedup import same_completed_proof_tree
    from phase165_r6_2_r4_r8_dedup import same_cited_scalar_specialization

    comparisons = {}
    for name, check in (
        ("same_completed_proof_tree", same_completed_proof_tree),
        ("same_cited_scalar_specialization", same_cited_scalar_specialization),
    ):
        try:
            comparisons[name] = bool(check(left, right))
        except (ValueError, TypeError, AttributeError) as exc:
            comparisons[name] = "ERROR_" + type(exc).__name__ + ": " + str(exc)
    comparisons["same_step_value"] = left == right
    comparisons["same_premise_object_identity"] = (
        len(left.premises) == len(right.premises)
        and all(a is b for a, b in zip(left.premises, right.premises))
    )
    return comparisons


def inspect_case(n: int, k: int, bridge: object) -> dict:
    """Trace one real registered group search through its original append logic."""
    import phase165_r3_recursive_search as recursive
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import (
        registered_group_goal_candidates,
        search_group_from_registered_goal,
    )

    candidates = registered_group_goal_candidates(bridge, n=n, k=k)
    if len(candidates) != 1:
        raise RuntimeError(f"R10EF requires exactly one registered goal for n={n}, k={k}")
    goal = candidates[0]
    observations = []
    previous = recursive.append_unique_verified_derivation
    contexts = []

    def observing_append(options, candidate):
        forward_and_observe(
            options, candidate, goal=goal, delegate=previous,
            observations=observations,
        )

    with patch.object(recursive, "append_unique_verified_derivation", observing_append):
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
    screened = contexts[-1] if contexts else None
    if screened is None:
        raise RuntimeError(f"R10EF missing screened context for n={n}, k={k}")
    attempts = []
    for i, observation in enumerate(observations):
        attempts.append({
            "attempt_index": i,
            "kept_after_original_dedup": observation.kept,
            "options_before": observation.options_before,
            "options_after": observation.options_after,
            **describe_step(observation.candidate, screened),
        })
    pairs = []
    for left, right in pairwise_kept_indices(observations):
        pairs.append({
            "left_attempt": left,
            "right_attempt": right,
            **_comparison(observations[left].candidate, observations[right].candidate),
        })
    return {
        "group": f"pi_{n+k}^{n}",
        "n": n,
        "k": k,
        "status": result.status.value,
        "is_complete": result.status is ProofSearchStatus.COMPLETE,
        "diagnostics": list(result.diagnostics),
        "proven_step_count": len(result.proven_steps),
        "open_goal_types": [type(item).__name__ for item in result.open_goals],
        "root_attempt_count": len(attempts),
        "root_kept_count": sum(item["kept_after_original_dedup"] for item in attempts),
        "root_candidate_attempts": attempts,
        "kept_candidate_pairs": pairs,
        "screened_context_observed": bool(contexts),
        "production_proof_rule_changed": False,
        "no_candidate_selection": True,
    }


def make_report() -> dict:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    bridge = build_shared_typed_bridge()
    cases = [inspect_case(n, k, bridge) for n, k in CASES]
    return {
        "phase": "169 R10EF",
        "mode": "AUDIT_ONLY",
        "review_type": "duplicate derivation provenance and conservative dedup",
        "cases": cases,
        "production_code_changed": False,
        "full_pytest_run": False,
    }


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = make_report()
    output = OUTPUT / "duplicate_root_trace.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    for item in report["cases"]:
        key = "R10EF_" + item["group"]
        print(key + "_STATUS=" + item["status"], flush=True)
        print(key + "_ROOT_ATTEMPTS=" + str(item["root_attempt_count"]), flush=True)
        print(key + "_KEPT_DERIVATIONS=" + str(item["root_kept_count"]), flush=True)
        print(key + "_PAIR_COMPARISONS=" + json.dumps(
            item["kept_candidate_pairs"], ensure_ascii=False), flush=True)
        for attempt in item["root_candidate_attempts"]:
            print(key + "_CANDIDATE=" + json.dumps({
                "index": attempt["attempt_index"],
                "kept": attempt["kept_after_original_dedup"],
                "rule": attempt["rule_name_observational_only"],
                "premise_types": attempt["premise_types"],
                "given_locators": [given["locator"] for given in attempt["given_ancestors"]],
            }, ensure_ascii=False), flush=True)
    print("R10EF_AUDIT_JSON=" + str(output), flush=True)
    print("R10EF_PRODUCTION_CHANGED=False", flush=True)
    print("R10EF_FULL_PYTEST_RUN=False", flush=True)


if __name__ == "__main__":
    main()
