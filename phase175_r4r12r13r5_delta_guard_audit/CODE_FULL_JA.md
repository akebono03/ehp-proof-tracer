# R13R5 完全コード

今回新規追加する全ファイルを以下に記す。既存クラス・関数・import は変更しない。

## `AUDIT_PLAN_JA.md`

```markdown
# Phase 175 R4R12R13R5 — Δ 単射候補の型付き監査

## 調査対象

- `phase175_r4r12r13r2_delta_injective_e_surjective.rule.delta_injective_inputs`
- `phase175_r4r12r13r3_public_delta_e_bridge.provider.delta_free_coordinate_proposals`
- `phase175_r4r10_cited_58_prop25_public.source.canonical_toda58`
- `phase169_r10e4_ordered_db_prior.db_prior.exact_prior_database_result`
- `phase165_r52_r9_shared_math.shared_expansion_provider`

## 目的

Δ 単射候補が0件となる位置を、出典・群の直和型・自由生成元・有限生成元・座標計算・公開接続に分けて記録する。監査結果をもって未解決証明を完成と見なさない。

## 変更範囲

追加するのはこの監査用パッケージのみ。既存ファイル、API、数学規則、GIVEN、証明データは変更しない。

## Gate

DryRun と本実行で読み取り専用監査が正常終了し、限定 pytest 3件が通過したら監査 PASS。`DELTA_CANDIDATES=0` 自体は未完成であり監査失敗を意味しない。

## 次の境界

R13R5 の結果で具体的な不一致が確定した後に、必要性が数学的に検証された一般的な表現同値性または照合規則のみを別 Phase/round で検討する。全体 pytest は Phase 175 の最後にのみ実施する。

```

## `README.md`

```markdown
# Phase 175 R4R12R13R5 — Delta Typed Guard Audit

This package performs a read-only audit of the existing, conditional Toda (5.8) Delta injectivity candidate. It compares the cited expression's canonical generator objects to the actual earlier database group presentation and checks whether the shared provider emits a proposal.

It does not alter production code, add mathematical rules, add GIVENs, or claim a completed proof. The audit explicitly distinguishes citation screening, group shape, each generator's exact equality, free-coordinate calculation, rule acceptance, and shared-provider availability.

Run from the repository root with `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r13r5_delta_guard_audit\run.ps1 -DryRun`, then without `-DryRun`.

Only three focused tests are executed. Full pytest is reserved for the end of Phase 175.

```

## `__init__.py`

```python
"""Read-only Phase 175 R13R5 audit."""

```

## `audit.py`

```python
"""Read-only R13R5 audit of the typed Delta-injectivity candidate frontier."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import traceback

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase165_r14_r6_generic_iso import MapInjective
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import (
    _linear_coordinates,
    delta_injective_inputs,
    DELTA_RULE_NAME,
)
from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
    delta_free_coordinate_proposals,
    screened_toda58_available,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from proof import Relation, RelationType

PACKAGE = "phase175_r4r12r13r5_delta_guard_audit"


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("R13R5_GIT_FAILURE: " + process.stderr.strip())
    return process.stdout.strip()


def inspect_delta_guard() -> dict[str, object]:
    """Separate citation, group structure, generator identity, and provider wiring."""
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    signed = canonical_toda58()
    goal = MapInjective(signed.map)
    source = Relation(signed.map.source_group, FreeCyclicGroup(signed.element), RelationType.EQUALITY)
    target = exact_prior_database_result(4, 3)
    proof_target = exact_prior_database_result(5, 4)
    if proof_target is None:
        raise RuntimeError("R13R5_TARGET_PRIOR_RECORD_MISSING")
    bridge = build_shared_typed_bridge()
    cited = screened_toda58_available(bridge)
    direct = delta_free_coordinate_proposals(goal, cited58=cited)
    shared = tuple(shared_expansion_provider(bridge, proof_target=proof_target)(goal))
    selected = tuple(candidate for candidate in shared if candidate.rule.name == DELTA_RULE_NAME)
    structure: dict[str, object] = {
        "target_prior_exists": target is not None,
        "target_is_relation": isinstance(target, Relation),
        "target_is_equality": isinstance(target, Relation) and target.relation_type is RelationType.EQUALITY,
        "target_lhs_matches_delta": isinstance(target, Relation) and target.lhs == signed.map.target_group,
        "target_rhs_is_direct_sum": isinstance(target, Relation) and isinstance(target.rhs, DirectSumGroup),
        "target_repr": repr(target),
        "source_repr": repr(source),
        "delta_image_repr": repr(signed),
    }
    if isinstance(target, Relation) and isinstance(target.rhs, DirectSumGroup):
        parts = target.rhs.summands
        free = tuple(p for p in parts if isinstance(p, FreeCyclicGroup))
        finite = tuple(p for p in parts if isinstance(p, FiniteCyclicGroup))
        structure.update({
            "summand_count": len(parts),
            "summand_types": [type(p).__name__ for p in parts],
            "free_summand_count": len(free),
            "finite_summand_count": len(finite),
            "summand_generator_reprs": [repr(getattr(p, "generator", None)) for p in parts],
        })
        if len(free) == 1 and len(finite) == 1:
            expression = signed.positive_value
            structure.update({
                "source_free_coordinate_expression_repr": repr(expression.left.expression),
                "source_torsion_coordinate_expression_repr": repr(expression.right.expression),
                "free_generator_exact_match": free[0].generator == expression.left.expression,
                "torsion_generator_exact_match": finite[0].generator == expression.right.expression,
                "linear_coordinates": _linear_coordinates(
                    expression, free[0].generator, finite[0].generator,
                ),
                "torsion_order": finite[0].order,
            })
    accepted = delta_injective_inputs(goal, source, target, signed)
    structure["delta_guard_accepts"] = accepted is not None
    return {
        "toda58_citation_screened": cited,
        "direct_provider_candidate_count": len(direct),
        "shared_provider_candidate_count": len(selected),
        "shared_other_candidate_names": [c.rule.name for c in shared if c.rule.name != DELTA_RULE_NAME][:15],
        "guard": structure,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "public_code_modified": False,
        "recursive_proof_executed": False,
        "proof_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    report: dict[str, object] = {
        "phase": "175-R4R12R13R5", "dry_run": dry_run,
        "gate": "FAIL_R13R5", "full_pytest_executed": False,
        "new_given": 0, "new_mathematical_rules": 0,
        "target_proof_complete": False,
    }
    try:
        if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
            raise RuntimeError("R13R5_WRONG_ROOT")
        if git(root, "branch", "--show-current") != "develop":
            raise RuntimeError("R13R5_WRONG_BRANCH")
        report["head"] = git(root, "rev-parse", "HEAD")
        report["diagnostics"] = inspect_delta_guard()
        report["gate"] = "PASS_R13R5_READ_ONLY_DELTA_GUARD_AUDIT_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    path = output / ("dry_run_report.json" if dry_run else "report.json")
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print("PHASE175_R13R5_GATE=" + str(report["gate"]))
    print("PHASE175_R13R5_HEAD=" + str(report.get("head", "UNVERIFIED")))
    diagnostics = report.get("diagnostics", {})
    if diagnostics:
        print("PHASE175_R13R5_CITED58=" + str(diagnostics["toda58_citation_screened"]))
        print("PHASE175_R13R5_DIRECT_DELTA_CANDIDATES=" + str(diagnostics["direct_provider_candidate_count"]))
        print("PHASE175_R13R5_SHARED_DELTA_CANDIDATES=" + str(diagnostics["shared_provider_candidate_count"]))
        guard = diagnostics["guard"]
        for key in ("target_is_relation", "target_lhs_matches_delta", "target_rhs_is_direct_sum", "free_generator_exact_match", "torsion_generator_exact_match", "linear_coordinates", "delta_guard_accepts"):
            print("PHASE175_R13R5_" + key.upper() + "=" + str(guard.get(key, "NOT_APPLICABLE")))
    print("PHASE175_R13R5_NEW_GIVEN=0")
    print("PHASE175_R13R5_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R13R5_REPORT=" + str(path))
    if "error" in report:
        print("PHASE175_R13R5_ERROR=" + str(report["error"]))
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

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$arguments = @('-m', 'phase175_r4r12r13r5_delta_guard_audit.audit', '--root', $root)
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q --import-mode=importlib phase175_r4r12r13r5_delta_guard_audit/tests/test_r13r5_delta_diagnostics.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
exit 0

```

## `tests/test_r13r5_delta_diagnostics.py`

```python
"""No proof may follow from candidate existence or a fabricated generator match."""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase165_r14_r6_generic_iso import MapInjective
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import delta_injective_inputs
from phase175_r4r12r13r3_public_delta_e_bridge.provider import delta_free_coordinate_proposals
from proof import Relation, RelationType


def matching_target():
    signed = canonical_toda58()
    return Relation(
        signed.map.target_group,
        DirectSumGroup((
            FreeCyclicGroup(signed.positive_value.left.expression),
            FiniteCyclicGroup(4, signed.positive_value.right.expression),
        )),
        RelationType.EQUALITY,
    )


def test_r13r5_matching_typed_generators_enable_only_a_candidate():
    signed = canonical_toda58()
    goal = MapInjective(signed.map)
    source = Relation(signed.map.source_group, FreeCyclicGroup(signed.element), RelationType.EQUALITY)
    assert delta_injective_inputs(goal, source, matching_target(), signed) is not None
    assert len(delta_free_coordinate_proposals(
        goal, cited58=True, database_lookup=lambda n, k: matching_target() if (n, k) == (4, 3) else None,
    )) == 1


def test_r13r5_missing_citation_does_not_emit_delta_candidate():
    signed = canonical_toda58()
    assert not delta_free_coordinate_proposals(
        MapInjective(signed.map), cited58=False,
        database_lookup=lambda n, k: matching_target(),
    )


def test_r13r5_unmatched_torsion_generator_is_rejected():
    signed = canonical_toda58()
    bad_target = Relation(
        signed.map.target_group,
        DirectSumGroup((FreeCyclicGroup(signed.positive_value.left.expression),
                        FiniteCyclicGroup(4, signed.element))),
        RelationType.EQUALITY,
    )
    source = Relation(signed.map.source_group, FreeCyclicGroup(signed.element), RelationType.EQUALITY)
    assert delta_injective_inputs(MapInjective(signed.map), source, bad_target, signed) is None

```
