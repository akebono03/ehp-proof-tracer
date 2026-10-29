"""Phase 171 R2A: read-only Proposition 5.6 / DB typed-goal alignment audit.

This inspects the current registered sources; it never creates proof leaves,
changes a mathematical rule, or interprets an unverified source as a proof.
"""
from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

SOURCE_AUDIT_HEAD = "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
REVIEWED_AUDIT_DIRECTORIES = (
    "phase171_r1_n3_registered_audit/",
    "phase171_r1c_k3_registered_audit/",
    "phase171_r1d_k3_three_gap_diagnostics/",
    "phase171_r2a_prop56_alignment_audit/",
)
EXPECTED_BLOBS = {
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
}
CASES = ((3, "pi6_3_group_relation"), (4, "pi7_4_group_relation"),
         (5, "pi8_5_group_relation"))


def git(root: Path, *arguments: str) -> str:
    """Execute a read-only Git query; reject failures."""
    result = subprocess.run(
        ["git", *arguments], cwd=root, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "git " + " ".join(arguments) + ": "
            + result.stderr.decode("utf-8", errors="replace").strip()
        )
    return result.stdout.decode("utf-8", errors="replace").strip()


def git_state(root: Path) -> dict:
    """Accept a clean descendant changing only reviewed Phase 171 audit files.

    The baseline commit is fixed, while subsequent audit-only commits do not
    require a new literal HEAD entry. Any production change is refused.
    """
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    upstream = git(root, "rev-parse", "--verify", "refs/remotes/origin/develop")
    if branch != "develop" or upstream != head:
        raise RuntimeError(f"unexpected HEAD/upstream: {branch} {head} {upstream}")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked files changed; audit refused")

    # git merge-base --is-ancestor exits nonzero if the reviewed baseline is
    # missing or this checkout does not descend from it. git() then fails shut.
    git(root, "merge-base", "--is-ancestor", SOURCE_AUDIT_HEAD, "HEAD")
    changed_files = git(
        root, "diff", "--name-only", "-z", SOURCE_AUDIT_HEAD, "HEAD"
    )
    paths = tuple(path for path in changed_files.split("\0") if path)
    unreviewed = tuple(
        path for path in paths
        if not any(path.startswith(prefix) for prefix in REVIEWED_AUDIT_DIRECTORIES)
    )
    if unreviewed:
        raise RuntimeError("unreviewed committed paths: " + ", ".join(unreviewed))

    for path, expected_blob in EXPECTED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected_blob:
            raise RuntimeError("reviewed source blob changed: " + path)
    process = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if process.returncode:
        raise RuntimeError("cannot inspect tracked diff")
    return {
        "branch": branch, "head": head, "origin_develop": upstream,
        "reviewed_baseline": SOURCE_AUDIT_HEAD,
        "committed_audit_changes": paths,
        "tracked_diff_sha256": sha256(process.stdout).hexdigest(),
    }


def validate_r1c_report(report: object) -> tuple[dict, ...]:
    """Require the observed 32-coordinate R1C audit, not untrusted status text."""
    if not isinstance(report, dict):
        raise ValueError("R1C report is not a JSON object")
    if (report.get("phase"), report.get("stem"), report.get("dry_run")) != ("171 R1C", 3, False):
        raise ValueError("wrong R1C audit scope")
    if report.get("result") != "AUDIT_COMPLETE_WITH_GAPS" or report.get("tracked_unchanged") is not True:
        raise ValueError("R1C audit is not a completed unchanged-tree inspection")
    preflight = report.get("preflight")
    if not isinstance(preflight, dict) or preflight.get("head") != SOURCE_AUDIT_HEAD:
        raise ValueError("R1C source commit differs")
    domain = report.get("domain")
    rows = report.get("rows")
    if not isinstance(domain, list) or not isinstance(rows, list) or len(domain) != 32 or len(rows) != 32:
        raise ValueError("R1C must contain 32 registered coordinates and worker rows")
    positions = []
    for registration, row in zip(domain, rows):
        if not isinstance(registration, dict) or not isinstance(row, dict):
            raise ValueError("invalid R1C row")
        n = registration.get("n")
        if type(n) is not int or n < 2 or registration.get("k") != 3 or row.get("n") != n or row.get("k") != 3:
            raise ValueError("R1C coordinate mismatch")
        positions.append(n)
    if positions != sorted(set(positions)):
        raise ValueError("R1C coordinates not unique and sorted")
    gaps = tuple(row for row in rows if row.get("result") != "COMPLETE_AND_WEB_VERIFIED")
    if tuple(row["n"] for row in gaps) != (3, 4, 5):
        raise ValueError("R1C gap coordinates differ")
    if any(row.get("search_status") != "search_failed" or row.get("proven_steps") != 0
           or row.get("result") != "PROOF_UNFINISHED" for row in gaps):
        raise ValueError("R1C gap search status differs")
    if (report.get("domain_checked"), report.get("domain_complete"),
        report.get("domain_gaps"), report.get("worker_failures")) != (32, 29, 3, 0):
        raise ValueError("R1C counts differ")
    return gaps


def short(value: object, limit: int = 450) -> str:
    """Render bounded diagnostic values without changing their semantics."""
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + " [truncated]"


def typed_differences(left: object, right: object, *, limit: int = 24) -> list[dict]:
    """Compare dataclass trees by exact type and field; never equate aliases."""
    differences: list[dict] = []

    def visit(a: object, b: object, path: str, depth: int) -> None:
        if len(differences) >= limit:
            return
        if type(a) is not type(b):
            differences.append({"path": path, "kind": "type", "left": type(a).__name__, "right": type(b).__name__})
            return
        if depth > 12:
            if a != b:
                differences.append({"path": path, "kind": "depth_limit", "left": short(a), "right": short(b)})
            return
        if is_dataclass(a) and not isinstance(a, type):
            for field in fields(a):
                visit(getattr(a, field.name), getattr(b, field.name), path + "." + field.name, depth + 1)
                if len(differences) >= limit:
                    break
            return
        if isinstance(a, (tuple, list)):
            if len(a) != len(b):
                differences.append({"path": path + ".length", "kind": "length", "left": len(a), "right": len(b)})
            for i in range(min(len(a), len(b))):
                visit(a[i], b[i], path + f"[{i}]", depth + 1)
                if len(differences) >= limit:
                    break
            return
        if isinstance(a, dict):
            if set(a) != set(b):
                differences.append({"path": path, "kind": "keys", "left": short(sorted(a, key=repr)), "right": short(sorted(b, key=repr))})
            for key in sorted(set(a) & set(b), key=repr):
                visit(a[key], b[key], path + "[" + short(key, 100) + "]", depth + 1)
                if len(differences) >= limit:
                    break
            return
        if a != b:
            differences.append({"path": path, "kind": "value", "left": short(a), "right": short(b)})

    visit(left, right, "goal", 0)
    return differences


def inspect_case(bridge: object, inputs: dict, n: int, key: str, *, selector=None) -> dict:
    """Compare actual typed DB goal and exact Proposition 5.6 component."""
    if selector is None:
        from phase165_r55_nk_only_goal import registered_group_goal_candidates
        selector = registered_group_goal_candidates

    goals = selector(bridge, n=n, k=3)
    source = inputs[key]
    matches = [
        (assertion_id, assertion)
        for assertion_id, assertion in bridge.registry._assertions.items()
        if assertion_id.endswith("boundary:Proposition 5.6:" + key)
    ]
    registry = []
    for identifier, assertion in matches:
        links = [link for link in bridge.proof_links if link.assertion_id == identifier]
        registry.append({
            "assertion_id": identifier,
            "origin": getattr(getattr(assertion, "origin", None), "value", str(getattr(assertion, "origin", None))),
            "content_type": type(assertion.content).__name__,
            "equals_candidate": assertion.content == source.statement,
            "proof_link_count": len(links),
            "linked_step_count": sum(link.step is not None for link in links),
            "recorded_content": short(assertion.content, 1500),
        })
    if len(goals) != 1:
        return {"n": n, "k": 3, "key": key, "goal_count": len(goals),
                "source_assertions": registry, "diagnostic": "goal is not unique"}
    goal = goals[0]
    return {
        "n": n, "k": 3, "key": key, "goal_count": len(goals),
        "goal_type": type(goal).__name__,
        "goal_repr": short(goal, 2500),
        "source_repr": short(source.statement, 2500),
        "exact_equal": type(goal) is type(source.statement) and goal == source.statement,
        "differences": typed_differences(goal, source.statement),
        "source_description": source.source_description,
        "source_assertions": registry,
    }


def render_markdown(payload: dict) -> str:
    """Report observable evidence without asserting that a theorem was proved."""
    rows = [
        "# Phase 171 R2A — Proposition 5.6 型付き照合監査", "",
        "本監査は数学的証明を作成しない。登録済み Goal と命題候補の実データを厳密比較する。", "",
        "| n | Goal | Proposition 5.6 候補との厳密一致 | 命題リンク数 |",
        "|---:|---|---|---:|",
    ]
    for item in payload["cases"]:
        counts = sum(entry["proof_link_count"] for entry in item["source_assertions"])
        rows.append(
            f"| {item['n']} | $\\pi_{{{item['n'] + 3}}}^{{{item['n']}}}$ | "
            f"{item.get('exact_equal')} | {counts} |"
        )
    for item in payload["cases"]:
        rows.extend(["", f"## $\\pi_{{{item['n'] + 3}}}^{{{item['n']}}}$", "",
                     "```json", json.dumps(item, ensure_ascii=False, indent=2), "```"])
    rows += ["", "SOURCE_UNVERIFIED やリンクなしの命題を証明済み前提と見なさない。", ""]
    return "\n".join(rows)


def run(root: Path, report_path: Path, *, dry_run: bool) -> int:
    """Validate source status, perform non-mutating comparison, write outside repo."""
    before = git_state(root)
    report = json.loads(report_path.read_text(encoding="utf-8-sig"))
    gaps = validate_r1c_report(report)
    print("PHASE171_R2A_MODE=AUDIT_ONLY", flush=True)
    print(f"PHASE171_R2A_SOURCE={report_path}", flush=True)
    print("PHASE171_R2A_GAPS=" + ",".join(str(gap["n"]) for gap in gaps), flush=True)
    if dry_run:
        result = {"mode": "DRY_RUN", "cases": []}
    else:
        from phase165_r52_r9_shared_math import build_shared_typed_bridge
        from phase165_r6_explicit_literature_inputs import prop56_inputs

        inputs = {item.component_key: item for item in prop56_inputs()}
        if len(inputs) != 5 or not {key for _, key in CASES}.issubset(inputs):
            raise RuntimeError("reviewed Proposition 5.6 candidate inventory changed")
        bridge = build_shared_typed_bridge()
        cases = [inspect_case(bridge, inputs, n, key) for n, key in CASES]
        for item in cases:
            summary = {
                "n": item["n"], "goal_count": item["goal_count"],
                "exact_equal": item.get("exact_equal"),
                "proof_link_count": sum(entry["proof_link_count"] for entry in item["source_assertions"]),
                "differences": item.get("differences", []),
                "source_assertions": [{"assertion_id": x["assertion_id"], "origin": x["origin"]} for x in item["source_assertions"]],
            }
            print("PHASE171_R2A_DETAIL=" + json.dumps(summary, ensure_ascii=False, sort_keys=True), flush=True)
        result = {"mode": "READ_ONLY_TYPED_ALIGNMENT", "cases": cases}
    after = git_state(root)
    unchanged = before == after
    print("PHASE171_R2A_TRACKED_UNCHANGED=" + str(unchanged), flush=True)
    if not unchanged:
        print("PHASE171_R2A_RESULT=TRACKED_CHANGED", flush=True)
        return 2
    if dry_run:
        print("PHASE171_R2A_DRY_RUN=PASS", flush=True)
    else:
        recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
        output = recovery / ("phase171_r2a_prop56_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        output.mkdir(parents=True, exist_ok=False)
        payload = {"phase": "171 R2A", "source_report": str(report_path),
                   "source_head": SOURCE_AUDIT_HEAD, "current_git": before,
                   "read_only": True, **result}
        (output / "alignment.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (output / "alignment.md").write_text(render_markdown(payload), encoding="utf-8")
        print("PHASE171_R2A_REPORT=" + str(output / "alignment.json"), flush=True)
    print("PHASE171_R2A_RESULT=PASS", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.root.resolve(), args.report.resolve(), dry_run=args.dry_run)
    except Exception as exc:
        print("PHASE171_R2A_ERROR=" + f"{type(exc).__name__}: {exc}", flush=True)
        print(traceback.format_exc()[-2500:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
