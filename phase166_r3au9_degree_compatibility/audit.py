"""Read-only inspection of generator base degrees and composition adjacency."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def parse_ints(value: str) -> tuple[int, ...] | None:
    try:
        return tuple(int(item) for item in (value or "").split())
    except ValueError:
        return None


def parse_number(value: str) -> int | None:
    try:
        return int((value or "").strip())
    except ValueError:
        return None


def inspect(sphere: list[dict[str, str]], master: list[dict[str, str]]) -> tuple[dict, list[dict]]:
    by_id: dict[int, list[dict[str, str]]] = {}
    for record in master:
        key = parse_number(record.get("id", ""))
        if key is not None:
            by_id.setdefault(key, []).append(record)

    output = []
    statuses = Counter()
    for csv_line, row in enumerate(sphere, 2):
        ids = parse_ints(row.get("Element", ""))
        factors = []
        if ids is not None:
            for identifier in ids:
                matches = by_id.get(identifier, [])
                if len(matches) == 1:
                    item = matches[0]
                    n = parse_number(item.get("n", ""))
                    k = parse_number(item.get("k", ""))
                    factors.append({
                        "id": identifier, "display": item.get("display", ""),
                        "latex": item.get("latex", ""), "n": n, "k": k,
                        "source": n + k if n is not None and k is not None else None,
                        "target": n, "stable": item.get("stable", ""),
                    })
                else:
                    factors.append({"id": identifier, "lookup_count": len(matches)})

        pairs = []
        if ids is not None:
            for left, right in zip(factors, factors[1:]):
                lt, rs = left.get("target"), right.get("source")
                if lt is None or rs is None:
                    status = "UNKNOWN_BASE_DEGREE"
                elif lt == rs:
                    status = "BASE_DEGREE_MATCH"
                else:
                    status = "BASE_DEGREE_MISMATCH_SHIFT_NOT_INFERRED"
                pairs.append({"left_id": left["id"], "right_id": right["id"],
                              "left_target": lt, "right_source": rs,
                              "difference_left_target_minus_right_source": lt - rs if lt is not None and rs is not None else None,
                              "status": status})
                statuses[status] += 1

        if ids is None:
            classification = "INVALID_ELEMENT"
        elif not ids:
            classification = "NO_FACTOR_IDS"
        elif any("lookup_count" in value for value in factors):
            classification = "ID_LOOKUP_REVIEW"
        elif any(value["source"] is None for value in factors):
            classification = "UNKNOWN_BASE_DEGREE"
        elif not pairs:
            classification = "SINGLE_FACTOR_BASE_DATA"
        elif all(value["status"] == "BASE_DEGREE_MATCH" for value in pairs):
            classification = "ALL_BASE_ADJACENCIES_MATCH"
        else:
            classification = "REQUIRES_DEGREE_RULE_REVIEW"
        statuses[classification] += 1
        output.append({
            "csv_line": csv_line, "n": row.get("n", ""), "k": row.get("k", ""),
            "component_id": row.get("id", ""), "Element": row.get("Element", ""),
            "generator_reference_optional": row.get("generator", ""),
            "factors_json": json.dumps(factors, ensure_ascii=False),
            "adjacency_json": json.dumps(pairs, ensure_ascii=False),
            "status": classification,
            "typed_expression_certified": False,
            "suspension_exponent_certified": False,
        })
    summary = {
        "phase": "166 R3-AU-9", "sphere_rows": len(sphere), "master_rows": len(master),
        "statuses": dict(sorted(statuses.items())),
        "rule": "n,k of master treated as candidate base source=n+k,target=n; no inferred suspension",
        "generator_reference_optional": True,
        "typed_expression_certified": 0, "production_code_modified": False,
        "full_pytest_run": False,
    }
    return summary, output


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        if rows:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results")
    args = parser.parse_args()
    def locate(name: str) -> Path:
        for path in (args.repo / "data" / name, args.repo / name):
            if path.is_file():
                return path
        raise FileNotFoundError(name)
    summary, rows = inspect(read_csv(locate("sphere.csv")), read_csv(locate("HyoujiGen.csv")))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(args.output / "all_degree_rows.csv", rows)
    write_csv(args.output / "degree_review_rows.csv", [row for row in rows if row["status"] in
              {"REQUIRES_DEGREE_RULE_REVIEW", "UNKNOWN_BASE_DEGREE", "ID_LOOKUP_REVIEW", "INVALID_ELEMENT"}])
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
