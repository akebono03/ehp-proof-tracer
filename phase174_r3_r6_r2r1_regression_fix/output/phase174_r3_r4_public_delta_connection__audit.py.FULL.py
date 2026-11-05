"""Verify the new rule is reconstructed through the ordinary public provider.

Proof of the Delta-zero subgoal is NOT a proof of the pi_8^5 named group goal.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile

from phase174_r3_r4_public_delta_connection.patch import (
    EXPECTED_SOURCE_SHA, SOURCE_PATH, git_blob_sha, replace_provider_call,
)

REVIEWED_HEAD = "ae2fdbffc4ce15b4141933dc9e529ff450265be1"
RULE_NAME = "EHP injective suspension and Delta-E exactness imply zero Delta"


def source_commit_and_worktree_match() -> bool:
    source = Path.cwd() / SOURCE_PATH
    original = subprocess.run(
        ("git", "show", "HEAD:" + SOURCE_PATH),
        check=True, capture_output=True,
    ).stdout
    return (
        git_blob_sha(original) == EXPECTED_SOURCE_SHA
        and source.read_bytes() == replace_provider_call(original)
    )


def prior_evidence() -> dict[str, object]:
    path = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    path = path / "EHPProofTracerAudit" / "phase174_r3_r3" / "audit.json"
    if not path.is_file():
        raise FileNotFoundError("Prior R3-R3 report is absent: " + str(path))
    prior = json.loads(path.read_text(encoding="utf-8-sig"))
    trial = prior.get("typed_inference_trial")
    if (
        prior.get("phase") != "174-R3-R3"
        or prior.get("local_head") != REVIEWED_HEAD
        or prior.get("mode") != "ISOLATED_GENERIC_INJECTION_TO_DELTA_ZERO"
        or prior.get("new_public_proof_steps") != 0
        or prior.get("full_pytest_performed") is not False
        or not isinstance(trial, dict)
        or trial.get("verified_in_memory_delta_zero") is not True
        or trial.get("new_given") != 0
        or trial.get("public_expansion_provider_modified") is not False
        or len(trial.get("premises", ())) != 2
        or not all(p.get("proof_status") == "VERIFIED_SOURCE_INFERENCE" for p in trial["premises"])
    ):
        raise ValueError("R3-R3 cited evidence or its original HEAD changed")
    return {
        "path": str(path),
        "origin_head": prior["local_head"],
        "premise_count": 2,
        "in_memory_delta_step_confirmed": True,
    }


def inspect_public_provider() -> dict[str, object]:
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from phase165_r12_r11_prop42_unified import (
        TodaProp42GeneralExactnessStatement,
        prefer_universal_prop42_derivation,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
    from phase174_r3_r6_r2_prop44_lemma54.source import (
        attach_earlier_verified_lemma54,
    )
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase174_r3_r3_injective_delta_zero.audit import proof_has_cited_leaf
    from phase174_r3_r3_injective_delta_zero.rule import delta_e_injectivity_inputs
    from proof import ProofRule
    from toda_rules import TodaDeltaZeroStatement

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(goals) != 1:
        raise ValueError("Expected a single registered typed pi_8^5 target")
    target = goals[0]
    citation = resolve_specialized_goal_citing_id(bridge, target)
    if citation is None:
        raise ValueError("No actual pi_8^5 publication position")
    amended = attach_earlier_verified_lemma54(bridge, citation)
    if amended is bridge:
        raise ValueError("Verified Lemma 5.4 must precede this proof target")
    bridge = amended
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citation,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    zero_delta = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    if zero_delta in available:
        raise ValueError("Zero Delta has been promoted to a source GIVEN")
    provider = shared_expansion_provider(screened, proof_target=target)
    proposals = provider(zero_delta)
    integrated = tuple(p for p in proposals if getattr(p.rule,"name",None) == RULE_NAME)
    if len(integrated) != 1:
        raise ValueError("The general Delta rule is not uniquely connected to the public provider")
    if integrated[0].subgoals != delta_e_injectivity_inputs(zero_delta):
        raise ValueError("Public subgoals diverge from the reviewed EHP inference")
    # Preserve First Successful Proof Search. An older valid route can win
    # before the new proposal; verify the new rule with a diagnostic root filter.
    # Subsidiary goals still use the actual citation-screened public provider.
    def new_rule_for_root(query: object):
        options = provider(query)
        if query != zero_delta:
            return options
        return tuple(
            proposal for proposal in options
            if getattr(proposal.rule, "name", None) == RULE_NAME
        )

    step = reconstruct_registered_goal(
        zero_delta, screened, citation, new_rule_for_root,
        lookup_mode="typed_reference",
    )
    if (
        step.rule is not ProofRule.INFERENCE or step.conclusion != zero_delta
        or getattr(step.inference_rule, "name", None) != RULE_NAME
        or len(step.premises) != 2
        or any(prior.rule is not ProofRule.INFERENCE for prior in step.premises)
        or not proof_has_cited_leaf(step.premises[0], TodaProp44UniversalStatement())
        or not proof_has_cited_leaf(step.premises[0], TodaLemma54TypedSource())
        or not proof_has_cited_leaf(step.premises[1], TodaProp42GeneralExactnessStatement())
    ):
        raise ValueError("Connected rule lacks real public source ancestry")

    selected = reconstruct_registered_goal(
        zero_delta, screened, citation, provider, lookup_mode="typed_reference",
    )
    if selected.rule is not ProofRule.INFERENCE or selected.conclusion != zero_delta:
        raise ValueError("Ordinary public provider cannot reconstruct Delta zero")
    return {
        "root_goal_type": type(target).__name__,
        "zero_delta_goal_type": type(zero_delta).__name__,
        "publication_citing_assertion_id": citation,
        "screened_source_count": len(available),
        "new_public_provider_proposals": len(integrated),
        "new_rule_name": RULE_NAME,
        "ordinary_first_success_rule": getattr(selected.inference_rule, "name", None),
        "premise_types": [type(x.conclusion).__name__ for x in step.premises],
        "premises_both_inferred": True,
        "source_ancestry_checked": True,
        "delta_zero_publicly_reconstructed": True,
        "named_group_goal_complete": False,
        "new_given": 0,
    }


def main() -> int:
    if not source_commit_and_worktree_match():
        raise ValueError("Production source was not connected exactly as reviewed")
    evidence = prior_evidence()
    current = inspect_public_provider()
    report = {
        "phase": "174-R3-R4",
        "mode": "PUBLIC_PROVIDER_DELTA_ONLY",
        "local_head": subprocess.run(
            ("git", "rev-parse", "HEAD"), check=True,
            capture_output=True, text=True,
        ).stdout.strip(),
        "prior_r3r3": evidence,
        "public_delta_result": current,
        "new_public_given": 0,
        "named_group_complete": False,
        "full_pytest_performed": False,
    }
    root = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    root = root / "EHPProofTracerAudit" / "phase174_r3_r4"
    root.mkdir(parents=True, exist_ok=True)
    dest = root / "audit.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R3R4_LOCAL_HEAD=" + report["local_head"])
    print("PHASE174_R3R4_PRIOR_R3R3=PASS")
    print("PHASE174_R3R4_PUBLIC_DELTA_PROPOSALS=" + str(current["new_public_provider_proposals"]))
    print("PHASE174_R3R4_PUBLIC_DELTA_RECONSTRUCTED=" + str(current["delta_zero_publicly_reconstructed"]))
    print("PHASE174_R3R4_TWO_INFERRED_PREMISES=" + str(current["premises_both_inferred"]))
    print("PHASE174_R3R4_SOURCE_ANCESTRY=PASS")
    print("PHASE174_R3R4_NAMED_GROUP_COMPLETED=False")
    print("PHASE174_R3R4_REPORT=" + str(dest))
    print("PHASE174_R3R4_AUDIT_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
