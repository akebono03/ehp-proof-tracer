# Phase 171 R2J-R4-R9-R11 — 変更・テストコード全文

## 既存の変更先

- ファイル：`phase165_r52_r9_shared_math.py`
- 関数：`shared_expansion_provider()`
- トップレベル import：変更なし。
- 関数内の R10 hook 直後に R11 の6行を挿入する。変更後の関数とモジュールの**全文**をインストーラーが `output/shared_expansion_provider_FULL.py` と `output/phase165_r52_r9_shared_math.FULL.py` に出力する。

## 実際に追加する6行（既存関数の途中に挿入）

```python
        from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import (
            expand_reverse_cited_eta_hopf_equalities,
        )
        directed = expand_reverse_cited_eta_hopf_equalities(goal, tuple(available))
        if directed:
            return directed
```

## 新規ファイル・追加位置

リポジトリ直下に `phase171_r2j_r4_r9_r11_public_eta_symmetry/` を作成する。既存クラス・関数は新規に書き直さない。以下は import を含む各ファイルの全文である。

## `source.py` — 新規の数学的候補生成関数

```python
"""Backward symmetry for an independently provable, cited eta–Hopf chain.

This module supplies *obligations*, not inferred ProofSteps or new GIVENs.
Only equality orientations from typed, screened Toda Definition/Propositions
are offered; arbitrary equalities never acquire a symmetric expansion.
"""
from __future__ import annotations

from expression import Composition, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2h_prop22_cited_hopf.source import expand_cited_prop22_right_formula
from phase171_r2i_eta_hopf_bridge.source import (
    eligible_eta_hopf_chains,
    expand_cited_eta_hopf_power,
)
from proof import Relation, RelationType
from relation_rules import equality_symmetry_inference_rule


def reverse_equality(goal: object) -> Relation | None:
    """Make the reverse typed equality, without asserting or proving it."""
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return None
    if goal.lhs == goal.rhs:
        return None
    return Relation(goal.rhs, goal.lhs, RelationType.EQUALITY)


def cited_chain_forward_equalities(available: tuple[object, ...]) -> tuple[Relation, ...]:
    """Select only concrete forward steps reachable from screened references.

    These remain unproved goals until canonical recursive search reconstructs
    the original R2I and Proposition 2.2 derivations.
    """
    if not isinstance(available, tuple):
        raise TypeError("screened fixed-statement conclusions must be a tuple")
    found: list[Relation] = []
    for chain in eligible_eta_hopf_chains(available):
        formula = Relation(
            MapApplication(
                EHP_H_MAP,
                Composition(chain.alpha, Suspension(chain.beta)),
            ),
            Composition(
                MapApplication(EHP_H_MAP, chain.alpha),
                Suspension(chain.beta),
            ),
            RelationType.EQUALITY,
        )
        for forward in (
            chain.alpha_composition,
            chain.hopf_composition,
            chain.cited_hopf,
            chain.intermediate,
            chain.beta_composition,
            chain.conclusion,
            formula,
        ):
            original = (
                expand_cited_eta_hopf_power(forward, available)
                + expand_cited_prop22_right_formula(forward, available)
            )
            if len(original) != 1:
                continue
            if forward not in found:
                found.append(forward)
    return tuple(found)


def expand_reverse_cited_eta_hopf_equalities(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Require the forward equality as a genuine, recursively proved premise.

    No generic symmetry of arbitrary database equalities is introduced.
    Source availability merely permits a search route; it is not evidence.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return ()
    forwards = tuple(
        forward for forward in cited_chain_forward_equalities(available)
        if reverse_equality(forward) == goal
    )
    if len(forwards) != 1:
        return ()
    return (GoalExpansion(equality_symmetry_inference_rule(), (forwards[0],)),)
```

## `install.py` — 保護インストーラー（既存変更に対応）

```python
"""Guarded R11 insertion after the exact reviewed R10 public provider hook.

Preserves already installed R7–R10 patches. Rejects all unknown tracked edits.
"""
from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

from phase171_r2j_r4_r9_r10_public_short_exact.install import (
    GIT_TARGET,
    R10_HOOK,
    _complete_function,
    _git,
    _verified_source_and_state,
)

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / GIT_TARGET
OUTPUT = PACKAGE / "output"
R11_HOOK = (
    "        from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import (\n"
    "            expand_reverse_cited_eta_hopf_equalities,\n"
    "        )\n"
    "        directed = expand_reverse_cited_eta_hopf_equalities(goal, tuple(available))\n"
    "        if directed:\n"
    "            return directed\n"
)


def _normal(blob: bytes) -> str:
    return blob.decode("utf-8-sig").replace("\r\n", "\n")


def _verified_r11_state(head_bytes: bytes, current_bytes: bytes) -> tuple[str, str]:
    """Derive the exact R10 baseline and allow one source-anchored R11 hook."""
    current = _normal(current_bytes)
    if current.count(R11_HOOK) > 1:
        raise RuntimeError("duplicate R11 provider hook")
    without = current.replace(R11_HOOK, "", 1)
    baseline_bytes = without.encode("utf-8")
    state, canonical_r10 = _verified_source_and_state(head_bytes, baseline_bytes)
    if state != "ALREADY_INSTALLED" or without != canonical_r10:
        raise RuntimeError("R10 base is not exactly the reviewed complete provider")
    if canonical_r10.count(R10_HOOK) != 1:
        raise RuntimeError("R10 hook is not unique")
    patched = canonical_r10.replace(R10_HOOK, R10_HOOK + R11_HOOK, 1)
    if current == canonical_r10:
        mode = "READY_TO_PATCH"
    elif current == patched:
        mode = "ALREADY_INSTALLED"
    else:
        raise RuntimeError("unexpected provider modification; refuse overwrite")
    if patched.count(R11_HOOK) != 1 or R11_HOOK not in _complete_function(patched):
        raise RuntimeError("R11 hook escaped shared_expansion_provider")
    ast.parse(patched)
    return mode, patched


def install(*, dry_run: bool) -> bool:
    if _git("branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("develop branch required")
    if not TARGET.is_file():
        raise RuntimeError("shared provider file is absent")
    original = TARGET.read_bytes()
    state, final = _verified_r11_state(_git("show", f"HEAD:{GIT_TARGET}"), original)
    print("PHASE171_R2J_R4_R9_R11_HEAD=" + _git("rev-parse", "HEAD").decode().strip(), flush=True)
    print("PHASE171_R2J_R4_R9_R11_PATCH_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE171_R2J_R4_R9_R11_RESULT=PASS_DRY_RUN", flush=True)
        return False
    OUTPUT.mkdir(exist_ok=True)
    if state == "READY_TO_PATCH":
        (OUTPUT / "phase165_r52_r9_shared_math.BEFORE.py").write_bytes(original)
        newline = "\r\n" if b"\r\n" in original else "\n"
        bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
        TARGET.write_bytes(bom + final.replace("\n", newline).encode("utf-8"))
        print("PHASE171_R2J_R4_R9_R11_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(
        _complete_function(final) + "\n", encoding="utf-8",
    )
    (OUTPUT / "phase165_r52_r9_shared_math.FULL.py").write_bytes(TARGET.read_bytes())
    print("PHASE171_R2J_R4_R9_R11_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"), flush=True)
    print("PHASE171_R2J_R4_R9_R11_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.FULL.py"), flush=True)
    return state == "READY_TO_PATCH"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
```

## `audit.py` — 公開経路監査

```python
"""Audit source-anchored equality symmetry in the independent public search.

No original finished R2I ProofStep is imported into the public search. A
previous source-verified tree checks only the mathematical shape of the rule.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import (
    _checked_chain,
    _screened_context,
    build_cited_r2i_proof,
)
from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import (
    cited_chain_forward_equalities,
    expand_reverse_cited_eta_hopf_equalities,
    reverse_equality,
)
from proof import ProofRule, find_inference_matches_for_rule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*args: str) -> str:
    if args not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("only read-only Git operations")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.strip()


def inspect_public_eta_symmetry() -> dict:
    """Check source-bound inverse routes then independently search pi_6^3."""
    screened, target, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    forward_root, actual_chain, ancestry = build_cited_r2i_proof()
    if (
        forward_root.rule is not ProofRule.INFERENCE
        or forward_root.conclusion != chain.conclusion
        or actual_chain != chain
        or any(node.conclusion == target for node in ancestry)
    ):
        raise RuntimeError("R2I source-backed inference is unavailable")

    forwards = cited_chain_forward_equalities(available)
    if chain.alpha_composition not in forwards or len(forwards) < 5:
        raise RuntimeError("no exact, source-anchored forward equality set")
    expected = reverse_equality(chain.alpha_composition)
    original = next((node for node in ancestry
                     if node.conclusion == chain.alpha_composition
                     and node.rule is ProofRule.INFERENCE), None)
    if original is None or expected is None:
        raise RuntimeError("actual R2I forward inference is missing")
    proposed = expand_reverse_cited_eta_hopf_equalities(expected, available)
    shared = shared_expansion_provider(screened, proof_target=target)(expected)
    same = tuple(option for option in shared
                 if option.rule.name == "equality symmetry"
                 and option.subgoals == (chain.alpha_composition,))
    if len(proposed) != 1 or len(same) != 1:
        raise RuntimeError("public source-anchored inverse was not connected")
    matches = find_inference_matches_for_rule(proposed[0].rule, (original,))
    if len(matches) != 1:
        raise RuntimeError("existing equality symmetry rule rejected genuine R2I ancestry")
    inverse_step = derive_inference_proof_step(matches[0])
    if (inverse_step.rule is not ProofRule.INFERENCE
            or inverse_step.conclusion != expected
            or inverse_step.premises != (original,)):
        raise RuntimeError("reverse equality was not genuinely inferred")
    for forward in forwards:
        inverse = reverse_equality(forward)
        routes = expand_reverse_cited_eta_hopf_equalities(inverse, available)
        if len(routes) != 1 or routes[0].subgoals != (forward,):
            raise RuntimeError("typed eta-Hopf chain inversion is inconsistent")
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=target,
    )
    complete = (
        public.status.value == "complete" and public.conclusion == target
        and not public.open_goals
    )
    return {
        "phase": "171-R2J-R4-R9-R11",
        "mode": "PUBLIC_TYPED_ETA_HOPF_SYMMETRY_INTEGRATION",
        "registered_target": repr(target),
        "source_anchored_forward_routes": len(forwards),
        "first_reverse": repr(expected),
        "source_anchored_reverse_routes": len(forwards),
        "first_reverse_inference_matched": True,
        "shared_first_reverse_connected": True,
        "public_search_status": public.status.value,
        "public_complete": complete,
        "public_proven_steps": len(public.proven_steps),
        "public_open_goals": [repr(item)[:1500] for item in public.open_goals[:25]],
        "public_diagnostics": list(public.diagnostics[:20]),
        "new_given_added": 0,
        "completed_proof_imported": False,
        "web_modified": False,
        "trust_boundary_modified": False,
        "public_web_verified": False,
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
    print("PHASE171_R2J_R4_R9_R11_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R11_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R11_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_public_eta_symmetry()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked source changed during read-only audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    dest = OUTPUT / "audit.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R11_REVERSED_EQUALITY=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R11_SHARED_REVERSE_CONNECTED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R11_REVERSE_ROUTES=" + str(report["source_anchored_reverse_routes"]), flush=True)
    print("PHASE171_R2J_R4_R9_R11_PUBLIC_SEARCH=" + report["public_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R11_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    if report["public_open_goals"]:
        print("PHASE171_R2J_R4_R9_R11_FIRST_OPEN_GOAL=" + report["public_open_goals"][0], flush=True)
    print("PHASE171_R2J_R4_R9_R11_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R11_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R11_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R11_REPORT=" + str(dest), flush=True)
    print("PHASE171_R2J_R4_R9_R11_RESULT=PASS_SYMMETRY_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py` — 新規限定テスト

```python
"""Source-bound equality-symmetry and public-provider regressions."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase171_r2i_eta_hopf_bridge.audit import (
    _checked_chain,
    _screened_context,
    build_cited_r2i_proof,
)
from phase171_r2j_r4_r9_r11_public_eta_symmetry.audit import (
    _git,
    inspect_public_eta_symmetry,
)
from phase171_r2j_r4_r9_r11_public_eta_symmetry.install import (
    R11_HOOK,
    _complete_function,
    install,
)
from phase171_r2j_r4_r9_r11_public_eta_symmetry.source import (
    cited_chain_forward_equalities,
    expand_reverse_cited_eta_hopf_equalities,
    reverse_equality,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _case():
    screened, target, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    return screened, target, chain, available


def test_first_reverse_requires_actual_forward_proof_obligation():
    _, _, chain, available = _case()
    goal = reverse_equality(chain.alpha_composition)
    assert goal is not None
    proposal, = expand_reverse_cited_eta_hopf_equalities(goal, available)
    assert proposal.rule.name == "equality symmetry"
    assert proposal.subgoals == (chain.alpha_composition,)
    assert not any(isinstance(item, ProofStep) for item in proposal.subgoals)


def test_all_forward_orientations_are_screened_and_reversible():
    _, _, chain, available = _case()
    forwards = cited_chain_forward_equalities(available)
    assert chain.alpha_composition in forwards
    assert chain.conclusion in forwards
    assert len(forwards) >= 5
    for forward in forwards:
        reverse = reverse_equality(forward)
        assert reverse is not None
        proposals = expand_reverse_cited_eta_hopf_equalities(reverse, available)
        assert len(proposals) == 1
        assert proposals[0].subgoals == (forward,)


def test_source_free_and_incomplete_source_sets_cannot_propose_reversal():
    _, _, chain, available = _case()
    reverse = reverse_equality(chain.alpha_composition)
    assert expand_reverse_cited_eta_hopf_equalities(reverse, ()) == ()
    without_definition = tuple(item for item in available
                               if item != TodaEtaFamilyGeneralDefinition())
    assert expand_reverse_cited_eta_hopf_equalities(reverse, without_definition) == ()


def test_wrong_relation_and_wrong_generator_do_not_match():
    _, _, chain, available = _case()
    reverse = reverse_equality(chain.alpha_composition)
    assert reverse is not None
    invalid = replace(reverse, relation_type=RelationType.INEQUALITY)
    assert expand_reverse_cited_eta_hopf_equalities(invalid, available) == ()
    alien = HomotopyElement("alien", 3, source=6, target=3,
                            generator=GeneratorSymbol("alien"))
    mismatched = replace(reverse, lhs=alien)
    assert expand_reverse_cited_eta_hopf_equalities(mismatched, available) == ()
    assert expand_reverse_cited_eta_hopf_equalities(object(), available) == ()


def test_reverse_equality_refuses_nonsymmetric_statement_or_trivial_cycle():
    _, _, chain, available = _case()
    forward = chain.alpha_composition
    assert reverse_equality(object()) is None
    assert reverse_equality(replace(forward, relation_type=RelationType.ZERO)) is None
    assert reverse_equality(Relation("x", "x", RelationType.EQUALITY)) is None
    with pytest.raises(TypeError):
        expand_reverse_cited_eta_hopf_equalities(forward, [available])


def test_symmetry_matches_only_a_proved_forward_step_from_real_r2i():
    _, _, chain, available = _case()
    root, actual, ancestry = build_cited_r2i_proof()
    assert root.rule is ProofRule.INFERENCE
    assert actual == chain
    original, = tuple(node for node in ancestry
                      if node.conclusion == chain.alpha_composition
                      and node.rule is ProofRule.INFERENCE)
    goal = reverse_equality(chain.alpha_composition)
    route, = expand_reverse_cited_eta_hopf_equalities(goal, available)
    matches = find_inference_matches_for_rule(route.rule, (original,))
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == (original,)


def test_shared_provider_exposes_exact_inverse_route():
    screened, target, chain, available = _case()
    inverse = reverse_equality(chain.alpha_composition)
    proposals = shared_expansion_provider(screened, proof_target=target)(inverse)
    matches = tuple(item for item in proposals
                    if item.rule.name == "equality symmetry"
                    and item.subgoals == (chain.alpha_composition,))
    assert len(matches) == 1
    assert len(expand_reverse_cited_eta_hopf_equalities(inverse, available)) == 1


def test_guarded_installer_is_idempotent_in_dry_run():
    from pathlib import Path
    assert install(dry_run=True) is False
    import phase165_r52_r9_shared_math as module
    function = _complete_function(Path(module.__file__).read_text(encoding="utf-8-sig").replace("\r\n", "\n"))
    assert function.count(R11_HOOK) == 1


def test_read_only_git_guard():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_public_audit_is_fail_closed_and_does_not_replay_old_tree():
    report = inspect_public_eta_symmetry()
    assert report["first_reverse_inference_matched"] is True
    assert report["shared_first_reverse_connected"] is True
    assert report["new_given_added"] == 0
    assert report["completed_proof_imported"] is False
    assert report["public_search_status"] in ("complete", "partial", "search_failed")
```

## `run.ps1` — 解凍後の実行スクリプト

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Git repository root required' }
    python -B -m phase171_r2j_r4_r9_r11_public_eta_symmetry.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R11 guarded preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R11_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m phase171_r2j_r4_r9_r11_public_eta_symmetry.install
    if ($LASTEXITCODE -ne 0) { throw 'R9-R11 guarded patch failed' }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r11_public_eta_symmetry\tests\test_audit.py' `
        '.\phase171_r2i_eta_hopf_bridge\tests\test_cited_eta_hopf.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R11 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R11_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r11_public_eta_symmetry.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R11 public equality audit failed' }
} finally {
    Pop-Location
}
```
