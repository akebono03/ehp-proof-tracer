"""Phase 166 R3-AU-2: read-only cross-database generator audit."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def locate(repo: Path, names: tuple[str, ...]) -> Path:
    tried = []
    for name in names:
        for path in (repo / "data" / name, repo / name):
            tried.append(str(path))
            if path.is_file():
                return path
    raise FileNotFoundError("Not found. Tried: " + "; ".join(tried))


def parse_ids(value: str) -> tuple[int, ...] | None:
    try:
        return tuple(int(token) for token in value.split()) if value.strip() else ()
    except ValueError:
        return None


def classify_gen_coe(value: str) -> str:
    numbers = parse_ids(value)
    if numbers is None:
        return "invalid"
    if not numbers:
        return "empty"
    nonzero = [number for number in numbers if number != 0]
    if len(nonzero) == 1:
        return "single_basis" if abs(nonzero[0]) == 1 else "single_basis_with_coefficient"
    return "linear_combination" if nonzero else "all_zero"


def inspect(
    sphere_rows: list[dict[str, str]],
    generator_rows: list[dict[str, str]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    by_id: dict[int, list[dict[str, str]]] = defaultdict(list)
    malformed_master_ids = 0
    for row in generator_rows:
        try:
            by_id[int(row["id"])].append(row)
        except (KeyError, ValueError):
            malformed_master_ids += 1

    records: list[dict[str, object]] = []
    statuses: Counter[str] = Counter()
    shapes: Counter[str] = Counter()
    flags: Counter[str] = Counter()
    for csv_line, row in enumerate(sphere_rows, start=2):
        element_raw = (row.get("Element") or "").strip()
        gen_coe_raw = (row.get("gen_coe") or "").strip()
        display = (row.get("generator") or "").strip()
        ids = parse_ids(element_raw)
        shape = classify_gen_coe(gen_coe_raw)
        if ids is None:
            status = "INVALID_ELEMENT"
            matches: list[list[dict[str, str]]] = []
        else:
            matches = [by_id.get(identifier, []) for identifier in ids]
            if not ids:
                status = "EMPTY_ELEMENT"
            elif any(not group for group in matches):
                status = "UNKNOWN_ID"
            elif any(len(group) > 1 for group in matches):
                status = "DUPLICATE_ID"
            else:
                status = "RESOLVED_IDS_NOT_VERIFIED"
        statuses[status] += 1
        shapes[shape] += 1

        flag_list = []
        if not display:
            flag_list.append("EMPTY_GENERATOR_TEXT")
        if shape in {"linear_combination", "single_basis_with_coefficient"}:
            flag_list.append("NONTRIVIAL_GEN_COE")
        if shape in {"invalid", "empty", "all_zero"}:
            flag_list.append("MISSING_OR_ZERO_GEN_COE")
        if status != "RESOLVED_IDS_NOT_VERIFIED":
            flag_list.append("ELEMENT_LOOKUP_REVIEW")
        if any(not (match.get("display") or "").strip() for group in matches for match in group):
            flag_list.append("EMPTY_MASTER_DISPLAY")
        try:
            n, k = int((row.get("n") or "").strip()), int((row.get("k") or "").strip())
        except ValueError:
            n = k = None
            flag_list.append("INVALID_GROUP_INDEX")
        for flag in flag_list:
            flags[flag] += 1
        records.append({
            "csv_line": csv_line,
            "n": row.get("n", ""),
            "k": row.get("k", ""),
            "component_id": row.get("id", ""),
            "orders": row.get("orders", ""),
            "generator": display,
            "Element": element_raw,
            "gen_coe": gen_coe_raw,
            "gen_coe_shape": shape,
            "base_generator_ids": json.dumps(list(ids), ensure_ascii=False) if ids is not None else "",
            "base_display": json.dumps(
                [[match.get("display", "") for match in group] for group in matches],
                ensure_ascii=False,
            ),
            "base_latex": json.dumps(
                [[match.get("latex", "") for match in group] for group in matches],
                ensure_ascii=False,
            ),
            "base_n_k": json.dumps(
                [[{"n": match.get("n", ""), "k": match.get("k", "")} for match in group] for group in matches],
                ensure_ascii=False,
            ),
            "element_lookup_status": status,
            "review_flags": "|".join(flag_list),
            "within_112_range": n is not None and k is not None and 2 <= n <= 15 and 0 <= k <= 7,
            "generated_latex": "",
            "latex_comparison_status": "NOT_CONNECTED_TO_TYPED_RENDERER",
            "mathematical_identity_confirmed": False,
        })
    summary: dict[str, object] = {
        "phase": "166 R3-AU-2",
        "read_only": True,
        "sphere_rows": len(sphere_rows),
        "master_generator_rows": len(generator_rows),
        "malformed_master_ids": malformed_master_ids,
        "duplicate_master_id_entries": sum(len(group) - 1 for group in by_id.values()),
        "element_lookup_status_counts": dict(sorted(statuses.items())),
        "gen_coe_shape_counts": dict(sorted(shapes.items())),
        "review_flag_counts": dict(sorted(flags.items())),
        "review_rows": sum(bool(record["review_flags"]) for record in records),
        "outside_112_range_rows": sum(not record["within_112_range"] for record in records),
        "latex_comparisons": 0,
        "mathematical_identities_confirmed": 0,
        "production_code_modified": False,
        "full_pytest_run": False,
        "interpretation": "Element ID lookup is not proof of generator identity; gen_coe is not a typed expression.",
    }
    return summary, records


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
    sphere_file = locate(args.repo, ("sphere.csv", "sphere(3).csv"))
    master_file = locate(args.repo, ("HyoujiGen.csv",))
    summary, rows = inspect(read_csv(sphere_file), read_csv(master_file))
    summary["sphere_path"] = str(sphere_file)
    summary["master_path"] = str(master_file)
    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "all_rows.csv", rows)
    write_csv(args.output / "review_rows.csv", [row for row in rows if row["review_flags"]])
    write_csv(args.output / "special_generators.csv", [
        row for row in rows
        if any(part in str(row["generator"]).lower().replace(" ", "") for part in
               ("c_1", "c1", "ef_1", "ef1", "omega", "ω", "sigma", "σ"))
    ])
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
