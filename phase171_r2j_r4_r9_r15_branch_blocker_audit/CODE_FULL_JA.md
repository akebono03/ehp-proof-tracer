# Phase 171 R15 — 変更対象と新規コード全文

既存のファイル、import、クラス、関数、メソッドは**変更しない**。リポジトリ直下に `phase171_r2j_r4_r9_r15_branch_blocker_audit/` を新設する。新規クラスはない。新規の関数は下記各ファイルの記載位置に追加する。コード中に `...` による省略はない。

## `audit.py`（新規・全文）

```python
"""R15: inspect recorded R14 root branches and unique unresolved subgoals.

This is a read-only diagnostic of R14's observed canonical search, not a new
proof search and not a source of mathematical assertions or ProofSteps.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
R14_REPORT = ROOT / "phase171_r2j_r4_r9_r14_root_branch_diagnostic" / "output" / "audit.json"
OUTPUT = PACKAGE / "output" / "audit.json"
PROVIDER_NAME = "phase165_r52_r9_shared_math.py"
PROVIDER = ROOT / PROVIDER_NAME
REVIEWED_PROVIDER_BLOB = "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"


def git_read(*args: str) -> bytes:
    """Run only an explicitly allowed, read-only Git command."""
    if args not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("show", "HEAD:" + PROVIDER_NAME),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("R15 permits read-only Git inspection only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True,
    ).stdout


def blob_sha(content: bytes) -> str:
    """Calculate the SHA-1 of the exact Git blob, including newline convention."""
    return hashlib.sha1(
        ("blob %d\0" % len(content)).encode("ascii") + content,
    ).hexdigest()


def normalize(content: bytes) -> str:
    """Permit only CRLF/UTF-8-BOM differences in the local checked-out source."""
    return content.decode("utf-8-sig").replace("\r\n", "\n")


def preflight() -> dict[str, str]:
    """Check current develop and the R11-compatible committed provider."""
    branch = git_read("branch", "--show-current").decode("utf-8").strip()
    head = git_read("rev-parse", "HEAD").decode("utf-8").strip()
    committed = git_read("show", "HEAD:" + PROVIDER_NAME)
    digest = blob_sha(committed)
    if branch != "develop":
        raise RuntimeError("develop is required")
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise RuntimeError("invalid HEAD")
    if digest != REVIEWED_PROVIDER_BLOB:
        raise RuntimeError("provider blob is not the reviewed R11 baseline")
    if normalize(PROVIDER.read_bytes()) != normalize(committed):
        raise RuntimeError("local shared provider differs from committed HEAD")
    return {"branch": branch, "head": head, "provider_blob": digest}


def checked_r14_report(raw: dict[str, Any]) -> dict[str, Any]:
    """Reject incomplete or incompatible audit input; never infer missing events."""
    if not isinstance(raw, dict):
        raise TypeError("R14 report must be a JSON object")
    expected = {
        "phase": "171-R2J-R4-R9-R14",
        "mode": "READ_ONLY_CANONICAL_BRANCH_EXCEPTION_TRACE",
        "tracked_status_unchanged": True,
        "source_changes": 0,
        "new_given": 0,
        "completed_proof_imported": False,
    }
    for name, value in expected.items():
        if raw.get(name) != value:
            raise ValueError("R14 report incompatible: " + name)
    if not re.fullmatch(r"[0-9a-f]{40}", str(raw.get("git_head", ""))):
        raise ValueError("R14 HEAD missing or invalid")
    for name in ("provider_events", "exception_events"):
        if not isinstance(raw.get(name), list):
            raise ValueError("R14 events missing: " + name)
    if raw.get("provider_events_dropped", 0) or raw.get("exception_events_dropped", 0):
        raise ValueError("R14 trace is truncated; cannot assess all root branches")
    if not isinstance(raw.get("origin_counts"), dict):
        raise ValueError("R14 origin counts missing")
    if raw.get("root_route_count") is None:
        raise ValueError("R14 root route count missing")
    return raw


def matches_goal(event_goal: str, origin_goal: str) -> bool:
    """Compare bounded repr prefixes only; this is a diagnostic, not goal equality."""
    return bool(event_goal) and origin_goal.startswith(event_goal)


def candidate_observation(origin: dict[str, Any], providers: list[dict[str, Any]]) -> dict[str, Any]:
    """Distinguish zero proposals from proposals whose proofs did not close."""
    goal = origin["target"]
    matches = [event for event in providers if matches_goal(event["goal"], goal)]
    if not matches:
        return {"observation": "NOT_OBSERVED", "provider_calls": 0, "candidate_counts": [], "rule_names": []}
    counts = [event["count"] for event in matches]
    names = sorted({name for event in matches for name in event.get("rules", [])})
    return {
        "observation": "NO_EXPANSION" if max(counts) == 0 else "PROPOSALS_UNPROVED",
        "provider_calls": len(matches),
        "candidate_counts": counts,
        "rule_names": names[:25],
    }


def route_signature(rule: str, subgoals: list[str]) -> tuple[str, tuple[str, ...]]:
    """The ordered tuple uniquely names the recorded route for diagnostics."""
    return (rule, tuple(subgoals))


def analyze_r14(raw: dict[str, Any]) -> dict[str, Any]:
    """Summarize R14 observations; do not interpret errors as mathematical proofs."""
    raw = checked_r14_report(raw)
    provider_events = raw["provider_events"]
    exception_events = raw["exception_events"]
    roots = [event for event in provider_events if event.get("role") == "root"]
    if len(roots) != 1:
        raise ValueError("expected one observed root-provider call")
    proposals = roots[0].get("proposals", [])
    if roots[0].get("count") != raw["root_route_count"]:
        raise ValueError("root provider count changed within R14 report")
    if len(proposals) != raw["root_route_count"]:
        raise ValueError("R14 did not record all root proposals")
    root_failure_events = [
        event for event in exception_events
        if event.get("target_role") == "root" and not event.get("origin")
    ]
    routes = []
    for index, item in enumerate(proposals, start=1):
        signature = route_signature(item["rule"], item["subgoals"])
        failures = [event for event in root_failure_events if
                    route_signature(event.get("candidate_rule", ""), event.get("candidate_subgoals", [])) == signature]
        routes.append({
            "index": index,
            "rule": item["rule"],
            "subgoals": item["subgoals"],
            "propagated_failures": dict(Counter(event["kind"] for event in failures)),
            "failure_events": len(failures),
            "status": "SUBGOAL_FAILURE_OBSERVED" if failures else "NO_ROOT_PROPAGATION_OBSERVED",
        })
    unique: dict[tuple[str, str], dict[str, Any]] = {}
    for event in exception_events:
        if not event.get("origin") or event.get("kind") != "no_derivation":
            continue
        key = (event.get("target_role", "other"), event["target"])
        if key not in unique:
            unique[key] = {
                "role": key[0],
                "goal": key[1],
                "count": 0,
                "first_active_roles": event.get("active_roles", []),
                "first_active_last": event.get("active_last", []),
                "last_attempted_rule": event.get("candidate_rule", ""),
                "accepted_options_so_far": event.get("accepted_options_so_far", 0),
            }
        unique[key]["count"] += 1
    blockers = []
    for item in unique.values():
        observation = candidate_observation(
            {"target": item["goal"]}, provider_events,
        )
        blockers.append({**item, **observation})
    blockers.sort(key=lambda item: (-item["count"], item["role"], item["goal"]))
    total_observed = sum(item["count"] for item in blockers)
    if total_observed != raw["origin_counts"].get("no_derivation", 0):
        raise ValueError("R14 origin count differs from recorded origin events")
    summary = dict(Counter(item["observation"] for item in blockers))
    return {
        "phase": "171-R2J-R4-R9-R15",
        "mode": "READ_ONLY_R14_ROOT_BLOCKER_DEDUPLICATION",
        "r14_git_head": raw["git_head"],
        "r14_public_search": raw["public_status"],
        "r14_first_open_is_reverse": raw["first_open_is_reverse"],
        "r14_root_routes": raw["root_route_count"],
        "r14_origin_counts": raw["origin_counts"],
        "unique_no_derivation_goal_count": len(blockers),
        "no_derivation_event_count": total_observed,
        "blocker_classes": summary,
        "root_branches": routes,
        "ranked_no_derivation_goals": blockers,
        "classification": (
            "UNIQUE_GOALS_WITH_ZERO_PROVIDER_EXPANSIONS" if summary.get("NO_EXPANSION") else
            "UNIQUE_GOALS_WITH_UNPROVED_EXPANSIONS" if summary.get("PROPOSALS_UNPROVED") else
            "R14_UNOBSERVED_OR_NO_ZERO_DERIVATION"
        ),
        "causal_claim": "None: root-route failures and individual origins are observational, not a full causal dependency graph",
        "source_changes": 0,
        "new_given": 0,
        "completed_proof_imported": False,
        "public_web_verified": False,
        "full_pytest": False,
    }


def main() -> None:
    """Check baseline, deduplicate the existing R14 JSON, and save results."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ready = preflight()
    print("PHASE171_R15_BRANCH=" + ready["branch"], flush=True)
    print("PHASE171_R15_HEAD=" + ready["head"], flush=True)
    print("PHASE171_R15_R11_PROVIDER=PASS", flush=True)
    if args.dry_run:
        print("PHASE171_R15_RESULT=PASS_DRY_RUN", flush=True)
        return
    if not R14_REPORT.is_file():
        raise RuntimeError("R14 output/audit.json was not found: " + str(R14_REPORT))
    before = git_read("status", "--porcelain", "--untracked-files=no")
    raw_bytes = R14_REPORT.read_bytes()
    raw = json.loads(raw_bytes.decode("utf-8-sig"))
    result = analyze_r14(raw)
    result["git_head"] = ready["head"]
    result["r14_report_sha256"] = hashlib.sha256(raw_bytes).hexdigest()
    if git_read("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("R15 changed tracked Git status")
    result["tracked_status_unchanged"] = True
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R15_R14_SEARCH=" + result["r14_public_search"], flush=True)
    print("PHASE171_R15_ROOT_ROUTES=" + str(result["r14_root_routes"]), flush=True)
    print("PHASE171_R15_UNIQUE_NO_DERIVATION_GOALS=" + str(result["unique_no_derivation_goal_count"]), flush=True)
    print("PHASE171_R15_BLOCKER_CLASSES=" + json.dumps(result["blocker_classes"], ensure_ascii=False), flush=True)
    print("PHASE171_R15_ROOT_BRANCHES=" + json.dumps(
        [{"index": b["index"], "rule": b["rule"], "failures": b["propagated_failures"]}
         for b in result["root_branches"]], ensure_ascii=False), flush=True)
    print("PHASE171_R15_TOP_BLOCKERS=" + json.dumps(
        [{"role": b["role"], "count": b["count"], "observation": b["observation"],
          "rule_names": b["rule_names"][:3], "goal": b["goal"][:220]}
         for b in result["ranked_no_derivation_goals"][:8]], ensure_ascii=False), flush=True)
    print("PHASE171_R15_CLASSIFICATION=" + result["classification"], flush=True)
    print("PHASE171_R15_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R15_NEW_GIVEN=0", flush=True)
    print("PHASE171_R15_REPORT=" + str(OUTPUT), flush=True)
    print("PHASE171_R15_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py`（新規・全文）

```python
"""R15 tests: audit-log interpretation is non-mutating and fail-closed."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase171_r2j_r4_r9_r15_branch_blocker_audit.audit import (
    analyze_r14,
    blob_sha,
    candidate_observation,
    checked_r14_report,
    git_read,
    matches_goal,
    normalize,
    route_signature,
)


def fixture_r14():
    root = {"role": "root", "goal": "root", "count": 2, "proposals": [
        {"rule": "root-a", "subgoals": ["A"]},
        {"rule": "root-b", "subgoals": ["B"]},
    ]}
    return {
        "phase": "171-R2J-R4-R9-R14",
        "mode": "READ_ONLY_CANONICAL_BRANCH_EXCEPTION_TRACE",
        "tracked_status_unchanged": True,
        "source_changes": 0,
        "new_given": 0,
        "completed_proof_imported": False,
        "git_head": "f" * 40,
        "provider_events": [root, {"role": "other", "goal": "A", "count": 0, "rules": []}],
        "exception_events": [
            {"origin": True, "kind": "no_derivation", "target_role": "other",
             "target": "A", "active_roles": ["root", "other"],
             "active_last": ["root", "A"], "candidate_rule": "",
             "accepted_options_so_far": 0},
            {"origin": False, "kind": "no_derivation", "target_role": "root",
             "target": "root", "candidate_rule": "root-a",
             "candidate_subgoals": ["A"]},
            {"origin": True, "kind": "no_derivation", "target_role": "other",
             "target": "A", "active_roles": ["root", "other"],
             "active_last": ["root", "A"], "candidate_rule": "",
             "accepted_options_so_far": 0},
            {"origin": False, "kind": "no_derivation", "target_role": "root",
             "target": "root", "candidate_rule": "root-b",
             "candidate_subgoals": ["B"]},
        ],
        "provider_events_dropped": 0,
        "exception_events_dropped": 0,
        "origin_counts": {"no_derivation": 2},
        "root_route_count": 2,
        "public_status": "partial",
        "first_open_is_reverse": True,
    }


def test_valid_r14_contract_and_deduplication():
    raw = fixture_r14()
    before = deepcopy(raw)
    report = analyze_r14(raw)
    assert raw == before
    assert report["r14_root_routes"] == 2
    assert report["unique_no_derivation_goal_count"] == 1
    assert report["no_derivation_event_count"] == 2
    assert report["blocker_classes"] == {"NO_EXPANSION": 1}
    assert report["classification"] == "UNIQUE_GOALS_WITH_ZERO_PROVIDER_EXPANSIONS"
    assert report["ranked_no_derivation_goals"][0]["count"] == 2


def test_root_branches_preserve_order_and_propagation_counts():
    report = analyze_r14(fixture_r14())
    assert [route["rule"] for route in report["root_branches"]] == ["root-a", "root-b"]
    assert [route["propagated_failures"] for route in report["root_branches"]] == [
        {"no_derivation": 1}, {"no_derivation": 1},
    ]


def test_candidate_with_proposals_is_not_labeled_missing():
    provider = [{"goal": "Relation(xxxxxxxxx)", "count": 1, "rules": ["rule-a"]}]
    result = candidate_observation({"target": "Relation(xxxxxxxxx) and tail"}, provider)
    assert result["observation"] == "PROPOSALS_UNPROVED"
    assert result["rule_names"] == ["rule-a"]
    assert matches_goal("Relation(xxxxxxxxx)", "Relation(xxxxxxxxx) and tail")
    assert not matches_goal("", "anything")
    assert route_signature("r", ["x"]) != route_signature("r", ["y"])


def test_incomplete_or_modified_r14_trace_fails_closed():
    raw = fixture_r14()
    raw["exception_events_dropped"] = 1
    with pytest.raises(ValueError, match="truncated"):
        checked_r14_report(raw)
    raw = fixture_r14()
    raw["source_changes"] = 1
    with pytest.raises(ValueError, match="source_changes"):
        checked_r14_report(raw)
    raw = fixture_r14()
    raw["origin_counts"]["no_derivation"] = 3
    with pytest.raises(ValueError, match="origin count"):
        analyze_r14(raw)


def test_no_new_derivation_is_inferred_from_missing_provider_trace():
    raw = fixture_r14()
    raw["provider_events"] = raw["provider_events"][:1]
    report = analyze_r14(raw)
    assert report["blocker_classes"] == {"NOT_OBSERVED": 1}
    assert "None:" in report["causal_claim"]


def test_read_only_git_guard_and_normalization():
    with pytest.raises(ValueError, match="read-only"):
        git_read("reset", "--hard")
    assert normalize(b"\xef\xbb\xbfabc\r\n") == "abc\n"
    assert blob_sha(b"test\n") == "9daeafb9864cf43055ae93beb0afd6c7d144bfa4"
```

## `__init__.py`（新規・全文）

```python
"""Phase 171 R15: read-only root-branch blocker audit."""
```

## `tests/__init__.py`（新規・全文）

```python
"""Focused tests for the Phase 171 R15 audit."""
```

## `run.ps1`（新規・全文）

```powershell
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Module = 'phase171_r2j_r4_r9_r15_branch_blocker_audit'
Push-Location $RepoRoot
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
        throw 'R15 requires the develop branch.'
    }
    Write-Output "PHASE171_R15_BRANCH=$Branch"

    python -m "$Module.audit" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15 preflight failed.' }
    if ($DryRun) {
        Write-Output 'PHASE171_R15_DRY_RUN=PASS'
        return
    }

    Write-Output 'PHASE171_R15_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider "$Module/tests/test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R15 focused pytest failed.' }
    Write-Output 'PHASE171_R15_FOCUSED_PYTEST=PASS'

    python -m "$Module.audit"
    if ($LASTEXITCODE -ne 0) { throw 'R15 audit failed.' }

    git status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed.' }
    git diff --stat
    if ($LASTEXITCODE -ne 0) { throw 'Git diff failed.' }
    Write-Output 'PHASE171_R15_RESULT=PASS_READ_ONLY_BLOCKER_AUDIT'
}
finally {
    Pop-Location
}
```

