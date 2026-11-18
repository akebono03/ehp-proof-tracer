"""R4R12: source-first public candidate for the already-existing EHP quotient.

No new rule, GIVEN, PDF claim, proof certificate or saved root proof is created.
An expansion is an UNPROVED obligation until normal search discharges it.
"""
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

from phase175_r4r12_public_two_summand_quotient import installer
from phase175_r4r11_signed_eta_torsion_public.audit import reviewed_eol_blob_matches

PACKAGE = "phase175_r4r12_public_two_summand_quotient"
PRIOR_PACKAGE = "phase175_r4r11_signed_eta_torsion_public"
PRIOR_GATE = "PASS_R4R11_SIGNED_ETA_TORSION_SHARED_CONNECTED_PI95_PENDING"
DRY_GATE = "PASS_R4R12_TWO_SUMMAND_QUOTIENT_DRYRUN"
FINAL_GATE = "PASS_R4R12_TWO_SUMMAND_QUOTIENT_ROOT_CANDIDATE_PI95_PENDING"
HEAD = installer.HEAD
PINNED_COMMITTED = {
    "phase175_r4r3_two_summand_quotient/rule.py": "0fdb4c5efa1f2e66470a0735f58f781aafe18d44",
    "phase165_r12_r2_quotient_rules.py": "2b3e8e0449382e9245ee22f08501e9cede0a5b59",
    "phase165_r12_r24_web_search_connection.py": "71d0c6c365a46e833a2bfe304c771d2e010178ca",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
}
PINNED_PRIOR_UNTRACKED = {
    "phase175_r4r11_signed_eta_torsion_public/rule.py": "613bcd5049be0ac431c556dfc413c410287e8bf0",
    "phase175_r4r11_signed_eta_torsion_public/provider.py": "a30d0a28ae7cb174d22ff0ac11b611413e8e596b",
    "phase175_r4r11_signed_eta_torsion_public/installer.py": "b113829a0871d788bd41f4c3271d3d3287d394ff",
    "phase175_r4r11_signed_eta_torsion_public/audit.py": "331833f0ea3b3b4474f759b5713b994315f9a5a3",
}


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, check=False, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    if process.returncode:
        raise RuntimeError("R4R12_GIT_FAILED: " + " ".join(args)
                           + " " + process.stderr.strip())
    return process.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R4R12_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R4R12_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")
    if head != HEAD:
        raise RuntimeError("R4R12_UNREVIEWED_HEAD: " + head)
    changed = sorted(set(
        git(root, "diff", "--name-only").splitlines()
        + git(root, "diff", "--cached", "--name-only").splitlines()
    ))
    if any(path not in (installer.TARGET.as_posix(), ".pytest_cache/v/cache/nodeids")
           for path in changed):
        raise RuntimeError("R4R12_UNREVIEWED_TRACKED_FILE: " + repr(changed))
    for path, sha in PINNED_COMMITTED.items():
        if git(root, "rev-parse", "HEAD:" + path) != sha:
            raise RuntimeError("R4R12_COMMITTED_SOURCE_DRIFT: " + path)
        file = root / path
        if not file.is_file() or not reviewed_eol_blob_matches(file.read_bytes(), sha):
            raise RuntimeError("R4R12_WORKING_SOURCE_DRIFT: " + path)
    for path, sha in PINNED_PRIOR_UNTRACKED.items():
        file = root / path
        if not file.is_file() or not reviewed_eol_blob_matches(file.read_bytes(), sha):
            raise RuntimeError("R4R12_PREVIOUS_MODULE_DRIFT: " + path)
    target, before, after, _ = installer.plan(root)
    if target != root / installer.TARGET:
        raise RuntimeError("R4R12_UNREVIEWED_INSTALL_TARGET")
    return {
        "head": head,
        "changed_tracked": changed,
        "pinned_committed_modules": len(PINNED_COMMITTED),
        "pinned_prior_modules": len(PINNED_PRIOR_UNTRACKED),
        "patch_required": before != after,
        "expected_after_blob": installer.git_blob_sha(after.replace(b"\r\n", b"\n")),
    }


def validate_prior(report: object) -> dict[str, object]:
    if not isinstance(report, dict):
        raise RuntimeError("R4R12_PRIOR_REPORT_NOT_OBJECT")
    expected = {
        "phase": "175-R4R11",
        "dry_run": False,
        "gate": PRIOR_GATE,
        "new_given": 0,
        "new_mathematical_rules": 1,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    if any(report.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R12_PRIOR_GATE_OR_SCOPE_INVALID")
    before = report.get("preflight")
    public = report.get("public")
    install = report.get("install")
    if (
        not isinstance(before, dict) or before.get("head") != "abf619040d52aa9fd61c5bca60db81e28912e24d"
        or not isinstance(public, dict)
        or not all(public.get(x) is True for x in (
            "r4r10_signed_delta_route_present",
            "r4r11_exact_delta_route_present",
            "prior_eta7_order_two_route_present",
            "exact_database_generator_identity_reused",
            "three_proof_obligations_preserved",
        ))
        or public.get("group_conclusion_completed") is not False
        or not isinstance(install, dict)
        or install.get("production_path") != installer.TARGET.as_posix()
        or install.get("full_function_exported") is not True
    ):
        raise RuntimeError("R4R12_PRIOR_EVIDENCE_NOT_AUTHENTIC")
    return {"r4r11_success_verified": True, "prior_head": before["head"]}


def find_prior(path: Path | None) -> Path:
    if path is not None:
        result = path.expanduser().resolve()
        if not result.is_file():
            raise RuntimeError("R4R12_PRIOR_REPORT_MISSING: " + str(result))
        return result
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    for candidate in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            validate_prior(json.loads(candidate.read_text(encoding="utf-8")))
            return candidate
        except (OSError, ValueError, TypeError, UnicodeError, RuntimeError):
            continue
    raise RuntimeError("R4R12_SUCCESSFUL_R4R11_REPORT_NOT_FOUND: " + str(folder))


def inspect_public_root() -> dict[str, object]:
    """Confirm real typed candidate paths; never replay the six actual proofs."""
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase175_r4r3_two_summand_quotient.rule import RULE_NAME, two_summand_quotient_inputs
    from phase175_r4r12_public_two_summand_quotient.provider import (
        ordered_summand_inputs, expand_public_two_summand_quotient,
    )
    from proof import ProofStep, Relation, RelationType

    root = exact_prior_database_result(5, 4)
    if (not isinstance(root, Relation)
            or root.relation_type is not RelationType.EQUALITY
            or root.lhs != TodaPrimaryGroup(9, 5)
            or not isinstance(root.rhs, FiniteCyclicGroup)
            or root.rhs.order != 2):
        raise RuntimeError("R4R12_UNEXPECTED_PI95_ROOT_GOAL")
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    sources = ordered_summand_inputs(goal, proof_target=root)
    if sources is None:
        raise RuntimeError("R4R12_ORDERED_EARLIER_DB_CANDIDATES_MISSING")
    middle, source = sources
    for relation in (middle, source):
        admitted = admitted_db_step(relation, proof_target=root)
        if admitted is None or not verified_db_step(admitted, proof_target=root):
            raise RuntimeError("R4R12_INAUTHENTIC_DB_PRIOR")
    initial = expand_public_two_summand_quotient(goal, proof_target=root)
    if not initial:
        raise RuntimeError("R4R12_ISOLATED_ROOT_QUOTIENT_PROPOSAL_MISSING")
    bridge = build_shared_typed_bridge()
    public = shared_expansion_provider(bridge, proof_target=root)
    found = tuple(exp for exp in public(goal) if exp.rule.name == RULE_NAME)
    if not found or any(exp not in initial for exp in found):
        raise RuntimeError("R4R12_PUBLIC_ROOT_QUOTIENT_PROPOSAL_MISSING")
    for exp in found:
        values = exp.subgoals
        if (len(values) != 6 or any(isinstance(item, ProofStep) for item in values)
                or values[0] != middle or values[1] != source
                or two_summand_quotient_inputs(goal, middle, source,
                                               values[2], values[5]) != values):
            raise RuntimeError("R4R12_UNVERIFIED_OR_MALFORMED_SUBGOALS")
    return {
        "target_group": "pi_9^5",
        "earlier_db_candidates": 2,
        "isolated_root_candidates": len(initial),
        "public_root_candidates": len(found),
        "each_candidate_proof_obligations": 6,
        "existing_r4r3_rule_reused": True,
        "new_given": 0,
        "root_group_completed": False,
        "actual_proof_search_executed": False,
    }


def report_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    result = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    result.mkdir(parents=True, exist_ok=False)
    return result


def run(root: Path, *, dry_run: bool, prior_report: Path | None) -> int:
    folder = report_folder()
    report = {
        "phase": "175-R4R12",
        "dry_run": dry_run,
        "gate": "FAIL_R4R12_TWO_SUMMAND_QUOTIENT",
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [installer.TARGET.as_posix()],
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    try:
        report["preflight"] = preflight(root)
        chosen = find_prior(prior_report)
        report["prior_report"] = str(chosen)
        report["prior"] = validate_prior(json.loads(chosen.read_text(encoding="utf-8")))
        report["install"] = installer.install(root, dry_run=dry_run, output=folder)
        report["public"] = None if dry_run else inspect_public_root()
        report["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (folder / "report.md").write_text(
        "# Phase 175 R4R12 — 既存一般商群規則の公開接続\n\n"
        + "Gate: `" + str(report["gate"]) + "`\n\n"
        + "R4R3 の数学規則を再利用。未解決の6前提は真とみなさない。\n"
        + "π₉⁵ の完成証明は宣言しない。\n", encoding="utf-8",
    )
    print("PHASE175_R4R12_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R12_NEW_GIVEN=0")
    print("PHASE175_R4R12_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4R12_ROOT_PROVIDER=" + (
        "CONNECTED" if isinstance(report.get("public"), dict)
        and report["public"].get("public_root_candidates", 0) > 0 else "NOT_CHECKED"
    ))
    print("PHASE175_R4R12_PI95=NOT_COMPLETE")
    print("PHASE175_R4R12_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R12_REPORT=" + str(folder / "report.json"))
    print("PHASE175_R4R12_GATE=" + str(report["gate"]))
    if "error" in report:
        print("PHASE175_R4R12_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r11-report", type=Path, default=None)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_report=args.r4r11_report)


if __name__ == "__main__":
    sys.exit(main())
