"""Read-only R3-AU-8 compatibility inspection; no inferred typing."""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def parse_ids(text: str) -> list[int] | None:
    try:
        return [int(x) for x in (text or "").split()]
    except ValueError:
        return None


def inspect(sphere: list[dict[str, str]], master: list[dict[str, str]]) -> tuple[dict, list[dict]]:
    columns = list(master[0]) if master else []
    index: dict[int, list[dict[str, str]]] = {}
    for row in master:
        try:
            index.setdefault(int(row["id"]), []).append(row)
        except (ValueError, KeyError, TypeError):
            continue
    records: list[dict] = []
    statuses = Counter()
    factor_counts = Counter()
    for line, row in enumerate(sphere, 2):
        ids = parse_ids(row.get("Element", ""))
        if ids is None:
            status = "INVALID_ELEMENT_IDS"
        elif not ids:
            status = "NO_COMPOSITION_IDS"
        elif any(len(index.get(i, [])) != 1 for i in ids):
            status = "ID_LOOKUP_REVIEW"
        else:
            status = "IDS_RESOLVED_TYPING_UNVERIFIED"
        statuses[status] += 1
        factor_counts[str(len(ids)) if ids is not None else "INVALID"] += 1
        details = []
        for factor_id in ids or []:
            hits = index.get(factor_id, [])
            details.append({
                "id": factor_id,
                "master_records": len(hits),
                "display": hits[0].get("display", "") if len(hits) == 1 else None,
                "master_raw": hits[0] if len(hits) == 1 else None,
            })
        records.append({
            "csv_line": line,
            "n": row.get("n", ""),
            "k": row.get("k", ""),
            "component_id": row.get("id", ""),
            "Element": row.get("Element", ""),
            "gen_coe": row.get("gen_coe", ""),
            "composition_factor_count": len(ids) if ids is not None else -1,
            "factor_metadata_json": json.dumps(details, ensure_ascii=False),
            "status": status,
            "composition_typed": False,
            "coefficient_sum_typed": False,
            "latex_certified": False,
        })
    summary = {
        "phase": "166 R3-AU-8",
        "sphere_rows": len(sphere),
        "master_rows": len(master),
        "master_columns": columns,
        "id_lookup_status": dict(sorted(statuses.items())),
        "composition_factor_counts": dict(sorted(factor_counts.items())),
        "existing_expression_nodes": ["HomotopyElement", "Composition", "Sum", "Multiple"],
        "existing_type_requirement": "Composition.is_type_compatible requires left.source == right.target",
        "interpretation": "Element is ordered composition IDs, gen_coe is a group-coordinate vector, generator is optional reference text",
        "typed_expression_certified": 0,
        "production_code_modified": False,
        "full_pytest_run": False,
    }
    return summary, records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results")
    args = parser.parse_args()
    def locate(name: str) -> Path:
        for candidate in (args.repo / "data" / name, args.repo / name):
            if candidate.is_file():
                return candidate
        raise FileNotFoundError(name)
    summary, records = inspect(read_rows(locate("sphere.csv")), read_rows(locate("HyoujiGen.csv")))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (args.output / "factor_metadata.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
