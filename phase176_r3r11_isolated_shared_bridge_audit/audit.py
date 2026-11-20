"""Phase 176 R3R11: read-only evidence inventory for isolated/shared bridge."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
from typing import Any

SOURCE_PATHS = (
    "phase165_r52_r9_shared_math.py",
    "phase175_r4r14r4_general_zero_transport/rule.py",
    "phase175_r4r14r5_public_zero_transport/provider.py",
    "phase175_r4r14r5_public_zero_transport/tests/test_provider.py",
)
EXPECTED_FUNCTIONS = {
    SOURCE_PATHS[0]: ("def shared_expansion_provider(",),
    SOURCE_PATHS[1]: ("def composite_value_zero_inputs(", "def expand_proved_composite_zero_image("),
    SOURCE_PATHS[2]: ("def build_public_composite_zero_transport_provider(",),
    SOURCE_PATHS[3]: ("def test_shared_provider_offers_same_generic_rule(",),
}


def git_output(root: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    if done.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {done.stderr.strip()}")
    return done.stdout.strip()


def scalar_evidence(obj: Any, prefix: str = "", depth: int = 0) -> list[dict[str, Any]]:
    """Expose scalar values by their actual JSON paths; do not invent field names."""
    if depth > 24:
        return []
    if isinstance(obj, dict):
        results: list[dict[str, Any]] = []
        for key, value in obj.items():
            results.extend(scalar_evidence(value, f"{prefix}.{key}" if prefix else str(key), depth + 1))
        return results
    if isinstance(obj, list):
        results = []
        for index, value in enumerate(obj[:200]):
            results.extend(scalar_evidence(value, f"{prefix}[{index}]", depth + 1))
        return results
    if obj is None or isinstance(obj, (bool, int, float, str)):
        value = obj if not isinstance(obj, str) or len(obj) <= 300 else obj[:300] + " [truncated]"
        return [{"path": prefix, "value": value}]
    return []


def interesting_evidence(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tokens = ("zero", "inferred", "candidate", "group", "open", "status", "source", "step", "goal", "bridge", "provider", "rule", "gate", "head", "proof")
    return [r for r in records if any(token in r["path"].lower() for token in tokens)]


def audit(root: Path, previous: Path) -> dict[str, Any]:
    if not previous.is_file():
        raise FileNotFoundError(f"R3R10 report missing: {previous}")
    previous_json = json.loads(previous.read_text(encoding="utf-8-sig"))
    if not isinstance(previous_json, dict):
        raise ValueError("R3R10 report must be a JSON object")
    head = git_output(root, "rev-parse", "HEAD")
    branch = git_output(root, "branch", "--show-current")
    repo_files: list[dict[str, Any]] = []
    for relative in SOURCE_PATHS:
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(f"required source missing: {path}")
        content = path.read_text(encoding="utf-8-sig")
        missing = [f for f in EXPECTED_FUNCTIONS[relative] if f not in content]
        if missing:
            raise ValueError(f"missing reviewed function in {relative}: {missing}")
        repo_files.append({"path": relative, "git_blob_sha": git_output(root, "hash-object", relative), "functions_present": True})
    records = scalar_evidence(previous_json)
    evidence = interesting_evidence(records)
    provider_text = (root / SOURCE_PATHS[2]).read_text(encoding="utf-8-sig")
    root_text = (root / SOURCE_PATHS[0]).read_text(encoding="utf-8-sig")
    rule_text = (root / SOURCE_PATHS[1]).read_text(encoding="utf-8-sig")
    checks = {
        "shared_provider_registration_present": "build_public_composite_zero_transport_provider(bridge)" in root_text,
        "source_screened_law_required": "screened_general_law(bridge)" in provider_text,
        "canonical_relation_equality_required": "cited_relation != Relation(lifted, Zero(), RelationType.EQUALITY)" in provider_text,
        "typed_suspension_required": "valid_suspension(goal.map)" in provider_text,
        "two_proved_premises_required": "composite_value_zero_inputs(goal, composite_image)" in rule_text,
    }
    result = {
        "phase": "176", "stage": "R3R11", "kind": "READ_ONLY_AUDIT",
        "git_head": head, "git_branch": branch,
        "previous_report_path": str(previous),
        "previous_report_top_level_keys": list(previous_json.keys()),
        "previous_report_relevant_scalar_evidence": evidence[:500],
        "source_inventory": repo_files,
        "static_contract_checks": checks,
        "candidate_count_measured_in_this_stage": False,
        "candidate_count_from_R3R10_console": 0,
        "isolated_inference_from_R3R10_console": True,
        "root_group_status_from_R3R10_console": "search_failed",
        "root_group_from_R3R10_console": [3, 5],
        "root_open_goals_from_R3R10_console": 3,
        "bridge_cause_confirmed": False,
        "new_given": 0, "new_math_rules": 0, "production_changes": 0,
        "gate": "PASS_R3R11_READ_ONLY_EVIDENCE_INVENTORY" if all(checks.values()) else "FAIL_R3R11_STATIC_CONTRACT",
        "next_step": "Inspect R3R10 exact typed step and goal identities; compare with screened law and Provider guards before modifying code.",
    }
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--previous", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    result = audit(args.root.resolve(), args.previous.resolve())
    if not args.dry_run:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PHASE176_R3R11_GATE={result['gate'] if not args.dry_run else 'PASS_R3R11_READ_ONLY_DRYRUN' if result['gate'].startswith('PASS') else result['gate']}")
    print(f"PHASE176_R3R11_HEAD={result['git_head']}")
    print(f"PHASE176_R3R11_PREVIOUS_KEYS={','.join(result['previous_report_top_level_keys'])}")
    print(f"PHASE176_R3R11_RELEVANT_EVIDENCE_RECORDS={len(result['previous_report_relevant_scalar_evidence'])}")
    print(f"PHASE176_R3R11_STATIC_CHECKS={sum(result['static_contract_checks'].values())}/{len(result['static_contract_checks'])}")
    print(f"PHASE176_R3R11_REPORT={args.output}")
    print("PHASE176_R3R11_BRIDGE_CAUSE_CONFIRMED=False")
    print("PHASE176_R3R11_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if result["gate"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
