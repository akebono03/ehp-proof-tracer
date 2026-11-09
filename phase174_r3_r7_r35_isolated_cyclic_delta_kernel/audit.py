"""R35: read-only source-first audit of the isolated cyclic Delta kernel rule."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "89fcf47a22dbb212fe635381fa5af3095d5c1527"
REVIEWED_HEAD = "4200211563834028ed6c4e2eeb01004646b92ba9"
R34_TRACKED = "phase165_r52_r9_shared_math.py"
PINS = {
    "phase165_r52_r9_shared_math.py": "6b965aa49db2ad8707c75dcc953d3c78cdd3e458",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/source.py": "b90fe1fee5db04228ed986083b5214709045a7ea",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_public.py": "6d32a6b7768245770bc14524b866fd2e8ef50db6",
    "phase165_r57_r20_general_specialization.py": "e09603bee51d776cd4326a95930fc9c41f272a1b",
    "phase174_r3_r7_r32_lower_delta_kernel_audit/kernel_contract.py": "c2357859b00ed0b446bac7a060a6d0c134fc7de5",
    "phase165_r12_r2_quotient_rules.py": "2b3e8e0449382e9245ee22f08501e9cede0a5b59",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, text=True,
        capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def same_reviewed_blob(data: bytes, sha: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return len(sha) == 40 and any(
        blob_sha(candidate) == sha for candidate in (
            data, normalized, normalized.replace(b"\n", b"\r\n"),
        )
    )


def verify_checkout() -> dict[str, object]:
    """Do not reset the user's R34 uncommitted/merged handoff."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R35 directly into the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R35 requires develop")
    local = git("rev-parse", "HEAD")
    remote_output = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_output.split()[0] if remote_output else ""
    if remote != REVIEWED_HEAD or local not in (BASE_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Unreviewed GitHub/local HEAD; re-audit before R35")
    staged = git("diff", "--cached", "--name-only").splitlines()
    if staged:
        raise RuntimeError("Staged edits require review")
    changed = git("diff", "--name-only").splitlines()
    if changed and (local != BASE_HEAD or changed != [R34_TRACKED]):
        raise RuntimeError("Unexpected tracked edits; no reset performed")
    for path, sha in PINS.items():
        file = ROOT / path
        if not file.is_file() or not same_reviewed_blob(file.read_bytes(), sha):
            raise RuntimeError("Reviewed code/source differs: " + path)
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "r34_mode": "UNMERGED_REVIEWED" if local == BASE_HEAD else "MERGED_REVIEWED",
        "tracked_edits_preserved": changed,
        "reviewed_pin_count": len(PINS),
    }


def inspect_isolated_frontier() -> dict[str, object]:
    """Observe the real screened citations, general diagonal and isolated rule."""
    from homotopy_groups import (
        FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup,
        TodaPrimaryGroupZeroStatement,
    )
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r57_r20_general_specialization import (
        expand_cited_general_specialization,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import (
        RULE_NAME, expand_cyclic_delta_kernel,
    )
    from proof import ProofRule, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement

    target_root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=target_root,
    )
    steps = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    delta = TodaDeltaMap(TodaPrimaryGroup(11, 11), TodaPrimaryGroup(9, 5))
    image = tuple(
        s.conclusion for s in steps
        if type(s.conclusion) is TodaDeltaImageUpToSignStatement
        and s.conclusion.map == delta
    )
    target = tuple(
        s.conclusion for s in steps
        if type(s.conclusion) is Relation
        and s.conclusion.relation_type is RelationType.EQUALITY
        and s.conclusion.lhs == delta.target_group
    )
    if len(image) != 1 or len(target) != 1:
        raise RuntimeError("R34 earlier two cited source steps not available")
    goal = KernelMultipleStatement(delta, delta.source_group, image[0].element, 2)
    proposals = expand_cyclic_delta_kernel(goal, tuple(s.conclusion for s in steps))
    if len(proposals) != 1 or proposals[0].rule.name != RULE_NAME:
        raise RuntimeError("R35 isolated kernel rule failed to recognize actual R34 source")
    source_goal = Relation(
        delta.source_group, FreeCyclicGroup(image[0].element), RelationType.EQUALITY,
    )
    if proposals[0].subgoals != (source_goal, target[0], image[0]):
        raise RuntimeError("R35 did not preserve exact R34 generator/source identity")
    general_diagonal = expand_cited_general_specialization(
        source_goal, tuple(s.conclusion for s in steps),
    )
    return {
        "screened_cited_codomain": 1,
        "screened_cited_signed_image": 1,
        "composite_generator_preserved": True,
        "isolated_kernel_expansions": len(proposals),
        "diagonal_generic_specialization_proposals": len(general_diagonal),
        "diagonal_proof_certified_by_audit": False,
        "kernel_proof_certified_by_audit": False,
        "shared_provider_connected_in_r35": False,
        "new_givens": 0,
        "new_direct_kernel_givens": 0,
        "new_direct_root_givens": 0,
        "new_general_rules_installed_in_public_provider": 0,
        "root_complete": False,
        "full_pytest": False,
    }


def report(dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    frontier = None if dry_run else inspect_isolated_frontier()
    return {
        "phase": "174-R3-R7-R35",
        "git_state": state,
        "frontier": frontier,
        "gate": (
            "PASS_R35_SOURCE_PREFLIGHT_ONLY" if dry_run else
            "PASS_R35_ISOLATED_COMPOSITE_KERNEL_RULE_AUDITED_PUBLIC_WIRING_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(args.dry_run)
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r35"
    )
    folder.mkdir(parents=True, exist_ok=True)
    file = folder / ("preflight.json" if args.dry_run else "isolated_kernel_audit.json")
    file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R35_"
    for key in ("local_head", "remote_head", "source_guard", "r34_mode", "reviewed_pin_count"):
        print(prefix + key.upper() + "=" + str(result["git_state"][key]))
    if result["frontier"] is not None:
        for key, val in result["frontier"].items():
            print(prefix + key.upper() + "=" + str(val))
    print(prefix + "REPORT=" + str(file))
    print(prefix + "GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
