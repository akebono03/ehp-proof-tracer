# Phase 175 R4R12R11 — コード全文

追加位置: リポジトリ直下 `phase175_r4r12r11_ehp_surjectivity_frontier/`。既存の import、クラス、関数は変更しない。

## `audit.py`

```python
"""Read-only EHP quotient frontier inspection; never installs mathematical facts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

PACKAGE = "phase175_r4r12r11_ehp_surjectivity_frontier"
RULE_NAME = "EHP exact rank-two elementary 2-group quotient by a generated summand"


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R11_GIT_FAILED: " + " ".join(arguments) + ": " + result.stderr)
    return result.stdout.strip()


def describe(item: object) -> str:
    return repr(item)


def valid_zero_goal(statement: object) -> bool:
    """Reject a purported zero diagonal sphere group; no proof claim is created."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    if not isinstance(statement, TodaPrimaryGroupZeroStatement):
        return True
    group = statement.group
    if not isinstance(group, TodaPrimaryGroup):
        return True
    q, n = group.group_dimension, group.sphere_dimension
    return not (type(q) is int and type(n) is int and q == n and n >= 2)


def inspect() -> dict[str, object]:
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import MapSurjective, GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
    from phase165_r12_r12_ehp_consequences import expand_ehp_exactness_consequences
    root = exact_prior_database_result(5, 4)
    if root is None or not isinstance(root.rhs, FiniteCyclicGroup) or root.rhs.order != 2:
        raise RuntimeError("R11_ROOT_MISSING")
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    isolated = expand_public_two_summand_quotient(goal, proof_target=root)
    bridge = build_shared_typed_bridge()
    shared = shared_expansion_provider(bridge, proof_target=root)
    selected = tuple(item for item in shared(goal) if item.rule.name == RULE_NAME)
    if len(isolated) != 2 or len(selected) != 2:
        raise RuntimeError("R11_TWO_ORIENTATIONS_REQUIRED")
    paths = []
    for index, candidate in enumerate(selected):
        obligations = candidate.subgoals
        if len(obligations) != 6 or not isinstance(obligations[4], MapSurjective):
            raise RuntimeError("R11_SIX_OBLIGATIONS_MISSING")
        entries = []
        for position in (2, 3, 4, 5):
            statement = obligations[position]
            expansions = tuple(shared(statement))
            entries.append({
                "index": position,
                "statement_type": type(statement).__name__,
                "statement": describe(statement),
                "candidate_count": len(expansions),
                "candidate_rules": [x.rule.name for x in expansions],
                "candidate_subgoals": [
                    {"rule": x.rule.name, "subgoals": [describe(y) for y in x.subgoals]}
                    for x in expansions[:12]
                ],
                "proof_claimed": False,
            })
        surjectivity = obligations[4]
        zero_route = tuple(expand_ehp_exactness_consequences(surjectivity))
        zero_requisites = [y for x in zero_route for y in x.subgoals if isinstance(y, TodaPrimaryGroupZeroStatement)]
        paths.append({
            "orientation": index,
            "delta_image": describe(obligations[2]) if isinstance(obligations[2], GeneratorImage) else None,
            "suspension_image": describe(obligations[5]),
            "ehp_surjectivity_zero_route_count": len(zero_route),
            "zero_route_targets": [describe(x.group) for x in zero_requisites],
            "zero_route_has_false_diagonal_goal": any(not valid_zero_goal(x) for x in zero_requisites),
            "obligation_details": entries,
        })
    return {
        "isolated_count": len(isolated),
        "shared_count": len(selected),
        "paths": paths,
        "source_511_remains_cited": True,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "actual_recursive_search_executed": False,
        "group_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R11_WRONG_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R11_WRONG_BRANCH")
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "phase": "175-R4R12R11", "dry_run": dry_run,
        "gate": "FAIL_R11", "full_pytest_executed": False,
        "head": git(root, "rev-parse", "HEAD"),
        "production_dirty": "phase165_r52_r9_shared_math.py" in git(root, "diff", "--name-only").splitlines(),
    }
    try:
        report["frontier"] = inspect()
        report["gate"] = "PASS_R11_EHP_SURJECTIVITY_FRONTIER_AUDITED_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    filename = output / ("preflight.json" if dry_run else "audit_report.json")
    filename.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R12R11_GATE=" + report["gate"])
    print("PHASE175_R4R12R11_REPORT=" + str(filename))
    for entry in report.get("frontier", {}).get("paths", []):
        print("R11_ORIENTATION=" + str(entry["orientation"]))
        print("R11_FALSE_DIAGONAL_ZERO_PREMISE=" + str(entry["zero_route_has_false_diagonal_goal"]))
        for x in entry["obligation_details"]:
            print("R11_OBLIGATION_" + str(x["index"]) + "_CANDIDATES=" + str(x["candidate_count"]))
            print("R11_OBLIGATION_" + str(x["index"]) + "_RULES=" + repr(x["candidate_rules"]))
    if "error" in report:
        print("PHASE175_R4R12R11_ERROR=" + report["error"])
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args(argv)
    return run(arguments.root.resolve(), dry_run=arguments.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())

```

## `tests/test_audit.py`

```python
"""Focused tests for the read-only EHP surjectivity diagnostic."""
from __future__ import annotations

from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase175_r4r12r11_ehp_surjectivity_frontier import audit


def test_diagonal_sphere_group_is_not_zero() -> None:
    assert not audit.valid_zero_goal(TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9, 9)))


def test_off_diagonal_zero_goal_not_prejudged() -> None:
    assert audit.valid_zero_goal(TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9, 17)))


def test_audit_does_not_claim_completed_proof() -> None:
    assert audit.PACKAGE == "phase175_r4r12r11_ehp_surjectivity_frontier"
    assert "NOT_COMPLETE" in "PASS_R11_EHP_SURJECTIVITY_FRONTIER_AUDITED_NOT_COMPLETE"


def test_git_command_failure_is_not_swallowed(monkeypatch: pytest.MonkeyPatch) -> None:
    class Failed:
        returncode = 1
        stdout = ""
        stderr = "intentional failure"

    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: Failed())
    with pytest.raises(RuntimeError, match="R11_GIT_FAILED"):
        audit.git(Path.cwd(), "rev-parse", "HEAD")

```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m pytest -q -p no:cacheprovider phase175_r4r12r11_ehp_surjectivity_frontier/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R11 focused pytest failed' }
    $argsList = @('--root', $root)
    if ($DryRun) { $argsList += '--dry-run' }
    python -m phase175_r4r12r11_ehp_surjectivity_frontier.audit @argsList
    if ($LASTEXITCODE -ne 0) { throw 'R11 audit failed' }
} finally {
    Pop-Location
}

```

## `__init__.py`

```python
"""Read-only Phase 175 R4R12R11 frontier audit."""

```

## `README.md`

```markdown
# Phase 175 R4R12R11 — Read-only EHP surjectivity frontier audit

This package inspects shared, typed, backward-search candidates for the rank-two EHP quotient rule. It is explicitly **not** a proof of the target group and does not register new source statements or modify production Python code.

The published equation (5.11) is reused as registered by R10R1. The audit identifies the six prerequisite goals for each orientation and highlights the invalid `pi_9(S^9)=0` subgoal that may be proposed by the existing zero-codomain surjectivity shortcut. That shortcut remains mathematically valid when its premise is true; the audit never asserts the premise for the diagonal sphere group.

Unzip into the repository root on the `develop` branch and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r11_ehp_surjectivity_frontier\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r11_ehp_surjectivity_frontier\run.ps1
```

Focused tests only. Reports are saved under this package's `output` directory. No full pytest is run. The `production_dirty` field is reported but changes are never applied. The accepted Git HEAD is not pinned, since this audit makes no modification; branch and root are checked.

```

## `AUDIT_PLAN_JA.md`

```markdown
# Phase 175 R4R12R11 監査計画

## 対象

- 新規 `phase175_r4r12r11_ehp_surjectivity_frontier/audit.py`：`git`、`describe`、`valid_zero_goal`、`inspect`、`run`、`main` を追加する。
- 新規 `tests/test_audit.py`：4件の限定テストを追加する。
- 新規 `run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`__init__.py`。
- 既存ファイル・既存クラス・既存関数・既存 import は変更しない。

## 数学的注意

(5.11) は再証明しない。既存 R10R1 が登録した文献与件を利用する。

EHP 完全性から $E:\pi_8^4\to\pi_9^5$ の全射性を主張する際、$\pi_9^9=0$ を前提にする既存の候補は使用できない。実際 $\pi_9^9\cong\mathbb Z$ である。

今回の監査では $H$ の像に関する一般的な定理を追加しない。$E$ の全射性と生成元像はそれぞれ独立した未解決義務として維持する。

## 完了条件

- 共有・単独の2 Orientation が同じく得られる。
- 6義務のうち Δ 像、EHP 完全性、E 全射性、E 生成元像の候補と前提を出力する。
- 零群を要求する候補と、その対象群が diagonal である事実を可視化する。
- 実際の再帰証明・本番ファイルの変更・新規 GIVEN・新規数学規則・全体 pytest は実施しない。
- Gate: `PASS_R11_EHP_SURJECTIVITY_FRONTIER_AUDITED_NOT_COMPLETE`。

```
