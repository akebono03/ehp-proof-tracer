"""Read-only Phase 166 R3-AD audit of generic stable transport."""
from __future__ import annotations

import json
from pathlib import Path

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaPrimaryGroup
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule
from toda_rules import Toda45IsomorphismStatement
from toda_stable_group_transport import toda_45_generic_finite_cyclic_transport_inference_rule


def audit_structural_transport():
    """Probe all stems using typed finite-cyclic examples, never assert sources exist."""
    rule = toda_45_generic_finite_cyclic_transport_inference_rule()
    cases = []
    for k in (1, 2, 3, 7):
        for r in (1, 2, 3, 7):
            n = k + 2
            from expression import GeneratorSymbol, HomotopyElement
            alpha = HomotopyElement(name=f"audit_{k}_{n}", dimension=n,
                                    source=n + k, target=n,
                                    generator=GeneratorSymbol(family="audit", index=n))
            source = TodaPrimaryGroup(n + k, n)
            target = TodaPrimaryGroup(n + k + r, n + r)
            group = Relation(source, FiniteCyclicGroup(2, alpha), RelationType.EQUALITY)
            iso = Toda45IsomorphismStatement(TodaIteratedSuspensionMap(r, source, target))
            steps = (ProofStep(group, (), ProofRule.GIVEN), ProofStep(iso, (), ProofRule.GIVEN))
            matches = find_inference_matches_for_rule(rule, steps)
            conclusion = rule.conclusion_builder(steps) if matches else None
            cases.append({"k": k, "r": r, "inference_matches": len(matches),
                          "correct_target": conclusion is not None and conclusion.lhs == target,
                          "correct_generator": conclusion is not None and
                          conclusion.rhs.generator == IteratedSuspension(alpha, r),
                          "note": "Synthetic premises test the inference rule only; not literary eligibility"})
    return cases


def audit_real_eta():
    bridge = build_shared_typed_bridge()
    reports = []
    for n in (4, 5, 6, 7):
        candidates = registered_group_goal_candidates(bridge, n=n, k=1)
        record = {"n": n, "stem": 1, "candidate_count": len(candidates)}
        if len(candidates) != 1:
            reports.append(record)
            continue
        goal = candidates[0]
        citing = resolve_specialized_goal_citing_id(bridge, goal)
        record["citing_assertion_id"] = citing
        if citing is None:
            reports.append(record)
            continue
        context = screen_shared_proof_context(bridge, goal=goal,
            citing_assertion_id=citing, explicit_publication_target=True)
        available = tuple(link.step.conclusion for link in context.proof_links
                          if link.step is not None and link.step.rule is ProofRule.GIVEN)
        source = [x for x in available if isinstance(x, Relation) and
                  x.lhs == TodaPrimaryGroup(4, 3) and isinstance(x.rhs, FiniteCyclicGroup)]
        general = [x for x in available if isinstance(x, Toda45IsomorphismStatement)]
        exp = n - 3
        related = []
        if source:
            transported = Relation(goal.lhs, FiniteCyclicGroup(source[0].rhs.order,
                                   IteratedSuspension(source[0].rhs.generator, exp)), RelationType.EQUALITY)
            related = expand_registered_toda45_finite_cyclic_goal(transported, available)
        record.update({"base_count": len(source), "toda45_count": len(general),
                       "transport_options": len(related),
                       "transport_rules": [x.rule.name for x in related]})
        result = search_group_from_registered_goal(n=n, k=1, bridge=bridge)
        record.update({"status": str(result.status), "complete": str(result.status).endswith(".COMPLETE"),
                       "open_goals": len(result.open_goals), "diagnostics": [str(x) for x in result.diagnostics]})
        reports.append(record)
    return reports


def main():
    report = {"phase": "166 R3-AD", "production_code_modified": False,
              "full_pytest_run": False, "structural_cases": audit_structural_transport(),
              "real_eta": audit_real_eta(),
              "higher_stems": "No registered named generator correspondence assumed; generic rule only"}
    output = Path(__file__).with_name("report.json")
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"structural_pass": sum(x["inference_matches"] == 1 and x["correct_target"] and x["correct_generator"] for x in report["structural_cases"]),
                      "structural_total": len(report["structural_cases"]), "real_eta": report["real_eta"],
                      "report": str(output)}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
