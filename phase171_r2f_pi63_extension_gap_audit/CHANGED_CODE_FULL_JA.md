# Phase 171 R2F — 変更コード全文

このパッケージは **AUDIT_ONLY** であり、既存のアプリケーションコード・クラス・関数・テストは変更しない。

## 変更対象

- 新規 `phase171_r2f_pi63_extension_gap_audit/audit.py`：全 import、`git_read`、`snapshot`、`typed_differences`、`matching_cited_steps`、`source_inventory`、`expansion_inventory`、`requirement_assessment`、`run`、`main`。
- 新規 `phase171_r2f_pi63_extension_gap_audit/tests/test_audit.py`：全 import と新規テスト関数7件。
- 新規 `phase171_r2f_pi63_extension_gap_audit/run.ps1`：PowerShell スクリプト全文。
- 新規 `README.md`（英語）、`監査仕様.md`（日本語）、`__init__.py`。

## 位置

いずれもリポジトリ直下の `phase171_r2f_pi63_extension_gap_audit/` に追加。既存ファイルの置換はない。

## 新規コード・文書の全文


### audit.py

```python
"""Read-only audit for the typed order-four extension of pi_6^3.

This code neither adds a ProofStep nor changes any inference rule or source.
A mathematical argument is not reported as a completed machine proof.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import fields, is_dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

EXPECTED_TARGET = "shared:0:boundary:Proposition 5.6:pi6_3_group_relation"
EXPECTED_DOUBLE_SUFFIX = "toda:adopted:eq5.3:nu_prime_double_relation"
EXPECTED_HOPF_SUFFIX = "toda:adopted:eq5.3:nu_prime_hopf_relation"
LOCATORS = (
    "Proposition 2.2", "Proposition 4.2 (4.4)", "(5.2)",
    "Proposition 5.3", "(5.3)", "Proposition 5.6",
)


def git_read(root: Path, *arguments: str) -> bytes:
    """Execute only listed read-only Git invocations and require success."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("rev-parse", "--verify", "refs/remotes/origin/develop"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
        ("diff", "--binary", "HEAD", "--"),
    }
    if arguments not in allowed:
        raise ValueError("Git operation not authorized for R2F audit")
    process = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, check=False,
    )
    if process.returncode:
        raise RuntimeError(
            "git " + " ".join(arguments) + ": "
            + process.stderr.decode("utf-8", errors="replace")
        )
    return process.stdout


def snapshot(root: Path) -> dict:
    """Record committed identity and exact tracked/untracked worktree state."""
    branch = git_read(root, "branch", "--show-current").decode().strip()
    if branch != "develop":
        raise RuntimeError("R2F requires develop but never switches branches")
    head = git_read(root, "rev-parse", "HEAD").decode().strip()
    try:
        upstream = git_read(root, "rev-parse", "--verify", "refs/remotes/origin/develop").decode().strip()
    except RuntimeError:
        upstream = None
    return {
        "branch": branch,
        "head": head,
        "origin_develop_local_ref": upstream,
        "head_equals_local_origin_ref": head == upstream,
        "status": git_read(root, "status", "--porcelain=v1", "--untracked-files=all").decode(
            "utf-8", errors="replace"
        ).splitlines(),
        "tracked_diff_sha256": sha256(git_read(root, "diff", "--binary", "HEAD", "--")).hexdigest(),
    }


def typed_differences(left: object, right: object, *, limit: int = 20) -> list[dict]:
    """Compare dataclass fields exactly; never accept name-only generator aliases."""
    differences: list[dict] = []

    def visit(a: object, b: object, path: str, depth: int) -> None:
        if len(differences) >= limit:
            return
        if type(a) is not type(b):
            differences.append({
                "path": path, "reason": "type_mismatch",
                "left": type(a).__name__, "right": type(b).__name__,
            })
            return
        if depth >= 12:
            if a != b:
                differences.append({"path": path, "reason": "depth_limit"})
            return
        if is_dataclass(a) and not isinstance(a, type):
            for field in fields(a):
                visit(getattr(a, field.name), getattr(b, field.name), path + "." + field.name, depth + 1)
            return
        if a != b:
            differences.append({
                "path": path, "reason": "value_mismatch",
                "left": repr(a)[:250], "right": repr(b)[:250],
            })

    visit(left, right, "generator", 0)
    return differences


def matching_cited_steps(bridge: object, suffix: str) -> tuple:
    """Require screened, no-premise, registered fixed GIVENs with exact identity."""
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    matches = []
    for link in bridge.proof_links:
        step = link.step
        if not link.assertion_id.endswith(suffix) or step is None:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and step.rule is ProofRule.GIVEN
                and not step.premises
                and step.conclusion == assertion.content):
            matches.append((link.assertion_id, step.conclusion))
    return tuple(matches)


def source_inventory(bridge: object) -> dict:
    """Count screened assertions, never count unscreened archive metadata as proof."""
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    output = {}
    for locator in LOCATORS:
        entries = []
        for link in bridge.proof_links:
            step = link.step
            if step is None:
                continue
            assertion = bridge.registry.assertion(link.assertion_id)
            reference = bridge.registry.reference(assertion.reference_id)
            if reference.locator != locator:
                continue
            if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                    or step.rule is not ProofRule.GIVEN
                    or step.premises or step.conclusion != assertion.content):
                continue
            entries.append({
                "id": link.assertion_id,
                "type": type(step.conclusion).__name__,
                "text": repr(step.conclusion)[:1200],
                "position": reference.publication_position,
            })
        output[locator] = {"count": len(entries), "steps": entries[:16]}
    return output


def expansion_inventory(goal: object, provider: object, bridge: object) -> dict:
    """Observe first-level proposals without treating a proposed premise as known."""
    from proof import ProofRule

    options = provider(goal)
    if not isinstance(options, tuple):
        raise TypeError("provider must return a tuple")
    counter = Counter()
    details = []
    for option in options:
        name = str(getattr(option.rule, "name", type(option.rule).__name__))
        counter[name] += 1
        if len(details) >= 16:
            continue
        children = []
        for child in option.subgoals[:10]:
            cited_matches = tuple(
                link.assertion_id for link in bridge.proof_links
                if link.step is not None
                and link.step.rule is ProofRule.GIVEN
                and not link.step.premises
                and link.step.conclusion == child
            )
            children.append({
                "type": type(child).__name__,
                "goal": repr(child)[:1200],
                "exact_screened_given_ids": cited_matches,
            })
        details.append({"rule": name, "subgoals": children})
    return {"count": len(options), "rules": dict(sorted(counter.items())), "examples": details}


def requirement_assessment(inventory: dict, *, double_present: bool, hopf_present: bool,
                           cyclic_expansions: int) -> list[dict]:
    """List known evidence and unproved obligations without asserting impossibility."""
    evidence = (
        ("prop22_hopf_composition", "Proposition 2.2",
         "H(nu' o eta_6)=eta_5^2 の型付き導出"),
        ("prop53_eta_squared", "Proposition 5.3",
         "pi_7^5 および pi_5^3 の位数2・生成性の特殊化"),
        ("toda52_pi52", "(5.2)",
         "pi_5^2 の群構造と生成元 eta_2^3 の輸送"),
        ("ehp_exact_window", "Proposition 4.2 (4.4)",
         "pi_7^3→pi_7^5→pi_5^2→pi_6^3→pi_6^5 の完全性"),
    )
    rows = [{
        "key": key,
        "screened_fixed_given_count": inventory[locator]["count"],
        "obligation": obligation,
        "certified_as_completed_inference": False,
    } for key, locator, obligation in evidence]
    rows.extend((
        {"key": "nu_prime_hopf", "screened_fixed_given_count": int(hopf_present),
         "obligation": "H(nu')=eta_5 と H の全射性を区別", "certified_as_completed_inference": False},
        {"key": "nu_prime_double", "screened_fixed_given_count": int(double_present),
         "obligation": "2nu'=eta_3 eta_4 eta_5 と E(eta_2^3) を同一視する証明",
         "certified_as_completed_inference": False},
        {"key": "finite_extension_structure", "screened_fixed_given_count": 0,
         "obligation": "E の単射・H の全射・完全性と Z/2×Z/2 から |pi_6^3|=4 を導く",
         "certified_as_completed_inference": False},
        {"key": "order_and_generator", "screened_fixed_given_count": 0,
         "obligation": "非零の 2nu' と位数4の群から位数4・生成性を導く",
         "certified_as_completed_inference": False},
    ))
    if cyclic_expansions:
        rows[-1]["note"] = "既存の巡回群構造への候補は存在するが証明ではない"
    return rows


def run(root: Path, *, dry_run: bool, search: bool) -> int:
    """Audit the current local worktree without modifying repository files."""
    before = snapshot(root)
    print("PHASE171_R2F_BRANCH=" + before["branch"], flush=True)
    print("PHASE171_R2F_HEAD=" + before["head"], flush=True)
    print("PHASE171_R2F_TRACKED_DIFF_SHA256=" + before["tracked_diff_sha256"], flush=True)
    if dry_run:
        if snapshot(root) != before:
            raise RuntimeError("worktree changed during DryRun")
        print("PHASE171_R2F_DRY_RUN=PASS", flush=True)
        print("PHASE171_R2F_RESULT=PASS_AUDIT_ONLY", flush=True)
        return 0

    from expression import Multiple
    from homotopy_groups import FiniteCyclicGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase166_r3c_publication_order import precedes_citing_assertion
    from proof import ProofRule

    complete = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(complete, n=3, k=3)
    if len(candidates) != 1:
        raise RuntimeError("expected one typed pi_6^3 DB goal")
    goal = candidates[0]
    if not isinstance(goal.rhs, FiniteCyclicGroup) or goal.rhs.order != 4:
        raise RuntimeError("unexpected pi_6^3 target group")
    citing = resolve_specialized_goal_citing_id(complete, goal)
    if citing != EXPECTED_TARGET:
        raise RuntimeError("unexpected source identity for pi_6^3 goal: " + repr(citing))
    screened = screen_shared_proof_context(
        complete, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    doubles = matching_cited_steps(screened, EXPECTED_DOUBLE_SUFFIX)
    hopfs = matching_cited_steps(screened, EXPECTED_HOPF_SUFFIX)
    if len(doubles) != 1 or len(hopfs) != 1:
        raise RuntimeError("R2E double and R3H Hopf must each be uniquely screened GIVENs")
    double_assertion = screened.registry.assertion(doubles[0][0])
    double_reference = screened.registry.reference(double_assertion.reference_id)
    if (double_reference.locator != "(5.3)"
            or double_reference.publication_position != 8100
            or not precedes_citing_assertion(screened, doubles[0][0], citing)):
        raise RuntimeError("R2E source does not precede the target at the reviewed position")
    relation = doubles[0][1]
    if not isinstance(relation.lhs, Multiple) or relation.lhs.coefficient != 2:
        raise RuntimeError("R2E conclusion is not a typed 2*generator equality")
    if any(link.step is not None and link.step.conclusion == goal
           for link in screened.proof_links):
        raise RuntimeError("forbidden direct target proof link was found")

    cyclic = CyclicStructureStatement(goal.lhs, goal.rhs.generator, 4)
    provider = shared_expansion_provider(screened, proof_target=goal)
    root = expansion_inventory(goal, provider, screened)
    cyclic_frontier = expansion_inventory(cyclic, provider, screened)
    sources = source_inventory(screened)
    assessment = requirement_assessment(
        sources, double_present=True, hopf_present=True,
        cyclic_expansions=cyclic_frontier["count"],
    )
    runtime_search = None
    if search:
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        result = search_group_from_registered_goal(n=3, k=3, bridge=complete)
        runtime_search = {
            "status": str(result.status),
            "conclusion_is_goal": result.conclusion == goal,
            "inference_step_count": sum(step.rule is ProofRule.INFERENCE
                                        for step in result.proven_steps),
            "given_step_count": sum(step.rule is ProofRule.GIVEN
                                    for step in result.proven_steps),
            "open_goals": [repr(x)[:1000] for x in result.open_goals[:16]],
        }
    report = {
        "phase": "171 R2F", "mode": "READ_ONLY_TYPED_GAP", "read_only": True,
        "git_before": before,
        "target": repr(goal), "citing_id": citing,
        "double_given_id": doubles[0][0], "hopf_given_id": hopfs[0][0],
        "double_publication_position": double_reference.publication_position,
        "double_precedes_target": True,
        "double_relation": repr(relation),
        "db_generator": repr(goal.rhs.generator),
        "nu_prime_from_double": repr(relation.lhs.expression),
        "generator_typed_equal": goal.rhs.generator == relation.lhs.expression,
        "generator_differences": typed_differences(goal.rhs.generator, relation.lhs.expression),
        "sources": sources,
        "root_expansions": root, "cyclic_expansions": cyclic_frontier,
        "remaining_obligations": assessment,
        "runtime_search": runtime_search,
        "root_proof_certified_by_this_audit": False,
    }
    if snapshot(root) != before:
        raise RuntimeError("worktree changed during source inspection")
    report["git_after_identical"] = True
    report_dir = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    report_dir = report_dir / ("phase171_r2f_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    report_dir.mkdir(parents=True, exist_ok=False)
    report_path = report_dir / "audit.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PHASE171_R2F_DOUBLE_SOURCE=PASS", flush=True)
    print("PHASE171_R2F_HOPF_SOURCE=PASS", flush=True)
    print("PHASE171_R2F_DB_GENERATOR_TYPED_EQUAL=" + str(report["generator_typed_equal"]), flush=True)
    print("PHASE171_R2F_ROOT_RULES=" + json.dumps(root["rules"], ensure_ascii=False), flush=True)
    print("PHASE171_R2F_CYCLIC_RULES=" + json.dumps(cyclic_frontier["rules"], ensure_ascii=False), flush=True)
    for row in assessment:
        print("PHASE171_R2F_OBLIGATION=" + json.dumps(row, ensure_ascii=False), flush=True)
    if runtime_search is not None:
        print("PHASE171_R2F_SEARCH=" + json.dumps(runtime_search, ensure_ascii=False), flush=True)
    print("PHASE171_R2F_REPORT=" + str(report_path), flush=True)
    print("PHASE171_R2F_WORKTREE_UNCHANGED=True", flush=True)
    print("PHASE171_R2F_RESULT=PASS_AUDIT_ONLY", flush=True)
    return 0


def main() -> int:
    """Run the audit in dry-run, frontier, or optional existing-search mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--search", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.root.resolve(), dry_run=args.dry_run, search=args.search)
    except Exception as exc:
        print("PHASE171_R2F_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        print(traceback.format_exc()[-3000:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

### tests/test_audit.py

```python
"""Source-independent, narrow tests for Phase 171 R2F read-only audit."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase171_r2f_pi63_extension_gap_audit import audit


def test_git_read_blocks_mutating_commands(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="not authorized"):
        audit.git_read(tmp_path, "reset", "--hard")
    with pytest.raises(ValueError, match="not authorized"):
        audit.git_read(tmp_path, "checkout", "--", "proof.py")


def test_typed_differences_rejects_same_text_with_different_types() -> None:
    left = SimpleNamespace(name="nu-prime", source=6)
    right = {"name": "nu-prime", "source": 6}
    result = audit.typed_differences(left, right)
    assert result == [{
        "path": "generator", "reason": "type_mismatch",
        "left": "SimpleNamespace", "right": "dict",
    }]


def test_typed_differences_detects_dataclass_field_mismatch() -> None:
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Generator:
        family: str
        decoration: str

    differences = audit.typed_differences(Generator("nu", "prime"), Generator("nu", "apostrophe"))
    assert len(differences) == 1
    assert differences[0]["path"] == "generator.decoration"


def test_assessment_keeps_sources_separate_from_proven_inference() -> None:
    sample = {locator: {"count": 1} for locator in audit.LOCATORS}
    rows = audit.requirement_assessment(
        sample, double_present=True, hopf_present=True, cyclic_expansions=0,
    )
    assert len(rows) == 8
    assert rows[4]["key"] == "nu_prime_hopf"
    assert rows[5]["key"] == "nu_prime_double"
    assert all(row["certified_as_completed_inference"] is False for row in rows)
    assert rows[-1]["screened_fixed_given_count"] == 0


def test_assessment_reports_absent_prop22_source_without_claiming_proof() -> None:
    sample = {locator: {"count": 0} for locator in audit.LOCATORS}
    rows = audit.requirement_assessment(
        sample, double_present=True, hopf_present=True, cyclic_expansions=2,
    )
    assert rows[0]["key"] == "prop22_hopf_composition"
    assert rows[0]["screened_fixed_given_count"] == 0
    assert "候補" in rows[-1]["note"]


def test_dry_run_preserves_snapshot_and_does_not_load_proof_engine(monkeypatch, tmp_path: Path, capsys) -> None:
    before = {"branch": "develop", "head": "dummy", "tracked_diff_sha256": "hash", "status": [" M source.py"]}
    monkeypatch.setattr(audit, "snapshot", lambda root: before.copy())
    assert audit.run(tmp_path, dry_run=True, search=False) == 0
    output = capsys.readouterr().out
    assert "PHASE171_R2F_RESULT=PASS_AUDIT_ONLY" in output
    assert "PHASE171_R2F_DRY_RUN=PASS" in output


def test_dry_run_fails_closed_when_snapshot_changes(monkeypatch, tmp_path: Path) -> None:
    calls = iter((
        {"branch": "develop", "head": "a", "tracked_diff_sha256": "one"},
        {"branch": "develop", "head": "a", "tracked_diff_sha256": "two"},
    ))
    monkeypatch.setattr(audit, "snapshot", lambda root: next(calls))
    with pytest.raises(RuntimeError, match="worktree changed"):
        audit.run(tmp_path, dry_run=True, search=False)
```

### run.ps1

```powershell
param(
    [switch] $DryRun,
    [switch] $Search
)
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path (Join-Path $package '..')).Path
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $repo
try {
    python -B -m phase171_r2f_pi63_extension_gap_audit.audit --root $repo --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_DRY_RUN_FAILED' }
    if ($DryRun.IsPresent) { return }
    $tests = @(
        'phase171_r2f_pi63_extension_gap_audit/tests/test_audit.py',
        'phase171_r2e_toda53_double_source/tests/test_source.py',
        'phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py',
        'test_phase165_r52_r9_shared_math.py'
    )
    python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider @tests
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R2F_FOCUSED_PYTEST=PASS'
    $argsAudit = @('-B', '-m', 'phase171_r2f_pi63_extension_gap_audit.audit', '--root', $repo)
    if ($Search.IsPresent) { $argsAudit += '--search' }
    & python @argsAudit
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_AUDIT_FAILED' }
}
finally {
    Pop-Location
}
```

### README.md

```markdown
# Phase 171 R2F: Typed Extension Gap Audit

This package is a read-only diagnostic for the proposed proof of the 2-primary cyclic structure of pi_6(S^3). It does not patch application code, register new literature, add ProofSteps, or claim to prove the target.

The diagnostic inspects the current local `develop` checkout, including existing uncommitted R2E changes. It verifies that the (5.3) Hopf and doubling equalities survive publication-order citation screening, compares the DB generator structurally with the cited generator, inspects the root and cyclic-structure backward expansions, and inventories source requirements from Proposition 2.2, Proposition 4.2 (4.4), (5.2), and Proposition 5.3. It can optionally run the existing registered group search.

Run `run.ps1 -DryRun` for a read-only Git-state preflight. Run `run.ps1` for focused pytest plus typed diagnostics, or `run.ps1 -Search` to additionally execute the existing proof search. The report is written outside the repository under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2f_*\audit.json`.

An existing source statement, a backward expansion, and a complete inference are different things. In particular, the report's prerequisite inventory does not certify a group proof. All repository file edits, checkout, reset, and automated Git synchronization are out of scope.
```

### 監査仕様.md

```markdown
# Phase 171 R2F — π₆³ の位数4・生成性を接続するための読み取り専用監査

## 目的

R2E の $2\nu'=\eta_3\circ\eta_4\circ\eta_5$ と既存の $H(\nu')=\eta_5$ が、publication precedence に基づく選別後も出典付き GIVEN として残ることを確認する。

さらに、DB Goal の生成元と (5.3) の $\nu'$ の型付き差分、$CyclicStructureStatement(\pi_6^3,\nu',4)$ の逆向き推論候補、および次の不足中間目標を記録する。

1. Proposition 2.2 を利用する $H(\nu'\circ\eta_6)=\eta_5^2$ の型付き導出。
2. Proposition 5.3 および (5.2) からの $\pi_5^2\cong\mathbb Z/2\{\eta_2^3\}$ と $\pi_7^5\cong\mathbb Z/2\{\eta_5^2\}$。
3. EHP 完全列の $H:\pi_7^3\to\pi_7^5$ の全射、$E:\pi_5^2\to\pi_6^3$ の単射、$H:\pi_6^3\to\pi_6^5$ の全射。
4. $E(\eta_2^3)=\eta_3\eta_4\eta_5$ の型付き接続。
5. $0\to\mathbb Z/2\to\pi_6^3\to\mathbb Z/2\to0$ から4元を導き、$2\nu'\ne0$ から位数4と生成性を導く一般的推論。

## 信頼境界

対象の Proposition 5.6 を GIVEN に追加しない。未確定の `(5.6)?` を引用しない。DB の生成元を文字列だけで同一視しない。監査結果は Proof Tree 完了の証明ではない。

## 変更対象

アプリの既存ファイル、既存クラス、既存関数、既存テストの変更はない。

新規：`audit.py`（Git 状態、出典、型、逆向き推論候補の観察）、`tests/test_audit.py`（限定単体テスト）、`run.ps1`、本監査文書、`README.md`。

実行後の JSON は `%LOCALAPPDATA%/EHPProofTracerRecovery/phase171_r2f_*/audit.json` に保存する。

## 完了境界

監査が成功しても、π₆³ の完成証明が生成されたことにはならない。数学的前提の検証と最小の推論規則は別の実装判断として残す。全体 pytest は Phase 171 の終了時に限る。
```

### __init__.py

```python
"""Phase 171 R2F read-only extension proof frontier audit."""
```

### tests/__init__.py

```python
"""Targeted audit tests only."""
```

## 限定 pytest

この配布環境で監査コードの独立テスト7件 PASS。リポジトリ固有のテストはユーザー環境で `run.ps1` が実行する。

## 完了条件

R2E と Hopf の出典付き GIVEN を各1件確認、出典順序が正当、DB 元との型付き差分・既存展開・不足前提を報告、実行前後の Git 状態が完全一致。監査によって証明は完成しない。

## 次段階との境界

Proposition 2.2 の型付き関係、EHP の核・像、短完全列の位数計算および生成性の一般的推論が独立に検証されるまでは、数学的な新規 INFERENCE も Proof Tree の完成宣言も行わない。
