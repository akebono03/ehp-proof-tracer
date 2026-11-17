"""Phase 175 R4: read-only, source-first audit of pi_9^5.

No mathematical rule, GIVEN, saved proof, or narrative is registered here.
The existing R1 observer runs in isolated worker processes.
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


PACKAGE = "phase175_r4_pi95_audit"
WORKER_MARKER = "__PHASE175_R4_PI95_WORKER__="
REVIEWED_R3_HEAD = "a1ce1558be6bab647c5d23d26047b9cce45d4e2e"
TARGET = (5, 4)
PRIOR = (4, 4)
ALLOWED_DIRTY_PREFIX = "phase175_r3r12_hopf_conclusion/"
TRACKED_PYTEST_CACHE_FILE = ".pytest_cache/v/cache/nodeids"
# R1's baseline predates the R3 general-provider integration. Only this
# reviewed path changed among the 18 inherited R1/R2 source blob pins.
REVIEWED_R3_SOURCE_PATH = "phase165_r52_r9_shared_math.py"
REVIEWED_R1_SOURCE_BLOB = "9fa11b383812570fae1a26868c98992a5934a327"
REVIEWED_R3_SOURCE_BLOB = "ee1efa2d91df479168b7b964d24e814e0f516449"


def git(root: Path, *args: str, allow_failure: bool = False) -> tuple[int, str]:
    """Read Git metadata; never fetch or mutate the checkout."""
    completed = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if completed.returncode and not allow_failure:
        raise RuntimeError("R4_GIT_ERROR: " + " ".join(args) + ": " + completed.stderr.strip())
    return completed.returncode, completed.stdout.strip()


def validate_dirty_paths(paths: list[str]) -> list[str]:
    """Allow reviewed display edits and one exact pytest cache file only.

    pytest updated an already-tracked nodeids cache before the R4 guard ran.
    The cache is never a proof/source input. All other tracked paths still
    fail closed; this function never resets or edits a user's working tree.
    """
    clean = sorted(set(path.strip() for path in paths if path.strip()))
    unexpected = [
        path for path in clean
        if not path.startswith(ALLOWED_DIRTY_PREFIX)
        and path != TRACKED_PYTEST_CACHE_FILE
    ]
    if unexpected:
        raise RuntimeError("R4_UNREVIEWED_TRACKED_CHANGES: " + repr(unexpected))
    return clean


def reviewed_source_pins(
    root: Path, source_blobs: dict[str, str], extra_pins: dict[str, str],
) -> dict[str, str]:
    """Merge reviewed historical pins, updating only the verified R3 source.

    The old R1 SHA is retained as a lineage guard. The R3 SHA must be the
    actual Git object at the reviewed R3 handoff, not a permissive exception
    for arbitrary later changes or working-tree modifications.
    """
    pins = dict(source_blobs)
    for name, sha in extra_pins.items():
        if name in pins and pins[name] != sha:
            raise RuntimeError("R4_SOURCE_PIN_CONFLICT: " + name)
        pins[name] = sha
    if pins.get(REVIEWED_R3_SOURCE_PATH) != REVIEWED_R1_SOURCE_BLOB:
        raise RuntimeError("R4_REVIEWED_R1_SOURCE_PIN_CHANGED")
    _, r3_blob = git(
        root, "rev-parse", REVIEWED_R3_HEAD + ":" + REVIEWED_R3_SOURCE_PATH,
    )
    if r3_blob != REVIEWED_R3_SOURCE_BLOB:
        raise RuntimeError("R4_REVIEWED_R3_SOURCE_PIN_MISMATCH")
    pins[REVIEWED_R3_SOURCE_PATH] = REVIEWED_R3_SOURCE_BLOB
    return pins


def preflight(root: Path) -> dict[str, object]:
    """Check Git lineage and the R1/R2 reviewed mathematical source blobs."""
    from phase175_r1_k4_audit.audit import SOURCE_BLOBS
    from phase175_r2_k4_frontier_audit.audit import EXTRA_PINS

    _, root_name = git(root, "rev-parse", "--show-toplevel")
    if Path(root_name).resolve() != root.resolve():
        raise RuntimeError("R4_NOT_REPOSITORY_ROOT")
    _, branch = git(root, "branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R4_WRONG_BRANCH: " + branch)
    _, head = git(root, "rev-parse", "HEAD")
    ancestor, _ = git(
        root, "merge-base", "--is-ancestor", REVIEWED_R3_HEAD, "HEAD",
        allow_failure=True,
    )
    if ancestor:
        raise RuntimeError("R4_REVIEWED_R3_HEAD_NOT_ANCESTOR")
    _, changed = git(root, "diff", "HEAD", "--name-only")
    dirty = validate_dirty_paths(changed.splitlines())
    pins = reviewed_source_pins(root, SOURCE_BLOBS, EXTRA_PINS)
    for path, expected in pins.items():
        if not (root / path).is_file():
            raise RuntimeError("R4_SOURCE_MISSING: " + path)
        _, observed = git(root, "rev-parse", "HEAD:" + path)
        if observed != expected:
            raise RuntimeError("R4_SOURCE_PIN_DRIFT: " + path)
    _, origin = git(root, "rev-parse", "--verify", "origin/develop", allow_failure=True)
    return {
        "branch": branch,
        "head": head,
        "reviewed_r3_ancestor": REVIEWED_R3_HEAD,
        "origin_develop_observed": origin or None,
        "head_matches_local_origin": bool(origin and origin == head),
        "tracked_dirty_allowed_r3r12": [
            path for path in dirty if path.startswith(ALLOWED_DIRTY_PREFIX)
        ],
        "tracked_dirty_pytest_cache": [
            path for path in dirty if path == TRACKED_PYTEST_CACHE_FILE
        ],
        "pinned_sources": pins,
        "r3_reviewed_source_pin_transition": {
            "path": REVIEWED_R3_SOURCE_PATH,
            "r1_baseline_blob": REVIEWED_R1_SOURCE_BLOB,
            "r3_reviewed_blob": REVIEWED_R3_SOURCE_BLOB,
            "r3_commit": REVIEWED_R3_HEAD,
        },
        "pinned_source_count": len(pins),
    }


def evidence_from_text(text: str) -> dict[str, object]:
    """Audit actual Chapter V proof clauses, not the goal as an axiom."""
    prop = r"\begin{proposition}\label{prop:5.8}"
    end_prop = r"\end{proposition}"
    next_eq = r"\begin{equation}\label{eq:5.9}"
    if text.count(prop) != 1:
        raise RuntimeError("R4_PROP58_SOURCE_AMBIGUOUS")
    start = text.index(prop)
    finish = text.find(end_prop, start)
    proof_end = text.find(next_eq, finish)
    if finish < 0 or proof_end < finish:
        raise RuntimeError("R4_PROP58_PROOF_BOUNDARY_MISSING")
    theorem = text[start:finish]
    proof = text[finish:proof_end]
    expected_theorem = (
        r"\pi^{4}_{8}=\mathbb Z_2\gen{\nu_{4}\circ\eta_7}"
        r"\oplus \mathbb Z_2\gen{E\nu'\circ\eta_7}"
    )
    expected = {
        "prior_pi84_printed": expected_theorem in theorem,
        "target_pi95_printed": r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}" in theorem,
        "source_ehp_delta_iota9": r"\Delta:\pi_9^9\to\pi_7^4" in proof,
        "source_ehp_delta_eta9": r"\Delta(\eta_9)" in proof,
        "source_eq58_image": r"(2\nu_4-E\nu')" in proof,
        "source_proposition25": "by Prop2.5" in proof,
        "source_pi95_quotient": r"\pi_9^5=E\pi_8^4" in proof,
        "source_ehp_dimension_typo": r"\pi^{9}_{8}" in proof,
    }
    required = [k for k in expected if k != "source_ehp_dimension_typo"]
    missing = [k for k in required if not expected[k]]
    if missing:
        raise RuntimeError("R4_SOURCE_PROOF_CLAUSE_MISSING: " + repr(missing))
    expected["source_ehp_dimension_typo_note"] = (
        "The transcription prints pi_8^9 where the EHP source must be pi_8^4; "
        "treat as a source-text defect, not a typed inference premise."
        if expected["source_ehp_dimension_typo"] else "No observed typo of this form"
    )
    expected["no_direct_goal_given"] = True
    return expected


def source_inventory(root: Path) -> dict[str, object]:
    """Verify the earlier fixed-source text, typed generator and manifest order."""
    from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
        checked_prior_statements,
        pinned_source_text,
        reviewed_source_positions,
    )
    from homotopy_groups import TodaPrimaryGroup

    record = evidence_from_text(pinned_source_text(root))
    source_group, image = checked_prior_statements(root)
    if (
        source_group.lhs != TodaPrimaryGroup(9, 5)
        or source_group.rhs.order != 2
        or image.map.target_group != source_group.lhs
        or image.positive_value != source_group.rhs.generator
    ):
        raise RuntimeError("R4_TYPED_PI95_SOURCE_INCONSISTENT")
    positions = reviewed_source_positions()
    if not (0 < positions[0] < positions[1]):
        raise RuntimeError("R4_SOURCE_POSITION_ORDER_CHANGED")
    record["typed_pi95_source_checked"] = True
    record["typed_nu5_eta8_generator_checked"] = True
    record["prop58_position"] = positions[0]
    record["eq510_position"] = positions[1]
    record["source_is_derived_goal_proof"] = False
    return record


def validate_observations(target: dict[str, object], prior: dict[str, object]) -> dict[str, object]:
    """Classify only actual R1 worker observations; never promote a target GIVEN."""
    if (target.get("n"), target.get("k")) != TARGET:
        raise RuntimeError("R4_TARGET_COORDINATE_MISMATCH")
    if (prior.get("n"), prior.get("k")) != PRIOR:
        raise RuntimeError("R4_PRIOR_COORDINATE_MISMATCH")
    if (
        target.get("audit_result") != "INCOMPLETE_AND_WEB_CONFIRMED"
        or target.get("search_status") not in ("search_failed", "partial")
        or target.get("db_goal_typed") is not True
        or target.get("search_conclusion_is_none") is not True
        or target.get("web_key") != "generic-partial-proof"
        or target.get("web_partial") is not True
        or target.get("search_proven_count") != 0
    ):
        raise RuntimeError("R4_TARGET_STATUS_CHANGED; inspect without silent promotion")
    goals = target.get("search_open_goals")
    if (
        not isinstance(goals, list) or len(goals) != 3
        or not isinstance(goals[0], str)
        or not goals[0].startswith("CyclicStructureStatement(")
        or any(not isinstance(g, str) or not g.startswith("Relation(") for g in goals[1:])
    ):
        raise RuntimeError("R4_TARGET_OPEN_GOALS_CHANGED")
    if (
        prior.get("audit_result") != "COMPLETE_AND_WEB_VERIFIED"
        or prior.get("db_goal_typed") is not True
        or prior.get("trust_verified") is not True
        or prior.get("search_open_count") != 0
    ):
        raise RuntimeError("R4_PI84_PRIOR_NOT_VERIFIED")
    return {
        "target_group": "pi_9^5",
        "prior_group": "pi_8^4",
        "open_goals_count": len(goals),
        "open_goals": goals,
        "target_status": target["audit_result"],
        "prior_status": prior["audit_result"],
        "proof_complete": False,
    }


def worker(n: int, k: int) -> int:
    """Reuse the existing R1 real group observer without changing providers."""
    try:
        from phase175_r1_k4_audit.audit import inspect_one_group
        record = inspect_one_group(n, k)
        print(WORKER_MARKER + json.dumps(record, ensure_ascii=False, default=str))
        return 0
    except Exception:
        print(traceback.format_exc(), file=sys.stderr)
        return 2


def decode_worker(stdout: str, exit_code: int, n: int, k: int) -> dict[str, object]:
    markers = [line[len(WORKER_MARKER):] for line in stdout.splitlines()
               if line.startswith(WORKER_MARKER)]
    if exit_code or len(markers) != 1:
        raise RuntimeError("R4_WORKER_FAILURE_OR_MARKERS: " + str((n, k, exit_code, len(markers))))
    try:
        result = json.loads(markers[0])
    except (ValueError, TypeError) as exc:
        raise RuntimeError("R4_WORKER_JSON_INVALID") from exc
    if not isinstance(result, dict) or (result.get("n"), result.get("k")) != (n, k):
        raise RuntimeError("R4_WORKER_COORDINATES_INVALID")
    return result


def launch_worker(root: Path, n: int, k: int, timeout: int, output: Path) -> dict[str, object]:
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        proc = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker",
             "--n", str(n), "--k", str(k)], cwd=root, env=env,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            check=False, timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        (output / f"pi_{n+k}_{n}.log").write_text(str(exc), encoding="utf-8")
        raise RuntimeError(f"R4_WORKER_TIMEOUT: {n},{k}") from exc
    (output / f"pi_{n+k}_{n}.log").write_text(
        proc.stdout + "\nSTDERR:\n" + proc.stderr, encoding="utf-8",
    )
    return decode_worker(proc.stdout, proc.returncode, n, k)


def make_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    name = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    out = base / "EHPProofTracerAudit" / PACKAGE / name
    out.mkdir(parents=True, exist_ok=False)
    return out


def write_report(out: Path, result: dict[str, object]) -> None:
    (out / "report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Phase 175 R4 — $\\pi_9^5$ 監査（Audit Only）", "",
        "Source-first。証明規則・GIVEN・Web Narrative の追加はない。", "",
        "- Gate: `" + str(result["gate"]) + "`",
        "- HEAD: `" + str(result.get("preflight", {}).get("head", "unknown")) + "`",
        "- 新規 GIVEN: 0／新規数学規則: 0／全体 pytest: 未実施", "",
        "## 出典監査", "",
        "Toda Proposition 5.8 の印刷結果は独立した目標証明として採用しない。",
        "同節の証明に現れる EHP 列の `\\pi_8^9` は次元の誤植候補。",
        "型付き検査・今後の推論で用いるべき対応箇所は `\\pi_8^4`。", "",
        "## 監査で確認する一般導出の候補", "",
        "1. 既証明の $\\pi_8^4=\\mathbb Z/2\\{\\nu_4\\eta_7\\}\\oplus\\mathbb Z/2\\{E\\nu'\\eta_7\\}$。",
        "2. Toda (5.8) と既証明の $\\pi_7^4$ による $\\Delta:\\pi_9^9\\to\\pi_7^4$ の単射性。",
        "3. EHP 完全性から $E:\\pi_8^4\\to\\pi_9^5$ の全射性。",
        "4. Proposition 2.5 と (5.8)、$2\\eta_7=0$ による $\\Delta(\\eta_9)=\\pm E\\nu'\\eta_7$。",
        "5. 完全性により $\\ker E=\\langle E\\nu'\\eta_7\\rangle$。",
        "6. 商群と懸垂の一般規則で $E(\\nu_4\\eta_7)=\\nu_5\\eta_8$ を検証。", "",
        "これらは実装済みの新たな ProofStep ではなく、次段階で接続すべき義務である。", "",
        "## 実測した Open Goals", "",
    ]
    observed = result.get("observations")
    if isinstance(observed, dict):
        for goal in observed["open_goals"]:
            lines.append("- `" + str(goal).replace("`", "'") + "`")
    else:
        lines.append("DryRun では Proof Search を起動しないため、実測 Open Goals はない。")
    lines.extend(["", "## 判定境界", "", "R4 は監査のみ。目標群の証明完成は宣言しない。", ""])
    (out / "report.md").write_text("\n".join(lines), encoding="utf-8")


def run(root: Path, dry_run: bool, timeout: int) -> int:
    out = make_report_path()
    report: dict[str, object] = {
        "phase": "175-R4", "mode": "READ_ONLY_AUDIT", "dry_run": dry_run,
        "production_changes": [], "new_given": 0,
        "new_mathematical_rules": 0, "full_pytest_executed": False,
        "gate": "FAIL_R4_AUDIT_NOT_COMPLETED",
    }
    try:
        report["preflight"] = preflight(root)
        report["source"] = source_inventory(root)
        if dry_run:
            report["gate"] = "PASS_R4_AUDIT_ONLY_DRYRUN"
        else:
            target = launch_worker(root, *TARGET, timeout, out)
            prior = launch_worker(root, *PRIOR, timeout, out)
            report["observations"] = validate_observations(target, prior)
            report["actual_rows"] = {"target": target, "prior_pi84": prior}
            report["gate"] = "PASS_R4_PI95_FRONTIER_RECORDED_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-5000:]
    write_report(out, report)
    print("PHASE175_R4_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4_PINNED_SOURCES=" + str(report.get("preflight", {}).get("pinned_source_count", 0)))
    print("PHASE175_R4_NEW_GIVEN=0")
    print("PHASE175_R4_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4_REPORT=" + str(out / "report.json"))
    print("PHASE175_R4_GATE=" + str(report["gate"]))
    if "error" in report:
        print("PHASE175_R4_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    options = parser.parse_args(argv)
    if options.worker:
        return worker(options.n, options.k)
    if options.timeout_seconds < 30:
        parser.error("--timeout-seconds must be at least 30")
    return run(options.root.resolve(), options.dry_run, options.timeout_seconds)


if __name__ == "__main__":
    sys.exit(main())
