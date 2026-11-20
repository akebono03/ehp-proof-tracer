"""Inspect isolated Lemma 5.7 and right-zero transport versus public expansion."""
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
PACKAGE = "phase176_r3r13_two_boundary_audit"
REVIEWED_HEAD = "71386d569456afa48c9d8d007ac63a373fd97efe"
MARKER = "PHASE176_R3R13_WORKER_JSON="
REQUIRED = {
    "phase165_r52_r9_shared_math.py": ("def shared_expansion_provider(",),
    "phase176_r3r10_right_zero_transport_isolated/rule.py": ("def expand_right_zero_transport(", "def right_zero_transport_inputs("),
    "phase176_r3r8_lemma57_provider_binding/audit.py": ("def source_bound_provider(",),
    "phase175_r3r9_lemma57_explicit_public/rule.py": ("def expand_cited_lemma57_explicit_zero(",),
    "phase175_r3r9_lemma57_explicit_public/source.py": ("def build_explicit_lemma57_source(",),
    "phase169_r10e4_ordered_db_prior/db_prior.py": ("def exact_prior_database_result(",),
    "sources/toda/Toda_05_2.tex": (r"\label{lemma:5.7}", r"E(\eta_2\circ\nu')=0"),
}


def command(*args: str) -> str:
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode:
        raise RuntimeError("COMMAND_FAILED " + " ".join(args) + " " + p.stderr[-1000:])
    return p.stdout.strip()


def source_preflight(root: Path) -> dict[str, str]:
    output = {}
    for path, anchors in REQUIRED.items():
        file = root / path
        if not file.is_file():
            raise RuntimeError("REQUIRED_SOURCE_MISSING " + path)
        content = "".join(file.read_text(encoding="utf-8-sig").split())
        if any("".join(a.split()) not in content for a in anchors):
            raise RuntimeError("REQUIRED_ANCHOR_MISSING " + path)
        output[path] = hashlib.sha256(file.read_bytes()).hexdigest()
    return output


def get_previous(root: Path) -> dict:
    base = root / "EHPProofTracerAudit"
    name = "phase176_r3r10_right_zero_transport_isolated"
    record_path = base / name / "report.json"
    if not record_path.is_file():
        raise RuntimeError("R3R10_REPORT_MISSING " + str(record_path))
    record = json.loads(record_path.read_text(encoding="utf-8"))
    obs = record.get("observed", {})
    if (record.get("gate") != "PASS_R3R10_ISOLATED_RIGHT_ZERO_TRANSPORT"
            or obs.get("base_step_inferred") is not True
            or obs.get("isolated_composite_zero_step_inferred") is not True
            or obs.get("shared_composite_zero_candidates") != 0
            or obs.get("root_proof_complete") is not False):
        raise RuntimeError("R3R10_EVIDENCE_NOT_VALIDATED")
    return {"path": str(record_path), "gate": record["gate"], "observed": obs}


def static_wiring_check(root: Path) -> dict:
    shared = (root / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8-sig")
    has_right = "expand_right_zero_transport" in shared
    has_explicit = "expand_cited_lemma57_explicit_zero" in shared
    return {
        "shared_direct_right_transport_reference": has_right,
        "shared_direct_explicit_lemma57_reference": has_explicit,
        "no_direct_registration_detected": not has_right and not has_explicit,
        "note": "Source-level observation only; dynamic comparisons are recorded separately.",
    }


def observe() -> dict:
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
    from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero, build_explicit_lemma57_source
    from phase176_r3r7_lemma57_derived_source_proof.audit import selected_source_steps
    from phase176_r3r8_lemma57_provider_binding.audit import source_bound_provider
    from phase176_r3r10_right_zero_transport_isolated.rule import expand_right_zero_transport, right_zero_transport_inputs, RULE_NAME
    from proof import Relation

    prior = exact_prior_database_result(2, 5)
    if type(prior) is not Relation or prior.lhs != TodaPrimaryGroup(7, 2):
        raise RuntimeError("PRIOR_DB_PRESENTATION_DRIFT")
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError("PRIOR_FACTORIZATION_DRIFT")
    base = GeneratorImage(TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)), Composition(factors[0], factors[1]), Zero())
    whole = GeneratorImage(TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)), prior.rhs.generator, Zero())
    if right_zero_transport_inputs(whole, base) != (base,):
        raise RuntimeError("TYPED_TRANSPORT_MISMATCH")
    public = search_group_from_registered_goal(n=3, k=5)
    if public.status.value != "search_failed" or len(public.open_goals) != 3:
        raise RuntimeError("PUBLIC_FRONTIER_DRIFT")
    target = next((g for g in public.open_goals if type(g) is Relation and g.lhs == TodaPrimaryGroup(8, 3)), None)
    if target is None:
        raise RuntimeError("TARGET_GOAL_MISSING")
    augmented = merge_isolated_cited_source(build_shared_typed_bridge(), build_explicit_lemma57_source(ROOT))
    screened = screen_independent_sources_for_derived_goal(augmented, goal=target)
    source_steps = selected_source_steps(screened, TodaLemma57ExplicitNuPrimeZero)
    if len(source_steps) != 1:
        raise RuntimeError("SCREENED_SOURCE_COUNT_DRIFT")
    ordinary = shared_expansion_provider(screened, proof_target=target)
    isolated_source = source_bound_provider(ordinary, source_steps, TodaLemma57ExplicitNuPrimeZero, expand_cited_lemma57_explicit_zero)
    base_ordinary = tuple(ordinary(base))
    base_bound = tuple(isolated_source(base))
    whole_ordinary = tuple(ordinary(whole))
    whole_bound = tuple(isolated_source(whole))
    isolated_right = tuple(expand_right_zero_transport(whole, base))
    if not isolated_right or isolated_right[0].rule.name != RULE_NAME:
        raise RuntimeError("ISOLATED_RIGHT_RULE_MISSING")
    cited_name = "extract explicit nu-prime zero-suspension clause of Toda Lemma 5.7"
    return {
        "source_steps": len(source_steps),
        "base_ordinary_candidates": len(base_ordinary),
        "base_ordinary_lemma57_candidates": sum(x.rule.name == cited_name for x in base_ordinary),
        "base_isolated_bound_candidates": len(base_bound),
        "base_isolated_lemma57_candidates": sum(x.rule.name == cited_name for x in base_bound),
        "whole_ordinary_candidates": len(whole_ordinary),
        "whole_ordinary_right_transport_candidates": sum(x.rule.name == RULE_NAME for x in whole_ordinary),
        "whole_isolated_source_bound_candidates": len(whole_bound),
        "whole_isolated_right_transport_candidates": len(isolated_right),
        "whole_isolated_right_transport_subgoals": [repr(s) for s in isolated_right[0].subgoals],
        "whole_source_bound_unchanged": whole_bound == whole_ordinary,
        "root_proof_complete": False,
        "public_provider_modified": False,
        "new_given": 0,
        "new_public_mathematical_rules": 0,
    }


def run_worker(timeout: int) -> dict:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    p = subprocess.run((sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"), cwd=ROOT, env=env,
                       text=True, capture_output=True, encoding="utf-8", errors="replace", timeout=timeout)
    lines = [x[len(MARKER):] for x in p.stdout.splitlines() if x.startswith(MARKER)]
    if p.returncode or len(lines) != 1:
        raise RuntimeError("WORKER_FAILED " + str(p.returncode) + " " + p.stderr[-4000:])
    result = json.loads(lines[0])
    if result["new_given"] != 0 or result["root_proof_complete"] is not False:
        raise RuntimeError("FALSE_PROOF_COMPLETION")
    return result


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    return base / "report.json"


def execute(dry_run: bool, timeout: int) -> int:
    report = {"phase": "176_R3R13", "dry_run": dry_run, "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "gate": "FAIL_R3R13", "full_pytest": "NOT_RUN", "new_given": 0,
              "public_mathematical_rules_added": 0, "root_proof_complete": False}
    try:
        if Path(command("git", "rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
            raise RuntimeError("REPOSITORY_ROOT_MISMATCH")
        if command("git", "branch", "--show-current") != "develop":
            raise RuntimeError("DEVELOP_REQUIRED")
        p = subprocess.run(("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD"), cwd=ROOT)
        if p.returncode:
            raise RuntimeError("REVIEWED_HEAD_NOT_ANCESTOR")
        if command("git", "status", "--porcelain", "--untracked-files=no"):
            raise RuntimeError("TRACKED_FILES_DIRTY")
        report["preflight"] = {"head": command("git", "rev-parse", "HEAD"), "sha256": source_preflight(ROOT)}
        report["prior"] = get_previous(Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()))
        report["static"] = static_wiring_check(ROOT)
        if not dry_run:
            report["observed"] = run_worker(timeout)
        report["gate"] = "PASS_R3R13_READ_ONLY_DRYRUN" if dry_run else "PASS_R3R13_TWO_BOUNDARY_AUDIT"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
    destination = report_path()
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R13_GATE=" + report["gate"])
    print("PHASE176_R3R13_REPORT=" + str(destination))
    print("PHASE176_R3R13_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    if "observed" in report:
        for key, value in report["observed"].items():
            print("PHASE176_R3R13_" + key.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R13_ERROR=" + report["error"])
    print("PHASE176_R3R13_FULL_PYTEST=NOT_RUN")
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
