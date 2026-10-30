"""Audit source-anchored equality symmetry in the independent public search.

No original finished R2I ProofStep is imported into the public search. A
previous source-verified tree checks only the mathematical shape of the rule.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import (
    _checked_chain,
    _screened_context,
    build_cited_r2i_proof,
)
from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import (
    cited_chain_forward_equalities,
    expand_reverse_cited_eta_hopf_equalities,
    reverse_equality,
)
from proof import ProofRule, find_inference_matches_for_rule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*args: str) -> str:
    if args not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("only read-only Git operations")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.strip()


def inspect_public_eta_symmetry() -> dict:
    """Check source-bound inverse routes then independently search pi_6^3."""
    screened, target, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    forward_root, actual_chain, ancestry = build_cited_r2i_proof()
    if (
        forward_root.rule is not ProofRule.INFERENCE
        or forward_root.conclusion != chain.conclusion
        or actual_chain != chain
        or any(node.conclusion == target for node in ancestry)
    ):
        raise RuntimeError("R2I source-backed inference is unavailable")

    forwards = cited_chain_forward_equalities(available)
    if chain.alpha_composition not in forwards or len(forwards) < 5:
        raise RuntimeError("no exact, source-anchored forward equality set")
    expected = reverse_equality(chain.alpha_composition)
    original = next((node for node in ancestry
                     if node.conclusion == chain.alpha_composition
                     and node.rule is ProofRule.INFERENCE), None)
    if original is None or expected is None:
        raise RuntimeError("actual R2I forward inference is missing")
    proposed = expand_reverse_cited_eta_hopf_equalities(expected, available)
    shared = shared_expansion_provider(screened, proof_target=target)(expected)
    same = tuple(option for option in shared
                 if option.rule.name == "equality symmetry"
                 and option.subgoals == (chain.alpha_composition,))
    if len(proposed) != 1 or len(same) != 1:
        raise RuntimeError("public source-anchored inverse was not connected")
    matches = find_inference_matches_for_rule(proposed[0].rule, (original,))
    if len(matches) != 1:
        raise RuntimeError("existing equality symmetry rule rejected genuine R2I ancestry")
    inverse_step = derive_inference_proof_step(matches[0])
    if (inverse_step.rule is not ProofRule.INFERENCE
            or inverse_step.conclusion != expected
            or inverse_step.premises != (original,)):
        raise RuntimeError("reverse equality was not genuinely inferred")
    for forward in forwards:
        inverse = reverse_equality(forward)
        routes = expand_reverse_cited_eta_hopf_equalities(inverse, available)
        if len(routes) != 1 or routes[0].subgoals != (forward,):
            raise RuntimeError("typed eta-Hopf chain inversion is inconsistent")
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=target,
    )
    complete = (
        public.status.value == "complete" and public.conclusion == target
        and not public.open_goals
    )
    return {
        "phase": "171-R2J-R4-R9-R11",
        "mode": "PUBLIC_TYPED_ETA_HOPF_SYMMETRY_INTEGRATION",
        "registered_target": repr(target),
        "source_anchored_forward_routes": len(forwards),
        "first_reverse": repr(expected),
        "source_anchored_reverse_routes": len(forwards),
        "first_reverse_inference_matched": True,
        "shared_first_reverse_connected": True,
        "public_search_status": public.status.value,
        "public_complete": complete,
        "public_proven_steps": len(public.proven_steps),
        "public_open_goals": [repr(item)[:1500] for item in public.open_goals[:25]],
        "public_diagnostics": list(public.diagnostics[:20]),
        "new_given_added": 0,
        "completed_proof_imported": False,
        "web_modified": False,
        "trust_boundary_modified": False,
        "public_web_verified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if branch != "develop":
        raise RuntimeError("develop branch required")
    print("PHASE171_R2J_R4_R9_R11_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R11_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R11_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_public_eta_symmetry()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked source changed during read-only audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    dest = OUTPUT / "audit.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R11_REVERSED_EQUALITY=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R11_SHARED_REVERSE_CONNECTED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R11_REVERSE_ROUTES=" + str(report["source_anchored_reverse_routes"]), flush=True)
    print("PHASE171_R2J_R4_R9_R11_PUBLIC_SEARCH=" + report["public_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R11_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    if report["public_open_goals"]:
        print("PHASE171_R2J_R4_R9_R11_FIRST_OPEN_GOAL=" + report["public_open_goals"][0], flush=True)
    print("PHASE171_R2J_R4_R9_R11_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R11_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R11_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R11_REPORT=" + str(dest), flush=True)
    print("PHASE171_R2J_R4_R9_R11_RESULT=PASS_SYMMETRY_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()
