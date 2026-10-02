
from __future__ import annotations

import argparse
import ast
import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


PUBLIC_MODULES = (
    "main",
    "web_app",
    "web_group_query",
    "web_group_proof",
    "web_operation_query",
    "web_operation_query_proof",
    "web_generator_proof",
    "web_generator_exploration",
    "web_generator_proof_scope",
    "web_generator_applicability",
    "web_generator_execution",
)


CATEGORY_CANONICAL = "canonical_candidate"
CATEGORY_PUBLIC_PROMOTION = "canonical_public_surface_candidate"
CATEGORY_HISTORICAL = "historical_compatibility"
CATEGORY_AUDIT = "audit_only_candidate"
CATEGORY_HEAVY = "performance_heavy_integration_candidate"
CATEGORY_REVIEW = "review_required"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def _module_analysis(path: Path) -> dict[str, object]:
    source = path.read_text(
        encoding="utf-8-sig"
    )
    tree = ast.parse(source)

    imported_public_names: dict[str, str] = {}

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in PUBLIC_MODULES:
                    local_name = (
                        alias.asname
                        if alias.asname
                        else root
                    )
                    imported_public_names[
                        local_name
                    ] = root

        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            root = node.module.split(".", 1)[0]
            if root not in PUBLIC_MODULES:
                continue
            for alias in node.names:
                local_name = (
                    alias.asname
                    if alias.asname
                    else alias.name
                )
                imported_public_names[
                    local_name
                ] = root

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
        names = {
            child.id
            for child in ast.walk(node)
            if isinstance(
                child,
                ast.Name,
            )
        }
        calls = {
            child.func.id
            for child in ast.walk(node)
            if (
                isinstance(
                    child,
                    ast.Call,
                )
                and isinstance(
                    child.func,
                    ast.Name,
                )
                and child.func.id
                in functions
            )
        }
        used_names[
            name
        ] = names
        local_calls[
            name
        ] = calls

    return {
        "imported_public_names": imported_public_names,
        "functions": functions,
        "used_names": used_names,
        "local_calls": local_calls,
    }


def _reachable_functions(
    start: str,
    local_calls: dict[str, set[str]],
) -> set[str]:
    seen = set()
    stack = [
        start
    ]

    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(
            name
        )
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


def _public_modules_used_by_test(
    analysis: dict[str, object],
    test_name: str,
) -> set[str]:
    imported_public_names = analysis[
        "imported_public_names"
    ]
    used_names = analysis[
        "used_names"
    ]
    local_calls = analysis[
        "local_calls"
    ]

    reachable = _reachable_functions(
        test_name,
        local_calls,
    )

    names = set()
    for function_name in reachable:
        names.update(
            used_names.get(
                function_name,
                set(),
            )
        )

    return {
        module
        for local_name, module in (
            imported_public_names.items()
        )
        if local_name in names
    }


def _promoted_category(
    original_category: str,
    public_modules: set[str],
) -> tuple[str, str]:
    if original_category in (
        CATEGORY_HISTORICAL,
        CATEGORY_AUDIT,
        CATEGORY_HEAVY,
    ):
        return (
            original_category,
            "R4-1 lane has precedence over public-surface evidence",
        )

    if original_category == CATEGORY_CANONICAL:
        return (
            CATEGORY_CANONICAL,
            "already canonical_candidate in R4-1",
        )

    if (
        original_category
        == CATEGORY_REVIEW
        and public_modules
    ):
        return (
            CATEGORY_PUBLIC_PROMOTION,
            "test function reaches current public module: "
            + ", ".join(
                sorted(
                    public_modules
                )
            ),
        )

    return (
        original_category,
        "no new direct public-surface evidence",
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
                "\n".join(
                    outputs
                ),
            )

    return (
        0,
        "\n".join(
            outputs
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--r4-1-classification",
        type=Path,
        default=Path(
            "phase155_r4_1_audit_output/"
            "phase155_r4_1_test_classification.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r4_2_audit_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    classification_path = (
        args.r4_1_classification
        if args.r4_1_classification.is_absolute()
        else repo_root
        / args.r4_1_classification
    )

    if not classification_path.exists():
        raise SystemExit(
            "R4-1 classification not found: "
            + str(
                classification_path
            )
        )

    rows = _read_csv(
        classification_path
    )

    analyses: dict[str, dict[str, object]] = {}
    result_rows = []
    surface_tests = defaultdict(
        list
    )
    category_counts = Counter()
    original_review_count = 0
    promoted_count = 0

    for row in rows:
        file_path = row[
            "file_path"
        ]
        function_name = row[
            "function_name"
        ]
        original_category = row[
            "category"
        ]

        if original_category == CATEGORY_REVIEW:
            original_review_count += 1

        if file_path not in analyses:
            analyses[
                file_path
            ] = _module_analysis(
                repo_root
                / file_path
            )

        public_modules = (
            _public_modules_used_by_test(
                analyses[
                    file_path
                ],
                function_name,
            )
        )

        (
            proposed_category,
            proposal_reason,
        ) = _promoted_category(
            original_category,
            public_modules,
        )

        if (
            proposed_category
            == CATEGORY_PUBLIC_PROMOTION
        ):
            promoted_count += 1

        for module in sorted(
            public_modules
        ):
            surface_tests[
                module
            ].append(
                file_path
                + "::"
                + function_name
            )

        category_counts[
            proposed_category
        ] += 1

        result_rows.append(
            {
                **row,
                "public_modules_used": ";".join(
                    sorted(
                        public_modules
                    )
                ),
                "proposed_category": (
                    proposed_category
                ),
                "proposal_reason": (
                    proposal_reason
                ),
            }
        )

    validated_categories = {
        CATEGORY_CANONICAL,
        CATEGORY_PUBLIC_PROMOTION,
    }

    canonical_test_ids = [
        row[
            "test_id"
        ]
        for row in result_rows
        if row[
            "proposed_category"
        ]
        in validated_categories
    ]

    canonical_files = sorted(
        {
            row[
                "file_path"
            ]
            for row in result_rows
            if row[
                "proposed_category"
            ]
            in validated_categories
        }
    )

    surface_matrix = []
    uncovered_surfaces = []

    for module in PUBLIC_MODULES:
        all_direct_tests = surface_tests.get(
            module,
            [],
        )

        canonical_direct_tests = [
            row[
                "test_id"
            ]
            for row in result_rows
            if (
                module
                in set(
                    filter(
                        None,
                        row[
                            "public_modules_used"
                        ].split(
                            ";"
                        ),
                    )
                )
                and row[
                    "proposed_category"
                ]
                in validated_categories
            )
        ]

        if not canonical_direct_tests:
            uncovered_surfaces.append(
                module
            )

        surface_matrix.append(
            {
                "public_module": module,
                "all_direct_test_count": len(
                    all_direct_tests
                ),
                "canonical_direct_test_count": len(
                    canonical_direct_tests
                ),
                "canonical_direct_tests": (
                    canonical_direct_tests
                ),
            }
        )

    collect_exit, collect_output = (
        _collect_only_batches(
            repo_root,
            canonical_files,
        )
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
        / "phase155_r4_2_proposed_classification.csv"
    )

    with csv_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        fieldnames = list(
            result_rows[
                0
            ].keys()
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
        / "phase155_r4_2_public_surface_matrix.json"
    ).write_text(
        json.dumps(
            surface_matrix,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r4_2_canonical_test_ids.txt"
    ).write_text(
        "\n".join(
            canonical_test_ids
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r4_2_canonical_files.txt"
    ).write_text(
        "\n".join(
            canonical_files
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r4_2_collect_only.txt"
    ).write_text(
        collect_output,
        encoding="utf-8",
    )

    remaining_review = category_counts[
        CATEGORY_REVIEW
    ]

    completion = {
        "all_public_surfaces_have_canonical_direct_tests": (
            not uncovered_surfaces
        ),
        "canonical_collect_only_exit_zero": (
            collect_exit
            == 0
        ),
        "review_population_not_increased": (
            remaining_review
            <= original_review_count
        ),
        "historical_lane_preserved": (
            category_counts[
                CATEGORY_HISTORICAL
            ]
            == sum(
                1
                for row in rows
                if row[
                    "category"
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
                    "category"
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
                    "category"
                ]
                == CATEGORY_HEAVY
            )
        ),
    }

    boundary_validated = all(
        completion.values()
    )

    metadata = {
        "source_test_functions": len(
            rows
        ),
        "original_review_required": (
            original_review_count
        ),
        "public_surface_promotions": (
            promoted_count
        ),
        "remaining_review_required": (
            remaining_review
        ),
        "validated_canonical_tests": len(
            canonical_test_ids
        ),
        "validated_canonical_files": len(
            canonical_files
        ),
        "category_counts": dict(
            category_counts
        ),
        "public_surface_count": len(
            PUBLIC_MODULES
        ),
        "uncovered_public_surfaces": (
            uncovered_surfaces
        ),
        "collect_only_exit_code": (
            collect_exit
        ),
        "completion": completion,
        "boundary_validated": (
            boundary_validated
        ),
        "production_changes": False,
        "existing_test_changes": False,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r4_2_metadata.json"
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
        "# Phase 155-R4-2 — canonical boundary validation",
        "",
        "## Public-surface promotion",
        "",
        f"- original review_required: {original_review_count}",
        f"- promoted by direct/reachable public-surface use: {promoted_count}",
        f"- remaining review_required: {remaining_review}",
        f"- validated canonical tests: {len(canonical_test_ids)}",
        f"- validated canonical files: {len(canonical_files)}",
        "",
        "## Public surface coverage",
        "",
        f"- public modules: {len(PUBLIC_MODULES)}",
        f"- uncovered public modules: {len(uncovered_surfaces)}",
    ]

    for module in uncovered_surfaces:
        lines.append(
            f"  - `{module}`"
        )

    lines.extend(
        [
            "",
            "## Proposed category counts",
            "",
        ]
    )

    for category in (
        CATEGORY_CANONICAL,
        CATEGORY_PUBLIC_PROMOTION,
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
                "**R4-2 canonical public-surface boundary validated: True**"
                if boundary_validated
                else "**R4-2 canonical public-surface boundary validated: False**"
            ),
            "",
            "No production code or existing test was changed.",
            "No test was executed beyond collect-only.",
            "Repository-wide pytest was NOT run.",
            "",
            "R4-2 does not claim that remaining review_required tests are removable.",
            "It only establishes that the proposed canonical lane directly covers every current public module.",
        ]
    )

    (
        output_dir
        / "phase155_r4_2_summary.md"
    ).write_text(
        "\n".join(
            lines
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R4-2 canonical boundary validation completed."
    )
    print(
        "original review_required:",
        original_review_count,
    )
    print(
        "public-surface promotions:",
        promoted_count,
    )
    print(
        "remaining review_required:",
        remaining_review,
    )
    print(
        "validated canonical tests:",
        len(
            canonical_test_ids
        ),
    )
    print(
        "validated canonical files:",
        len(
            canonical_files
        ),
    )
    print(
        "public surfaces:",
        len(
            PUBLIC_MODULES
        ),
    )
    print(
        "uncovered public surfaces:",
        len(
            uncovered_surfaces
        ),
    )
    print(
        "canonical collect-only exit code:",
        collect_exit,
    )
    print(
        "R4-2 canonical public-surface boundary validated:",
        boundary_validated,
    )
    print(
        "production changes: none"
    )
    print(
        "existing-test changes: none"
    )
    print(
        "repository-wide pytest: NOT run"
    )
    print(
        "output:",
        output_dir,
    )

    return (
        0
        if boundary_validated
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
