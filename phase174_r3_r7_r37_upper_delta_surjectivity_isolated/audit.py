"""R37 source-first preflight and isolated upper Delta surjectivity audit."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "92e3e639cd84f53028b11ac49b87908a630a69c8"
REVIEWED_HEAD = "660cadd928a2cbca00f71c5c35cd3af1230a54e9"
R36_TRACKED = "phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py"
PINS = {
    R36_TRACKED: "da8036f299a02445c5b5b0743919640ca1524354",
    "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py": "fac88c852cd4c18e8d013e3dc12ab95ad57d7b03",
    "phase174_r3_r7_r36_cited_kernel_provider_wiring/audit.py": "b3d74e831edb49a60a54c5b609394fd815870068",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r25_prop27_isolated_inference/rule.py": "e5ab7aa7a88f8ce49844ced057a81bd34c9a1e3b",
    "phase165_r12_r12_ehp_consequences.py": "895dc98ad4d25f14fb7aac8fa52460a77fd049bc",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, text=True,
        capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def reviewed_blob(data: bytes, sha: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return len(sha) == 40 and any(
        blob_sha(content) == sha for content in (
            data, normalized, normalized.replace(b"\n", b"\r\n"),
        )
    )


def verify_checkout() -> dict[str, object]:
    """Require a reviewed R36 merge or preserved, uncommitted R36 patch."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R37 directly at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R37 requires develop branch")
    local = git("rev-parse", "HEAD")
    remote_info = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_info.split()[0] if remote_info else ""
    if remote != REVIEWED_HEAD or local not in (BASE_HEAD, REVIEWED_HEAD):
        raise RuntimeError("R36 handoff HEAD changed; review before R37")
    staged = git("diff", "--cached", "--name-only").splitlines()
    if staged:
        raise RuntimeError("Staged edits require review: " + repr(staged))
    changed = git("diff", "--name-only").splitlines()
    if changed and (local != BASE_HEAD or changed != [R36_TRACKED]):
        raise RuntimeError("Unexpected tracked edits; do not reset: " + repr(changed))
    for path, sha in PINS.items():
        local_file = ROOT / path
        if not local_file.is_file() or not reviewed_blob(local_file.read_bytes(), sha):
            raise RuntimeError("Reviewed source differs: " + path)
    return {
        "local_head": local, "remote_head": remote,
        "source_guard": "PASS", "r36_preserved": True,
        "handoff_mode": "UNMERGED_REVIEWED_R36" if local == BASE_HEAD else "MERGED_REVIEWED_R36",
        "reviewed_pin_count": len(PINS),
    }


def inspect_isolated_upper_delta() -> dict[str, object]:
    """Inspect real R36 kernel path and the four distinct upper Delta obligations."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization
    from phase174_r3_r7_r36_cited_kernel_provider_wiring.audit import (
        audit_public_connection,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME,
        expand_upper_delta_surjectivity,
        upper_delta_surjectivity_inputs,
    )
    from proof import ProofRule

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    root_prerequisites = ehp_zero_inputs(root)
    if root_prerequisites is None or type(root_prerequisites[0]) is not MapSurjective:
        raise RuntimeError("R3 zero goal no longer has correct upper Delta obligation")
    goal = root_prerequisites[0]
    prerequisite_set = upper_delta_surjectivity_inputs(goal)
    proposals = expand_upper_delta_surjectivity(goal)
    if (prerequisite_set is None or len(proposals) != 1
            or proposals[0].subgoals != prerequisite_set
            or proposals[0].rule.name != RULE_NAME):
        raise RuntimeError("R37 general upper Delta rule failed typed expansion")
    r36 = audit_public_connection()
    if (not r36["kernel_inference_in_audit"]
            or not r36["diagonal_source_inferred"]):
        raise RuntimeError("R36 certified-kernel inputs have regressed")
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    provider = shared_expansion_provider(bridge, proof_target=root)
    prop27_options = provider(typed_specialization(6))
    if not any(o.subgoals for o in prop27_options):
        raise RuntimeError("Positioned Proposition 2.7 instance not publicly proposed")
    public_upper = tuple(
        proposal for proposal in provider(goal)
        if getattr(proposal.rule, "name", None) == RULE_NAME
    )
    injection_zero_image = hopf_injectivity_from_zero_image_inputs(prerequisite_set[0])
    if injection_zero_image is None:
        raise RuntimeError("R5 Hopf injectivity prerequisites not well typed")
    screened_zero_images = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == injection_zero_image[0]
    )
    source = (ROOT / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    p59 = source.index(r"\begin{proposition}\label{prop:5.9}")
    lemma = source.index(r"\begin{lemma}\label{lemma:5.10}", p59)
    if r"E\pi_{10}^5=0" not in source[p59:lemma]:
        raise RuntimeError("Toda proof zero-suspension-image dependency changed")
    return {
        "isolated_upper_surjectivity_expansions": len(proposals),
        "four_independent_obligations_typed": len(prerequisite_set) == 4,
        "r36_kernel_inference_audit_preserved": True,
        "prop27_public_instance_proposed": True,
        "actual_zero_suspension_image_source_leaves": len(screened_zero_images),
        "zero_image_independently_proved_in_r37": False,
        "upper_delta_surjectivity_proved_in_r37": False,
        "public_upper_surjectivity_provider_connected_in_r37": bool(public_upper),
        "web_http_checked": False,
        "root_complete": False,
        "new_givens": 0,
        "new_public_math_rules": 0,
        "full_pytest": False,
    }


def report(dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    details = None if dry_run else inspect_isolated_upper_delta()
    return {
        "phase": "174-R3-R7-R37",
        "git_state": state,
        "details": details,
        "gate": (
            "PASS_R37_REVIEWED_SOURCE_PREFLIGHT_ONLY" if dry_run else
            "PASS_R37_CONDITIONAL_UPPER_DELTA_SURJECTIVITY_ISOLATED_IMAGE_ZERO_AND_PUBLIC_WIRING_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(args.dry_run)
    output_dir = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r37"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / ("preflight.json" if args.dry_run else "upper_delta_conditional.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R37_"
    for key, val in result["git_state"].items():
        print(prefix + key.upper() + "=" + str(val))
    if result["details"] is not None:
        for key, val in result["details"].items():
            print(prefix + key.upper() + "=" + str(val))
    print(prefix + "REPORT=" + str(output))
    print(prefix + "GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
