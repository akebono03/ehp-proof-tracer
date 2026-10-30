"""R2J-R4-R8: replay the fully inferred cyclic presentation of pi_6^3.

The source is the real R4-R7 nonzero/order tree and its R4-R6 cardinality
parent.  The registered pi_6^3 relation is a requested GOAL, never a GIVEN.
The public proof search/rendering integration is explicitly not changed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r2_generator_image_replay.audit import proof_ancestry
from phase171_r2j_r4_r5_short_exact_sequence.audit import _screened_leaf_ids
from phase171_r2j_r4_r7_nonzero_nu_order.audit import build_nonzero_nu_order_proof
from phase171_r2j_r4_r8_cyclic_structure.source import (
    cyclic_group_from_generator_order,
    expand_cyclic_group_from_full_element_order,
    inferred_cyclic_group_rule,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("only read-only Git commands are permitted")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def build_cyclic_pi63_proof() -> tuple[ProofStep, tuple[ProofStep, ...], dict]:
    """Prove the registered goal using R4-R7 roots, with no imported group fact."""
    screened, pi63_goal, citing = _screened_context()
    double_nonzero, element_order_root, _, r7_report = build_nonzero_nu_order_proof()
    if (
        element_order_root.rule is not ProofRule.INFERENCE
        or len(element_order_root.premises) != 2
        or r7_report["nu_prime_order_four_proven"] is not True
        or r7_report["new_given_added"] != 0
        or double_nonzero.rule is not ProofRule.INFERENCE
    ):
        raise RuntimeError("genuine R4-R7 order proof is required")
    cardinality_root = element_order_root.premises[0]
    if cardinality_root.rule is not ProofRule.INFERENCE:
        raise RuntimeError("middle-group cardinality must be inferred")
    cardinality = cardinality_root.conclusion
    element_order = element_order_root.conclusion
    if (
        cardinality.group != TodaPrimaryGroup(6, 3)
        or cardinality.order != 4
        or element_order.group != cardinality.group
        or element_order.order != cardinality.order
        or not isinstance(pi63_goal, Relation)
        or pi63_goal.relation_type is not RelationType.EQUALITY
        or pi63_goal.lhs != cardinality.group
        or not isinstance(pi63_goal.rhs, FiniteCyclicGroup)
        or pi63_goal.rhs.order != 4
    ):
        raise RuntimeError("R4-R7 roots and registered group goal are incompatible")

    result_goal = cyclic_group_from_generator_order(
        cardinality, element_order, requested=pi63_goal,
    )
    if result_goal != pi63_goal:
        raise RuntimeError("proved generator cannot be identified with goal generator")
    proposals = expand_cyclic_group_from_full_element_order(
        pi63_goal, cardinality, element_order,
    )
    parents = (cardinality_root, element_order_root)
    rule = inferred_cyclic_group_rule(pi63_goal)
    if (
        len(proposals) != 1
        or proposals[0].subgoals != (cardinality, element_order)
        or proposals[0].rule.name != rule.name
    ):
        raise RuntimeError("cyclic-group inference obligation is not unique")
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, parents)
        if len(match.premises) == 2
        and match.premises[0] is cardinality_root
        and match.premises[1] is element_order_root
    )
    if len(matches) != 1:
        raise RuntimeError("expected exactly one typed generator-order inference")
    root = derive_inference_proof_step(matches[0])
    nodes = proof_ancestry(root)
    leaves = tuple(node for node in nodes if node.rule is ProofRule.GIVEN)
    source_ids = _screened_leaf_ids(screened, citing, leaves)
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != pi63_goal
        or root.premises != parents
        or not source_ids
        or any(node.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE) for node in nodes)
        or any(node.rule is ProofRule.GIVEN and node.conclusion in (
            pi63_goal, cardinality, element_order,
        ) for node in nodes)
        or any(node is root for node in root.premises)
        or not any(node is double_nonzero for node in nodes)
        or not any(node is cardinality_root for node in nodes)
        or not any(node is element_order_root for node in nodes)
    ):
        raise RuntimeError("cyclic proof improperly imported a target or unproved premise")
    report = {
        "phase": "171-R2J-R4-R8",
        "mode": "READ_ONLY_TYPED_CYCLIC_STRUCTURE_REPLAY",
        "status": "INFERRED",
        "registered_goal": repr(pi63_goal),
        "derived_conclusion": repr(root.conclusion),
        "cardinality": repr(cardinality),
        "element_order": repr(element_order),
        "inference_rule": root.inference_rule.name,
        "inferences": sum(node.rule is ProofRule.INFERENCE for node in nodes),
        "given_leaves": len(leaves),
        "verified_source_ids": list(dict.fromkeys(source_ids)),
        "new_given_added": 0,
        "pi63_cyclic_group_proven": True,
        "public_proof_search_wired": False,
        "public_web_verified": False,
        "production_modified": False,
        "full_pytest": False,
    }
    return root, nodes, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R4-R8 requires the develop branch")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    required = (
        "phase171_r2j_r4_r7_nonzero_nu_order/audit.py",
        "phase171_r2j_r4_r6_middle_cardinality/audit.py",
        "phase171_r2j_r4_r3_double_image_bridge/audit.py",
    )
    for relative in required:
        if not (ROOT / relative).is_file():
            raise RuntimeError("missing verified prior proof: " + relative)
    print("PHASE171_R2J_R4_R8_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R8_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R8_RESULT=PASS_DRY_RUN", flush=True)
        return
    root, nodes, report = build_cyclic_pi63_proof()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked source modified during read-only audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R8_PI63_CYCLIC=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R8_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R4_R8_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R8_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R8_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R8_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R8_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R8_RUN=PASS", flush=True)
    print("PHASE171_R2J_R4_R8_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
