from __future__ import annotations
import ast
import csv
import json
from pathlib import Path

FILES = (
    "tests/test_phase49_probe.py",
    "tests/test_phase56_probe.py",
    "tests/test_phase56_pi_i_minus_1_1_zero.py",
    "tests/test_phase56_prop44_eta2_specialization.py",
    "tests/test_phase56_prop44_second_summand_restriction.py",
    "tests/test_phase56_toda52_composition_isomorphism.py",
)
# Classification is deliberately conservative: no test is automatically retired.
CHRONOLOGY_NAMES = (
    "round_one", "round_two", "round_three", "round_four",
    "round_five", "round_six", "last_round",
    "fixed_point_in_one_round", "fixed_point_in_six_rounds",
)
MATHEMATICAL_NAMES = (
    "generator", "eta2", "eta_2", "hopf", "isomorphism",
    "zero", "map", "composition", "premise", "provenance",
    "restriction", "source", "target", "relation",
    "injectivity", "surjectivity", "derived", "inference",
    "wrong", "rejects", "scope", "formula",
)
def classify(name: str) -> tuple[str, str]:
    if any(token in name for token in CHRONOLOGY_NAMES):
        return ("CHRONOLOGY_REVIEW", "Historical inference round ordering; compare current trace before deciding retirement")
    if any(token in name for token in MATHEMATICAL_NAMES):
        return ("MATH_COVERAGE_REQUIRED", "Mathematical content or premise/provenance guard; must preserve or migrate")
    return ("MANUAL_REVIEW", "Cannot establish equivalent coverage from test name alone")

def main() -> None:
    project = Path.cwd()
    out = project / "phase165_r6_audit_results" / "legacy83_classification"
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for rel in FILES:
        path = project / rel
        if not path.is_file():
            raise FileNotFoundError(f"Required historical test missing: {rel}")
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                label, reason = classify(node.name)
                records.append(dict(file=rel, name=node.name, line=node.lineno,
                                    category=label, reason=reason, retirement_approved=False))
    if len(records) != 83:
        raise ValueError(f"Expected 83 historical test functions, found {len(records)}; no report published")
    with (out / "classification.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer=csv.DictWriter(f, fieldnames=tuple(records[0]))
        writer.writeheader()
        writer.writerows(records)
    categories={key:sum(r["category"]==key for r in records)
                for key in ("CHRONOLOGY_REVIEW","MATH_COVERAGE_REQUIRED","MANUAL_REVIEW")}
    report={"status":"CLASSIFIED_NO_RETIREMENT", "tests":len(records),
            "files":len(FILES), "categories":categories,
            "retirement_approved":0, "coverage_equivalence_verified":False,
            "existing_tests_modified":0, "production_files_modified":0,
            "full_pytest_run":False,
            "csv":str(out / "classification.csv")}
    (out/"summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
