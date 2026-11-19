# Phase 175 R4R12R13R4 — 変更コード全文

既存の共有関数は環境依存の最新内容を保持し、インストーラが `output/shared_expansion_provider_FULL.py` に変更後の全文を書き出します。

## `rule.py`（新規ファイル全文）

```python
"""Generic EHP intermediate Hopf-zero rules for the shared backward search.

The zero-map conclusion is about H, NOT about its codomain group. Both
consecutive exactness windows are checked using Toda Proposition 4.2 indices.
This module supplies conditional rules only; no literature GIVEN is created.
"""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaHopfInvariantZeroStatement, TodaProp42ExactnessStatement


DELTA_TO_H_ZERO = "EHP injective Delta and H-Delta exactness imply zero Hopf map"
H_ZERO_TO_E_SURJ = "EHP zero Hopf map and E-H exactness imply suspension surjectivity"


def hopf_zero_inputs(goal: object) -> tuple[MapInjective, TodaProp42ExactnessStatement] | None:
    """Require the unique correctly indexed H-Delta exactness window."""
    if not isinstance(goal, TodaHopfInvariantZeroStatement):
        return None
    h = goal.map
    if not isinstance(h, TodaHopfInvariantMap):
        return None
    b, c = h.source_group, h.target_group
    if not isinstance(b, TodaPrimaryGroup) or not isinstance(c, TodaPrimaryGroup):
        return None
    if any(type(x) is not int for x in (
        b.group_dimension, b.sphere_dimension, c.group_dimension, c.sphere_dimension,
    )):
        return None
    n = b.sphere_dimension - 1
    i = b.group_dimension
    if n < 1 or c != TodaPrimaryGroup(i, 2 * n + 1):
        return None
    d = TodaPrimaryGroup(i - 2, n)
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=b,
        middle_term=c,
        target_term=d,
        first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
    ))
    if prop42_exactness_indices(exact) != (n, i, "h_delta"):
        return None
    return MapInjective(TodaDeltaMap(c, d)), exact


def hopf_zero_from_injective_delta_rule(goal: TodaHopfInvariantZeroStatement) -> InferenceRule:
    required = hopf_zero_inputs(goal)
    if required is None:
        raise ValueError("invalid typed H-Delta zero-map goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and hopf_zero_inputs(goal) == required
        )

    return InferenceRule(
        name=DELTA_TO_H_ZERO,
        description=(
            "Exactness gives im(H)=ker(Delta); an independently proved "
            "injective Delta has zero kernel, hence H is the zero map."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=MapInjective, statement_pattern=required[0]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[1]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_hopf_zero_from_injective_delta(goal: object) -> tuple[GoalExpansion, ...]:
    required = hopf_zero_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(hopf_zero_from_injective_delta_rule(goal), required),)


def suspension_surjective_inputs(
    goal: object,
) -> tuple[TodaHopfInvariantZeroStatement, TodaProp42ExactnessStatement] | None:
    """Require actual H=0, rather than the false shortcut that codomain(H)=0."""
    if not isinstance(goal, MapSurjective):
        return None
    e = goal.map
    if not isinstance(e, TodaSuspensionMap):
        return None
    a, b = e.source_group, e.target_group
    if not isinstance(a, TodaPrimaryGroup) or not isinstance(b, TodaPrimaryGroup):
        return None
    if any(type(x) is not int for x in (
        a.group_dimension, a.sphere_dimension, b.group_dimension, b.sphere_dimension,
    )):
        return None
    if b != TodaPrimaryGroup(a.group_dimension + 1, a.sphere_dimension + 1):
        return None
    n = a.sphere_dimension
    i = b.group_dimension
    c = TodaPrimaryGroup(i, 2 * n + 1)
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=a,
        middle_term=b,
        target_term=c,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
    ))
    if prop42_exactness_indices(exact) != (n, i, "e_h"):
        return None
    return TodaHopfInvariantZeroStatement(TodaHopfInvariantMap(b, c)), exact


def suspension_surjective_from_zero_hopf_rule(goal: MapSurjective) -> InferenceRule:
    required = suspension_surjective_inputs(goal)
    if required is None:
        raise ValueError("invalid typed E-H surjectivity goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and suspension_surjective_inputs(goal) == required
        )

    return InferenceRule(
        name=H_ZERO_TO_E_SURJ,
        description=(
            "Exactness gives im(E)=ker(H); an independently proved zero "
            "Hopf map has full kernel, so E is surjective."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaHopfInvariantZeroStatement,
                           statement_pattern=required[0]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[1]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_suspension_surjective_from_zero_hopf(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    required = suspension_surjective_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(suspension_surjective_from_zero_hopf_rule(goal), required),)
```

## `provider.py`（新規ファイル全文）

```python
"""Connect two ordinary generic EHP expansions to public backward search.

No hard-coded homotopy group, generator, route, or source assertion is supplied.
"""
from __future__ import annotations

from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r12r13r4_hopf_zero_public.rule import (
    expand_hopf_zero_from_injective_delta,
    expand_suspension_surjective_from_zero_hopf,
)


def expand_public_hopf_zero_ehp(goal: object) -> tuple[GoalExpansion, ...]:
    """Do not assert conclusions: return obligations for recursive resolution."""
    return (
        expand_hopf_zero_from_injective_delta(goal)
        + expand_suspension_surjective_from_zero_hopf(goal)
    )
```

## `installer.py`（新規ファイル全文）

```python
"""Fail-closed, single-hook installer; exports complete changed shared function."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("phase165_r52_r9_shared_math.py")
ANCHOR = "    # Phase 175 R4R12R13R3: conditional Delta injectivity and E surjectivity.\n"
INSERT = '''    # Phase 175 R4R12R13R4: retain H=0 as a verified intermediate ProofStep.
    # All subgoals are resolved by the ordinary source-first recursive search.
    from phase175_r4r12r13r4_hopf_zero_public.provider import (
        expand_public_hopf_zero_ehp,
    )
    extra_providers = (expand_public_hopf_zero_ehp,) + tuple(extra_providers)
'''


def render(text: str) -> tuple[str, bool]:
    if text.count(INSERT) == 1:
        return text, False
    if "expand_public_hopf_zero_ehp" in text:
        raise RuntimeError("R13R4_PARTIAL_OR_UNREVIEWED_INSTALLATION")
    if text.count(ANCHOR) != 1:
        raise RuntimeError("R13R4_MISSING_R13R3_ANCHOR")
    return text.replace(ANCHOR, INSERT + ANCHOR, 1), True


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    target = root / TARGET
    raw = target.read_bytes()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    after, required = render(text)
    output.mkdir(parents=True, exist_ok=True)
    start = after.index("def shared_expansion_provider(")
    next_def = after.find("\ndef ", start + 5)
    function = after[start:] if next_def == -1 else after[start:next_def]
    (output / "shared_expansion_provider_FULL.py").write_text(function, encoding="utf-8")
    if required and not dry_run:
        data = after.replace("\n", "\r\n").encode("utf-8") if b"\r\n" in raw else after.encode("utf-8")
        target.write_bytes(data)
    return {"target": str(TARGET), "required": required,
            "installed": required and not dry_run,
            "complete_changed_function": str(output / "shared_expansion_provider_FULL.py")}
```

## `audit.py`（新規ファイル全文）

```python
"""Phase 175 R13R4: install and audit general H-zero intermediate candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import traceback

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase175_r4r12r13r4_hopf_zero_public import installer
from phase175_r4r12r13r4_hopf_zero_public.rule import (
    DELTA_TO_H_ZERO, H_ZERO_TO_E_SURJ, hopf_zero_inputs,
    suspension_surjective_inputs,
)

PACKAGE = "phase175_r4r12r13r4_hopf_zero_public"


def git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", check=False)
    if done.returncode:
        raise RuntimeError("R13R4_GIT_FAILURE: " + " ".join(args) + " " + done.stderr.strip())
    return done.stdout.strip()


def audit_frontier() -> dict[str, object]:
    """Observe actual shared proposals; NEVER count a proposal as proof."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    e_goal = MapSurjective(TodaSuspensionMap(
        TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5),
    ))
    inputs = suspension_surjective_inputs(e_goal)
    if inputs is None:
        raise RuntimeError("R13R4_INVALID_EHP_GOAL")
    h_goal = inputs[0]
    delta_goal = hopf_zero_inputs(h_goal)
    if delta_goal is None:
        raise RuntimeError("R13R4_INVALID_H_DELTA_GOAL")
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase165_r52_r9_shared_math import shared_expansion_provider
    target = exact_prior_database_result(5, 4)
    if target is None:
        raise RuntimeError("R13R4_MISSING_TYPED_TARGET")
    bridge = build_shared_typed_bridge()
    expand = shared_expansion_provider(bridge, proof_target=target)
    e_options = tuple(expand(e_goal))
    h_options = tuple(expand(h_goal))
    delta_options = tuple(expand(delta_goal[0]))
    selected_e = tuple(x for x in e_options if x.rule.name == H_ZERO_TO_E_SURJ)
    selected_h = tuple(x for x in h_options if x.rule.name == DELTA_TO_H_ZERO)
    if len(selected_e) != 1 or len(selected_h) != 1:
        raise RuntimeError("R13R4_PUBLIC_H_ZERO_CHAIN_MISSING")
    if selected_e[0].subgoals != inputs or selected_h[0].subgoals != delta_goal:
        raise RuntimeError("R13R4_INCORRECT_PARENT_GOALS")
    return {
        "e_surjectivity_new_candidates": len(selected_e),
        "hopf_zero_new_candidates": len(selected_h),
        "delta_injectivity_candidates": len(delta_options),
        "hopf_zero_goal": repr(h_goal),
        "delta_injectivity_goal": repr(delta_goal[0]),
        "actual_recursive_proof_executed": False,
        "hopf_zero_proved": False,
        "e_surjectivity_proved": False,
        "target_group_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    result: dict[str, object] = {
        "phase": "175-R4R12R13R4", "dry_run": dry_run,
        "gate": "FAIL_R13R4", "new_given": 0,
        "new_mathematical_rules": 2,
        "new_axioms": 0,
        "new_generic_inference_connections": 2,
        "full_pytest_executed": False,
        "target_proof_complete": False,
    }
    try:
        if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
            raise RuntimeError("R13R4_WRONG_REPOSITORY_ROOT")
        if git(root, "branch", "--show-current") != "develop":
            raise RuntimeError("R13R4_WRONG_BRANCH")
        result["head"] = git(root, "rev-parse", "HEAD")
        result["install"] = installer.install(root, dry_run=dry_run, output=output)
        if not dry_run:
            result["frontier"] = audit_frontier()
        result["gate"] = ("PASS_R13R4_DRYRUN_NOT_COMPLETE" if dry_run
                          else "PASS_R13R4_ZERO_HOPF_PUBLIC_CANDIDATES_NOT_COMPLETE")
    except Exception as exc:
        result["error"] = type(exc).__name__ + ": " + str(exc)
        result["traceback"] = traceback.format_exc()[-6000:]
    path = output / ("dry_run_report.json" if dry_run else "report.json")
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PHASE175_R13R4_GATE=" + str(result["gate"]))
    print("PHASE175_R13R4_HEAD=" + str(result.get("head", "UNVERIFIED")))
    if "frontier" in result:
        print("PHASE175_R13R4_H_ZERO_CANDIDATES=" + str(result["frontier"]["hopf_zero_new_candidates"]))
        print("PHASE175_R13R4_E_CANDIDATES=" + str(result["frontier"]["e_surjectivity_new_candidates"]))
        print("PHASE175_R13R4_DELTA_CANDIDATES=" + str(result["frontier"]["delta_injectivity_candidates"]))
    print("PHASE175_R13R4_NEW_GIVEN=0")
    print("PHASE175_R13R4_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R13R4_REPORT=" + str(path))
    if "error" in result:
        print("PHASE175_R13R4_ERROR=" + str(result["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
```

## `tests/test_rule.py`（新規ファイル全文）

```python
"""Generic EHP H-zero proof obligations and negative guards."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import (
    TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase175_r4r12r13r4_hopf_zero_public import installer, provider
from phase175_r4r12r13r4_hopf_zero_public.rule import (
    DELTA_TO_H_ZERO, H_ZERO_TO_E_SURJ,
    expand_hopf_zero_from_injective_delta,
    expand_suspension_surjective_from_zero_hopf,
    hopf_zero_inputs, suspension_surjective_inputs,
)
from proof import InferenceRule, ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule
from toda_rules import TodaHopfInvariantZeroStatement


def e_goal() -> MapSurjective:
    return MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)))


def invented_proof(statement: object, rule: ProofRule = ProofRule.INFERENCE) -> ProofStep:
    return ProofStep(statement, (), rule, inference_rule=InferenceRule("test-only"))


def test_hopf_zero_is_intermediate_goal_not_zero_codomain() -> None:
    e_required = suspension_surjective_inputs(e_goal())
    assert e_required is not None
    h_goal, e_h = e_required
    assert isinstance(h_goal, TodaHopfInvariantZeroStatement)
    assert h_goal.map == TodaHopfInvariantMap(TodaPrimaryGroup(9, 5), TodaPrimaryGroup(9, 9))
    h_required = hopf_zero_inputs(h_goal)
    assert h_required is not None
    delta, h_delta = h_required
    assert delta == MapInjective(TodaDeltaMap(TodaPrimaryGroup(9, 9), TodaPrimaryGroup(7, 4)))
    assert e_h.window.target_term == h_delta.window.middle_term


def test_two_backward_expansions_are_visible() -> None:
    h_goal = suspension_surjective_inputs(e_goal())[0]
    assert len(provider.expand_public_hopf_zero_ehp(e_goal())) == 1
    assert len(provider.expand_public_hopf_zero_ehp(h_goal)) == 1
    assert provider.expand_public_hopf_zero_ehp(MapInjective(h_goal.map)) == ()


def test_zero_hopf_rule_accepts_only_both_proven_parents() -> None:
    h_goal = suspension_surjective_inputs(e_goal())[0]
    expansion = expand_hopf_zero_from_injective_delta(h_goal)[0]
    assert expansion.rule.name == DELTA_TO_H_ZERO
    parents = tuple(invented_proof(x) for x in expansion.subgoals)
    matches = find_inference_matches_for_rule(expansion.rule, parents)
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == h_goal
    assert not find_inference_matches_for_rule(expansion.rule, parents[:1])
    assert not find_inference_matches_for_rule(
        expansion.rule, (invented_proof(parents[0].conclusion, ProofRule.GIVEN), parents[1]),
    )


def test_surjectivity_rule_accepts_only_zero_map_and_exactness() -> None:
    expansion = expand_suspension_surjective_from_zero_hopf(e_goal())[0]
    assert expansion.rule.name == H_ZERO_TO_E_SURJ
    parents = tuple(invented_proof(x) for x in expansion.subgoals)
    matches = find_inference_matches_for_rule(expansion.rule, parents)
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == e_goal()
    assert not find_inference_matches_for_rule(expansion.rule, parents[:1])


def test_wrong_hopf_map_dimensions_are_rejected() -> None:
    normal = suspension_surjective_inputs(e_goal())[0]
    wrong = TodaHopfInvariantZeroStatement(TodaHopfInvariantMap(
        TodaPrimaryGroup(9, 5), TodaPrimaryGroup(9, 8)))
    assert hopf_zero_inputs(wrong) is None
    assert expand_hopf_zero_from_injective_delta(wrong) == ()
    assert hopf_zero_inputs(normal) is not None


def test_invalid_e_map_dimensions_rejected() -> None:
    wrong = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 6)))
    assert suspension_surjective_inputs(wrong) is None
    assert expand_suspension_surjective_from_zero_hopf(wrong) == ()


def test_installer_idempotence_and_fail_closed_anchor() -> None:
    source = "def shared_expansion_provider(bridge):\n" + installer.ANCHOR + "    return ()\n"
    changed, required = installer.render(source)
    assert required and changed.count("expand_public_hopf_zero_ehp") == 2
    assert installer.render(changed) == (changed, False)
    with pytest.raises(RuntimeError, match="ANCHOR"):
        installer.render("def not_the_public_provider():\n    return ()\n")
```

## `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$arguments = @('-m', 'phase175_r4r12r13r4_hopf_zero_public.audit', '--root', $root)
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q --import-mode=importlib phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py phase175_r4r12r13r3_public_delta_e_bridge/tests/test_provider.py phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
exit 0
```

## R13R4R1 修正注記

変更する実行ファイルは `run.ps1` のみ。上記の全文をそのまま置き換える。2つの `test_rule.py` を同時に収集する際は `--import-mode=importlib` を使用する。
