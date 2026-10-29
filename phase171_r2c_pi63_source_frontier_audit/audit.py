"""Phase 171 R2C: read-only audit of existing typed premises for pi_6^3.

Never promotes candidate literature statements into ProofSteps, modifies a
proof registry, or equates differently typed generator expressions.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

BASELINE = "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
REVIEWED_DIRECTORIES = (
    "phase171_r1_n3_registered_audit/",
    "phase171_r1c_k3_registered_audit/",
    "phase171_r1d_k3_three_gap_diagnostics/",
    "phase171_r2a_prop56_alignment_audit/",
    "phase171_r2b_prop56_source_dependency_audit/",
    "phase171_r2c_pi63_source_frontier_audit/",
)
EXPECTED_BLOBS = {
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r6_explicit_literature_inputs.py": "c430eb4acee83eaa6338dab9834d46808fac0ad4",
    "phase169_r3h_source_registry.py": "1829e3ac1381e10270dac73a196bfd4983540ea4",
    "phase163_r4_r11_literature_registration.py": "2f3a42173f6482167c364e9ff28621b3bcb62792",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}
LOCATORS = (
    "(5.3)", "Proposition 5.3", "Proposition 2.2", "(4.4)",
    "Proposition 5.6", "(5.6)",
)
TARGET_N = 3
TARGET_K = 3


def git(root: Path, *args: str) -> str:
    """Execute a read-only Git command with explicit failure handling."""
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)
    if proc.returncode:
        raise RuntimeError(
            "git " + " ".join(args) + ": " + proc.stderr.decode("utf-8", "replace").strip()
        )
    return proc.stdout.decode("utf-8", "replace").strip()


def tracked_state(root: Path) -> dict:
    """Allow only audited-path commits ahead of upstream and unchanged source blobs."""
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    upstream_ref = "refs/remotes/origin/develop"
    upstream = git(root, "rev-parse", "--verify", upstream_ref)
    if branch != "develop":
        raise RuntimeError("expected develop branch")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked files are modified")
    git(root, "merge-base", "--is-ancestor", BASELINE, "HEAD")
    try:
        git(root, "merge-base", "--is-ancestor", upstream_ref, "HEAD")
    except RuntimeError as exc:
        raise RuntimeError("origin/develop is behind local HEAD or has diverged") from exc
    committed = git(root, "diff", "--name-only", "-z", BASELINE, "HEAD")
    changed = tuple(path for path in committed.split("\0") if path)
    unknown = tuple(path for path in changed
                    if not any(path.startswith(prefix) for prefix in REVIEWED_DIRECTORIES))
    if unknown:
        raise RuntimeError("non-audit committed changes: " + ", ".join(unknown))
    for path, digest in EXPECTED_BLOBS.items():
        if digest and git(root, "rev-parse", "HEAD:" + path) != digest:
            raise RuntimeError("source blob changed: " + path)
    diff = subprocess.run(["git", "diff", "--binary", "HEAD", "--"],
                          cwd=root, capture_output=True, check=False)
    if diff.returncode:
        raise RuntimeError("cannot inspect tracked binary diff")
    return {
        "branch": branch, "head": head, "origin_develop": upstream,
        "baseline": BASELINE, "reviewed_changes": list(changed),
        "tracked_diff_sha256": sha256(diff.stdout).hexdigest(),
    }


def validate_r2b(report: object) -> dict:
    """Require exactly the saved, successful three-gap R2B scope and provenance."""
    if not isinstance(report, dict) or report.get("phase") != "171 R2B":
        raise ValueError("R2B report required")
    if report.get("read_only") is not True:
        raise ValueError("R2B must be read-only")
    cases = report.get("cases")
    if not isinstance(cases, list) or len(cases) != 3:
        raise ValueError("R2B must contain exactly three cases")
    for expected_n, case in zip((3, 4, 5), cases):
        if not isinstance(case, dict) or case.get("n") != expected_n or case.get("proof_link_count") != 0:
            raise ValueError("R2B gap case or proof-link state differs")
        if case.get("blockers") != ["TYPED_GOAL_MISMATCH", "NO_VERIFIED_PROOF_LINK"]:
            raise ValueError("R2B blocker inventory differs")
    source = report.get("source")
    if not isinstance(source, dict) or not source.get("has_question_marker"):
        raise ValueError("R2B unresolved source reference is missing")
    if "(5.3)" not in source.get("references_in_proof", []):
        raise ValueError("R2B source proof lacks (5.3)")
    return cases[0]


def locator_inventory(bridge: object, *, locators: tuple[str, ...] = LOCATORS) -> list[dict]:
    """Inspect exact registered source provenance; a candidate is not a proof."""
    registry = bridge.registry
    assertions = tuple(registry._assertions.values())
    links = tuple(bridge.proof_links)
    items = []
    for locator in locators:
        matches = []
        for assertion in assertions:
            reference = registry.reference(assertion.reference_id)
            if reference.locator != locator:
                continue
            associated = tuple(link for link in links if link.assertion_id == assertion.assertion_id)
            exact_given = sum(
                link.step is not None
                and getattr(getattr(link.step, "rule", None), "name", None) == "GIVEN"
                and getattr(assertion.origin, "value", None) == "fixed_statement"
                and link.step.conclusion == assertion.content
                for link in associated
            )
            matches.append({
                "assertion_id": assertion.assertion_id,
                "origin": getattr(assertion.origin, "value", str(assertion.origin)),
                "statement_type": type(assertion.content).__name__,
                "statement_repr": repr(assertion.content)[:1500],
                "link_count": len(associated),
                "matching_given_count": exact_given,
                "scope_repr": repr(getattr(assertion, "scope", None))[:350],
            })
        items.append({"locator": locator, "assertion_count": len(matches),
                      "matching_given_total": sum(m["matching_given_count"] for m in matches),
                      "assertions": matches})
    return items


def summarize_pi63(bridge: object, goal: object, inventory: list[dict]) -> dict:
    """Compare registered target and citation provenance without making a derivation."""
    target_id = "shared:0:boundary:Proposition 5.6:pi6_3_group_relation"
    candidate = bridge.registry._assertions.get(target_id)
    if candidate is None:
        raise ValueError("Proposition 5.6 pi6_3 candidate absent")
    links = tuple(link for link in bridge.proof_links if link.assertion_id == target_id)
    if links:
        raise ValueError("Proposition 5.6 target unexpectedly has proof links")
    source53 = next(item for item in inventory if item["locator"] == "(5.3)")
    adopted_hopf = [entry for entry in source53["assertions"]
                    if "nu_prime_hopf_relation" in entry["assertion_id"]]
    return {
        "target": "pi_6^3", "goal_repr": repr(goal)[:2300],
        "candidate_repr": repr(candidate.content)[:2300],
        "typed_equal": type(goal) is type(candidate.content) and goal == candidate.content,
        "candidate_link_count": len(links),
        "toda53_hopf_assertion_count": len(adopted_hopf),
        "toda53_hopf_link_count": sum(item["matching_given_count"] for item in adopted_hopf),
        "toda53_hopf_assertions": adopted_hopf,
        "not_established": [
            "Equality of the DB generator and the literature generator",
            "Verified derivation of the target cyclic group structure",
            "Evidence chain for the order-four relation and generator property",
        ],
    }


def markdown_report(payload: dict) -> str:
    """Document observed and unproved facts without TeX tables."""
    summary = payload["pi63"]
    lines = [
        "# Phase 171 R2C — π₆³ の型付き前提監査", "",
        "R2B が確定した型付き不一致と証明リンク欠落を前提に、現行台帳の出典と型付き命題を監査した。", "",
        "この監査は証明木を変更せず、文献候補を GIVEN に昇格させない。", "",
        "## π₆³ の状態", "",
        f"DB Goal と Proposition 5.6 候補の完全一致：{summary['typed_equal']}。", "",
        f"Proposition 5.6 結論の ProofStep リンク：{summary['candidate_link_count']}件。", "",
        f"(5.3) Hopf 関係の候補：{summary['toda53_hopf_assertion_count']}件。", "",
        f"同関係の照合可能な GIVEN：{summary['toda53_hopf_link_count']}件。", "",
        "## 文献位置別の監査", "",
    ]
    for item in payload["inventory"]:
        lines.append(f"{item['locator']}：登録{item['assertion_count']}件、照合可能な GIVEN {item['matching_given_total']}件。")
        for statement in item["assertions"][:12]:
            lines.append("  - " + statement["assertion_id"] + "（" + statement["origin"] + "）")
    lines.extend([
        "", "## 次の実装との境界", "",
        "(5.3) の Hopf 関係が登録済みであっても、その事実だけでは ν′ の位数や群構造は証明されない。", "",
        "出典を確認できない (5.6)? は採用しない。π₇⁴、π₈⁵ の構成は本監査に含めない。", "",
    ])
    return "\n".join(lines)


def run(root: Path, report_path: Path, *, dry_run: bool) -> int:
    """Validate saved evidence and inspect the real typed registry read-only."""
    before = tracked_state(root)
    report = json.loads(report_path.read_text(encoding="utf-8-sig"))
    validate_r2b(report)
    print("PHASE171_R2C_MODE=READ_ONLY_PI63_FRONTIER", flush=True)
    print("PHASE171_R2C_TARGET=3,3", flush=True)
    if dry_run:
        after = tracked_state(root)
        if before != after:
            raise RuntimeError("Git state changed during DryRun")
        print("PHASE171_R2C_DRY_RUN=PASS", flush=True)
        print("PHASE171_R2C_TRACKED_UNCHANGED=True", flush=True)
        print("PHASE171_R2C_RESULT=PASS", flush=True)
        return 0

    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=TARGET_N, k=TARGET_K)
    if len(goals) != 1:
        raise RuntimeError("expected one registered typed pi_6^3 Goal")
    inventory = locator_inventory(bridge)
    summary = summarize_pi63(bridge, goals[0], inventory)
    output = {
        "phase": "171 R2C", "mode": "READ_ONLY_PI63_FRONTIER", "read_only": True,
        "source_report": str(report_path), "git": before,
        "pi63": summary, "inventory": inventory,
    }
    for item in inventory:
        print("PHASE171_R2C_SOURCE=" + json.dumps({
            "locator": item["locator"], "assertion_count": item["assertion_count"],
            "matching_given_total": item["matching_given_total"],
        }, ensure_ascii=False), flush=True)
    print("PHASE171_R2C_DETAIL=" + json.dumps({
        "n": 3, "k": 3, "typed_equal": summary["typed_equal"],
        "candidate_link_count": summary["candidate_link_count"],
        "toda53_hopf_assertion_count": summary["toda53_hopf_assertion_count"],
        "toda53_hopf_link_count": summary["toda53_hopf_link_count"],
    }, ensure_ascii=False), flush=True)
    after = tracked_state(root)
    if before != after:
        raise RuntimeError("Git state changed during audit")
    output["tracked_unchanged"] = True
    base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    directory = base / ("phase171_r2c_pi63_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    directory.mkdir(parents=True, exist_ok=False)
    path = directory / "frontier.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    (directory / "frontier.md").write_text(markdown_report(output), encoding="utf-8")
    print("PHASE171_R2C_REPORT=" + str(path), flush=True)
    print("PHASE171_R2C_TRACKED_UNCHANGED=True", flush=True)
    print("PHASE171_R2C_RESULT=PASS", flush=True)
    return 0


def main() -> int:
    """Provide a safe CLI for Windows PowerShell module execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.root.resolve(), args.report.resolve(), dry_run=args.dry_run)
    except Exception as exc:
        print("PHASE171_R2C_ERROR=" + f"{type(exc).__name__}: {exc}", flush=True)
        print(traceback.format_exc()[-2400:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
