# R4-R11 repair3 完全コード

変更対象: 新規モジュール・新規テスト・監査・実行スクリプト。既存 API への変更なし。

## `phase163_r4_r11_literature_registration.py`

```python
"""Phase 163 R4-R11 repair3: register typed literature assertions as data.

Proof ancestry is deliberately not certified here. Every entry is marked
SOURCE_UNVERIFIED in a separate evidence ledger. No search eligibility granted.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase163_r4_r10_generator_integrity import verify_prop56_pi5_2_generator
from phase163_r4_r11_prop56_remaining import (
    COMPONENT_KEYS,
    verify_prop56_remaining_component,
)
from scalar_rules import ScalarGreaterEqualStatement
from unified_statement_registry import (
    AssertionKind,
    UnifiedStatementRegistry,
)


LOCATOR = "Proposition 5.6"
ALL_KEYS = ("pi5_2_group_relation",) + COMPONENT_KEYS


@dataclass(frozen=True)
class LiteratureAssertionInput:
    component_key: str
    statement: object
    source_description: str
    scope_statement: object | None = None

    def __post_init__(self) -> None:
        if self.component_key not in ALL_KEYS:
            raise ValueError("unknown Proposition 5.6 component")
        if self.statement is None:
            raise ValueError("statement is required")
        if not isinstance(self.source_description, str) or not self.source_description.strip():
            raise ValueError("source_description is required")


@dataclass(frozen=True)
class LiteratureAssertionEvidence:
    assertion_id: str
    source_description: str
    verification_status: str
    proof_status: str


@dataclass(frozen=True)
class LiteratureRegistrationResult:
    snapshot: RegistryBridgeResult
    evidence: tuple[LiteratureAssertionEvidence, ...]


def register_prop56_literature_statements(
    base: RegistryBridgeResult,
    inputs: tuple[LiteratureAssertionInput, ...],
) -> LiteratureRegistrationResult:
    """Register exactly five checked typed conclusions, without proof certification.

    The source_description is a candidate provenance label, not independent
    verification against the printed literature. Keep proof_links unchanged.
    """
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    if not isinstance(inputs, tuple):
        raise TypeError("inputs must be a tuple")
    if not all(isinstance(item, LiteratureAssertionInput) for item in inputs):
        raise TypeError("all items must be LiteratureAssertionInput")
    keys = tuple(item.component_key for item in inputs)
    if len(keys) != len(ALL_KEYS) or set(keys) != set(ALL_KEYS):
        raise ValueError("all five distinct Proposition 5.6 components required")

    ids = {f"boundary:{LOCATOR}:{key}" for key in ALL_KEYS}
    existing = {r.assertion_id: r for r in base.records if r.assertion_id in ids}
    if len(existing) != 5 or any(
        rec.source != "boundary" or rec.status is not MigrationStatus.METADATA_ONLY
        for rec in existing.values()
    ):
        raise ValueError("all five target entries must be metadata-only boundaries")

    # Validate on a temporary snapshot first. No mutation of base, even on errors.
    new_contents = {f"boundary:{LOCATOR}:{item.component_key}": item.statement for item in inputs}
    trial = _copy_snapshot(base, new_contents)
    verify_prop56_pi5_2_generator(trial)
    for item in inputs:
        if item.component_key in COMPONENT_KEYS:
            if item.component_key == "higher_nu_group_relation":
                if not isinstance(item.scope_statement, ScalarGreaterEqualStatement):
                    raise ValueError("typed scope n >= 6 required")
            elif item.scope_statement is not None:
                raise ValueError("unexpected scope statement for concrete component")
            verify_prop56_remaining_component(
                trial,
                item.component_key,
                higher_range=item.scope_statement,
            )
        elif item.scope_statement is not None:
            raise ValueError("unexpected scope for pi5_2 component")

    evidence = tuple(
        LiteratureAssertionEvidence(
            assertion_id=f"boundary:{LOCATOR}:{item.component_key}",
            source_description=item.source_description,
            verification_status="SOURCE_UNVERIFIED",
            proof_status="PROOF_ANCESTRY_NOT_CHECKED",
        )
        for item in inputs
    )
    return LiteratureRegistrationResult(snapshot=trial, evidence=evidence)


def _copy_snapshot(
    base: RegistryBridgeResult,
    new_contents: dict[str, object],
) -> RegistryBridgeResult:
    registry = UnifiedStatementRegistry()
    references: set[str] = set()
    for record in base.records:
        if record.assertion_id is None:
            continue
        current = base.registry.assertion(record.assertion_id)
        if current.reference_id not in references:
            registry.add_reference(base.registry.reference(current.reference_id))
            references.add(current.reference_id)
        if record.assertion_id in new_contents:
            current = replace(
                current,
                content=new_contents[record.assertion_id],
                kind=AssertionKind.STATEMENT,
            )
        registry.add_assertion(current)
    records: list[MigrationRecord] = []
    for record in base.records:
        if record.assertion_id in new_contents:
            records.append(replace(
                record,
                status=MigrationStatus.STRUCTURED,
                detail=(
                    "Typed literature candidate; source unverified; "
                    "no proof ancestry verification or proof eligibility"
                ),
            ))
        else:
            records.append(record)
    return RegistryBridgeResult(registry, tuple(records), base.proof_links)


def existing_prop56_candidates() -> tuple[LiteratureAssertionInput, ...]:
    """Read existing Phase 65 conclusions; do not treat their proofs as citations."""
    from probes.probe_phase65_capabilities import build_phase65_representative_result

    data = build_phase65_representative_result()
    sources = (
        ("pi5_2_group_relation", "pi5_2_step"),
        ("pi6_3_group_relation", "pi6_3_step"),
        ("pi7_4_group_relation", "pi7_4_step"),
        ("pi8_5_group_relation", "pi8_5_step"),
        ("higher_nu_group_relation", "higher_step"),
    )
    return tuple(
        LiteratureAssertionInput(
            component_key=key,
            statement=data[step_key].conclusion,
            source_description=f"Phase65 representative {step_key}; Toda {LOCATOR} candidate",
            scope_statement=(
                data["higher_range_step"].conclusion
                if key == "higher_nu_group_relation" else None
            ),
        )
        for key, step_key in sources
    )
```

## `tests/test_phase163_r4_r11_literature_registration.py`

```python
from dataclasses import replace

import pytest

from homotopy_groups import FiniteCyclicGroup
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from phase163_r4_r11_literature_registration import (
    ALL_KEYS,
    LiteratureAssertionInput,
    existing_prop56_candidates,
    register_prop56_literature_statements,
)
from proof import Relation
from scalar_rules import ScalarGreaterEqualStatement


def _base_and_inputs():
    return build_registry_bridge(), existing_prop56_candidates()


def test_r4_r11_repair3_registers_five_typed_literature_candidates():
    base, candidates = _base_and_inputs()
    result = register_prop56_literature_statements(base, candidates)
    assert tuple(item.component_key for item in candidates) == ALL_KEYS
    assert len(result.evidence) == 5
    for candidate in candidates:
        assertion_id = f"boundary:Proposition 5.6:{candidate.component_key}"
        assertion = result.snapshot.registry.assertion(assertion_id)
        assert assertion.content is candidate.statement
        assert any(
            record.assertion_id == assertion_id and record.status is MigrationStatus.STRUCTURED
            for record in result.snapshot.records
        )
    assert all(e.verification_status == "SOURCE_UNVERIFIED" for e in result.evidence)
    assert all(e.proof_status == "PROOF_ANCESTRY_NOT_CHECKED" for e in result.evidence)


def test_r4_r11_repair3_does_not_modify_base_or_add_proof_links():
    base, candidates = _base_and_inputs()
    original_links = base.proof_links
    result = register_prop56_literature_statements(base, candidates)
    assert result.snapshot.proof_links == original_links
    for candidate in candidates:
        assertion_id = f"boundary:Proposition 5.6:{candidate.component_key}"
        assert any(
            record.assertion_id == assertion_id and record.status is MigrationStatus.METADATA_ONLY
            for record in base.records
        )
        assert base.registry.assertion(assertion_id).content != candidate.statement


def test_r4_r11_repair3_rejects_missing_component():
    base, candidates = _base_and_inputs()
    with pytest.raises(ValueError, match="five distinct"):
        register_prop56_literature_statements(base, candidates[:-1])


def test_r4_r11_repair3_rejects_duplicate_component():
    base, candidates = _base_and_inputs()
    with pytest.raises(ValueError, match="five distinct"):
        register_prop56_literature_statements(base, candidates[:-1] + (candidates[0],))


def test_r4_r11_repair3_rejects_wrong_generator():
    base, candidates = _base_and_inputs()
    bad = candidates[1]
    relation = bad.statement
    assert isinstance(relation, Relation)
    changed = replace(relation, rhs=FiniteCyclicGroup(order=4, generator="wrong"))
    inputs = candidates[:1] + (replace(bad, statement=changed),) + candidates[2:]
    with pytest.raises(ValueError, match="generator"):
        register_prop56_literature_statements(base, inputs)


def test_r4_r11_repair3_requires_typed_higher_scope():
    base, candidates = _base_and_inputs()
    changed = candidates[:-1] + (replace(candidates[-1], scope_statement=None),)
    with pytest.raises(ValueError, match="typed scope"):
        register_prop56_literature_statements(base, changed)


def test_r4_r11_repair3_rejects_false_scope():
    base, candidates = _base_and_inputs()
    scope = candidates[-1].scope_statement
    assert isinstance(scope, ScalarGreaterEqualStatement)
    changed = candidates[:-1] + (
        replace(candidates[-1], scope_statement=replace(scope, right=5)),
    )
    with pytest.raises(ValueError, match="scope"):
        register_prop56_literature_statements(base, changed)


def test_r4_r11_repair3_rejects_prior_structured_target():
    base, candidates = _base_and_inputs()
    result = register_prop56_literature_statements(base, candidates)
    with pytest.raises(ValueError, match="metadata-only"):
        register_prop56_literature_statements(result.snapshot, candidates)
```

## `audit.py`

```python
"""Read-only Proposition 5.6 registration audit; no proof ancestry replay."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r11_literature_registration import (
    ALL_KEYS,
    existing_prop56_candidates,
    register_prop56_literature_statements,
)


def run_audit(directory: Path) -> dict[str, object]:
    base = build_registry_bridge()
    result = register_prop56_literature_statements(
        base, existing_prop56_candidates()
    )
    evidence = result.evidence
    output = {
        "phase": "163 R4-R11 repair3",
        "status": "TYPED_SOURCE_UNVERIFIED",
        "registered_count": len(evidence),
        "registered_keys": list(ALL_KEYS),
        "source_status": "SOURCE_UNVERIFIED",
        "proof_status": "PROOF_ANCESTRY_NOT_CHECKED",
        "proof_links_unchanged": result.snapshot.proof_links == base.proof_links,
        "original_metadata_unchanged": all(
            r.status.value == "metadata_only"
            for r in base.records
            if r.assertion_id in {e.assertion_id for e in evidence}
        ),
        "evidence": [
            {
                "assertion_id": e.assertion_id,
                "source_description": e.source_description,
                "verification_status": e.verification_status,
                "proof_status": e.proof_status,
            }
            for e in evidence
        ],
        "notes": [
            "All five typed components have verified structure and generators.",
            "This is a candidate literature assertion catalog, not literature authentication.",
            "No ProofStepLink generated and no backward search eligibility granted.",
            "Prior Phase 161 provenance failures are separate and unresolved.",
        ],
    }
    if len(evidence) != 5 or not output["proof_links_unchanged"]:
        raise RuntimeError("registration audit integrity failed")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "summary.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 163 R4-R11 repair3 — Proposition 5.6 型付き文献登録",
        "",
        "状態: TYPED_SOURCE_UNVERIFIED（型付き構造を登録、文献原本との独立照合は未実施）",
        "",
        "| 成分 | 型付き登録 | 文献照合 | 証明木検証 |",
        "|---|---|---|---|",
    ]
    for e in evidence:
        lines.append(
            f"| `{e.assertion_id.rsplit(':', 1)[-1]}` | STRUCTURED | {e.verification_status} | {e.proof_status} |"
        )
    lines.extend([
        "", "生成元・直和構造と `n >= 6` は既存の R10/R11 構造検査で確認。",
        "原典照合済み・証明済み・Phase 164 探索可能という意味ではありません。",
        "過去に検出された2個の前提なし推論ノードは未解決のままです。",
        "全体 pytest は実施していません。", "",
    ])
    (directory / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return output


if __name__ == "__main__":
    output = run_audit(Path("phase163_r4_r11_repair3_output"))
    print("Phase 163 R4-R11 repair3:", output["status"], output["registered_count"])
    print("Saved phase163_r4_r11_repair3_output/report.md")
    print("Full pytest not run.")
```

## `run.ps1`

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'proof.py',
  'homotopy_groups.py',
  'unified_statement_registry.py',
  'phase163_r4_registry_bridge.py',
  'phase163_r4_r10_generator_integrity.py',
  'phase163_r4_r11_prop56_remaining.py',
  'probes\probe_phase65_capabilities.py',
  'tests\test_phase65_prop56_integration.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing required project file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r11_literature_registration.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r11_literature_registration.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r11_literature_registration.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r11_literature_registration.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r11_literature_registration.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 repair3 focused tests failed; audit skipped.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R11 repair3 literature registration audit failed.' }
Write-Host 'R4-R11 repair3 typed literature registration complete. Full suite not run.'
```

## 完了条件

- 5成分の型付き Statement の検査成功
- 生成元・直和・範囲の維持
- 文献独立照合は SOURCE_UNVERIFIED のまま
- proof links を追加せず、既存 snapshot を変更しない
- Phase 164 の探索と既存 renderer は対象外
