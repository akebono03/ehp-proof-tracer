"""Phase 165 R12-R4: read-only pi_4^3 canonical-search audit."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from expression import eta
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType


def target_goal() -> Relation:
    return Relation(
        lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3),
        rhs=FiniteCyclicGroup(order=2, generator=eta(3)),
        relation_type=RelationType.EQUALITY,
    )


def run_worker() -> dict:
    from phase165_r52_r9_shared_math import search_shared_group_goal
    from phase165_r52_partial_proof import ProofSearchStatus

    result = search_shared_group_goal(
        n=3,
        k=1,
        group_structure=target_goal().rhs,
    )
    status = result.status.value
    complete = result.status is ProofSearchStatus.COMPLETE
    conclusion_is_target = complete and result.conclusion == target_goal()
    if complete and not conclusion_is_target:
        raise AssertionError("completed result does not match requested pi43 goal")
    return {
        "search_status": status,
        "target_pi43_proof_certified": bool(conclusion_is_target),
        "proven_step_count": len(result.proven_steps),
        "open_goal_count": len(result.open_goals),
        "open_goals": [repr(item) for item in result.open_goals[:25]],
        "open_goals_truncated": len(result.open_goals) > 25,
        "diagnostics": list(result.diagnostics),
        "root_conclusion": repr(result.conclusion) if complete else None,
        "observed_rule_names": sorted({
            step.inference_rule.name
            for step in result.proven_steps
            if step.inference_rule is not None
        }),
    }



def decode_worker_output(data: bytes) -> str:
    """Decode worker pipe bytes without breaking the audit on Windows."""
    if not isinstance(data, bytes):
        raise TypeError("worker output must be bytes")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return data.decode("cp932")
        except UnicodeDecodeError:
            return data.decode("utf-8", errors="replace")


def audit(timeout_seconds: int = 120) -> dict:
    root = Path(__file__).resolve().parents[1]
    from phase165_r8_rule_provider import discover_inference_rules
    rules, report = discover_inference_rules()
    expected = (
        "first_isomorphism_quotient_inference_rule",
        "infinite_cyclic_quotient_structure_inference_rule",
    )
    module = "phase165_r12_r2_quotient_rules"
    registered = sorted(name for name in expected if any(
        rule.name == name for rule in rules
    ))
    # Rule names may differ from factory names: verify through the canonical registry IDs.
    from phase165_r10_rule_registry import build_rule_registry
    from phase165_r8_rule_provider import DEFAULT_RULE_MODULES
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    r12_ids = sorted(entry.rule_id for entry in registry.entries if entry.factory_module == module)
    report_data = {
        "phase": "165 R12-R4",
        "mode": "READ_ONLY_CANONICAL_PI43_SEARCH",
        "goal": repr(target_goal()),
        "registered_rule_count": len(registry.entries),
        "production_provider_rule_count": len(rules),
        "r12_r2_rule_ids": r12_ids,
        "expected_r12_r2_registered": all(
            f"{module}.{name}" in r12_ids for name in expected
        ),
        "full_pytest_run": False,
    }
    # Windows may emit CP932 bytes even if the parent expects UTF-8.
    # Keep the pipe binary and explicitly request UTF-8 in the Python worker.
    child_env = os.environ.copy()
    child_env["PYTHONIOENCODING"] = "utf-8"
    child_env["PYTHONUTF8"] = "1"
    try:
        process = subprocess.run(
            [sys.executable, "-m", "phase165_r12_r4_pi43_search.audit", "--worker"],
            cwd=root,
            env=child_env,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        report_data.update({
            "search_status": "TIMEOUT",
            "target_pi43_proof_certified": False,
            "diagnostics": [f"canonical search exceeded {timeout_seconds} seconds"],
        })
        return report_data
    stdout = decode_worker_output(process.stdout)
    stderr = decode_worker_output(process.stderr)
    if process.returncode != 0:
        report_data.update({
            "search_status": "ERROR",
            "target_pi43_proof_certified": False,
            "diagnostics": [stderr[-5000:], stdout[-2000:]],
        })
        return report_data
    try:
        payload = json.loads(stdout)
        if not isinstance(payload, dict):
            raise ValueError("worker output is not a JSON object")
        report_data.update(payload)
    except (json.JSONDecodeError, ValueError):
        report_data.update({
            "search_status": "INVALID_OUTPUT",
            "target_pi43_proof_certified": False,
            "diagnostics": [stdout[-3000:], stderr[-2000:]],
        })
    return report_data


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--worker":
        print(json.dumps(run_worker(), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(audit(), ensure_ascii=False, indent=2))
