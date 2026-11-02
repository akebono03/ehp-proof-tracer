"""Read-only diagnosis of the actual accepted Toda (5.6) root premises.

No source claims, proof leaves, or group goals are promoted. The canonical
first-success search is run unchanged and the four real accepted ProofSteps
are matched against their already authored root InferenceRule.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
from typing import Any

REVIEWED_ANCESTOR = "f7184464fb299d22de7ee3f0579f0fc24cf3a008"
REVIEWED_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "sources/toda/Toda_04_2.tex": "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase173_r4_r1_source_bound_56/rule.py": "e05ada41cbcf53e8b755428afd245ba2da619fa8",
}
REVIEWED_UNTRACKED = {
    "phase173_r4_r1_lemma54_source_bridge/source.py":
        "88829b6d8a860d278a2890fa291d1d8102e6a210553fc31c72e4c8c172797d51",
    "phase173_r4_r1_lemma54_source_bridge/audit.py":
        "eeddbf95dec5bf25f69b6fc8f6e06fed486058771307f8ea654be8b59b84e6fa",
}


def _git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ("git", *arguments), cwd=root, capture_output=True,
        text=True, encoding="utf-8", check=True,
    ).stdout.strip()


def only_audit_additions(diff: str) -> tuple[str, ...]:
    """Permit only known-scope phase173 additions after the reviewed ancestor."""
    paths: list[str] = []
    for line in diff.splitlines():
        parts = line.split("\t")
        if len(parts) != 2:
            raise RuntimeError("Unrecognized committed change: " + repr(line))
        status, path = parts
        if (status != "A" or not path.startswith("phase173_")
                or "/" not in path or "\\" in path or ".." in Path(path).parts):
            raise RuntimeError("Non-audit committed change: " + repr(line))
        paths.append(path)
    return tuple(paths)


def guard_sources(root: Path) -> dict[str, Any]:
    """Require reviewed sources and an unchanged local tracked worktree."""
    if _git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Phase 173 R4-R1 requires develop")
    head = _git(root, "rev-parse", "HEAD")
    if head != _git(root, "rev-parse", "origin/develop"):
        raise RuntimeError("Local HEAD differs from origin/develop")
    test = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_ANCESTOR, head),
        cwd=root, capture_output=True, check=False,
    )
    if test.returncode != 0:
        raise RuntimeError("Unreviewed Git history")
    additions = only_audit_additions(
        _git(root, "diff", "--name-status", "--no-renames", REVIEWED_ANCESTOR, head)
    )
    for path, blob in REVIEWED_BLOBS.items():
        if _git(root, "rev-parse", "HEAD:" + path) != blob:
            raise RuntimeError("Reviewed production blob changed: " + path)
        for args in (("diff", "--quiet", "HEAD", "--", path),
                     ("diff", "--cached", "--quiet", "--", path)):
            test = subprocess.run(("git", *args), cwd=root,
                                  capture_output=True, check=False)
            if test.returncode != 0:
                raise RuntimeError("Production source differs from reviewed blob: " + path)
    for path, digest in REVIEWED_UNTRACKED.items():
        source = root / path
        if not source.is_file() or sha256(source.read_bytes()).hexdigest() != digest:
            raise RuntimeError("Reviewed Phase 173 package has changed: " + path)
    return {"head": head, "reviewed_blobs": list(REVIEWED_BLOBS),
            "reviewed_untracked": list(REVIEWED_UNTRACKED),
            "audit_only_new_commits": list(additions), "git_mutated": False}


def summarize_premise_states(states: tuple[str, ...], matches: int | None) -> str:
    """Distinguish missing accepted premises from matcher rejection."""
    if len(states) != 4:
        raise ValueError("Exactly four premise states are required")
    if any(s == "MISSING" for s in states):
        return "MISSING_ACCEPTED_PREMISE"
    if any(s == "WRONG_RULE" for s in states):
        return "WRONG_PROOF_RULE"
    if any(s == "AMBIGUOUS" for s in states):
        return "AMBIGUOUS_ACCEPTED_STEPS"
    if any(s != "ACCEPTED" for s in states):
        return "INVALID_PREMISE_STATE"
    if matches is None:
        return "NOT_MATCHED"
    if matches == 0:
        return "MATCHER_REJECTED_FOUR_ACCEPTED_PREMISES"
    if matches == 1:
        return "MATCHED_PROOF_NOT_COMPLETED"
    raise ValueError("Unexpected number of inference matches")


def inspect_runtime(root: Path) -> dict[str, Any]:
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56
    from phase173_r4_r1_lemma54_source_bridge.source import (
        ADOPTED_ASSERTION_ID, TodaLemma54TypedSource,
        add_verified_lemma54_source, canonical_hopf_relation,
        expand_cited_lemma54_hopf,
    )
    from proof import (
        ProofRule, apply_inference_match, find_inference_matches_for_rule,
        match_premise_pattern,
    )
    from unified_statement_registry import AssertionOrigin

    original = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(original, n=4, k=3)
    if len(goals) != 1:
        raise RuntimeError("Expected unique pi_7^4 registered goal")
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(original, goal)
    if citing_id is None:
        raise RuntimeError("Missing positioned pi_7^4 citing assertion")
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(encoding="utf-8-sig")
    augmented = add_verified_lemma54_source(
        original, citing_assertion_id=citing_id, chapter=chapter,
    )
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        augmented, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    ))
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )
    if sum(type(x) is TodaLemma54TypedSource for x in available) != 1:
        raise RuntimeError("No unique screened Lemma 5.4 typed source")
    if not any(link.assertion_id == ADOPTED_ASSERTION_ID for link in screened.proof_links):
        raise RuntimeError("Lemma 5.4 source disappeared under publication screen")

    def extra(statement: object):
        cited = expand_cited_lemma54_hopf(statement, available)
        if cited:
            return cited
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    root_proposals = expand_source_bound_toda56(
        goal, available, screened, proof_target=goal,
    )
    if len(root_proposals) != 1 or len(root_proposals[0].subgoals) != 4:
        raise RuntimeError("Expected exactly one four-premise Toda (5.6) root")
    root = root_proposals[0]
    provider = shared_expansion_provider(
        screened, extra_providers=(extra,), proof_target=goal,
    )
    result = search_shared_group_goal(
        n=4, k=3, group_structure=goal.rhs,
        bridge=augmented, citing_assertion_id=citing_id,
        expansion_provider=provider,
    )
    status = getattr(result.status, "value", str(result.status))
    steps = result.proven_steps
    chosen = []
    rows = []
    states: list[str] = []
    for index, (pattern, subgoal) in enumerate(zip(root.rule.premise_patterns, root.subgoals), 1):
        accepted = tuple(
            step for step in steps
            if type(step.conclusion) is type(subgoal) and step.conclusion == subgoal
        )
        if not accepted:
            state = "MISSING"
        elif len(accepted) > 1:
            state = "AMBIGUOUS"
        elif pattern.proof_rule is not None and accepted[0].rule is not pattern.proof_rule:
            state = "WRONG_RULE"
        else:
            state = "ACCEPTED"
        states.append(state)
        chosen.append(accepted[0] if len(accepted) == 1 else None)
        pattern_match = None
        if len(accepted) == 1:
            pattern_match = match_premise_pattern(pattern, accepted[0]) is not None
        rows.append({
            "index": index, "state": state, "accepted_count": len(accepted),
            "proof_rules": [step.rule.value for step in accepted],
            "proof_rule_names": [
                step.inference_rule.name if step.inference_rule is not None else "NONE"
                for step in accepted
            ],
            "premise_pattern_match": pattern_match,
            "expected_type": type(subgoal).__name__,
            "accepted_equal": bool(accepted) and accepted[0].conclusion == subgoal,
        })
    match_count = None
    guard_accepts = None
    conclusion_matches = None
    if all(x is not None for x in chosen):
        exact_steps = tuple(chosen)
        guard_accepts = bool(root.rule.match_guard(exact_steps, ()))
        matches = find_inference_matches_for_rule(root.rule, exact_steps)
        match_count = len(matches)
        if len(matches) == 1:
            conclusion_matches = apply_inference_match(matches[0]).conclusion == goal
    if result.status.value == "complete" and result.conclusion != goal:
        raise RuntimeError("Completed proof conclusion differs from requested goal")
    classification = summarize_premise_states(tuple(states), match_count)
    if status == "complete":
        classification = "COMPLETED_ROOT"
    return {
        "status": status, "complete": status == "complete",
        "goal": repr(goal), "source_bound_root_rule": root.rule.name,
        "accepted_proven_step_count": len(steps),
        "premises": rows, "root_match_count": match_count,
        "root_guard_accepts": guard_accepts,
        "root_application_matches_goal": conclusion_matches,
        "root_diagnosis": classification,
        "lemma54_hopf_proved_in_search": any(
            s.conclusion == canonical_hopf_relation() and s.rule is ProofRule.INFERENCE
            for s in steps
        ),
        "unresolved_goal_count": len(result.open_goals),
        "first_open_goals": [repr(x)[:600] for x in result.open_goals[:5]],
        "first_diagnostics": [str(x)[:600] for x in result.diagnostics[:5]],
        "production_changes": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 173 R4-R1 isolated root matcher audit")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    pre = guard_sources(root)
    print("PHASE173_R4_R1_ROOT_MATCH_SOURCE_GUARD=PASS")
    if args.dry_run:
        print("PHASE173_R4_R1_ROOT_MATCH_DRY_RUN=PASS")
        return 0
    observed = inspect_runtime(root)
    dest = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_root_match_probe/audit.json"
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({
        "phase": "173-R4-R1", "scope": "READ_ONLY_MATCH_DIAGNOSTIC",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "preflight": pre, "runtime": observed,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R1_ROOT_MATCH_AUDIT=PASS")
    print("PROOF_STATUS=" + observed["status"])
    print("LEMMA54_HOPF_PROVED=" + str(observed["lemma54_hopf_proved_in_search"]))
    for item in observed["premises"]:
        i = item["index"]
        print("PREMISE_" + str(i) + "_STATE=" + item["state"])
        print("PREMISE_" + str(i) + "_RULES=" + repr(item["proof_rules"]))
        print("PREMISE_" + str(i) + "_MATCH=" + str(item["premise_pattern_match"]))
    print("ROOT_GUARD_ACCEPTS=" + str(observed["root_guard_accepts"]))
    print("ROOT_MATCH_COUNT=" + str(observed["root_match_count"]))
    print("ROOT_APPLICATION_MATCHES_GOAL=" + str(observed["root_application_matches_goal"]))
    print("ROOT_DIAGNOSIS=" + observed["root_diagnosis"])
    print("AUDIT_JSON=" + str(dest))
    print("NO_PRODUCTION_CHANGES=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
