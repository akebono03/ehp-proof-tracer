"""Isolated source-first probe, independent of public shared search wiring."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement,
    build_cited_toda55_quadruple_source,
    canonical_quadruple_goal,
    expand_cited_quadruple,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r27r1_toda55_quadruple_isolated"


def checked_head() -> str:
    def git(*args: str) -> str:
        proc = subprocess.run(("git", *args), cwd=ROOT, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
        if proc.returncode:
            raise RuntimeError("git error: " + proc.stderr)
        return proc.stdout.strip()
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT:
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    return git("rev-parse", "HEAD")


def capture() -> dict[str, object]:
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase169_r10d2_general_family_definition.family_citation import CitedStableFamilyDefinition
    from proof import ProofRule
    bridge = build_cited_toda55_quadruple_source()
    citation = bridge.proof_links[0].step.conclusion
    assert citation == Toda55UniversalQuadrupleStatement()
    goal = canonical_quadruple_goal(5)
    if goal is None:
        raise RuntimeError("NU5_CANONICAL_GOAL_MISSING")
    family = CitedStableFamilyDefinition(4, 4, 3)
    available = (citation, family, TodaEtaFamilyGeneralDefinition())
    proposals = expand_cited_quadruple(goal, available)
    if len(proposals) != 1 or len(proposals[0].subgoals) != 3:
        raise RuntimeError("ISOLATED_CANDIDATE_MISSING")
    if any(isinstance(child, ProofRule) for child in proposals[0].subgoals):
        raise RuntimeError("UNEXPECTED_PROOF_OBJECT")
    return {
        "source_assertion_count": len(bridge.proof_links),
        "source_statement": repr(citation),
        "nu5_goal": repr(goal),
        "isolated_candidate_count": len(proposals),
        "candidate_rule": proposals[0].rule.name,
        "candidate_children": [repr(child) for child in proposals[0].subgoals],
        "public_provider_modified": False,
        "isolated_candidate_is_proof": False,
        "nu5_quadruple_proved": False,
        "root_pi83_proved": False,
        "new_direct_group_given": 0,
        "full_pytest": "NOT_RUN",
    }


def report_path() -> Path:
    parent = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    path = parent / "EHPProofTracerAudit" / PACKAGE
    path.mkdir(parents=True, exist_ok=True)
    return path / "report.json"


def execute(dry_run: bool) -> int:
    result: dict[str, object] = {
        "phase": "176_R3R27R1", "gate": "FAIL_R3R27R1",
        "full_pytest": "NOT_RUN", "public_provider_modified": False,
    }
    try:
        result["head"] = checked_head()
        if dry_run:
            result["gate"] = "PASS_R3R27R1_DRYRUN"
        else:
            result["observed"] = capture()
            result["gate"] = "PASS_R3R27R1_CITED_QUADRUPLE_ISOLATED"
    except Exception as exc:
        result["error"] = type(exc).__name__ + ": " + str(exc)
    path = report_path()
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R27R1_GATE=" + str(result["gate"]))
    print("PHASE176_R3R27R1_HEAD=" + str(result.get("head", "UNVERIFIED")))
    if "observed" in result:
        for key, value in result["observed"].items():
            print("PHASE176_R3R27R1_" + key.upper() + "=" + str(value))
    if "error" in result:
        print("PHASE176_R3R27R1_ERROR=" + str(result["error"]))
    print("PHASE176_R3R27R1_REPORT=" + str(path))
    print("PHASE176_R3R27R1_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if str(result["gate"]).startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return execute(parser.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())
