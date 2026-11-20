"""R3R10: isolated generic right-composition zero-image inference audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r10_right_zero_transport_isolated"
REVIEWED_HEAD = "01880f0cb62ffa610a91ef8f474c4d260f0ecf66"
MARKER = "PHASE176_R3R10_WORKER_JSON="
SOURCES = {
    "phase176_r3r9_right_composition_type_boundary/audit.py": (
        "def observe(", "GENERATOR_IMAGE_BASE_ZERO_TO_RIGHT_COMPOSITION_ZERO_TRANSPORT_NOT_CERTIFIED",
    ),
    "phase176_r3r7_lemma57_derived_source_proof/audit.py": (
        "def derive_from_existing_source(",
    ),
    "phase175_r3r9_lemma57_explicit_public/source.py": (
        "def build_explicit_lemma57_source(",
    ),
    "phase175_r3r9_lemma57_explicit_public/rule.py": (
        "def expand_cited_lemma57_explicit_zero(",
    ),
    "phase174_r3_r7_r9_composition_associativity/rule.py": (
        "def typed_composition_factors(",
    ),
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": (
        "def expression_endpoints(",
    ),
    "phase165_r52_r9_shared_math.py": (
        "def build_shared_typed_bridge(",
    ),
    "sources/toda/Toda_05_2.tex": (r"\label{lemma:5.7}", r"E(\eta_2\circ\nu')=0"),
}


def git(*args: str, check: bool = True) -> tuple[int, str]:
    result = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=False)
    if check and result.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(args) + ": " + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def check_sources(root: Path) -> dict[str, str]:
    hashes = {}
    for name, anchors in SOURCES.items():
        path = root / name
        if not path.is_file():
            raise RuntimeError("REQUIRED_SOURCE_MISSING: " + name)
        contents = "".join(path.read_text(encoding="utf-8-sig").split())
        if any("".join(anchor.split()) not in contents for anchor in anchors):
            raise RuntimeError("SOURCE_ANCHOR_MISSING: " + name)
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")[1]).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current")[1] != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD", check=False)[0]:
        raise RuntimeError("REVIEWED_HEAD_NOT_ANCESTOR")
    if git("status", "--porcelain", "--untracked-files=no")[1]:
        raise RuntimeError("TRACKED_FILES_DIRTY")
    return {"head": git("rev-parse", "HEAD")[1],
            "source_sha256": check_sources(ROOT), "full_pytest": "NOT_RUN",
            "historical_source_guards": "FOUR_KNOWN_FAILURES_NOT_PASSING"}


def observe() -> dict[str, object]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase175_r3r6_lemma57_general.source import merge_isolated_cited_source
    from phase175_r3r9_lemma57_explicit_public.rule import expand_cited_lemma57_explicit_zero
    from phase175_r3r9_lemma57_explicit_public.source import (
        TodaLemma57ExplicitNuPrimeZero, build_explicit_lemma57_source,
    )
    from phase176_r3r7_lemma57_derived_source_proof.audit import (
        derive_from_existing_source, selected_source_steps,
    )
    from phase176_r3r8_lemma57_provider_binding.audit import source_bound_provider
    from phase176_r3r10_right_zero_transport_isolated.rule import (
        RULE_NAME, expand_right_zero_transport, right_zero_transport_inputs,
    )
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    from proof import ProofRule, Relation, find_inference_matches_for_rule

    result = search_group_from_registered_goal(n=3, k=5)
    if result.status.value != "search_failed" or len(result.open_goals) != 3:
        raise RuntimeError("PUBLIC_SEARCH_FRONTIER_DRIFT")
    target = next((g for g in result.open_goals
                   if type(g) is Relation and g.lhs == TodaPrimaryGroup(8, 3)), None)
    if target is None:
        raise RuntimeError("TARGET_GOAL_MISSING")
    prior = exact_prior_database_result(2, 5)
    if type(prior) is not Relation or prior.lhs != TodaPrimaryGroup(7, 2):
        raise RuntimeError("PRIOR_GOAL_MISSING")
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError("THREE_FACTOR_GENERATOR_REQUIRED")
    prefix = Composition(factors[0], factors[1])
    base = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
        prefix, Zero(),
    )
    whole = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        prior.rhs.generator, Zero(),
    )
    if right_zero_transport_inputs(whole, base) != (base,):
        raise RuntimeError("R3R10_TYPE_CONTRACT_NOT_SATISFIED")
    bridge = merge_isolated_cited_source(
        build_shared_typed_bridge(), build_explicit_lemma57_source(ROOT),
    )
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target)
    sources = selected_source_steps(screened, TodaLemma57ExplicitNuPrimeZero)
    if len(sources) != 1:
        raise RuntimeError("LEMMA57_SOURCE_COUNT_DRIFT")
    ordinary = shared_expansion_provider(screened, proof_target=target)
    bound = source_bound_provider(
        ordinary, sources, TodaLemma57ExplicitNuPrimeZero,
        expand_cited_lemma57_explicit_zero,
    )
    cited = tuple(x for x in bound(base) if
                  x.rule.name == "extract explicit nu-prime zero-suspension clause of Toda Lemma 5.7")
    if len(cited) != 1:
        raise RuntimeError("LEMMA57_CANDIDATE_COUNT_DRIFT")
    base_step = derive_from_existing_source(cited[0], sources[0])
    if base_step.rule is not ProofRule.INFERENCE or base_step.conclusion != base:
        raise RuntimeError("LEMMA57_STEP_NOT_INFERRED")
    options = expand_right_zero_transport(whole, base)
    if len(options) != 1 or options[0].rule.name != RULE_NAME:
        raise RuntimeError("R3R10_ZERO_TRANSPORT_NOT_OFFERED")
    if options[0].subgoals != (base,):
        raise RuntimeError("R3R10_SUBGOAL_MISMATCH")
    matches = tuple(find_inference_matches_for_rule(options[0].rule, (base_step,)))
    if len(matches) != 1:
        raise RuntimeError("R3R10_ACTUAL_MATCH_NOT_UNIQUE")
    whole_step = derive_inference_proof_step(matches[0])
    if (whole_step.rule is not ProofRule.INFERENCE
            or whole_step.conclusion != whole
            or whole_step.premises != (base_step,)):
        raise RuntimeError("R3R10_PROOF_ANCESTRY_INVALID")
    return {
        "target": [3, 5], "search_status": result.status.value,
        "open_goals": len(result.open_goals),
        "source_count": len(sources),
        "base_step_inferred": True,
        "isolated_composite_zero_step_inferred": True,
        "isolated_composite_zero_rule": RULE_NAME,
        "isolated_subgoals": [repr(x) for x in options[0].subgoals],
        "shared_composite_zero_candidates": len(ordinary(whole)),
        "no_direct_root_given": True,
        "root_proof_complete": False,
        "production_modified": False,
        "new_given": 0,
        "new_isolated_mathematical_rules": 1,
        "public_mathematical_rules_added": 0,
        "full_pytest": "NOT_RUN",
    }


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    try:
        run = subprocess.run((sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"),
                             cwd=ROOT, env=env, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("WORKER_TIMEOUT") from exc
    lines = [line[len(MARKER):] for line in run.stdout.splitlines() if line.startswith(MARKER)]
    if run.returncode or len(lines) != 1:
        raise RuntimeError("WORKER_FAILED: " + str(run.returncode) + " " + run.stderr[-5000:])
    report = json.loads(lines[0])
    if (report.get("root_proof_complete") is not False
            or report.get("new_given") != 0
            or report.get("isolated_composite_zero_step_inferred") is not True):
        raise RuntimeError("FALSE_ISOLATED_PROOF_CLAIM")
    return report


def report_path() -> Path:
    directory = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "report.json"


def execute(dry_run: bool, timeout: int) -> int:
    report = {"phase": "176_R3R10", "dry_run": dry_run,
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "gate": "FAIL_R3R10", "full_pytest": "NOT_RUN",
              "new_given": 0, "public_mathematical_rules_added": 0,
              "root_proof_complete": False}
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["observed"] = worker(timeout)
        report["gate"] = "PASS_R3R10_READ_ONLY_DRYRUN" if dry_run else "PASS_R3R10_ISOLATED_RIGHT_ZERO_TRANSPORT"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-8000:]
    report_path().write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R10_GATE=" + report["gate"])
    print("PHASE176_R3R10_REPORT=" + str(report_path()))
    print("PHASE176_R3R10_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    if "observed" in report:
        row = report["observed"]
        print("PHASE176_R3R10_SOURCE_COUNT=" + str(row["source_count"]))
        print("PHASE176_R3R10_BASE_STEP_INFERRED=" + str(row["base_step_inferred"]))
        print("PHASE176_R3R10_ISOLATED_COMPOSITE_ZERO_STEP_INFERRED=" + str(row["isolated_composite_zero_step_inferred"]))
        print("PHASE176_R3R10_SHARED_COMPOSITE_ZERO_CANDIDATES=" + str(row["shared_composite_zero_candidates"]))
        print("PHASE176_R3R10_GROUP=(3,5) STATUS=" + row["search_status"] + " OPEN=" + str(row["open_goals"]))
    if "error" in report:
        print("PHASE176_R3R10_ERROR=" + report["error"])
    print("PHASE176_R3R10_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe(), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return execute(args.dry_run, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
