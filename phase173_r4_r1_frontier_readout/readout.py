"""Read the Phase 173 R4-R1 audit report without promoting observations to proofs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPORT_RELATIVE = Path(
    "EHPProofTracerRecovery/phase173_r4_r1_committed_cache_resume/audit.json"
)


def validate_report(data: Any) -> dict[str, Any]:
    """Require the exact audited scope and source guard before reading findings."""
    if not isinstance(data, dict):
        raise ValueError("R4-R1 report must be an object")
    if data.get("phase") != "173-R4-R1" or data.get("scope") != "AUDIT_ONLY":
        raise ValueError("Unexpected phase or scope in R4-R1 report")
    if data.get("status") != "OBSERVATION_ONLY_NOT_A_PROOF":
        raise ValueError("Report does not assert observation-only status")
    if data.get("production_changes") != []:
        raise ValueError("Production changes are not empty")
    preflight = data.get("preflight")
    if not isinstance(preflight, dict):
        raise ValueError("Missing reviewed preflight")
    if preflight.get("reviewed_source_files_unchanged") is not True:
        raise ValueError("Reviewed source guard is not confirmed")
    toda = preflight.get("toda")
    if not isinstance(toda, dict) or toda.get("specialization_i") != 7:
        raise ValueError("Toda (5.6) specialization not recorded")
    if toda.get("specialized_source_groups") != ["pi_6^3", "pi_7^7"]:
        raise ValueError("Unexpected source groups for Toda (5.6)")
    public_root = data.get("public_root")
    if not isinstance(public_root, dict):
        raise ValueError("Runtime root observations are missing; DryRun is insufficient")
    if public_root.get("target_is_screened_given") is not False:
        raise ValueError("Target proof-goal trust boundary is not confirmed")
    if public_root.get("discovered_complete_proof") is not False:
        raise ValueError("This report must not claim a complete proof")
    if not isinstance(public_root.get("root_proposals"), list):
        raise ValueError("Missing root proposals")
    if public_root.get("root_candidate_count") != len(public_root["root_proposals"]):
        raise ValueError("Root count and proposal list disagree")
    if not isinstance(public_root.get("prior_pi63"), dict):
        raise ValueError("Missing prior-pi63 observation")
    if not isinstance(preflight.get("existing_rule_inventory"), list):
        raise ValueError("Missing reviewed rule inventory")
    return data


def summarize_report(data: dict[str, Any]) -> str:
    """Format the source, prior-result and root frontiers without inferring proof."""
    data = validate_report(data)
    preflight = data["preflight"]
    public = data["public_root"]
    prior = public["prior_pi63"]
    outputs = [
        "PHASE173_R4_R1_FRONTIER_READOUT=PASS",
        "SCOPE=AUDIT_ONLY_NO_PROOF_PROMOTION",
        "HEAD=" + str(preflight.get("head", "MISSING")),
        "REVIEWED_SOURCE_UNCHANGED=True",
        "GOAL=" + str(public.get("goal", "MISSING")),
        "ROOT_CANDIDATES=" + str(public["root_candidate_count"]),
        "CITED_PROP44_UNIVERSAL_GIVEN=" + str(public.get("prop44_cited_universal_given_count")),
        "DIRECT_TODA56_GIVEN=" + str(public.get("toda56_decomposition_direct_given_count")),
        "SCREENED_GIVEN_COUNT=" + str(public.get("screened_given_count")),
        "PRIOR_PI63_ELIGIBLE=" + str(prior.get("eligible")),
        "PRIOR_PI63_REASON=" + str(prior.get("reason")),
        "PRIOR_PI63_SOURCE_ASSERTION_ID=" + str(prior.get("source_assertion_id")),
        "PRIOR_PI63_PROVEN_IN_THIS_AUDIT=" + str(prior.get("proven_in_this_audit")),
        "PI77_DB_GOAL_COUNT=" + str(public.get("pi77_db_goal_count")),
        "PI77_PROVEN_IN_THIS_AUDIT=" + str(public.get("pi77_proven_in_this_audit")),
        "TRACKED_WORKTREE_EXCEPTIONS=" + repr(preflight.get("worktree_exceptions", [])),
        "COMMITTED_CACHE_EXCEPTION=" + repr(preflight.get("committed_cache_exception", [])),
        "--- EXISTING_RULE_INVENTORY ---",
    ]
    for index, rule in enumerate(preflight["existing_rule_inventory"], 1):
        if not isinstance(rule, dict):
            raise ValueError("Rule inventory must contain objects")
        outputs.append(
            f"RULE_{index}: name={rule.get('function')} "
            f"defined={rule.get('defined_exactly_once')} "
            f"premise_pattern={rule.get('mentions_premise_pattern')} "
            f"literature_reference={rule.get('mentions_literature_reference')} "
            f"direct_sum={rule.get('mentions_direct_sum')}"
        )
    outputs.append("--- ROOT_PROPOSALS ---")
    for index, root in enumerate(public["root_proposals"], 1):
        if not isinstance(root, dict):
            raise ValueError("Root proposals must be objects")
        outputs.append(f"ROOT_{index}_RULE=" + str(root.get("rule")))
        children = root.get("children", [])
        if not isinstance(children, list):
            raise ValueError("Root children must be a list")
        for child_index, child in enumerate(children, 1):
            if not isinstance(child, dict):
                raise ValueError("Root children must be objects")
            prefix = f"ROOT_{index}_SUBGOAL_{child_index}"
            outputs.extend((
                prefix + "_TYPE=" + str(child.get("type")),
                prefix + "_REPR=" + str(child.get("repr")),
                prefix + "_EXACT_SCREENED_GIVEN=" + str(child.get("exact_screened_given")),
                prefix + "_RULES=" + repr(child.get("immediate_child_rule_names", [])),
                prefix + "_PROBE_ERROR=" + str(child.get("child_probe_error", "NONE")),
            ))
    outputs.extend((
        "COMPLETE_PROOF_CERTIFIED=False",
        "NEXT_STEP=REVIEW_TYPED_PREMISES_AND_SOURCE_BOUND_56_CONNECTION",
        "PHASE173_R4_R1_REPORT_READ_ONLY=True",
    ))
    return "\n".join(outputs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read Phase 173 R4-R1 JSON frontier")
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.report.is_file():
        raise FileNotFoundError("R4-R1 audit.json is unavailable: " + str(args.report))
    data = validate_report(json.loads(args.report.read_text(encoding="utf-8-sig")))
    if args.dry_run:
        print("PHASE173_R4_R1_FRONTIER_READOUT_DRY_RUN=PASS")
        print("PHASE173_R4_R1_NO_PRODUCTION_CHANGES=True")
    else:
        print(summarize_report(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
