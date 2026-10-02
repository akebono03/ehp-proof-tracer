
from __future__ import annotations

import argparse
import ast
import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


CATEGORY_CANONICAL = "canonical_candidate"
CATEGORY_PUBLIC = "canonical_public_surface_candidate"
CATEGORY_INTERNAL = "canonical_internal_contract_candidate"
CATEGORY_LINEAGE_SUPPORT = "lineage_support_candidate"
CATEGORY_HISTORICAL = "historical_compatibility"
CATEGORY_AUDIT = "audit_only_candidate"
CATEGORY_HEAVY = "performance_heavy_integration_candidate"
CATEGORY_REVIEW = "review_required"


EXCLUDED_ROOT_PREFIXES = (
    "apply_",
    "audit_",
    "show_",
    "test_",
    "probe_",
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def _production_modules(repo_root: Path) -> set[str]:
    modules = set()

    for path in sorted(repo_root.glob("*.py")):
        stem = path.stem

        if stem.startswith(EXCLUDED_ROOT_PREFIXES):
            continue

        if stem in {
            "conftest",
            "setup",
        }:
            continue

        modules.add(stem)

    return modules


def _module_analysis(
    path: Path,
    production_modules: set[str],
) -> dict[str, object]:
    source = path.read_text(
        encoding="utf-8-sig"
    )
    tree = ast.parse(source)

    imported_production_names: dict[str, str] = {}
    imported_test_helpers: set[str] = set()

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]

                if root in production_modules:
                    local_name = (
                        alias.asname
                        if alias.asname
                        else root
                    )
                    imported_production_names[
                        local_name
                    ] = root

                if root == "tests":
                    local_name = (
                        alias.asname
                        if alias.asname
                        else root
                    )
                    imported_test_helpers.add(local_name)

        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue

            root = node.module.split(".", 1)[0]

            if root in production_modules:
                for alias in node.names:
                    local_name = (
                        alias.asname
                        if alias.asname
                        else alias.name
                    )
                    imported_production_names[
                        local_name
                    ] = root

            if root == "tests":
                for alias in node.names:
                    local_name = (
                        alias.asname
                        if alias.asname
                        else alias.name
                    )
                    imported_test_helpers.add(local_name)

    functions = {
        node.name: node
        for node in tree.body
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
    }

    used_names: dict[str, set[str]] = {}
    local_calls: dict[str, set[str]] = {}

    for name, node in functions.items():
        used_names[name] = {
            child.id
            for child in ast.walk(node)
            if isinstance(child, ast.Name)
        }

        local_calls[name] = {
            child.func.id
            for child in ast.walk(node)
            if (
                isinstance(child, ast.Call)
                and isinstance(
                    child.func,
                    ast.Name,
                )
                and child.func.id in functions
            )
        }

    return {
        "imported_production_names": imported_production_names,
        "imported_test_helpers": imported_test_helpers,
        "functions": functions,
        "used_names": used_names,
        "local_calls": local_calls,
    }


def _reachable_functions(
    start: str,
    local_calls: dict[str, set[str]],
) -> set[str]:
    seen = set()
    stack = [start]

    while stack:
        name = stack.pop()

        if name in seen:
            continue

        seen.add(name)

        stack.extend(
            sorted(
                local_calls.get(
                    name,
                    set(),
                )
                - seen
            )
        )

    return seen


def _ownership_for_test(
    analysis: dict[str, object],
    test_name: str,
) -> tuple[set[str], set[str]]:
    reachable = _reachable_functions(
        test_name,
        analysis["local_calls"],
    )

    names = set()
    for function_name in reachable:
        names.update(
            analysis["used_names"].get(
                function_name,
                set(),
            )
        )

    production_modules = {
        module
        for local_name, module in (
            analysis[
                "imported_production_names"
            ].items()
        )
        if local_name in names
    }

    test_helpers = {
        local_name
        for local_name in (
            analysis[
                "imported_test_helpers"
            ]
        )
        if local_name in names
    }

    return (
        production_modules,
        test_helpers,
    )


def _reclassify(
    original_category: str,
    production_modules: set[str],
    test_helpers: set[str],
) -> tuple[str, str]:
    if original_category in (
        CATEGORY_CANONICAL,
        CATEGORY_PUBLIC,
        CATEGORY_HISTORICAL,
        CATEGORY_AUDIT,
        CATEGORY_HEAVY,
    ):
        return (
            original_category,
            "R4-2 lane preserved",
        )

    if (
        original_category
        == CATEGORY_REVIEW
        and production_modules
    ):
        return (
            CATEGORY_INTERNAL,
            "test reaches current production module: "
            + ", ".join(
                sorted(
                    production_modules
                )
            ),
        )

    if (
        original_category
        == CATEGORY_REVIEW
        and test_helpers
    ):
        return (
            CATEGORY_LINEAGE_SUPPORT,
            "test reaches tests.* helper without direct current production ownership",
        )

    return (
        original_category,
        "no current production ownership or tests.* lineage evidence",
    )


def _collect_only_batches(
    repo_root: Path,
    files: list[str],
    batch_size: int = 40,
) -> tuple[int, str]:
    outputs = []

    for index in range(
        0,
        len(files),
        batch_size,
    ):
        batch = files[
            index:
            index
            + batch_size
        ]

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "--collect-only",
                "-q",
                "-p",
                "no:cacheprovider",
                *batch,
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )

        outputs.append(
            "=== batch "
            + str(
                index
                // batch_size
                + 1
            )
            + " ===\n"
            + completed.stdout
            + completed.stderr
        )

        if completed.returncode != 0:
            return (
                completed.returncode,
                "\n".join(outputs),
            )

    return (
        0,
        "\n".join(outputs),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--r4-2-classification",
        type=Path,
        default=Path(
            "phase155_r4_2_audit_output/"
            "phase155_r4_2_proposed_classification.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r4_3_audit_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    classification_path = (
        args.r4_2_classification
        if args.r4_2_classification.is_absolute()
        else repo_root
        / args.r4_2_classification
    )

    if not classification_path.exists():
        raise SystemExit(
            "R4-2 classification not found: "
            + str(classification_path)
        )

    production_modules = _production_modules(
        repo_root
    )

    rows = _read_csv(
        classification_path
    )

    analyses: dict[str, dict[str, object]] = {}
    result_rows = []
    module_owners = defaultdict(list)
    category_counts = Counter()

    original_review_count = sum(
        1
        for row in rows
        if row[
            "proposed_category"
        ]
        == CATEGORY_REVIEW
    )

    internal_promotions = 0
    lineage_support_count = 0

    for row in rows:
        file_path = row["file_path"]
        function_name = row[
            "function_name"
        ]
        original_category = row[
            "proposed_category"
        ]

        if file_path not in analyses:
            analyses[file_path] = (
                _module_analysis(
                    repo_root / file_path,
                    production_modules,
                )
            )

        (
            ownership_modules,
            test_helpers,
        ) = _ownership_for_test(
            analyses[file_path],
            function_name,
        )

        (
            proposed_category,
            reason,
        ) = _reclassify(
            original_category,
            ownership_modules,
            test_helpers,
        )

        if (
            proposed_category
            == CATEGORY_INTERNAL
        ):
            internal_promotions += 1

        if (
            proposed_category
            == CATEGORY_LINEAGE_SUPPORT
        ):
            lineage_support_count += 1

        for module in sorted(
            ownership_modules
        ):
            module_owners[module].append(
                row["test_id"]
            )

        category_counts[
            proposed_category
        ] += 1

        result_rows.append(
            {
                **row,
                "current_production_modules_used": ";".join(
                    sorted(
                        ownership_modules
                    )
                ),
                "tests_helper_names_used": ";".join(
                    sorted(
                        test_helpers
                    )
                ),
                "r4_3_category": (
                    proposed_category
                ),
                "r4_3_reason": reason,
            }
        )

    canonical_categories = {
        CATEGORY_CANONICAL,
        CATEGORY_PUBLIC,
        CATEGORY_INTERNAL,
    }

    canonical_ids = [
        row["test_id"]
        for row in result_rows
        if row[
            "r4_3_category"
        ]
        in canonical_categories
    ]

    canonical_files = sorted(
        {
            row["file_path"]
            for row in result_rows
            if row[
                "r4_3_category"
            ]
            in canonical_categories
        }
    )

    collect_exit, collect_output = (
        _collect_only_batches(
            repo_root,
            canonical_files,
        )
    )

    remaining_review = category_counts[
        CATEGORY_REVIEW
    ]

    owned_modules = {
        module
        for module, test_ids in (
            module_owners.items()
        )
        if test_ids
    }

    unowned_production_modules = sorted(
        production_modules
        - owned_modules
    )

    module_matrix = [
        {
            "production_module": module,
            "owning_test_count": len(
                module_owners.get(
                    module,
                    [],
                )
            ),
            "owning_test_ids": (
                module_owners.get(
                    module,
                    [],
                )
            ),
        }
        for module in sorted(
            production_modules
        )
    ]

    completion = {
        "canonical_collect_only_exit_zero": (
            collect_exit == 0
        ),
        "review_population_reduced": (
            remaining_review
            < original_review_count
        ),
        "historical_lane_preserved": (
            category_counts[
                CATEGORY_HISTORICAL
            ]
            == sum(
                1
                for row in rows
                if row[
                    "proposed_category"
                ]
                == CATEGORY_HISTORICAL
            )
        ),
        "audit_lane_preserved": (
            category_counts[
                CATEGORY_AUDIT
            ]
            == sum(
                1
                for row in rows
                if row[
                    "proposed_category"
                ]
                == CATEGORY_AUDIT
            )
        ),
        "heavy_lane_preserved": (
            category_counts[
                CATEGORY_HEAVY
            ]
            == sum(
                1
                for row in rows
                if row[
                    "proposed_category"
                ]
                == CATEGORY_HEAVY
            )
        ),
    }

    consolidation_validated = all(
        completion.values()
    )

    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root
        / args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_path = (
        output_dir
        / "phase155_r4_3_consolidated_classification.csv"
    )

    with csv_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        fieldnames = list(
            result_rows[0].keys()
        )
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(
            result_rows
        )

    (
        output_dir
        / "phase155_r4_3_production_ownership_matrix.json"
    ).write_text(
        json.dumps(
            module_matrix,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r4_3_canonical_test_ids.txt"
    ).write_text(
        "\n".join(
            canonical_ids
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r4_3_canonical_files.txt"
    ).write_text(
        "\n".join(
            canonical_files
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r4_3_collect_only.txt"
    ).write_text(
        collect_output,
        encoding="utf-8",
    )

    metadata = {
        "source_test_functions": len(rows),
        "root_production_modules": len(
            production_modules
        ),
        "production_modules_with_test_ownership": len(
            owned_modules
        ),
        "production_modules_without_test_ownership": len(
            unowned_production_modules
        ),
        "unowned_production_modules": (
            unowned_production_modules
        ),
        "original_review_required": (
            original_review_count
        ),
        "internal_contract_promotions": (
            internal_promotions
        ),
        "lineage_support_candidates": (
            lineage_support_count
        ),
        "remaining_review_required": (
            remaining_review
        ),
        "validated_canonical_tests": len(
            canonical_ids
        ),
        "validated_canonical_files": len(
            canonical_files
        ),
        "category_counts": dict(
            category_counts
        ),
        "collect_only_exit_code": (
            collect_exit
        ),
        "completion": completion,
        "consolidation_validated": (
            consolidation_validated
        ),
        "production_changes": False,
        "existing_test_changes": False,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r4_3_metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Phase 155-R4-3 — review-required lineage / current-contract consolidation",
        "",
        "## Current production ownership",
        "",
        f"- root production modules: {len(production_modules)}",
        f"- modules with direct/reachable test ownership: {len(owned_modules)}",
        f"- modules without detected ownership: {len(unowned_production_modules)}",
        "",
        "## Review consolidation",
        "",
        f"- original review_required: {original_review_count}",
        f"- internal-contract promotions: {internal_promotions}",
        f"- lineage-support candidates: {lineage_support_count}",
        f"- remaining review_required: {remaining_review}",
        "",
        "## Canonical lane",
        "",
        f"- validated canonical tests: {len(canonical_ids)}",
        f"- validated canonical files: {len(canonical_files)}",
        f"- collect-only exit code: {collect_exit}",
        "",
        "## Proposed categories",
        "",
    ]

    for category in (
        CATEGORY_CANONICAL,
        CATEGORY_PUBLIC,
        CATEGORY_INTERNAL,
        CATEGORY_LINEAGE_SUPPORT,
        CATEGORY_HISTORICAL,
        CATEGORY_AUDIT,
        CATEGORY_HEAVY,
        CATEGORY_REVIEW,
    ):
        lines.append(
            f"- `{category}`: {category_counts[category]}"
        )

    lines.extend(
        [
            "",
            "## Validation",
            "",
        ]
    )

    for key, value in completion.items():
        lines.append(
            "- "
            + key
            + ": "
            + (
                "PASS"
                if value
                else "FAIL"
            )
        )

    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            (
                "**R4-3 current-contract consolidation validated: True**"
                if consolidation_validated
                else "**R4-3 current-contract consolidation validated: False**"
            ),
            "",
            "No production code or existing test was changed.",
            "No test was executed beyond collect-only.",
            "Repository-wide pytest was NOT run.",
            "",
            "Remaining `review_required` and `lineage_support_candidate` tests are not classified as removable.",
            "They are the input for the next R4 boundary decision.",
        ]
    )

    (
        output_dir
        / "phase155_r4_3_summary.md"
    ).write_text(
        "\n".join(lines)
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R4-3 current-contract consolidation completed."
    )
    print(
        "root production modules:",
        len(production_modules),
    )
    print(
        "production modules with test ownership:",
        len(owned_modules),
    )
    print(
        "production modules without test ownership:",
        len(unowned_production_modules),
    )
    print(
        "original review_required:",
        original_review_count,
    )
    print(
        "internal-contract promotions:",
        internal_promotions,
    )
    print(
        "lineage-support candidates:",
        lineage_support_count,
    )
    print(
        "remaining review_required:",
        remaining_review,
    )
    print(
        "validated canonical tests:",
        len(canonical_ids),
    )
    print(
        "validated canonical files:",
        len(canonical_files),
    )
    print(
        "canonical collect-only exit code:",
        collect_exit,
    )
    print(
        "R4-3 current-contract consolidation validated:",
        consolidation_validated,
    )
    print("production changes: none")
    print("existing-test changes: none")
    print("repository-wide pytest: NOT run")
    print("output:", output_dir)

    return (
        0
        if consolidation_validated
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
