"""Review Phase 173 R3 root expansions without changing mathematical proofs.

Accept a descendant of the reviewed baseline only when every committed change
since that baseline is an added Phase 173 audit file, and the reviewed source
blobs remain identical. R1 history is optional across Windows profiles.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
from typing import Any

BASELINE = "11ea331f322883e2f2cf34b9e865dea2134f5058"
REVIEWED_BLOBS = {
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}
TARGETS = ((4, 3), (5, 3))


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8",
        capture_output=True, check=True,
    )
    return result.stdout.strip()


def verify_committed_changes(diff_text: str) -> tuple[str, ...]:
    """Accept only newly added files below Phase 173 audit directories."""
    paths = []
    for line in diff_text.splitlines():
        fields = line.split("\t")
        if len(fields) != 2:
            raise RuntimeError("Unrecognized Git name-status entry: " + repr(line))
        status, name = fields
        if status != "A" or not name.startswith("phase173_") or "/" not in name:
            raise RuntimeError("Reviewed production scope changed: " + repr(line))
        if ".." in Path(name).parts or "\\" in name:
            raise RuntimeError("Invalid audit path: " + repr(name))
        paths.append(name)
    return tuple(paths)


def preflight(root: Path) -> dict[str, Any]:
    """Validate lineage, reviewed content, publication source, and clean files."""
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3 requires develop")
    head = git(root, "rev-parse", "HEAD")
    if git(root, "rev-parse", "origin/develop") != head:
        raise RuntimeError("Local HEAD is not origin/develop; inspect git status")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASELINE, head],
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("Reviewed baseline is not an ancestor of HEAD")
    changes = verify_committed_changes(
        git(root, "diff", "--name-status", "--no-renames", BASELINE, head)
    )
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("Tracked worktree must be clean")
    for name, sha in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + name) != sha:
            raise RuntimeError("Reviewed source content changed: " + name)
    source = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig"
    )
    anchor = r"\begin{proposition}\label{prop:5.6}"
    begin = source.index(anchor)
    finish = source.index(r"\end{proposition}", begin)
    excerpt = source[begin:finish]
    for fragment in (r"\pi^{4}_{7}", r"\pi^{n}_{n+3}", r"\nu'"):
        if fragment not in excerpt:
            raise RuntimeError("Proposition 5.6 source text differs")
    return {"head": head, "reviewed_baseline": BASELINE,
            "committed_audit_additions": list(changes),
            "reviewed_source_blobs": dict(REVIEWED_BLOBS)}


def r1_baseline_status(local_appdata: Path) -> str:
    """Cross-check locally available R1 reports; absence is not a proof fact."""
    directory = local_appdata / "EHPProofTracerRecovery"
    reports = sorted(
        directory.glob("phase173_r1_*/audit.json"),
        key=lambda path: path.stat().st_mtime, reverse=True,
    ) if directory.is_dir() else []
    for path in reports:
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        rows = data.get("rows")
        if not isinstance(rows, list):
            continue
        observed = {(row.get("n"), row.get("k")): row for row in rows
                    if isinstance(row, dict)}
        if all(pair in observed for pair in TARGETS):
            for pair in TARGETS:
                if observed[pair].get("audit_result") != "PROOF_UNFINISHED":
                    raise RuntimeError("R1 local baseline disagrees: " + str(pair))
            return "MATCHED:" + str(path)
    return "NOT_AVAILABLE_IN_THIS_PROFILE"


def inspect_roots() -> list[dict[str, Any]]:
    """Inspect already registered proof proposals, never certify them."""
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from phase169_r3m_prior_result_catalog.prior_results import (
        resolve_prior_group_result,
    )
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    rows = []
    for n, k in TARGETS:
        goals = registered_group_goal_candidates(bridge, n=n, k=k)
        if len(goals) != 1:
            raise RuntimeError(f"n={n} k={k}: expected one typed goal, found {len(goals)}")
        goal = goals[0]
        citing = resolve_specialized_goal_citing_id(bridge, goal)
        if citing is None:
            raise RuntimeError(f"n={n} k={k}: source position missing")
        assertion = bridge.registry.assertion(citing)
        locator = bridge.registry.reference(assertion.reference_id).locator
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing,
            explicit_publication_target=True,
        )
        screened = prefer_universal_prop42_derivation(screened)
        given = tuple(
            link.step.conclusion for link in screened.proof_links
            if link.step is not None and link.step.rule is ProofRule.GIVEN
        )
        if any(type(statement) is type(goal) and statement == goal for statement in given):
            raise RuntimeError("Target was admitted as GIVEN")
        provider = shared_expansion_provider(screened, proof_target=goal)
        options = provider(goal)
        roots = []
        memo: list[object] = []
        for option in options:
            children = []
            for child in option.subgoals:
                item = {"type": type(child).__name__, "repr": repr(child)[:1600]}
                is_new = not any(type(old) is type(child) and old == child for old in memo)
                if is_new:
                    memo.append(child)
                    item["exact_screened_given"] = any(
                        type(source) is type(child) and source == child for source in given
                    )
                    try:
                        proposals = provider(child)
                        item["child_proposal_count"] = len(proposals)
                        item["child_proposal_rules"] = [p.rule.name for p in proposals]
                    except Exception as exc:
                        item["child_probe_error"] = type(exc).__name__ + ": " + str(exc)
                else:
                    item["duplicate_subgoal"] = True
                children.append(item)
            roots.append({"rule": option.rule.name, "children": children})
        prior = []
        for earlier_n in range(3, n):
            source = resolve_prior_group_result(
                screened, source_n=earlier_n, source_k=k,
                citing_assertion_id=citing,
            )
            prior.append({"n": earlier_n, "k": k, "eligible": source.eligible,
                          "reason": source.reason, "stable_source": earlier_n >= k + 2})
        rows.append({"n": n, "k": k, "source_locator": locator,
                     "citing_assertion_id": citing,
                     "screened_given_count": len(given),
                     "target_direct_given_count": 0,
                     "root_candidate_count": len(roots),
                     "roots": roots, "prior_sources": prior})
    return rows


def format_report(rows: list[dict[str, Any]]) -> str:
    output = ["PHASE173_R3_PORTABLE_FRONTIER=AUDIT_ONLY"]
    for row in rows:
        output.append("R3 n=%d k=%d locator=%s GIVEN=%d roots=%d" % (
            row["n"], row["k"], row["source_locator"],
            row["screened_given_count"], row["root_candidate_count"],
        ))
        for index, root in enumerate(row["roots"], start=1):
            output.append("  ROOT %d rule=%s" % (index, root["rule"]))
            for child in root["children"]:
                output.append("    SUBGOAL %s proposals=%s exact_given=%s" % (
                    child["type"], child.get("child_proposal_count", "DUPLICATE"),
                    child.get("exact_screened_given", "DUPLICATE"),
                ))
                for name in child.get("child_proposal_rules", []):
                    output.append("      CANDIDATE_RULE " + name)
                if "child_probe_error" in child:
                    output.append("      PROBE_ERROR " + child["child_probe_error"])
                output.append("      STATEMENT " + child["repr"][:650])
        for prior in row["prior_sources"]:
            output.append("  PRIOR n=%d eligible=%s reason=%s" % (
                prior["n"], prior["eligible"], prior["reason"],
            ))
    output.append("PHASE173_R3_PORTABLE_FRONTIER=PASS")
    output.append("OBSERVATION_IS_NOT_A_PROOF=True")
    return "\n".join(output)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only R3 source and root audit")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    state = preflight(root)
    print("PHASE173_R3_HEAD_REVIEW=PASS")
    print("PHASE173_R3_REVIEWED_SOURCE_BLOBS=PASS")
    print("PHASE173_R3_CURRENT_HEAD=" + state["head"])
    if args.dry_run:
        print("PHASE173_R3_DRY_RUN=PASS")
        return 0
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        raise RuntimeError("LOCALAPPDATA not set")
    baseline_state = r1_baseline_status(Path(local_appdata))
    print("PHASE173_R3_R1_LOCAL_BASELINE=" + baseline_state)
    rows = inspect_roots()
    report = {"phase": "173-R3", "mode": "AUDIT_ONLY",
              "observations_are_not_proofs": True,
              "r1_local_baseline": baseline_state, **state, "rows": rows}
    out = Path(local_appdata) / "EHPProofTracerRecovery" / "phase173_r3_portable"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "audit.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    markdown = format_report(rows)
    (out / "audit.md").write_text(markdown + "\n", encoding="utf-8")
    print(markdown)
    print("PHASE173_R3_REPORT=" + str(json_path))
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("Tracked files changed during R3")
    print("PHASE173_R3_TRACKED_UNCHANGED=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
