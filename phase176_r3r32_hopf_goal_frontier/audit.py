"""Read-only Phase 176 R3R32 inspection of the local Hopf proof frontier."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = (
    "hopf_rules.py",
    "tests/test_hopf_rules.py",
    "phase165_r52_r9_shared_math.py",
)
OPTIONAL_MARKERS = (
    "phase176_r3r31",
    "phase176_r3r31r1",
)


def function_names(source: str) -> list[str]:
    tree = ast.parse(source)
    return [node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]


def review_file(root: Path, name: str) -> dict:
    path = root / name
    if not path.is_file():
        return {"file": name, "present": False}
    source = path.read_text(encoding="utf-8-sig")
    try:
        names = function_names(source)
        parse_error = None
    except SyntaxError as exc:
        names = []
        parse_error = f"{exc.msg} at line {exc.lineno}"
    return {
        "file": name,
        "present": True,
        "syntax_error": parse_error,
        "function_names": names,
        "indicators": {
            "toda_prop22_right": "toda_prop22_right_inference_rule" in source,
            "hopf_composition_formula": "hopf_composition_formula_inference_rule" in source,
            "shared_expansion_provider": "shared_expansion_provider" in source,
            "phase176_r3r31": "phase176_r3r31" in source,
            "nu_hopf_source": "build_adopted_toda53_hopf_reference" in source,
        },
    }


def git_status(root: Path) -> dict:
    cmds = {
        "branch": ["git", "branch", "--show-current"],
        "head": ["git", "rev-parse", "HEAD"],
        "status": ["git", "status", "--short"],
        "diff_check": ["git", "diff", "--check"],
    }
    out = {}
    for key, cmd in cmds.items():
        p = subprocess.run(cmd, cwd=root, text=True, capture_output=True, check=False)
        out[key] = {"returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    return out


def make_report(root: Path) -> dict:
    files = [review_file(root, name) for name in REQUIRED]
    hopf = files[0]
    return {
        "phase": "176 R3R32",
        "mode": "READ_ONLY_LOCAL_FRONTIER_AUDIT",
        "root": str(root),
        "git": git_status(root),
        "files": files,
        "existing_phase_directories": sorted(p.name for p in root.iterdir() if p.is_dir() and any(p.name.startswith(m) for m in OPTIONAL_MARKERS)),
        "goals": [
            "H(nu_prime eta_6^2) = eta_5^3",
            "eta_5^3 = 4 nu_5",
        ],
        "verified_by_this_audit": {
            "repository_files_present": all(x["present"] for x in files),
            "repository_files_parse": all(x.get("syntax_error") is None for x in files if x["present"]),
            "hopf_right_rule_definition_present": hopf["indicators"]["toda_prop22_right"] if hopf["present"] else False,
            "proof_completed": False,
            "group_structure_completed": False,
        },
        "next_checks": [
            "Inspect R3R31 local provider candidate shape for the exact Hopf goal",
            "Check typed Suspension(eta_5 squared) versus eta_6 squared",
            "Check cited Toda (5.3) Hopf premise admission to the current root",
            "Check cited Toda (5.5) n=5 rewrite and equality transitivity",
            "Do not conclude group order from a Hopf image alone",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    report = make_report(root)
    ok = report["verified_by_this_audit"]["repository_files_present"] and report["verified_by_this_audit"]["repository_files_parse"]
    if not args.dry_run:
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerAudit" / "phase176_r3r32_hopf_goal_frontier"
        base.mkdir(parents=True, exist_ok=True)
        target = base / "report.json"
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("REPORT=" + str(target))
    print("PHASE176_R3R32_GATE=" + ("PASS_READ_ONLY_FRONTIER_COLLECTED" if ok else "FAIL_REQUIRED_SOURCE_MISSING_OR_SYNTAX"))
    print("PHASE176_R3R32_PROOF_COMPLETED=False")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
