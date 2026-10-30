"""Audit-only second Hopf reconstruction and remaining scoped search.

Preserve the first R9-R4 source-bound Hopf branch, while proving the second
H-surjectivity branch with an INFERENCE codomain, not a DB GIVEN.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r4_source_bound_hopf.audit import (
    hopf_goal as first_hopf_goal,
)
from phase171_r2j_r4_r9_r4_source_bound_hopf.source import source_bound_hopf_provider
from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.source import (
    bind_cited_hopf_codomain,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in permitted:
        raise ValueError("read-only Git operations only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        text=True, capture_output=True,
    ).stdout.strip()


def build_second_bound_context():
    """Keep R9-R4's bound H and source-screen the other cited H branch."""
    screened, target, citing = _screened_context()
    root, _, report = build_cyclic_pi63_proof()
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != target
        or report["new_given_added"] != 0
    ):
        raise RuntimeError("genuine R4-R8 inferred root required")
    fallback = shared_expansion_provider(screened, proof_target=target)
    previous, _, first_source_id = source_bound_hopf_provider(
        root, screened, citing, first_hopf_goal(), fallback,
    )
    provider, bound, second_source_id, second_hopf = bind_cited_hopf_codomain(
        root, screened, citing, previous,
        expected_locator="Proposition 5.1",
    )
    if (
        second_hopf == first_hopf_goal()
        or second_source_id == first_source_id
    ):
        raise RuntimeError("second Hopf branch must be distinct from first")
    return screened, target, citing, provider, bound, second_source_id, second_hopf


def audit_second_source_bound_hopf() -> dict:
    screened, target, citing, provider, bound, source_id, second_hopf = (
        build_second_bound_context()
    )
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
        raise RuntimeError("cited codomain not independently inferred")
    hopf = reconstruct_registered_goal(
        second_hopf, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    if (
        hopf.rule is not ProofRule.INFERENCE
        or hopf.conclusion != second_hopf
        or len(hopf.premises) != 2
        or tuple(x.rule for x in hopf.premises)
        != (ProofRule.INFERENCE, ProofRule.GIVEN)
        or hopf.premises[0].conclusion != bound.conclusion
    ):
        raise RuntimeError("second Hopf surjectivity was not re-derived")
    earlier_hopf = reconstruct_registered_goal(
        first_hopf_goal(), screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    if (
        earlier_hopf.rule is not ProofRule.INFERENCE
        or any(item.rule is not ProofRule.INFERENCE
               for item in earlier_hopf.premises)
    ):
        raise RuntimeError("first source-bound Hopf branch regressed")
    result = search_registered_partial_proof(
        n=3, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing,
        expansion_provider=provider,
        lookup_mode="typed_reference_publication",
    )
    complete = (
        result.status is ProofSearchStatus.COMPLETE
        and result.conclusion == target
        and not result.open_goals
    )
    accepted = False
    trust_result = None
    if complete:
        try:
            trust_result = verify_proof_tree_for_narrative(
                result, screened, citing_assertion_id=citing,
            )
            accepted = True
        except UnverifiedProofTree as error:
            trust_result = str(error)
    return {
        "phase": "171-R2J-R4-R9-R6",
        "mode": "AUDIT_ONLY_SOURCE_BOUND_SECOND_CITED_HOPF",
        "source_assertion_id": source_id,
        "source_locator": "Proposition 5.1",
        "bound_group": repr(bound.conclusion),
        "second_hopf": repr(second_hopf),
        "bound_group_inferred": True,
        "second_hopf_surjective_inferred": True,
        "second_hopf_premise_rules": [s.rule.value for s in hopf.premises],
        "first_hopf_preserved": True,
        "scoped_search_status": result.status.value,
        "scoped_search_complete": complete,
        "scoped_proven_steps": len(result.proven_steps),
        "scoped_open_goals": [repr(item)[:1200] for item in result.open_goals[:20]],
        "first_unresolved_goal": (
            repr(result.open_goals[0])[:1200] if result.open_goals else None
        ),
        "scoped_diagnostics": list(result.diagnostics[:20]),
        "trust_boundary_accepted": accepted,
        "trust_boundary_result": trust_result,
        "new_given_added": 0,
        "public_provider_modified": False,
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
        raise RuntimeError("R9-R6 requires develop")
    for relative in (
        "phase171_r2j_r4_r9_r4_source_bound_hopf/source.py",
        "phase171_r2j_r4_r9_r5_remaining_match_frontier/audit.py",
        "phase171_r2j_r4_r8_cyclic_structure/audit.py",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError("missing prior phase dependency: " + relative)
    print("PHASE171_R2J_R4_R9_R6_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R6_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R6_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = audit_second_source_bound_hopf()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files modified during R9-R6 audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R9_R6_BOUND_GROUP=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R6_SECOND_HOPF=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R6_FIRST_HOPF_PRESERVED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R6_SCOPED_SEARCH=" + report["scoped_search_status"], flush=True)
    if report["first_unresolved_goal"] is not None:
        print("PHASE171_R2J_R4_R9_R6_FIRST_OPEN_GOAL=" + report["first_unresolved_goal"], flush=True)
    print("PHASE171_R2J_R4_R9_R6_TRUST_VERIFIED=" + str(report["trust_boundary_accepted"]), flush=True)
    print("PHASE171_R2J_R4_R9_R6_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R6_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R6_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R6_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R9_R6_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
