# Phase 171 R2J-R4-R9-R14 — 追加コード・テスト全文

既存ソース・既存クラス・既存関数・既存 import の変更はありません。新規パッケージはリポジトリ直下に追加します。以下はすべて省略なしの全文です。

## `audit.py`

```python
"""Phase 171 R14: inspect canonical root-search branch failures without changes.

Python's temporary trace hook watches exceptions raised by the original
`reconstruct_registered_goal.resolve`.  It does not replace the resolver, alter
any GoalExpansion, manufacture a ProofStep, or mark a source as GIVEN.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from types import FrameType
from typing import Any, Callable
from unittest.mock import patch

import phase165_r52_r9_shared_math as shared_math
from phase165_r3_recursive_search import RegisteredGoalUnresolved
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _checked_chain, _screened_context
from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import reverse_equality

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output" / "audit.json"
SOURCE = ROOT / "phase165_r52_r9_shared_math.py"
SOURCE_NAME = "phase165_r52_r9_shared_math.py"
REVIEWED_PROVIDER_BLOB = "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"
MAX_EXCEPTIONS = 450
MAX_CALLS = 240
MAX_REPR = 850


def git_read(*args: str) -> bytes:
    """Allow only read-only Git queries needed to verify the known baseline."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("show", "HEAD:" + SOURCE_NAME),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if args not in allowed:
        raise ValueError("R14 refuses a non-read-only Git command")
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=True,
    ).stdout


def preflight() -> dict[str, str]:
    """Refuse a branch or tracked provider different from committed R11."""
    branch = git_read("branch", "--show-current").decode("utf-8").strip()
    head = git_read("rev-parse", "HEAD").decode("utf-8").strip()
    committed = git_read("show", "HEAD:" + SOURCE_NAME)
    digest = hashlib.sha1(
        ("blob %d\0" % len(committed)).encode("ascii") + committed,
    ).hexdigest()
    if branch != "develop":
        raise RuntimeError("develop branch required")
    if digest != REVIEWED_PROVIDER_BLOB:
        raise RuntimeError("R11 reviewed provider blob differs from HEAD: " + digest)
    local = SOURCE.read_bytes()
    if local.decode("utf-8-sig").replace("\r\n", "\n") != committed.decode("utf-8-sig").replace("\r\n", "\n"):
        raise RuntimeError("worktree provider differs from HEAD")
    return {"branch": branch, "head": head, "provider_blob": digest}


def same(left: object, right: object) -> bool:
    """Use the exact goal equality relation of the canonical resolver."""
    return type(left) is type(right) and left == right


def role(goal: object, root: object, forward: object, reverse: object) -> str:
    """Name only three inspected goals, not any inferred mathematical type."""
    if same(goal, root):
        return "root"
    if same(goal, forward):
        return "forward"
    if same(goal, reverse):
        return "reverse"
    return "other"


def short(value: object, limit: int = MAX_REPR) -> str:
    """Bound JSON report size without changing statement equality."""
    return repr(value)[:limit]


def classify_error(message: str) -> str:
    """Separate true cycles, zero derivations, and uniqueness failures."""
    if message == "cyclic proof dependency":
        return "cycle"
    match = re.search(r"found (\d+)\Z", message)
    if match:
        count = int(match.group(1))
        if count == 0:
            return "no_derivation"
        if count > 1:
            return "ambiguous_derivations"
    return "other_unresolved"


class CanonicalResolveTrace:
    """Observe original recursive-search exceptions via temporary sys.settrace.

    An 'origin' event is the deepest traceback frame at the moment the
    RegisteredGoalUnresolved exception is raised; 'propagated' means a parent
    expansion received the child's failure. Both are diagnostic, not proof.
    """

    def __init__(
        self, root: object, forward: object, reverse: object,
        *, target_module: str = "phase165_r3_recursive_search",
    ) -> None:
        self.root = root
        self.forward = forward
        self.reverse = reverse
        self.target_module = target_module
        self.exceptions: list[dict[str, Any]] = []
        self.exception_totals: Counter[str] = Counter()
        self.origin_totals: Counter[str] = Counter()
        self.dropped = 0
        self.calls = 0
        self._previous: Callable | None = None

    def __enter__(self) -> "CanonicalResolveTrace":
        self._previous = sys.gettrace()
        if self._previous is not None:
            raise RuntimeError("an existing trace/debugger must not be replaced")
        sys.settrace(self._global)
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        sys.settrace(self._previous)

    def _global(self, frame: FrameType, event: str, arg: Any):
        if (event == "call" and frame.f_code.co_name == "resolve"
                and frame.f_globals.get("__name__") == self.target_module):
            self.calls += 1
            return self._local
        return None

    def _local(self, frame: FrameType, event: str, arg: Any):
        if event != "exception":
            return self._local
        exception_type, exception, traceback = arg
        if not issubclass(exception_type, RegisteredGoalUnresolved):
            return self._local
        deepest = traceback
        while deepest is not None and deepest.tb_next is not None:
            deepest = deepest.tb_next
        originated = deepest is not None and deepest.tb_frame is frame
        kind = classify_error(str(exception))
        self.exception_totals[kind] += 1
        if originated:
            self.origin_totals[kind] += 1
        if len(self.exceptions) >= MAX_EXCEPTIONS:
            self.dropped += 1
            return self._local
        loc = frame.f_locals
        expansion = loc.get("expansion")
        current = loc.get("target")
        active = loc.get("active", ())
        if not isinstance(active, (tuple, list)):
            active = ()
        options = loc.get("options")
        if not isinstance(options, (tuple, list)):
            options = ()
        self.exceptions.append({
            "origin": originated,
            "kind": kind,
            "message": str(exception)[:1100],
            "line": frame.f_lineno,
            "target_role": role(current, self.root, self.forward, self.reverse),
            "target": short(current),
            "active_roles": [role(item, self.root, self.forward, self.reverse) for item in active],
            "active_last": [short(item, 360) for item in active[-4:]],
            "candidate_rule": str(getattr(getattr(expansion, "rule", None), "name", ""))[:140],
            "candidate_subgoals": [short(goal, 450) for goal in getattr(expansion, "subgoals", ())[:8]],
            "accepted_options_so_far": len(options),
        })
        return self._local


class ExactProviderObserver:
    """Record provider candidates but return their original tuple unchanged."""

    def __init__(self, original: Callable, root: object, forward: object, reverse: object) -> None:
        self.original = original
        self.root = root
        self.forward = forward
        self.reverse = reverse
        self.providers = 0
        self.calls = 0
        self.events: list[dict] = []
        self.dropped = 0

    def __call__(self, *args, **kwargs):
        provider = self.original(*args, **kwargs)
        if not callable(provider):
            raise TypeError("provider factory returned non-callable")
        if not same(kwargs.get("proof_target"), self.root):
            return provider
        self.providers += 1

        def observe(goal: object):
            expansions = provider(goal)
            if not isinstance(expansions, tuple):
                raise TypeError("provider returned non-tuple")
            self.calls += 1
            if len(self.events) < MAX_CALLS:
                self.events.append({
                    "role": role(goal, self.root, self.forward, self.reverse),
                    "goal": short(goal, 500),
                    "count": len(expansions),
                    "rules": [str(getattr(item.rule, "name", ""))[:150] for item in expansions[:25]],
                    "proposals": [
                        {"rule": str(getattr(item.rule, "name", ""))[:140],
                         "subgoals": [short(x, 450) for x in item.subgoals[:6]]}
                        for item in expansions[:12]
                    ],
                })
            else:
                self.dropped += 1
            return expansions

        return observe


def summarize(report: dict) -> str:
    """Classify observation conservatively: cycles alone do not prove causality."""
    if report["public_status"] == "complete":
        return "ROOT_COMPLETE_REQUIRES_TRUST_BOUNDARY"
    origin = report["origin_counts"]
    if origin.get("ambiguous_derivations", 0):
        return "ROOT_PARTIAL_AMBIGUITY_OBSERVED"
    if origin.get("no_derivation", 0):
        return "ROOT_PARTIAL_WITH_ZERO_DERIVATION_SUBGOALS"
    if origin.get("cycle", 0):
        return "ROOT_PARTIAL_WITH_CYCLE_ONLY_OBSERVED"
    return "ROOT_PARTIAL_WITHOUT_CLASSIFIED_CANONICAL_FAILURE"


def inspect_root() -> dict:
    """Trace the genuine n=3, k=3 public search, with zero source changes."""
    bridge = shared_math.build_shared_typed_bridge()
    screened, root, citing = _screened_context()
    chain, _ = _checked_chain(screened, citing)
    forward = chain.alpha_composition
    reverse = reverse_equality(forward)
    if reverse is None:
        raise RuntimeError("no R11 reverse goal")
    observed = ExactProviderObserver(
        shared_math.shared_expansion_provider, root, forward, reverse,
    )
    trace = CanonicalResolveTrace(root, forward, reverse)
    contexts: list = []
    with patch.object(shared_math, "shared_expansion_provider", observed):
        with trace:
            public = search_group_from_registered_goal(
                n=3, k=3, bridge=bridge, goal=root,
                context_sink=contexts.append,
            )
    if len(contexts) != 1:
        raise RuntimeError("public search did not expose exactly one context")
    actual_chain, _ = _checked_chain(contexts[0], citing)
    if actual_chain.alpha_composition != forward:
        raise RuntimeError("public and cited goal identity differ")
    root_routes = [x for x in observed.events if x["role"] == "root"]
    first_open = public.open_goals[0] if public.open_goals else None
    report = {
        "phase": "171-R2J-R4-R9-R14",
        "mode": "READ_ONLY_CANONICAL_BRANCH_EXCEPTION_TRACE",
        "root": short(root),
        "forward": short(forward),
        "reverse": short(reverse),
        "public_status": public.status.value,
        "first_open_is_reverse": first_open is not None and same(first_open, reverse),
        "public_open_count": len(public.open_goals),
        "public_proven_steps": len(public.proven_steps),
        "public_diagnostics": list(public.diagnostics[:10]),
        "root_provider_instances": observed.providers,
        "provider_calls": observed.calls,
        "provider_events": observed.events,
        "provider_events_dropped": observed.dropped,
        "root_route_count": root_routes[0]["count"] if len(root_routes) == 1 else None,
        "resolver_calls": trace.calls,
        "exception_counts": dict(trace.exception_totals),
        "origin_counts": dict(trace.origin_totals),
        "exception_events": trace.exceptions,
        "exception_events_dropped": trace.dropped,
        "new_given": 0,
        "source_changes": 0,
        "completed_proof_imported": False,
        "trust_boundary_modified": False,
        "full_pytest": False,
        "public_web_verified": False,
    }
    report["classification"] = summarize(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ready = preflight()
    print("PHASE171_R14_BRANCH=" + ready["branch"], flush=True)
    print("PHASE171_R14_HEAD=" + ready["head"], flush=True)
    print("PHASE171_R14_R11_BASELINE=PASS", flush=True)
    if args.dry_run:
        print("PHASE171_R14_RESULT=PASS_DRY_RUN", flush=True)
        return
    before = git_read("status", "--porcelain", "--untracked-files=no")
    report = inspect_root()
    after = git_read("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("tracked source changed during R14 read-only audit")
    report.update({"git_head": ready["head"], "tracked_status_unchanged": True})
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R14_PUBLIC_SEARCH=" + report["public_status"], flush=True)
    print("PHASE171_R14_ROOT_ROUTES=" + str(report["root_route_count"]), flush=True)
    print("PHASE171_R14_RESOLVER_CALLS=" + str(report["resolver_calls"]), flush=True)
    print("PHASE171_R14_ORIGIN_COUNTS=" + json.dumps(report["origin_counts"], ensure_ascii=False), flush=True)
    print("PHASE171_R14_CLASSIFICATION=" + report["classification"], flush=True)
    print("PHASE171_R14_NEW_GIVEN=0", flush=True)
    print("PHASE171_R14_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R14_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R14_REPORT=" + str(OUTPUT), flush=True)
    print("PHASE171_R14_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py`

```python
"""Focused tests for read-only branch diagnostics and exception classification."""
from __future__ import annotations

import sys

import pytest

from phase165_r3_recursive_search import GoalExpansion, RegisteredGoalUnresolved
from phase171_r2j_r4_r9_r14_root_branch_diagnostic.audit import (
    CanonicalResolveTrace,
    ExactProviderObserver,
    classify_error,
    git_read,
    preflight,
    role,
    same,
    summarize,
)
from proof import Relation, RelationType
from relation_rules import equality_symmetry_inference_rule


def _targets():
    root = Relation("G", "C4", RelationType.EQUALITY)
    forward = Relation("a", "b", RelationType.EQUALITY)
    reverse = Relation("b", "a", RelationType.EQUALITY)
    return root, forward, reverse


def test_error_classification_preserves_failure_distinction():
    assert classify_error("cyclic proof dependency") == "cycle"
    assert classify_error("expected one registered derivation for X, found 0") == "no_derivation"
    assert classify_error("expected one registered derivation for X, found 3") == "ambiguous_derivations"
    assert classify_error("unknown failure") == "other_unresolved"


def test_temporary_trace_restores_original_hook_and_records_true_origin():
    root, forward, reverse = _targets()
    namespace = {"__name__": "phase165_r3_recursive_search", "RegisteredGoalUnresolved": RegisteredGoalUnresolved}
    exec(
        "def resolve(target, active):\n"
        "    if target in active:\n"
        "        raise RegisteredGoalUnresolved('cyclic proof dependency')\n"
        "    return target\n",
        namespace,
    )
    previous = sys.gettrace()
    assert previous is None
    with CanonicalResolveTrace(root, forward, reverse) as trace:
        with pytest.raises(RegisteredGoalUnresolved, match="cyclic proof dependency"):
            namespace["resolve"](forward, [root, forward])
    assert sys.gettrace() is previous
    assert trace.calls == 1
    assert trace.origin_totals["cycle"] == 1
    assert trace.exceptions[0]["origin"] is True
    assert trace.exceptions[0]["target_role"] == "forward"


def test_trace_distinguishes_origin_from_propagation():
    root, forward, reverse = _targets()
    namespace = {"__name__": "phase165_r3_recursive_search", "RegisteredGoalUnresolved": RegisteredGoalUnresolved}
    exec(
        "def resolve(target, active):\n"
        "    if target == 'outer':\n"
        "        return resolve('inner', active)\n"
        "    raise RegisteredGoalUnresolved('expected one registered derivation for inner, found 0')\n",
        namespace,
    )
    with CanonicalResolveTrace(root, forward, reverse) as trace:
        with pytest.raises(RegisteredGoalUnresolved):
            namespace["resolve"]("outer", ["outer"])
    assert trace.calls == 2
    assert trace.origin_totals["no_derivation"] == 1
    assert trace.exception_totals["no_derivation"] >= 2
    assert any(not item["origin"] for item in trace.exceptions)


def test_provider_observer_preserves_candidate_identity_and_order():
    root, forward, reverse = _targets()
    first = GoalExpansion(equality_symmetry_inference_rule(), (forward,))
    second = GoalExpansion(equality_symmetry_inference_rule(), (reverse,))
    original = (first, second)

    def factory(*args, **kwargs):
        def provider(goal):
            return original
        return provider

    watcher = ExactProviderObserver(factory, root, forward, reverse)
    result = watcher(proof_target=root)(reverse)
    assert result is original
    assert result[0] is first
    assert result[1] is second
    assert watcher.providers == 1
    assert watcher.events[0]["count"] == 2
    assert watcher.events[0]["role"] == "reverse"
    assert watcher(proof_target=forward)(reverse) is original
    assert watcher.providers == 1


def test_goal_identity_and_report_classification_do_not_claim_completion():
    root, forward, reverse = _targets()
    assert same(root, root)
    assert not same(root, "G")
    assert role(root, root, forward, reverse) == "root"
    assert role(reverse, root, forward, reverse) == "reverse"
    assert summarize({"public_status": "partial", "origin_counts": {"cycle": 1}}) == "ROOT_PARTIAL_WITH_CYCLE_ONLY_OBSERVED"
    assert summarize({"public_status": "partial", "origin_counts": {"cycle": 2, "no_derivation": 1}}) == "ROOT_PARTIAL_WITH_ZERO_DERIVATION_SUBGOALS"
    assert summarize({"public_status": "partial", "origin_counts": {"ambiguous_derivations": 1}}) == "ROOT_PARTIAL_AMBIGUITY_OBSERVED"


def test_preflight_is_read_only_and_matches_r11_provider():
    assert preflight()["provider_blob"] == "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"
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
$Module = 'phase171_r2j_r4_r9_r14_root_branch_diagnostic'
Push-Location $RepoRoot
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
        throw 'Phase 171 R14 requires develop.'
    }
    $Head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Could not inspect HEAD.' }
    Write-Output "PHASE171_R14_BRANCH=$Branch"
    Write-Output "PHASE171_R14_HEAD=$Head"

    python -m "$Module.audit" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R14 preflight failed.' }
    if ($DryRun) {
        Write-Output 'PHASE171_R14_DRY_RUN=PASS'
        return
    }

    Write-Output 'PHASE171_R14_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider "$Module/tests/test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R14 focused pytest failed.' }
    Write-Output 'PHASE171_R14_FOCUSED_PYTEST=PASS'

    python -m "$Module.audit"
    if ($LASTEXITCODE -ne 0) { throw 'R14 root exception audit failed.' }
    git status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Git status failed.' }
    git diff --stat
    if ($LASTEXITCODE -ne 0) { throw 'Git diff failed.' }
    Write-Output 'PHASE171_R14_RESULT=PASS_READ_ONLY_ROOT_BRANCH_AUDIT'
}
finally {
    Pop-Location
}
```

## `__init__.py`

```python
"""Read-only Phase 171 R14 package."""
```

## `tests/__init__.py`

```python
"""Focused diagnostic tests."""
```

