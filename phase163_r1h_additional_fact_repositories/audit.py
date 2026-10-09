"""Read-only inventory of additional known fact repositories."""
from __future__ import annotations

import csv
import importlib
import json
from pathlib import Path


TARGETS = (
    ("map_facts", "MAP_ISOMORPHISM_FACT_REPOSITORY", ("facts",)),
    ("generator_facts", "GENERATOR_FACT_REPOSITORY", ("typing_facts", "ambient_group_facts")),
)


def inspect_fact_repositories(importer=importlib.import_module):
    """Inspect selected existing singleton registries without modifying them."""
    rows = []
    errors = []
    for module_name, repository_name, attributes in TARGETS:
        try:
            repository = getattr(importer(module_name), repository_name)
            for attribute in attributes:
                entries = getattr(repository, attribute)
                if not isinstance(entries, tuple):
                    raise TypeError(f"{repository_name}.{attribute} is not a tuple")
                for index, entry in enumerate(entries):
                    rows.append({
                        "module": module_name,
                        "repository": repository_name,
                        "collection": attribute,
                        "index": index,
                        "entry_type": type(entry).__name__,
                        "entry_repr": repr(entry),
                    })
        except Exception as exc:
            errors.append({"repository": repository_name, "error": f"{type(exc).__name__}: {exc}"})
    return rows, errors


def write_report(output: Path, rows: list[dict], errors: list[dict]):
    """Write a bounded factual report, not an inferred theorem count."""
    output.mkdir(parents=True, exist_ok=True)
    with (output / "fact_entries.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=(
            "module", "repository", "collection", "index", "entry_type", "entry_repr"
        ))
        writer.writeheader()
        writer.writerows(rows)
    counts = {}
    for row in rows:
        key = f"{row['repository']}.{row['collection']}"
        counts[key] = counts.get(key, 0) + 1
    summary = {
        "phase": "163 R1H",
        "status": "R1_NOT_COMPLETE",
        "counts_of_fact_instances": counts,
        "errors": errors,
        "limitations": [
            "Fact entries are not necessarily published mathematical statements",
            "Only two explicitly named singleton repositories are inspected",
            "InferenceRuleCatalog is a different category and is not counted here",
            "Other runtime repositories and literature ordering remain unverified",
        ],
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 163 R1H — 追加 Fact Repository 監査", "",
        "この集計は選択した Fact Repository の登録実体であり、数学的命題の総数ではありません。", "",
        *[f"- `{key}`: {value} 件" for key, value in sorted(counts.items())],
        "", "## エラー", *([f"- {item['repository']}: {item['error']}" for item in errors] or ["- なし"]),
        "", "## 次の境界", "推論規則の Catalog と文献 Statement を区別して追加調査する。", "",
    ]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main():
    rows, errors = inspect_fact_repositories()
    summary = write_report(Path("phase163_r1h_output"), rows, errors)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
