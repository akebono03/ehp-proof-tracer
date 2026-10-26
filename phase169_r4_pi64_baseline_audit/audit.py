"""Phase 169 R4: read-only production search and citation audit for pi_6^4.

No proof step, registry assertion, production file or test is created or changed.
Only JSON/Markdown reports in this package's output/ directory are written.
"""
from __future__ import annotations

import csv
import json
import subprocess
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parent
EXPECTED_GITHUB_DEVELOP = "ff08b601badf339457ff524ca21847b5d6a67ef5"


def stable_range_allows(n: int, k: int) -> bool:
    """Report the existing one-step composite Toda (4.5) range n >= k+2.

    This is an audit of the implemented guard, not an independent theorem.
    """
    return type(n) is int and type(k) is int and n >= 2 and k >= 0 and n >= k + 2


def short(value: Any, limit: int = 1600) -> str:
    result = repr(value)
    return result if len(result) <= limit else result[:limit] + " [TRUNCATED]"


def describe_search(result: Any) -> dict[str, Any]:
    status = getattr(result, "status", None)
    steps = tuple(getattr(result, "proven_steps", ()))
    conclusion = getattr(result, "conclusion", None)
    return {
        "status": getattr(status, "value", str(status)),
        "steps": len(steps),
        "open_goals": [short(item) for item in getattr(result, "open_goals", ())],
        "diagnostics": list(getattr(result, "diagnostics", ())),
        "conclusion": short(conclusion),
        "has_root_in_proven_steps": conclusion is not None and any(
            step.conclusion == conclusion for step in steps
        ),
        "proof_rules": [getattr(step.rule, "name", str(step.rule)) for step in steps],
    }


def run_git(*args: str) -> dict[str, Any]:
    process = subprocess.run(
        ["git", *args], cwd=REPOSITORY, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    return {"exit_code": process.returncode,
            "stdout": process.stdout.strip(), "stderr": process.stderr.strip()}


def raw_database_rows(n: int, k: int) -> dict[str, Any]:
    """Read the exact CSV source rows without importing them as proof leaves."""
    source = REPOSITORY / "data" / "sphere.csv"
    generators = REPOSITORY / "data" / "HyoujiGen.csv"
    result: dict[str, Any] = {
        "sphere_path": str(source), "generator_dictionary_path": str(generators),
        "sphere_exists": source.is_file(), "generator_dictionary_exists": generators.is_file(),
        "matching_rows": [],
    }
    if source.is_file():
        with source.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("n") == str(n) and row.get("k") == str(k):
                    result["matching_rows"].append({
                        field: row.get(field) for field in (
                            "id", "n", "k", "orders", "generator", "Element",
                            "gen_coe", "hyouji", "P", "E", "H",
                        )
                    })
    return result


def assertion_summary(bridge: Any, assertion: Any) -> dict[str, Any]:
    ref = bridge.registry.reference(assertion.reference_id)
    return {
        "assertion_id": assertion.assertion_id,
        "locator": str(ref.locator),
        "publication_position": ref.publication_position,
        "component_position": assertion.component_position,
        "origin": getattr(assertion.origin, "name", str(assertion.origin)),
        "content_type": type(assertion.content).__name__,
        "content": short(assertion.content, 2200),
    }


def collect_relevant_assertions(bridge: Any) -> list[dict[str, Any]]:
    result = []
    for assertion in bridge.registry._assertions.values():
        row = assertion_summary(bridge, assertion)
        if any(token in row["locator"] for token in (
            "(4.5)", "Proposition 5.3", "Proposition 5.1", "Chapter V, i)"
        )):
            result.append(row)
    return result


def eligible_claims(screened: Any) -> tuple[object, ...]:
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    claims = []
    for link in screened.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = screened.registry.assertion(link.assertion_id)
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and assertion.content == link.step.conclusion):
            claims.append(link.step.conclusion)
    return tuple(claims)


def trace_model(result: Any, screened: Any) -> dict[str, Any]:
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model

    model = build_linked_proof_narrative_model(result, screened)
    citations = []
    for item in model.citations:
        citations.append({
            "number": item.number,
            "locator": str(item.reference.locator),
            "step_indices": list(item.step_indices),
            "assertion_ids": list(item.assertion_ids),
        })
    from proof import ProofRule
    return {
        "model_steps": len(model.steps),
        "model_citations": citations,
        "given_steps": sum(step.rule is ProofRule.GIVEN for step in model.steps),
        "root_index": model.root_index,
        "step_citation_numbers": [list(numbers) for numbers in model.step_citation_numbers],
    }


def run_case(bridge: Any, n: int, k: int) -> tuple[dict[str, Any], Any, Any, tuple[object, ...]]:
    from phase165_r55_nk_only_goal import (
        registered_group_goal_candidates, search_group_from_registered_goal,
    )
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context

    report: dict[str, Any] = {"n": n, "k": k, "group": f"pi_{n+k}^{n}"}
    goals = registered_group_goal_candidates(bridge, n=n, k=k)
    report["database_source"] = raw_database_rows(n, k)
    report["goal_count"] = len(goals)
    report["registered_goals"] = [short(goal, 3400) for goal in goals]
    if len(goals) != 1:
        report["classification"] = "GOAL_NOT_UNIQUE"
        return report, None, None, ()
    goal = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    report["citing_assertion_id"] = citing
    screened = None
    claims: tuple[object, ...] = ()
    if citing:
        report["citing_assertion"] = assertion_summary(
            bridge, bridge.registry.assertion(citing)
        )
        try:
            screened = screen_shared_proof_context(
                bridge, goal=goal, citing_assertion_id=citing,
                explicit_publication_target=True,
            )
            claims = eligible_claims(screened)
            report["screened_given_count"] = len(screened.proof_links)
            report["screened_claim_count"] = len(claims)
            report["self_given"] = any(
                link.assertion_id == citing for link in screened.proof_links
            )
            report["screened_source_ids"] = [
                link.assertion_id for link in screened.proof_links
            ]
        except Exception as exc:
            report["screen_error"] = f"{type(exc).__name__}: {exc}"
    contexts: list[Any] = []
    try:
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, goal=goal, context_sink=contexts.append,
        )
        report["search"] = describe_search(result)
        report["classification"] = "SEARCH_" + report["search"]["status"].upper()
        report["search_context_count"] = len(contexts)
        if contexts:
            try:
                report["proof_model"] = trace_model(result, contexts[-1])
            except Exception as exc:
                report["model_error"] = f"{type(exc).__name__}: {exc}"
        if report["search"]["status"] == "complete" and contexts and citing:
            try:
                from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
                verify_proof_tree_for_narrative(
                    result, contexts[-1], citing_assertion_id=citing,
                )
                report["trust_boundary_verified"] = True
            except Exception as exc:
                report["trust_boundary_verified"] = False
                report["trust_boundary_error"] = f"{type(exc).__name__}: {exc}"
    except Exception as exc:
        report["search_error"] = f"{type(exc).__name__}: {exc}"
        report["classification"] = "SEARCH_EXCEPTION"
        report["search_traceback"] = traceback.format_exc(limit=8)
    return report, goal, screened, claims


def audit_transport(lower: Any, upper: Any, upper_claims: tuple[object, ...]) -> dict[str, Any]:
    from homotopy_groups import TodaPrimaryGroup, TodaIteratedSuspensionMap, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
    from phase169_r3o_stable_composite_rule import expand_cited_toda45_composite_transport
    from phase165_r12_r21_eta_generator_chain import (
        _composition_eta_suspensions, expand_cited_eta_generator,
    )
    from toda_rules import Toda45IsomorphismStatement
    from phase165_r52_r27_r5_literature import _toda45_universal_statement
    from phase165_r57_r20_general_specialization import specialize_typed_statement

    report: dict[str, Any] = {"lower_present": lower is not None, "upper_present": upper is not None}
    report["source_stable_range"] = stable_range_allows(3, 2)
    report["next_source_stable_range"] = stable_range_allows(4, 2)
    if lower is None or upper is None:
        report["classification"] = "MISSING_UNIQUE_GOAL"
        return report
    report["dimensions_match_one_suspension"] = (
        lower.lhs == TodaPrimaryGroup(5, 3)
        and upper.lhs == TodaPrimaryGroup(6, 4)
    )
    schema = _toda45_universal_statement()
    concrete = Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(
        exponent=1, source_group=lower.lhs, target_group=upper.lhs,
    ))
    report["concrete_iso_statement"] = short(concrete)
    report["toda45_schema_specializes"] = (
        specialize_typed_statement(schema, concrete) is not None
    )
    trial_composite = expand_cited_toda45_composite_transport(
        upper, (lower, schema),
    )
    report["composite_candidates_with_injected_schema_and_lower"] = len(trial_composite)
    actual_composite = expand_cited_toda45_composite_transport(
        upper, upper_claims,
    )
    report["composite_candidates_in_actual_screened_context"] = len(actual_composite)
    report["basic_finite_cyclic_candidates_in_actual_context"] = len(
        expand_registered_toda45_finite_cyclic_goal(upper, upper_claims)
    )
    image = GeneratorImage(
        map=TodaSuspensionMap(lower.lhs, upper.lhs),
        source_generator=lower.rhs.generator,
        target_generator=upper.rhs.generator,
    )
    report["generator_image"] = short(image)
    report["eta_composite_image_witness_possible"] = (
        _composition_eta_suspensions(image) is not None
    )
    report["eta_image_expansion_count"] = len(expand_cited_eta_generator(image))
    report["lower_goal_in_upper_screened_claims"] = any(
        type(item) is type(lower) and item == lower for item in upper_claims
    )
    report["classification"] = (
        "STABLE_RANGE_BLOCKED" if not report["source_stable_range"]
        else "CANDIDATE_PRESENT" if actual_composite else "NO_SCREENED_CANDIDATE"
    )
    return report


def report_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 169 R4 — π₆⁴ 読み取り専用監査",
        "",
        "GitHub develop 既知 HEAD: `" + EXPECTED_GITHUB_DEVELOP + "`",
        "ローカル HEAD: `" + str(report["git"]["head"]["stdout"]) + "`",
        "",
        "## 探索結果",
    ]
    for key in ("pi_5^3", "pi_6^4"):
        case = report["cases"].get(key, {})
        search = case.get("search", {})
        lines.extend([
            f"### {key}",
            "",
            f"- 判定: `{case.get('classification', 'UNKNOWN')}`",
            f"- Goal 候補: {case.get('goal_count', 'UNKNOWN')}",
            f"- 証明 Step: {search.get('steps', '未確認')}",
            f"- 未解決 Goal: {len(search.get('open_goals', []))}",
            f"- Citation target: `{case.get('citing_assertion_id')}`",
            f"- 自己 GIVEN: `{case.get('self_given')}`",
            "",
        ])
        if key == "pi_5^3":
            lines.append(f"- R3Z baseline (28 Step, 6 Reference, verified): `{case.get('r3z_baseline_maintained', '未確認')}`")
            lines.append("")
        if "proof_model" in case:
            lines.append(f"- モデル Reference 数: {len(case['proof_model'].get('model_citations', []))}")
            lines.append("")
        if "model_error" in case:
            lines.append("- モデルエラー: `" + case["model_error"] + "`")
        if "trust_boundary_error" in case:
            lines.append("- Trust Boundary エラー: `" + case["trust_boundary_error"] + "`")
        for index, goal in enumerate(search.get("open_goals", []), start=1):
            lines.append(f"{index}. `{goal}`")
        lines.append("")
        if "search_error" in case:
            lines.append("検索エラー: `" + case["search_error"] + "`")
            lines.append("")
    tr = report.get("transport", {})
    lines.extend([
        "## Toda (4.5) と生成元",
        "",
        f"- n=3, k=2 安定範囲: `{tr.get('source_stable_range')}`",
        f"- n=4, k=2 安定範囲: `{tr.get('next_source_stable_range')}`",
        f"- 引用済み前提における複合輸送候補: `{tr.get('composite_candidates_in_actual_screened_context')}`",
        f"- 前提を人工的に渡した場合の複合輸送候補: `{tr.get('composite_candidates_with_injected_schema_and_lower')}`（証明には採用しない診断）",
        f"- 生成元の合成懸垂に対する Goal 展開候補: `{tr.get('eta_image_expansion_count')}`",
        "",
        "R4 は証明を生成しない。特に、候補・既知の群構造・出典だけから完成証明を主張しない。",
        "",
        "## 次工程の境界",
        "",
        "得られた未解決 Goal と文献順を確認し、別の合法的導出経路の有無を決める。"
        " 安定範囲の条件は R4 では変更しない。",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    report: dict[str, Any] = {
        "phase": "169-R4", "mode": "AUDIT_ONLY", "production_modified": False,
        "full_pytest_run": False,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git": {
            "head": run_git("rev-parse", "HEAD"),
            "branch": run_git("branch", "--show-current"),
            "tracked_worktree_files": run_git("diff", "--name-only"),
            "staged_files": run_git("diff", "--cached", "--name-only"),
        },
        "cases": {},
    }
    try:
        from phase165_r52_r9_shared_math import build_shared_typed_bridge
        bridge = build_shared_typed_bridge()
        report["relevant_assertions"] = collect_relevant_assertions(bridge)
        goals: dict[str, Any] = {}
        claims: dict[str, tuple[object, ...]] = {}
        for n, k in ((3, 2), (4, 2)):
            key = f"pi_{n+k}^{n}"
            case, goal, _screened, given = run_case(bridge, n, k)
            report["cases"][key] = case
            goals[key] = goal
            claims[key] = given
            if key == "pi_5^3":
                baseline_model = case.get("proof_model", {})
                case["r3z_baseline_maintained"] = (
                    case.get("search", {}).get("status") == "complete"
                    and case.get("search", {}).get("steps") == 28
                    and len(baseline_model.get("model_citations", ())) == 6
                    and case.get("trust_boundary_verified") is True
                )
            print(f"R4_{key}: {case['classification']}")
            print("  steps:", case.get("search", {}).get("steps", "unknown"))
            print("  open_goals:", len(case.get("search", {}).get("open_goals", ())))
        report["transport"] = audit_transport(
            goals["pi_5^3"], goals["pi_6^4"], claims["pi_6^4"],
        )
        print("R4_TRANSPORT:", report["transport"]["classification"])
    except Exception as exc:
        report["audit_error"] = f"{type(exc).__name__}: {exc}"
        report["audit_traceback"] = traceback.format_exc()
        print("R4_AUDIT_ERROR:", report["audit_error"])
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    (output / "audit.md").write_text(report_markdown(report), encoding="utf-8")
    print("R4_JSON=", output / "audit.json")
    print("R4_MARKDOWN=", output / "audit.md")
    print("R4_FULL_PYTEST_RUN=False")
    if report.get("audit_error"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
