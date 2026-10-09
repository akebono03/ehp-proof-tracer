"""Read-only inventory report for the available Phase 163 R4 adapters."""
from collections import Counter
from pathlib import Path

from phase163_r4_registry_bridge import build_registry_bridge


def main() -> None:
    result = build_registry_bridge()
    counts = Counter(record.status.value for record in result.records)
    sources = Counter(record.source for record in result.records)
    lines = [
        "# Phase 163 R4 — 部分統合監査",
        "",
        "この件数は bridge に読み込んだ登録レコード数であり、数学的に異なる全命題数ではない。",
        "",
        "## データソース別",
    ]
    lines.extend(f"- {key}: {value}" for key, value in sorted(sources.items()))
    lines.extend(["", "## 状態別"])
    lines.extend(f"- {key}: {value}" for key, value in sorted(counts.items()))
    lines.extend(["", "## 未解決", ""])
    if not result.unresolved:
        lines.append("- なし（対象としたデータソース内）")
    for record in result.unresolved:
        lines.append(f"- {record.source} / {record.source_key}: {record.detail}")
    lines.extend([
        "", "## R4 の境界", "",
        "- toda_rules.py の全推論規則についての網羅的移行は未実施。",
        "- standard_repository.py の ProofStep は明示的に渡した場合だけ橋渡しする。",
        "- boundary component は構造化した数学的 Statement ではなく metadata_only。",
        "- Definition の出典調査・全件登録は未実施。",
        "- 数学的同値性や文献内の証明完了時点は推定していない。",
        "- 既存 API、proof search、renderer の動作は変更しない。",
        "- 全体 pytest は未実施。",
    ])
    output = Path("phase163_r4_output")
    output.mkdir(exist_ok=True)
    target = output / "report.md"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Phase 163 R4 partial registry inventory saved: {target.resolve()}")
    print("Records:", len(result.records), "Unresolved:", len(result.unresolved))
    print("Not a complete mathematical assertion count. Full suite not run.")


if __name__ == "__main__":
    main()
