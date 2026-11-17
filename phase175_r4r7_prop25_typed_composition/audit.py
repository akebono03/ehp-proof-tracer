"""Phase 175 R4R7: isolated and source-guarded conditional Prop 2.5 rule audit."""
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

PACKAGE = "phase175_r4r7_prop25_typed_composition"
PRIOR_PACKAGE = "phase175_r4r6_prop25_eq58_source_frontier"
PRIOR_GATE = "PASS_R4R6_PROP25_EQ58_SOURCE_FRONTIER_RECORDED_NOT_PUBLIC"
DRY_GATE = "PASS_R4R7_PROP25_TYPED_INFERENCE_DRYRUN"
FINAL_GATE = "PASS_R4R7_PROP25_TYPED_INFERENCE_ISOLATED_NOT_PUBLIC"
REVIEWED_HEAD = "c48fdc307ba67a5e21b0ef49d57953468f7b47e2"
REVIEWED_R4R6_HEAD = "11968d23724cee147520b5fa3fd5a6e89989003e"
REVIEWED_R4R6_PATHS = (
    "phase175_r4r6_prop25_eq58_source_frontier/AUDIT_PLAN_JA.md",
    "phase175_r4r6_prop25_eq58_source_frontier/CODE_FULL_JA.md",
    "phase175_r4r6_prop25_eq58_source_frontier/README.md",
    "phase175_r4r6_prop25_eq58_source_frontier/TEST_RESULTS_JA.md",
    "phase175_r4r6_prop25_eq58_source_frontier/__init__.py",
    "phase175_r4r6_prop25_eq58_source_frontier/audit.py",
    "phase175_r4r6_prop25_eq58_source_frontier/run.ps1",
    "phase175_r4r6_prop25_eq58_source_frontier/tests/test_audit.py",
)
PRIOR_HISTORICAL_HEAD = "bc1a9eff9c1d051764ff817bb1948f55a1479961"
PRIOR_AUDIT_SHA256 = "cedcfc994d4ccf6989bc9025a82741e51105708da0d1305fb3282e5ae41f9b7d"
PINNED_GIT_BLOBS = {
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
    "sources/toda/Toda_02_2.tex": "ed3667788805a429140dedf5d183736e43e0f2c3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r52_r9_shared_math.py": "df4e0f834e9bc321f338ec10b363c79d82623457",
    "phase175_r4r5r3_public_order_zero/provider.py": "9a736418a2f191cfe485e3777c8bbb2143f2a9f3",
}


def git(root: Path, *parts: str) -> str:
    result = subprocess.run(
        ["git", *parts], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R4R7_GIT_ERROR: " + " ".join(parts) + " " + result.stderr.strip())
    return result.stdout.strip()


def reviewed_head_lineage(root: Path, head: str) -> list[str]:
    """Accept only the reviewed R4R6 successor with its exact committed paths.

    The original R4R7 baseline is also supported. Any unrelated or later
    commit is rejected; individual source blobs and R4R6 audit bytes are
    independently checked in preflight().
    """
    if head == REVIEWED_HEAD:
        return []
    if head != REVIEWED_R4R6_HEAD:
        raise RuntimeError("R4R7_UNREVIEWED_HEAD: " + head)
    git(root, "merge-base", "--is-ancestor", REVIEWED_HEAD, head)
    changed = sorted(set(git(root, "diff", "--name-only", REVIEWED_HEAD, head).splitlines()))
    if changed != sorted(REVIEWED_R4R6_PATHS):
        raise RuntimeError("R4R7_UNREVIEWED_R4R6_LINEAGE: " + repr(changed))
    return changed


def preflight(root: Path) -> dict[str, object]:
    """Guard the reviewed Git lineage, source blobs and inherited R4R6 code."""
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R4R7_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R4R7_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")
    reviewed_changes = reviewed_head_lineage(root, head)
    tracked = sorted(set(
        git(root, "diff", "--name-only").splitlines()
        + git(root, "diff", "--cached", "--name-only").splitlines()
    ))
    if [path for path in tracked if path != ".pytest_cache/v/cache/nodeids"]:
        raise RuntimeError("R4R7_UNREVIEWED_TRACKED_CHANGES: " + repr(tracked))
    for path, expected in PINNED_GIT_BLOBS.items():
        if not (root / path).is_file():
            raise RuntimeError("R4R7_SOURCE_FILE_MISSING: " + path)
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("R4R7_SOURCE_BLOB_DRIFT: " + path)
    prior_audit = root / PRIOR_PACKAGE / "audit.py"
    if (not prior_audit.is_file()
            or hashlib.sha256(prior_audit.read_bytes()).hexdigest() != PRIOR_AUDIT_SHA256):
        raise RuntimeError("R4R7_REVIEWED_R4R6_AUDIT_DRIFT")
    return {
        "head": head,
        "reviewed_r4r7_base_head": REVIEWED_HEAD,
        "reviewed_r4r6_successor_head": REVIEWED_R4R6_HEAD,
        "reviewed_intervening_paths": reviewed_changes,
        "pinned_blobs": len(PINNED_GIT_BLOBS),
        "prior_audit_sha256": PRIOR_AUDIT_SHA256,
        "tracked_changed": tracked,
    }


def validate_prior(data: object) -> dict[str, object]:
    """Only an actual completed R4R6 audit, not a mathematical proof."""
    if not isinstance(data, dict):
        raise RuntimeError("R4R7_R4R6_REPORT_INVALID")
    expected = {
        "phase": "175-R4R6",
        "mode": "READ_ONLY_SOURCE_TYPE_BOUNDARY_AUDIT",
        "gate": PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
    }
    if any(data.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R7_R4R6_SCOPE_OR_GATE_INVALID")
    pre = data.get("preflight")
    history = data.get("prior_history")
    printed = data.get("source_evidence")
    typed = data.get("typed_frontier")
    boundary = data.get("order_and_implementation_boundary")
    if (not isinstance(pre, dict) or pre.get("head") != REVIEWED_HEAD
            or not isinstance(history, dict)
            or history.get("historical_reviewed_head") != PRIOR_HISTORICAL_HEAD
            or history.get("historical_production_blob_checked") is not True
            or history.get("historical_rule_sha256_checked") is not True
            or not isinstance(printed, dict)
            or printed.get("proposition_2_5_inclusion_and_conditions") is not True
            or printed.get("equation_5_8_signed_identity") is not True
            or printed.get("source_sign_preserved") != "±"
            or printed.get("printed_relation_is_a_verified_proof_step") is not False
            or not isinstance(typed, dict)
            or (typed.get("m"), typed.get("i"), typed.get("j")) != (4, 8, 9)
            or typed.get("j_less_than_3m_minus_1") is not True
            or typed.get("typed_endpoints_are_verified_proof_steps") is not False
            or not isinstance(boundary, dict)
            or boundary.get("new_prop25_provider_connected") is not False
            or boundary.get("signed_reduction_executed_as_proof_step") is not False
            or boundary.get("prior_proof_search_executed") is not False):
        raise RuntimeError("R4R7_R4R6_EVIDENCE_INVALID")
    return {
        "r4r6_head": pre["head"],
        "r4r5r3_historical_head": history["historical_reviewed_head"],
        "printed_source_is_not_proof": True,
        "r4r6_public_proof_completed": False,
    }


def latest_real_prior(explicit: Path | None = None) -> Path:
    if explicit is not None:
        candidate = explicit.expanduser().resolve()
        if not candidate.is_file():
            raise RuntimeError("R4R7_R4R6_REPORT_MISSING: " + str(candidate))
        return candidate
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    rejected: list[str] = []
    for path in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            validate_prior(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError, UnicodeError, RuntimeError) as error:
            rejected.append(path.name + ": " + str(error))
            continue
        return path
    raise RuntimeError(
        "R4R7_SUCCESSFUL_R4R6_REPORT_NOT_FOUND: " + str(folder)
        + " rejected=" + repr(rejected[:5])
    )


def check_source_and_boundaries(root: Path) -> dict[str, object]:
    """Revalidate Toda wording and verify public provider wasn't wired to R4R7."""
    from phase175_r4r6_prop25_eq58_source_frontier import audit as prior_audit

    printed = prior_audit.source_evidence(
        (root / "sources/toda/Toda_02_2.tex").read_text(encoding="utf-8"),
        (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8"),
    )
    if (printed["printed_relation_is_a_verified_proof_step"] is not False
            or printed["source_sign_preserved"] != "±"):
        raise RuntimeError("R4R7_PRINTED_SOURCE_PROMOTED_TO_PROOF")
    typed = prior_audit.typed_frontier()
    if (typed["m"], typed["i"], typed["j"]) != (4, 8, 9):
        raise RuntimeError("R4R7_SPECIALIZATION_CHANGED")
    shared = (root / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8")
    if ("phase175_r4r7_prop25_typed_composition" in shared
            or "expand_prop25_signed_composition" in shared):
        raise RuntimeError("R4R7_PREMATURE_PUBLIC_CONNECTION")
    return {
        "source_rechecked": True,
        "m_i_j": [4, 8, 9],
        "numeric_equality_condition": True,
        "sign_retained": True,
        "primary_branch_not_assumed": True,
        "public_search_unchanged": True,
        "source_is_proof": False,
    }


def audit_isolated_rule() -> dict[str, object]:
    """Create a typed backward obligation only; not a verified parent step."""
    from expression import Composition, HomotopyElement, IteratedSuspension, Multiple, Sum
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from proof import Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement
    from phase175_r4r7_prop25_typed_composition.rule import expand_prop25_signed_composition

    alpha = HomotopyElement("iota", 9, source=9, target=9)
    beta = HomotopyElement("eta", 7, source=8, target=7)
    gamma = HomotopyElement("eta", 9, source=10, target=9)
    nu = HomotopyElement("nu", 4, source=7, target=4)
    other = HomotopyElement("E_nu_prime", 4, source=7, target=4)
    representative = Sum(Multiple(2, nu), Multiple(-1, other))
    signed = TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(9, 9), TodaPrimaryGroup(7, 4)),
        alpha, representative,
    )
    identity = Relation(Composition(alpha, IteratedSuspension(beta, 2)),
                        gamma, RelationType.EQUALITY)
    goal = TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4)),
        gamma, Composition(representative, beta),
    )
    results = expand_prop25_signed_composition(goal, signed, identity)
    if (len(results) != 1 or results[0].subgoals != (signed, identity)
            or results[0].rule.conclusion_pattern != goal):
        raise RuntimeError("R4R7_ISOLATED_TYPED_GOAL_INVALID")
    return {
        "isolated_backward_proposals": 1,
        "unproved_parent_obligations": 2,
        "signed_goal_retained": True,
        "verified_parent_proof_steps_created": 0,
        "previous_proof_search_executed": False,
        "public_provider_connected": False,
        "pi95_completed": False,
    }


def report_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def run(root: Path, *, dry_run: bool, prior_path: Path | None) -> int:
    output = report_folder()
    result: dict[str, object] = {
        "phase": "175-R4R7", "mode": "ISOLATED_TYPED_CONDITIONAL_INFERENCE",
        "dry_run": dry_run,
        "new_given": 0, "new_mathematical_rules": 1,
        "production_changes": [], "rule_connected_to_public": False,
        "pi95_proof_complete": False, "full_pytest_executed": False,
        "gate": "FAIL_R4R7_PROP25_TYPED_INFERENCE",
    }
    try:
        result["preflight"] = preflight(root)
        path = latest_real_prior(prior_path)
        result["prior_report"] = str(path)
        result["prior"] = validate_prior(json.loads(path.read_text(encoding="utf-8")))
        result["source_and_boundary"] = check_source_and_boundaries(root)
        result["isolated"] = audit_isolated_rule()
        result["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as error:
        result["error"] = type(error).__name__ + ": " + str(error)
        result["traceback"] = traceback.format_exc()[-6000:]
    (output / "report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (output / "report.md").write_text(
        "# Phase 175 R4R7 — Toda Proposition 2.5 型付き一般推論\n\n"
        + "Gate: `" + str(result["gate"]) + "`\n\n"
        + "一般規則は独立した証明済み前提2件を必要とする。\n"
        + "符号 ± は保存し、m が奇数または j<3m−1 の場合だけ扱う。\n"
        + "2-primary の条件を無証明で仮定しない。\n"
        + "公開 Proof Search は未接続。π₉⁵ の証明は未完成。\n",
        encoding="utf-8",
    )
    print("PHASE175_R4R7_HEAD=" + str(result.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R7_NEW_GIVEN=0")
    print("PHASE175_R4R7_NEW_MATHEMATICAL_RULES=1")
    print("PHASE175_R4R7_PRODUCTION_CHANGES=0")
    print("PHASE175_R4R7_PUBLIC_RULE=NOT_CONNECTED")
    print("PHASE175_R4R7_PI95=NOT_COMPLETE")
    print("PHASE175_R4R7_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R7_REPORT=" + str(output / "report.json"))
    print("PHASE175_R4R7_GATE=" + str(result["gate"]))
    if "error" in result:
        print("PHASE175_R4R7_ERROR=" + str(result["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r6-report", type=Path, default=None)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_path=args.r4r6_report)


if __name__ == "__main__":
    sys.exit(main())
