"""Read-only replay of H: pi_6^3 -> pi_6^5 surjectivity.

Source boundary: cited Toda (5.3) H(nu')=eta_5 and the earlier cited
Proposition 5.1 higher-eta schema. The pi_6^5 group is an INFERENCE from
that schema, never a GIVEN or an adopted database result.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation,
    expand_registered_eta_specialization,
    specialize_eta_group_relation,
)
from phase166_r3c_publication_order import precedes_citing_assertion
from phase169_r3h_source_registry import ASSERTION_ID as HOPF_ASSERTION_ID
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r2_cyclic_hopf_surjective.source import _valid_surjective_pair
from phase171_r2j_r4_r2_generator_image_replay.audit import proof_ancestry
from phase171_r2j_r4_r4_cited_hopf_surjectivity.source import (
    cited_hopf_cyclic_surjectivity_rule,
)
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in allowed:
        raise ValueError("only listed read-only Git operations are allowed")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def screened_source_link(screened, citing: str, *, assertion_id: str | None = None,
                         locator: str | None = None,
                         predicate=None):
    """Select one earlier fixed GIVEN, allowing shared-bridge namespace prefixes.

    Assertion identifiers are namespace-qualified by build_shared_typed_bridge.
    Match the full source identifier at a colon boundary, never just a label.
    """
    matches = []
    for link in screened.proof_links:
        if assertion_id is not None and not (
            link.assertion_id == assertion_id
            or link.assertion_id.endswith(":" + assertion_id)
        ):
            continue
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if not (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and step.conclusion == assertion.content
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and (locator is None or reference.locator == locator)
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            continue
        if predicate is not None and not predicate(step.conclusion):
            continue
        matches.append(link)
    if len(matches) != 1:
        raise RuntimeError("expected one publication-screened fixed source")
    return matches[0]


def build_cited_hopf_surjectivity_proof() -> tuple[ProofStep, tuple[ProofStep, ...], dict]:
    """Reconstruct an inferred codomain and infer H-surjectivity from (5.3)."""
    screened, pi63_goal, citing = _screened_context()
    hopf_link = screened_source_link(
        screened, citing, assertion_id=HOPF_ASSERTION_ID, locator="(5.3)",
        predicate=lambda item: isinstance(item, Relation),
    )
    source_link = screened_source_link(
        screened, citing, locator="Proposition 5.1",
        predicate=_is_generic_eta_group_relation,
    )
    hopf_image = hopf_link.step.conclusion
    schema = source_link.step.conclusion
    target_group = TodaPrimaryGroup(6, 5)
    prior_group = specialize_eta_group_relation(schema, 5)
    goal = MapSurjective(TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), target_group))
    if prior_group.lhs != target_group or not _valid_surjective_pair(
        goal, prior_group, hopf_image,
    ):
        raise RuntimeError("cited Hopf image does not match the prior group generator")

    prior_proposals = expand_registered_eta_specialization(prior_group, (schema,))
    if len(prior_proposals) != 1 or prior_proposals[0].subgoals != (schema,):
        raise RuntimeError("Proposition 5.1 has no unique typed specialization")
    public_options = shared_expansion_provider(screened, proof_target=pi63_goal)(prior_group)
    if not any(
        option.rule.name == prior_proposals[0].rule.name
        and option.subgoals == prior_proposals[0].subgoals
        for option in public_options
    ):
        raise RuntimeError("prior-group specialization absent from shared provider")

    def source_bound_provider(current: object):
        return expand_registered_eta_specialization(current, (schema,))

    group_proof = reconstruct_registered_goal(
        prior_group, screened, citing, source_bound_provider,
        lookup_mode="typed_reference_publication",
    )
    if not (
        group_proof.rule is ProofRule.INFERENCE
        and group_proof.conclusion == prior_group
        and len(group_proof.premises) == 1
        and group_proof.premises[0] is source_link.step
    ):
        raise RuntimeError("prior group not derived from the screened general source")

    rule = cited_hopf_cyclic_surjectivity_rule(goal, prior_group, hopf_image)
    matches = tuple(
        match for match in find_inference_matches_for_rule(
            rule, (group_proof, hopf_link.step),
        )
        if match.premises == (group_proof, hopf_link.step)
    )
    if len(matches) != 1:
        raise RuntimeError("expected exactly one checked Hopf surjectivity inference")
    root = derive_inference_proof_step(matches[0])
    ancestry = proof_ancestry(root)
    leaves = tuple(step for step in ancestry if step.rule is ProofRule.GIVEN)
    if not (
        root.rule is ProofRule.INFERENCE
        and root.conclusion == goal
        and root.premises == (group_proof, hopf_link.step)
        and len(leaves) == 2
        and len({id(step) for step in leaves}) == 2
        and all(step is source_link.step or step is hopf_link.step for step in leaves)
        and all(not step.premises for step in leaves)
        and all(step.rule in (ProofRule.GIVEN, ProofRule.INFERENCE) for step in ancestry)
        and all(step.conclusion != pi63_goal for step in ancestry)
    ):
        raise RuntimeError("Hopf proof contains an untrusted leaf or target group result")
    report = {
        "phase": "171-R2J-R4-R4",
        "mode": "READ_ONLY_CITED_HOPF_SURJECTIVITY_REPLAY",
        "status": "INFERRED",
        "hopf_assertion_id": hopf_link.assertion_id,
        "prior_group_source_id": source_link.assertion_id,
        "source_group_relation": repr(schema),
        "prior_group_inferred": repr(prior_group),
        "cited_hopf_image": repr(hopf_image),
        "conclusion": repr(root.conclusion),
        "root_rule": root.inference_rule.name,
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in ancestry),
        "given_leaves": len(leaves),
        "new_given_added": 0,
        "pi63_group_proven": False,
        "production_modified": False,
        "full_pytest": False,
    }
    return root, ancestry, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R2J-R4-R4 must run on develop")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    print("PHASE171_R2J_R4_R4_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R4_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R4_RESULT=PASS_DRY_RUN", flush=True)
        return
    root, ancestry, report = build_cited_hopf_surjectivity_proof()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files changed during read-only audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    target = OUTPUT / "audit.json"
    target.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R4_H_SURJECTIVE=" + report["status"], flush=True)
    print("PHASE171_R2J_R4_R4_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R4_R4_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R4_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R4_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R4_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R4_REPORT=" + str(target), flush=True)
    print("PHASE171_R2J_R4_R4_RUN=PASS", flush=True)


if __name__ == "__main__":
    main()
