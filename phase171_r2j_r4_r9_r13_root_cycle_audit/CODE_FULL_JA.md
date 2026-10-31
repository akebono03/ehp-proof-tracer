# Phase 171 R13 — 新規コード・関連テスト全文

既存ファイル・関数・クラスは変更しない。`audit.py` の新規関数および新規クラスの追加位置は新規ディレクトリ直下。既存 import の変更はない。

## `audit.py`

```python
"""Read-only diagnosis of root-search equality symmetry recursion.

The wrapper returns the original provider's candidate tuple unchanged. It
observes the existing canonical resolver's active and solved goals via Python
frames, but never alters the resolver, ProofSteps, rules, or registry.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable
from unittest.mock import patch

import phase165_r52_r9_shared_math as shared_math
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _checked_chain, _screened_context
from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import reverse_equality
from phase171_r2j_r4_r9_r12_public_symmetry_diagnostic.audit import (
    git_read,
    preflight,
)

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output" / "audit.json"
MAX_EVENTS = 120


def same_statement(left: object, right: object) -> bool:
    """Use the same equality convention as the canonical proof search."""
    return type(left) is type(right) and left == right


def goal_role(goal: object, root: object, forward: object, reverse: object) -> str | None:
    """Classify only the three concrete goals under this diagnosis."""
    if same_statement(goal, root):
        return "root"
    if same_statement(goal, forward):
        return "forward"
    if same_statement(goal, reverse):
        return "reverse"
    return None


def resolution_stack_snapshot(
    frame: object,
    root: object,
    forward: object,
    reverse: object,
) -> dict:
    """Read the active resolver stack without modifying any resolver local.

    Only an actual frame from phase165_r3_recursive_search.resolve qualifies;
    unrelated stack frames never receive authority as proof evidence.
    """
    current = frame
    while current is not None:
        code = getattr(current, "f_code", None)
        globals_dict = getattr(current, "f_globals", {})
        if (
            getattr(code, "co_name", None) == "resolve"
            and globals_dict.get("__name__") == "phase165_r3_recursive_search"
        ):
            local = current.f_locals
            active = local.get("active", ())
            solved = local.get("solved", ())
            if not isinstance(active, (tuple, list)) or not isinstance(solved, (tuple, list)):
                raise RuntimeError("unexpected canonical resolver state")
            roles = [goal_role(item, root, forward, reverse) or "other" for item in active]
            solved_goals = [entry[0] for entry in solved if isinstance(entry, tuple) and len(entry) == 2]
            return {
                "resolver_found": True,
                "active_depth": len(active),
                "active_roles": roles,
                "root_active": any(same_statement(item, root) for item in active),
                "forward_active": any(same_statement(item, forward) for item in active),
                "reverse_active": any(same_statement(item, reverse) for item in active),
                "forward_solved": any(same_statement(item, forward) for item in solved_goals),
                "reverse_solved": any(same_statement(item, reverse) for item in solved_goals),
            }
        current = getattr(current, "f_back", None)
    return {
        "resolver_found": False,
        "active_depth": 0,
        "active_roles": [],
        "root_active": False,
        "forward_active": False,
        "reverse_active": False,
        "forward_solved": False,
        "reverse_solved": False,
    }


def classify_trace(public_status: str, events: list[dict]) -> str:
    """Classify observed routing, not mathematical completeness."""
    if public_status == "complete":
        return "ROOT_COMPLETE_REQUIRES_TRUST_BOUNDARY"
    reverses = [item for item in events if item["role"] == "reverse"]
    if not reverses:
        return "REVERSE_NOT_VISITED_IN_PUBLIC_ROOT"
    if any(
        item["stack"]["forward_active"]
        and item["symmetry_exact"] == 1
        and item["routes_total"] == 1
        for item in reverses
    ):
        return "REVERSE_SYMMETRY_CYCLE_WITH_ACTIVE_FORWARD"
    if any(item["symmetry_exact"] == 0 for item in reverses):
        return "REVERSE_ROUTE_MISSING_IN_ROOT_CONTEXT"
    if any(item["routes_total"] > 1 for item in reverses):
        return "MULTIPLE_REVERSE_ROUTES_REQUIRE_AMBIGUITY_AUDIT"
    return "ROOT_PARTIAL_WITHOUT_OBSERVED_DIRECT_SYMMETRY_CYCLE"


class ProviderFactoryObserver:
    """Wrap only the existing root provider, preserving its exact results."""

    def __init__(
        self,
        factory: Callable,
        root: object,
        forward: object,
        reverse: object,
    ) -> None:
        if not callable(factory):
            raise TypeError("factory must be callable")
        self.factory = factory
        self.root = root
        self.forward = forward
        self.reverse = reverse
        self.root_provider_instances = 0
        self.focus_calls = {"root": 0, "forward": 0, "reverse": 0}
        self.events: list[dict] = []
        self.dropped_events = 0

    def __call__(self, *args, **kwargs):
        provider = self.factory(*args, **kwargs)
        if not callable(provider):
            raise TypeError("shared provider factory returned a noncallable")
        if not same_statement(kwargs.get("proof_target"), self.root):
            return provider
        self.root_provider_instances += 1

        def observed(goal: object):
            role = goal_role(goal, self.root, self.forward, self.reverse)
            if role is None:
                return provider(goal)
            self.focus_calls[role] += 1
            stack = resolution_stack_snapshot(
                sys._getframe(1), self.root, self.forward, self.reverse,
            )
            routes = provider(goal)
            if not isinstance(routes, tuple):
                raise TypeError("provider contract violated")
            if len(self.events) < MAX_EVENTS:
                matching = sum(
                    getattr(item.rule, "name", None) == "equality symmetry"
                    and item.subgoals == (self.forward,)
                    for item in routes
                )
                self.events.append({
                    "role": role,
                    "stack": stack,
                    "routes_total": len(routes),
                    "symmetry_exact": matching,
                    "rules": [str(getattr(item.rule, "name", "<unnamed>")) for item in routes[:15]],
                })
            else:
                self.dropped_events += 1
            return routes

        return observed


def inspect_public_root() -> dict:
    """Observe the authentic public group search through a temporary wrapper."""
    original_bridge = shared_math.build_shared_typed_bridge()
    screened, root, citing = _screened_context()
    chain, _available = _checked_chain(screened, citing)
    forward = chain.alpha_composition
    reverse = reverse_equality(forward)
    if reverse is None:
        raise RuntimeError("R11 has no reverse equality to diagnose")
    observer = ProviderFactoryObserver(
        shared_math.shared_expansion_provider, root, forward, reverse,
    )
    contexts: list[object] = []
    with patch.object(shared_math, "shared_expansion_provider", observer):
        public = search_group_from_registered_goal(
            n=3,
            k=3,
            bridge=original_bridge,
            goal=root,
            context_sink=contexts.append,
        )
    if len(contexts) != 1:
        raise RuntimeError("public search did not expose a unique root context")
    public_chain, _ = _checked_chain(contexts[0], citing)
    if public_chain.alpha_composition != forward:
        raise RuntimeError("public context disagrees with the screened R11 equality")
    first_open = public.open_goals[0] if public.open_goals else None
    return {
        "phase": "171-R2J-R4-R9-R13",
        "mode": "ROOT_STACK_AUDIT_ONLY",
        "root_goal": repr(root),
        "forward_goal": repr(forward),
        "reverse_goal": repr(reverse),
        "public_search_status": public.status.value,
        "public_open_count": len(public.open_goals),
        "public_proven_steps": len(public.proven_steps),
        "first_open_is_reverse": first_open is not None and same_statement(first_open, reverse),
        "public_diagnostics": list(public.diagnostics[:10]),
        "root_provider_instances": observer.root_provider_instances,
        "focus_calls": observer.focus_calls,
        "events": observer.events,
        "dropped_events": observer.dropped_events,
        "classification": classify_trace(public.status.value, observer.events),
        "new_given_added": 0,
        "existing_source_modified": False,
        "completed_proof_replayed": False,
        "full_pytest": False,
        "web_verified": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    pre = preflight()
    print("PHASE171_R13_BRANCH=" + pre["branch"], flush=True)
    print("PHASE171_R13_HEAD=" + pre["head"], flush=True)
    print("PHASE171_R13_R11_BASELINE=PASS", flush=True)
    if args.dry_run:
        print("PHASE171_R13_RESULT=PASS_DRY_RUN", flush=True)
        return
    before = git_read("status", "--porcelain", "--untracked-files=no")
    report = inspect_public_root()
    after = git_read("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("tracked source changed during root audit")
    report["git_head"] = pre["head"]
    report["tracked_status_unchanged"] = True
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R13_PUBLIC_SEARCH=" + report["public_search_status"], flush=True)
    print("PHASE171_R13_FIRST_OPEN_IS_REVERSE=" + str(report["first_open_is_reverse"]), flush=True)
    print("PHASE171_R13_FOCUS_CALLS=" + json.dumps(report["focus_calls"], ensure_ascii=False), flush=True)
    print("PHASE171_R13_ROOT_PROVIDER_INSTANCES=" + str(report["root_provider_instances"]), flush=True)
    print("PHASE171_R13_CLASSIFICATION=" + report["classification"], flush=True)
    print("PHASE171_R13_NEW_GIVEN=0", flush=True)
    print("PHASE171_R13_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R13_REPORT=" + str(OUTPUT), flush=True)
    print("PHASE171_R13_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py`

```python
"""Nonmutating R13 wrapper and canonical-stack regression tests."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase171_r2j_r4_r9_r13_root_cycle_audit.audit import (
    ProviderFactoryObserver,
    classify_trace,
    goal_role,
    resolution_stack_snapshot,
    same_statement,
)
from phase171_r2j_r4_r9_r12_public_symmetry_diagnostic.audit import (
    git_read,
    preflight,
)
from proof import Relation, RelationType
from phase165_r3_recursive_search import GoalExpansion
from relation_rules import equality_symmetry_inference_rule


def _goals():
    root = Relation("G", "C4", RelationType.EQUALITY)
    forward = Relation("a", "b", RelationType.EQUALITY)
    reverse = Relation("b", "a", RelationType.EQUALITY)
    return root, forward, reverse


def _fake_frame(name, module, locals_dict, back=None):
    return SimpleNamespace(
        f_code=SimpleNamespace(co_name=name),
        f_globals={"__name__": module},
        f_locals=locals_dict,
        f_back=back,
    )


def test_stack_snapshot_reports_active_forward_cycle_without_mutating_state():
    root, forward, reverse = _goals()
    active = [root, forward, reverse]
    solved = [(Relation("x", "x", RelationType.EQUALITY), object())]
    real = _fake_frame(
        "resolve", "phase165_r3_recursive_search", {"active": active, "solved": solved},
    )
    wrapper = _fake_frame("observed", "phase171_r2j_r4_r9_r13_root_cycle_audit.audit", {}, real)
    before = tuple(active)
    result = resolution_stack_snapshot(wrapper, root, forward, reverse)
    assert result["resolver_found"] is True
    assert result["active_roles"] == ["root", "forward", "reverse"]
    assert result["forward_active"] is True
    assert result["reverse_active"] is True
    assert result["forward_solved"] is False
    assert tuple(active) == before
    assert len(solved) == 1


def test_stack_snapshot_does_not_trust_noncanonical_resolver():
    root, forward, reverse = _goals()
    impostor = _fake_frame("resolve", "unrelated_module", {"active": [root, forward, reverse]})
    result = resolution_stack_snapshot(impostor, root, forward, reverse)
    assert result["resolver_found"] is False
    assert result["active_roles"] == []
    assert result["forward_active"] is False


def test_root_provider_observer_preserves_identity_order_and_subgoals():
    root, forward, reverse = _goals()
    candidate = GoalExpansion(equality_symmetry_inference_rule(), (forward,))
    calls = []

    def factory(*args, **kwargs):
        calls.append(kwargs.get("proof_target"))

        def provider(goal):
            return (candidate,)

        return provider

    watcher = ProviderFactoryObserver(factory, root, forward, reverse)
    observed = watcher(proof_target=root)
    result = observed(reverse)
    assert result is not None and result[0] is candidate
    assert calls == [root]
    assert watcher.root_provider_instances == 1
    assert watcher.focus_calls["reverse"] == 1
    assert watcher.events[0]["symmetry_exact"] == 1
    assert watcher.events[0]["routes_total"] == 1
    assert watcher.events[0]["stack"]["resolver_found"] is False
    unobserved = watcher(proof_target=forward)
    assert unobserved(reverse) == (candidate,)
    assert watcher.root_provider_instances == 1


def test_classification_distinguishes_cycle_missing_and_ambiguous():
    stack = {"forward_active": True}
    cycle = {"role": "reverse", "stack": stack, "symmetry_exact": 1, "routes_total": 1}
    assert classify_trace("partial", [cycle]) == "REVERSE_SYMMETRY_CYCLE_WITH_ACTIVE_FORWARD"
    assert classify_trace("partial", []) == "REVERSE_NOT_VISITED_IN_PUBLIC_ROOT"
    missing = {"role": "reverse", "stack": stack, "symmetry_exact": 0, "routes_total": 1}
    assert classify_trace("partial", [missing]) == "REVERSE_ROUTE_MISSING_IN_ROOT_CONTEXT"
    ambiguous = {"role": "reverse", "stack": stack, "symmetry_exact": 1, "routes_total": 2}
    assert classify_trace("partial", [ambiguous]) == "MULTIPLE_REVERSE_ROUTES_REQUIRE_AMBIGUITY_AUDIT"
    assert classify_trace("complete", [cycle]) == "ROOT_COMPLETE_REQUIRES_TRUST_BOUNDARY"


def test_statement_roles_match_by_typed_value_not_text():
    root, forward, reverse = _goals()
    assert same_statement(root, root)
    assert not same_statement(root, "G")
    assert goal_role(root, root, forward, reverse) == "root"
    assert goal_role(forward, root, forward, reverse) == "forward"
    assert goal_role(reverse, root, forward, reverse) == "reverse"
    assert goal_role(object(), root, forward, reverse) is None


def test_reviewed_baseline_and_read_only_guard():
    assert preflight()["shared_provider_blob"] == "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"
    with pytest.raises(ValueError, match="read-only"):
        git_read("reset", "--hard")
```

## `run.ps1`

```powershell
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ModuleName = 'phase171_r2j_r4_r9_r13_root_cycle_audit'
Push-Location $RepoRoot
try {
    $GitBranch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $GitBranch -ne 'develop') {
        throw 'R13 requires Git develop. No source was modified.'
    }
    $GitHead = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not read Git HEAD.'
    }
    Write-Output "PHASE171_R13_BRANCH=$GitBranch"
    Write-Output "PHASE171_R13_HEAD=$GitHead"

    if ($DryRun) {
        python -m "$ModuleName.audit" --dry-run
        if ($LASTEXITCODE -ne 0) {
            throw 'R13 preflight failed.'
        }
        Write-Output 'PHASE171_R13_DRY_RUN=PASS'
        return
    }

    python -m "$ModuleName.audit" --dry-run
    if ($LASTEXITCODE -ne 0) {
        throw 'R13 source baseline check failed; audit cancelled.'
    }
    Write-Output 'PHASE171_R13_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider "$ModuleName/tests/test_audit.py"
    if ($LASTEXITCODE -ne 0) {
        throw 'R13 focused pytest failed; audit cancelled.'
    }
    Write-Output 'PHASE171_R13_FOCUSED_PYTEST=PASS'

    python -m "$ModuleName.audit"
    if ($LASTEXITCODE -ne 0) {
        throw 'R13 root diagnosis failed.'
    }
    git status -sb
    if ($LASTEXITCODE -ne 0) {
        throw 'Git status query failed.'
    }
    git diff --stat
    if ($LASTEXITCODE -ne 0) {
        throw 'Git diff query failed.'
    }
    Write-Output 'PHASE171_R13_RESULT=PASS_READ_ONLY_ROOT_AUDIT'
}
finally {
    Pop-Location
}
```

## `README.md`

```markdown
# Phase 171 R2J-R4-R9-R13: Public Root Search Recursion Audit

This is a read-only audit of equality-symmetry dependencies in the real public proof search for `pi_6^3`.

The R12 audit established that both orientations of the first unresolved equality are individually reconstructible, while the complete public root search is still partial. R13 observes the canonical recursive searcher's *active* and *solved* goals at the moment the equality goals are expanded. It distinguishes an active forward-goal cycle from missing routes, ambiguity, and unrelated root failures.

The package uses the R12 audit's reviewed baseline check and must be unpacked alongside the existing R12 package. The real `shared_expansion_provider` function is temporarily wrapped in-process during one ordinary public search. The wrapper returns every proposal without reordering or mutation and is restored even if the search raises an error.

**No repository source file is modified. No new GIVEN or inference rule is added. No completed proof tree is reused.** The audit JSON alone is written under this package's `output` directory.

## Windows PowerShell

From the repository root, after extracting the ZIP there:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r13_root_cycle_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r13_root_cycle_audit\run.ps1"
```

The targeted pytest uses `-p no:cacheprovider` to avoid updating `.pytest_cache/v/cache/nodeids`. Existing changes to that tracked file from earlier runs are not touched.

## Result classification

`REVERSE_SYMMETRY_CYCLE_WITH_ACTIVE_FORWARD` means the forward equality is already active in the canonical resolver when it is requested as the only premise of the inverse equality. `MULTIPLE_REVERSE_ROUTES_REQUIRE_AMBIGUITY_AUDIT` means competing inverse proposals were observed. Other classifications are recorded literally; no classification alone establishes a complete proof.

The next change, if any, must be justified by the JSON trace and a separate minimal patch. Do not treat a `partial` result as a completed Web proof.
```

## `監査仕様.md`

```markdown
# Phase 171 R2J-R4-R9-R13 監査仕様

## 出発点

- R12 の限定 pytest は 5 PASS。
- 共通 Provider による順向き・逆向きの等式は単独では `proved`。
- 対称律候補は direct、merge、Root gate、本番 Provider のすべてで 1 件。
- しかし公開探索は `partial` のまま。

## 変更対象

既存ファイル・既存クラス・既存関数：変更なし。

新規ファイルは `phase171_r2j_r4_r9_r13_root_cycle_audit/` 以下の `audit.py`、`tests/test_audit.py`、`run.ps1`、`README.md`、`監査仕様.md`、`CODE_FULL_JA.md`、`__init__.py`、`tests/__init__.py`。

## 監査方法

1. Git `develop` と R11 の共有 Provider blob を検査する。R12 監査パッケージを利用する。
2. 公開探索の `shared_expansion_provider` を、プロセス内に限って一時的に観測ラッパーで包む。ラッパーは候補 tuple を一切変更しない。
3. `reconstruct_registered_goal()` の内部 `resolve()` の active / solved を、フレーム参照で読み取る。注目するのは群構造の Root Goal と、最初の順・逆向き等式のみ。
4. 対称律が唯一の候補なのに順向き Goal が `active` である場合、循環依存を検出する。提案数が複数ある場合は曖昧性監査と区別する。
5. `output/audit.json` に保存し、通常の公開 Web 完成を主張しない。

## pytest と完了条件

`python -m pytest -q -p no:cacheprovider phase171_r2j_r4_r9_r13_root_cycle_audit/tests/test_audit.py`

- 限定テスト 6 件が PASS する。
- 既存 Provider・探索器のコードを変更せず、公開探索の注目 Goal の active stack が採取される。
- 新規 `GIVEN` は 0。既存の完成 Proof Tree は再利用しない。
- 本 Phase では全体 pytest を実行しない。

## 次の境界

R13 は監査のみ。結果が循環依存なら、その一般的な原因に対する最小変更を別段階で設計する。型付き証明の検証、引用文献の制約、Trust Boundary は変更しない。
```

## `__init__.py`

```python
"""Phase 171 R13 public-root recursion diagnostic package."""
```

## `tests/__init__.py`

```python
"""Tests for the read-only R13 root recursion audit."""
```

