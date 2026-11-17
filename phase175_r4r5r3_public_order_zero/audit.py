"""Phase 175 R4R5R3: source-guarded general public order-zero wiring.

One shared backward provider is added; previous isolated R4R5R2 results
are revalidated as audit provenance and NEVER inserted as proof certificates.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

from phase175_r4r5r3_public_order_zero import installer

EXPECTED_HEAD = "2789fb6297efaa35962695b95300063feb6e2ea2"
PRIOR_GATE = "PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_ISOLATED_NOT_PUBLIC"
PRIOR_PACKAGE = "phase175_r4r5_eta7_annihilator_isolated"
PRIOR_RULE_SHA256 = "228a856bb4aa535edf4243885dee8472b8789c7d85c3507fc5eb1aace8a42bcd"
DRY_GATE = "PASS_R4R5R3_PUBLIC_PROVIDER_DRYRUN"
FINAL_GATE = "PASS_R4R5R3_SHARED_PROVIDER_CONNECTED_NOT_COMPLETE"


def latest_prior(explicit: Path | None) -> Path:
    if explicit is not None:
        path = explicit.resolve()
        if not path.is_file():
            raise RuntimeError("R4R5R3_PRIOR_REPORT_NOT_FOUND")
        return path
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    for candidate in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            content = json.loads(candidate.read_text(encoding="utf-8"))
        except (ValueError, OSError, UnicodeError):
            continue
        if isinstance(content, dict) and content.get("gate") == PRIOR_GATE:
            return candidate
    raise RuntimeError("R4R5R3_SUCCESSFUL_R4R5R2_REPORT_MISSING")


def validate_prior(prior: object) -> dict[str, object]:
    if not isinstance(prior, dict):
        raise RuntimeError("R4R5R3_PRIOR_REPORT_INVALID")
    expected = {
        "phase": "175-R4R5R2", "gate": PRIOR_GATE,
        "dry_run": False, "production_changes": [], "new_given": 0,
        "new_mathematical_rules": 1, "rule_connected_to_public": False,
        "pi95_proof_complete": False, "full_pytest_executed": False,
    }
    if any(prior.get(k) != v for k, v in expected.items()):
        raise RuntimeError("R4R5R3_PRIOR_SCOPE_INVALID")
    pre = prior.get("preflight", {})
    eta = prior.get("eta7", {})
    direct = prior.get("direct_sum", {})
    if (not isinstance(pre, dict) or pre.get("head") != EXPECTED_HEAD
            or not isinstance(eta, dict) or not isinstance(direct, dict)
            or eta.get("derived_rule_proof_step") is not True
            or eta.get("prior_proof_search_executed") is not False
            or eta.get("prior_status") != "ADOPTED_DATABASE_PRIOR"
            or direct.get("inferred_zero_steps") != 2
            or direct.get("prior_proof_search_executed") is not False):
        raise RuntimeError("R4R5R3_PRIOR_EVIDENCE_INVALID")
    return {
        "prior_head": pre["head"], "isolated_eta7_verified": True,
        "isolated_direct_sum_inferences": 2,
        "prior_report_is_not_public_proof": True,
    }


def reviewed_head_lineage(root: Path) -> dict[str, object]:
    """Accept the reviewed HEAD or descendants changing only the R4R5R2 package.

    The source is still independently guarded by its committed Git blob, and
    the prior inference rule by its byte-level SHA256. Other committed changes
    must receive a separate source review; no arbitrary later HEAD is trusted.
    """
    import subprocess

    current = installer.git_blob(root, "HEAD")
    if current == EXPECTED_HEAD:
        return {"current_head": current, "intervening_paths": []}
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EXPECTED_HEAD, current],
        cwd=root, text=True, capture_output=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("R4R5R3_UNREVIEWED_HEAD")
    changed = subprocess.run(
        ["git", "diff", "--name-only", EXPECTED_HEAD, current],
        cwd=root, text=True, capture_output=True, check=True,
    ).stdout.splitlines()
    paths = sorted(set(name.strip() for name in changed if name.strip()))
    prefix = PRIOR_PACKAGE + "/"
    if any(not name.startswith(prefix) or name == prefix for name in paths):
        raise RuntimeError("R4R5R3_UNREVIEWED_HEAD_CHANGES")
    return {"current_head": current, "intervening_paths": paths}


def source_guard(root: Path) -> dict[str, object]:
    lineage = reviewed_head_lineage(root)
    path = root / PRIOR_PACKAGE / "rule.py"
    if not path.is_file():
        raise RuntimeError("R4R5R3_R4R5R2_RULE_MISSING")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != PRIOR_RULE_SHA256:
        raise RuntimeError("R4R5R3_R4R5R2_RULE_DRIFT")
    return {
        "reviewed_head": str(lineage["current_head"]),
        "reviewed_base_head": EXPECTED_HEAD,
        "reviewed_intervening_paths": list(lineage["intervening_paths"]),
        "production_blob": installer.PINNED_GIT_BLOB,
        "isolated_rule_sha256": actual,
    }

def public_order_zero_evidence() -> dict[str, object]:
    """Verify real accepted DB-prior parent ProofSteps without prior search.

    This checks the public provider's source-first proposals against R4R5R2's
    exact two source groups and checks ordinary inference replay separately.
    It does not claim that pi_9^5 has a completed root proof tree.
    """
    from expression import Multiple, Zero
    from homotopy_groups import DirectSumGroup
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase175_r4r5_eta7_annihilator_isolated.rule import RULE_NAME
    from phase175_r4r5r3_public_order_zero.provider import build_public_order_zero_provider
    from proof import (
        ProofRule, Relation, apply_inference_match, find_inference_matches_for_rule,
    )

    root = exact_prior_database_result(5, 4)
    eta = exact_prior_database_result(7, 1)
    direct = exact_prior_database_result(4, 4)
    if (not isinstance(root, Relation) or not isinstance(eta, Relation)
            or not isinstance(direct, Relation)
            or not isinstance(direct.rhs, DirectSumGroup)
            or len(direct.rhs.summands) != 2):
        raise RuntimeError("R4R5R3_SOURCE_ROWS_NOT_TYPED")
    bridge = object()
    expand = build_public_order_zero_provider(bridge=bridge, proof_target=root)
    counted = []
    sources = [eta] + [direct] * len(direct.rhs.summands)
    components = [eta.rhs] + list(direct.rhs.summands)
    for source, item in zip(sources, components):
        target = Relation(Multiple(item.order, item.generator), Zero())
        found = expand(target)
        if len(found) != 1 or found[0].subgoals != (source,) or found[0].rule.name != RULE_NAME:
            raise RuntimeError("R4R5R3_SHARED_SOURCE_FIRST_PROPOSAL_INVALID")
        admitted = admitted_db_step(source, proof_target=root)
        if admitted is None or not verified_db_step(admitted, proof_target=root):
            raise RuntimeError("R4R5R3_PARENT_DB_PRIOR_NOT_AUTHENTICATED")
        matches = find_inference_matches_for_rule(found[0].rule, (admitted,))
        if len(matches) != 1:
            raise RuntimeError("R4R5R3_INFERENCE_MATCH_FAILED")
        step = apply_inference_match(matches[0])
        if (step.rule is not ProofRule.INFERENCE
                or step.conclusion != target
                or step.premises != (admitted,)):
            raise RuntimeError("R4R5R3_INFERENCE_REPLAY_FAILED")
        counted.append(repr(target))
    return {
        "public_provider_proposals_with_verified_parent": len(counted),
        "source_groups": ["pi_8^7", "pi_8^4", "pi_8^4"],
        "conclusions": counted, "new_given": 0,
        "previous_proof_search_executed": False,
        "target_pi95_completed": False,
    }


def run(root: Path, *, dry_run: bool, prior_file: Path | None) -> int:
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / "phase175_r4r5r3_public_order_zero" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    record: dict[str, object] = {
        "phase": "175-R4R5R3", "dry_run": dry_run,
        "new_given": 0, "new_mathematical_rules": 0,
        "connected_previously_isolated_general_rules": 1,
        "public_pi95_complete": False, "full_pytest_executed": False,
        "gate": "FAIL_R4R5R3_SOURCE_FIRST_PUBLIC_PROVIDER",
    }
    try:
        prior_path = latest_prior(prior_file)
        record["prior_report"] = str(prior_path)
        record["prior"] = validate_prior(json.loads(prior_path.read_text(encoding="utf-8")))
        record["source_guard"] = source_guard(root)
        # Check git clean before mutating. Untracked isolated packages are allowed.
        import subprocess
        changed = subprocess.run(
            ["git", "diff", "--name-only"], cwd=root, text=True,
            capture_output=True, check=True,
        ).stdout.strip().splitlines()
        changed += subprocess.run(
            ["git", "diff", "--cached", "--name-only"], cwd=root, text=True,
            capture_output=True, check=True,
        ).stdout.strip().splitlines()
        if any(name.strip() for name in changed):
            raise RuntimeError("R4R5R3_UNREVIEWED_TRACKED_CHANGES")
        record["install"] = installer.install(root, dry_run=dry_run, output=folder)
        if not dry_run:
            record["general_rule"] = public_order_zero_evidence()
            result = subprocess.run(
                [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                 "--import-mode=importlib",
                 "phase175_r4r5r3_public_order_zero/tests/test_real_integration.py"],
                cwd=root, text=True, capture_output=True,
            )
            record["real_integration_pytest"] = {
                "exit_code": result.returncode,
                "stdout": result.stdout[-4000:],
                "stderr": result.stderr[-2000:],
            }
            if result.returncode != 0:
                raise RuntimeError("R4R5R3_REAL_INTEGRATION_PYTEST_FAILED")
        record["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as error:
        record["error"] = f"{type(error).__name__}: {error}"
        record["traceback"] = traceback.format_exc()[-6000:]
    (folder / "report.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (folder / "report.md").write_text(
        "# Phase 175 R4R5R3 — 一般零関係の共有探索接続\n\n"
        + "Gate: `" + str(record["gate"]) + "`\n\n"
        + "先行 DB 結果を再証明せず、既存の一般規則を共有 Provider に接続。\n"
        + "Proposition 2.5 と (5.8) は本段階の対象外。\n"
        + "π₉⁵ の完成証明は依然として未完成。\n",
        encoding="utf-8",
    )
    print("PHASE175_R4R5R3_HEAD=" + str(record.get("source_guard", {}).get("reviewed_head", "UNKNOWN")))
    print("PHASE175_R4R5R3_NEW_GIVEN=0")
    print("PHASE175_R4R5R3_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4R5R3_SHARED_RULE_CONNECTED=" + str(not dry_run and "error" not in record))
    print("PHASE175_R4R5R3_VERIFIED_PUBLIC_PROVIDER_EXAMPLES=" + str(record.get("general_rule", {}).get("public_provider_proposals_with_verified_parent", 0)))
    print("PHASE175_R4R5R3_PRIOR_PROOF_SEARCH_EXECUTED=False")
    print("PHASE175_R4R5R3_REAL_INTEGRATION_PYTEST=" + (
        "NOT_RUN" if dry_run else "PASS" if "error" not in record else "FAIL"
    ))
    print("PHASE175_R4R5R3_PI95_PROOF=NOT_COMPLETE")
    print("PHASE175_R4R5R3_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R5R3_FULL_FUNCTION=" + str(folder / "shared_expansion_provider_FULL.py"))
    print("PHASE175_R4R5R3_REPORT=" + str(folder / "report.json"))
    print("PHASE175_R4R5R3_GATE=" + str(record["gate"]))
    if "error" in record:
        print("PHASE175_R4R5R3_ERROR=" + str(record["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r5r2-report", type=Path)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_file=args.r4r5r2_report)


if __name__ == "__main__":
    sys.exit(main())
