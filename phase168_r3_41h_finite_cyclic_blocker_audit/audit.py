"""Phase 168 R3-41H: read-only provenance audit for blocked finite cyclic goals.

Observe the existing typed search once per target and compare actual blocked
subgoals against screened GIVEN links, registered fixed assertions, and the
current no-argument backward rule catalog. This does not infer any proof.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
from unittest.mock import patch
from zipfile import ZIP_DEFLATED, ZipFile

from phase168_r3_41g_zero_step_search_trace.audit import (
    SearchObservation, instrument_reconstruction,
)

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
CASES = (("pi6_4", 4, 2), ("pi6_3", 3, 3))
SOURCES = (
    "phase165_r12_r5_structure_bridge.py",
    "phase165_r12_r31_proven_cyclic_reuse.py",
    "phase165_r3_recursive_search.py",
    "phase165_r52_r9_shared_math.py",
    "phase165_r52_r16_web_citation_gate.py",
    "phase165_r55_nk_only_goal.py",
)


def unique_by_typed_value(items: tuple[object, ...] | list[object]) -> tuple[object, ...]:
    """Deduplicate audit observations only; no source or ProofStep is changed."""
    unique = []
    for item in items:
        if not any(type(item) is type(existing) and item == existing for existing in unique):
            unique.append(item)
    return tuple(unique)


def classify_blocker(*, status: str, proved: int, finite_blocked: int,
                     root_options: int) -> str:
    """Describe a search observation, not a theorem or a missing fact."""
    if status == "complete":
        return "COMPLETE"
    if finite_blocked and not proved and root_options:
        return "FINITE_CYCLIC_PREMISE_NO_EXPANSION"
    if finite_blocked:
        return "FINITE_CYCLIC_PREMISE_BLOCKED_WITH_OTHER_PROGRESS"
    if not root_options:
        return "ROOT_NO_EXPANSION_OR_NOT_REACHED"
    return "OTHER_UNRESOLVED_SEARCH"


def inspect_cyclic_goal(goal, *, screened, registry, all_links) -> dict:
    """Count exact source matches, never choose a candidate or add a GIVEN."""
    from proof import ProofRule, Relation
    from unified_statement_registry import AssertionOrigin

    exact_screened = []
    group_related_screened = []
    for link in screened.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        statement = link.step.conclusion
        if type(statement) is type(goal) and statement == goal:
            exact_screened.append(link.assertion_id)
        if (isinstance(statement, Relation)
                and getattr(statement, "lhs", None) == goal.group):
            group_related_screened.append(link.assertion_id)

    exact_registered = []
    same_group_registered = []
    for assertion in registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is type(goal) and assertion.content == goal:
            entry = registry.reference(assertion.reference_id)
            exact_registered.append({
                "assertion_id": assertion.assertion_id,
                "reference_id": assertion.reference_id,
                "locator": entry.locator,
                "publication_position": entry.publication_position,
                "component_position": assertion.component_position,
            })
        if (isinstance(assertion.content, Relation)
                and getattr(assertion.content, "lhs", None) == goal.group):
            same_group_registered.append(assertion.assertion_id)

    return {
        "type": type(goal).__name__,
        "goal": repr(goal),
        "order": goal.order,
        "group": repr(goal.group),
        "generator": repr(goal.generator),
        "screened_exact_given_assertion_ids": exact_screened,
        "screened_relation_same_group_ids": group_related_screened,
        "registered_fixed_exact_assertions": exact_registered,
        "registered_fixed_same_group_relation_ids": same_group_registered,
        "total_screened_links": len(screened.proof_links),
        "all_initial_link_count": len(all_links),
    }


def catalog_cyclic_rule_patterns() -> list[dict]:
    """Catalog templates are candidates, NOT proved or even applicable rules."""
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r6_2_unified_registry_r1.unified_backward_rule_registry import (
        build_unified_backward_rule_registry,
    )

    catalog, _report = build_unified_backward_rule_registry()
    relevant = []
    for entry in catalog.entries():
        statement = entry.rule.conclusion_pattern
        if not isinstance(statement, CyclicStructureStatement):
            continue
        relevant.append({
            "name": entry.rule.name,
            "rule_id": entry.rule_id,
            "order_pattern": repr(statement.order),
            "premise_types": [
                (part.statement_type.__name__ if part.statement_type is not None else None)
                for part in entry.rule.premise_patterns
            ],
            "eligibility": entry.eligibility,
        })
    return relevant


def run_case(name: str, n: int, k: int) -> dict:
    """Rerun an existing public search without changing its semantics."""
    import phase165_r52_r2_search_adapter as search_adapter
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal

    measurement = SearchObservation()
    contexts = []
    original_reconstruct = search_adapter.reconstruct_registered_goal

    def spy(*args, **kwargs):
        return instrument_reconstruction(
            original_reconstruct, args, kwargs, measurement,
        )

    bridge = build_shared_typed_bridge()
    with patch.object(search_adapter, "reconstruct_registered_goal", spy):
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
    context = contexts[-1] if contexts else bridge
    blocked = unique_by_typed_value([
        target for target in measurement.no_option_targets
        if isinstance(target, CyclicStructureStatement) and target.order is not None
    ])
    info = [inspect_cyclic_goal(
        goal, screened=context, registry=bridge.registry,
        all_links=bridge.proof_links,
    ) for goal in blocked]
    classification = classify_blocker(
        status=result.status.value,
        proved=measurement.event_counts["proved"],
        finite_blocked=len(blocked),
        root_options=measurement.root_option_count,
    )
    record = {
        "name": name, "n": n, "k": k,
        "status": result.status.value,
        "result_step_count": len(result.proven_steps),
        "proved_event_count": measurement.event_counts["proved"],
        "unresolved_event_count": measurement.event_counts["unresolved"],
        "root_option_count": measurement.root_option_count,
        "root_rules": list(measurement.root_rule_names),
        "root_goal": repr(measurement.root_goal),
        "context_capture_count": len(contexts),
        "blocked_finite_cyclic_goals": info,
        "blocked_goal_count": len(blocked),
        "context_fixed_source_type_counts": dict(Counter(
            type(link.step.conclusion).__name__
            for link in context.proof_links if link.step is not None
        )),
        "classification": classification,
        "capture_error": None,
    }
    print(name, result.status.value,
          "root_options", measurement.root_option_count,
          "proved", measurement.event_counts["proved"],
          "blocked_finite_cyclic", len(blocked), classification)
    return record


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cases = []
    for name, n, k in CASES:
        try:
            cases.append(run_case(name, n, k))
        except Exception as exc:
            cases.append({
                "name": name, "n": n, "k": k,
                "capture_error": f"{type(exc).__name__}: {exc}",
            })
    catalog = catalog_cyclic_rule_patterns()
    report = {
        "phase": "168 R3-41H",
        "mode": "READ_ONLY_FINITE_CYCLIC_PREMISE_PROVENANCE",
        "cases": cases,
        "registered_cyclic_conclusion_templates": catalog,
        "source_sha256": {
            filename: hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()
            for filename in SOURCES
        },
        "capture_errors": sum(item.get("capture_error") is not None for item in cases),
        "source_inference_not_certified_by_template": True,
        "production_code_modified": False,
        "full_pytest_run": False,
    }
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 168 R3-41H — 有限巡回群の証明前提の接続監査", "",
        "読み取り専用。命題・推論規則・ProofStep は変更しない。", "",
        "| 対象 | 状態 | ProofStep | 根候補 | 展開0件の有限巡回群前提 | 既存の直接引用 | 判定 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for item in cases:
        if item.get("capture_error") is not None:
            lines.append(f'| {item["name"]} | ERROR | - | - | - | - | {item["capture_error"]} |')
            continue
        direct = sum(len(v["screened_exact_given_assertion_ids"])
                     for v in item["blocked_finite_cyclic_goals"])
        lines.append(
            f'| {item["name"]} | {item["status"]} | {item["result_step_count"]} | '
            f'{item["root_option_count"]} | {item["blocked_goal_count"]} | '
            f'{direct} | {item["classification"]} |'
        )
    lines.extend((
        "", "## 判定の境界", "",
        "- 登録済み主張の存在と使用可能な GIVEN、推論規則の適用可能性は異なる。",
        "- 登録済みルールの conclusion_pattern は適用可能性や証明済みを意味しない。",
        "- 後の命題・未接続の主張を証明の前提に加えない。",
        "- 有限巡回群前提への証明が未接続なら、Renderer ではなく探索側の課題。",
        "- 112群全件の検証ではなく、2群の標本監査。",
        "- 全体 pytest は実行しない。", "",
    ))
    (OUTPUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    with ZipFile(OUTPUT / "review_bundle.zip", "w", ZIP_DEFLATED) as archive:
        for filename in ("audit.json", "audit.md"):
            archive.write(OUTPUT / filename, arcname=filename)
    print("CATALOG_FINITE_CYCLIC_TEMPLATES", len(catalog))
    print("CAPTURE_ERRORS", report["capture_errors"])
    print("REPORT", OUTPUT / "audit.md")
    print("UPLOAD_BUNDLE", OUTPUT / "review_bundle.zip")
    print("READ_ONLY: project implementation unchanged; full pytest NOT run")
    if report["capture_errors"]:
        raise SystemExit("R3-41H observed capture errors; inspect report")


if __name__ == "__main__":
    main()
