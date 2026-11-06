"""Phase 174 R3-R7-R5: isolated generic image-zero/Hopf-injectivity audit.

No production module, group database, public provider or renderer is changed.
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
PHASE = "174-R3-R7-R5"
REVIEWED_HEAD = "1f3a61d7d6cfc7854e56c4f5c372bf5c71e203df"
# Reviewed on 2026-11-06: exactly one successor commit added only
# phase174_r3_r7_r4_delta_surjectivity_audit/ package files. All nine
# pinned source blobs below are unchanged. No other successor is accepted.
REVIEWED_R4_SUCCESSOR_HEAD = "db9ef1cd1560744352bced43d3b4e1b95003edfb"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "map_property_rules.py": "4adeebc9dedb3daf210cd8755be811aca32f1e8b",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r12_r12_ehp_consequences.py": "895dc98ad4d25f14fb7aac8fa52460a77fd049bc",
    "phase165_r14_r9_ehp_exactness.py": "c39759f0b693ce89100ef8439e8aec7fe325694f",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
}
TODA_CLAUSES = {
    "nonzero_group": r"\pi^{5}_{10}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8^2}",
    "suspension_of_generator_zero": (
        r"E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0"
    ),
    "zero_suspension_image": r"E\pi_{10}^5=0",
    "free_group_later_conclusion": r"\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=True,
    )
    return result.stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def accepted_source_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return any(blob_sha(item) == expected for item in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def reviewed_develop_head_pair(local: str, remote: str) -> bool:
    """Accept only identical, individually reviewed develop commits.

    The one reviewed successor to R5's original HEAD introduces the R4R1
    audit package only; pinned mathematical sources are checked separately.
    """
    return (
        local == remote
        and local in (REVIEWED_HEAD, REVIEWED_R4_SUCCESSOR_HEAD)
    )


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be directly under the repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if not reviewed_develop_head_pair(local, remote):
        raise RuntimeError("Unreviewed develop HEAD: source review is required")
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes require review")
    for path, expected in SOURCE_BLOBS.items():
        p = root / path
        if not p.is_file() or not accepted_source_blob(p.read_bytes(), expected):
            raise RuntimeError("Pinned source changed: " + path)
    return {
        "local_head": local,
        "remote_head": remote,
        "branch": "develop",
        "source_guard": "PASS",
        "reviewed_files": list(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def verify_toda_source(root: Path = ROOT) -> dict[str, Any]:
    text = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    start = text.index(r"\begin{proposition}\label{prop:5.9}")
    end = text.index(r"\qed", start)
    section = text[start:end]
    offsets = {key: section.find(value) for key, value in TODA_CLAUSES.items()}
    if any(value < 0 for value in offsets.values()):
        raise RuntimeError("Toda Proposition 5.9 cited transcription changed")
    if not (offsets["nonzero_group"] < offsets["suspension_of_generator_zero"]
            < offsets["zero_suspension_image"]
            < offsets["free_group_later_conclusion"]):
        raise RuntimeError("Toda source premise/conclusion order changed")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "clauses": list(TODA_CLAUSES),
        "source_offsets": offsets,
        "printed_edition_independently_verified": False,
        "source_conclusion_is_not_given": True,
    }


def prior_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return (
        base / "EHPProofTracerAudit" / "phase174_r3_r7_r4"
        / "delta_surjectivity_audit.json"
    )


def validate_r4_evidence(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R4"
            or report.get("gate") != "PASS_READ_ONLY_DELTA_SURJECTIVITY_GAP"):
        raise RuntimeError("R4 certified audit gate is absent")
    if (report.get("new_group_given") != 0
            or report.get("new_inference_rules") != 0
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R4 audit changed proof evidence or completion claims")
    source = report.get("source_review") or {}
    if source.get("pi10_5_nonzero_but_suspension_zero") is not True:
        raise RuntimeError("R4 source nonzero-group/zero-image distinction absent")
    live = report.get("live") or {}
    candidates = live.get("candidate_obligations") or {}
    expected = {
        "delta_surjectivity": 0,
        "eh_exactness": 1,
        "hd_exactness": 1,
        "hopf_injectivity": 1,
        "false_pi10_5_zero_shortcut": 0,
    }
    if any((candidates.get(name) or {}).get("proposal_count") != count
           for name, count in expected.items()):
        raise RuntimeError("R4 observed candidate frontier changed")
    neighbors = live.get("neighbor_groups") or {}
    for label in ("pi_10^5", "pi_9^5"):
        item = neighbors.get(label) or {}
        if (item.get("search_status") != "search_failed"
                or len(item.get("open_goals", [])) != 3):
            raise RuntimeError("R4 neighboring group search evidence changed")
    return {
        "gate": report["gate"],
        "observed_counts": expected,
        "neighbor_search_status": {
            label: neighbors[label]["search_status"]
            for label in ("pi_10^5", "pi_9^5")
        },
        "source_zero_map_is_not_proven_step": True,
    }


def inspect_screened_zero_image_frontier() -> dict[str, Any]:
    from homotopy_groups import (
        TodaHopfInvariantMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
    )
    from map_property_rules import ImageZeroStatement
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
    from phase165_r14_r6_generic_iso import MapInjective
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        expand_hopf_injective_from_zero_image,
        hopf_injectivity_from_zero_image_inputs,
    )
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    target_zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target_zero)
    screened = prefer_universal_prop42_derivation(screened)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if is_exact_given(target_zero, admitted):
        raise RuntimeError("Forbidden direct zero-group GIVEN encountered")
    provider = shared_expansion_provider(screened, proof_target=target_zero)
    hopf_goal = MapInjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(11, 6), TodaPrimaryGroup(11, 11),
    ))
    inputs = hopf_injectivity_from_zero_image_inputs(hopf_goal)
    if inputs is None or not isinstance(inputs[0], ImageZeroStatement):
        raise RuntimeError("Generic image-zero antecedent is malformed")
    if is_exact_given(inputs[0], admitted):
        raise RuntimeError("Unscreened zero-image fact was inserted as GIVEN")
    options = expand_hopf_injective_from_zero_image(hopf_goal)
    if len(options) != 1 or options[0].subgoals != inputs:
        raise RuntimeError("Expected exactly one isolated generic alternative")
    old = expand_generic_ehp_hopf_goal(hopf_goal)
    if len(old) != 1:
        raise RuntimeError("Previous zero-group shortcut rule changed")
    return {
        "source_screening": "independent_source_screened",
        "screened_given_count": len(admitted),
        "isolated_hopf_injectivity_candidate_count": len(options),
        "isolated_subgoals": [
            {"type": type(x).__name__, "repr": repr(x)[:1000]} for x in inputs
        ],
        "production_hopf_injectivity_frontier": summarize_proposals(
            provider, hopf_goal, admitted,
        ),
        "production_zero_image_frontier": summarize_proposals(
            provider, inputs[0], admitted,
        ),
        "production_eh_exactness_frontier": summarize_proposals(
            provider, inputs[1], admitted,
        ),
        "old_zero_group_shortcut": [
            {"type": type(x).__name__, "repr": repr(x)[:1000]}
            for x in old[0].subgoals
        ],
        "isolated_candidate_is_not_proof": True,
        "new_verified_proof_steps": 0,
        "no_public_provider_wiring": True,
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return (
        base / "EHPProofTracerAudit" / "phase174_r3_r7_r5"
        / "zero_image_hopf_injective.json"
    )


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    source = verify_toda_source(root)
    previous = prior_path()
    if not previous.is_file():
        raise RuntimeError("R3-R7-R4 certified audit JSON is required")
    prior = validate_r4_evidence(json.loads(previous.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_screened_zero_image_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_ISOLATED_RULE",
        "git_state": git_state,
        "source_review": source,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "production_files_changed": False,
        "full_pytest_run": False,
        "completion_claimed": False,
        "gate": (
            "PASS_PREFLIGHT" if dry_run
            else "PASS_ISOLATED_HOPF_INJECTIVITY_ZERO_IMAGE_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    destination = report_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R5_"
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "R4_OBSERVED_DELTA_SURJECTIVITY_PROPOSALS=0")
    print(prefix + "SOURCE_PI105_NONZERO_BUT_E_IMAGE_ZERO=VERIFIED_TRANSCRIPTION")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "ISOLATED_HOPF_INJECTIVITY_PROPOSALS=" + str(
            live["isolated_hopf_injectivity_candidate_count"]
        ))
        for name, key in (
            ("PRODUCTION_IMAGE_ZERO", "production_zero_image_frontier"),
            ("PRODUCTION_EH_EXACTNESS", "production_eh_exactness_frontier"),
            ("PRODUCTION_HOPF_INJECTIVITY", "production_hopf_injectivity_frontier"),
        ):
            print(prefix + name + "_PROPOSALS=" + str(
                live[key]["proposal_count"]
            ))
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
