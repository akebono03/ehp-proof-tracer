# Phase 163 R4-R13 — 全コード（追加ファイル）

変更対象：phase163_r4_r13_inventory.py、tests/test_phase163_r4_r13_inventory.py、audit.py、run.ps1。
既存の import、クラス、関数は変更しません。新規クラス・関数は phase163_r4_r13_inventory.py に追加します。

## phase163_r4_r13_inventory.py

```python
"""Phase 163 R4-R13: read-only inventory of typed and metadata-only records.

No new mathematical assertions, provenance claims, or proof-search eligibility.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from proof import Relation
from toda_literature_statement_boundary import TodaFixedStatementComponent


class InventoryClassification(str, Enum):
    TYPED_SOURCE_UNVERIFIED = "TYPED_SOURCE_UNVERIFIED"
    METADATA_ONLY = "METADATA_ONLY"
    OTHER_TYPED_NOT_AUDITED = "OTHER_TYPED_NOT_AUDITED"
    UNRESOLVED_SOURCE = "UNRESOLVED_SOURCE"


@dataclass(frozen=True)
class InventoryItem:
    assertion_id: str | None
    locator: str | None
    component_key: str | None
    classification: InventoryClassification
    statement_type: str | None
    scope_text: str | None
    scope_assessment: str
    generator_assessment: str
    detail: str


@dataclass(frozen=True)
class InventoryReport:
    items: tuple[InventoryItem, ...]
    proof_links_count: int

    def count(self, classification: InventoryClassification) -> int:
        return sum(item.classification is classification for item in self.items)


def _generator_assessment(content: object) -> str:
    if not isinstance(content, Relation):
        return "NOT_A_GROUP_RELATION"
    group = content.rhs
    if isinstance(group, (FiniteCyclicGroup, FreeCyclicGroup)):
        return "PRESENT" if group.generator is not None else "MISSING"
    if isinstance(group, DirectSumGroup):
        summands = group.summands
        return "PRESENT" if summands and all(
            isinstance(term, (FiniteCyclicGroup, FreeCyclicGroup))
            and term.generator is not None for term in summands
        ) else "INCOMPLETE_OR_UNSUPPORTED"
    return "NOT_A_CYCLIC_PRESENTATION"


def inventory_registry_snapshot(
    snapshot: RegistryBridgeResult,
    source_unverified_ids: frozenset[str],
    typed_scope_ids: frozenset[str],
) -> InventoryReport:
    """Classify every migration record without modifying registry or links.

    A text scope alone is not proof of a separately checked typed range.
    An assertion not explicitly in source_unverified_ids is NOT marked verified.
    """
    if not isinstance(snapshot, RegistryBridgeResult):
        raise TypeError("snapshot must be RegistryBridgeResult")
    if not isinstance(source_unverified_ids, frozenset) or not isinstance(typed_scope_ids, frozenset):
        raise TypeError("ID collections must be frozensets")
    if not typed_scope_ids.issubset(source_unverified_ids):
        raise ValueError("typed scope ids must be among audited typed registrations")
    items: list[InventoryItem] = []
    observed_ids: set[str] = set()
    for record in snapshot.records:
        if record.assertion_id is None:
            items.append(InventoryItem(
                assertion_id=None, locator=None, component_key=None,
                classification=InventoryClassification.UNRESOLVED_SOURCE,
                statement_type=None, scope_text=None,
                scope_assessment="NOT_APPLICABLE", generator_assessment="NOT_ASSESSED",
                detail=record.detail,
            ))
            continue
        assertion_id = record.assertion_id
        observed_ids.add(assertion_id)
        assertion = snapshot.registry.assertion(assertion_id)
        reference = snapshot.registry.reference(assertion.reference_id)
        original_component = isinstance(assertion.content, TodaFixedStatementComponent)
        if record.status is MigrationStatus.METADATA_ONLY:
            if not original_component:
                raise ValueError("metadata_only assertion unexpectedly contains typed content")
            classification = InventoryClassification.METADATA_ONLY
        elif record.status is MigrationStatus.STRUCTURED:
            if original_component:
                raise ValueError("structured assertion still contains component metadata")
            classification = (
                InventoryClassification.TYPED_SOURCE_UNVERIFIED
                if assertion_id in source_unverified_ids else
                InventoryClassification.OTHER_TYPED_NOT_AUDITED
            )
        else:
            classification = InventoryClassification.UNRESOLVED_SOURCE
        scope = assertion.scope
        scope_assessment = (
            "TYPED_SCOPE_CHECKED_SOURCE_UNVERIFIED" if assertion_id in typed_scope_ids
            else "TEXT_SCOPE_ONLY_NOT_CHECKED" if scope is not None
            else "NO_SCOPE_METADATA"
        )
        component_key = (
            assertion_id.rsplit(":", 1)[-1]
            if record.source == "boundary" else None
        )
        items.append(InventoryItem(
            assertion_id=assertion_id,
            locator=reference.locator,
            component_key=component_key,
            classification=classification,
            statement_type=type(assertion.content).__name__,
            scope_text=scope,
            scope_assessment=scope_assessment,
            generator_assessment=(
                "NOT_ASSESSED_METADATA_ONLY" if original_component
                else _generator_assessment(assertion.content)
            ),
            detail=record.detail,
        ))
    unknown_ids = source_unverified_ids - observed_ids
    if unknown_ids:
        raise ValueError("typed evidence refers to absent assertion ids: " + ", ".join(sorted(unknown_ids)))
    return InventoryReport(tuple(items), len(snapshot.proof_links))


def existing_phase163_r4_r13_inventory() -> InventoryReport:
    """Read R4-R11, R4-R12 and stable minimum snapshots; do not traverse proofs."""
    from phase163_r4_registry_bridge import build_registry_bridge
    from phase163_r4_r11_literature_registration import (
        existing_prop56_candidates,
        register_prop56_literature_statements,
    )
    from phase163_r4_r12_literature_registration import (
        existing_prop51_prop53_candidates,
        register_prop51_prop53_literature_statements,
    )
    from phase163_r4_r12_stable_bases import register_stable_minimal_dimensions, BASE_ID_1
    from toda_upstream_bootstrap import _build_phase50_result

    prop56_inputs = existing_prop56_candidates()
    prop56 = register_prop56_literature_statements(build_registry_bridge(), prop56_inputs)
    prop53_inputs = existing_prop51_prop53_candidates()
    prop53 = register_prop51_prop53_literature_statements(prop56.snapshot, prop53_inputs)
    minimal = register_stable_minimal_dimensions(
        prop53, _build_phase50_result()["final_group_step"].conclusion
    )
    typed_ids = frozenset(
        [e.assertion_id for e in prop56.evidence]
        + [e.assertion_id for e in prop53.evidence]
    )
    scope_ids = frozenset(
        ["boundary:Proposition 5.6:higher_nu_group_relation"]
        + ["boundary:Proposition 5.1:higher_eta_group_relation"]
        + ["boundary:Proposition 5.3:higher_eta_squared_group_relation"]
    )
    report = inventory_registry_snapshot(minimal.snapshot, typed_ids, scope_ids)
    stable = minimal.snapshot.registry.assertion(BASE_ID_1)
    if stable.origin.value != "proof_internal":
        raise ValueError("stable pi4_3 minimum must remain proof_internal")
    return report

```

## tests/test_phase163_r4_r13_inventory.py

```python
from dataclasses import replace

import pytest

from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r13_inventory import (
    InventoryClassification,
    _generator_assessment,
    inventory_registry_snapshot,
)
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, DirectSumGroup
from proof import Relation, RelationType


def test_inventory_original_boundary_is_metadata_only():
    report = inventory_registry_snapshot(build_registry_bridge(), frozenset(), frozenset())
    assert report.count(InventoryClassification.METADATA_ONLY) > 0
    assert any(item.component_key == "pi6_4_group_relation" and
               item.classification is InventoryClassification.METADATA_ONLY for item in report.items)


def test_inventory_does_not_assume_scope_was_typed_checked():
    report = inventory_registry_snapshot(build_registry_bridge(), frozenset(), frozenset())
    item = next(i for i in report.items if i.assertion_id ==
                "boundary:Proposition 5.3:higher_eta_squared_group_relation")
    assert item.scope_text == "n >= 5"
    assert item.scope_assessment == "TEXT_SCOPE_ONLY_NOT_CHECKED"


def test_inventory_records_no_phantom_source_verification():
    report = inventory_registry_snapshot(build_registry_bridge(), frozenset(), frozenset())
    assert report.count(InventoryClassification.TYPED_SOURCE_UNVERIFIED) == 0


def test_inventory_refuses_unknown_evidence_id():
    with pytest.raises(ValueError, match="absent assertion"):
        inventory_registry_snapshot(build_registry_bridge(), frozenset({"unknown"}), frozenset())


def test_inventory_refuses_scope_without_typed_evidence():
    with pytest.raises(ValueError, match="typed scope ids"):
        inventory_registry_snapshot(build_registry_bridge(), frozenset(), frozenset({"x"}))


def test_generator_assessment_for_cyclic_and_direct_sum():
    def relation(rhs):
        return Relation(lhs="group", rhs=rhs, relation_type=RelationType.EQUALITY)
    assert _generator_assessment(relation(FiniteCyclicGroup(order=2, generator="eta"))) == "PRESENT"
    assert _generator_assessment(relation(FreeCyclicGroup(generator="nu"))) == "PRESENT"
    assert _generator_assessment(relation(DirectSumGroup(summands=(
        FreeCyclicGroup(generator="nu"), FiniteCyclicGroup(order=4, generator="E_nu")
    )))) == "PRESENT"


def test_metadata_inventory_does_not_mutate_bridge():
    baseline = build_registry_bridge()
    before = tuple((r.assertion_id, r.status) for r in baseline.records)
    inventory_registry_snapshot(baseline, frozenset(), frozenset())
    assert before == tuple((r.assertion_id, r.status) for r in baseline.records)

```

## audit.py

```python
"""Read-only Phase 163 R4-R13 cross-registry registration inventory."""
from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) in sys.path:
    sys.path.remove(str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT))

from phase163_r4_r13_inventory import (
    InventoryClassification,
    existing_phase163_r4_r13_inventory,
)


def run_audit(destination: Path) -> dict[str, object]:
    report = existing_phase163_r4_r13_inventory()
    counts = Counter(item.classification.value for item in report.items)
    boundaries = [item for item in report.items if item.assertion_id and
                  item.assertion_id.startswith("boundary:")]
    unregistered = [item for item in boundaries if
                    item.classification is InventoryClassification.METADATA_ONLY]
    typed = [item for item in boundaries if
             item.classification is InventoryClassification.TYPED_SOURCE_UNVERIFIED]
    typed_scopes = [item for item in typed if item.scope_text is not None]
    scope_unchecked = [item for item in boundaries if item.scope_text is not None and
                       item.scope_assessment == "TEXT_SCOPE_ONLY_NOT_CHECKED"]
    generator_incomplete = [item for item in typed if
                            item.generator_assessment in ("MISSING", "INCOMPLETE_OR_UNSUPPORTED")]
    output = {
        "phase": "163 R4-R13",
        "audit_status": "READ_ONLY_INVENTORY_COMPLETE",
        "classification_counts": dict(sorted(counts.items())),
        "boundary_total": len(boundaries),
        "boundary_typed_source_unverified": len(typed),
        "boundary_metadata_only": len(unregistered),
        "typed_scope_count": sum(x.scope_assessment == "TYPED_SCOPE_CHECKED_SOURCE_UNVERIFIED" for x in typed_scopes),
        "metadata_scope_text_only": len(scope_unchecked),
        "typed_generator_incomplete": len(generator_incomplete),
        "proof_links_count": report.proof_links_count,
        "notes": [
            "No literature originals independently checked",
            "Other typed theorem_facts were not revalidated",
            "The independently registered pi4_3 proof-internal stable base is not counted as a fixed boundary",
            "No proof ancestry or backward search was executed",
        ],
        "items": [{**asdict(item), "classification": item.classification.value}
                  for item in report.items],
    }
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "summary.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 163 R4-R13 — Fixed Statement 横断棚卸し", "",
        "**監査状態: READ_ONLY_INVENTORY_COMPLETE**", "",
        f"- 文献境界の総数: {len(boundaries)}",
        f"- 型付き・原典未照合: {len(typed)}",
        f"- metadata_only: {len(unregistered)}",
        f"- 範囲が文字列だけの未登録候補: {len(scope_unchecked)}",
        f"- 型付き登録の生成元不足または未対応直和: {len(generator_incomplete)}",
        "", "## 未登録 Fixed Statement（登録候補）", "",
        "| locator | component_key | role / type | scope | generator |",
        "|---|---|---|---|---|",
    ]
    for item in unregistered:
        lines.append(f"| {item.locator} | `{item.component_key}` | {item.statement_type} | "
                     f"{item.scope_text or '-'} | {item.generator_assessment} |")
    lines.extend(["", "## 型付き登録済み（原典未照合）", "",
                  "| locator | component_key | type | scope | generator |",
                  "|---|---|---|---|---|"])
    for item in typed:
        lines.append(f"| {item.locator} | `{item.component_key}` | {item.statement_type} | "
                     f"{item.scope_text or '-'} | {item.generator_assessment} |")
    lines.extend(["", "## 境界・制限", "",
                  "- 文献原本の独立照合は行っていません。",
                  "- metadata_only の成分は Statement や ProofStep に昇格していません。",
                  "- 範囲は typed scope 検査済みと単なる文字列を区別しています。",
                  "- 生成元評価の NOT_A_GROUP_RELATION は不足の認定ではありません。",
                  "- pi_4^3 の独立登録は proof_internal として維持され、文献固定成分に数えていません。",
                  "- 全体 pytest、証明木の全祖先検証、Phase 164 接続は行っていません。", ""])
    (destination / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return output


if __name__ == "__main__":
    output = run_audit(Path("phase163_r4_r13_output"))
    print("Phase 163 R4-R13:", output["audit_status"])
    print("Boundary total:", output["boundary_total"])
    print("Typed source-unverified:", output["boundary_typed_source_unverified"])
    print("Metadata only:", output["boundary_metadata_only"])
    print("Saved phase163_r4_r13_output/report.md and summary.json")
    print("Full pytest not run.")

```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Required = @(
  'phase163_r4_registry_bridge.py',
  'unified_statement_registry.py',
  'phase163_r4_r11_literature_registration.py',
  'phase163_r4_r12_literature_registration.py',
  'phase163_r4_r12_stable_bases.py',
  'toda_literature_statement_boundary.py',
  'tests\test_phase59_prop53_integration.py'
)
foreach ($Filename in $Required) {
  if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
    throw "Missing prior phase file: $Filename"
  }
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r13_inventory.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r13_inventory.py') -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r13_inventory.py') -Destination (Join-Path $ProjectRoot 'tests\test_phase163_r4_r13_inventory.py') -Force
& python -B -m pytest -q tests/test_phase163_r4_r13_inventory.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R13 focused tests failed.' }
$env:PYTHONPATH = "$ProjectRoot$([System.IO.Path]::PathSeparator)$env:PYTHONPATH"
& python -B (Join-Path $PackageRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-R13 inventory audit failed.' }
Write-Host 'R4-R13 read-only inventory finished. Full pytest not run.'

```
