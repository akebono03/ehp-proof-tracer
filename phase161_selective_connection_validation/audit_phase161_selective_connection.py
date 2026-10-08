"""Read-only Phase 161 isolated selective Production connection experiment."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
from proof_repository import ProofRepository, ProofRepositoryEntry
from repository_proof_scope import build_repository_proof_scope
from repository_inference import build_depth_two_producer_search_report, execute_depth_two_producer_search
from rule_catalog import InferenceRuleCatalog, InferenceRuleCatalogEntry
from standard_production_repository import build_standard_production_proof_repository
from standard_production_applicability_catalog import build_standard_production_applicability_catalog

RULE_NAMES = (
    "Toda Proposition 5.1 n=3 Delta injectivity",
    "Toda Proposition 5.3 n=3 Delta injectivity implies Hopf zero",
    "Toda Proposition 5.3 n=3 Hopf zero implies suspension surjective",
    "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity",
    "Toda Proposition 5.3 n=3 Hopf surjective implies Delta zero",
    "Toda Proposition 5.3 n=3 Delta zero implies suspension injective",
    "Toda Proposition 5.3 n=3 suspension isomorphism",
)

def unique_conclusions(steps):
    result = []
    for step in steps:
        if not any(step.conclusion == existing.conclusion for existing in result):
            result.append(step)
    return result

def extract_trace(step):
    selected = {}
    boundaries = []
    seen = set()
    def visit(current):
        identity = id(current)
        if identity in seen:
            return
        seen.add(identity)
        rule = current.inference_rule
        rule_name = getattr(rule, "name", None)
        if rule_name in RULE_NAMES:
            selected.setdefault(rule_name, current)
            for premise in current.premises:
                visit(premise)
        else:
            boundaries.append(current)
    visit(step)
    return selected, unique_conclusions(boundaries)

def main():
    production_repository = build_standard_production_proof_repository()
    production_catalog = build_standard_production_applicability_catalog()
    scope = build_repository_proof_scope(production_repository)
    goal = TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
            target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        )
    )
    candidates = [node for node in scope.nodes if node.proof_step.conclusion == goal]
    traces = [(node, *extract_trace(node.proof_step)) for node in candidates]
    traces.sort(key=lambda item: (len(item[1]), -len(item[2])), reverse=True)
    report = {
        "scope": "Actual Production proof scope and rule instances only; isolated temporary objects; not general goal-only discovery",
        "production_roots": len(production_repository.entries()),
        "production_scope_nodes": len(scope.nodes),
        "production_catalog_entries": len(production_catalog.entries()),
        "matching_goal_nodes_in_ancestry": len(candidates),
        "trace_found": bool(traces),
    }
    if not traces:
        report["outcome"] = "GOAL_NOT_FOUND_IN_PRODUCTION_ANCESTRY"
    else:
        chosen_node, selected, boundaries = traces[0]
        report["selected_trace_rule_names"] = [name for name in RULE_NAMES if name in selected]
        report["missing_trace_rule_names"] = [name for name in RULE_NAMES if name not in selected]
        report["trace_boundary_count"] = len(boundaries)
        report["trace_boundary_types"] = [type(step.conclusion).__name__ for step in boundaries]
        report["trace_boundary_rule_kinds"] = [step.rule.name for step in boundaries]
        report["trace_origin_root"] = chosen_node.root_entry.key
        if len(selected) == 7 and len(boundaries) == 6:
            temporary_repository = ProofRepository()
            for index, step in enumerate(boundaries):
                temporary_repository.register(ProofRepositoryEntry(key=f"phase161.scope.premise.{index}",step=step))
            temporary_catalog = InferenceRuleCatalog()
            for index, name in enumerate(RULE_NAMES):
                rule = selected[name].inference_rule
                original_entries = [entry for entry in production_catalog.entries() if entry.rule.name == name]
                related = [entry for entry in original_entries if entry.rule is rule]
                temporary_catalog.register(InferenceRuleCatalogEntry(
                    key=f"phase161.scope.rule.{index}",
                    rule=rule,
                    conclusion_type=type(selected[name].conclusion),
                    fixed_point_safe=True,
                    goal_compatibility=lambda requested, expected=selected[name].conclusion: requested == expected,
                ))
                report.setdefault("selected_rule_evidence", []).append({
                    "name":name,
                    "actual_production_catalog_entries":len(original_entries),
                    "same_identity_as_catalog_entry":bool(related),
                    "temporary_search_eligibility_only":True,
                })
            depth_records=[]
            for depth in (2,3,4):
                item={"max_depth":depth}
                try:
                    search=build_depth_two_producer_search_report(temporary_repository,temporary_catalog,goal,max_depth=depth)
                    item["search_status"]=search.status.value
                    item["producer_nodes"]=len(search.search_result.producer_nodes) if search.search_result else 0
                    execution=execute_depth_two_producer_search(temporary_repository,temporary_catalog,goal,max_depth=depth)
                    item["execution_status"]=execution.report.status.value
                    item["goal_derived"]=bool(execution.repository_inference_result and execution.repository_inference_result.goal_step)
                except Exception as exc:
                    item["exception_type"]=type(exc).__name__
                    item["exception_message"]=str(exc)
                depth_records.append(item)
            report["depth_results"]=depth_records
            report["outcome"]="ISOLATED_EXECUTION_EVALUATED"
        else:
            report["outcome"]="PRODUCTION_TRACE_DIFFERS_FROM_PHASE59_SEVEN_RULE_SIX_PREMISE_SHAPE"
    report["limitations"]=[
        "Temporary fixed_point_safe=True is only an isolated opt-in experiment, not a safety certification.",
        "No mutation of the production repository, production catalog or persistent files.",
        "Selecting facts/rules from an existing proof ancestry is not independent discovery from goal alone.",
        "This run does not perform full pytest.",
    ]
    output=ROOT / "phase161_selective_connection_validation.json"
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    print("Wrote:",output)

if __name__=="__main__":
    main()
