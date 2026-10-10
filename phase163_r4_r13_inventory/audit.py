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
