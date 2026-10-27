"""Read-only Phase 169 R6 diagnostic for the incomplete pi_8^6 proof route."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaIteratedSuspensionMap
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from phase169_r3o_stable_composite_rule import expand_cited_toda45_composite_transport
from phase169_r5b_pi75_prior_transport.rule import (
    expand_prior_cited_toda45_composite_transport,
)
from phase165_r52_r27_r5_literature import _toda45_universal_statement
from proof import ProofRule
from toda_rules import Toda45IsomorphismStatement
from web_group_proof import build_standard_web_group_proof_view

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8",
    ).stdout.strip()


def citation_screened_claims(context) -> tuple[object, ...]:
    """Return only verified screened GIVEN conclusions; never promote a DB goal."""
    return tuple(
        link.step.conclusion
        for link in context.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and not link.step.premises
    )


def prior_summary(prior) -> dict[str, object]:
    return {
        "eligible": prior.eligible,
        "reason": prior.reason,
        "source_assertion_id": prior.source_assertion_id,
        "relation_available_as_db_goal": prior.relation is not None,
    }


def inspect() -> dict[str, object]:
    """Inspect source position and actual search, preserving original ProofSteps."""
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=6, k=2)
    if len(candidates) != 1:
        raise RuntimeError("R6 requires a unique typed pi_8^6 goal")
    goal = candidates[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    if citing is None:
        raise RuntimeError("R6 pi_8^6 has no positioned publication citation")

    prior4 = resolve_prior_group_result(
        bridge, source_n=4, source_k=2, citing_assertion_id=citing,
    )
    prior5 = resolve_prior_group_result(
        bridge, source_n=5, source_k=2, citing_assertion_id=citing,
    )
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=6, k=2, bridge=bridge, goal=goal, context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("R6 public proof search produced no unique screened context")
    context = contexts[0]
    available = citation_screened_claims(context)
    schema = _toda45_universal_statement()
    schema_screened = any(claim == schema for claim in available)

    actual_r3o = expand_cited_toda45_composite_transport(goal, available)
    actual_r5b = expand_prior_cited_toda45_composite_transport(
        goal, available, context, proof_target=goal,
    )
    actual_r57 = expand_registered_toda45_finite_cyclic_goal(goal, available)

    source4 = prior4.relation
    source5 = prior5.relation
    goal_only_one_step = (
        expand_cited_toda45_composite_transport(goal, (source5, schema))
        if source5 is not None else ()
    )
    goal_only_two_step = (
        expand_cited_toda45_composite_transport(goal, (source4, schema))
        if source4 is not None else ()
    )
    direct_iso_specializable = False
    direct_generator_is_iterated_form = False
    if source4 is not None:
        direct_iso = Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(
            exponent=2, source_group=source4.lhs, target_group=goal.lhs,
        ))
        direct_iso_specializable = specialize_typed_statement(schema, direct_iso) is not None
        if isinstance(source4.rhs, FiniteCyclicGroup) and isinstance(goal.rhs, FiniteCyclicGroup):
            direct_generator_is_iterated_form = (
                IteratedSuspension(source4.rhs.generator, 2) == goal.rhs.generator
            )

    web = build_standard_web_group_proof_view(6, 2, mode="narrative")
    if web.partial_result != (result.status is not ProofSearchStatus.COMPLETE):
        raise RuntimeError("Web partial state does not match proof-search state")
    data = {
        "phase": "169-R6",
        "mode": "AUDIT_ONLY",
        "head": git("rev-parse", "HEAD"),
        "pi86_target_citation": citing,
        "candidate_count": len(candidates),
        "prior_pi64": prior_summary(prior4),
        "prior_pi75": prior_summary(prior5),
        "screened_pi64_given": source4 is not None and source4 in available,
        "screened_pi75_given": source5 is not None and source5 in available,
        "screened_toda45": schema_screened,
        "existing_r3o_options": len(actual_r3o),
        "existing_r5b_options": len(actual_r5b),
        "existing_r57_options": len(actual_r57),
        "goal_only_one_step_options": len(goal_only_one_step),
        "goal_only_two_step_options": len(goal_only_two_step),
        "two_step_iso_specializable": direct_iso_specializable,
        "two_step_db_generator_equals_iterated_expression": direct_generator_is_iterated_form,
        "pi86_status": result.status.value,
        "pi86_steps": len(result.proven_steps),
        "pi86_open_goals": len(result.open_goals),
        "pi86_unresolved_types": [type(item).__name__ for item in result.open_goals],
        "pi86_diagnostics": list(result.diagnostics),
        "web_key": web.key,
        "web_partial": web.partial_result,
        "web_steps": len(web.steps),
        "web_rendered_lines": len(web.rendered_lines),
        "full_pytest_run": False,
        "production_modified": False,
    }
    if result.status is ProofSearchStatus.COMPLETE:
        from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
        verify_proof_tree_for_narrative(result, context, citing_assertion_id=citing)
        data["proof_tree_verified"] = True
    else:
        data["proof_tree_verified"] = False
    return data


def summary_markdown(data: dict[str, object]) -> str:
    """Write only observed diagnostic values, never treat goal-only trials as proof."""
    keys = (
        "pi86_target_citation", "screened_toda45", "screened_pi64_given",
        "screened_pi75_given", "existing_r3o_options", "existing_r5b_options",
        "existing_r57_options", "goal_only_one_step_options", "goal_only_two_step_options",
        "two_step_iso_specializable", "two_step_db_generator_equals_iterated_expression",
        "pi86_status", "pi86_steps", "pi86_open_goals", "web_key", "web_partial",
    )
    lines = ["# Phase 169 R6 — π₈⁶ 輸送経路の原因切り分け", ""]
    for key in keys:
        lines.append(f"- {key}: `{data[key]}`")
    for source in ("prior_pi64", "prior_pi75"):
        lines.append("")
        lines.append(f"## {source}")
        for key, value in data[source].items():
            lines.append(f"- {key}: `{value}`")
    lines.extend([
        "", "## 境界", "",
        "Goal-only は探索候補の診断に限る。ProofStep は生成せず、既存 Provider も変更しない。",
        "DB の群構造を GIVEN に昇格させず、Toda (4.5) の適用範囲も変更しない。",
        "この監査では全体 pytest を実行しない。", "",
    ])
    return "\n".join(lines)


def main() -> None:
    branch = git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R6 audit requires the develop branch")
    print("R6_GIT_BRANCH=" + branch)
    print("R6_GIT_HEAD=" + git("rev-parse", "HEAD"))
    report = inspect()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    (OUTPUT / "audit.md").write_text(summary_markdown(report), encoding="utf-8")
    printed = (
        "screened_toda45", "existing_r3o_options", "existing_r5b_options",
        "existing_r57_options", "goal_only_one_step_options", "goal_only_two_step_options",
        "two_step_iso_specializable", "two_step_db_generator_equals_iterated_expression",
        "pi86_status", "pi86_steps", "pi86_open_goals", "web_key", "web_partial",
    )
    for key in printed:
        print("R6_" + key.upper() + "=" + str(report[key]))
    for name in ("prior_pi64", "prior_pi75"):
        print("R6_" + name.upper() + "_ELIGIBLE=" + str(report[name]["eligible"]))
        print("R6_" + name.upper() + "_REASON=" + str(report[name]["reason"]))
    print("R6_AUDIT_ONLY=True")
    print("R6_FULL_PYTEST_RUN=False")
    print("R6_REPORT=" + str(OUTPUT / "audit.md"))
    print("R6_JSON=" + str(OUTPUT / "audit.json"))


if __name__ == "__main__":
    main()
