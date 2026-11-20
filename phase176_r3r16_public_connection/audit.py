"""R3R16 focused public connection audit; no invented complete-proof status."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r16_public_connection"


def report_file() -> Path:
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "report.json"


def observe() -> dict:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
    from phase175_r3r9_lemma57_explicit_public.rule import RULE_NAME as CITED_RULE
    from phase176_r3r10_right_zero_transport_isolated.rule import RULE_NAME as RIGHT_RULE
    from phase176_r3r16_public_connection.provider import build_public_lemma57_right_provider
    from proof import Relation

    root = search_group_from_registered_goal(n=3, k=5)
    goal = next((g for g in root.open_goals if type(g) is Relation and g.lhs == TodaPrimaryGroup(8, 3)), None)
    # A completed search has no open goal; use registered DB target only as a goal if needed.
    if goal is None:
        from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
        goal = exact_prior_database_result(3, 5)
    if goal is None:
        raise RuntimeError("TARGET_RELATION_NOT_AVAILABLE")
    prior = exact_prior_database_result(2, 5)
    if prior is None:
        raise RuntimeError("PRIOR_NOT_AVAILABLE")
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError("EXPECTED_TYPED_COMPOSITION_MISSING")
    base = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
        Composition(factors[0], factors[1]), Zero(),
    )
    whole = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        prior.rhs.generator, Zero(),
    )
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    accepted = tuple(link.step for link in screened.proof_links if
                     link.step is not None and type(link.step.conclusion) is TodaLemma57ExplicitNuPrimeZero)
    if len(accepted) != 1:
        raise RuntimeError("CITED_SOURCE_SCREEN_COUNT_NOT_ONE")
    provider = shared_expansion_provider(screened, proof_target=goal)
    cited = tuple(o for o in provider(base) if o.rule.name == CITED_RULE)
    right = tuple(o for o in provider(whole) if o.rule.name == RIGHT_RULE)
    if len(cited) != 1 or len(right) != 1 or right[0].subgoals != (base,):
        raise RuntimeError("PUBLIC_TWO_STEP_PROPOSAL_MISSING")
    from proof import ProofRule, find_inference_matches_for_rule
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    cited_matches = tuple(find_inference_matches_for_rule(cited[0].rule, accepted))
    if len(cited_matches) != 1:
        raise RuntimeError("PUBLIC_CITED_PROOF_STEP_NOT_MATCHED")
    step1 = derive_inference_proof_step(cited_matches[0])
    matches2 = tuple(find_inference_matches_for_rule(right[0].rule, (step1,)))
    if len(matches2) != 1:
        raise RuntimeError("PUBLIC_RIGHT_PROOF_STEP_NOT_MATCHED")
    step2 = derive_inference_proof_step(matches2[0])
    if (step1.rule is not ProofRule.INFERENCE or step2.rule is not ProofRule.INFERENCE
            or step2.premises != (step1,)):
        raise RuntimeError("PUBLIC_NESTED_PROOF_INVALID")
    # Exercise the genuine recursive proof engine, not just manual rule matching.
    from phase165_r3_recursive_search import reconstruct_registered_goal
    citation_id = next(link.assertion_id for link in screened.proof_links
                       if link.step is not None
                       and type(link.step.conclusion) is TodaLemma57ExplicitNuPrimeZero)
    recursively_proved = reconstruct_registered_goal(
        whole, screened, citation_id, provider, lookup_mode="typed_reference",
    )
    if recursively_proved.conclusion != whole or recursively_proved.rule is not ProofRule.INFERENCE:
        raise RuntimeError("RECURSIVE_PUBLIC_PROOF_MISSING")
    return {
        "recursive_public_two_stage_proved": True,
        "screened_cited_source_steps": len(accepted),
        "public_base_cited_candidates": len(cited),
        "public_whole_right_candidates": len(right),
        "public_nested_inference_steps": 2,
        "public_search_status": root.status.value,
        "public_open_goals": len(root.open_goals),
        "root_proof_complete": root.status.value == "complete",
        "new_direct_group_given": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = {"phase": "176_R3R16", "dry_run": args.dry_run,
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "gate": "FAIL_R3R16", "full_pytest": "NOT_RUN"}
    try:
        from phase176_r3r16_public_connection.installer import preflight
        _, status = preflight()
        if args.dry_run:
            report["gate"] = "PASS_R3R16_DRYRUN_" + status
        else:
            if status != "ALREADY_INSTALLED":
                raise RuntimeError("PUBLIC_INSTALL_MISSING")
            report["observed"] = observe()
            report["gate"] = "PASS_R3R16_PUBLIC_TWO_STEP_CONNECTED"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    target = report_file()
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R16_GATE=" + report["gate"])
    if "observed" in report:
        for key, value in report["observed"].items():
            print("PHASE176_R3R16_" + key.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R16_ERROR=" + report["error"])
    print("PHASE176_R3R16_REPORT=" + str(target))
    print("PHASE176_R3R16_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
