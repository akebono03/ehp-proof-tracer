"""Phase 174 R3-R7-R3: source-first generic EHP-zero candidate audit.

No production provider is changed by this audit. A backward proposal is not
proof and cannot discharge missing Delta surjectivity or free-group premises.
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
PHASE = "174-R3-R7-R3"
BASE_HEAD = "c055e8ddddaee2c0d0552bbdcc3e3afc62b6ff9c"
ALLOWED_NEXT_COMMIT_PREFIX = "phase174_r3_r7_r2_ehp_chain_audit/"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r12_r12_ehp_consequences.py": "895dc98ad4d25f14fb7aac8fa52460a77fd049bc",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r14_r9_ehp_exactness.py": "c39759f0b693ce89100ef8439e8aec7fe325694f",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
}
EXPECTED_COUNTS = {
    "delta_e_exactness": 1,
    "e_h_exactness": 1,
    "delta_isomorphism": 1,
    "delta_surjectivity": 0,
    "terminal_zero": 1,
    "target_zero": 0,
}


def git(*args: str, cwd: Path = ROOT) -> str:
    process = subprocess.run(
        ("git",) + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
        errors="replace",
    )
    return process.stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def accepted_source_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return any(
        blob_sha(item) == expected
        for item in (data, normalized, normalized.replace(b"\n", b"\r\n"))
    )


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    repo = Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve()
    if repo != root.resolve():
        raise RuntimeError("The audit must be extracted immediately under the repo root")
    branch = git("branch", "--show-current", cwd=root)
    local_head = git("rev-parse", "HEAD", cwd=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote_head = remote_line.split()[0] if remote_line else ""
    if branch != "develop" or local_head != remote_head:
        raise RuntimeError("Expected develop with local HEAD matching live origin/develop")
    base = git("merge-base", BASE_HEAD, remote_head, cwd=root)
    if base != BASE_HEAD:
        raise RuntimeError("Remote develop is not descended from the reviewed baseline")
    changed = git("diff", "--name-only", BASE_HEAD, remote_head, cwd=root)
    paths = changed.splitlines() if changed else []
    if any(not path.startswith(ALLOWED_NEXT_COMMIT_PREFIX) for path in paths):
        raise RuntimeError("Remote develop changed an unaudited path; redo source review")
    staged = git("diff", "--cached", "--name-only", cwd=root)
    if staged:
        raise RuntimeError("Staged changes must be reviewed separately")
    for relative, sha in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file() or not accepted_source_blob(file.read_bytes(), sha):
            raise RuntimeError("Audited source blob has changed: " + relative)
    toda = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    for clause in (
        r"\pi^{n}_{n+5}=0\ (n\ge7)",
        r"\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}",
        r"\pi^{6}_{11}\xrightarrow{E}\pi^{7}_{12}",
        r"\pi_{12}^{13}=0",
    ):
        if clause not in toda:
            raise RuntimeError("Toda Proposition 5.9 proof transcription changed")
    return {
        "branch": branch,
        "local_head": local_head,
        "remote_head": remote_head,
        "reviewed_base_head": BASE_HEAD,
        "allowed_followup_paths": paths,
        "source_guard_count": len(SOURCE_BLOBS),
        "staged_changes": [],
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root
        ).splitlines(),
    }


def previous_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r2" / "ehp_chain_audit.json"


def verify_r2_evidence(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("phase") != "174-R3-R7-R2":
        raise RuntimeError("Wrong previous audit phase")
    if data.get("gate") != "PASS_READ_ONLY_TYPED_EHP_CHAIN":
        raise RuntimeError("Previous typed EHP audit not certified")
    prior = data.get("previous_audit") or {}
    if prior.get("zero_root_proposal_count") != 0:
        raise RuntimeError("Unexpected previous zero-root proposal count")
    live = data.get("live_obligations") or {}
    counts = {
        key: (live.get("obligations") or {}).get(key, {}).get("proposal_count")
        for key in EXPECTED_COUNTS
    }
    if counts != EXPECTED_COUNTS:
        raise RuntimeError("Previous source-screened proposal counts differ")
    pi = live.get("pi11_6") or {}
    if (pi.get("search_status") != "search_failed"
            or len(pi.get("open_goal_types", ())) != 2):
        raise RuntimeError("Previous pi_11^6 blocker differs")
    if data.get("new_group_given") != 0 or data.get("new_inference_rules") != 0:
        raise RuntimeError("Previous audit introduced unapproved premises")
    return {
        "previous_gate": data["gate"],
        "proposal_counts": counts,
        "pi11_6_open_goal_types": pi["open_goal_types"],
        "pi11_6_frontier": pi.get("candidate_frontier"),
        "delta_isomorphism_candidate_is_not_surjectivity_evidence": True,
    }


def inspect_new_candidate() -> dict[str, Any]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        ehp_zero_inputs, expand_ehp_zero_from_delta_surjectivity,
    )
    from proof import ProofRule

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    requirements = ehp_zero_inputs(goal)
    if requirements is None:
        raise RuntimeError("The typed general EHP condition does not apply")
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    screened = prefer_universal_prop42_derivation(screened)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if is_exact_given(goal, admitted):
        raise RuntimeError("The desired zero-group claim was an admitted GIVEN")
    existing = shared_expansion_provider(screened, proof_target=goal)
    old_root = summarize_proposals(existing, goal, admitted)
    new_root = expand_ehp_zero_from_delta_surjectivity(goal)
    if old_root["proposal_count"] != 0 or len(new_root) != 1:
        raise RuntimeError("Candidate root baseline differs")
    branches = {}
    for name, child in zip(
        ("delta_surjectivity", "delta_e_exactness", "e_h_exactness", "terminal_zero"),
        requirements,
    ):
        branch = summarize_proposals(existing, child, admitted, limit=5)
        branches[name] = {
            "goal": branch["goal"],
            "proposal_count": branch["proposal_count"],
            "proposals": branch["proposals"],
        }
    if branches["delta_surjectivity"]["proposal_count"] != 0:
        raise RuntimeError("A Delta-surjectivity candidate appeared unexpectedly")
    return {
        "source_screening": "independent_source_screened",
        "existing_zero_root_proposals": old_root["proposal_count"],
        "isolated_generic_root_proposals": len(new_root),
        "generic_root_rule": new_root[0].rule.name,
        "separate_premises": branches,
        "delta_surjectivity_still_unproved": True,
        "source_first_proof_steps_created": 0,
        "not_registered_with_production_provider": True,
        "no_target_direct_given": True,
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r3" / "generic_zero_rule.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_and_sources(root)
    report_file = previous_report_path()
    if not report_file.is_file():
        raise RuntimeError("Previous R3-R7-R2 JSON is required: " + str(report_file))
    evidence = verify_r2_evidence(json.loads(report_file.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_new_candidate()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "ISOLATED_GENERIC_RULE_AUDIT",
        "git_state": state,
        "prior_evidence": evidence,
        "new_candidate": live,
        "original_print_edition_verified": False,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "new_isolated_inference_rules": 1,
        "production_files_modified": False,
        "full_pytest_run": False,
        "generic_zero_group_completion_claimed": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_ISOLATED_RULE_DELTA_SURJECTIVITY_PENDING",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = make_report(dry_run=args.dry_run)
    destination = report_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PHASE174_R3R7R3_REMOTE_HEAD=" + result["git_state"]["remote_head"])
    print("PHASE174_R3R7R3_LOCAL_HEAD=" + result["git_state"]["local_head"])
    print("PHASE174_R3R7R3_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R3_PREVIOUS_DELTA_SURJECTIVITY_PROPOSALS=0")
    if result["new_candidate"] is not None:
        candidate = result["new_candidate"]
        print("PHASE174_R3R7R3_ISOLATED_ROOT_PROPOSALS=" + str(
            candidate["isolated_generic_root_proposals"]
        ))
        for name, item in candidate["separate_premises"].items():
            print("PHASE174_R3R7R3_CHILD_" + name.upper() + "_PROPOSALS=" + str(
                item["proposal_count"]
            ))
        print("PHASE174_R3R7R3_PUBLIC_PROVIDER_UNCHANGED=True")
    print("PHASE174_R3R7R3_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R7R3_NEW_PRODUCTION_RULES=0")
    print("PHASE174_R3R7R3_FULL_PYTEST=False")
    print("PHASE174_R3R7R3_REPORT=" + str(destination))
    print("PHASE174_R3R7R3_GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
