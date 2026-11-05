"""Phase 174 R3-R7: read-only source-first audit of unresolved typed goals.

This module neither adds inference rules nor registers source or group GIVENs.
A source-screened expansion is a candidate, NOT a verified proof step.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7"
PRIOR_HEAD = "f2e148afefb11eb0b0ca31da67c65ec1ffe9e1e9"
REVIEWED_HEAD = "1a6a5a57992963c7a21aa22079a145a310b4e0ed"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "sources/toda/Toda_06_2.tex": "76934583cff01c8ea83f768e26947eb9b556653b",
    "sources/toda/Toda_07_2.tex": "b5b366f2d2b72d7b419192fa74ab848eff098686",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
    "phase174_r3_r6_source_extension/source.py": "9cd5cd0dd3f8e7a798a8e0006480785b0c67a1bb",
}
HISTORICAL_REPORT = (
    "phase173_r4_r15r12r3_all_n4_status_audit/all_n4_status_report.json"
)
# These are diagnostic probes, not a predetermined implementation target.
# (3,8), (7,5) are the premises of the Chapter VII / Toda (5.6) route;
# (3,9), (7,6) are the corresponding next-stem premises.
TARGETS = ((5, 3), (4, 8), (4, 9), (3, 8), (7, 5), (3, 9), (7, 6))


def git(*args: str, cwd: Path = ROOT) -> str:
    process = subprocess.run(
        ("git",) + args,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return process.stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\x00" + data
    ).hexdigest()


def accepted_blob(data: bytes, expected_sha: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    variants = (data, normalized, normalized.replace(b"\n", b"\r\n"))
    return any(git_blob(candidate) == expected_sha for candidate in variants)


def verify_git_state(root: Path = ROOT) -> dict[str, Any]:
    repo_root = Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve()
    if repo_root != root.resolve():
        raise RuntimeError("The audit directory must be directly under the repository root")
    branch = git("branch", "--show-current", cwd=root)
    local = git("rev-parse", "HEAD", cwd=root)
    remote_lines = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    if not remote_lines:
        raise RuntimeError("origin/develop is unavailable; live GitHub verification required")
    remote = remote_lines.split()[0]
    if branch != "develop":
        raise RuntimeError("Expected the develop branch; no checkout will be attempted")
    if remote != REVIEWED_HEAD:
        raise RuntimeError("develop has changed; review the new remote HEAD before continuing")
    if local not in (PRIOR_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local HEAD is outside the two reviewed audit baselines")
    changed = git("status", "--porcelain=v1", "--untracked-files=normal", cwd=root)
    staged = git("diff", "--cached", "--name-only", cwd=root)
    return {
        "branch": branch,
        "local_head": local,
        "reviewed_remote_head": remote,
        "local_equals_remote": local == remote,
        "requires_local_reconciliation_before_implementation": local != remote,
        "tracked_and_untracked_status": changed.splitlines() if changed else [],
        "staged_file_paths": staged.splitlines() if staged else [],
        "does_not_clean_or_apply_changes": True,
    }


def verify_math_sources(root: Path = ROOT) -> dict[str, Any]:
    for relative_path, expected in SOURCE_BLOBS.items():
        path = root / relative_path
        if not path.is_file() or not accepted_blob(path.read_bytes(), expected):
            raise RuntimeError("An audited source or proof provider differs: " + relative_path)
    toda5 = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    toda6 = (root / "sources/toda/Toda_06_2.tex").read_text(encoding="utf-8-sig")
    toda7 = (root / "sources/toda/Toda_07_2.tex").read_text(encoding="utf-8-sig")
    clauses = {
        "toda56_general_isomorphism": (
            toda5,
            r"\pi^{\,3}_{i-1}\oplus \pi^{\,7}_{i}",
        ),
        "toda56_generator_image": (
            toda5,
            r"E\alpha+\nu_{4}\circ\beta",
        ),
        "lemma61_hopf_invariant": (
            toda6,
            r"H(\varepsilon_3)=\nu_5^{\,2}",
        ),
        "lemma61_two_torsion": (
            toda6,
            r"2\varepsilon_n=2\varepsilon=0",
        ),
        "theorem71_n3_n4_n5": (
            toda7,
            r"\pit{n+8}{n}=\gen{\varepsilon_{n}}\cong\mathbb Z_{2}",
        ),
        "theorem71_pi124_proof_route": (
            toda7,
            r"\pit{12}{4}=\gen{\varepsilon_{4}}\cong\mathbb Z_{2}",
        ),
        "chapter7_pi124_premise_decomposition": (
            toda7,
            r"(5.6) と Prop5.9 より",
        ),
    }
    missing = [name for name, (text, fragment) in clauses.items() if fragment not in text]
    if missing:
        raise RuntimeError("Reviewed Toda clauses changed: " + ", ".join(missing))
    return {
        "source_blobs": dict(SOURCE_BLOBS),
        "source_clauses": {name: True for name in clauses},
        "original_print_edition_independently_verified": False,
        "source_transcriptions_not_direct_target_given": True,
        "hypotheses_and_generator_images_still_require_typed_proofs": True,
    }


def historical_n4_status(root: Path = ROOT) -> dict[str, Any]:
    path = root / HISTORICAL_REPORT
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    summary = data.get("summary", {})
    rows = data.get("rows", [])
    by_k = {row["k"]: row for row in rows if row.get("n") == 4}
    if len(by_k) != 33 or 8 not in by_k or 9 not in by_k:
        raise RuntimeError("Historical Phase 173 report is missing required rows")
    return {
        "source_file": HISTORICAL_REPORT,
        "recorded_head": data.get("head_reviewed"),
        "historical_only_not_new_live_evidence": True,
        "registered_n4": summary.get("all_registered_groups"),
        "historical_category_counts": summary.get("all_status_counts"),
        "named_pending_k_ge_8": summary.get("k_ge_8_abstract_only"),
        "selected_frontiers": {
            str(k): {
                "search_status": by_k[k].get("search_status"),
                "category": by_k[k].get("category"),
                "open_goal_types": by_k[k].get("open_goal_types"),
                "proven_steps": by_k[k].get("proven_steps"),
            }
            for k in (8, 9)
        },
    }


def statement_description(value: object, *, limit: int = 480) -> dict[str, str]:
    text = repr(value).replace("\r", " ").replace("\n", " ")
    if len(text) > limit:
        text = text[:limit] + " [truncated for diagnostics]"
    return {"type": type(value).__name__, "repr": text}


def is_exact_given(statement: object, admitted: tuple[object, ...]) -> bool:
    return any(type(statement) is type(candidate) and statement == candidate for candidate in admitted)


def summarize_proposals(
    provider: object,
    goal: object,
    admitted: tuple[object, ...],
    *,
    limit: int = 8,
) -> dict[str, Any]:
    from phase165_r3_recursive_search import SourceBoundGoal

    actual_goal = goal.conclusion if isinstance(goal, SourceBoundGoal) else goal
    proposals = provider(actual_goal)
    if not isinstance(proposals, tuple):
        raise TypeError("Production expansion provider must return a tuple")
    records: list[dict[str, Any]] = []
    for option in proposals[:limit]:
        children = option.subgoals
        if not isinstance(children, tuple):
            raise TypeError("Production expansion subgoals must be a tuple")
        records.append({
            "rule": getattr(option.rule, "name", None),
            "child_count": len(children),
            "children": [
                {
                    "statement": statement_description(
                        child.conclusion if isinstance(child, SourceBoundGoal) else child
                    ),
                    "is_exact_screened_given": is_exact_given(
                        child.conclusion if isinstance(child, SourceBoundGoal) else child,
                        admitted,
                    ),
                    "is_source_bound_wrapper": isinstance(child, SourceBoundGoal),
                }
                for child in children
            ],
        })
    return {
        "goal": statement_description(actual_goal),
        "proposal_count": len(proposals),
        "shown_proposal_count": len(records),
        "proposals": records,
        "verified_proof_steps_created_by_probe": 0,
    }


def source_screened_frontier(bridge: object, goal: object, open_goals: tuple) -> dict[str, Any]:
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from proof import ProofRule

    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
        screening = "source_first_independent"
    else:
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing_id,
            explicit_publication_target=True,
        )
        screening = "publication_screened"
    screened = prefer_universal_prop42_derivation(screened)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if is_exact_given(goal, admitted):
        raise RuntimeError("The target itself is a direct screened GIVEN")
    provider = shared_expansion_provider(screened, proof_target=goal)
    return {
        "screening_mode": screening,
        "citing_assertion_id": citing_id,
        "admitted_given_count": len(admitted),
        "target_direct_given_count": 0,
        "root": summarize_proposals(provider, goal, admitted),
        "open_goal_frontier": [
            summarize_proposals(provider, item, admitted, limit=6)
            for item in open_goals[:4]
        ],
    }


def inspect_live_selected_targets() -> list[dict[str, Any]]:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import (
        registered_group_goal_candidates,
        search_group_from_registered_goal,
    )

    bridge = build_shared_typed_bridge()
    results: list[dict[str, Any]] = []
    for n, k in TARGETS:
        row: dict[str, Any] = {
            "n": n, "k": k, "group": f"pi_{n+k}^{n}",
            "historical_or_db_statement_is_not_a_proof": True,
            "search_error": None,
            "frontier_error": None,
        }
        print(f"PHASE174_R3R7_LIVE_START={row['group']}", flush=True)
        candidates = registered_group_goal_candidates(bridge, n=n, k=k)
        row["typed_registered_relation_count"] = len(candidates)
        row["typed_registered_relation_samples"] = [
            statement_description(item) for item in candidates[:2]
        ]
        try:
            result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
            row["status"] = getattr(result.status, "value", str(result.status))
            row["conclusion_present"] = result.conclusion is not None
            row["proven_step_count"] = len(result.proven_steps)
            row["open_goal_count"] = len(result.open_goals)
            row["open_goals"] = [statement_description(x) for x in result.open_goals]
            row["abstract_structure_present"] = result.abstract_structure is not None
            row["diagnostics"] = [str(x)[:500] for x in result.diagnostics[:4]]
        except Exception as error:
            row["search_error"] = f"{type(error).__name__}: {error}"
            results.append(row)
            continue
        if len(candidates) == 1:
            try:
                row["source_screened_frontier"] = source_screened_frontier(
                    bridge, candidates[0], tuple(result.open_goals),
                )
            except Exception as error:
                row["frontier_error"] = f"{type(error).__name__}: {error}"
        else:
            row["source_screened_frontier"] = {
                "reason": "Zero or multiple typed Relation roots; no unchecked root selected",
                "direct_given_registered": False,
            }
        print(
            f"PHASE174_R3R7_LIVE_GROUP={row['group']} STATUS={row['status']} "
            f"STEPS={row['proven_step_count']} OPEN={row['open_goal_count']}",
            flush=True,
        )
        results.append(row)
    return results


def report_location() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7" / "audit.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_state(root)
    sources = verify_math_sources(root)
    history = historical_n4_status(root)
    rows = [] if dry_run else inspect_live_selected_targets()
    pi85 = next((row for row in rows if (row["n"], row["k"]) == (5, 3)), None)
    baseline_complete = bool(
        pi85 is not None and pi85.get("status") == "complete"
        and pi85.get("proven_step_count") == 16
        and pi85.get("open_goal_count") == 0
    )
    live_errors = [
        {"group": row["group"], "search": row.get("search_error"),
         "frontier": row.get("frontier_error")}
        for row in rows
        if row.get("search_error") or row.get("frontier_error")
    ]
    return {
        "phase": PHASE,
        "mode": "READ_ONLY_DRY_RUN" if dry_run else "READ_ONLY_SOURCE_FIRST_LIVE",
        "git_state": state,
        "source_review": sources,
        "phase173_historical_frontier": history,
        "selected_target_count": len(rows),
        "selected_targets": rows,
        "pi85_previous_completed_proof_preserved": (
            "NOT_EXECUTED" if dry_run else baseline_complete
        ),
        "runtime_errors": live_errors,
        "new_group_given": 0,
        "new_inference_rules": 0,
        "new_proof_steps_by_audit": 0,
        "production_files_edited_by_audit": False,
        "full_pytest_run": False,
        "implementation_candidate_approved": False,
        "audit_gate": (
            "PASS_PREFLIGHT" if dry_run else
            "PASS_READ_ONLY" if baseline_complete and not live_errors else "NEEDS_REVIEW"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    report = make_report(dry_run=arguments.dry_run)
    destination = report_location()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PHASE174_R3R7_REMOTE_HEAD=" + report["git_state"]["reviewed_remote_head"])
    print("PHASE174_R3R7_LOCAL_HEAD=" + report["git_state"]["local_head"])
    print("PHASE174_R3R7_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7_HISTORICAL_N4_REGISTERED=" + str(
        report["phase173_historical_frontier"]["registered_n4"]
    ))
    print("PHASE174_R3R7_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R7_NEW_RULES=0")
    print("PHASE174_R3R7_FULL_PYTEST=False")
    print("PHASE174_R3R7_REPORT=" + str(destination))
    print("PHASE174_R3R7_AUDIT_GATE=" + report["audit_gate"])
    return 0 if report["audit_gate"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
