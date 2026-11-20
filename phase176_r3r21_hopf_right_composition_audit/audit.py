"""R3R21 source-level, read-only audit of the Hopf right-composition frontier."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "phase176_r3r21_hopf_right_composition_audit"
FILES = {
    "hopf_rules.py": ("toda_prop22_right_inference_rule", "hopf_composition_formula_inference_rule", "hopf_composition_law_inference_rule"),
    "tests/test_hopf_rules.py": ("test_hopf_composition_formula", "test_hopf_invariant_reaches_hopf_composition_formula"),
    "phase176_r3r20_cyclic_candidate_boundary/audit.py": ("capture",),
}


def names_in_file(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    return {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


def inspect() -> dict[str, object]:
    findings: dict[str, object] = {}
    for relative, required in FILES.items():
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError("MISSING_FILE: " + relative)
        found = names_in_file(path)
        absent = sorted(set(required) - found)
        if absent:
            raise RuntimeError("MISSING_SYMBOLS: " + relative + ": " + repr(absent))
        findings[relative] = {"symbols": list(required), "present": True}
    source = (ROOT / "hopf_rules.py").read_text(encoding="utf-8-sig")
    right_start = source.index("def toda_prop22_right_inference_rule(")
    right_end = source.index("\ndef ", right_start + 4)
    right = source[right_start:right_end]
    formula_start = source.index("def hopf_composition_formula_inference_rule(")
    formula_end = source.index("\ndef ", formula_start + 4)
    formula = source[formula_start:formula_end]
    checks = {
        "right_formula_uses_suspension_of_gamma": "Suspension(" in right and "expression=gamma" in right,
        "right_formula_uses_actual_h_map": "EHP_H_MAP" in right,
        "right_formula_cites_toda_prop22": "Proposition 2.2" in right,
        "general_formula_requires_hopf_law_premise": "HopfCompositionLawStatement" in formula,
        "general_formula_requires_expression_premise": "statement_type=Expression" in formula,
        "general_formula_suspends_right_factor": "Suspension(" in formula,
    }
    if not all(checks.values()):
        raise RuntimeError("RIGHT_FORMULA_SOURCE_CHANGED: " + repr(checks))
    return {"files": findings, "formula_guards": checks,
            "mathematical_candidate": "H((nu_prime eta_6) eta_7) = (eta_5 eta_6) eta_7",
            "needs_typed_premise_validation": True,
            "needs_hopf_image_order_proof": True,
            "needs_hopf_injectivity_or_kernel_proof": True,
            "needs_cyclic_exhaustion_proof": True,
            "root_proof_complete": False}


def git_value(*args: str) -> str:
    completed = subprocess.run(("git", *args), cwd=ROOT, capture_output=True, text=True, check=True)
    return completed.stdout.strip()


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    directory = base / "EHPProofTracerAudit" / PACKAGE
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "report.json"


def execute(dry_run: bool) -> int:
    report: dict[str, object] = {"phase": "176_R3R21", "dry_run": dry_run,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate": "FAIL_R3R21", "new_given": 0, "new_mathematical_rules": 0,
        "production_changes": 0, "full_pytest": "NOT_RUN"}
    try:
        if Path(git_value("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
            raise RuntimeError("WRONG_REPOSITORY_ROOT")
        if git_value("branch", "--show-current") != "develop":
            raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
        report["head"] = git_value("rev-parse", "HEAD")
        report["inspection"] = inspect()
        report["gate"] = "PASS_R3R21_SOURCE_FRONTIER_ONLY" if not dry_run else "PASS_R3R21_DRYRUN"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    target = report_path()
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R21_GATE=" + str(report["gate"]))
    print("PHASE176_R3R21_HEAD=" + str(report.get("head", "UNVERIFIED")))
    if "error" in report:
        print("PHASE176_R3R21_ERROR=" + str(report["error"]))
    print("PHASE176_R3R21_REPORT=" + str(target))
    print("PHASE176_R3R21_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if str(report["gate"]).startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return execute(args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
