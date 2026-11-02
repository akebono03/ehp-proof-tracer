"""Isolated publication-screened proof search for Toda Lemma 5.4 -> (5.6)."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
from typing import Any

REVIEWED_ANCESTOR = "cc1b206f787986dccc659cc9a5982bea3bb05d50"
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


def git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ("git", *arguments), cwd=root,
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return completed.stdout.strip()


def validate_audit_additions(changes: str) -> tuple[str, ...]:
    """Reject modifications to any committed file after reviewed ancestor."""
    paths = []
    for record in changes.splitlines():
        fields = record.split("\t")
        if len(fields) != 2:
            raise RuntimeError("Unexpected commit status: " + repr(record))
        status, path = fields
        if (status != "A" or not path.startswith("phase173_")
                or "/" not in path or "\\" in path or ".." in Path(path).parts):
            raise RuntimeError("Non-audit committed change: " + repr(record))
        paths.append(path)
    return tuple(paths)


def guard_sources(root: Path) -> dict[str, Any]:
    """Check reviewed production content and require audit-only intervening commits."""
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only the reviewed develop branch is supported")
    head = git(root, "rev-parse", "HEAD")
    if head != git(root, "rev-parse", "origin/develop"):
        raise RuntimeError("Local develop differs from origin/develop")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_ANCESTOR, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("Unreviewed Git history")
    additions = validate_audit_additions(
        git(root, "diff", "--name-status", "--no-renames", REVIEWED_ANCESTOR, head)
    )
    for path, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("Reviewed blob changed: " + path)
        for arguments in (("diff", "--quiet", "--", path),
                          ("diff", "--cached", "--quiet", "--", path)):
            checked = subprocess.run(("git", *arguments), cwd=root,
                                     capture_output=True, check=False)
            if checked.returncode != 0:
                raise RuntimeError("Reviewed working source changed: " + path)
    return {"head": head, "added_audit_files": list(additions),
            "reviewed_sources": sorted(REVIEWED_BLOBS), "no_git_mutation": True}


def collect_ancestry(root: object) -> tuple[object, ...]:
    """Flatten only real ProofStep ancestry, avoiding repeated shared nodes."""
    from proof import ProofStep
    if not isinstance(root, ProofStep):
        return ()
    visited: set[int] = set()
    sequence: list[ProofStep] = []

    def visit(node: ProofStep) -> None:
        if id(node) in visited:
            return
        visited.add(id(node))
        sequence.append(node)
        for parent in node.premises:
            visit(parent)

    visit(root)
    return tuple(sequence)


def inspect_runtime(root: Path) -> dict[str, Any]:
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3c_publication_order import precedes_citing_assertion
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56
    from phase173_r4_r1_lemma54_source_bridge.source import (
        ADOPTED_ASSERTION_ID, TodaLemma54TypedSource,
        add_verified_lemma54_source, canonical_hopf_relation,
        expand_cited_lemma54_hopf,
    )
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    original = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(original, n=4, k=3)
    if len(candidates) != 1:
        raise RuntimeError("pi_7^4 requires exactly one typed target goal")
    goal = candidates[0]
    citing_id = resolve_specialized_goal_citing_id(original, goal)
    if citing_id is None:
        raise RuntimeError("pi_7^4 lacks a unique source publication position")
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig"
    )
    augmented = add_verified_lemma54_source(
        original, citing_assertion_id=citing_id, chapter=chapter,
    )
    if not precedes_citing_assertion(augmented, ADOPTED_ASSERTION_ID, citing_id):
        raise RuntimeError("Lemma 5.4 is not positioned before the goal")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        augmented, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    ))
    matching_links = tuple(
        link for link in screened.proof_links
        if link.assertion_id == ADOPTED_ASSERTION_ID
        and link.step is not None and link.step.rule is ProofRule.GIVEN
        and type(link.step.conclusion) is TodaLemma54TypedSource
    )
    if len(matching_links) != 1:
        raise RuntimeError("Lemma 5.4 is not uniquely citation-screened")
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )

    def extra(statement: object):
        candidates = expand_cited_lemma54_hopf(statement, available)
        if candidates:
            return candidates
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    provider = shared_expansion_provider(
        screened, extra_providers=(extra,), proof_target=goal,
    )
    hopf = canonical_hopf_relation()
    hopf_candidates = provider(hopf)
    goal_candidates = provider(goal)
    result = search_shared_group_goal(
        n=4, k=3, group_structure=goal.rhs,
        bridge=augmented, citing_assertion_id=citing_id,
        expansion_provider=provider,
    )
    status = getattr(result.status, "value", str(result.status))
    final_steps = [
        step for step in result.proven_steps
        if step.conclusion == goal and step.rule is ProofRule.INFERENCE
    ]
    if status == "complete" and (result.conclusion != goal or not final_steps):
        raise RuntimeError("Uncertified completion must not be accepted")
    final = final_steps[-1] if final_steps else None
    ancestry = collect_ancestry(final)
    source_present = any(
        step.rule is ProofRule.GIVEN and type(step.conclusion) is TodaLemma54TypedSource
        for step in ancestry
    )
    hopf_present = any(
        step.rule is ProofRule.INFERENCE and step.conclusion == hopf
        for step in ancestry
    )
    certified = status == "complete" and source_present and hopf_present
    if status == "complete" and not certified:
        raise RuntimeError("Complete result lacks cited Lemma 5.4 Hopf ancestry")
    return {
        "goal": repr(goal), "citing_id": citing_id,
        "citation_screened_lemma54_count": len(matching_links),
        "direct_hopf_given_count": sum(
            type(x) is type(hopf) and x == hopf for x in available
        ),
        "hopf_proposal_names": [x.rule.name for x in hopf_candidates],
        "root_proposal_names": [x.rule.name for x in goal_candidates],
        "status": status, "complete": status == "complete",
        "complete_and_source_certified": certified,
        "source_in_final_proof_ancestry": source_present,
        "hopf_in_final_proof_ancestry": hopf_present,
        "proven_step_count": len(result.proven_steps),
        "open_goals": [repr(x)[:700] for x in result.open_goals[:15]],
        "diagnostics": [str(x)[:700] for x in result.diagnostics[:15]],
        "publication_position_preserved": True,
        "production_changes": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase173 R4-R1 isolated cited Lemma 5.4 proof")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    check = guard_sources(root)
    print("PHASE173_R4_R1_LEMMA54_SOURCE_GUARD=PASS")
    if args.dry_run:
        print("PHASE173_R4_R1_LEMMA54_DRY_RUN=PASS")
        return 0
    result = inspect_runtime(root)
    destination = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_lemma54_source_bridge/audit.json"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps({
        "phase": "173-R4-R1", "scope": "ISOLATED_TYPED_CITED_LEMMA54",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "preflight": check, "runtime": result, "production_changes": [],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("LEMMA54_SCREENED_SOURCE=" + str(result["citation_screened_lemma54_count"]))
    print("LEMMA54_DIRECT_HOPF_GIVEN=" + str(result["direct_hopf_given_count"]))
    print("LEMMA54_HOPF_PROPOSALS=" + repr(result["hopf_proposal_names"]))
    print("TODA56_ROOT_PROPOSALS=" + repr(result["root_proposal_names"]))
    print("PHASE173_R4_R1_PROOF_STATUS=" + str(result["status"]))
    print("PHASE173_R4_R1_COMPLETE=" + str(result["complete"]))
    print("PHASE173_R4_R1_SOURCE_CERTIFIED=" + str(result["complete_and_source_certified"]))
    print("PHASE173_R4_R1_OPEN_GOALS=" + repr(result["open_goals"]))
    print("PHASE173_R4_R1_REPORT=" + str(destination))
    print("PHASE173_R4_R1_NO_PRODUCTION_CHANGES=True")
    print("PHASE173_R4_R1_LEMMA54_AUDIT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
