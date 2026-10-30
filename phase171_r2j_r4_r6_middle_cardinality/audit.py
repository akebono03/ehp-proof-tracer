"""R2J-R4-R6: replay cardinality of pi_6^3 from a proved short exact EHP sequence.

The pi_5^2 group is a uniquely screened earlier Proposition 5.6
component, not the pi_6^3 target.  The pi_6^5 group is an INFERENCE
already inside the genuine R4-R5 proof tree.  No group structure of
the middle term and no order-four generator is assumed or concluded.
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
from phase171_r2j_r4_r5_short_exact_sequence.audit import (
    _screened_leaf_ids,
    build_short_exact_proof,
)
from phase171_r2j_r4_r6_middle_cardinality.source import (
    cardinality_from_short_exact,
    expand_finite_cardinality_from_short_exact,
    finite_cardinality_from_short_exact_rule,
)
from phase166_r3c_publication_order import precedes_citing_assertion
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
PRIOR_SUFFIX = "boundary:Proposition 5.6:pi5_2_group_relation"


def _git(*arguments: str) -> str:
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in permitted:
        raise ValueError("only read-only Git operations are permitted")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def screened_prior_pi52(screened, citing: str):
    """Select exactly one earlier fixed GIVEN for pi_5^2, not a DB goal.

    Identifiers may carry a ``shared:N:`` registry prefix.  The
    literature position and typed contents must also agree.
    """
    matches = []
    for link in screened.proof_links:
        if not (
            link.assertion_id == PRIOR_SUFFIX
            or link.assertion_id.endswith(":" + PRIOR_SUFFIX)
        ):
            continue
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and isinstance(step.conclusion, Relation)
            and step.conclusion.relation_type is RelationType.EQUALITY
            and step.conclusion.lhs == TodaPrimaryGroup(5, 2)
            and isinstance(step.conclusion.rhs, FiniteCyclicGroup)
            and type(step.conclusion.rhs.order) is int
            and step.conclusion.rhs.order > 0
            and step.conclusion == assertion.content
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and reference.locator == "Proposition 5.6"
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            matches.append(link)
    if len(matches) != 1:
        raise RuntimeError("unique earlier, source-screened pi_5^2 component is required")
    return matches[0]


def proven_right_group_from_short_exact(root: ProofStep) -> ProofStep:
    """Reuse the genuine pi_6^5 inference within the R4-R5 H proof branch."""
    if root.rule is not ProofRule.INFERENCE or len(root.premises) != 3:
        raise RuntimeError("short-exact root has wrong inferred ancestry")
    hopf_root = root.premises[2]
    if hopf_root.rule is not ProofRule.INFERENCE or len(hopf_root.premises) != 2:
        raise RuntimeError("Hopf surjectivity proof branch is not complete")
    group_root = hopf_root.premises[0]
    if (
        group_root.rule is not ProofRule.INFERENCE
        or not isinstance(group_root.conclusion, Relation)
        or group_root.conclusion.relation_type is not RelationType.EQUALITY
        or group_root.conclusion.lhs != TodaPrimaryGroup(6, 5)
        or not isinstance(group_root.conclusion.rhs, FiniteCyclicGroup)
        or len(group_root.premises) != 1
        or group_root.premises[0].rule is not ProofRule.GIVEN
    ):
        raise RuntimeError("pi_6^5 group must be a proved source-specialized relation")
    return group_root


def build_middle_cardinality_proof() -> tuple[ProofStep, tuple[ProofStep, ...], dict]:
    """Attach an earlier pi_5^2 fact to the R4-R5 proof without new GIVENs."""
    screened, pi63_goal, citing = _screened_context()
    left = screened_prior_pi52(screened, citing)
    exact_root, _, _ = build_short_exact_proof()
    right = proven_right_group_from_short_exact(exact_root)
    goal = cardinality_from_short_exact(
        left.step.conclusion, exact_root.conclusion, right.conclusion,
    )
    if goal is None or goal.group != TodaPrimaryGroup(6, 3) or goal.order != 4:
        raise RuntimeError("finite end-group data do not yield pi_6^3 of order four")
    proposals = expand_finite_cardinality_from_short_exact(
        goal, left.step.conclusion, exact_root.conclusion, right.conclusion,
    )
    if len(proposals) != 1 or proposals[0].subgoals != (
        left.step.conclusion, exact_root.conclusion, right.conclusion,
    ):
        raise RuntimeError("finite cardinality backward obligation not unique")
    parents = (left.step, exact_root, right)
    rule = finite_cardinality_from_short_exact_rule(goal)
    matches = tuple(
        item for item in find_inference_matches_for_rule(rule, parents)
        if len(item.premises) == 3
        and all(a is b for a, b in zip(item.premises, parents))
    )
    if len(matches) != 1:
        raise RuntimeError("no unique typed cardinality inference match")
    root = derive_inference_proof_step(matches[0])
    nodes = proof_ancestry(root)
    leaves = tuple(node for node in nodes if node.rule is ProofRule.GIVEN)
    ids = _screened_leaf_ids(screened, citing, leaves)
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != goal
        or root.premises != parents
        or left.assertion_id not in ids
        or any(node.conclusion == pi63_goal for node in nodes)
        or any(node.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE) for node in nodes)
        or any(node.rule is ProofRule.GIVEN and node.conclusion == goal for node in nodes)
    ):
        raise RuntimeError("cardinality proof has a fabricated premise or target-group result")
    report = {
        "phase": "171-R2J-R4-R6",
        "mode": "READ_ONLY_TYPED_MIDDLE_CARDINALITY_REPLAY",
        "status": "INFERRED",
        "prior_pi52_assertion_id": left.assertion_id,
        "prior_pi52_relation": repr(left.step.conclusion),
        "pi65_derived_relation": repr(right.conclusion),
        "short_exact": repr(exact_root.conclusion),
        "conclusion": repr(root.conclusion),
        "cardinality": goal.order,
        "root_inference_rule": rule.name,
        "inferences": sum(node.rule is ProofRule.INFERENCE for node in nodes),
        "given_leaves": len(leaves),
        "verified_source_ids": list(dict.fromkeys(ids)),
        "new_given_added": 0,
        "nu_prime_order_four_proven": False,
        "pi63_group_proven": False,
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
        raise RuntimeError("R4-R6 requires the develop branch")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if not (ROOT / "phase171_r2j_r4_r5_short_exact_sequence" / "audit.py").is_file():
        raise RuntimeError("R4-R5 must exist in the worktree")
    print("PHASE171_R2J_R4_R6_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R6_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R6_RESULT=PASS_DRY_RUN", flush=True)
        return
    root, nodes, report = build_middle_cardinality_proof()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files changed during read-only audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R6_MIDDLE_CARDINALITY=" + report["status"], flush=True)
    print("PHASE171_R2J_R4_R6_CARDINALITY=" + str(report["cardinality"]), flush=True)
    print("PHASE171_R2J_R4_R6_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R4_R6_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R6_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R6_NU_PRIME_ORDER_FOUR_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R6_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R6_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R6_REPORT=" + str(path), flush=True)
    print("PHASE171_R2J_R4_R6_RUN=PASS", flush=True)
    print("PHASE171_R2J_R4_R6_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
