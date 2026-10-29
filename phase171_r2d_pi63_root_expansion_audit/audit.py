"""Inspect the real screened backward-search frontier for pi_6^3, read-only.

A proposed GoalExpansion, a fixed statement, or an archive text is not a
completed ProofStep. This diagnostic never promotes any of them into proof.
"""
from __future__ import annotations

import argparse
from collections import Counter
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
    "phase171_r2d_pi63_root_expansion_audit/",
)
EXPECTED_BLOBS = {
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r6_explicit_literature_inputs.py": "c430eb4acee83eaa6338dab9834d46808fac0ad4",
    "phase169_r3h_source_registry.py": "1829e3ac1381e10270dac73a196bfd4983540ea4",
    "phase163_r4_r11_literature_registration.py": "2f3a42173f6482167c364e9ff28621b3bcb62792",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase165_r3_recursive_search.py": "9c424f61a2b4a2d7789777017ad4f91292b0ad30",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}
LOCATORS = (
    "(5.3)", "Proposition 5.3", "Proposition 2.2",
    "Proposition 4.2 (4.4)", "(4.4)",
    "Proposition 5.6", "(5.6)",
)
MAX_PREVIEW = 30


def git(root: Path, *args: str) -> str:
    """Run read-only Git commands with a checked return code."""
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "git " + " ".join(args) + ": "
            + result.stderr.decode("utf-8", "replace").strip()
        )
    return result.stdout.decode("utf-8", "replace").strip()


def tracked_state(root: Path) -> dict:
    """Allow committed audit-only additions, never unscreened source edits."""
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
        raise RuntimeError("origin/develop is ahead of or diverged from local HEAD") from exc
    changed = tuple(path for path in git(
        root, "diff", "--name-only", "-z", BASELINE, "HEAD"
    ).split("\0") if path)
    outside = tuple(path for path in changed if not any(
        path.startswith(prefix) for prefix in REVIEWED_DIRECTORIES
    ))
    if outside:
        raise RuntimeError("unreviewed committed changes: " + ", ".join(outside))
    for path, expected in EXPECTED_BLOBS.items():
        if expected and git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("source blob changed: " + path)
    changes = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"],
        cwd=root, capture_output=True, check=False,
    )
    if changes.returncode:
        raise RuntimeError("cannot inspect tracked diff")
    return {
        "branch": branch, "head": head, "upstream": upstream,
        "baseline": BASELINE, "reviewed_changes": list(changed),
        "tracked_diff_sha256": sha256(changes.stdout).hexdigest(),
    }


def validate_r2c(payload: object) -> dict:
    """Reject any report other than the successful recorded pi_6^3 frontier."""
    if not isinstance(payload, dict) or payload.get("phase") != "171 R2C":
        raise ValueError("R2C report required")
    if payload.get("read_only") is not True:
        raise ValueError("R2C source report must be read-only")
    if payload.get("tracked_unchanged") is not True:
        raise ValueError("R2C tracked verification missing")
    case = payload.get("pi63")
    if not isinstance(case, dict) or case.get("target") != "pi_6^3":
        raise ValueError("R2C pi_6^3 report missing")
    if case.get("typed_equal") is not False or case.get("candidate_link_count") != 0:
        raise ValueError("R2C source goal/proof state differs")
    if case.get("toda53_hopf_link_count") != 1:
        raise ValueError("R2C (5.3) Hopf premise inventory differs")
    return case


def eligible_source_inventory(complete_bridge: object, screened_bridge: object) -> list[dict]:
    """Count screened eligible GIVENs per exact source locator, not aliases."""
    registry = complete_bridge.registry
    fixed = tuple(registry._assertions.values())
    steps = tuple(screened_bridge.proof_links)
    inventory = []
    for locator in LOCATORS:
        registered = []
        available = []
        for assertion in fixed:
            reference = registry.reference(assertion.reference_id)
            if reference.locator != locator:
                continue
            registered.append(assertion.assertion_id)
            for link in steps:
                step = link.step
                if (link.assertion_id == assertion.assertion_id
                        and step is not None
                        and getattr(getattr(step, "rule", None), "name", "") == "GIVEN"
                        and not getattr(step, "premises", ())
                        and type(step.conclusion) is type(assertion.content)
                        and step.conclusion == assertion.content):
                    available.append(assertion.assertion_id)
        inventory.append({
            "locator": locator,
            "registered_assertions": len(registered),
            "screened_given_links": len(available),
            "screened_ids": available,
        })
    return inventory


def root_expansion_inventory(goal: object, provider: object, screened_bridge: object) -> dict:
    """Summarize genuine backward proposals; never treat proposals as proofs."""
    if not callable(provider):
        raise TypeError("provider must be callable")
    options = provider(goal)
    if not isinstance(options, tuple):
        raise TypeError("provider must return a tuple")
    names = Counter()
    examples = []
    linked = tuple(screened_bridge.proof_links)
    for index, option in enumerate(options):
        premises = getattr(option, "subgoals", None)
        rule = getattr(option, "rule", None)
        if not isinstance(premises, tuple) or rule is None:
            raise TypeError("invalid typed backward expansion")
        name = str(getattr(rule, "name", type(rule).__name__))
        names[name] += 1
        if index >= MAX_PREVIEW:
            continue
        children = []
        for child in premises[:12]:
            source_count = sum(
                link.step is not None
                and type(link.step.conclusion) is type(child)
                and link.step.conclusion == child
                for link in linked
            )
            children.append({
                "goal_type": type(child).__name__,
                "goal_repr": repr(child)[:900],
                "screened_exact_step_count": source_count,
            })
        examples.append({
            "rule": name, "subgoal_count": len(premises),
            "subgoals": children, "truncated_subgoals": len(premises) > 12,
        })
    return {
        "root_expansions": len(options),
        "distinct_rule_names": len(names),
        "rule_counts": dict(sorted(names.items())),
        "preview_count": len(examples),
        "preview": examples,
        "truncated_expansions": len(options) > MAX_PREVIEW,
        "root_is_verified_proof": False,
    }


def markdown_report(payload: dict) -> str:
    """Report observed source availability and proof-search proposals in Japanese."""
    lines = [
        "# Phase 171 R2D — π₆³ backward expansion frontier", "",
        "このレポートは source screening（出典の選別）と backward expansion（逆向き推論候補）の診断である。", "",
        "推論候補数は完成済み ProofStep 数ではない。", "",
        "## Screened Sources", "",
    ]
    for entry in payload["screened_sources"]:
        lines.append(
            f"{entry['locator']}：登録 {entry['registered_assertions']}件、"
            f"使用可能な照合済み GIVEN {entry['screened_given_links']}件。"
        )
    frontier = payload["frontier"]
    lines += [
        "", "## Root Goal", "",
        "引用の付いた Goal assertion：" + str(payload["citing_assertion_id"]),
        "選別した ProofStepLink 件数：" + str(payload["screened_link_total"]),
        "Root の逆向き推論候補：" + str(frontier["root_expansions"]),
        "候補の規則別件数：" + repr(frontier["rule_counts"]),
        "", "## 保留", "",
        "R2C の型付き不一致と Proposition 5.6 の root ProofStep 欠落は解決していない。",
        "原典の (5.6)? は未確認のままとする。DB の群構造を前提として採用しない。",
        "", "## 次 Phase との境界", "",
        "R2E 以降の導出規則の実装は、本監査で現れた不足前提の出典確認後に別途判断する。",
    ]
    return "\n".join(lines) + "\n"


def run(root: Path, report_path: Path, *, dry_run: bool) -> int:
    """Read saved R2C evidence, then inspect the actual screened search path."""
    before = tracked_state(root)
    source = json.loads(report_path.read_text(encoding="utf-8-sig"))
    validate_r2c(source)
    print("PHASE171_R2D_MODE=READ_ONLY_ROOT_EXPANSION", flush=True)
    print("PHASE171_R2D_TARGET=3,3", flush=True)
    if dry_run:
        if tracked_state(root) != before:
            raise RuntimeError("Git state changed during DryRun")
        print("PHASE171_R2D_DRY_RUN=PASS", flush=True)
        print("PHASE171_R2D_TRACKED_UNCHANGED=True", flush=True)
        print("PHASE171_R2D_RESULT=PASS", flush=True)
        return 0

    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=3)
    if len(goals) != 1:
        raise RuntimeError("expected exactly one typed pi_6^3 DB Goal")
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    else:
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing_id,
            explicit_publication_target=True,
        )
    screened = prefer_universal_prop42_derivation(screened)
    inventory = eligible_source_inventory(bridge, screened)
    provider = shared_expansion_provider(screened, proof_target=goal)
    frontier = root_expansion_inventory(goal, provider, screened)
    payload = {
        "phase": "171 R2D", "mode": "READ_ONLY_ROOT_EXPANSION", "read_only": True,
        "source_report": str(report_path), "git": before,
        "citing_assertion_id": citing_id,
        "target_repr": repr(goal)[:2400],
        "screened_link_total": len(screened.proof_links),
        "screened_sources": inventory,
        "frontier": frontier,
    }
    for item in inventory:
        print("PHASE171_R2D_SOURCE=" + json.dumps(item, ensure_ascii=False), flush=True)
    print("PHASE171_R2D_ROOT=" + json.dumps({
        "citing_assertion_id": citing_id,
        "screened_link_total": len(screened.proof_links),
        "root_expansions": frontier["root_expansions"],
        "distinct_rule_names": frontier["distinct_rule_names"],
        "rule_counts": frontier["rule_counts"],
        "preview_count": frontier["preview_count"],
    }, ensure_ascii=False), flush=True)
    for option in frontier["preview"][:8]:
        print("PHASE171_R2D_DETAIL=" + json.dumps(option, ensure_ascii=False), flush=True)
    if tracked_state(root) != before:
        raise RuntimeError("Git state changed during audit")
    payload["tracked_unchanged"] = True
    base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    directory = base / ("phase171_r2d_pi63_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    directory.mkdir(parents=True, exist_ok=False)
    output = directory / "frontier.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (directory / "frontier.md").write_text(markdown_report(payload), encoding="utf-8")
    print("PHASE171_R2D_REPORT=" + str(output), flush=True)
    print("PHASE171_R2D_TRACKED_UNCHANGED=True", flush=True)
    print("PHASE171_R2D_RESULT=PASS", flush=True)
    return 0


def main() -> int:
    """Run this audit from a module invocation at the repository root."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.root.resolve(), args.report.resolve(), dry_run=args.dry_run)
    except Exception as exc:
        print("PHASE171_R2D_ERROR=" + f"{type(exc).__name__}: {exc}", flush=True)
        print(traceback.format_exc()[-2800:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
