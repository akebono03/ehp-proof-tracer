
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
from pathlib import Path


REMOVABLE = "removable_duplicate"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _split_test_id(test_id: str) -> tuple[str, str]:
    file_path, function_name = test_id.split("::", 1)
    return file_path.replace("\\", "/"), function_name


def _function_sources(
    path: Path,
    function_name: str,
) -> list[str]:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    result = []

    for node in tree.body:
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == function_name
        ):
            decorator_lines = [d.lineno for d in node.decorator_list]
            start = min([node.lineno, *decorator_lines]) - 1
            end = node.end_lineno or node.lineno
            result.append("".join(lines[start:end]))

    return result


def _normalized(source: str) -> str:
    tree = ast.parse(source)
    return ast.dump(tree, include_attributes=False)


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--r3-3d-output",
        type=Path,
        default=Path("phase155_r3_3d_audit_output"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("phase155_r3_3d_r1_audit_output"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    r3d = (
        args.r3_3d_output
        if args.r3_3d_output.is_absolute()
        else repo_root / args.r3_3d_output
    )
    out = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root / args.output_dir
    )
    out.mkdir(parents=True, exist_ok=True)

    pair_path = r3d / "phase155_r3_3d_pair_closure.csv"
    dup_path = r3d / "phase155_r3_3d_duplicate_definitions.csv"

    if not pair_path.exists():
        raise SystemExit(f"missing R3-3D pair closure: {pair_path}")
    if not dup_path.exists():
        raise SystemExit(f"missing R3-3D duplicate definitions: {dup_path}")

    pair_rows = _read_csv(pair_path)
    dup_rows = _read_csv(dup_path)

    unresolved = [
        row
        for row in pair_rows
        if row.get("closure_status") == "unresolved_removable_pair"
    ]

    duplicate_details = []
    exact_duplicate_name_groups = 0
    divergent_duplicate_name_groups = 0

    for row in dup_rows:
        file_path = row["file_path"]
        function_name = row["function_name"]
        path = repo_root / file_path
        sources = _function_sources(path, function_name)

        normalized = [_normalized(source) for source in sources]
        hashes = [_hash(value) for value in normalized]
        exact = len(set(hashes)) == 1

        if exact:
            exact_duplicate_name_groups += 1
        else:
            divergent_duplicate_name_groups += 1

        duplicate_details.append(
            {
                "file_path": file_path,
                "function_name": function_name,
                "definition_count": len(sources),
                "exact_same_ast": exact,
                "normalized_hashes": hashes,
            }
        )

    duplicate_keys = {
        (row["file_path"], row["function_name"])
        for row in dup_rows
    }

    unresolved_details = []
    overlap_duplicate_names = set()

    for row in unresolved:
        older_file, older_name = _split_test_id(row["older_test_id"])
        newer_file, newer_name = _split_test_id(row["newer_test_id"])

        older_overlap = (older_file, older_name) in duplicate_keys
        newer_overlap = (newer_file, newer_name) in duplicate_keys

        if older_overlap:
            overlap_duplicate_names.add((older_file, older_name))
        if newer_overlap:
            overlap_duplicate_names.add((newer_file, newer_name))

        unresolved_details.append(
            {
                "candidate_id": row.get("candidate_id", ""),
                "older_test_id": row["older_test_id"],
                "newer_test_id": row["newer_test_id"],
                "older_overlap_source_duplicate": older_overlap,
                "newer_overlap_source_duplicate": newer_overlap,
            }
        )

    summary = {
        "unresolved_removable_pairs": len(unresolved),
        "source_level_duplicate_name_groups": len(dup_rows),
        "exact_duplicate_name_groups": exact_duplicate_name_groups,
        "divergent_duplicate_name_groups": divergent_duplicate_name_groups,
        "unresolved_pair_endpoints_overlapping_duplicate_names": len(
            overlap_duplicate_names
        ),
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (out / "phase155_r3_3d_r1_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out / "phase155_r3_3d_r1_unresolved_pairs.json").write_text(
        json.dumps(unresolved_details, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out / "phase155_r3_3d_r1_duplicate_definitions.json").write_text(
        json.dumps(duplicate_details, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Phase 155-R3-3D-r1 — closure failure root-cause audit",
        "",
        f"- unresolved removable pairs: {len(unresolved)}",
        f"- source-level duplicate name groups: {len(dup_rows)}",
        f"- exact duplicate name groups: {exact_duplicate_name_groups}",
        f"- divergent duplicate name groups: {divergent_duplicate_name_groups}",
        f"- unresolved-pair endpoints overlapping duplicate-name groups: {len(overlap_duplicate_names)}",
        "",
        "## Unresolved removable pairs",
        "",
    ]

    for item in unresolved_details:
        lines.extend(
            [
                f"- {item['candidate_id']}",
                f"  - older: `{item['older_test_id']}`",
                f"  - newer: `{item['newer_test_id']}`",
                f"  - older overlaps source duplicate: {item['older_overlap_source_duplicate']}",
                f"  - newer overlaps source duplicate: {item['newer_overlap_source_duplicate']}",
            ]
        )

    lines.extend(["", "## Source-level duplicate test names", ""])

    for item in duplicate_details:
        lines.extend(
            [
                f"- `{item['file_path']}::{item['function_name']}`",
                f"  - definitions: {item['definition_count']}",
                f"  - exact same AST: {item['exact_same_ast']}",
            ]
        )

    lines.extend(
        [
            "",
            "No production code or existing test was changed.",
            "Repository-wide pytest was NOT run.",
        ]
    )

    (out / "phase155_r3_3d_r1_summary.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("Phase 155-R3-3D-r1 root-cause audit completed.")
    print("unresolved removable pairs:", len(unresolved))
    print("source-level duplicate name groups:", len(dup_rows))
    print("exact duplicate name groups:", exact_duplicate_name_groups)
    print("divergent duplicate name groups:", divergent_duplicate_name_groups)
    print(
        "unresolved-pair endpoints overlapping duplicate-name groups:",
        len(overlap_duplicate_names),
    )
    print("production changes: none")
    print("existing-test changes: none")
    print("test deletion: none")
    print("repository-wide pytest: NOT run")
    print("output:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
