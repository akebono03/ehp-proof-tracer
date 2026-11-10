"""Real source-first Group query audit for the two general R56 inferences."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r56_cyclic_generator_bridge.install import review


PACKAGE = Path(__file__).resolve().parent


def _search_with_model(n: int, k: int, bridge):
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative

    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or result.open_goals:
        raise RuntimeError(f"pi_{n+k}^{n} is not independently completed")
    if len(contexts) != 1:
        raise RuntimeError("public screened source context is missing or duplicated")
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=None,
        derived_target_without_citing_id=True,
    )
    return result, build_linked_proof_narrative_model(result, contexts[0])


def inspect_public() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import (
        CYCLIC_RULE_NAME, SURJECTIVE_RULE_NAME,
    )
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    first, model1 = _search_with_model(6, 5, bridge)
    expected = exact_prior_database_result(6, 5)
    if expected is None or first.conclusion != expected:
        raise RuntimeError("pi_11^6 goal mismatches exact registered database structure")
    cyclic_roots = [step for step in model1.steps
                    if step.rule is ProofRule.INFERENCE
                    and step.conclusion == expected
                    and getattr(step.inference_rule, "name", None) == CYCLIC_RULE_NAME]
    if len(cyclic_roots) != 1:
        raise RuntimeError("pi_11^6 has no inferred, general four-premise cyclic root")
    if len(cyclic_roots[0].premises) != 4:
        raise RuntimeError("pi_11^6 cyclic source contract was weakened")

    second, model2 = _search_with_model(7, 5, bridge)
    if (not isinstance(second.conclusion, TodaPrimaryGroupZeroStatement)
            or second.conclusion.group != TodaPrimaryGroup(12, 7)):
        raise RuntimeError("pi_12^7 zero root changed")
    full = tuple(model2.steps)
    two_step = [step for step in full if step.rule is ProofRule.INFERENCE
                and getattr(step.inference_rule, "name", None) == SURJECTIVE_RULE_NAME]
    prior_used = [step for step in full if step.rule is ProofRule.GIVEN
                  and step.conclusion == expected
                  and "ADOPTED_DATABASE_PRIOR" in (step.note or "")]
    if not two_step:
        raise RuntimeError("pi_12^7 did not select the shared generator-to-surjectivity rule")
    if len(prior_used) != 1:
        raise RuntimeError("pi_12^7 did not reuse the ordered prior DB result")
    if any(item.conclusion == expected and item.rule is ProofRule.INFERENCE for item in full):
        raise RuntimeError("pi_12^7 unnecessarily reproved its admitted prior group")

    return {
        "pi11_6_complete": True,
        "pi11_6_group_root_rule": CYCLIC_RULE_NAME,
        "pi11_6_group_root_premise_count": len(cyclic_roots[0].premises),
        "pi11_6_steps": len(model1.steps),
        "pi11_6_citation_count": len(model1.citations),
        "pi12_7_complete": True,
        "pi12_7_surjectivity_rule": SURJECTIVE_RULE_NAME,
        "pi12_7_prior_db_adopted_once": True,
        "pi12_7_prior_group_reproved": False,
        "pi12_7_steps": len(model2.steps),
        "pi12_7_citation_count": len(model2.citations),
        "new_given": 0,
        "new_math_rules": 2,
        "full_pytest": False,
        "gate": "PASS_R56_TWO_GENERAL_RULES_SOURCE_FIRST_PUBLIC",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = review()
    data = None if args.dry_run else inspect_public()
    report = {
        "phase": "174-R3-R7-R56",
        "local_head": state["local_head"],
        "source_guard": state["source_guard"],
        "inspection": data,
        "gate": "PASS_PREFLIGHT_ONLY" if args.dry_run else data["gate"],
    }
    destination = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    destination /= Path("EHPProofTracerAudit") / "phase174_r3_r7_r56"
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / ("preflight.json" if args.dry_run else "public_proofs.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R56_SOURCE_GUARD=" + str(report["source_guard"]))
    if data is not None:
        for key, value in data.items():
            if key != "gate":
                print("PHASE174_R56_" + key.upper() + "=" + str(value))
    print("PHASE174_R56_REPORT=" + str(output))
    print("PHASE174_R56_GATE=" + str(report["gate"]))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
