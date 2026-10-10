"""Phase 163 R4-R12 repair2 focused stable-base audit."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) in sys.path:
    sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))

from phase163_r4_r12_stable_bases import (
    BASE_ID_1, BASE_ID_2, GENERAL_ID_1, GENERAL_ID_2,
    existing_stable_minimal_registration,
)


def run_audit(destination: Path) -> dict[str, object]:
    result = existing_stable_minimal_registration()
    registry = result.snapshot.registry
    targets = (BASE_ID_1, BASE_ID_2, GENERAL_ID_1, GENERAL_ID_2)
    statements = {key: registry.assertion(key) for key in targets}
    output = {
        "phase": "163 R4-R12 repair2",
        "status": "TYPED_SOURCE_UNVERIFIED",
        "new_independent_minimum": BASE_ID_1,
        "existing_independent_minimum": BASE_ID_2,
        "generic_1_scope": statements[GENERAL_ID_1].scope,
        "generic_2_scope": statements[GENERAL_ID_2].scope,
        "1_stem_relation": result.relation_1,
        "2_stem_relation": result.relation_2,
        "source_verification": result.source_status,
        "proof_ancestry": result.proof_status,
        "base_1_generator": repr(statements[BASE_ID_1].content.rhs.generator),
        "base_2_generator": repr(statements[BASE_ID_2].content.rhs.generator),
        "proof_links_count": len(result.snapshot.proof_links),
    }
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "summary.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 163 R4-R12 repair2 — stable 最低次元の独立登録",
        "", "状態: TYPED_SOURCE_UNVERIFIED", "",
        "| stem | 最低次元 Statement | 一般形の範囲 | 関係 |",
        "|---|---|---|---|",
        f"| 1-stem | `{BASE_ID_1}` | n >= 3 | n=3 は適用範囲内、個別の導出結果として記録 |",
        f"| 2-stem | `{BASE_ID_2}` | n >= 5 | n=4 は適用範囲外、既存の独立成分を保持 |",
        "", "pi_4^3 の出典候補は現行 Phase 50 の final_group_step.conclusion です。",
        "新しい文献固定成分と断定せず、PROOF_INTERNAL（導出結果）として区別しています。",
        "Proposition 5.1／5.3 の既存8成分や ProofStepLink は変更していません。",
        "原典の独立照合・証明木全祖先の検証・全体 pytest は未実施です。", "",
    ]
    (destination / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return output


if __name__ == "__main__":
    result = run_audit(Path("phase163_r4_r12_repair2_output"))
    print("Phase 163 R4-R12 repair2:", result["status"])
    print("Minimum stem entries: 2 (new 1, reused 1)")
    print("Saved phase163_r4_r12_repair2_output/report.md")
    print("Full pytest not run.")
