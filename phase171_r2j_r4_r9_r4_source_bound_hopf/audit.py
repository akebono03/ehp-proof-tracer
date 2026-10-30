"""R2J-R4-R9-R4: source-bound Hopf replay through canonical backward search.

Audit only; no production provider changes. A DB-admitted cyclic group cannot
replace the inference from the screened Proposition 5.3 in this Hopf rule.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r4_source_bound_hopf.source import source_bound_hopf_provider
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("read-only Git commands only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, text=True,
        capture_output=True, check=True,
    ).stdout.strip()


def hopf_goal() -> MapSurjective:
    return MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))


def build_source_bound_context():
    screened, target, citing = _screened_context()
    original, _, original_report = build_cyclic_pi63_proof()
    if (
        original.rule is not ProofRule.INFERENCE
        or original.conclusion != target
        or original_report["new_given_added"] != 0
    ):
        raise RuntimeError("validated R4-R8 proof is required")
    fallback = shared_expansion_provider(screened, proof_target=target)
    provider, bound, source_id = source_bound_hopf_provider(
        original, screened, citing, hopf_goal(), fallback,
    )
    return screened, target, citing, provider, bound, source_id



def previous_hopf_match_evidence() -> dict:
    """Read the existing R9-R3 observation without accepting it as proof."""
    path = ROOT / "phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic" / "output" / "audit.json"
    if not path.is_file():
        return {"available": False, "input_proof_rules": [], "expected_proof_rules": []}
    row = json.loads(path.read_text(encoding="utf-8"))
    attempts = row.get("hopf_match_attempts", [])
    if row.get("hopf_failure_class") != "HOPF_MATCHER_REJECTED_RECONSTRUCTED_PREMISES" or len(attempts) != 1:
        return {"available": False, "input_proof_rules": [], "expected_proof_rules": []}
    attempt = attempts[0]
    return {
        "available": True,
        "input_proof_rules": attempt.get("input_proof_rules", []),
        "expected_proof_rules": attempt.get("expected_proof_rules", []),
        "database_given_hypothesis_supported": (
            attempt.get("input_proof_rules") == ["given", "inference"]
            and attempt.get("expected_proof_rules") == ["inference", "inference"]
        ),
    }

def audit_source_bound_search() -> dict:
    """Reconstruct the H subgoal first; then observe the full scoped search."""
    screened, target, citing, provider, bound, source_id = build_source_bound_context()
    group = reconstruct_registered_goal(
        bound, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    if (
        group.rule is not ProofRule.INFERENCE
        or group.conclusion != bound.conclusion
        or len(group.premises) != 1
        or group.premises[0].rule is not ProofRule.GIVEN
        or group.premises[0].conclusion != bound.source
    ):
        raise RuntimeError("source-bounded cyclic group was not independently derived")
    hopf = reconstruct_registered_goal(
        hopf_goal(), screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    if (
        hopf.rule is not ProofRule.INFERENCE
        or hopf.conclusion != hopf_goal()
        or len(hopf.premises) != 2
        or any(x.rule is not ProofRule.INFERENCE for x in hopf.premises)
        or hopf.premises[0].conclusion != bound.conclusion
    ):
        raise RuntimeError("source-bound Hopf surjectivity was not independently inferred")

    result = search_registered_partial_proof(
        n=3, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing, expansion_provider=provider,
        lookup_mode="typed_reference_publication",
    )
    complete = (
        result.status is ProofSearchStatus.COMPLETE
        and result.conclusion == target
        and not result.open_goals
    )
    verified = False
    verification = None
    if complete:
        try:
            verification = verify_proof_tree_for_narrative(
                result, screened, citing_assertion_id=citing,
            )
            verified = True
        except UnverifiedProofTree as exc:
            verification = str(exc)
    return {
        "phase": "171-R2J-R4-R9-R4",
        "mode": "AUDIT_ONLY_SOURCE_BOUND_HOPF",
        "hopf_source_assertion_id": source_id,
        "previous_hopf_match_evidence": previous_hopf_match_evidence(),
        "bound_group_inferred": True,
        "hopf_surjective_inferred": True,
        "hopf_premise_rules": [x.rule.value for x in hopf.premises],
        "scoped_search_status": result.status.value,
        "scoped_search_complete": complete,
        "scoped_proven_steps": len(result.proven_steps),
        "scoped_open_goals": [repr(x)[:1200] for x in result.open_goals[:20]],
        "scoped_diagnostics": list(result.diagnostics[:15]),
        "trust_boundary_accepted": verified,
        "trust_boundary_result": verification,
        "public_provider_modified": False,
        "public_web_verified": False,
        "new_given_added": 0,
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
        raise RuntimeError("R9-R4 requires develop")
    for path in (
        "phase171_r2j_r4_r8_cyclic_structure/audit.py",
        "phase171_r2j_r4_r9_r2_scoped_search_bridge/source.py",
        "phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic/audit.py",
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError("missing R9 prerequisite: " + path)
    print("PHASE171_R2J_R4_R9_R4_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R4_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R4_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = audit_source_bound_search()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files changed during source-bound audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    target = OUTPUT / "audit.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R4_BOUND_GROUP=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R4_HOPF_SURJECTIVE=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R4_SCOPED_SEARCH=" + report["scoped_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R4_TRUST_VERIFIED=" + str(report["trust_boundary_accepted"]), flush=True)
    print("PHASE171_R2J_R4_R9_R4_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R4_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R4_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R4_REPORT=" + str(target), flush=True)
    print("PHASE171_R2J_R4_R9_R4_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
