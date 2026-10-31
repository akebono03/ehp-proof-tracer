# Phase 171 R2J-R4-R9-R12 — コード全文

今回の R12 は **AUDIT_ONLY** であり、既存コードを変更しない。

- 既存変更ファイル：なし。
- 既存変更クラス・関数：なし。
- 新規ファイルの追加位置：リポジトリ直下 `phase171_r2j_r4_r9_r12_public_symmetry_diagnostic/`。
- 新規クラス：`audit.py` の `TracingProvider`（全体を掲載）。
- 新規関数：`audit.py` 内の監査関数一式、`tests/test_audit.py` 内の限定テスト5件（全文を掲載）。
- 既存 import の変更：なし。
- 新規 import：新規ファイル内の全文を下に掲載。
- 根拠のない本体修正を行わず、報告を元に次の限定パッチを検討する。

## R11 のコード読解で確認できたこと

`shared_expansion_provider()` の内部では、逆向き候補が返ると `return directed` で返却する。
この経路は `merge_backward_expansions()` と `retain_ordered_root_expansions()` に到達しない。
これはその 2 関数の不具合を証明するものではなく、今回は公開探索で前提が解消されない原因を分類する。

## `audit.py`（全文）

```python
"""Read-only audit of R11 equality-symmetry adoption in public proof search.

No proof step is installed, no GIVEN is created, and no repository source is
modified. The complete public search and the focused recursive searches are
independent invocations of the existing canonical searcher.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Callable

from phase165_r3_recursive_search import (
    GoalExpansion,
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge,
    shared_expansion_provider,
)
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
from phase165_r57_r26_generic_search_connection import merge_backward_expansions
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase171_r2i_eta_hopf_bridge.audit import (
    _checked_chain,
    _screened_context,
)
from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import (
    expand_reverse_cited_eta_hopf_equalities,
    reverse_equality,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
SOURCE = ROOT / "phase165_r52_r9_shared_math.py"
SOURCE_IN_GIT = "phase165_r52_r9_shared_math.py"
R11_BLOB_SHA = "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"


def git_read(*arguments: str) -> bytes:
    """Allow only source-inspection commands and current branch metadata."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
        ("show", f"HEAD:{SOURCE_IN_GIT}"),
    }
    if arguments not in allowed:
        raise ValueError("R12 audit permits read-only Git operations only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True, capture_output=True,
    ).stdout


def git_blob_sha(contents: bytes) -> str:
    """Return the canonical SHA-1 blob identifier for unmodified Git bytes."""
    header = f"blob {len(contents)}\0".encode("ascii")
    return hashlib.sha1(header + contents).hexdigest()


def normalized_source(contents: bytes) -> str:
    """Compare checked-out CRLF and Git LF without changing either file."""
    return contents.decode("utf-8-sig").replace("\r\n", "\n")


def preflight() -> dict:
    """Require reviewed committed R11 and a matching, unedited worktree."""
    branch = git_read("branch", "--show-current").decode().strip()
    head = git_read("rev-parse", "HEAD").decode().strip()
    head_blob = git_read("show", f"HEAD:{SOURCE_IN_GIT}")
    worktree_blob = SOURCE.read_bytes()
    if branch != "develop":
        raise RuntimeError("R12 requires the develop branch")
    actual_sha = git_blob_sha(head_blob)
    if actual_sha != R11_BLOB_SHA:
        raise RuntimeError(
            "R11 is not the committed reviewed baseline; first synchronize "
            "develop so HEAD contains the R11 provider hook. "
            f"actual blob={actual_sha}"
        )
    if normalized_source(worktree_blob) != normalized_source(head_blob):
        raise RuntimeError("tracked shared provider differs from committed HEAD")
    return {
        "branch": branch,
        "head": head,
        "shared_provider_blob": actual_sha,
        "tracked_status_before": git_read(
            "status", "--porcelain", "--untracked-files=no"
        ).decode("utf-8", errors="replace"),
    }


def route_profile(expansions: tuple[GoalExpansion, ...]) -> dict:
    """Describe proposals without treating a proposal as a proved ProofStep."""
    if not isinstance(expansions, tuple):
        raise TypeError("expansions must be a tuple")
    if any(not isinstance(item, GoalExpansion) for item in expansions):
        raise TypeError("each route must be GoalExpansion")
    names = tuple(str(getattr(item.rule, "name", "<unnamed>")) for item in expansions)
    return {
        "count": len(expansions),
        "rule_names": list(names[:30]),
        "symmetry_count": names.count("equality symmetry"),
        "proposals": [
            {
                "rule": str(getattr(item.rule, "name", "<unnamed>")),
                "subgoals": [repr(x)[:750] for x in item.subgoals],
            }
            for item in expansions[:20]
        ],
        "profile_truncated": len(expansions) > 20,
    }


def route_matches(
    expansions: tuple[GoalExpansion, ...],
    rule_name: str,
    subgoals: tuple[object, ...],
) -> int:
    """Count the exact R11 premise route through each inspected stage."""
    return sum(
        getattr(item.rule, "name", None) == rule_name
        and item.subgoals == subgoals
        for item in expansions
    )


class TracingProvider:
    """Log provider calls without changing their order or returned proposals."""

    def __init__(self, original: Callable[[object], tuple[GoalExpansion, ...]]):
        if not callable(original):
            raise TypeError("provider must be callable")
        self.original = original
        self.calls: list[dict] = []
        self.count = 0

    def __call__(self, goal: object) -> tuple[GoalExpansion, ...]:
        self.count += 1
        routes = self.original(goal)
        if len(self.calls) < 150:
            self.calls.append({
                "goal": repr(goal)[:950],
                "routes": route_profile(routes),
            })
        return routes


def focused_reconstruction(
    goal: object,
    screened: object,
    citing: str,
    provider: Callable[[object], tuple[GoalExpansion, ...]],
) -> dict:
    """Run canonical reconstruction on one goal with a progress observer."""
    traced = TracingProvider(provider)
    observations: list[dict] = []

    def observer(kind: str, target: object, step: object) -> None:
        if len(observations) < 250:
            observations.append({
                "event": kind,
                "goal": repr(target)[:950],
                "rule": getattr(getattr(step, "rule", None), "name", None),
            })

    try:
        result = reconstruct_registered_goal(
            goal,
            screened,
            citing,
            traced,
            lookup_mode="typed_reference_publication",
            progress_observer=observer,
            completed_internal_proofs=(),
        )
    except RegisteredGoalUnresolved as error:
        return {
            "status": "unresolved",
            "message": str(error),
            "provider_calls": traced.count,
            "calls": traced.calls,
            "observations": observations,
        }
    return {
        "status": "proved",
        "conclusion_matches": type(result.conclusion) is type(goal)
        and result.conclusion == goal,
        "root_rule": str(result.rule),
        "provider_calls": traced.count,
        "calls": traced.calls,
        "observations": observations,
    }


def inspect() -> dict:
    """Compare direct, merged, filtered, and actual public-search proposals."""
    original_bridge = build_shared_typed_bridge()
    screened_reference, target, citing = _screened_context()
    if not isinstance(citing, str) or not citing:
        raise RuntimeError("no resolved citation for pi_6^3")
    resolved_citing = resolve_specialized_goal_citing_id(original_bridge, target)
    if resolved_citing != citing:
        raise RuntimeError("the R2I and public citing goal IDs are different")
    public_contexts: list[object] = []
    public = search_group_from_registered_goal(
        n=3,
        k=3,
        bridge=original_bridge,
        goal=target,
        context_sink=public_contexts.append,
    )
    if len(public_contexts) > 1:
        raise RuntimeError("ambiguous root proof contexts captured")
    actual_context = public_contexts[0] if public_contexts else screened_reference
    context_captured = len(public_contexts) == 1
    chain, available = _checked_chain(actual_context, citing)
    forward_goal = chain.alpha_composition
    reverse_goal = reverse_equality(forward_goal)
    if reverse_goal is None:
        raise RuntimeError("first unresolved equality cannot be reversed")
    direct = expand_reverse_cited_eta_hopf_equalities(reverse_goal, available)
    merged = merge_backward_expansions(direct, ())
    gated = retain_ordered_root_expansions(target, reverse_goal, merged)
    provider = shared_expansion_provider(actual_context, proof_target=target)
    public_reverse_routes = provider(reverse_goal)
    public_forward_routes = provider(forward_goal)
    original_rule = "equality symmetry"
    obligations = (forward_goal,)
    counts = {
        "direct": route_matches(direct, original_rule, obligations),
        "deduplicated": route_matches(merged, original_rule, obligations),
        "root_gate": route_matches(gated, original_rule, obligations),
        "actual_public_provider": route_matches(
            public_reverse_routes, original_rule, obligations
        ),
    }
    forward = focused_reconstruction(forward_goal, actual_context, citing, provider)
    reverse = focused_reconstruction(reverse_goal, actual_context, citing, provider)
    first_open = public.open_goals[0] if public.open_goals else None
    observed_open_is_reverse = type(first_open) is type(reverse_goal) and first_open == reverse_goal
    if counts["direct"] == 0:
        classification = "R11_NOT_PROPOSED_FOR_PUBLIC_CONTEXT"
    elif counts["actual_public_provider"] == 0:
        classification = "R11_PROPOSAL_DROPPED_BEFORE_CANONICAL_SEARCH"
    elif forward["status"] == "unresolved":
        classification = "FORWARD_PREMISE_UNRESOLVED_IN_CANONICAL_SEARCH"
    elif reverse["status"] == "unresolved":
        classification = "REVERSE_UNRESOLVED_DESPITE_FORWARD_PROOF_CHECK_MATCH_OR_AMBIGUITY"
    elif public.status.value != "complete":
        classification = "FOCUSED_REVERSE_PROVED_BUT_ROOT_SEARCH_STILL_PARTIAL"
    else:
        classification = "PUBLIC_SEARCH_COMPLETE_NEEDS_TRUST_BOUNDARY_VERIFICATION"
    return {
        "phase": "171-R2J-R4-R9-R12",
        "mode": "AUDIT_ONLY",
        "target": repr(target),
        "context_captured_from_public_path": context_captured,
        "reference_source_count": len(screened_reference.proof_links),
        "public_source_count": len(actual_context.proof_links),
        "first_reported_open_is_reverse_goal": observed_open_is_reverse,
        "public_first_open": repr(first_open)[:1300],
        "public_status": public.status.value,
        "public_diagnostics": list(public.diagnostics[:12]),
        "public_proven_steps": len(public.proven_steps),
        "public_open_goal_count": len(public.open_goals),
        "forward_goal": repr(forward_goal),
        "reverse_goal": repr(reverse_goal),
        "r11_route_stage_counts": counts,
        "r11_direct": route_profile(direct),
        "r11_gate": route_profile(gated),
        "public_reverse": route_profile(public_reverse_routes),
        "public_forward": route_profile(public_forward_routes),
        "forward_search": forward,
        "reverse_search": reverse,
        "classification": classification,
        "new_given_added": 0,
        "completed_proof_replay": False,
        "existing_source_modified": False,
        "full_pytest": False,
        "public_web_verified": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    meta = preflight()
    print("PHASE171_R12_BRANCH=" + meta["branch"], flush=True)
    print("PHASE171_R12_HEAD=" + meta["head"], flush=True)
    print("PHASE171_R12_REVIEWED_R11_BLOB=PASS", flush=True)
    if args.dry_run:
        print("PHASE171_R12_RESULT=PASS_DRY_RUN", flush=True)
        return
    result = inspect()
    after = git_read("status", "--porcelain", "--untracked-files=no").decode(
        "utf-8", errors="replace"
    )
    if meta["tracked_status_before"] != after:
        raise RuntimeError("tracked status changed during the read-only audit")
    result.update({
        "git_head": meta["head"],
        "shared_provider_blob": meta["shared_provider_blob"],
        "tracked_status_unchanged": True,
    })
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PHASE171_R12_PUBLIC_SEARCH=" + result["public_status"], flush=True)
    print("PHASE171_R12_FIRST_OPEN_IS_REVERSE=" + str(
        result["first_reported_open_is_reverse_goal"]
    ), flush=True)
    print("PHASE171_R12_ROUTE_COUNTS=" + json.dumps(
        result["r11_route_stage_counts"], ensure_ascii=False
    ), flush=True)
    print("PHASE171_R12_FORWARD=" + result["forward_search"]["status"], flush=True)
    print("PHASE171_R12_REVERSE=" + result["reverse_search"]["status"], flush=True)
    print("PHASE171_R12_CLASSIFICATION=" + result["classification"], flush=True)
    print("PHASE171_R12_NEW_GIVEN=0", flush=True)
    print("PHASE171_R12_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R12_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R12_REPORT=" + str(destination), flush=True)
    print("PHASE171_R12_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py`（全文）

```python
"""Read-only R12 stage and observation tests; no completed tree is injected."""
from __future__ import annotations

import pytest

from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
from phase165_r57_r26_generic_search_connection import merge_backward_expansions
from phase171_r2j_r4_r9_r12_public_symmetry_diagnostic.audit import (
    TracingProvider,
    git_blob_sha,
    git_read,
    normalized_source,
    route_matches,
    route_profile,
)
from proof import Relation, RelationType
from relation_rules import equality_symmetry_inference_rule


def test_only_read_only_git_commands_are_allowed():
    with pytest.raises(ValueError, match="read-only"):
        git_read("reset", "--hard")
    with pytest.raises(ValueError, match="read-only"):
        git_read("checkout", "develop")


def test_exact_symmetry_route_is_preserved_by_merge_and_nonroot_gate():
    forward = Relation("x", "y", RelationType.EQUALITY)
    reverse = Relation("y", "x", RelationType.EQUALITY)
    candidate = GoalExpansion(equality_symmetry_inference_rule(), (forward,))
    initial = (candidate,)
    merged = merge_backward_expansions(initial, ())
    gated = retain_ordered_root_expansions(object(), reverse, merged)
    for routes in (initial, merged, gated):
        assert route_matches(routes, "equality symmetry", (forward,)) == 1
        assert route_profile(routes)["symmetry_count"] == 1
    assert gated[0] is candidate


def test_tracing_provider_retains_original_candidates_and_observes_calls():
    forward = Relation("x", "y", RelationType.EQUALITY)
    reverse = Relation("y", "x", RelationType.EQUALITY)
    candidate = GoalExpansion(equality_symmetry_inference_rule(), (forward,))
    calls = []

    def provider(goal):
        calls.append(goal)
        return (candidate,)

    tracing = TracingProvider(provider)
    actual = tracing(reverse)
    assert actual == (candidate,)
    assert actual[0] is candidate
    assert calls == [reverse]
    assert tracing.count == 1
    assert tracing.calls[0]["routes"]["symmetry_count"] == 1


def test_route_profile_rejects_non_expansion_results():
    with pytest.raises(TypeError):
        route_profile([])
    with pytest.raises(TypeError):
        route_profile((object(),))
    assert route_profile(())["count"] == 0


def test_git_blob_and_crlf_normalization_do_not_mutate_source():
    payload = b"a\r\nb\r\n"
    assert normalized_source(payload) == "a\nb\n"
    assert normalized_source(b"\xef\xbb\xbfa\n") == "a\n"
    assert git_blob_sha(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
```

## `run.ps1`（全文）

```powershell
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ModuleName = 'phase171_r2j_r4_r9_r12_public_symmetry_diagnostic'
Push-Location $RepoRoot
try {
    $GitBranch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $GitBranch -ne 'develop') {
        throw 'R12 requires Git develop. No source was modified.'
    }
    $GitHead = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not read Git HEAD.'
    }
    Write-Output "PHASE171_R12_BRANCH=$GitBranch"
    Write-Output "PHASE171_R12_HEAD=$GitHead"

    if ($DryRun) {
        python -m "$ModuleName.audit" --dry-run
        if ($LASTEXITCODE -ne 0) {
            throw 'R12 preflight failed; install nothing.'
        }
        Write-Output 'PHASE171_R12_DRY_RUN=PASS'
        return
    }

    python -m "$ModuleName.audit" --dry-run
    if ($LASTEXITCODE -ne 0) {
        throw 'R12 source baseline check failed; audit cancelled.'
    }

    Write-Output 'PHASE171_R12_FOCUSED_PYTEST_START'
    python -m pytest -q "$ModuleName/tests/test_audit.py"
    if ($LASTEXITCODE -ne 0) {
        throw 'R12 focused pytest failed; audit cancelled.'
    }
    Write-Output 'PHASE171_R12_FOCUSED_PYTEST=PASS'

    python -m "$ModuleName.audit"
    if ($LASTEXITCODE -ne 0) {
        throw 'R12 public-search diagnosis failed without modifying source.'
    }

    git status -sb
    if ($LASTEXITCODE -ne 0) {
        throw 'Git status query failed.'
    }
    git diff --stat
    if ($LASTEXITCODE -ne 0) {
        throw 'Git diff query failed.'
    }
    Write-Output 'PHASE171_R12_RESULT=PASS_READ_ONLY_AUDIT'
}
finally {
    Pop-Location
}
```

## `__init__.py`（全文）

```python
"""Phase 171 R12: read-only public-search route diagnosis."""
```

## `tests/__init__.py`（全文）

```python
"""Focused R12 regression tests."""
```

## `README.md`（全文）

```markdown
# EHP Proof Tracer — Phase 171 R2J-R4-R9-R12

This is a **read-only diagnostic release**. It does not patch project source,
create mathematical axioms, insert GIVEN proof steps, or replay finished trees.

## Prerequisite

The `develop` branch must contain the committed R11 equality-symmetry hook.
The reviewed SHA-1 Git blob of `phase165_r52_r9_shared_math.py` is
`10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac`.

The R10 commit `40fccc4d` is not sufficient; R11 was subsequently committed
as `e941ac47`. GitHub's develop branch was checked with the R11 hook in place.
A different source blob fails closed rather than being silently overwritten.

## Run on Windows PowerShell

Unpack the archive into the root of the EHP Proof Tracer checkout, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File '.\phase171_r2j_r4_r9_r12_public_symmetry_diagnostic\run.ps1' `
  -DryRun
powershell -NoProfile -ExecutionPolicy Bypass `
  -File '.\phase171_r2j_r4_r9_r12_public_symmetry_diagnostic\run.ps1'
```

The detailed structured report will be written to
`phase171_r2j_r4_r9_r12_public_symmetry_diagnostic/output/audit.json`.
Only focused tests are executed. No full test suite is run.

## Diagnosis

The audit verifies the registered public-search context, then compares R11's
exact reverse-equality route at four points: direct rule output, deduplication,
root ordering gate, and the actual shared provider. It also reconstructs the
forward and reverse equalities *independently* through the canonical recursive
searcher, collecting accepted steps and unresolved subgoals as observations.

A proposed `GoalExpansion` is never counted as a proved `ProofStep`. A completed
Web proof is never declared merely because the candidate exists. All outputs
are recorded read-only, and no source changes are made automatically.

The next patch must be selected based on this report, not on a guessed search
failure. No implementation for a future phase is included.
```

## `監査仕様.md`（全文）

```markdown
# Phase 171 R2J-R4-R9-R12 監査仕様

## 対象

- リポジトリ：`akebono03/ehp-proof-tracer`
- 分岐：`develop`
- 既存ファイル変更：なし
- 既存関数変更：なし
- 新規監査クラス：`TracingProvider`
- 新規監査関数：`git_read`、`git_blob_sha`、`normalized_source`、`preflight`、`route_profile`、`route_matches`、`focused_reconstruction`、`inspect`、`main`
- テスト：新規 `tests/test_audit.py` 内の5関数

## 背景

R11 では `shared_expansion_provider()` の `expand()` 内で
`expand_reverse_cited_eta_hopf_equalities()` が候補を返すと即座に `return directed` する。
したがってこの場合、当該候補は既存の `merge_backward_expansions()` と
`retain_ordered_root_expansions()` に到達しない。これはコード読解で確認できる事実だが、
公開探索で `partial` になる直接原因とはまだ限らない。

## 記録する値

1. R11 の候補が独立した公開探索の Source screening（出典審査）で生成できるか。
2. 比較用に merge と root gate を個別適用した際、同じ候補が残るか。
3. 実際の共通 Provider（候補生成器）が候補を返すか。
4. `reconstruct_registered_goal()` が forward（順向き）と reverse（逆向き）それぞれの式を再帰構成できるか。
5. 各探索の受理済み推論と unresolved（未解決）の通知、候補規則、候補数。
6. 通常の群構造探索の status・最初の open goal と diagnostics。

## 安全条件

- `GIVEN` は追加しない。
- 完成済み証明木を通常探索へ注入しない。
- `phase165_r52_r9_shared_math.py` を変更しない。
- 監査は現在の `develop` にコミット済みの R11 blob がある場合だけ動作する。
- `pytest` は新規の限定テストのみ。全体テストは Phase 完了まで保留。
- 原因が未特定なら実装修正を行わない。
- `public_web_verified` は常に `False` として記録し、完成認定を先取りしない。

## 判定

`audit.json` 内の `classification` と `forward_search`、`reverse_search`、
`r11_route_stage_counts` を次段階の修正判断に使う。`classification` は
再現ログからの分類であり、数学的な証明完了の認定ではない。
```

