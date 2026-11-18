"""Phase 175 R4R6: read-only Prop 2.5 / (5.8) source and type frontier.

An audited source sentence, a typed endpoint, and a verified ProofStep are
intentionally separate. This module installs no inference rule and creates
no completed proof for pi_9^5.
"""
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


PACKAGE = "phase175_r4r6_prop25_eq58_source_frontier"
PRIOR_PACKAGE = "phase175_r4r5r3_public_order_zero"
PRIOR_GATE = "PASS_R4R5R3_SHARED_PROVIDER_CONNECTED_NOT_COMPLETE"
# These describe the *historical R4R5R3 source guard*, not the later R4R6 HEAD.
PRIOR_REVIEWED_BASE_HEAD = "2789fb6297efaa35962695b95300063feb6e2ea2"
PRIOR_CHANGED_PREFIX = "phase175_r4r5_eta7_annihilator_isolated/"
PRIOR_PRODUCTION_BLOB = "ee1efa2d91df479168b7b964d24e814e0f516449"
PRIOR_RULE_SHA256 = "228a856bb4aa535edf4243885dee8472b8789c7d85c3507fc5eb1aace8a42bcd"
DRY_GATE = "PASS_R4R6_PROP25_EQ58_SOURCE_DRYRUN"
FINAL_GATE = "PASS_R4R6_PROP25_EQ58_SOURCE_FRONTIER_RECORDED_NOT_PUBLIC"
REVIEWED_HEADS = (
    "8d8c1eaaeffed2bc798c2ed19c8fe97c8e2ca5fc",
    "c48fdc307ba67a5e21b0ef49d57953468f7b47e2",
)
PINNED_BLOBS = {
    "sources/toda/Toda_02_2.tex": "ed3667788805a429140dedf5d183736e43e0f2c3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r52_r9_shared_math.py": "df4e0f834e9bc321f338ec10b363c79d82623457",
    "phase175_r4r4_pi95_premise_frontier/audit.py": "0a9fbbd1c3262dfc46ec8f6e8a819eb5876742fc",
    "phase175_r4r5r3_public_order_zero/provider.py": "9a736418a2f191cfe485e3777c8bbb2143f2a9f3",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
}


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode != 0:
        raise RuntimeError("R4R6_GIT_FAILED: " + " ".join(args) + ": " + process.stderr.strip())
    return process.stdout.strip()


def validate_tracked_changes(paths: list[str]) -> list[str]:
    changed = sorted({item.strip() for item in paths if item.strip()})
    disallowed = [name for name in changed if name != ".pytest_cache/v/cache/nodeids"]
    if disallowed:
        raise RuntimeError("R4R6_UNREVIEWED_TRACKED_CHANGES: " + repr(disallowed))
    return changed


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R4R6_NOT_REPOSITORY_ROOT")
    branch = git(root, "branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R4R6_WRONG_BRANCH: " + branch)
    head = git(root, "rev-parse", "HEAD")
    if head not in REVIEWED_HEADS:
        raise RuntimeError("R4R6_UNREVIEWED_HEAD: " + head)
    dirty = validate_tracked_changes(
        git(root, "diff", "--name-only").splitlines()
        + git(root, "diff", "--cached", "--name-only").splitlines()
    )
    for path, expected in PINNED_BLOBS.items():
        if not (root / path).is_file():
            raise RuntimeError("R4R6_SOURCE_MISSING: " + path)
        observed = git(root, "rev-parse", "HEAD:" + path)
        if observed != expected:
            raise RuntimeError("R4R6_SOURCE_PIN_DRIFT: " + path)
    return {
        "head": head,
        "branch": branch,
        "reviewed_source_blobs": dict(PINNED_BLOBS),
        "allowed_tracked_dirty": dirty,
        "root_repository_matches": True,
    }


def find_real_prior(explicit: Path | None = None) -> Path:
    """Find a *validated* successful prior without hiding rejected reports.

    A failed or incompatible newer report does not mask an older valid one.
    An explicit report path is passed to run() for the same strict validation.
    """
    if explicit is not None:
        candidate = explicit.expanduser().resolve()
        if not candidate.is_file():
            raise RuntimeError("R4R6_PRIOR_REPORT_MISSING: " + str(candidate))
        return candidate

    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    candidates = sorted(folder.glob("*/report.json"), reverse=True)
    if not candidates:
        raise RuntimeError(
            "R4R6_SUCCESSFUL_R4R5R3_REAL_REPORT_MISSING: searched="
            + str(folder)
        )

    rejected: list[str] = []
    for candidate in candidates:
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
            validate_prior(data)
        except (OSError, ValueError, UnicodeError, RuntimeError) as exc:
            rejected.append(str(candidate) + " => " + type(exc).__name__ + ": " + str(exc))
            continue
        return candidate

    raise RuntimeError(
        "R4R6_PRIOR_REPORTS_FOUND_BUT_REJECTED: "
        + " | ".join(rejected[:5])
        + (" | additional_rejected=" + str(len(rejected) - 5)
           if len(rejected) > 5 else "")
    )


def validate_prior(data: object) -> dict[str, object]:
    """Validate the real R4R5R3 report against its historical producer.

    R4R5R3 ran *before* the public-provider change was committed, so its
    reviewed_head must not be compared to the later R4R6 checkout HEADs.
    The independent Git history and blob checks run in validate_prior_history.
    """
    if not isinstance(data, dict):
        raise RuntimeError("R4R6_PRIOR_INVALID")
    expected = {
        "phase": "175-R4R5R3",
        "gate": PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "connected_previously_isolated_general_rules": 1,
        "public_pi95_complete": False,
        "full_pytest_executed": False,
    }
    if any(data.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R6_PRIOR_GATE_OR_SCOPE_INVALID")

    source_guard = data.get("source_guard")
    general = data.get("general_rule")
    integration = data.get("real_integration_pytest")
    if not isinstance(source_guard, dict):
        raise RuntimeError("R4R6_PRIOR_EVIDENCE_INVALID: source_guard not a dict")
    reviewed_head = source_guard.get("reviewed_head")
    paths = source_guard.get("reviewed_intervening_paths")
    if (not isinstance(reviewed_head, str)
            or len(reviewed_head) != 40
            or reviewed_head == "0" * 40
            or any(c not in "0123456789abcdef" for c in reviewed_head)
            or source_guard.get("reviewed_base_head") != PRIOR_REVIEWED_BASE_HEAD
            or source_guard.get("production_blob") != PRIOR_PRODUCTION_BLOB
            or source_guard.get("isolated_rule_sha256") != PRIOR_RULE_SHA256
            or not isinstance(paths, list)
            or any(not isinstance(path, str)
                   or not path.startswith(PRIOR_CHANGED_PREFIX)
                   or ".." in path.split("/")
                   or path == PRIOR_CHANGED_PREFIX
                   for path in paths)
            or paths != sorted(set(paths))):
        raise RuntimeError("R4R6_PRIOR_EVIDENCE_INVALID: historical source guard")
    if (not isinstance(general, dict)
            or general.get("public_provider_proposals_with_verified_parent") != 3
            or general.get("source_groups") != ["pi_8^7", "pi_8^4", "pi_8^4"]
            or general.get("new_given") != 0
            or general.get("previous_proof_search_executed") is not False
            or general.get("target_pi95_completed") is not False
            or not isinstance(integration, dict)
            or integration.get("exit_code") != 0):
        raise RuntimeError("R4R6_PRIOR_EVIDENCE_INVALID: proof/provider replay boundary")
    return {
        "r4r5r3_head": reviewed_head,
        "r4r5r3_base_head": PRIOR_REVIEWED_BASE_HEAD,
        "verified_provider_examples": 3,
        "earlier_proof_search_rerun": False,
        "prior_report_is_not_mathematical_proof": True,
    }


def validate_prior_history(root: Path, source_guard: dict[str, object]) -> dict[str, object]:
    """Revalidate the exact earlier Git range recorded by R4R5R3.

    This cannot be replaced by a check against the present R4R6 HEAD:
    its full provider-wiring commit was created *after* the prior report.
    """
    reviewed_head = str(source_guard["reviewed_head"])
    current_head = git(root, "rev-parse", "HEAD")
    for ancestor, descendant in (
        (PRIOR_REVIEWED_BASE_HEAD, reviewed_head),
        (reviewed_head, current_head),
    ):
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=root, capture_output=True, text=True, check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "R4R6_PRIOR_HISTORY_INVALID: unreviewed ancestor "
                + ancestor + " -> " + descendant
            )
    actual_changed_paths = sorted(set(git(
        root, "diff", "--name-only", PRIOR_REVIEWED_BASE_HEAD, reviewed_head,
    ).splitlines()))
    recorded_changed_paths = source_guard["reviewed_intervening_paths"]
    if actual_changed_paths != recorded_changed_paths:
        raise RuntimeError("R4R6_PRIOR_HISTORY_INVALID: changed paths differ")
    if any(not path.startswith(PRIOR_CHANGED_PREFIX)
           for path in actual_changed_paths):
        raise RuntimeError("R4R6_PRIOR_HISTORY_INVALID: unexpected changed file")
    if git(root, "rev-parse", reviewed_head + ":phase165_r52_r9_shared_math.py") != PRIOR_PRODUCTION_BLOB:
        raise RuntimeError("R4R6_PRIOR_HISTORY_INVALID: prior production blob drift")
    rule_path = root / PRIOR_CHANGED_PREFIX / "rule.py"
    if not rule_path.is_file() or hashlib.sha256(rule_path.read_bytes()).hexdigest() != PRIOR_RULE_SHA256:
        raise RuntimeError("R4R6_PRIOR_HISTORY_INVALID: isolated inference rule drift")
    return {
        "historical_reviewed_head": reviewed_head,
        "historical_reviewed_base_head": PRIOR_REVIEWED_BASE_HEAD,
        "current_head": current_head,
        "changed_paths": actual_changed_paths,
        "historical_production_blob_checked": True,
        "historical_rule_sha256_checked": True,
    }


def section(source: str, opening: str, closing: str) -> str:
    start = source.find(opening)
    if start < 0 or source.find(opening, start + len(opening)) >= 0:
        raise RuntimeError("R4R6_SOURCE_SECTION_NOT_UNIQUE: " + opening)
    end = source.find(closing, start + len(opening))
    if end < 0:
        raise RuntimeError("R4R6_SOURCE_SECTION_UNTERMINATED: " + opening)
    return source[start:end + len(closing)]


def source_evidence(chapter_2: str, chapter_5: str) -> dict[str, object]:
    prop25 = section(chapter_2, r"\begin{proposition}\label{prop:2.5}", r"\end{proposition}")
    equation58 = section(chapter_5, r"\begin{equation}\label{eq:5.8}", r"\end{equation}")
    proposition58 = section(chapter_5, r"\begin{proposition}\label{prop:5.8}", r"\end{proposition}")
    proof_start = chapter_5.find(r"\begin{proposition}\label{prop:5.8}") + len(proposition58)
    proof_end = chapter_5.find(r"\begin{equation}\label{eq:5.9}", proof_start)
    if proof_end < proof_start or proof_end < 0:
        raise RuntimeError("R4R6_PROP58_PROOF_RANGE_MISSING")
    proof = chapter_5[proof_start:proof_end]
    required25 = (
        r"\alpha\in\pi_{i+1}(S^{2m+1})",
        r"\beta\in \pi_{j-1}(S^{i-1})",
        r"\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)",
        r"j<3m-1",
        r"2\)-primary",
        "等号",
    )
    if any(piece not in prop25 for piece in required25):
        raise RuntimeError("R4R6_PROP25_SOURCE_DRIFT")
    if r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" not in equation58:
        raise RuntimeError("R4R6_EQ58_SIGNED_FORMULA_DRIFT")
    required_proof = (
        r"\Delta(\eta_9)",
        r"\Delta(\iota_9)\circ \eta_7",
        r"\nu_4\circ (2\eta_7)",
        r"E\nu'\circ \eta_7",
    )
    if any(piece not in proof for piece in required_proof):
        raise RuntimeError("R4R6_PROP58_PROOF_CHAIN_DRIFT")
    if r"\pi^{4}_{8}=\mathbb Z_2" not in proposition58:
        raise RuntimeError("R4R6_PROP58_SOURCE_GROUP_DRIFT")
    return {
        "proposition_2_5_inclusion_and_conditions": True,
        "equation_5_8_signed_identity": True,
        "proposition_5_8_printed_composition_chain": True,
        "printed_relation_is_a_verified_proof_step": False,
        "source_sign_preserved": "±",
    }


def typed_frontier(m: int = 4, i: int = 8, j: int = 9) -> dict[str, object]:
    """Check dimensions and the j < 3m - 1 sufficient equality condition.

    Integer endpoints are checked, not represented as a proven ProofStep.
    """
    if not all(isinstance(value, int) and not isinstance(value, bool) for value in (m, i, j)):
        raise RuntimeError("R4R6_TYPED_INDICES_INVALID")
    if not (m >= 2 and i == 2 * m and j >= 2):
        raise RuntimeError("R4R6_EXPECTED_IOTA_SPECIALIZATION_INVALID")
    if not j < 3 * m - 1:
        raise RuntimeError("R4R6_PROP25_EQUALITY_CONDITION_NOT_MET")
    alpha = (i + 1, 2 * m + 1)
    beta = (j - 1, i - 1)
    e2beta = (j + 1, i + 1)
    composite = (j + 1, 2 * m + 1)
    delta_alpha = (i - 1, m)
    composite_after_delta = (j - 1, m)
    delta_composite = (j - 1, m)
    if not (alpha == (9, 9) and beta == (8, 7)
            and e2beta == composite == (10, 9)
            and delta_alpha == (7, 4)
            and composite_after_delta == delta_composite == (8, 4)):
        raise RuntimeError("R4R6_TYPED_ENDPOINT_MISMATCH")
    return {
        "m": m, "i": i, "j": j,
        "j_less_than_3m_minus_1": True,
        "alpha": "pi_9^9 (iota_9)",
        "beta": "pi_8^7 (eta_7)",
        "e2_beta": "pi_10^9 (eta_9)",
        "delta_alpha": "pi_7^4",
        "delta_alpha_composed_beta": "pi_8^4",
        "delta_composite": "pi_8^4",
        "typed_endpoints_are_verified_proof_steps": False,
    }


def order_two_and_boundaries(root: Path) -> dict[str, object]:
    from homotopy_groups import DirectSumGroup
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from proof import Relation

    eta = exact_prior_database_result(7, 1)
    pi84 = exact_prior_database_result(4, 4)
    if (not isinstance(eta, Relation)
            or getattr(eta.rhs, "order", None) != 2
            or not isinstance(pi84, Relation)
            or not isinstance(pi84.rhs, DirectSumGroup)
            or len(pi84.rhs.summands) != 2
            or any(getattr(item, "order", None) != 2 for item in pi84.rhs.summands)):
        raise RuntimeError("R4R6_TWO_TORSION_SOURCE_ROWS_INVALID")
    production = (root / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8")
    public = (root / "phase175_r4r5r3_public_order_zero/provider.py").read_text(encoding="utf-8")
    if ("build_public_order_zero_provider" not in production
            or "build_public_order_zero_provider" not in public
            or "eligible_order_zero_sources" not in public):
        raise RuntimeError("R4R6_SHARED_PROVIDER_BOUNDARY_DRIFT")
    return {
        "eta7_prior_group_order": 2,
        "pi84_prior_cyclic_summand_orders": [2, 2],
        "signed_term_reduction": "±(2nu4 - E_nu_prime)∘eta7 = E_nu_prime∘eta7; uses 2eta7=0 and 2(E_nu_prime∘eta7)=0",
        "signed_reduction_executed_as_proof_step": False,
        "shared_order_zero_provider_present": True,
        "new_prop25_provider_connected": False,
        "prior_proof_search_executed": False,
    }


def report_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    path = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    path.mkdir(parents=True, exist_ok=False)
    return path


def run(root: Path, *, dry_run: bool, prior_path: Path | None) -> int:
    output = report_folder()
    result: dict[str, object] = {
        "phase": "175-R4R6",
        "mode": "READ_ONLY_SOURCE_TYPE_BOUNDARY_AUDIT",
        "dry_run": dry_run,
        "gate": "FAIL_R4R6_PROP25_EQ58_SOURCE_FRONTIER",
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
    }
    try:
        result["preflight"] = preflight(root)
        found = find_real_prior(prior_path)
        result["prior_report"] = str(found)
        prior_data = json.loads(found.read_text(encoding="utf-8"))
        result["prior_evidence"] = validate_prior(prior_data)
        result["prior_history"] = validate_prior_history(root, prior_data["source_guard"])
        result["source_evidence"] = source_evidence(
            (root / "sources/toda/Toda_02_2.tex").read_text(encoding="utf-8"),
            (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8"),
        )
        result["typed_frontier"] = typed_frontier()
        result["order_and_implementation_boundary"] = order_two_and_boundaries(root)
        result["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["traceback"] = traceback.format_exc()[-6000:]
    (output / "report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 175 R4R6 — Proposition 2.5 / (5.8) 出典・型・境界監査",
        "", "Gate: `" + str(result["gate"]) + "`", "",
        "Toda Proposition 2.5 の m=4, i=8, j=9 は j < 3m−1 を満たす。",
        "符号 ± を保存し、2η₇=0 と π₈⁴ の位数2成分を用いる整理を記録する。",
        "ここでは ProofStep を生成せず、(5.8) の直接 GIVEN 化もしない。",
        "π₉⁵ は generic-partial-proof のまま。", "",
        "新規 GIVEN: 0 / 新規数学規則: 0 / 全体 pytest: 未実施", "",
    ]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("PHASE175_R4R6_HEAD=" + str(result.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R6_PRIOR_HISTORICAL_HEAD=" + str(result.get("prior_history", {}).get("historical_reviewed_head", "UNVERIFIED")))
    print("PHASE175_R4R6_NEW_GIVEN=0")
    print("PHASE175_R4R6_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4R6_PRODUCTION_CHANGES=0")
    print("PHASE175_R4R6_PI95=NOT_COMPLETE")
    print("PHASE175_R4R6_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R6_REPORT=" + str(output / "report.json"))
    print("PHASE175_R4R6_GATE=" + str(result["gate"]))
    if "error" in result:
        print("PHASE175_R4R6_ERROR=" + str(result["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r5r3-report", type=Path, default=None)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_path=args.r4r5r3_report)


if __name__ == "__main__":
    sys.exit(main())
