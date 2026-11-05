"""R3-R7-R1: read-only zero-root frontier audit, not a proof implementation.

No source GIVENs, proof steps, inference rules, or production files are added.
The source transcription and source-screened candidate rules are diagnostic
inputs only; neither constitutes a completed mathematical derivation.
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
PACKAGE = Path(__file__).resolve().parent
PHASE = "174-R3-R7-R1"
REVIEWED_HEAD = "992975395195a0e49955617ba1ae772127036dde"
PREVIOUS_HEAD = "1a6a5a57992963c7a21aa22079a145a310b4e0ed"
EVIDENCE = PACKAGE / "evidence" / "phase174_r3_r7_audit.json"
EVIDENCE_SHA256 = "4d0c7188863e3d0196a23762a2c86ba3180f52f6c28a7762569321981ef66698"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
    "toda_stable_group_transport.py": "3ba5db0a0fd91f2831d766eb557dc28d25f4d4db",
    "phase173_r4_r11_zero_public_connection/route.py": "e3230eed2dfa8dd3efc60cc0a03f787fa92bbeaa",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "phase174_r3_r7_source_first_audit/audit.py": "1fa57f56cd90dc7b440d29f8a1361430cf182540",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    completed = subprocess.run(
        ("git",) + args,
        cwd=cwd,
        capture_output=True,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def accepted_blob(content: bytes, expected: str) -> bool:
    normalized = content.replace(b"\r\n", b"\n")
    return any(
        git_blob(candidate) == expected
        for candidate in (content, normalized, normalized.replace(b"\n", b"\r\n"))
    )


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("The audit package must be directly under the repository root")
    branch = git("branch", "--show-current", cwd=root)
    local_head = git("rev-parse", "HEAD", cwd=root)
    remote_output = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote_head = remote_output.split()[0] if remote_output else ""
    if branch != "develop":
        raise RuntimeError("Expected develop branch; audit performs no checkout")
    if remote_head != REVIEWED_HEAD:
        raise RuntimeError("Remote develop HEAD changed: new source review is required")
    if local_head not in (PREVIOUS_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local HEAD is outside reviewed baselines")
    for relative, sha in SOURCE_BLOBS.items():
        path = root / relative
        if not path.is_file() or not accepted_blob(path.read_bytes(), sha):
            raise RuntimeError("Reviewed source/code changed: " + relative)
    return {
        "branch": branch,
        "local_head": local_head,
        "remote_head": remote_head,
        "local_equals_remote": local_head == remote_head,
        "source_blobs_pass": True,
        "staged_paths": git("diff", "--cached", "--name-only", cwd=root).splitlines(),
        "status_porcelain": git("status", "--porcelain=v1", cwd=root).splitlines(),
        "writes_to_repository": False,
    }


def validate_previous_audit(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("phase") != "174-R3-R7" or data.get("audit_gate") != "PASS_READ_ONLY":
        raise RuntimeError("R3-R7 evidence is not the completed read-only audit")
    state = data.get("git_state", {})
    if (state.get("local_head") != PREVIOUS_HEAD
            or state.get("reviewed_remote_head") != PREVIOUS_HEAD):
        raise RuntimeError("R3-R7 evidence HEAD differs from reviewed ancestry")
    if data.get("runtime_errors") or data.get("new_group_given") != 0:
        raise RuntimeError("Earlier audit contained runtime errors or new group GIVEN")
    rows = data.get("selected_targets", [])
    if len(rows) != 7:
        raise RuntimeError("R3-R7 evidence must contain exactly seven selected groups")
    by_group = {row["group"]: row for row in rows}
    required = {
        "pi_8^5", "pi_12^4", "pi_13^4", "pi_11^3",
        "pi_12^7", "pi_12^3", "pi_13^7",
    }
    if set(by_group) != required:
        raise RuntimeError("R3-R7 selected group inventory differs")
    baseline = by_group["pi_8^5"]
    if (baseline.get("status") != "complete"
            or baseline.get("proven_step_count") != 16
            or baseline.get("open_goal_count") != 0):
        raise RuntimeError("Previously completed pi_8^5 was not preserved")
    zero = by_group["pi_12^7"]
    goals = zero.get("open_goals", [])
    if (zero.get("status") != "search_failed"
            or zero.get("open_goal_count") != 1
            or len(goals) != 1
            or goals[0].get("type") != "TodaPrimaryGroupZeroStatement"
            or "group_dimension=12, sphere_dimension=7" not in goals[0].get("repr", "")):
        raise RuntimeError("The expected pi_12^7 zero frontier changed")
    return {
        "reviewed_evidence_head": PREVIOUS_HEAD,
        "verified_baseline": "pi_8^5: 16 steps, complete, zero open goals",
        "zero_target": "pi_12^7",
        "zero_goal_type": "TodaPrimaryGroupZeroStatement",
        "zero_goal_open_count": 1,
        "previous_zero_root_proposal_count_measured": False,
        "previous_zero_root_note": (
            "R3-R7 explicitly skipped the standalone zero-root proposal probe "
            "because it had no registered Relation candidate. "
            "No zero-root provider count can be inferred from that report."
        ),
        "other_frontier_summary": summarize_other_frontiers(rows),
    }


def summarize_other_frontiers(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for row in rows:
        group = row["group"]
        if group in ("pi_8^5", "pi_12^7"):
            continue
        frontier = row.get("source_screened_frontier", {})
        open_entries = frontier.get("open_goal_frontier", [])
        result.append({
            "group": group,
            "open_goals": row["open_goal_count"],
            "open_goal_candidate_counts": [entry["proposal_count"] for entry in open_entries],
            "cyclic_structure_blockers": sum(
                1 for entry in open_entries
                if entry.get("goal", {}).get("type") == "CyclicStructureStatement"
                and entry.get("proposal_count") == 0
            ),
            "only_equality_symmetry_for_all_open_goals": bool(open_entries) and all(
                entry.get("proposal_count") > 0
                and all(proposal.get("rule") == "equality symmetry"
                        for proposal in entry.get("proposals", []))
                for entry in open_entries
            ),
        })
    return result


def verify_toda_proof_route(root: Path = ROOT) -> dict[str, Any]:
    source = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig"
    )
    snippets = {
        "proposition_59_general_five_stem_zero":
            r"\pi^{n}_{n+5}=0\ (n\ge7)",
        "pi_11_6_generator":
            r"\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}",
        "exact_delta_iso":
            r"\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}",
        "exact_next_suspension":
            r"\pi^{6}_{11}\xrightarrow{E}\pi^{7}_{12}",
        "exact_next_zero":
            r"\pi_{12}^{13}=0",
        "proof_says_pi_12_7_zero":
            r"\pi_{12}^7=0",
        "stable_transport_45":
            r"(4.5) により, Propの最後の結果が得られる",
    }
    missing = [name for name, snippet in snippets.items() if snippet not in source]
    if missing:
        raise RuntimeError("Toda proof excerpts absent or revised: " + ", ".join(missing))
    return {
        "transcription": "sources/toda/Toda_05_2.tex",
        "proposition": "Toda Proposition 5.9",
        "source_checks": {name: True for name in snippets},
        "route": (
            "exact pi_13^13 --Delta(isomorphism)--> pi_11^6 "
            "--E--> pi_12^7 --> pi_12^13=0"
        ),
        "necessary_derived_premises": [
            "EHP exactness with precise map/group dimensions",
            "Delta: pi_13^13 -> pi_11^6 is an isomorphism",
            "pi_12^13=0 from below-diagonal vanishing",
            "zero-group conclusion from exactness and the preceding isomorphism",
        ],
        "printed_source_result_not_a_given": True,
        "original_edition_independently_verified": False,
    }


def live_zero_frontier() -> dict[str, Any]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase173_r4_r11_zero_public_connection.route import (
        prepare_zero_toda56_public_connection,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from proof import ProofRule

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    specialized = prepare_zero_toda56_public_connection(bridge=bridge, goal=goal)
    if specialized is None:
        screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
        screened = prefer_universal_prop42_derivation(screened)
        provider = shared_expansion_provider(screened, proof_target=goal)
        screening = "independent_source_screened_shared_provider"
    else:
        screened, provider = specialized
        screening = "toda56_zero_connection"
    given = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if is_exact_given(goal, given):
        raise RuntimeError("Direct target zero-GIVEN found; source-first rule forbids it")
    zero = summarize_proposals(provider, goal, given, limit=20)
    previous_result = search_group_from_registered_goal(n=7, k=5, bridge=bridge)
    if previous_result.conclusion is not None and previous_result.status.value == "complete":
        raise RuntimeError("Unexpectedly complete zero proof; audit baseline changed")
    precursor = search_group_from_registered_goal(n=6, k=5, bridge=bridge)
    return {
        "zero_goal_type": type(goal).__name__,
        "screening_path": screening,
        "screened_given_count": len(given),
        "direct_zero_target_given": False,
        "zero_root": zero,
        "zero_search_status": getattr(previous_result.status, "value", str(previous_result.status)),
        "zero_open_goal_types": [type(x).__name__ for x in previous_result.open_goals],
        "preceding_group": "pi_11^6",
        "preceding_group_status": getattr(precursor.status, "value", str(precursor.status)),
        "preceding_group_steps": len(precursor.proven_steps),
        "preceding_group_open_goal_types": [type(x).__name__ for x in precursor.open_goals],
        "probe_created_proofs": 0,
    }


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_and_sources(root)
    evidence_bytes = EVIDENCE.read_bytes()
    if hashlib.sha256(evidence_bytes).hexdigest() != EVIDENCE_SHA256:
        raise RuntimeError("Uploaded Phase 174 R3-R7 evidence bytes changed")
    evidence = validate_previous_audit(json.loads(evidence_bytes.decode("utf-8-sig")))
    source = verify_toda_proof_route(root)
    live = None if dry_run else live_zero_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_LIVE_ZERO_ROOT",
        "git_state": state,
        "previous_evidence_sha256": hashlib.sha256(evidence_bytes).hexdigest(),
        "previous_evidence": evidence,
        "toda_proof_route": source,
        "live_zero_root": live,
        "new_group_given": 0,
        "new_inference_rules": 0,
        "production_files_changed": False,
        "full_pytest_run": False,
        "implementation_approved": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_READ_ONLY_ZERO_ROOT_DIAGNOSTIC",
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r1" / "zero_root_audit.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = report_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state = report["git_state"]
    print("PHASE174_R3R7R1_REMOTE_HEAD=" + state["remote_head"])
    print("PHASE174_R3R7R1_LOCAL_HEAD=" + state["local_head"])
    print("PHASE174_R3R7R1_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R1_TODA_PROP59_ROUTE=CONFIRMED_IN_TRANSCRIPTION")
    print("PHASE174_R3R7R1_PREVIOUS_ZERO_ROOT_PROBED=False")
    if report["live_zero_root"] is not None:
        live = report["live_zero_root"]
        print("PHASE174_R3R7R1_ZERO_SCREENING=" + live["screening_path"])
        print("PHASE174_R3R7R1_ZERO_ROOT_PROPOSALS=" + str(live["zero_root"]["proposal_count"]))
        print("PHASE174_R3R7R1_PI116_STATUS=" + live["preceding_group_status"])
        print("PHASE174_R3R7R1_PI127_STATUS=" + live["zero_search_status"])
        print("PHASE174_R3R7R1_DIRECT_ZERO_GIVEN=False")
    print("PHASE174_R3R7R1_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R7R1_NEW_RULES=0")
    print("PHASE174_R3R7R1_FULL_PYTEST=False")
    print("PHASE174_R3R7R1_REPORT=" + str(path))
    print("PHASE174_R3R7R1_GATE=" + report["gate"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
