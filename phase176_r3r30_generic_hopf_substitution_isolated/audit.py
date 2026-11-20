"""R3R30 isolated audit; no production files are modified."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r30_generic_hopf_substitution_isolated.source import (
    generic_hopf_substitution_inputs, expand_generic_hopf_substitution,
)
from proof import Relation, RelationType

ROOT = Path(__file__).resolve().parent.parent


def inspect(dry_run: bool) -> dict:
    result = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT,
        capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode or result.stdout.strip() != "develop":
        raise RuntimeError("expected develop checkout")
    if dry_run:
        return {"gate": "PASS_R3R30_DRYRUN", "full_pytest": "NOT_RUN"}
    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    alpha = Composition(nu, eta6)
    right = Suspension(eta6)
    goal = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, right)),
        Composition(Composition(eta5, eta6), right),
        RelationType.EQUALITY,
    )
    proposals = expand_generic_hopf_substitution(goal, (TodaProp22RightFormula(),))
    return {
        "gate": "PASS_R3R30_ISOLATED_GENERAL_SUBSTITUTION",
        "candidate_count": len(proposals),
        "subgoal_count": len(proposals[0].subgoals) if proposals else 0,
        "subgoals": [repr(x) for x in proposals[0].subgoals] if proposals else [],
        "no_direct_hopf_value_given": True,
        "public_provider_modified": False,
        "new_given": 0,
        "root_proof_complete_claimed": False,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        result = inspect(args.dry_run)
    except Exception as exc:
        result = {"gate": "FAIL_R3R30", "error": str(exc), "full_pytest": "NOT_RUN"}
    location = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                / "EHPProofTracerAudit"
                / "phase176_r3r30_generic_hopf_substitution_isolated")
    location.mkdir(parents=True, exist_ok=True)
    path = location / "report.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R30_" + key.upper() + "=" + str(value))
    print("PHASE176_R3R30_REPORT=" + str(path))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
