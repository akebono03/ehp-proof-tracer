"""Phase 174 R3-R7-R7: source-first audit of a composite zero generator.

Reads the previously certified R6 evidence, verifies the Toda transcription,
and checks only source-screened backward proposals. No proof is created.
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
PHASE = "174-R3-R7-R7"
BASE_HEAD = "cbe3b866b1e39f15fc1c6965004b705e31d61de5"
REVIEWED_R6_HEAD = "67c57fc9ae63ce783ffdf9b502d472900abad57f"
ALLOWED_SUCCESSOR_PREFIX = "phase174_r3_r7_r6_cyclic_generator_zero_image/"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py": "66407339808ed4ba8a65c04fd3bfbbf05bde6745",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/audit.py": "8dff5c0a38558648b8894539c8b12929febd734a",
}
TODA_CLAUSES = {
    "annihilator_family": r"\nu_n\circ \eta_{n+3}=0\ (n\ge6)",
    "suspension_equals_composite_zero": (
        r"E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0"
    ),
    "zero_image_is_later_conclusion": r"E\pi_{10}^5=0",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def accepted_source_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return any(blob_sha(candidate) == expected for candidate in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def reviewed_head_lineage(
    local: str,
    remote: str,
    successors: tuple[str, ...],
    changed_paths: tuple[str, ...],
) -> str:
    if local != remote or len(local) != 40:
        raise RuntimeError("Local/remote develop HEAD mismatch")
    if local == BASE_HEAD and not successors and not changed_paths:
        return "REVIEWED_BASE"
    if (local == REVIEWED_R6_HEAD
            and successors == (REVIEWED_R6_HEAD,)
            and changed_paths
            and all(path.startswith(ALLOWED_SUCCESSOR_PREFIX)
                    for path in changed_paths)):
        return "REVIEWED_R6_ONLY_SUCCESSOR"
    raise RuntimeError("Unreviewed develop HEAD or changed sources")


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be under repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes require review")
    if local == BASE_HEAD:
        successors: tuple[str, ...] = ()
        changed_paths: tuple[str, ...] = ()
    else:
        subprocess.run(
            ("git", "merge-base", "--is-ancestor", BASE_HEAD, local),
            cwd=root, check=True, capture_output=True,
        )
        successors = tuple(git(
            "rev-list", "--reverse", f"{BASE_HEAD}..{local}", cwd=root,
        ).splitlines())
        changed_paths = tuple(git(
            "diff", "--name-only", f"{BASE_HEAD}..{local}", cwd=root,
        ).splitlines())
    lineage = reviewed_head_lineage(local, remote, successors, changed_paths)
    for relative, expected in SOURCE_BLOBS.items():
        path = root / relative
        if (not path.is_file()
                or not accepted_source_blob(path.read_bytes(), expected)):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "head_lineage": lineage,
        "source_guard": "PASS",
        "reviewed_source_files": list(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def verify_toda_source(root: Path = ROOT) -> dict[str, Any]:
    body = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    start = body.index(r"\begin{proposition}\label{prop:5.9}")
    end = body.index(r"\qed", start)
    section = body[start:end]
    offsets = {key: section.find(value) for key, value in TODA_CLAUSES.items()}
    if (any(offset < 0 for offset in offsets.values())
            or not (offsets["annihilator_family"]
                    < offsets["suspension_equals_composite_zero"]
                    < offsets["zero_image_is_later_conclusion"])):
        raise RuntimeError("Toda (5.9) or Proposition 5.9 proof transcription differs")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "locator": "Toda Proposition 5.9 proof, equation (5.9)",
        "clause_offsets": offsets,
        "printed_edition_independently_verified": False,
        "typed_specialization_not_assumed_proved": True,
        "zero_image_conclusion_not_given": True,
    }


def prior_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r6" / "cyclic_generator_zero_image.json"


def validate_r6_evidence(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R6"
            or report.get("gate") != "PASS_ISOLATED_CYCLIC_ZERO_IMAGE_CHILDREN_UNPROVEN"):
        raise RuntimeError("Certified R6 full audit gate required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("completion_claimed") is not False
            or report.get("public_provider_changed") is not False):
        raise RuntimeError("R6 trust contract differs")
    live = report.get("live") or {}
    expected = {
        "isolated_zero_image_candidate_count": 1,
        "production_image_zero_frontier": 0,
        "production_presentation_frontier": 3,
        "production_generator_zero_frontier": 0,
    }
    if live.get("isolated_zero_image_candidate_count") != 1:
        raise RuntimeError("R6 generic candidate count differs")
    for key, count in expected.items():
        if key.startswith("production_") and (live.get(key) or {}).get("proposal_count") != count:
            raise RuntimeError("R6 observed child candidates differ: " + key)
    if (live.get("registered_presentation_is_not_proof") is not True
            or live.get("public_provider_unchanged") is not True):
        raise RuntimeError("R6 evidence screening differs")
    return {
        "gate": report["gate"],
        "production_generator_zero_proposals": 0,
        "completion_claimed": False,
    }


def inspect_composite_frontier() -> dict[str, Any]:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from map_property_rules import ImageZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        cyclic_generator_zero_image_inputs,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import (
        composite_zero_generator_inputs, expand_generator_zero_from_composite,
    )
    from phase174_r3_r7_source_first_audit.audit import is_exact_given, summarize_proposals
    from proof import ProofRule, Relation, RelationType
    from homotopy_groups import FiniteCyclicGroup

    target_zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target_zero)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=target_zero)
    presentation = exact_prior_database_result(5, 5)
    if (not isinstance(presentation, Relation)
            or presentation.relation_type is not RelationType.EQUALITY
            or presentation.lhs != TodaPrimaryGroup(10, 5)
            or not isinstance(presentation.rhs, FiniteCyclicGroup)
            or presentation.rhs.order != 2):
        raise RuntimeError("R6 source-screened finite cyclic presentation changed")
    suspension = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6))
    image_zero_goal = ImageZeroStatement(suspension)
    r6_children = cyclic_generator_zero_image_inputs(image_zero_goal, presentation)
    if r6_children is None:
        raise RuntimeError("R6 typed child construction changed")
    generator_zero = r6_children[1]
    nu6 = HomotopyElement(
        "nu_6", dimension=6, source=9, target=6,
        generator=GeneratorSymbol("nu", 6),
    )
    eta9 = HomotopyElement(
        "eta_9", dimension=9, source=10, target=9,
        generator=GeneratorSymbol("eta", 9),
    )
    eta10 = HomotopyElement(
        "eta_10", dimension=10, source=11, target=10,
        generator=GeneratorSymbol("eta", 10),
    )
    left = Composition(nu6, eta9)
    mapped_composite = Composition(left, eta10)
    image_candidate = GeneratorImage(
        suspension, generator_zero.source_generator, mapped_composite,
    )
    required = composite_zero_generator_inputs(generator_zero, image_candidate)
    options = expand_generator_zero_from_composite(generator_zero, image_candidate)
    if (required is None or len(options) != 1
            or options[0].subgoals != required
            or required[1].lhs != left
            or required[1].rhs != Zero()):
        raise RuntimeError("Typed source-factorization candidate invalid")
    if any(is_exact_given(item, admitted) for item in (
        target_zero, image_zero_goal, generator_zero, image_candidate, required[1],
    )):
        raise RuntimeError("Target, generator, or composed identity was GIVEN")
    return {
        "source_screening": "independent_source_screened",
        "candidate_from_toda_text_is_not_evidence": True,
        "registered_presentation_is_not_proof": True,
        "isolated_generator_zero_candidate_count": len(options),
        "typed_children": [
            {"type": type(item).__name__, "repr": repr(item)[:1500]}
            for item in required
        ],
        "public_composite_image_frontier": summarize_proposals(
            provider, required[0], admitted,
        ),
        "public_left_factor_zero_frontier": summarize_proposals(
            provider, required[1], admitted,
        ),
        "public_generator_zero_frontier": summarize_proposals(
            provider, generator_zero, admitted,
        ),
        "public_provider_unchanged": True,
        "new_verified_steps": 0,
    }


def output_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r7" / "composite_zero_audit.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    github = verify_git_and_sources(root)
    source = verify_toda_source(root)
    path = prior_report_path()
    if not path.is_file():
        raise RuntimeError("R6 full audit report is required")
    prior = validate_r6_evidence(json.loads(path.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_composite_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_ISOLATED_RULE",
        "git_state": github,
        "source_review": source,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "gate": (
            "PASS_PREFLIGHT" if dry_run
            else "PASS_ISOLATED_COMPOSITE_ZERO_CHILDREN_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R7_"
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["head_lineage"])
    print(prefix + "TODA59_ANHILATOR=VERIFIED_TRANSCRIPTION")
    print(prefix + "R6_GENERATOR_ZERO_PROPOSALS=0")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "ISOLATED_COMPOSITE_ZERO_PROPOSALS=" + str(
            live["isolated_generator_zero_candidate_count"]
        ))
        for label, key in (
            ("PUBLIC_COMPOSITE_IMAGE", "public_composite_image_frontier"),
            ("PUBLIC_LEFT_FACTOR_ZERO", "public_left_factor_zero_frontier"),
            ("PUBLIC_GENERATOR_ZERO", "public_generator_zero_frontier"),
        ):
            print(prefix + label + "_PROPOSALS=" + str(
                live[key]["proposal_count"]
            ))
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
