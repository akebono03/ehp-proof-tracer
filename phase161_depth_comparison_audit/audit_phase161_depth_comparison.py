"""Read-only depth comparison for the Phase 59 seeded EHP proof."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from proof_repository import ProofRepository, ProofRepositoryEntry
from repository_inference import (
    build_depth_two_producer_search_report,
    execute_depth_two_producer_search,
)
from rule_catalog import InferenceRuleCatalog, InferenceRuleCatalogEntry
from test_phase59_n3_ehp_chain import build_phase59_3_data


def main():
    data = build_phase59_3_data()
    repository = ProofRepository()
    for index, step in enumerate(data["premise_steps"]):
        repository.register(
            ProofRepositoryEntry(
                key=f"phase161.depth.premise.{index}",
                step=step,
                phase="161",
                theorem="read-only depth comparison",
            )
        )
    catalog = InferenceRuleCatalog()
    for index, rule in enumerate(data["rules"]):
        matches = [
            step for step in data["result"].steps
            if getattr(step, "inference_rule", None) is rule
        ]
        if not matches:
            raise RuntimeError(f"Missing Phase 59 step for {rule.name}")
        catalog.register(
            InferenceRuleCatalogEntry(
                key=f"phase161.depth.rule.{index}",
                rule=rule,
                conclusion_type=type(matches[0].conclusion),
                fixed_point_safe=True,
            )
        )
    goal = data["expected_suspension_isomorphism"]
    rows = []
    for max_depth in (2, 3, 4):
        row = {"max_depth": max_depth}
        try:
            report = build_depth_two_producer_search_report(
                repository, catalog, goal, max_depth=max_depth
            )
            row["search_status"] = report.status.name
            row["producer_nodes"] = (
                len(report.search_result.producer_nodes)
                if report.search_result is not None else 0
            )
            row["producer_rules"] = (
                [node.producer_rule.name for node in report.search_result.producer_nodes]
                if report.search_result is not None else []
            )
            execution = execute_depth_two_producer_search(
                repository, catalog, goal, max_depth=max_depth
            )
            row["execution_status"] = execution.report.status.name
            inferred = execution.repository_inference_result
            row["goal_derived"] = (
                inferred.goal_step is not None
                and inferred.goal_step.conclusion == goal
            ) if inferred is not None else False
            row["execution_result_available"] = inferred is not None
        except Exception as exc:
            row["error_type"] = type(exc).__name__
            row["error"] = str(exc)
        rows.append(row)
    result = {
        "scope": "Phase 59 seeded premise/rule catalog only; not production goal-only proof search",
        "goal_type": type(goal).__name__,
        "initial_premises": len(data["premise_steps"]),
        "registered_rules": len(data["rules"]),
        "depth_comparison": rows,
    }
    output = ROOT / "phase161_depth_comparison_audit.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Wrote: {output}")


if __name__ == "__main__":
    main()
