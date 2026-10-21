"""Phase 166 R3-AU: cross-audit sphere DB gen_coe generator display data.

Read-only audit. This phase does not invent a gen_coe -> typed-expression
conversion that production code does not currently have.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


SPHERE_FILENAMES = ("sphere.csv", "sphere(3).csv")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def parse_int_list(value: str) -> tuple[int, ...] | None:
    value = (value or "").strip()
    if not value:
        return ()
    try:
        return tuple(int(part) for part in value.split())
    except ValueError:
        return None


def locate(repo: Path, names: tuple[str, ...]) -> Path:
    inspected: list[Path] = []
    for name in names:
        for candidate in (repo / name, repo / "data" / name):
            inspected.append(candidate)
            if candidate.is_file():
                return candidate
    raise FileNotFoundError(
        "database CSV not found; inspected: "
        + ", ".join(str(path) for path in inspected)
    )


def classify_shape(gen_coe: tuple[int, ...] | None) -> str:
    if gen_coe is None:
        return "invalid"
    if not gen_coe:
        return "empty"
    nonzero = [value for value in gen_coe if value != 0]
    if len(nonzero) == 1:
        value = nonzero[0]
        if abs(value) == 1:
            return "single_basis"
        return "single_basis_with_coefficient"
    return "linear_combination"


def inspect(rows: list[dict[str, str]], source_path: Path) -> tuple[dict, list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    shape_counts: Counter[str] = Counter()
    stem_counts: Counter[str] = Counter()
    generator_counts: Counter[str] = Counter()

    for csv_line, row in enumerate(rows, start=2):
        raw_gen_coe = row.get("gen_coe", "")
        parsed = parse_int_list(raw_gen_coe)
        shape = classify_shape(parsed)
        shape_counts[shape] += 1

        n_text = (row.get("n", "") or "").strip()
        k_text = (row.get("k", "") or "").strip()
        try:
            n = int(float(n_text))
            k = int(float(k_text))
            stem_key = str(k)
        except ValueError:
            n = None
            k = None
            stem_key = "invalid"
        stem_counts[stem_key] += 1

        generator_text = (row.get("generator", "") or "").strip()
        generator_counts["nonempty" if generator_text else "empty"] += 1

        records.append(
            {
                "csv_line": csv_line,
                "n": n_text,
                "k": k_text,
                "component_id": (row.get("id", "") or "").strip(),
                "order": (row.get("orders", "") or "").strip(),
                "generator_text": generator_text,
                "element_ids": (row.get("Element", "") or "").strip(),
                "gen_coe_raw": raw_gen_coe,
                "gen_coe_shape": shape,
                "gen_coe_length": None if parsed is None else len(parsed),
                "gen_coe_nonzero_count": None if parsed is None else sum(value != 0 for value in parsed),
                "within_112_public_groups": bool(
                    n is not None and k is not None and 2 <= n <= 15 and 0 <= k <= 7
                ),
                "typed_expression_from_gen_coe_available": False,
                "generated_latex_from_gen_coe": "",
                "comparison_status": (
                    "INVALID_GEN_COE"
                    if parsed is None
                    else "UNWIRED_GEN_COE_TO_TYPED_EXPRESSION"
                ),
                "accuracy_confirmed": False,
            }
        )

    summary = {
        "phase": "166 R3-AU gen_coe cross audit",
        "read_only": True,
        "source_csv": str(source_path),
        "sphere_rows": len(rows),
        "all_registered_rows_audited": True,
        "limited_to_112_groups": False,
        "shape_counts": dict(sorted(shape_counts.items())),
        "generator_text_counts": dict(sorted(generator_counts.items())),
        "stem_counts": dict(
            sorted(
                stem_counts.items(),
                key=lambda item: (
                    item[0] == "invalid",
                    int(item[0]) if item[0] != "invalid" else 10**9,
                ),
            )
        ),
        "typed_expression_from_gen_coe_available": False,
        "generated_latex_comparison_completed": 0,
        "accuracy_confirmed": 0,
        "production_code_modified": False,
        "full_pytest_run": False,
        "finding": (
            "Current production code stores gen_coe on GroupComponent but has no "
            "gen_coe -> typed generator expression conversion path. Therefore this "
            "audit must not claim that generator_text and generated LaTeX agree."
        ),
        "next_boundary": (
            "A later substep may add a typed conversion only after the mathematical "
            "meaning of gen_coe is established from existing DB conventions and tests."
        ),
    }
    return summary, records


def write_records(path: Path, records: list[dict[str, object]]) -> None:
    if not records:
        path.write_text("", encoding="utf-8-sig")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "results",
    )
    args = parser.parse_args()

    source_path = locate(args.repo, SPHERE_FILENAMES)
    rows = read_csv(source_path)
    summary, records = inspect(rows, source_path)

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_records(args.output / "gen_coe_cross_audit.csv", records)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
