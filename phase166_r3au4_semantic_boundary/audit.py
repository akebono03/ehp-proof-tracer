"""R3-AU-4: read-only structural audit of Element and gen_coe."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def locate(repo: Path, filenames: tuple[str, ...]) -> Path:
    for filename in filenames:
        for candidate in (repo / "data" / filename, repo / filename):
            if candidate.is_file():
                return candidate
    raise FileNotFoundError("Missing input: " + ", ".join(filenames))


def integers(raw: str) -> tuple[int, ...] | None:
    try:
        return tuple(int(part) for part in (raw or "").split())
    except ValueError:
        return None


def inspect(rows: list[dict[str, str]]) -> tuple[dict[str, object], list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    classes: Counter[str] = Counter()
    lengths: Counter[str] = Counter()
    mismatch = 0
    optional_missing = 0
    for line, row in enumerate(rows, 2):
        element = integers(row.get("Element", ""))
        coefficients = integers(row.get("gen_coe", ""))
        optional = (row.get("generator") or "").strip()
        if not optional:
            optional_missing += 1
        if element is None or coefficients is None:
            category = "INVALID_ENCODING"
        elif not element and not coefficients:
            category = "EMPTY_DATA_ROW"
        elif not coefficients:
            category = "NO_COEFFICIENTS"
        elif all(coefficient == 0 for coefficient in coefficients):
            category = "ZERO_COEFFICIENT_VECTOR"
        elif sum(value != 0 for value in coefficients) > 1:
            category = "MULTIPLE_NONZERO_COEFFICIENTS"
        elif abs(next(x for x in coefficients if x != 0)) > 1:
            category = "SCALED_SINGLE_COEFFICIENT"
        else:
            category = "UNIT_SINGLE_COEFFICIENT"
        classes[category] += 1
        elen = None if element is None else len(element)
        clen = None if coefficients is None else len(coefficients)
        lengths[f"Element={elen};gen_coe={clen}"] += 1
        differing = elen is not None and clen is not None and elen != clen
        mismatch += differing
        records.append({
            "csv_line": line,
            "n": row.get("n", ""),
            "k": row.get("k", ""),
            "component_id": row.get("id", ""),
            "orders": row.get("orders", ""),
            "Element": row.get("Element", ""),
            "gen_coe": row.get("gen_coe", ""),
            "element_length": elen,
            "coefficient_length": clen,
            "lengths_differ": differing,
            "nonzero_positions_zero_based": json.dumps([i for i, x in enumerate(coefficients or ()) if x != 0]),
            "nonzero_values": json.dumps([x for x in (coefficients or ()) if x != 0]),
            "coefficient_class": category,
            "reference_generator_text": optional,
            "reference_generator_missing_is_error": False,
            "element_coefficient_alignment_inferred": False,
            "typed_expression_confirmed": False,
            "latex_confirmed": False,
        })
    return {
        "phase": "166 R3-AU-4",
        "source_rows": len(rows),
        "coefficient_classes": dict(sorted(classes.items())),
        "length_pairs": dict(sorted(lengths.items())),
        "different_element_and_coefficient_lengths": mismatch,
        "optional_reference_generator_blank": optional_missing,
        "generator_blank_is_error": False,
        "per_position_Element_gen_coe_alignment_assumed": False,
        "typed_expression_certified": 0,
        "latex_certified": 0,
        "production_code_modified": False,
        "full_pytest_run": False,
    }, records


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8-sig")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results")
    args = parser.parse_args()
    sphere = locate(args.repo, ("sphere.csv", "sphere(3).csv"))
    summary, rows = inspect(read_csv(sphere))
    summary["source_csv"] = str(sphere)
    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "all_rows.csv", rows)
    write_csv(args.output / "nontrivial_coefficients.csv", [r for r in rows if r["coefficient_class"] in ("MULTIPLE_NONZERO_COEFFICIENTS", "SCALED_SINGLE_COEFFICIENT")])
    write_csv(args.output / "zero_or_empty.csv", [r for r in rows if r["coefficient_class"] in ("ZERO_COEFFICIENT_VECTOR", "EMPTY_DATA_ROW", "NO_COEFFICIENTS")])
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
