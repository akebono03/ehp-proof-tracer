"""Phase 174 R3-R7-R4: read-only source-first Delta-surjectivity gap audit.

Candidate expansions are not proofs. No production rules or GIVENs are changed.
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
PHASE = "174-R3-R7-R4"
BASE_HEAD = "ae537ca26093fd262f18280ab0ec2034b8c15bf6"
REVIEWED_HEAD = "1f3a61d7d6cfc7854e56c4f5c372bf5c71e203df"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r12_r12_ehp_consequences.py": "895dc98ad4d25f14fb7aac8fa52460a77fd049bc",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r14_r9_ehp_exactness.py": "c39759f0b693ce89100ef8439e8aec7fe325694f",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
    "phase174_r3_r7_source_first_audit/audit.py": "1fa57f56cd90dc7b440d29f8a1361430cf182540",
}
SOURCE_CLAUSES = {
    "nonzero_preceding_group": r"\pi^{5}_{10}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8^2}",
    "zero_suspension_of_preceding_group": r"E\pi_{10}^5=0",
    "delta_eta11_image": r"\Delta(\eta_{11})=\nu_5\circ\eta_8^2",
    "hopf_delta_iota13": r"H(\Delta(\iota_{13}))=\pm2\iota_{11}",
    "preceding_free_group_is_conclusion": r"\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}",
    "delta_iso_is_conclusion": r"\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}",
    "target_zero_is_conclusion": r"\pi_{12}^7=0",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, capture_output=True, check=True,
        text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def accepted_source_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return any(blob_sha(x) == expected for x in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def audited_head_pair(local_head: str, remote_head: str) -> dict[str, Any]:
    allowed = (BASE_HEAD, REVIEWED_HEAD)
    if local_head not in allowed or remote_head not in allowed:
        raise RuntimeError("An unreviewed develop HEAD was detected")
    if local_head == REVIEWED_HEAD and remote_head == BASE_HEAD:
        raise RuntimeError("Remote develop moved behind reviewed local HEAD")
    return {
        "local_head": local_head, "remote_head": remote_head,
        "local_equals_remote": local_head == remote_head,
        "reconciliation_before_implementation_required": local_head != remote_head,
    }


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be directly under repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    remote_lines = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote_head = remote_lines.split()[0] if remote_lines else ""
    heads = audited_head_pair(git("rev-parse", "HEAD", cwd=root), remote_head)
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes need separate review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes need separate review")
    for relative, sha in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file() or not accepted_source_blob(file.read_bytes(), sha):
            raise RuntimeError("Source Guard failed: " + relative)
    return {
        "branch": "develop", **heads,
        "verified_source_files": list(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def verify_toda_proof_chain(root: Path = ROOT) -> dict[str, Any]:
    text = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    start = text.index(r"\begin{proposition}\label{prop:5.9}")
    end = text.index(r"\qed", start)
    segment = text[start:end]
    offsets = {key: segment.find(value) for key, value in SOURCE_CLAUSES.items()}
    if any(offset < 0 for offset in offsets.values()):
        raise RuntimeError("Reviewed Toda Proposition 5.9 transcription changed")
    ordered = (
        "zero_suspension_of_preceding_group",
        "preceding_free_group_is_conclusion",
        "delta_iso_is_conclusion",
        "target_zero_is_conclusion",
    )
    if [offsets[key] for key in ordered] != sorted(offsets[key] for key in ordered):
        raise RuntimeError("Reviewed Toda argument order changed")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "verified_clauses": list(SOURCE_CLAUSES),
        "proof_offsets": offsets,
        "original_print_edition_verified": False,
        "source_conclusions_never_used_as_given": True,
        "pi10_5_nonzero_but_suspension_zero": True,
    }


def prior_path(label: str, filename: str) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / label / filename


def validate_prior_evidence(r2: dict[str, Any], r3: dict[str, Any]) -> dict[str, Any]:
    if (r2.get("phase") != "174-R3-R7-R2"
            or r2.get("gate") != "PASS_READ_ONLY_TYPED_EHP_CHAIN"):
        raise RuntimeError("R3-R7-R2 audit evidence is invalid")
    if (r3.get("phase") != "174-R3-R7-R3"
            or r3.get("gate") != "PASS_ISOLATED_RULE_DELTA_SURJECTIVITY_PENDING"):
        raise RuntimeError("R3-R7-R3 audit evidence is invalid")
    live = r2.get("live_obligations") or {}
    counts = live.get("obligations") or {}
    expected = {"delta_surjectivity": 0, "delta_e_exactness": 1, "e_h_exactness": 1}
    if any((counts.get(key) or {}).get("proposal_count") != value
           for key, value in expected.items()):
        raise RuntimeError("Prior EHP candidate counts changed")
    pi = live.get("pi11_6") or {}
    if (pi.get("search_status") != "search_failed"
            or len(pi.get("open_goal_types", [])) != 2):
        raise RuntimeError("Prior pi11_6 open goals changed")
    candidate = r3.get("new_candidate") or {}
    delta = (candidate.get("separate_premises") or {}).get("delta_surjectivity") or {}
    if (candidate.get("isolated_generic_root_proposals") != 1
            or delta.get("proposal_count") != 0
            or candidate.get("not_registered_with_production_provider") is not True):
        raise RuntimeError("Prior isolated EHP rule gap changed")
    if r3.get("new_group_given") != 0 or r3.get("new_production_inference_rules") != 0:
        raise RuntimeError("Unapproved GIVEN or production rule detected")
    return {
        "r2_gate": r2["gate"], "r3_gate": r3["gate"],
        "pi11_6_open_goal_types": pi["open_goal_types"],
        "pi11_6_root_and_open_goal_frontier": pi.get("candidate_frontier", []),
        "delta_surjectivity_candidate_count": 0,
        "isolated_zero_root_is_not_proof": True,
    }


def exactness_diagnostic_goals() -> dict[str, object]:
    from homotopy_groups import (
        TodaDeltaMap, TodaEHPExactnessWindow, TodaHopfInvariantMap,
        TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
    )
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from toda_rules import TodaProp42ExactnessStatement

    lower = TodaPrimaryGroup(10, 5)
    middle = TodaPrimaryGroup(11, 6)
    target = TodaPrimaryGroup(11, 11)
    delta_target = TodaPrimaryGroup(9, 5)
    top = TodaPrimaryGroup(13, 13)
    eh = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        lower, middle, target, EHP_E_MAP, EHP_H_MAP,
    ))
    hd = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        middle, target, delta_target, EHP_H_MAP, EHP_DELTA_MAP,
    ))
    if prop42_exactness_indices(eh) != (5, 11, "e_h"):
        raise RuntimeError("E-H window dimensions changed")
    if prop42_exactness_indices(hd) != (5, 11, "h_delta"):
        raise RuntimeError("H-Delta window dimensions changed")
    return {
        "delta_surjectivity": MapSurjective(TodaDeltaMap(top, middle)),
        "eh_exactness": eh,
        "hd_exactness": hd,
        "hopf_injectivity": MapInjective(TodaHopfInvariantMap(middle, target)),
        "false_pi10_5_zero_shortcut": TodaPrimaryGroupZeroStatement(lower),
    }


def inspect_live_delta_frontier() -> dict[str, Any]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import (
        registered_group_goal_candidates, search_group_from_registered_goal,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target)
    screened = prefer_universal_prop42_derivation(screened)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    goals = exactness_diagnostic_goals()
    if is_exact_given(target, admitted):
        raise RuntimeError("Goal pi12_7=0 is an inadmissible direct GIVEN")
    for key in ("delta_surjectivity", "false_pi10_5_zero_shortcut"):
        if is_exact_given(goals[key], admitted):
            raise RuntimeError("Unproved or false statement admitted as GIVEN")
    provider = shared_expansion_provider(screened, proof_target=target)
    branches = {
        name: summarize_proposals(provider, goal, admitted, limit=8)
        for name, goal in goals.items()
    }
    if branches["delta_surjectivity"]["proposal_count"] != 0:
        raise RuntimeError("Previous Delta-surjectivity gap unexpectedly changed")
    if (branches["eh_exactness"]["proposal_count"] < 1
            or branches["hd_exactness"]["proposal_count"] < 1):
        raise RuntimeError("The cited Proposition 4.2 windows are unavailable")
    hopf_candidates = expand_generic_ehp_hopf_goal(goals["hopf_injectivity"])
    if (len(hopf_candidates) != 1
            or goals["false_pi10_5_zero_shortcut"] not in hopf_candidates[0].subgoals):
        raise RuntimeError("Generic Hopf injectivity shortcut contract changed")
    # These are independent live searches. The database selects goals, never proofs.
    neighbors: dict[str, Any] = {}
    for n, k in ((5, 5), (5, 4)):
        label = f"pi_{n+k}^{n}"
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        candidates = registered_group_goal_candidates(bridge, n=n, k=k)
        neighbors[label] = {
            "registered_goal_count": len(candidates),
            "search_status": getattr(result.status, "value", str(result.status)),
            "proven_steps": len(result.proven_steps),
            "open_goals": [
                {"type": type(goal).__name__, "repr": repr(goal)[:1000]}
                for goal in result.open_goals
            ],
            "registered_goal_is_not_evidence": True,
        }
    return {
        "screening": "independent_source_screened",
        "screened_given_count": len(admitted),
        "candidate_obligations": branches,
        "hopf_injectivity_generic_subgoals": [
            {"type": type(goal).__name__, "repr": repr(goal)}
            for goal in hopf_candidates[0].subgoals
        ],
        "pi10_5_zero_shortcut_invalid": True,
        "neighbor_groups": neighbors,
        "delta_surjectivity_still_unproved": True,
        "new_proof_steps_by_audit": 0,
    }


def report_location() -> Path:
    return prior_path("phase174_r3_r7_r4", "delta_surjectivity_audit.json")


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_and_sources(root)
    source = verify_toda_proof_chain(root)
    p2 = prior_path("phase174_r3_r7_r2", "ehp_chain_audit.json")
    p3 = prior_path("phase174_r3_r7_r3", "generic_zero_rule.json")
    if not p2.is_file() or not p3.is_file():
        raise RuntimeError("Previous R3-R7-R2 and R3-R7-R3 audit JSON files are required")
    prior = validate_prior_evidence(
        json.loads(p2.read_text(encoding="utf-8-sig")),
        json.loads(p3.read_text(encoding="utf-8-sig")),
    )
    live = None if dry_run else inspect_live_delta_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_DELTA_SURJECTIVITY_GAP",
        "git_state": state,
        "source_review": source,
        "prior_evidence": prior,
        "live": live,
        "source_is_not_target_given": True,
        "new_group_given": 0,
        "new_inference_rules": 0,
        "production_files_changed": False,
        "full_pytest_run": False,
        "completion_claimed": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_READ_ONLY_DELTA_SURJECTIVITY_GAP",
    }


def main() -> int:
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--dry-run", action="store_true")
    parsed = args.parse_args()
    report = make_report(dry_run=parsed.dry_run)
    destination = report_location()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R4_"
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "NONZERO_PI105_AND_ZERO_SUSPENSION=VERIFIED_TRANSCRIPTION")
    print(prefix + "PREVIOUS_DELTA_SURJECTIVITY_PROPOSALS=0")
    if report["live"] is not None:
        for name, summary in report["live"]["candidate_obligations"].items():
            print(prefix + "GOAL_" + name.upper() + "_PROPOSALS=" + str(
                summary["proposal_count"]
            ))
        for name, item in report["live"]["neighbor_groups"].items():
            print(prefix + "GROUP_" + name.replace("^", "_") + "_STATUS=" + item["search_status"])
            print(prefix + "GROUP_" + name.replace("^", "_") + "_OPEN=" + str(
                len(item["open_goals"])
            ))
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
