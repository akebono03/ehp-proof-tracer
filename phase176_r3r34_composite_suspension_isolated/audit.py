"""Read-only R3R34 dependency and frontier report."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "phase176_r3r34_composite_suspension_isolated"


def preflight() -> dict:
    command = subprocess.run(("git", "branch", "--show-current"), cwd=ROOT,
                             capture_output=True, text=True)
    if command.returncode or command.stdout.strip() != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    paths = (
        "phase171_r2h_prop22_cited_hopf/source.py",
        "phase165_r12_r21_eta_generator_chain.py",
        "phase176_r3r30_generic_hopf_substitution_isolated/source.py",
        "phase165_r52_r9_shared_math.py",
    )
    for path in paths:
        if not (ROOT / path).is_file():
            raise RuntimeError("MISSING_DEPENDENCY: " + path)
    return {"develop": True, "required_sources": list(paths)}


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Suspension
    from proof import Relation, RelationType
    from phase176_r3r34_composite_suspension_isolated.source import (
        expand_composite_suspension_equality,
    )
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    e5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    e6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    e7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    goal = Relation(Suspension(Composition(e5, e6)), Composition(e6, e7), RelationType.EQUALITY)
    branch = expand_composite_suspension_equality(goal)
    if len(branch) != 1:
        raise RuntimeError("ISOLATED_BRANCH_NOT_FOUND")
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    provider = shared_expansion_provider(screened, proof_target=roots[0])
    image = branch[0].subgoals[0]
    return {
        "isolated_rule": branch[0].rule.name,
        "isolated_subgoals": len(branch[0].subgoals),
        "existing_image_candidate_rules": [x.rule.name for x in provider(image)],
        "existing_equality_candidate_rules": [x.rule.name for x in provider(goal)],
        "shared_provider_modified": False,
        "proof_completed": False,
        "root_group_proved": False,
    }


def run(dry_run: bool) -> int:
    report = {"gate": "FAIL_R3R34", "full_pytest": "NOT_RUN", "new_given": 0,
              "production_modified": False}
    try:
        report["preflight"] = preflight()
        if dry_run:
            report["gate"] = "PASS_R3R34_DRYRUN"
        else:
            report["frontier"] = probe()
            report["gate"] = "PASS_R3R34_ISOLATED_BRIDGE_NOT_CONNECTED"
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / "report.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R34_GATE=" + report["gate"])
    for key, value in report.get("frontier", {}).items():
        print("PHASE176_R3R34_" + key.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R34_ERROR=" + report["error"])
    print("REPORT=" + str(output))
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
