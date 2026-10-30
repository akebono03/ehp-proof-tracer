# Phase 171 R2J-R4-R9-R10 — 変更コードの全文

## 変更する既存ファイル・関数

- 既存ファイル `phase165_r52_r9_shared_math.py` の関数 `shared_expansion_provider()` のみ。
- 変更後の import（トップレベル）は変更なし。関数内の既存 R9 hook 直後に次の2行だけを挿入する。
- インストーラーはこの関数の**全文**とモジュール**全文**をそれぞれ `output/shared_expansion_provider_FULL.py`、`output/phase165_r52_r9_shared_math.FULL.py` に書き出す。既存関数の他部分を省略した差分適用はしない。

```python
        from phase171_r2j_r4_r5_short_exact_sequence.source import expand_ehp_short_exact
        options.extend(expand_ehp_short_exact(goal))
```

## 新規ファイルと追加位置

`phase171_r2j_r4_r9_r10_public_short_exact/` をリポジトリ直下に追加。既存クラスは一切変更しない。以下のファイルは import を含めてすべて全文である。

## 保護インストーラー（全文） — `install.py`

```python
"""Guarded minimal provider patch for the already implemented EHP short-exact rule.

The installer recognizes only the reviewed baseline and the exact R7/R8/R9/R10
hooks. It neither resets Git nor overwrites an unknown tracked modification.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
GIT_TARGET = "phase165_r52_r9_shared_math.py"
REVIEWED_ORIGINAL_BLOB_SHA = "68846671215c38e3e0a572932b8ed955a7880edc"
R7_HOOK = (
    "        from phase171_r2j_r4_r9_r7_public_cyclic_root.source import (\n"
    "            expand_cited_double_cyclic_root,\n"
    "        )\n"
    "        options.extend(expand_cited_double_cyclic_root(goal, tuple(available)))\n"
)
R8_HOOK = (
    "        from phase171_r2j_r4_r9_r8_public_cardinality.source import (\n"
    "            expand_cited_ehp_middle_cardinality,\n"
    "        )\n"
    "        options.extend(expand_cited_ehp_middle_cardinality(goal, tuple(available)))\n"
)
R9_HOOK = (
    "        from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import (\n"
    "            expand_cited_full_order_cyclic_structure,\n"
    "        )\n"
    "        options.extend(expand_cited_full_order_cyclic_structure(goal, tuple(available)))\n"
)
R10_HOOK = (
    "        from phase171_r2j_r4_r5_short_exact_sequence.source import expand_ehp_short_exact\n"
    "        options.extend(expand_ehp_short_exact(goal))\n"
)
HOOKS = (R7_HOOK, R8_HOOK, R9_HOOK, R10_HOOK)


def _git(*arguments: str) -> bytes:
    """Allow only read operations and an explicit tracked HEAD file."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("show", f"HEAD:{GIT_TARGET}"),
    }
    if arguments not in allowed:
        raise ValueError("only read-only reviewed Git commands are allowed")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True, check=True,
    ).stdout


def _normal(blob: bytes) -> str:
    """Normalize CRLF and optional UTF-8 BOM for exact source inspection."""
    return blob.decode("utf-8-sig").replace("\r\n", "\n")


def _git_blob_sha(blob: bytes) -> str:
    """Compute the exact Git blob identity of an untouched reviewed file."""
    return hashlib.sha1(f"blob {len(blob)}\0".encode("ascii") + blob).hexdigest()


def _complete_function(source: str) -> str:
    """Extract the full original function with no code abbreviation."""
    candidates = [
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(candidates) != 1:
        raise RuntimeError("expected a unique shared_expansion_provider function")
    node = candidates[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def _verified_source_and_state(head_bytes: bytes, current_bytes: bytes) -> tuple[str, str]:
    """Accept only the reviewed R7/R8/R9 chain, optionally with R10 already in it."""
    head_text = _normal(head_bytes)
    current = _normal(current_bytes)
    head_newline = "\r\n" if b"\r\n" in head_bytes else "\n"
    raw_reviewed = head_bytes
    for hook in HOOKS:
        if head_text.count(hook) > 1:
            raise RuntimeError("duplicate provider hook in HEAD")
        raw_reviewed = raw_reviewed.replace(
            hook.replace("\n", head_newline).encode("utf-8"), b"",
        )
    if _git_blob_sha(raw_reviewed) != REVIEWED_ORIGINAL_BLOB_SHA:
        raise RuntimeError("HEAD provider differs from reviewed GitHub baseline")
    expected = head_text
    anchor = "        options.extend(expand_finite_cyclic_relation(goal))\n"
    for index, hook in enumerate((R7_HOOK, R8_HOOK, R9_HOOK)):
        preceding = anchor if index == 0 else HOOKS[index - 1]
        if hook not in expected:
            if expected.count(preceding) != 1:
                raise RuntimeError("reviewed predecessor hook is absent or ambiguous")
            expected = expected.replace(preceding, preceding + hook, 1)
    if any(expected.count(hook) != 1 for hook in (R7_HOOK, R8_HOOK, R9_HOOK)):
        raise RuntimeError("R7/R8/R9 prerequisites are absent")
    final = expected if R10_HOOK in expected else expected.replace(
        R9_HOOK, R9_HOOK + R10_HOOK, 1,
    )
    if current == expected and R10_HOOK not in expected:
        state = "READY_TO_PATCH"
    elif current == final:
        state = "ALREADY_INSTALLED"
    else:
        raise RuntimeError("unknown tracked provider changes; no files overwritten")
    if any(final.count(hook) != 1 for hook in HOOKS):
        raise RuntimeError("missing or duplicated provider hook")
    function = _complete_function(final)
    if any(hook not in function for hook in HOOKS):
        raise RuntimeError("patch left the existing provider function")
    ast.parse(final)
    return state, final


def install(*, dry_run: bool) -> bool:
    """Guard R7–R9 and insert exactly the existing short-exact expander."""
    if _git("branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("develop branch required")
    if not TARGET.is_file():
        raise RuntimeError("shared provider file is absent")
    current_bytes = TARGET.read_bytes()
    state, final = _verified_source_and_state(
        _git("show", f"HEAD:{GIT_TARGET}"), current_bytes,
    )
    print("PHASE171_R2J_R4_R9_R10_HEAD=" + _git("rev-parse", "HEAD").decode().strip(), flush=True)
    print("PHASE171_R2J_R4_R9_R10_PATCH_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE171_R2J_R4_R9_R10_RESULT=PASS_DRY_RUN", flush=True)
        return False
    OUTPUT.mkdir(exist_ok=True)
    if state == "READY_TO_PATCH":
        (OUTPUT / "phase165_r52_r9_shared_math.BEFORE.py").write_bytes(current_bytes)
        newline = "\r\n" if b"\r\n" in current_bytes else "\n"
        bom = b"\xef\xbb\xbf" if current_bytes.startswith(b"\xef\xbb\xbf") else b""
        TARGET.write_bytes(bom + final.replace("\n", newline).encode("utf-8"))
        print("PHASE171_R2J_R4_R9_R10_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(
        _complete_function(final) + "\n", encoding="utf-8",
    )
    (OUTPUT / "phase165_r52_r9_shared_math.FULL.py").write_bytes(TARGET.read_bytes())
    print("PHASE171_R2J_R4_R9_R10_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"), flush=True)
    print("PHASE171_R2J_R4_R9_R10_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.FULL.py"), flush=True)
    return state == "READY_TO_PATCH"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    install(dry_run=arguments.dry_run)


if __name__ == "__main__":
    main()
```

## 公開探索監査コード（全文） — `audit.py`

```python
"""Audit canonical EHP short-exact backward proposals after R10 integration.

An earlier fully inferred R4-R5 tree is used only to check the proposed rule
and subgoal shape. The public search is run independently, never fed that tree.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r5_short_exact_sequence.audit import build_short_exact_proof
from phase171_r2j_r4_r5_short_exact_sequence.source import expand_ehp_short_exact
from proof import ProofRule, find_inference_matches_for_rule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("read-only Git operations only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()


def equivalent_short_exact_routes(options: tuple, root: object) -> int:
    """Count exactly matching rule-and-subgoal routes (not rule names alone)."""
    return sum(
        option.rule.name == root.inference_rule.name
        and option.subgoals == tuple(parent.conclusion for parent in root.premises)
        for option in options
    )


def inspect_public_short_exact() -> dict:
    """Require a genuine original inference and independently query public search."""
    screened, target, _ = _screened_context()
    short_exact_root, ancestors, original_report = build_short_exact_proof()
    if (
        short_exact_root.rule is not ProofRule.INFERENCE
        or short_exact_root.inference_rule is None
        or len(short_exact_root.premises) != 3
        or any(parent.rule is not ProofRule.INFERENCE for parent in short_exact_root.premises)
        or original_report["new_given_added"] != 0
        or not ancestors
        or any(node.conclusion == target for node in ancestors)
    ):
        raise RuntimeError("R4-R5 short exact proof ancestry is untrusted")
    expected = expand_ehp_short_exact(short_exact_root.conclusion)
    if len(expected) != 1 or equivalent_short_exact_routes(expected, short_exact_root) != 1:
        raise RuntimeError("existing generic short-exact rule is unavailable")
    shared = shared_expansion_provider(screened, proof_target=target)(
        short_exact_root.conclusion,
    )
    if equivalent_short_exact_routes(shared, short_exact_root) != 1:
        raise RuntimeError("common provider did not expose exactly one EHP short-exact route")
    matches = tuple(
        match for match in find_inference_matches_for_rule(
            expected[0].rule, short_exact_root.premises,
        ) if match.premises == short_exact_root.premises
    )
    if len(matches) != 1:
        raise RuntimeError("short exact inference failed matching real R4-R5 premises")
    derived = derive_inference_proof_step(matches[0])
    if derived.rule is not ProofRule.INFERENCE or derived.conclusion != short_exact_root.conclusion:
        raise RuntimeError("generic rule failed to infer the short exact conclusion")
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=target,
    )
    complete = (public.status.value == "complete" and public.conclusion == target
                and not public.open_goals)
    return {
        "phase": "171-R2J-R4-R9-R10",
        "mode": "PUBLIC_SHORT_EXACT_PROPOSAL_INTEGRATION",
        "short_exact_goal": repr(short_exact_root.conclusion),
        "proof_rule": short_exact_root.inference_rule.name,
        "original_source_inferences": original_report["inferences"],
        "original_source_given": original_report["given_leaves"],
        "short_exact_proposed": True,
        "short_exact_inference_matched": True,
        "shared_short_exact_connected": True,
        "shared_short_exact_route_count": equivalent_short_exact_routes(shared, short_exact_root),
        "short_exact_subgoals": [repr(item) for item in expected[0].subgoals],
        "public_search_status": public.status.value,
        "public_complete": complete,
        "public_proven_steps": len(public.proven_steps),
        "public_open_goals": [repr(item)[:1500] for item in public.open_goals[:20]],
        "public_diagnostics": list(public.diagnostics[:20]),
        "new_given_added": 0,
        "completed_proof_imported": False,
        "web_modified": False,
        "trust_boundary_modified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if branch != "develop":
        raise RuntimeError("develop branch required")
    print("PHASE171_R2J_R4_R9_R10_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R10_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R10_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_public_short_exact()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files changed during read-only audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R10_SHORT_EXACT_INFERENCE=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R10_SHARED_SHORT_EXACT_CONNECTED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R10_PUBLIC_SEARCH=" + report["public_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R10_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    if report["public_open_goals"]:
        print("PHASE171_R2J_R4_R9_R10_FIRST_OPEN_GOAL=" + report["public_open_goals"][0], flush=True)
    print("PHASE171_R2J_R4_R9_R10_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R10_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R10_REPORT=" + str(path), flush=True)
    print("PHASE171_R2J_R4_R9_R10_RESULT=PASS_SHORT_EXACT_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()
```

## PowerShell 実行コード（全文） — `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Git repository root required' }
    python -B -m phase171_r2j_r4_r9_r10_public_short_exact.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R10 guarded preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R10_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m phase171_r2j_r4_r9_r10_public_short_exact.install
    if ($LASTEXITCODE -ne 0) { throw 'R9-R10 guarded integration failed' }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r10_public_short_exact\tests\test_audit.py' `
        '.\phase171_r2j_r4_r5_short_exact_sequence\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R10 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R10_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r10_public_short_exact.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R10 public short-exact audit failed' }
} finally {
    Pop-Location
}
```

## 限定テスト（import を含む全文） — `tests/test_audit.py`

```python
"""Focused short-exact public-provider and fail-closed proof tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r5_short_exact_sequence.audit import build_short_exact_proof
from phase171_r2j_r4_r5_short_exact_sequence.source import (
    EHPShortExactSequence,
    expand_ehp_short_exact,
    short_exact_from_ehp,
)
from phase171_r2j_r4_r9_r10_public_short_exact.audit import (
    _git,
    equivalent_short_exact_routes,
    inspect_public_short_exact,
)
from phase171_r2j_r4_r9_r10_public_short_exact.install import (
    R10_HOOK,
    _complete_function,
    install,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement


def _premises():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    c = TodaPrimaryGroup(6, 5)
    return (
        MapInjective(TodaSuspensionMap(a, b)),
        TodaProp42ExactnessStatement(TodaEHPExactnessWindow(a, b, c, EHP_E_MAP, EHP_H_MAP)),
        MapSurjective(TodaHopfInvariantMap(b, c)),
    )


def test_generic_short_exact_requires_only_three_unproven_typed_subgoals():
    goal = short_exact_from_ehp(*_premises())
    assert isinstance(goal, EHPShortExactSequence)
    proposal, = expand_ehp_short_exact(goal)
    assert proposal.subgoals == _premises()
    assert all(not isinstance(item, ProofStep) for item in proposal.subgoals)


def test_short_exact_rule_refuses_given_map_properties():
    goal = short_exact_from_ehp(*_premises())
    proposal, = expand_ehp_short_exact(goal)
    for forged in range(3):
        parents = tuple(ProofStep(value, (), ProofRule.GIVEN if i == forged else ProofRule.INFERENCE)
                        for i, value in enumerate(proposal.subgoals))
        assert find_inference_matches_for_rule(proposal.rule, parents) == ()


def test_malformed_ehp_window_or_wrong_middle_group_fails_closed():
    injection, exact, hopf = _premises()
    goal = short_exact_from_ehp(injection, exact, hopf)
    assert goal is not None
    assert expand_ehp_short_exact(replace(goal, middle_group=TodaPrimaryGroup(7, 3))) == ()
    assert short_exact_from_ehp(injection, replace(exact, window=replace(
        exact.window, first_map=EHP_DELTA_MAP,
    )), hopf) is None
    assert expand_ehp_short_exact(object()) == ()


def test_wrong_map_endpoints_are_not_accepted():
    injection, exact, hopf = _premises()
    assert short_exact_from_ehp(replace(injection, map=TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    )), exact, hopf) is None
    assert short_exact_from_ehp(injection, exact, replace(hopf, map=TodaHopfInvariantMap(
        TodaPrimaryGroup(6, 4), TodaPrimaryGroup(6, 5),
    ))) is None


def test_shared_provider_reuses_actual_verified_ehp_rule():
    screened, target, _ = _screened_context()
    root, _, report = build_short_exact_proof()
    candidates = shared_expansion_provider(screened, proof_target=target)(root.conclusion)
    assert equivalent_short_exact_routes(candidates, root) == 1
    assert report["new_given_added"] == 0
    assert len(root.premises) == 3


def test_public_audit_never_reports_fabricated_group_or_success():
    report = inspect_public_short_exact()
    assert report["shared_short_exact_connected"] is True
    assert report["short_exact_inference_matched"] is True
    assert report["completed_proof_imported"] is False
    assert report["new_given_added"] == 0
    assert report["public_search_status"] in ("complete", "partial", "search_failed")
    if report["public_complete"]:
        assert report["public_search_status"] == "complete"
        assert report["public_open_goals"] == []


def test_patch_keeps_full_function_and_is_idempotent_in_dry_run():
    assert install(dry_run=True) is False
    content = (pytest.importorskip("phase165_r52_r9_shared_math").__file__)
    from pathlib import Path
    source = Path(content).read_text(encoding="utf-8-sig")
    function = _complete_function(source.replace("\r\n", "\n"))
    assert function.count(R10_HOOK) == 1
    assert "def shared_expansion_provider(" in function


def test_git_guard_prevents_mutating_commands():
    with pytest.raises(ValueError):
        _git("reset", "--hard")
```

## 新規パッケージ初期化コード（全文） — `__init__.py`

```python
"""Phase 171 R2J-R4-R9-R10: connect an existing EHP short-exact inference."""
```

## 新規テストパッケージ初期化コード（全文） — `tests/__init__.py`

```python
"""Focused regressions for R4-R9-R10."""
```
