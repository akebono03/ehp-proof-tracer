"""R10EO-R2 read-only, source-index artifact and live-goal audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase169_r10eo_r1_definition_audit.audit import inspect_live_goal
from phase169_r10eo_r2_definition_index.definition_index import (
    check_existing_reviewed_records,
    index_definitions,
)


def render_report(index: dict, checked: tuple[dict, ...], live: dict) -> str:
    """Report normalized candidates without implying literature approval."""
    lines = [
        "# Phase 169 R10EO-R2 — Definition Index 監査", "",
        "採用済み転写 TeX の字面一致を索引化しただけであり、Source Attestation（出典の審査済み認証）ではない。",
        "CSV・字面一致から FIXED_STATEMENT や GIVEN を生成しない。", "",
        "| ID | 生成元 | k | n0 | 一意な候補 | 出典候補 |",
        "|---:|---|---:|---:|---|---|",
    ]
    for entry in index["families"]:
        labels = ", ".join(f"{item['source_id']}:{item['line']}"
                           for item in entry["occurrences"])
        lines.append(
            f"| {entry['family_id']} | {entry['display']} | {entry['stem']} | "
            f"{entry['minimum_n']} | {entry['status']} | {labels or '—'} |"
        )
    lines.extend([
        "", "## 既存の審査済み Source Record との一致", "",
        f"既存の {len(checked)} 件について、構造化した字面候補と整合。",
        "既存の SOURCE_RECORDS と CHAPTER_VI_SOURCE_RECORDS は本工程で削除・変更しない。",
        "", "## 11-stem の実行時監査", "",
        f"- 群: `{live['target']}`",
        f"- Status: `{live['status']}`",
        f"- Open Goal: `{', '.join(live['open_goal_types'])}`",
        f"- Trust Boundary: `{live['trust']}`",
        "", "## 次工程との境界", "",
        "次工程で、採用済み文献・命題の掲載位置・定義の適用範囲を検証し、",
        "source attestation を明示した上で初めて既存の Definition GIVEN 経路に接続する。",
        "生成元の名称ごとの推論規則追加は行わない。",
        "完成証明が得られない限り Trust Boundary の PASS を主張しない。",
        "", "全体 pytest は Phase 最終段階のみ。", "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    indexed = index_definitions()
    reviewed = check_existing_reviewed_records(indexed)
    live = inspect_live_goal(n=30, k=11)
    report = {
        "phase": "169 R10EO-R2", "mode": "AUDIT_ONLY",
        "definition_index": indexed,
        "existing_reviewed_record_checks": reviewed,
        "pi41_30": live,
        "new_givens": 0,
        "new_inference_rules": 0,
        "production_changes": False,
        "full_pytest_run": False,
    }
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "audit.md").write_text(render_report(indexed, reviewed, live), encoding="utf-8")
    print("R10EO_R2_SERIES=" + str(indexed["registered_series"]))
    print("R10EO_R2_UNIQUE_TEXT_CANDIDATES=" + str(indexed["unique_literal_candidates"]))
    print("R10EO_R2_AMBIGUOUS_TEXT_CANDIDATES=" + str(indexed["ambiguous_literal_candidates"]))
    print("R10EO_R2_EXISTING_REVIEWED_RECORDS=" + str(len(reviewed)))
    zeta = next(x for x in indexed["families"] if x["family_id"] == 16)
    print("R10EO_R2_ZETA_TEXT_STATUS=" + zeta["status"])
    print("R10EO_R2_ZETA_CANDIDATES=" + str(len(zeta["occurrences"])))
    print("R10EO_R2_PI41_30_STATUS=" + live["status"])
    print("R10EO_R2_PI41_30_OPEN_GOALS=" + str(live["open_goal_types"]))
    print("R10EO_R2_PI41_30_TRUST=" + live["trust"])
    print("R10EO_R2_AUDIT_PATH=" + str(output / "audit.json"))
    print("R10EO_R2_MODE=AUDIT_ONLY")


if __name__ == "__main__":
    main()
