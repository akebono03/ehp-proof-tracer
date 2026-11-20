"""Read-only audit of nested compositions and the cited right Hopf formula."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = "phase176_r3r23_hopf_composition_type_audit"
ROOT = Path(__file__).resolve().parent.parent
ANCHORS = {
    "expression.py": "class Composition(Expression):",
    "phase171_r2h_prop22_cited_hopf/source.py": "def _formula_parts(",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "def expression_endpoints(",
    "phase174_r3_r7_r9_composition_associativity/rule.py": "def typed_composition_factors(",
    "phase171_r2i_eta_hopf_bridge/source.py": "def eligible_eta_hopf_chains(",
    "phase175_r3_pi73_hopf_lift/rule.py": "def expand_cited_hopf_lift(",
    "tests/test_hopf_rules.py": "def test_hopf_composition_formula(",
    "phase174_r3_r7_r9_composition_associativity/tests/test_rule.py": "def test_generic_reassociation_preserves_factors_and_map(",
}


def inspect_source(root: Path) -> dict[str, bool]:
    result = {}
    for name, anchor in ANCHORS.items():
        path = root / name
        if not path.is_file() or anchor not in path.read_text(encoding="utf-8-sig"):
            raise RuntimeError("SOURCE_ANCHOR_MISSING: " + name)
        result[name] = True
    return result


def git_state(root: Path) -> dict[str, str]:
    def git(*args: str) -> str:
        p = subprocess.run(("git", *args), cwd=root, capture_output=True, text=True)
        if p.returncode:
            raise RuntimeError("GIT_FAILED: " + p.stderr.strip())
        return p.stdout.strip()
    if Path(git("rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    return {"head": git("rev-parse", "HEAD"), "branch": "develop"}


def inspect_runtime() -> dict[str, object]:
    from expression import Composition, HomotopyElement, MapApplication, Suspension
    from map_facts import EHP_H_MAP
    from proof import Relation, RelationType
    from phase171_r2h_prop22_cited_hopf.source import (
        _formula_parts, expand_cited_prop22_right_formula, TodaProp22RightFormula,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors

    # Abstract typed stand-ins, not assertions about actual homotopy elements.
    a = HomotopyElement("a", 3, source=6, target=3)
    b = HomotopyElement("b", 6, source=7, target=6)
    c = HomotopyElement("c", 7, source=8, target=7)
    alpha = Composition(a, b)
    nested = Composition(alpha, c)
    right = Composition(a, Composition(b, c))
    gamma = HomotopyElement("gamma", 6, source=7, target=6)
    suspended = Suspension(gamma)
    candidate = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, suspended)),
        Composition(MapApplication(EHP_H_MAP, alpha), suspended),
        RelationType.EQUALITY,
    )
    simple_left = HomotopyElement("simple", 3, source=7, target=3)
    one = Composition(simple_left, suspended)
    simple = Relation(
        MapApplication(EHP_H_MAP, one),
        Composition(MapApplication(EHP_H_MAP, simple_left), suspended),
        RelationType.EQUALITY,
    )
    return {
        "abstract_standins_only": True,
        "alpha_endpoints": expression_endpoints(alpha),
        "nested_endpoints": expression_endpoints(nested),
        "right_associated_endpoints": expression_endpoints(right),
        "alpha_builtin_compatible": alpha.is_type_compatible(),
        "nested_builtin_compatible": nested.is_type_compatible(),
        "right_builtin_compatible": right.is_type_compatible(),
        "typed_factors_preserved": typed_composition_factors(nested) == typed_composition_factors(right),
        "candidate_formula_recognized": _formula_parts(candidate) is not None,
        "candidate_formula_expansions": len(expand_cited_prop22_right_formula(candidate, (TodaProp22RightFormula(),))),
        "simple_formula_recognized": _formula_parts(simple) is not None,
        "simple_formula_expansions": len(expand_cited_prop22_right_formula(simple, (TodaProp22RightFormula(),))),
        "hopf_image_proved": False,
        "root_proof_complete": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    return base / "report.json"


def execute(dry_run: bool) -> int:
    report = {"phase": "176_R3R23", "dry_run": dry_run, "gate": "FAIL_R3R23", "full_pytest": "NOT_RUN", "new_given": 0, "new_mathematical_rules": 0}
    try:
        report.update(git_state(ROOT))
        report["source_guard"] = inspect_source(ROOT)
        if dry_run:
            report["gate"] = "PASS_R3R23_DRYRUN"
        else:
            v = inspect_runtime()
            report["observed"] = v
            if not (v["alpha_endpoints"] == (7, 3)
                    and v["nested_endpoints"] == (8, 3)
                    and v["right_associated_endpoints"] == (8, 3)
                    and v["typed_factors_preserved"]
                    and not v["nested_builtin_compatible"]
                    and not v["candidate_formula_recognized"]
                    and v["candidate_formula_expansions"] == 0
                    and v["simple_formula_recognized"]
                    and v["simple_formula_expansions"] == 1):
                raise RuntimeError("FRONTIER_CHANGED_REVIEW_REQUIRED")
            report["gate"] = "PASS_R3R23_TYPED_BOUNDARY_AUDITED"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    path = report_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("PHASE176_R3R23_GATE=" + report["gate"])
    print("PHASE176_R3R23_HEAD=" + str(report.get("head", "UNVERIFIED")))
    for key, val in report.get("observed", {}).items():
        print("PHASE176_R3R23_" + key.upper() + "=" + str(val))
    if "error" in report:
        print("PHASE176_R3R23_ERROR=" + report["error"])
    print("PHASE176_R3R23_REPORT=" + str(path))
    print("PHASE176_R3R23_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return execute(args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
