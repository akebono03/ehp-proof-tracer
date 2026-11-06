"""Phase 174 R3-R7-R6: read-only, source-first cyclic-generator zero-image audit.

All source and prior-evidence checks fail closed. An isolated candidate does
not certify its two independent children, nor change the public proof engine.
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
PHASE = "174-R3-R7-R6"
REVIEWED_HEAD = "db9ef1cd1560744352bced43d3b4e1b95003edfb"
REVIEWED_R5_SUCCESSOR_HEAD = "cbe3b866b1e39f15fc1c6965004b705e31d61de5"
ALLOWED_SUCCESSOR_PREFIX = "phase174_r3_r7_r5_zero_image_hopf_injective/"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "map_property_rules.py": "4adeebc9dedb3daf210cd8755be811aca32f1e8b",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "phase165_r12_r24_web_search_connection.py": "71d0c6c365a46e833a2bfe304c771d2e010178ca",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase174_r3_r7_r4_delta_surjectivity_audit/audit.py": "25140e70398f1ba00c4a223b7de406242f67ab84",
}
TODA_CLAUSES = {
    "nonzero_group_presentation": r"\pi^{5}_{10}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8^2}",
    "suspended_generator_zero": (
        r"E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0"
    ),
    "zero_image_conclusion": r"E\pi_{10}^5=0",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    )
    return result.stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def accepted_source_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return any(blob_sha(item) == expected for item in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def validate_reviewed_head_lineage(
    local: str, remote: str, successor_commits: tuple[str, ...],
    changed_paths: tuple[str, ...],
) -> str:
    """Accept base or exactly one R5-only successor, never arbitrary HEADs."""
    if local != remote or not local or len(local) != 40:
        raise RuntimeError("Local/remote develop HEAD mismatch")
    if local == REVIEWED_HEAD:
        if successor_commits or changed_paths:
            raise RuntimeError("Base HEAD cannot contain successor changes")
        return "REVIEWED_BASE"
    if (local != REVIEWED_R5_SUCCESSOR_HEAD
            or len(successor_commits) != 1
            or successor_commits[0] != REVIEWED_R5_SUCCESSOR_HEAD
            or not changed_paths
            or any(not path.startswith(ALLOWED_SUCCESSOR_PREFIX)
                   for path in changed_paths)):
        raise RuntimeError("Unreviewed develop HEAD or non-R5 changes")
    return "REVIEWED_R5_ONLY_SUCCESSOR"


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be installed directly under repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes require review")
    if local == REVIEWED_HEAD:
        successor_commits: tuple[str, ...] = ()
        changed_paths: tuple[str, ...] = ()
    else:
        subprocess.run(
            ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, local),
            cwd=root, check=True, capture_output=True,
        )
        successor_commits = tuple(
            git("rev-list", "--reverse", f"{REVIEWED_HEAD}..{local}", cwd=root).splitlines()
        )
        changed_paths = tuple(
            git("diff", "--name-only", f"{REVIEWED_HEAD}..{local}", cwd=root).splitlines()
        )
    lineage = validate_reviewed_head_lineage(local, remote, successor_commits, changed_paths)
    for relative, expected in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file() or not accepted_source_blob(file.read_bytes(), expected):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "branch": "develop",
        "source_guard": "PASS",
        "head_lineage": lineage,
        "successor_changed_paths": list(changed_paths),
        "reviewed_source_files": list(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def verify_toda_source(root: Path = ROOT) -> dict[str, Any]:
    text = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    start = text.index(r"\begin{proposition}\label{prop:5.9}")
    end = text.index(r"\qed", start)
    section = text[start:end]
    positions = {key: section.find(clause) for key, clause in TODA_CLAUSES.items()}
    if (any(offset < 0 for offset in positions.values())
            or not (positions["nonzero_group_presentation"]
                    < positions["suspended_generator_zero"]
                    < positions["zero_image_conclusion"])):
        raise RuntimeError("Toda Proposition 5.9 cited clauses absent or out of order")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "locator": "Proposition 5.9, proof; Equation (5.9)",
        "clause_offsets": positions,
        "printed_edition_independently_verified": False,
        "source_statement_not_admitted_as_given": True,
    }


def prior_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return (
        base / "EHPProofTracerAudit" / "phase174_r3_r7_r5"
        / "zero_image_hopf_injective.json"
    )


def validate_r5_evidence(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R5"
            or report.get("gate") != "PASS_ISOLATED_HOPF_INJECTIVITY_ZERO_IMAGE_PENDING"):
        raise RuntimeError("Certified R5 audit gate is required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R5 proof trust contract changed")
    live = report.get("live") or {}
    if (live.get("isolated_hopf_injectivity_candidate_count") != 1
            or (live.get("production_zero_image_frontier") or {}).get("proposal_count") != 0
            or (live.get("production_eh_exactness_frontier") or {}).get("proposal_count") != 1
            or live.get("no_public_provider_wiring") is not True):
        raise RuntimeError("R5 observed zero-image frontier changed")
    return {
        "gate": report["gate"],
        "production_image_zero_proposals": 0,
        "isolated_hopf_injectivity_proposals": 1,
        "prior_complete_proof_claimed": False,
    }


def inspect_screened_cyclic_generator_frontier() -> dict[str, Any]:
    from homotopy_groups import (
        FiniteCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
        TodaSuspensionMap,
    )
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        cyclic_generator_zero_image_inputs, expand_zero_image_from_cyclic_generator,
    )
    from proof import Relation, RelationType, ProofRule

    target_zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target_zero)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=target_zero)
    e = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6))
    zero_image = ImageZeroStatement(e)
    presentation = exact_prior_database_result(5, 5)
    if (not isinstance(presentation, Relation)
            or presentation.relation_type is not RelationType.EQUALITY
            or presentation.lhs != e.source_group
            or not isinstance(presentation.rhs, FiniteCyclicGroup)
            or presentation.rhs.order != 2):
        raise RuntimeError("Registered π10^5 cyclic presentation shape changed")
    if any(is_exact_given(goal, admitted) for goal in (target_zero, zero_image)):
        raise RuntimeError("Forbidden target-zero or E-image-zero GIVEN")
    choices = expand_zero_image_from_cyclic_generator(zero_image, presentation)
    required = cyclic_generator_zero_image_inputs(zero_image, presentation)
    if len(choices) != 1 or required is None or choices[0].subgoals != required:
        raise RuntimeError("Isolated cyclic-generator rule did not produce two goals")
    if not isinstance(required[1], GeneratorImage):
        raise RuntimeError("Typed generator image child is absent")
    return {
        "source_screening": "independent_source_screened",
        "registered_presentation_is_not_proof": True,
        "registered_presentation": {
            "type": type(presentation).__name__,
            "rhs_type": type(presentation.rhs).__name__,
            "order": presentation.rhs.order,
            "generator": repr(presentation.rhs.generator),
            "is_exact_screened_given": is_exact_given(presentation, admitted),
        },
        "isolated_zero_image_candidate_count": len(choices),
        "isolated_child_goals": [
            {"type": type(child).__name__, "repr": repr(child)[:1000]}
            for child in required
        ],
        "production_image_zero_frontier": summarize_proposals(provider, zero_image, admitted),
        "production_presentation_frontier": summarize_proposals(provider, required[0], admitted),
        "production_generator_zero_frontier": summarize_proposals(provider, required[1], admitted),
        "public_provider_unchanged": True,
        "new_verified_steps": 0,
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return (
        base / "EHPProofTracerAudit" / "phase174_r3_r7_r6"
        / "cyclic_generator_zero_image.json"
    )


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    source_review = verify_toda_source(root)
    path = prior_path()
    if not path.is_file():
        raise RuntimeError("R3-R7-R5 certified audit JSON is required")
    prior = validate_r5_evidence(json.loads(path.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_screened_cyclic_generator_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_ISOLATED_RULE",
        "git_state": git_state,
        "source_review": source_review,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "gate": (
            "PASS_PREFLIGHT" if dry_run
            else "PASS_ISOLATED_CYCLIC_ZERO_IMAGE_CHILDREN_UNPROVEN"
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
    prefix = "PHASE174_R3R7R6_"
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["head_lineage"])
    print(prefix + "SOURCE_PI105_NONZERO_BUT_GENERATOR_SUSPENDS_ZERO=VERIFIED_TRANSCRIPTION")
    print(prefix + "R5_OBSERVED_IMAGE_ZERO_PROPOSALS=0")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "ISOLATED_CYCLIC_ZERO_IMAGE_PROPOSALS=" + str(
            live["isolated_zero_image_candidate_count"]
        ))
        for label, key in (
            ("PRODUCTION_IMAGE_ZERO", "production_image_zero_frontier"),
            ("PRODUCTION_PRESENTATION", "production_presentation_frontier"),
            ("PRODUCTION_GENERATOR_ZERO", "production_generator_zero_frontier"),
        ):
            print(prefix + label + "_PROPOSALS=" + str(live[key]["proposal_count"]))
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
