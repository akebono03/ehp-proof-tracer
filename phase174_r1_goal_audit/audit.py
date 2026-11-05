"""Phase 174 R1: read-only inspection of three public typed proof searches.

This program creates no mathematical claims, modifies no repository source,
and never promotes an unresolved goal or database record to a proof.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

TARGETS = ((5, 3), (4, 8), (4, 9))
PRIOR_OPEN_GOALS = {(5, 3): 3, (4, 8): 3, (4, 9): 2}
EXPECTED_HEAD = "cb85913905b2f7452bda2a2c4428e6fe5a3a793a"


def value_name(value: Any) -> str:
    return getattr(value, "value", str(value))


def statement_record(statement: object) -> dict[str, object]:
    record: dict[str, object] = {
        "type": type(statement).__name__,
        "module": type(statement).__module__,
        "repr": repr(statement),
    }
    for attribute in ("lhs", "rhs", "group", "conclusion", "source"):
        if hasattr(statement, attribute):
            value = getattr(statement, attribute)
            record[attribute] = {
                "type": type(value).__name__,
                "repr": repr(value),
            }
    return record


def step_record(step: object) -> dict[str, object]:
    rule = getattr(step, "rule", None)
    premises = tuple(getattr(step, "premises", ()))
    inference_rule = getattr(step, "inference_rule", None)
    return {
        "rule": value_name(rule),
        "conclusion": statement_record(getattr(step, "conclusion", None)),
        "premise_count": len(premises),
        "premises": [
            {
                "rule": value_name(getattr(premise, "rule", None)),
                "conclusion": statement_record(getattr(premise, "conclusion", None)),
            }
            for premise in premises
        ],
        "inference_rule_name": getattr(inference_rule, "name", None),
    }


def result_record(result: object) -> dict[str, object]:
    open_goals = tuple(getattr(result, "open_goals", ()))
    abstract = getattr(result, "abstract_structure", None)
    record: dict[str, object] = {
        "status": value_name(getattr(result, "status", None)),
        "structure_status": value_name(getattr(result, "structure_status", None)),
        "conclusion": (
            statement_record(result.conclusion)
            if getattr(result, "conclusion", None) is not None else None
        ),
        "open_goal_count": len(open_goals),
        "open_goals": [statement_record(goal) for goal in open_goals],
        "proven_step_count": len(getattr(result, "proven_steps", ())),
        "proven_steps": [
            step_record(step)
            for step in getattr(result, "proven_steps", ())
        ],
        "diagnostics": list(getattr(result, "diagnostics", ())),
        "references": list(getattr(result, "references", ())),
        "abstract_certificate": None,
    }
    if abstract is not None:
        record["abstract_certificate"] = {
            "group": statement_record(abstract.group),
            "invariant_summands": [
                list(summand) for summand in abstract.invariant_summands
            ],
            "proof_step": step_record(abstract.proof_step),
        }
    return record


def proposal_record(proposal: object) -> dict[str, object]:
    rule = getattr(proposal, "rule", None)
    subgoals = tuple(getattr(proposal, "subgoals", ()))
    return {
        "rule": getattr(rule, "name", str(rule)),
        "subgoal_count": len(subgoals),
        "subgoals": [statement_record(goal) for goal in subgoals],
    }


def probe_root_expansions(bridge: object, goal: object) -> dict[str, object]:
    """Inspect source-screened rule proposals without accepting them as proofs."""
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from proof import ProofRule

    citing = resolve_specialized_goal_citing_id(bridge, goal)
    if citing is None:
        return {
            "status": "NO_CITING_ASSERTION",
            "certifies_proof": False,
        }
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    given = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=goal)
    proposals = provider(goal)
    return {
        "status": "SOURCE_SCREENED_PROPOSALS_ONLY",
        "certifies_proof": False,
        "screened_given_count": len(given),
        "target_given_count": sum(
            type(claim) is type(goal) and claim == goal for claim in given
        ),
        "root_proposal_count": len(proposals),
        "inspected_proposal_count": min(len(proposals), 12),
        "inspected_proposals": [
            proposal_record(proposal) for proposal in proposals[:12]
        ],
    }


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], check=True, capture_output=True,
        encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def output_path() -> Path:
    directory = Path(
        os.environ.get("LOCALAPPDATA", tempfile.gettempdir())
    ) / "EHPProofTracerAudit" / "phase174_r1"
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "audit.json"


def audit_targets() -> dict[str, object]:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import (
        registered_group_goal_candidates,
        search_group_from_registered_goal,
    )
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from phase165_r52_partial_proof import PartialProofResult

    bridge = build_shared_typed_bridge()
    rows: list[dict[str, object]] = []
    for n, k in TARGETS:
        row: dict[str, object] = {
            "n": n,
            "k": k,
            "group": f"pi_{n+k}^{n}",
            "previous_open_goal_count": PRIOR_OPEN_GOALS[(n, k)],
            "route": "search_group_from_registered_goal",
            "runtime_error": None,
        }
        try:
            candidates = registered_group_goal_candidates(
                bridge, n=n, k=k,
            )
            row["candidate_count"] = len(candidates)
            row["candidates"] = [
                statement_record(goal) for goal in candidates
            ]
            row["candidate_sources"] = []
            row["root_proposal_probes"] = []
            for goal in candidates:
                citing_id = resolve_specialized_goal_citing_id(bridge, goal)
                source: dict[str, object] = {
                    "citing_assertion_id": citing_id,
                }
                if citing_id is not None:
                    assertion = bridge.registry.assertion(citing_id)
                    source["assertion_origin"] = value_name(assertion.origin)
                    source["reference_id"] = str(assertion.reference_id)
                    source["reference_locator"] = repr(
                        bridge.registry.reference(assertion.reference_id).locator
                    )
                row["candidate_sources"].append(source)
                try:
                    row["root_proposal_probes"].append(
                        probe_root_expansions(bridge, goal)
                    )
                except Exception as exc:
                    row["root_proposal_probes"].append({
                        "status": "PROBE_FAILED_NOT_A_PROOF_RESULT",
                        "certifies_proof": False,
                        "error": f"{type(exc).__name__}: {exc}",
                    })

            result = search_group_from_registered_goal(
                n=n, k=k, bridge=bridge,
            )
            if not isinstance(result, PartialProofResult):
                raise TypeError("Unexpected public result type")
            row["result"] = result_record(result)
            print(
                "PHASE174_R1_GROUP={0} STATUS={1} OPEN={2} ABSTRACT={3} STEPS={4}".format(
                    row["group"], row["result"]["status"],
                    row["result"]["open_goal_count"],
                    row["result"]["abstract_certificate"] is not None,
                    row["result"]["proven_step_count"],
                )
            )
        except Exception as exc:
            row["runtime_error"] = {
                "type": type(exc).__name__,
                "message": str(exc),
            }
            print(
                f"PHASE174_R1_GROUP={row['group']} ERROR={type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
        rows.append(row)
    return {
        "phase": "174-R1",
        "mode": "READ_ONLY",
        "reviewed_github_develop_head": EXPECTED_HEAD,
        "local_head": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
        "target_count": len(rows),
        "rows": rows,
        "proofs_inferred_by_audit": False,
        "source_or_test_files_modified_by_audit": False,
        "full_pytest_performed": False,
    }


def main() -> int:
    local_head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    if branch != "develop" or local_head != EXPECTED_HEAD:
        print(
            f"PHASE174_R1_PREFLIGHT_FAILED BRANCH={branch} HEAD={local_head}",
            file=sys.stderr,
        )
        return 2
    result = audit_targets()
    path = output_path()
    path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"PHASE174_R1_REPORT={path}")
    if any(row["runtime_error"] is not None for row in result["rows"]):
        print("PHASE174_R1_AUDIT_GATE=ERROR")
        return 1
    print("PHASE174_R1_AUDIT_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
