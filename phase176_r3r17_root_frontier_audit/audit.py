"""Read-only inspection of the public (n,k)=(3,5) proof-search frontier."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r17_root_frontier_audit"


def git(*args: str) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("GIT_COMMAND_FAILED: " + " ".join(args) + ": " + result.stderr[-1000:])
    return result.stdout.strip()


def preflight() -> dict[str, object]:
    from phase176_r3r16_public_connection.installer import preflight as installed_preflight
    _, status = installed_preflight()
    if status != "ALREADY_INSTALLED":
        raise RuntimeError("R3R16_PUBLIC_CONNECTION_REQUIRED: " + status)
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_GIT_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    return {
        "head": git("rev-parse", "HEAD"),
        "r3r16_install": status,
        "tracked_patch_expected": "phase165_r52_r9_shared_math.py",
        "full_pytest": "NOT_RUN",
    }


def describe_options(options: tuple, limit: int = 24) -> dict[str, object]:
    """Summarize unverified proposals; a candidate is not a proved step."""
    rows = tuple(options)
    return {
        "count": len(rows),
        "truncated": len(rows) > limit,
        "options": [
            {"rule": getattr(o.rule, "name", type(o.rule).__name__),
             "subgoal_count": len(o.subgoals),
             "subgoals": [repr(x)[:800] for x in o.subgoals]}
            for o in rows[:limit]
        ],
    }


def classify_frontier(*, public_status: str, root_options_count: int,
                      proved_zero_image: bool) -> str:
    if public_status == "complete":
        return "ROOT_COMPLETE"
    if root_options_count == 0 and proved_zero_image:
        return "ROOT_RULE_FRONTIER_AFTER_PROVED_ZERO_IMAGE"
    if root_options_count > 0:
        return "ROOT_HAS_UNVERIFIED_CANDIDATES"
    return "ROOT_FRONTIER_UNRESOLVED"


def observe() -> dict[str, object]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase175_r3r9_lemma57_explicit_public.rule import RULE_NAME as LEMMA57_RULE
    from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
    from phase176_r3r10_right_zero_transport_isolated.rule import RULE_NAME as RIGHT_RULE
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from proof import Relation, ProofRule

    public = search_group_from_registered_goal(n=3, k=5)
    root_goal = next((x for x in public.open_goals
                      if type(x) is Relation and x.lhs == TodaPrimaryGroup(8, 3)), None)
    if root_goal is None:
        root_goal = exact_prior_database_result(3, 5)
    if root_goal is None or root_goal.lhs != TodaPrimaryGroup(8, 3):
        raise RuntimeError("TYPED_ROOT_GOAL_NOT_FOUND")
    previous = exact_prior_database_result(2, 5)
    if previous is None:
        raise RuntimeError("TYPED_PREVIOUS_GOAL_NOT_FOUND")
    factors = typed_composition_factors(previous.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError("PREVIOUS_GENERATOR_FACTORIZATION_CHANGED")
    base = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
        Composition(factors[0], factors[1]), Zero(),
    )
    whole = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        previous.rhs.generator, Zero(),
    )
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root_goal)
    provider = shared_expansion_provider(screened, proof_target=root_goal)
    root_options = tuple(provider(root_goal))
    base_options = tuple(o for o in provider(base) if o.rule.name == LEMMA57_RULE)
    whole_options = tuple(o for o in provider(whole) if o.rule.name == RIGHT_RULE)
    source_steps = tuple(link.step for link in screened.proof_links
                         if link.step is not None
                         and type(link.step.conclusion) is TodaLemma57ExplicitNuPrimeZero)
    if len(source_steps) != 1 or len(base_options) != 1 or len(whole_options) != 1:
        raise RuntimeError("R3R16_TWO_STAGE_CANDIDATE_REGRESSION")
    citing_id = next(link.assertion_id for link in screened.proof_links
                     if link.step is not None
                     and type(link.step.conclusion) is TodaLemma57ExplicitNuPrimeZero)
    inferred = reconstruct_registered_goal(
        whole, screened, citing_id, provider, lookup_mode="typed_reference",
    )
    if inferred.rule is not ProofRule.INFERENCE or inferred.conclusion != whole:
        raise RuntimeError("R3R16_RECURSIVE_PROOF_REGRESSION")
    rows = {
        "target": [3, 5],
        "public_status": public.status.value,
        "public_open_goals_count": len(public.open_goals),
        "public_open_goal_types": [type(x).__name__ for x in public.open_goals],
        "public_open_goals": [repr(x)[:1200] for x in public.open_goals[:12]],
        "root_goal": repr(root_goal)[:2000],
        "root_options": describe_options(root_options),
        "base_cited_options": len(base_options),
        "whole_right_options": len(whole_options),
        "screened_lemma57_source_steps": len(source_steps),
        "recursive_two_stage_proved": True,
        "root_proof_complete": public.status.value == "complete",
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_modified_by_audit": False,
        "full_pytest": "NOT_RUN",
    }
    rows["frontier_classification"] = classify_frontier(
        public_status=rows["public_status"],
        root_options_count=rows["root_options"]["count"],
        proved_zero_image=rows["recursive_two_stage_proved"],
    )
    return rows


def report_file() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "report.json"


def execute(dry_run: bool) -> int:
    report: dict[str, object] = {
        "phase": "176_R3R17", "dry_run": dry_run,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate": "FAIL_R3R17", "full_pytest": "NOT_RUN",
    }
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["observed"] = observe()
        report["gate"] = (
            "PASS_R3R17_READ_ONLY_DRYRUN" if dry_run else
            "PASS_R3R17_ROOT_FRONTIER_RECORDED"
        )
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    output = report_file()
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R17_GATE=" + str(report["gate"]))
    print("PHASE176_R3R17_REPORT=" + str(output))
    if "preflight" in report:
        print("PHASE176_R3R17_HEAD=" + str(report["preflight"]["head"]))
    if "observed" in report:
        row = report["observed"]
        print("PHASE176_R3R17_PUBLIC_STATUS=" + row["public_status"])
        print("PHASE176_R3R17_PUBLIC_OPEN_GOALS=" + str(row["public_open_goals_count"]))
        print("PHASE176_R3R17_ROOT_CANDIDATES=" + str(row["root_options"]["count"]))
        print("PHASE176_R3R17_ROOT_RULES=" + repr([x["rule"] for x in row["root_options"]["options"]]))
        print("PHASE176_R3R17_FRONTIER=" + row["frontier_classification"])
        print("PHASE176_R3R17_RECURSIVE_TWO_STAGE_PROVED=" + str(row["recursive_two_stage_proved"]))
        print("PHASE176_R3R17_ROOT_PROOF_COMPLETE=" + str(row["root_proof_complete"]))
    if "error" in report:
        print("PHASE176_R3R17_ERROR=" + report["error"])
    print("PHASE176_R3R17_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    return execute(parser.parse_args().dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
