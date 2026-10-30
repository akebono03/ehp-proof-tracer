"""Read-only Phase 171 R2J-R4-R7 replay: 2 nu' != 0, then order(nu')=4.

Use the R4-R3 typed double relation, R2J-R3 injectivity, a unique earlier
pi_5^2 group source and the R4-R6 cardinality. No middle-group structure
is given or inferred here; its cyclic presentation is reserved for R4-R8.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from expression import MapApplication
from homotopy_groups import TodaPrimaryGroup
from map_facts import EHP_E_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapInjective
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r2_generator_image_replay.audit import proof_ancestry
from phase171_r2j_r4_r3_double_image_bridge.audit import build_double_image_proof
from phase171_r2j_r4_r5_short_exact_sequence.audit import _screened_leaf_ids
from phase171_r2j_r4_r6_middle_cardinality.audit import build_middle_cardinality_proof
from phase171_r2j_r4_r7_nonzero_nu_order.source import (
    FiniteElementOrder,
    NonZeroGroupElement,
    inferred_nonzero_double_rule,
    inferred_order_four_rule,
    injected_generator_nonzero_rule,
    nonzero_cyclic_generator_image,
    nonzero_double_from_equality,
    order_four_from_nonzero_double,
)
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("R4-R7 permits read-only Git commands only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def _infer(rule, parents: tuple[ProofStep, ...], goal: object) -> ProofStep:
    """Require one ordered, real matcher result and a genuine ProofStep root."""
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, parents)
        if len(match.premises) == len(parents)
        and all(a is b for a, b in zip(match.premises, parents))
    )
    if len(matches) != 1:
        raise RuntimeError("no unique genuine typed inference match")
    root = derive_inference_proof_step(matches[0])
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != goal
        or len(root.premises) != len(parents)
        or any(a is not b for a, b in zip(root.premises, parents))
    ):
        raise RuntimeError("derived inference step failed the parent contract")
    return root


def build_nonzero_nu_order_proof() -> tuple[ProofStep, ProofStep, tuple[ProofStep, ...], dict]:
    """Replay all earlier proof trees, then derive double nonzero and order four."""
    screened, pi63_goal, citing = _screened_context()
    cardinality_root, _, cardinality_report = build_middle_cardinality_proof()
    double_root, _, double_report = build_double_image_proof()
    if (
        cardinality_root.rule is not ProofRule.INFERENCE
        or cardinality_root.conclusion.group != TodaPrimaryGroup(6, 3)
        or cardinality_root.conclusion.order != 4
        or double_root.rule is not ProofRule.INFERENCE
        or not isinstance(double_root.conclusion, Relation)
        or cardinality_report["new_given_added"] != 0
        or double_report["new_given_added"] != 0
    ):
        raise RuntimeError("R4-R3/R4-R6 inferred antecedents are unavailable")

    # Reuse exact ProofSteps from the successful R4-R6 tree; do not recreate
    # the source as a GIVEN or reconstruct the injectivity result from labels.
    prior_group = cardinality_root.premises[0]
    short_exact = cardinality_root.premises[1]
    if (
        prior_group.rule is not ProofRule.GIVEN
        or len(short_exact.premises) != 3
        or short_exact.rule is not ProofRule.INFERENCE
    ):
        raise RuntimeError("prior group or short exact proof ancestry malformed")
    e_injective = short_exact.premises[0]
    if (
        e_injective.rule is not ProofRule.INFERENCE
        or not isinstance(e_injective.conclusion, MapInjective)
    ):
        raise RuntimeError("missing proved E injection from short exact proof")
    typed_equality = double_root.conclusion
    image = typed_equality.rhs
    if not isinstance(image, MapApplication) or image.map != EHP_E_MAP:
        raise RuntimeError("R4-R3 double equality has no typed E-image")

    generator_nonzero = nonzero_cyclic_generator_image(
        prior_group.conclusion, e_injective.conclusion, image,
    )
    if generator_nonzero is None:
        raise RuntimeError("prior generator does not match injected triple eta")
    image_rule = injected_generator_nonzero_rule(
        generator_nonzero, prior_group.conclusion, e_injective.conclusion,
    )
    image_root = _infer(image_rule, (prior_group, e_injective), generator_nonzero)

    doubled_nonzero = nonzero_double_from_equality(
        typed_equality, generator_nonzero,
    )
    if doubled_nonzero is None:
        raise RuntimeError("derived double equality is not compatible with nonzero E-image")
    double_nonzero_rule = inferred_nonzero_double_rule(
        doubled_nonzero, typed_equality, generator_nonzero,
    )
    double_nonzero_root = _infer(
        double_nonzero_rule, (double_root, image_root), doubled_nonzero,
    )

    order_goal = order_four_from_nonzero_double(
        cardinality_root.conclusion, doubled_nonzero,
    )
    if (
        order_goal is None
        or not isinstance(order_goal, FiniteElementOrder)
        or order_goal.group != TodaPrimaryGroup(6, 3)
        or order_goal.element != typed_equality.lhs.expression
        or order_goal.order != 4
    ):
        raise RuntimeError("nonzero doubled element and group order do not prove order four")
    order_rule = inferred_order_four_rule(
        order_goal, cardinality_root.conclusion, doubled_nonzero,
    )
    order_root = _infer(
        order_rule, (cardinality_root, double_nonzero_root), order_goal,
    )
    nodes = proof_ancestry(order_root)
    leaves = tuple(node for node in nodes if node.rule is ProofRule.GIVEN)
    ids = _screened_leaf_ids(screened, citing, leaves)
    if (
        double_nonzero_root.rule is not ProofRule.INFERENCE
        or double_nonzero_root.conclusion != NonZeroGroupElement(
            TodaPrimaryGroup(6, 3), typed_equality.lhs,
        )
        or not ids
        or any(node.conclusion == pi63_goal for node in nodes)
        or any(node.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE) for node in nodes)
        or any(node.rule is ProofRule.GIVEN and node.conclusion in (
            order_goal, doubled_nonzero, generator_nonzero,
        ) for node in nodes)
    ):
        raise RuntimeError("a group result or forged nonzero/order-four fact entered ancestry")
    report = {
        "phase": "171-R2J-R4-R7",
        "mode": "READ_ONLY_TYPED_NONZERO_AND_ELEMENT_ORDER_REPLAY",
        "status": "INFERRED",
        "prior_source": repr(prior_group.conclusion),
        "e_injective": repr(e_injective.conclusion),
        "double_relation": repr(typed_equality),
        "cardinality": repr(cardinality_root.conclusion),
        "nonzero_image": repr(image_root.conclusion),
        "nonzero_double": repr(double_nonzero_root.conclusion),
        "element_order": repr(order_root.conclusion),
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in nodes),
        "given_leaves": len(leaves),
        "verified_source_ids": list(dict.fromkeys(ids)),
        "new_given_added": 0,
        "nu_prime_double_nonzero_proven": True,
        "nu_prime_order_four_proven": True,
        "pi63_cyclic_presentation_proven": False,
        "production_modified": False,
        "full_pytest": False,
    }
    return double_nonzero_root, order_root, nodes, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R4-R7 requires the develop branch")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    for relative in (
        "phase171_r2j_r4_r3_double_image_bridge/audit.py",
        "phase171_r2j_r4_r6_middle_cardinality/audit.py",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError("missing earlier proof module: " + relative)
    print("PHASE171_R2J_R4_R7_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R7_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R7_RESULT=PASS_DRY_RUN", flush=True)
        return
    nonzero, order, nodes, report = build_nonzero_nu_order_proof()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked source changed during read-only proof replay")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R7_DOUBLE_NONZERO=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R7_NU_PRIME_ORDER_FOUR=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R7_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R4_R7_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R7_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R7_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R7_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R7_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R7_RUN=PASS", flush=True)
    print("PHASE171_R2J_R4_R7_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
