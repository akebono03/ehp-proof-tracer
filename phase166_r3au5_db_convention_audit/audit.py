"""R3-AU-5: read-only inspection of composition IDs and generator coefficients."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def find_file(repo: Path, filename: str) -> Path:
    for path in (repo / "data" / filename, repo / filename):
        if path.is_file():
            return path
    raise FileNotFoundError(filename)


def ints(raw: str) -> tuple[int, ...] | None:
    try:
        return tuple(int(x) for x in (raw or "").split())
    except ValueError:
        return None


def audit(sphere_rows: list[dict[str, str]], master_rows: list[dict[str, str]]):
    master: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in master_rows:
        try:
            master[int(row["id"])].append(row)
        except (KeyError, ValueError):
            continue

    output = []
    categories = Counter()
    counts = Counter()
    for line, row in enumerate(sphere_rows, 2):
        raw_element = (row.get("Element") or "").strip()
        raw_coe = (row.get("gen_coe") or "").strip()
        element = ints(raw_element)
        coe = ints(raw_coe)
        names = [] if element is None else [
            [m.get("display", "") for m in master.get(i, [])] for i in element
        ]
        valid_ids = element is not None and all(len(master.get(i, [])) == 1 for i in element)
        nonzero = [] if coe is None else [(i, x) for i, x in enumerate(coe) if x]
        if not raw_element and not raw_coe and not (row.get("n") or "").strip():
            category = "SEPARATOR_CANDIDATE"
        elif element is None or coe is None:
            category = "INVALID_ENCODING"
        elif not valid_ids:
            category = "ID_LOOKUP_REVIEW"
        elif not nonzero:
            category = "ZERO_VECTOR"
        elif len(nonzero) > 1:
            category = "LINEAR_COMBINATION"
        elif abs(nonzero[0][1]) != 1:
            category = "SCALED_SINGLE"
        else:
            category = "UNIT_SINGLE"
        categories[category] += 1
        counts["reference_generator_blank"] += not bool((row.get("generator") or "").strip())
        counts["composition_factor_count_" + str(len(element) if element is not None else -1)] += 1
        counts["coefficients_count_" + str(len(coe) if coe is not None else -1)] += 1
        output.append({
            "csv_line": line,
            "n": row.get("n", ""),
            "k": row.get("k", ""),
            "id": row.get("id", ""),
            "orders": row.get("orders", ""),
            "Element": raw_element,
            "Element_factor_ids": json.dumps(element, ensure_ascii=False) if element is not None else "",
            "Element_factor_names": json.dumps(names, ensure_ascii=False),
            "gen_coe": raw_coe,
            "gen_coe_nonzero_positions_zero_based": json.dumps(nonzero),
            "reference_generator_optional": row.get("generator", ""),
            "classification": category,
            "composition_order_verified": bool(valid_ids and element),
            "coefficient_basis_order_verified": False,
            "typed_expression_connected": False,
            "latex_verified": False,
        })
    summary = {
        "phase": "166 R3-AU-5",
        "source_rows": len(sphere_rows),
        "master_rows": len(master_rows),
        "categories": dict(sorted(categories.items())),
        "counts": dict(sorted(counts.items())),
        "known_convention": {
            "Element": "ordered display-element IDs denoting composition",
            "gen_coe": "coordinates of the generator as a linear combination of elements",
            "max_composition_length": 5,
            "max_direct_sum_components": 12,
            "generator": "optional reference text",
        },
        "unverified": "mapping of coordinate positions to exact expression terms; mathematical typing and renderer output",
        "read_only": True,
        "production_code_modified": False,
        "full_pytest_run": False,
    }
    return summary, output


def write_rows(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        if records:
            writer = csv.DictWriter(stream, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results")
    args = parser.parse_args()
    sphere = next(
        (path for name in ("sphere.csv", "sphere(3).csv")
         for path in (args.repo / "data" / name, args.repo / name) if path.is_file()),
        None,
    )
    if sphere is None:
        raise FileNotFoundError("sphere.csv / sphere(3).csv")
    master = find_file(args.repo, "HyoujiGen.csv")
    summary, rows = audit(read_csv(sphere), read_csv(master))
    summary["source_csv"] = str(sphere)
    summary["master_csv"] = str(master)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_rows(args.output / "all_rows.csv", rows)
    write_rows(args.output / "nontrivial_rows.csv", [
        row for row in rows if row["classification"] in
        {"LINEAR_COMBINATION", "SCALED_SINGLE", "ZERO_VECTOR", "INVALID_ENCODING", "ID_LOOKUP_REVIEW"}
    ])
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
