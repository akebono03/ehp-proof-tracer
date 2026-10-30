"""Read-only Phase 171 R2J-R4-R3 replay of 2 nu' = E(eta_2^3).

The cited Toda (5.3) double relation and the inferred R4-R2 image are
combined by a checked InferenceRule. No cyclic group structure is asserted.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2j_r4_r1_extension_frontier_audit.audit import DOUBLE_SUFFIX
from phase171_r2j_r4_r2_generator_image_replay.audit import (
    _screened_eta_definition,
    prepare_image_obligation,
    proof_ancestry,
    scoped_provider,
)
from phase171_r2j_r4_r3_double_image_bridge.source import (
    typed_double_image_conclusion,
    typed_double_image_rule,
)
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("read-only Git operation required")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def screened_double_proof_step(screened, citing: str) -> tuple[str, ProofStep]:
    """Read a unique earlier fixed, typed and actually linked source leaf."""
    matches: list[tuple[str, ProofStep]] = []
    for link in screened.proof_links:
        if not link.assertion_id.endswith(DOUBLE_SUFFIX):
            continue
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and isinstance(step.conclusion, Relation)
            and step.conclusion == assertion.content
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and reference.locator == "(5.3)"
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            matches.append((link.assertion_id, step))
    if len(matches) != 1:
        raise RuntimeError("expected exactly one earlier Toda (5.3) double-relation GIVEN")
    return matches[0]


def build_double_image_proof() -> tuple[ProofStep, tuple[ProofStep, ...], dict]:
    """Reconstruct the R4-R2 tree and connect it to the screened Toda leaf."""
    screened, pi63_goal, citing, image = prepare_image_obligation()
    eta_assertion_id, general = _screened_eta_definition(screened, citing)
    double_assertion_id, cited_double = screened_double_proof_step(screened, citing)
    target = typed_double_image_conclusion(cited_double.conclusion, image)
    if target is None:
        raise RuntimeError("typed Toda relation and image are structurally incompatible")
    image_root = reconstruct_registered_goal(
        image,
        screened,
        citing,
        scoped_provider((general,)),
        lookup_mode="typed_reference_publication",
    )
    if image_root.rule is not ProofRule.INFERENCE or image_root.conclusion != image:
        raise RuntimeError("R4-R2 generator image was not inferred")
    image_ancestors = proof_ancestry(image_root)
    image_leaves = tuple(
        step for step in image_ancestors if step.rule is ProofRule.GIVEN
    )
    if (
        len(image_leaves) != 1
        or image_leaves[0].conclusion != general
        or image_leaves[0].premises
        or any(step.conclusion == pi63_goal for step in image_ancestors)
    ):
        raise RuntimeError("R4-R2 image replay imported an unapproved premise")

    rule = typed_double_image_rule(cited_double.conclusion, image)
    matches = tuple(
        match for match in find_inference_matches_for_rule(
            rule, (cited_double, image_root),
        )
        if len(match.premises) == 2
        and match.premises[0] is cited_double
        and match.premises[1] is image_root
    )
    if len(matches) != 1:
        raise RuntimeError("exactly one genuine typed substitution match required")
    root = derive_inference_proof_step(matches[0])
    ancestors = proof_ancestry(root)
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != target
        or root.premises != (cited_double, image_root)
        or any(step.conclusion == pi63_goal for step in ancestors)
        or any(step.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE) for step in ancestors)
    ):
        raise RuntimeError("invalid proof root or cyclic-group result admitted")
    given = tuple(step for step in ancestors if step.rule is ProofRule.GIVEN)
    if (
        len(given) != 2
        or not any(step is cited_double for step in given)
        or not any(step is image_leaves[0] for step in given)
        or any(step.premises for step in given)
    ):
        raise RuntimeError("uncited or additional GIVEN leaf in the combined proof")
    report = {
        "phase": "171-R2J-R4-R3",
        "mode": "READ_ONLY_TYPED_INFERENCE_REPLAY",
        "status": "INFERRED",
        "double_source_id": double_assertion_id,
        "eta_definition_source_id": eta_assertion_id,
        "double_source": repr(cited_double.conclusion),
        "generator_image": repr(image_root.conclusion),
        "derived_relation": repr(root.conclusion),
        "root_inference_rule": root.inference_rule.name,
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in ancestors),
        "given_leaves": len(given),
        "new_given_added": 0,
        "pi63_group_proven": False,
        "production_modified": False,
        "full_pytest": False,
    }
    return root, ancestors, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R2J-R4-R3 requires develop; branch is not changed")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if not (ROOT / "phase171_r2j_r4_r2_generator_image_replay" / "audit.py").is_file():
        raise RuntimeError("R4-R2 audit is required in the local worktree")
    print("PHASE171_R2J_R4_R3_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R3_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R3_RESULT=PASS_DRY_RUN", flush=True)
        return
    root, ancestors, report = build_double_image_proof()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked worktree changed during inference replay")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R3_DOUBLE_IMAGE=" + report["status"], flush=True)
    print("PHASE171_R2J_R4_R3_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R4_R3_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R3_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R3_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R3_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R3_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R3_RUN=PASS", flush=True)


if __name__ == "__main__":
    main()
