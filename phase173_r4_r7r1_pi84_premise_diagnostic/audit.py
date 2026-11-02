"""Read-only diagnosis of the failed pi_8^4 isolated Toda (5.6) proof.

This module does not broaden any proof policy, assert a group conclusion, or
modify the production provider. It observes the actual accepted ProofSteps and
checks which of the four documented source-first premises remains blocked.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
from typing import Any

REVIEWED_HEAD = "fc6631c1b791a856b4af08657af2453e3f198474"
REVIEWED_BLOBS = {
    "phase173_r4_r7_source_first_rule/rule.py": "5113c88e263c28b748c1543ec57bbcedb3eff5bf",
    "phase173_r4_r7_source_first_rule/source.py": "b9b2ddee9296a5eed44163694e28e7789b14aba9",
    "phase173_r4_r7_source_first_rule/audit.py": "aff87939bb9d34488e6f9121659ed3f6b1b80564",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase165_r52_r9_shared_math.py": "3e4c5f9c62b04d618f845b0f82d1cb1cacccdf2e",
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
}


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + result.stderr.strip()[:500])
    return result.stdout.strip()


def preflight(root: Path, *, remote: bool) -> dict[str, str]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("not repository root")
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != REVIEWED_HEAD:
        raise RuntimeError(f"unreviewed branch/HEAD: {branch} {head}")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked files are modified")
    for filename, blob in REVIEWED_BLOBS.items():
        if not (root / filename).is_file():
            raise RuntimeError("reviewed file missing: " + filename)
        if git(root, "rev-parse", "HEAD:" + filename) != blob:
            raise RuntimeError("reviewed Git blob changed: " + filename)
    if remote:
        line = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not line or line.split()[0] != REVIEWED_HEAD:
            raise RuntimeError("remote develop HEAD advanced")
    return {"branch": branch, "head": head, "source_guard": "PASS"}


def _short(value: object, maximum: int = 1000) -> str:
    return repr(value)[:maximum]


def premise_diagnosis(
    obligations: tuple[object, ...], accepted_steps: tuple[object, ...],
    direct_steps: tuple[object, ...], db_steps: tuple[object | None, ...],
    verified_db, root_rule: object,
) -> tuple[dict[str, Any], ...]:
    """Describe observed premise identity and provenance without deriving steps."""
    if len(obligations) != 4 or len(db_steps) != 4:
        raise ValueError("exactly four source-first obligations are required")
    if not callable(verified_db):
        raise TypeError("verified_db must be callable")
    records = []
    for index, premise in enumerate(obligations):
        candidates = tuple(step for step in accepted_steps
                           if type(step.conclusion) is type(premise)
                           and step.conclusion == premise)
        direct = tuple(step for step in direct_steps
                       if type(step.conclusion) is type(premise)
                       and step.conclusion == premise)
        db = db_steps[index]
        records.append({
            "index": index,
            "type": type(premise).__name__,
            "statement": _short(premise, 1300),
            "observed_count": len(candidates),
            "observed_rules": [str(step.rule) for step in candidates],
            "observed_notes": [step.note for step in candidates],
            "observed_inference_names": [
                getattr(step.inference_rule, "name", None) for step in candidates
            ],
            "direct_fixed_count": len(direct),
            "direct_fixed_rules": [str(step.rule) for step in direct],
            "adopted_db_available": db is not None,
            "observed_verified_db": [verified_db(index, step) for step in candidates]
                if index in (1, 2) else [],
            "observed_db_equal": [db is not None and db == step for step in candidates],
        })
    if all(record["observed_count"] == 1 for record in records):
        selected = tuple(next(step for step in accepted_steps
                              if type(step.conclusion) is type(premise)
                              and step.conclusion == premise)
                         for premise in obligations)
        try:
            guard_ok = bool(root_rule.match_guard(selected, {}))
            from proof import find_inference_matches_for_rule
            matching = len(tuple(find_inference_matches_for_rule(root_rule, selected)))
        except Exception as exc:
            guard_ok = False
            matching = 0
            records[0]["premise_set_error"] = type(exc).__name__ + ": " + str(exc)[:500]
        records[0]["root_match_guard_if_observed_selected"] = guard_ok
        records[0]["root_inference_matches_if_observed_selected"] = matching
    return tuple(records)


def inspect_live(root: Path) -> dict[str, Any]:
    """Run the existing isolated pi_8^4 route and retain precise blockers."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase173_r4_r7_source_first_rule.rule import expand_source_first_toda56
    from phase173_r4_r7_source_first_rule.source import screened_source_first_context
    from phase173_r4_r1_lemma54_source_bridge.source import expand_cited_lemma54_hopf
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    goal = exact_prior_database_result(4, 4)
    if goal is None:
        raise RuntimeError("pi_8^4 typed database goal unavailable")
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(encoding="utf-8-sig")
    screened = screened_source_first_context(bridge, goal=goal, chapter=chapter)
    if screened is None:
        raise RuntimeError("reviewed source-first context unavailable")
    direct_steps = tuple(link.step for link in screened.proof_links if link.step is not None)
    available = tuple(step.conclusion for step in direct_steps if step.rule is ProofRule.GIVEN)
    proposals = expand_source_first_toda56(goal, available, proof_target=goal, bridge=screened)
    if len(proposals) != 1:
        raise RuntimeError("expected one bounded source-first pi_8^4 expansion")
    proposal = proposals[0]

    def extra(statement: object):
        hopf = expand_cited_lemma54_hopf(statement, available)
        if hopf:
            return hopf
        return expand_source_first_toda56(statement, available,
                                          proof_target=goal, bridge=screened)

    provider = shared_expansion_provider(
        screened, extra_providers=(extra,), proof_target=goal, prior_conclusions=(),
    )
    context_id = next(iter(screened.registry._assertions))
    result = search_registered_partial_proof(
        n=4, k=4, goal=goal, bridge=screened,
        citing_assertion_id=context_id, expansion_provider=provider,
        lookup_mode="typed_reference",
    )
    db_steps = (None, admitted_db_step(proposal.subgoals[1], proof_target=goal, bridge=screened),
                admitted_db_step(proposal.subgoals[2], proof_target=goal, bridge=screened), None)
    def verify_db(index: int, step: object) -> bool:
        return verified_db_step(step, proof_target=goal, bridge=screened)
    records = premise_diagnosis(
        proposal.subgoals, tuple(result.proven_steps), direct_steps,
        db_steps, verify_db, proposal.rule,
    )
    return {
        "target": "pi_8^4", "search_status": result.status.value,
        "open_goals": [_short(statement, 1300) for statement in result.open_goals],
        "diagnostics": [_short(statement, 1000) for statement in result.diagnostics],
        "proven_steps": len(result.proven_steps),
        "steps": [{"conclusion": _short(step.conclusion),
                   "rule": str(step.rule), "note": step.note,
                   "inference_rule": getattr(step.inference_rule, "name", None)}
                  for step in result.proven_steps],
        "premises": records,
        "root_accepted": any(step.conclusion == goal and step.rule is ProofRule.INFERENCE
                             for step in result.proven_steps),
        "no_new_proof_rules": True,
        "no_target_given": True,
    }


def run(root: Path, *, dry_run: bool, remote: bool) -> int:
    base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    output = base / ("phase173_r4_r7r1_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    report: dict[str, Any] = {
        "phase": "173 R4-R7R1", "mode": "READ_ONLY_PREMISE_DIAGNOSTIC",
        "reviewed_head": REVIEWED_HEAD, "dry_run": dry_run,
        "result": "NOT_STARTED", "full_pytest": False,
        "production_modified": False, "output": str(output),
    }
    print("PHASE173_R4_R7R1_OUTPUT=" + str(output), flush=True)
    before = None
    code = 2
    try:
        before = preflight(root, remote=remote)
        report["preflight"] = before
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
        else:
            observation = inspect_live(root)
            report["observation"] = observation
            print("PHASE173_R4_R7R1_pi_8^4_STATUS=" + observation["search_status"], flush=True)
            print("PHASE173_R4_R7R1_pi_8^4_ROOT_ACCEPTED=" + str(observation["root_accepted"]), flush=True)
            for item in observation["premises"]:
                print(
                    "PHASE173_R4_R7R1_PREMISE=" + str(item["index"]) +
                    " TYPE=" + item["type"] +
                    " OBSERVED=" + str(item["observed_count"]) +
                    " DIRECT=" + str(item["direct_fixed_count"]) +
                    " DB_AVAILABLE=" + str(item["adopted_db_available"]) +
                    " DB_VERIFIED=" + repr(item["observed_verified_db"]) +
                    " RULES=" + repr(item["observed_inference_names"]),
                    flush=True,
                )
            for item in observation["open_goals"][:6]:
                print("PHASE173_R4_R7R1_OPEN=" + item[:500], flush=True)
            print("PHASE173_R4_R7R1_PROVEN_STEPS=" + str(observation["proven_steps"]), flush=True)
            report["result"] = "OBSERVATION_COMPLETE"
        code = 0
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        print("PHASE173_R4_R7R1_ERROR=" + report["error"], flush=True)
    finally:
        if before is not None:
            try:
                report["tracked_unchanged"] = preflight(root, remote=False) == before
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = type(exc).__name__ + ": " + str(exc)[:400]
            if not report["tracked_unchanged"]:
                report["result"] = "TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        (output / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        print("PHASE173_R4_R7R1_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE173_R4_R7R1_RESULT=" + report["result"], flush=True)
        print("PHASE173_R4_R7R1_REPORT=" + str(output / "audit.json"), flush=True)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-remote-check", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), dry_run=args.dry_run,
               remote=not args.skip_remote_check)


if __name__ == "__main__":
    raise SystemExit(main())
