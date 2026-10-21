from __future__ import annotations
import json
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "r3_report.json"

def run():
    from phase165_r12_r4_pi43_search.audit import target_goal
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r57_r10_step_narrative import ordered_proof_ancestry
    from proof import ProofRule

    goal = target_goal()
    result = search_group_from_registered_goal(n=3, k=1)
    complete = result.status is ProofSearchStatus.COMPLETE
    roots = [s for s in result.proven_steps if s.conclusion == goal and s.rule is ProofRule.INFERENCE]
    problems = []
    if not complete: problems.append("Search result not COMPLETE")
    if len(roots) != 1: problems.append(f"Expected one derived root, found {len(roots)}")
    ancestry = ordered_proof_ancestry(roots[0]) if len(roots) == 1 else ()
    identifiers = {id(s): i + 1 for i,s in enumerate(ancestry)}
    registered = {id(s) for s in result.proven_steps}
    rows=[]
    publication_status=[]
    for index,step in enumerate(ancestry,1):
        rule = step.inference_rule
        lit = getattr(rule,"literature_reference",None)
        locator = getattr(lit,"locator",None)
        dependencies = []
        for premise in step.premises:
            pid=identifiers.get(id(premise))
            dependencies.append(pid)
            if pid is None or pid >= index:
                problems.append(f"Step {index} has unresolved/forward premise")
        if id(step) not in registered:
            problems.append(f"Step {index} missing from proven_steps")
        if step.rule is ProofRule.INFERENCE and (rule is None or not getattr(rule,"name",None)):
            problems.append(f"Step {index} has missing inference rule")
        if step.rule is ProofRule.GIVEN and (step.premises or not locator):
            problems.append(f"Step {index} has invalid GIVEN ancestry or missing locator")
        position_candidates={}
        for obj_name,obj in (("rule",rule),("reference",lit),("step",step)):
            if obj is None: continue
            for field in ("publication_position","component_position","source_assertion_id"):
                value=getattr(obj,field,None)
                if value is not None: position_candidates[obj_name+"."+field]=repr(value)
        if step.rule is ProofRule.GIVEN:
            publication_status.append({"step":index,"locator":locator,
                                      "position_metadata":position_candidates,
                                      "verified":bool(position_candidates)})
        rows.append({
            "step":index,
            "kind":step.rule.value,
            "rule":getattr(rule,"name",None),
            "locator":locator,
            "conclusion_type":type(step.conclusion).__name__,
            "conclusion":repr(step.conclusion),
            "premises":dependencies,
            "position_metadata":position_candidates,
        })
    names=[s["rule"] or "" for s in rows]
    required=(
        "first isomorphism theorem for generated kernel",
        "infinite cyclic quotient structure",
        "finite cyclic structure gives group relation",
    )
    for name in required:
        if name not in names: problems.append("Required inference absent: "+name)
    report={
        "phase":"167 R3",
        "mode":"READ_ONLY_PROOFSTEP_STRUCTURE",
        "target":"pi_4^3",
        "status":result.status.value,
        "search_entry":"phase165_r55_nk_only_goal.search_group_from_registered_goal",
        "diagnostics":list(result.diagnostics),
        "conclusion_matches_goal": result.conclusion == goal,
        "proven_step_count":len(result.proven_steps),
        "ancestry_count":len(ancestry),
        "root_is_derived":len(roots)==1,
        "all_premises_precede_dependents":not any("premise" in p for p in problems),
        "given_count":sum(s.rule is ProofRule.GIVEN for s in ancestry),
        "publication_metadata_in_proofstep":publication_status,
        "publication_order_verification":"NOT_VERIFIED_FROM_PROOFSTEP_METADATA",
        "semantic_forward_replay":"NOT_PERFORMED",
        "problems":problems,
        "steps":rows,
        "scope_notes":[
            "A structural dependency audit does not prove semantic correctness of inference rules.",
            "Literature publication ordering may be stored in an external registry; absence of fields in ProofStep does not imply ordering failure.",
            "No repository source files or existing tests are changed.",
        ],
        "full_pytest_run":False,
    }
    OUTPUT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({key:report[key] for key in (
        "mode","status","search_entry","diagnostics","conclusion_matches_goal","proven_step_count",
        "ancestry_count","root_is_derived","given_count",
        "publication_order_verification","semantic_forward_replay","problems"
    )},ensure_ascii=False,indent=2))
    print("REPORT:",OUTPUT)
if __name__ == "__main__":
    try: run()
    except Exception:
        OUTPUT.write_text(json.dumps({"error":traceback.format_exc()},ensure_ascii=False,indent=2),encoding="utf-8")
        raise
