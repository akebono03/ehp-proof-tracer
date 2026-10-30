"""Read-only replay: infer a short exact EHP sequence from cited proof trees.

R2J-R3 supplies inferred E injectivity; R4-R4 supplies inferred H
surjectivity; Proposition 4.2 supplies inferred E-H exactness. No completed
pi_6^3 group relation or DB group candidate is an admitted proof premise.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r12_r11_prop42_unified import (
    TodaProp42GeneralExactnessStatement,
    expand_cited_prop42_exactness,
    prop42_exactness_indices,
)
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r3_ehp_exactness.audit import build_r2j_r3_proof
from phase171_r2j_r4_r1_extension_frontier_audit.audit import _extension_window
from phase171_r2j_r4_r2_generator_image_replay.audit import proof_ancestry
from phase171_r2j_r4_r4_cited_hopf_surjectivity.audit import (
    build_cited_hopf_surjectivity_proof,
)
from phase171_r2j_r4_r5_short_exact_sequence.source import (
    ehp_short_exact_rule,
    expand_ehp_short_exact,
    short_exact_from_ehp,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("only read-only Git operations are allowed")
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _cited_prop42_source(screened, citing: str):
    """Pick the one earlier, actually linked universal EHP source."""
    found = []
    for link in screened.proof_links:
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and step.conclusion == assertion.content
            and type(step.conclusion) is TodaProp42GeneralExactnessStatement
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and reference.locator == "Proposition 4.2 (4.4)"
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            found.append(link)
    if len(found) != 1:
        raise RuntimeError("expected one screened Proposition 4.2 universal source")
    return found[0]


def _screened_leaf_ids(screened, citing: str, leaves: tuple[ProofStep, ...]) -> tuple[str, ...]:
    """Reject uncited GIVEN roots, including a forged completed target group."""
    resolved: list[str] = []
    for leaf in leaves:
        if leaf.rule is not ProofRule.GIVEN or leaf.premises:
            raise RuntimeError("proof ancestry contains a non-leaf GIVEN")
        matching_ids = []
        for link in screened.proof_links:
            step = link.step
            assertion = screened.registry.assertion(link.assertion_id)
            if (
                isinstance(step, ProofStep)
                and step.rule is ProofRule.GIVEN
                and not step.premises
                and type(step.conclusion) is type(leaf.conclusion)
                and step.conclusion == leaf.conclusion
                and assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and assertion.content == step.conclusion
                and precedes_citing_assertion(screened, link.assertion_id, citing)
            ):
                matching_ids.append(link.assertion_id)
        if len(matching_ids) != 1:
            raise RuntimeError("proof leaf lacks one unambiguous screened earlier source")
        resolved.append(matching_ids[0])
    return tuple(resolved)


def build_short_exact_proof() -> tuple[ProofStep, tuple[ProofStep, ...], dict]:
    """Reconstruct all dependencies, then apply one typed inference match."""
    screened, pi63_goal, citing = _screened_context()
    prop42_source = _cited_prop42_source(screened, citing)
    _, injection_root, _, _ = build_r2j_r3_proof()
    projection_root, _, _ = build_cited_hopf_surjectivity_proof()
    exactness_goal = _extension_window()
    if prop42_exactness_indices(exactness_goal) != (2, 6, "e_h"):
        raise RuntimeError("unexpected E-H exactness indices for pi_6^3")
    options = expand_cited_prop42_exactness(
        exactness_goal, (prop42_source.step.conclusion,),
    )
    if len(options) != 1 or options[0].subgoals != (prop42_source.step.conclusion,):
        raise RuntimeError("Proposition 4.2 specialized E-H window is unavailable")
    public_options = shared_expansion_provider(screened, proof_target=pi63_goal)(exactness_goal)
    if not any(
        item.rule.name == options[0].rule.name and item.subgoals == options[0].subgoals
        for item in public_options
    ):
        raise RuntimeError("E-H exactness rule is not connected to shared provider")

    def exactness_provider(current: object):
        return expand_cited_prop42_exactness(
            current, (prop42_source.step.conclusion,),
        )

    exactness_root = reconstruct_registered_goal(
        exactness_goal,
        screened,
        citing,
        exactness_provider,
        lookup_mode="typed_reference_publication",
    )
    if (
        exactness_root.rule is not ProofRule.INFERENCE
        or exactness_root.conclusion != exactness_goal
        or len(exactness_root.premises) != 1
        or exactness_root.premises[0] is not prop42_source.step
    ):
        raise RuntimeError("E-H exactness lacks the original source-backed proof")
    expected = short_exact_from_ehp(
        injection_root.conclusion,
        exactness_root.conclusion,
        projection_root.conclusion,
    )
    if expected is None:
        raise RuntimeError("E-injective, E-H exact, H-surjective premises do not match")
    proposals = expand_ehp_short_exact(expected)
    if len(proposals) != 1 or proposals[0].subgoals != (
        injection_root.conclusion,
        exactness_root.conclusion,
        projection_root.conclusion,
    ):
        raise RuntimeError("short-exact inference obligations are not unique")
    parents = (injection_root, exactness_root, projection_root)
    rule = ehp_short_exact_rule(expected)
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, parents)
        if len(match.premises) == 3
        and all(a is b for a, b in zip(match.premises, parents))
    )
    if len(matches) != 1:
        raise RuntimeError("no unique typed inference from three proved EHP premises")
    root = derive_inference_proof_step(matches[0])
    nodes = proof_ancestry(root)
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != expected
        or root.premises != parents
        or any(node.conclusion == pi63_goal for node in nodes)
        or any(node.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE) for node in nodes)
    ):
        raise RuntimeError("untrusted proof ancestry or completed group import")
    leaves = tuple(node for node in nodes if node.rule is ProofRule.GIVEN)
    leaf_ids = _screened_leaf_ids(screened, citing, leaves)
    if prop42_source.assertion_id not in leaf_ids:
        raise RuntimeError("Proposition 4.2 universal source absent from proof ancestry")
    report = {
        "phase": "171-R2J-R4-R5",
        "mode": "READ_ONLY_TYPED_SHORT_EXACT_REPLAY",
        "status": "INFERRED",
        "short_exact_sequence": repr(root.conclusion),
        "e_injective": repr(injection_root.conclusion),
        "e_h_exactness": repr(exactness_root.conclusion),
        "h_surjective": repr(projection_root.conclusion),
        "prop42_source_id": prop42_source.assertion_id,
        "verified_source_ids": list(dict.fromkeys(leaf_ids)),
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in nodes),
        "given_leaves": len(leaves),
        "new_given_added": 0,
        "pi63_group_proven": False,
        "order_four_proven": False,
        "production_modified": False,
        "full_pytest": False,
    }
    return root, nodes, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R2J-R4-R5 requires the develop branch")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if not (
        ROOT / "phase171_r2j_r4_r4_cited_hopf_surjectivity" / "audit.py"
    ).is_file():
        raise RuntimeError("R4-R4 local audit must be retained in the worktree")
    print("PHASE171_R2J_R4_R5_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R5_HEAD=" + head, flush=True)
    if arguments.dry_run:
        print("PHASE171_R2J_R4_R5_RESULT=PASS_DRY_RUN", flush=True)
        return
    root, nodes, report = build_short_exact_proof()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked worktree changed during read-only proof replay")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R5_SHORT_EXACT=" + report["status"], flush=True)
    print("PHASE171_R2J_R4_R5_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R4_R5_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R5_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R5_ORDER_FOUR_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R5_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R5_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R5_REPORT=" + str(path), flush=True)
    print("PHASE171_R2J_R4_R5_RUN=PASS", flush=True)


if __name__ == "__main__":
    main()
