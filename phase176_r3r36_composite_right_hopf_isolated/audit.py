"""R3R36 source-first, read-only audit of composite-right Hopf expansions."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = "phase176_r3r36_composite_right_hopf_isolated"
ROOT = Path(__file__).resolve().parent.parent
SOURCES = {
    "phase171_r2h_prop22_cited_hopf/source.py": (
        "class TodaProp22RightFormula:",
        "def _formula_parts(",
    ),
    "phase176_r3r30_generic_hopf_substitution_isolated/source.py": (
        "def generic_hopf_substitution_inputs(",
    ),
    "phase176_r3r34_composite_suspension_isolated/source.py": (
        "def composite_suspension_equality_input(",
    ),
    "phase165_r52_r9_shared_math.py": (
        "options.extend(expand_composite_suspension_equality(goal))",
    ),
}


def run_git(*args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
    )
    if completed.returncode:
        raise RuntimeError("GIT_FAILED: " + completed.stderr.strip())
    return completed.stdout.strip()


def preflight() -> dict:
    if str(Path(run_git("rev-parse", "--show-toplevel")).resolve()).casefold() != str(ROOT.resolve()).casefold():
        raise RuntimeError("WRONG_REPOSITORY")
    if run_git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    for relative, signatures in SOURCES.items():
        file = ROOT / relative
        if not file.is_file():
            raise RuntimeError("DEPENDENCY_MISSING: " + relative)
        source = file.read_text(encoding="utf-8-sig")
        if not all(signature in source for signature in signatures):
            raise RuntimeError("DEPENDENCY_SIGNATURE_CHANGED: " + relative)
    return {"head": run_git("rev-parse", "HEAD"), "dependency_guards": len(SOURCES)}


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
    from map_facts import EHP_H_MAP
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r36_composite_right_hopf_isolated.source import (
        COMPOSITE_FORMULA_RULE_NAME,
        COMPOSITE_SUBSTITUTION_RULE_NAME,
        composite_right_formula_parts,
        composite_hopf_substitution_inputs,
        expand_cited_composite_right_hopf,
    )
    from proof import (
        ProofRule, Relation, RelationType, apply_inference_match, find_inference_match,
    )
    from unified_statement_registry import AssertionOrigin

    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    right = Suspension(Composition(eta5, eta6))
    composite = Composition(nu, right)
    formula = Relation(
        MapApplication(EHP_H_MAP, composite),
        Composition(MapApplication(EHP_H_MAP, nu), right),
        RelationType.EQUALITY,
    )
    substituted = Relation(
        formula.lhs, Composition(eta5, right), RelationType.EQUALITY,
    )
    hopf = Relation(MapApplication(EHP_H_MAP, nu), eta5, RelationType.EQUALITY)
    if composite_right_formula_parts(formula) != (nu, right.expression):
        raise RuntimeError("COMPOSITE_FORMULA_NOT_RECOGNIZED")
    if composite_hopf_substitution_inputs(substituted) != (formula, hopf):
        raise RuntimeError("COMPOSITE_SUBSTITUTION_NOT_RECOGNIZED")

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    source_steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    available = tuple(step.conclusion for step in source_steps)
    formula_candidates = expand_cited_composite_right_hopf(formula, available)
    substitution_candidates = expand_cited_composite_right_hopf(substituted, available)
    if (len(formula_candidates) != 1
            or formula_candidates[0].rule.name != COMPOSITE_FORMULA_RULE_NAME
            or len(substitution_candidates) != 1
            or substitution_candidates[0].rule.name != COMPOSITE_SUBSTITUTION_RULE_NAME
            or substitution_candidates[0].subgoals != (formula, hopf)):
        raise RuntimeError("ISOLATED_CANDIDATE_CONTRACT_FAILURE")

    universal = next((step for step in source_steps
                      if step.conclusion == TodaProp22RightFormula()), None)
    hopf_source = next((step for step in source_steps
                        if step.conclusion == hopf), None)
    formula_step = None
    substituted_step = None
    if universal is not None:
        match = find_inference_match(formula_candidates[0].rule, (universal,))
        if match is not None:
            formula_step = apply_inference_match(match)
    if formula_step is not None and hopf_source is not None:
        match = find_inference_match(
            substitution_candidates[0].rule,
            (formula_step, hopf_source),
        )
        if match is not None:
            substituted_step = apply_inference_match(match)

    existing_provider = shared_expansion_provider(screened, proof_target=roots[0])
    return {
        "gate": "PASS_R3R36_ISOLATED_CANDIDATES_AUDITED_NOT_PUBLIC",
        "root": repr(roots[0]),
        "screened_prop22_count": available.count(TodaProp22RightFormula()),
        "screened_hopf_nu_prime_count": available.count(hopf),
        "composite_formula_candidates": len(formula_candidates),
        "composite_substitution_candidates": len(substitution_candidates),
        "composite_substitution_subgoals": len(substitution_candidates[0].subgoals),
        "formula_local_replay_from_screened_given": (
            formula_step is not None and formula_step.conclusion == formula
        ),
        "substitution_local_replay_from_screened_given": (
            substituted_step is not None
            and substituted_step.conclusion == substituted
            and substituted_step.rule is ProofRule.INFERENCE
        ),
        "existing_formula_candidate_names": [
            item.rule.name for item in existing_provider(formula)
        ],
        "existing_substituted_candidate_names": [
            item.rule.name for item in existing_provider(substituted)
        ],
        "shared_provider_modified_by_r3r36": False,
        "shared_dfs_source_order_gate_verified": False,
        "transport_to_eta_cube_proved": False,
        "hopf_image_goal_proved": False,
        "root_group_proved": False,
        "new_given": 0,
        "full_pytest": "NOT_RUN",
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    directory = base / "EHPProofTracerAudit" / PACKAGE
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "report.json"


def execute(dry_run: bool) -> int:
    report: dict = {"gate": "FAIL_R3R36", "full_pytest": "NOT_RUN"}
    try:
        report.update(preflight())
        if dry_run:
            report["gate"] = "PASS_R3R36_DRYRUN"
        else:
            report.update(probe())
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)
    file = report_path()
    file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    for key, value in report.items():
        print("PHASE176_R3R36_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(file))
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return execute(parser.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())
