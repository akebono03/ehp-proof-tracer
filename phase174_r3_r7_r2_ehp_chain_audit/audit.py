"""R3-R7-R2: inspect typed EHP zero-group obligations without adding proofs.

This probe only reads Git state, accepted Toda source transcription,
existing screened proof providers, and the preceding R3-R7-R1 audit result.
Candidate GoalExpansion objects are NOT verified ProofSteps.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R2"
# The R1 report was captured at PREVIOUS_AUDIT_HEAD; the later develop commit
# only adds the reviewed R1 audit package and leaves mathematical sources intact.
PREVIOUS_AUDIT_HEAD = "992975395195a0e49955617ba1ae772127036dde"
REVIEWED_HEAD = "c055e8ddddaee2c0d0552bbdcc3e3afc62b6ff9c"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r12_r12_ehp_consequences.py": "895dc98ad4d25f14fb7aac8fa52460a77fd049bc",
    "phase165_r12_r15_toda51.py": "6a7120ba9955749a74ee90fe1d85e003f80873a0",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r14_r9_ehp_exactness.py": "c39759f0b693ce89100ef8439e8aec7fe325694f",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
    "phase174_r3_r7_source_first_audit/audit.py": "1fa57f56cd90dc7b440d29f8a1361430cf182540",
}
SOURCE_EXCERPTS = {
    "five_stem_general_result": r"\pi^{n}_{n+5}=0\ (n\ge7)",
    "preceding_free_generator": r"\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}",
    "delta_isomorphism": r"\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}",
    "suspension_map": r"\pi^{6}_{11}\xrightarrow{E}\pi^{7}_{12}",
    "terminal_zero": r"\pi_{12}^{13}=0",
    "target_zero": r"\pi_{12}^7=0",
    "proof_hopf_delta_identity": r"H(\Delta(\iota_{13}))=\pm2\iota_{11}",
}


def command(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        args, cwd=cwd, capture_output=True, text=True,
        check=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def matches_git_blob(data: bytes, sha: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return any(
        git_blob_sha(item) == sha
        for item in (data, normalized, normalized.replace(b"\n", b"\r\n"))
    )


def validate_sources(root: Path = ROOT) -> dict[str, Any]:
    actual_root = Path(command("git", "rev-parse", "--show-toplevel", cwd=root)).resolve()
    if actual_root != root.resolve():
        raise RuntimeError("Audit package must be directly beneath the repository root")
    branch = command("git", "branch", "--show-current", cwd=root)
    local_head = command("git", "rev-parse", "HEAD", cwd=root)
    remote_line = command("git", "ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote_head = remote_line.split()[0] if remote_line else ""
    if branch != "develop" or remote_head != REVIEWED_HEAD:
        raise RuntimeError("Git develop HEAD changed or is not at the reviewed baseline")
    if local_head not in (PREVIOUS_AUDIT_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local HEAD is outside the audited two-commit lineage")
    ancestor = command(
        "git", "merge-base", PREVIOUS_AUDIT_HEAD, REVIEWED_HEAD, cwd=root
    )
    if ancestor != PREVIOUS_AUDIT_HEAD:
        raise RuntimeError("The prior R1 audit baseline is not an ancestor")
    changed_paths = command(
        "git", "diff", "--name-only", PREVIOUS_AUDIT_HEAD, REVIEWED_HEAD,
        cwd=root,
    ).splitlines()
    if not changed_paths or any(
        not path.startswith("phase174_r3_r7_r1_zero_root_audit/")
        for path in changed_paths
    ):
        raise RuntimeError("Unexpected changes in reviewed Git HEAD lineage")
    staged = command("git", "diff", "--cached", "--name-only", cwd=root)
    if staged:
        raise RuntimeError("Staged changes require a separate review")
    for relative, sha in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file() or not matches_git_blob(file.read_bytes(), sha):
            raise RuntimeError("Source Guard failed for " + relative)
    return {
        "branch": branch,
        "local_head": local_head,
        "remote_head": remote_head,
        "previous_audit_head": PREVIOUS_AUDIT_HEAD,
        "reviewed_lineage_paths": changed_paths,
        "source_guard_files": len(SOURCE_BLOBS),
        "staged_changes": [],
        "working_tree_status": command(
            "git", "status", "--porcelain=v1", "--untracked-files=normal", cwd=root
        ).splitlines(),
    }


def verify_toda_transcription(root: Path = ROOT) -> dict[str, Any]:
    source = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    missing = [key for key, phrase in SOURCE_EXCERPTS.items() if phrase not in source]
    if missing:
        raise RuntimeError("Missing Toda Proposition 5.9 proof text: " + ", ".join(missing))
    return {
        "source_path": "sources/toda/Toda_05_2.tex",
        "checked_excerpts": list(SOURCE_EXCERPTS),
        "original_print_edition_independently_verified": False,
        "source_quotation_is_not_target_given": True,
    }


def previous_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r1" / "zero_root_audit.json"


def validate_previous_report(report: dict[str, Any]) -> dict[str, Any]:
    if report.get("phase") != "174-R3-R7-R1":
        raise RuntimeError("Wrong prior audit phase")
    if report.get("gate") != "PASS_READ_ONLY_ZERO_ROOT_DIAGNOSTIC":
        raise RuntimeError("Prior zero-root audit did not pass")
    state = report.get("git_state", {})
    if state.get("remote_head") != PREVIOUS_AUDIT_HEAD or state.get("local_head") != PREVIOUS_AUDIT_HEAD:
        raise RuntimeError("Prior zero-root audit HEAD differs")
    live = report.get("live_zero_root") or {}
    zero = live.get("zero_root") or {}
    if (zero.get("proposal_count") != 0
            or live.get("preceding_group") != "pi_11^6"
            or live.get("preceding_group_status") != "search_failed"
            or live.get("zero_search_status") != "search_failed"
            or live.get("direct_zero_target_given") is not False):
        raise RuntimeError("R3-R7-R1 measured zero-root/prior state differs")
    if report.get("new_inference_rules") != 0 or report.get("new_group_given") != 0:
        raise RuntimeError("Prior audit has new rules or GIVENs")
    return {
        "prior_gate": report["gate"],
        "zero_root_proposal_count": 0,
        "precursor": "pi_11^6",
        "precursor_status": "search_failed",
        "source_context": live.get("screening_path"),
    }


def ehp_chain_dimensions() -> dict[str, Any]:
    return {
        "delta_e": {
            "source": (13, 13), "middle": (11, 6), "target": (12, 7),
            "first_map": "Delta", "second_map": "E", "expected_indices": (6, 12, "delta_e"),
        },
        "e_h": {
            "source": (11, 6), "middle": (12, 7), "target": (12, 13),
            "first_map": "E", "second_map": "H", "expected_indices": (6, 12, "e_h"),
        },
    }


def classify_proposals(count: int) -> str:
    if not isinstance(count, int) or count < 0:
        raise ValueError("Candidate count must be nonnegative integer")
    return "NO_CANDIDATE" if count == 0 else "CANDIDATES_NOT_PROOFS"


def typed_chain_goals() -> dict[str, object]:
    from homotopy_groups import (
        TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroup,
        TodaPrimaryGroupZeroStatement,
    )
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from phase165_r14_r6_generic_iso import MapIsomorphism, MapSurjective
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from toda_rules import TodaProp42ExactnessStatement

    d = TodaPrimaryGroup(13, 13)
    a = TodaPrimaryGroup(11, 6)
    b = TodaPrimaryGroup(12, 7)
    c = TodaPrimaryGroup(12, 13)
    delta_e = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        d, a, b, EHP_DELTA_MAP, EHP_E_MAP,
    ))
    e_h = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        a, b, c, EHP_E_MAP, EHP_H_MAP,
    ))
    if prop42_exactness_indices(delta_e) != (6, 12, "delta_e"):
        raise RuntimeError("Typed Delta-E EHP window was not validated")
    if prop42_exactness_indices(e_h) != (6, 12, "e_h"):
        raise RuntimeError("Typed E-H EHP window was not validated")
    delta = TodaDeltaMap(d, a)
    return {
        "delta_e_exactness": delta_e,
        "e_h_exactness": e_h,
        "delta_isomorphism": MapIsomorphism(delta),
        "delta_surjectivity": MapSurjective(delta),
        "terminal_zero": TodaPrimaryGroupZeroStatement(c),
        "target_zero": TodaPrimaryGroupZeroStatement(b),
    }


def inspect_live_obligations() -> dict[str, Any]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import (
        registered_group_goal_candidates, search_group_from_registered_goal,
    )
    from phase165_r12_r11_prop42_unified import (
        TodaProp42GeneralExactnessStatement, prefer_universal_prop42_derivation,
    )
    from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    goals = typed_chain_goals()
    target = goals["target_zero"]
    assert isinstance(target, TodaPrimaryGroupZeroStatement)
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target)
    screened = prefer_universal_prop42_derivation(screened)
    givens = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if is_exact_given(target, givens):
        raise RuntimeError("Target itself was admitted as a direct GIVEN")
    provider = shared_expansion_provider(screened, proof_target=target)
    diagnostics = {}
    for name, goal in goals.items():
        summary = summarize_proposals(provider, goal, givens, limit=10)
        diagnostics[name] = {
            "goal": summary["goal"],
            "proposal_count": summary["proposal_count"],
            "interpretation": classify_proposals(summary["proposal_count"]),
            "proposals": summary["proposals"],
            "probe_created_proof_steps": 0,
        }
    if diagnostics["target_zero"]["proposal_count"] != 0:
        raise RuntimeError("The previously measured zero-root baseline changed")

    prior = search_group_from_registered_goal(n=6, k=5, bridge=bridge)
    prior_candidates = registered_group_goal_candidates(bridge, n=6, k=5)
    prior_roots = []
    prior_source_context = "NO_SINGLE_TYPED_RELATION_GOAL"
    if len(prior_candidates) == 1:
        prior_goal = prior_candidates[0]
        prior_screened = screen_independent_sources_for_derived_goal(
            bridge, goal=prior_goal,
        )
        prior_screened = prefer_universal_prop42_derivation(prior_screened)
        prior_givens = tuple(
            link.step.conclusion for link in prior_screened.proof_links
            if link.step is not None and link.step.rule is ProofRule.GIVEN
        )
        if is_exact_given(prior_goal, prior_givens):
            raise RuntimeError("Previous free-cyclic group goal was directly GIVEN")
        prior_provider = shared_expansion_provider(
            prior_screened, proof_target=prior_goal,
        )
        prior_roots.append(summarize_proposals(
            prior_provider, prior_goal, prior_givens, limit=10,
        ))
        for subgoal in tuple(prior.open_goals)[:5]:
            prior_roots.append(summarize_proposals(
                prior_provider, subgoal, prior_givens, limit=6,
            ))
        prior_source_context = "independent_source_screened"

    return {
        "zero_goal": repr(target),
        "source_screening": "independent_source_screened",
        "screened_given_count": len(givens),
        "general_prop42_given_count": sum(
            type(x) is TodaProp42GeneralExactnessStatement for x in givens
        ),
        "general_toda51_zero_given_count": sum(
            type(x) is Toda51BelowDiagonalZeroStatement for x in givens
        ),
        "no_direct_target_given": True,
        "typed_ehp_chain": {name: repr(goal) for name, goal in goals.items()},
        "obligations": diagnostics,
        "pi11_6": {
            "registered_relation_candidates": len(prior_candidates),
            "search_status": getattr(prior.status, "value", str(prior.status)),
            "proven_steps": len(prior.proven_steps),
            "open_goal_types": [type(x).__name__ for x in prior.open_goals],
            "source_screening": prior_source_context,
            "candidate_frontier": prior_roots,
        },
        "proof_steps_created_by_audit": 0,
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r2" / "ehp_chain_audit.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = validate_sources(root)
    source = verify_toda_transcription(root)
    previous_path = previous_report_path()
    if not previous_path.is_file():
        raise RuntimeError("R3-R7-R1 saved audit JSON is required: " + str(previous_path))
    previous = validate_previous_report(json.loads(
        previous_path.read_text(encoding="utf-8-sig")
    ))
    live = None if dry_run else inspect_live_obligations()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_TYPED_EHP_CHAIN",
        "git_state": state,
        "source_review": source,
        "previous_audit": previous,
        "expected_ehp_windows": ehp_chain_dimensions(),
        "live_obligations": live,
        "new_group_given": 0,
        "new_inference_rules": 0,
        "production_files_changed": False,
        "full_pytest_run": False,
        "implementation_rule_approved": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_READ_ONLY_TYPED_EHP_CHAIN",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    report = make_report(dry_run=arguments.dry_run)
    path = report_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PHASE174_R3R7R2_REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print("PHASE174_R3R7R2_LOCAL_HEAD=" + report["git_state"]["local_head"])
    print("PHASE174_R3R7R2_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R2_PREVIOUS_ZERO_ROOT_PROPOSALS=" + str(
        report["previous_audit"]["zero_root_proposal_count"]
    ))
    print("PHASE174_R3R7R2_TYPED_WINDOWS=2")
    if report["live_obligations"] is not None:
        live = report["live_obligations"]
        for name, row in live["obligations"].items():
            print("PHASE174_R3R7R2_GOAL_" + name.upper() + "_PROPOSALS=" + str(
                row["proposal_count"]
            ))
        precursor = live["pi11_6"]
        print("PHASE174_R3R7R2_PI116_STATUS=" + precursor["search_status"])
        print("PHASE174_R3R7R2_PI116_OPEN_GOALS=" + str(
            len(precursor["open_goal_types"])
        ))
        print("PHASE174_R3R7R2_PI116_REGISTERED_GOALS=" + str(
            precursor["registered_relation_candidates"]
        ))
    print("PHASE174_R3R7R2_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R7R2_NEW_RULES=0")
    print("PHASE174_R3R7R2_FULL_PYTEST=False")
    print("PHASE174_R3R7R2_REPORT=" + str(path))
    print("PHASE174_R3R7R2_GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
