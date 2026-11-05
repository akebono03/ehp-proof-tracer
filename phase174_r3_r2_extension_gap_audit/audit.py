"""Phase 174 R3-R2: inspect the general cyclic extension proof obligations.

This program reads verified prior audit records and the current public types.
It never constructs ProofSteps or promotes any proposed inference to a proof.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any

REVIEWED_HEADS = (
    "1c6e6e594042f498e3cb4977ef9c72ce3d1da9f9",
    "8687759569d7820e26c53aac6f38aedb8ea04f0b",
)
R3R1_ORIGINAL_HEAD = "1c6e6e594042f498e3cb4977ef9c72ce3d1da9f9"


def git(*args: str) -> str:
    completed = subprocess.run(
        ("git",) + args, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    return completed.stdout.strip()


def prior_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r1" / "audit.json"


def validate_prior_frontier(report: object) -> dict[str, Any]:
    """Keep R3-R1's typed failures intact, including its citation boundary."""
    if not isinstance(report, dict):
        raise ValueError("R3-R1 report is not a mapping")
    if report.get("phase") != "174-R3-R1":
        raise ValueError("Unexpected previous phase")
    if report.get("mode") != "READ_ONLY_TWO_HOP_FRONTIER":
        raise ValueError("Previous audit mode changed")
    if report.get("local_head") != R3R1_ORIGINAL_HEAD:
        raise ValueError("Previous frontier HEAD provenance changed")
    if report.get("new_proof_steps") != 0 or report.get("full_pytest_performed") is not False:
        raise ValueError("Prior report unexpectedly asserts completed proofs")
    root = report.get("pi85_frontier")
    if not isinstance(root, dict) or root.get("root_proposal_count") != 3:
        raise ValueError("Previous root proposal count changed")
    if root.get("screened_given_count") != 27:
        raise ValueError("Previous citation-screened premise count changed")
    proposals = root.get("root_proposals")
    if not isinstance(proposals, list) or len(proposals) != 3:
        raise ValueError("Missing three root proposal records")
    for i in (0, 2):
        proposal = proposals[i]
        if proposal.get("rule") != "finite cyclic structure gives group relation":
            raise ValueError("Finite cyclic root rule changed")
        children = proposal.get("children")
        if proposal.get("child_count") != 1 or not isinstance(children, list) or len(children) != 1:
            raise ValueError("Finite cyclic root child count changed")
        child = children[0]
        if child.get("unwrapped_goal", {}).get("type") != "CyclicStructureStatement":
            raise ValueError("Finite cyclic root child type changed")
        if child.get("exact_screened_given") is not False:
            raise ValueError("Unproved cyclic child was treated as GIVEN")
        if child.get("second_hop_proposal_count") != 0:
            raise ValueError("Cyclic child now has another proposed expansion")
    middle = proposals[1]
    if middle.get("rule") != "equality symmetry" or middle.get("child_count") != 1:
        raise ValueError("Symmetry root changed")
    middle_child = middle.get("children", [])[0]
    if middle_child.get("unwrapped_goal", {}).get("type") != "Relation":
        raise ValueError("Symmetry child is not a Relation")
    if middle_child.get("second_hop_proposal_count") != 1:
        raise ValueError("Symmetry second hop count changed")
    if root.get("proofs_verified_by_this_audit") != 0 or root.get("new_given") != 0:
        raise ValueError("R3-R1 improperly admitted proof evidence")
    return root


def derive_structural_obligations(
    *, source_order: int, subgroup_index: int, doubled_lift: bool,
    mono_proved: bool, index_proved: bool, double_proved: bool,
) -> dict[str, Any]:
    """Describe conditions, not a theorem proving them.

    Arithmetic here is a design estimate only. In particular it never creates
    a CyclicStructureStatement or verifies a mathematical ProofStep.
    """
    if type(source_order) is not int or source_order < 2:
        raise ValueError("source_order must be a positive integer >= 2")
    if type(subgroup_index) is not int or subgroup_index < 2:
        raise ValueError("subgroup_index must be an integer >= 2")
    requirements = (
        ("source_cyclic_presentation", False),
        ("verified_injection", mono_proved),
        ("verified_cokernel_order", index_proved),
        ("verified_double_lift", doubled_lift and double_proved),
        ("typed_generator_identification", False),
    )
    return {
        "conditional_cardinality": source_order * subgroup_index,
        "all_obligations_proved_by_this_audit": False,
        "requirements": [
            {"name": name, "verified_by_this_audit": False, "indicated_existing": present}
            for name, present in requirements
        ],
        "not_a_ProofStep": True,
    }


def inspect_actual_existing_rules() -> dict[str, Any]:
    """Inspect common typed rules without executing an inference match."""
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase165_r12_r2_quotient_rules import (
        CyclicStructureStatement,
        QuotientIsomorphismStatement,
        infinite_cyclic_quotient_structure_inference_rule,
    )
    from phase165_r12_r5_structure_bridge import finite_cyclic_structure_as_relation_inference_rule
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from proof import Relation

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(goals) != 1:
        raise ValueError("Unreviewed number of typed pi_8^5 goals")
    goal = goals[0]
    if (
        not isinstance(goal, Relation)
        or goal.lhs != TodaPrimaryGroup(8, 5)
        or not isinstance(goal.rhs, FiniteCyclicGroup)
        or goal.rhs.order != 8
    ):
        raise ValueError("The typed target presentation has changed")
    cyclic = CyclicStructureStatement(goal.lhs, goal.rhs.generator, 8)
    quotient_rule = infinite_cyclic_quotient_structure_inference_rule()
    structure_rule = finite_cyclic_structure_as_relation_inference_rule()
    source_pattern = quotient_rule.premise_patterns[1].statement_pattern
    quotient_pattern = quotient_rule.premise_patterns[0].statement_pattern
    if not isinstance(source_pattern, CyclicStructureStatement) or source_pattern.order is not None:
        raise ValueError("Existing quotient rule is no longer based on infinite cyclic source")
    if not isinstance(quotient_pattern, QuotientIsomorphismStatement):
        raise ValueError("Existing quotient premise type changed")
    if structure_rule.premise_patterns[0].statement_type is not CyclicStructureStatement:
        raise ValueError("Finite group relation bridge premise type changed")
    return {
        "named_goal_repr": repr(goal),
        "required_cyclic_goal_type": type(cyclic).__name__,
        "required_cyclic_goal_repr": repr(cyclic),
        "required_cyclic_order": cyclic.order,
        "existing_infinite_quotient_rule": quotient_rule.name,
        "existing_infinite_quotient_source_order": source_pattern.order,
        "existing_finite_bridge_rule": structure_rule.name,
        "existing_finite_bridge_premise": type(cyclic).__name__,
        "no_rule_was_invoked_as_proof": True,
    }


def make_report() -> dict[str, Any]:
    head = git("rev-parse", "HEAD")
    if git("branch", "--show-current") != "develop" or head not in REVIEWED_HEADS:
        raise RuntimeError("Local HEAD not among reviewed commits")
    prior = prior_report_path()
    if not prior.is_file():
        raise FileNotFoundError("R3-R1 audit report missing: " + str(prior))
    previous = json.loads(prior.read_text(encoding="utf-8-sig"))
    frontier = validate_prior_frontier(previous)
    existing = inspect_actual_existing_rules()
    cyclic_children = [
        frontier["root_proposals"][i]["children"][0]
        for i in (0, 2)
    ]
    matching = [
        item["unwrapped_goal"]["repr"] == existing["required_cyclic_goal_repr"]
        for item in cyclic_children
    ]
    return {
        "phase": "174-R3-R2",
        "mode": "READ_ONLY_CYCLIC_EXTENSION_GAP",
        "local_head": head,
        "prior_r3r1_original_head": R3R1_ORIGINAL_HEAD,
        "prior_report_path": str(prior),
        "screened_given_count": frontier["screened_given_count"],
        "root_proposal_count": frontier["root_proposal_count"],
        "cyclic_children_count": len(cyclic_children),
        "cyclic_children_no_second_hop": all(x["second_hop_proposal_count"] == 0 for x in cyclic_children),
        "cyclic_children_exact_target_match": matching,
        "cyclic_children_reprs": [x["unwrapped_goal"]["repr"] for x in cyclic_children],
        "existing_rule_contract": existing,
        "extension_obligations": derive_structural_obligations(
            source_order=4, subgroup_index=2, doubled_lift=True,
            mono_proved=False, index_proved=False, double_proved=False,
        ),
        "source_locators_to_reuse": (
            "Toda (4.8): conditional Delta(iota_7) = 0",
            "Toda Lemma 5.4",
            "Toda (5.5): twice nu_5 = E^2 nu_prime",
            "Toda Proposition 5.6 (prior pi_6^3 proof)",
        ),
        "new_proof_steps": 0,
        "new_given": 0,
        "production_changes": False,
        "full_pytest_performed": False,
    }


def main() -> int:
    report = make_report()
    output_dir = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r2"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "audit.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R3R2_LOCAL_HEAD=" + report["local_head"])
    print("PHASE174_R3R2_PRIOR_FRONTIER=PASS")
    print("PHASE174_R3R2_CYCLIC_CHILDREN=" + str(report["cyclic_children_count"]))
    print("PHASE174_R3R2_ZERO_SECOND_HOP=" + str(report["cyclic_children_no_second_hop"]))
    print("PHASE174_R3R2_TARGET_CYCLIC_MATCH=" + str(report["cyclic_children_exact_target_match"]))
    print("PHASE174_R3R2_EXISTING_QUOTIENT_SOURCE_ORDER=None")
    print("PHASE174_R3R2_EXTENSION_OBLIGATIONS=" + str(len(report["extension_obligations"]["requirements"])))
    print("PHASE174_R3R2_NEW_GIVEN=0")
    print("PHASE174_R3R2_NEW_PROOFS=0")
    print("PHASE174_R3R2_REPORT=" + str(output))
    print("PHASE174_R3R2_AUDIT_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
