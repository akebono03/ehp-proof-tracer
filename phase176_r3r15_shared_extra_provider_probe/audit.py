"""Read-only proof-search integration probe using shared_expansion_provider's API."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r15_shared_extra_provider_probe"
REVIEWED_HEAD = "dc67a7c79ac483b3c9dbf014fcd26171dfa2b6b2"
MARKER = "PHASE176_R3R15_WORKER_JSON="
SOURCES = {
    "phase176_r3r14_isolated_two_stage_provider/provider.py": "def preceding_zero_image(",
    "phase176_r3r10_right_zero_transport_isolated/rule.py": "def expand_right_zero_transport(",
    "phase175_r3r9_lemma57_explicit_public/rule.py": "def expand_cited_lemma57_explicit_zero(",
    "phase165_r52_r9_shared_math.py": "def shared_expansion_provider(",
    "sources/toda/Toda_05_2.tex": r"E(\eta_2\circ\nu')=0",
}


def git(*args: str, check: bool = True) -> tuple[int, str]:
    process = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                             text=True, encoding="utf-8", errors="replace")
    if check and process.returncode:
        raise RuntimeError("GIT_FAILED " + " ".join(args) + " " + process.stderr[-800:])
    return process.returncode, process.stdout.strip()


def preflight() -> dict:
    if Path(git("rev-parse", "--show-toplevel")[1]).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current")[1] != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD", check=False)[0]:
        raise RuntimeError("REVIEWED_HEAD_NOT_ANCESTOR")
    if git("status", "--porcelain", "--untracked-files=no")[1]:
        raise RuntimeError("TRACKED_FILES_DIRTY")
    for name, anchor in SOURCES.items():
        path = ROOT / name
        if not path.is_file():
            raise RuntimeError("SOURCE_FILE_MISSING " + name)
        normalized = "".join(path.read_text(encoding="utf-8-sig").split())
        if "".join(anchor.split()) not in normalized:
            raise RuntimeError("SOURCE_ANCHOR_MISSING " + name)
    return {"head": git("rev-parse", "HEAD")[1], "source_anchors": len(SOURCES)}


def observe() -> dict:
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase175_r3r6_lemma57_general.source import merge_isolated_cited_source
    from phase175_r3r9_lemma57_explicit_public.source import (
        TodaLemma57ExplicitNuPrimeZero, build_explicit_lemma57_source,
    )
    from phase176_r3r7_lemma57_derived_source_proof.audit import selected_source_steps
    from phase176_r3r14_isolated_two_stage_provider.provider import preceding_zero_image
    from phase176_r3r15_shared_extra_provider_probe.provider import build_screened_extra_provider
    from phase176_r3r10_right_zero_transport_isolated.rule import RULE_NAME as RIGHT_RULE_NAME
    from proof import Relation

    public = search_group_from_registered_goal(n=3, k=5)
    if public.status.value != "search_failed" or len(public.open_goals) != 3:
        raise RuntimeError("PUBLIC_FRONTIER_DRIFT")
    target = next((g for g in public.open_goals if type(g) is Relation
                   and g.lhs == TodaPrimaryGroup(8, 3)), None)
    if target is None:
        raise RuntimeError("PUBLIC_ROOT_GOAL_MISSING")
    prior = exact_prior_database_result(2, 5)
    if type(prior) is not Relation or prior.lhs != TodaPrimaryGroup(7, 2):
        raise RuntimeError("PRIOR_PRESENTATION_CHANGED")
    whole = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        prior.rhs.generator, Zero(),
    )
    base = preceding_zero_image(whole)
    if base is None:
        raise RuntimeError("TYPED_BASE_NOT_AVAILABLE")
    merged = merge_isolated_cited_source(
        build_shared_typed_bridge(), build_explicit_lemma57_source(ROOT),
    )
    screened = screen_independent_sources_for_derived_goal(merged, goal=target)
    steps = selected_source_steps(screened, TodaLemma57ExplicitNuPrimeZero)
    if len(steps) != 1:
        raise RuntimeError("SOURCE_SCREEN_NOT_UNIQUE")
    ordinary = shared_expansion_provider(screened, proof_target=target)
    extra = build_screened_extra_provider(steps)
    connected = shared_expansion_provider(
        screened, extra_providers=(extra,), proof_target=target,
    )
    cited_name = "extract explicit nu-prime zero-suspension clause of Toda Lemma 5.7"
    ordinary_base = tuple(ordinary(base))
    ordinary_whole = tuple(ordinary(whole))
    connected_base = tuple(connected(base))
    connected_whole = tuple(connected(whole))
    base_matches = tuple(x for x in connected_base if x.rule.name == cited_name)
    whole_matches = tuple(x for x in connected_whole if x.rule.name == RIGHT_RULE_NAME)
    if ordinary_base or ordinary_whole:
        raise RuntimeError("BASELINE_CANDIDATE_DRIFT")
    if len(base_matches) != 1 or len(whole_matches) != 1:
        raise RuntimeError("SHARED_EXTRA_PROVIDER_NOT_OFFERED")
    if base_matches[0].subgoals != (steps[0].conclusion,):
        raise RuntimeError("CITATION_PREMISE_CHANGED")
    if whole_matches[0].subgoals != (base,):
        raise RuntimeError("RIGHT_PREMISE_CHANGED")
    if tuple(connected(target)) != tuple(ordinary(target)):
        raise RuntimeError("ROOT_OPTIONS_MUTATED")
    return {
        "screened_cited_source_steps": len(steps),
        "ordinary_base_candidates": len(ordinary_base),
        "extra_base_cited_candidates": len(base_matches),
        "ordinary_whole_candidates": len(ordinary_whole),
        "extra_whole_right_candidates": len(whole_matches),
        "extra_whole_right_subgoals": [repr(x) for x in whole_matches[0].subgoals],
        "root_options_unchanged": True,
        "public_search_status": public.status.value,
        "public_open_goals": len(public.open_goals),
        "shared_api_accepts_extra_provider": True,
        "production_modified": False,
        "root_proof_complete": False,
        "new_given": 0,
        "public_mathematical_rules_added": 0,
        "full_pytest": "NOT_RUN",
    }


def report_path() -> Path:
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "report.json"


def execute(dry_run: bool, timeout: int) -> int:
    report = {
        "phase": "176_R3R15", "dry_run": dry_run,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate": "FAIL_R3R15", "full_pytest": "NOT_RUN",
        "root_proof_complete": False, "new_given": 0,
        "public_mathematical_rules_added": 0,
    }
    try:
        report["preflight"] = preflight()
        if not dry_run:
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
            proc = subprocess.run(
                (sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"),
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                errors="replace", env=env, timeout=timeout,
            )
            rows = [line[len(MARKER):] for line in proc.stdout.splitlines()
                    if line.startswith(MARKER)]
            if proc.returncode or len(rows) != 1:
                raise RuntimeError("WORKER_FAILED " + str(proc.returncode) + " " + proc.stderr[-4000:])
            data = json.loads(rows[0])
            if (data.get("root_proof_complete") is not False
                    or data.get("production_modified") is not False
                    or data.get("shared_api_accepts_extra_provider") is not True):
                raise RuntimeError("INVALID_COMPLETION_CLAIM")
            report["observed"] = data
        report["gate"] = ("PASS_R3R15_READ_ONLY_DRYRUN" if dry_run else
                          "PASS_R3R15_SHARED_EXTRA_PROVIDER_PROBE")
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
    path = report_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R15_GATE=" + report["gate"])
    print("PHASE176_R3R15_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE176_R3R15_REPORT=" + str(path))
    if "observed" in report:
        for key, value in report["observed"].items():
            print("PHASE176_R3R15_" + key.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R15_ERROR=" + report["error"])
    print("PHASE176_R3R15_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout", type=int, default=180)
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
