
from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


CATEGORY_CANONICAL = "canonical_candidate"
CATEGORY_HISTORICAL = "historical_compatibility"
CATEGORY_AUDIT = "audit_only_candidate"
CATEGORY_HEAVY = "performance_heavy_integration_candidate"
CATEGORY_REVIEW = "review_required"


FOCUSED_SCRIPT_PATHS = (
    "phase153_closure_audit/run_phase153_closure_audit.ps1",
    "phase154_closure_audit/run_phase154_closure_audit.ps1",
)


AUDIT_NAME_TOKENS = (
    "audit",
    "inventory",
    "snapshot",
    "closure",
    "parity",
    "population",
    "coverage_matrix",
)


HEAVY_NAME_TOKENS = (
    "all_group",
    "all_groups",
    "full_depth",
    "exhaustive",
    "population",
    "cross_group",
    "determinism_audit",
    "final_regression",
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def _test_functions(path: Path) -> list[str]:
    tree = ast.parse(
        path.read_text(
            encoding="utf-8-sig"
        )
    )
    return [
        node.name
        for node in tree.body
        if (
            isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and node.name.startswith(
                "test_"
            )
        )
    ]


def _phase_number(path: str) -> int | None:
    match = re.search(
        r"test_phase(\d+)",
        Path(path).name,
    )
    if match is None:
        return None
    return int(
        match.group(1)
    )


def _extract_focused_test_files(
    repo_root: Path,
) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}

    pattern = re.compile(
        r'["\']?\.?[\\/](tests[\\/]+test_[^"`\']+?\.py)["\']?'
    )

    for relative in FOCUSED_SCRIPT_PATHS:
        path = repo_root / relative
        if not path.exists():
            result[relative] = []
            continue

        source = path.read_text(
            encoding="utf-8-sig"
        )
        files = []
        for match in pattern.finditer(source):
            normalized = (
                match.group(1)
                .replace("\\", "/")
            )
            if normalized not in files:
                files.append(
                    normalized
                )

        result[relative] = files

    return result


def _historical_ids(
    verified_pairs: list[
        dict[
            str,
            str,
        ]
    ],
) -> set[str]:
    return {
        test_id
        for row in verified_pairs
        if row.get(
            "decision"
        )
        == "historical_keep"
        for test_id in (
            row[
                "older_test_id"
            ],
            row[
                "newer_test_id"
            ],
        )
    }


def _file_signals(
    relative: str,
    focused_files: set[str],
) -> dict[str, object]:
    name = Path(
        relative
    ).name.lower()
    phase = _phase_number(
        relative
    )
    is_core_non_phase = (
        phase is None
    )
    is_focused = (
        relative in focused_files
    )
    audit_name = any(
        token in name
        for token in AUDIT_NAME_TOKENS
    )
    heavy_name = any(
        token in name
        for token in HEAVY_NAME_TOKENS
    )

    return {
        "phase": phase,
        "core_non_phase": (
            is_core_non_phase
        ),
        "focused_regression_file": (
            is_focused
        ),
        "audit_name_signal": (
            audit_name
        ),
        "heavy_name_signal": (
            heavy_name
        ),
    }


def _classify_test(
    relative: str,
    function_name: str,
    historical_ids: set[str],
    focused_files: set[str],
) -> tuple[str, str, int]:
    test_id = (
        relative
        + "::"
        + function_name
    )
    signals = _file_signals(
        relative,
        focused_files,
    )

    if test_id in historical_ids:
        return (
            CATEGORY_HISTORICAL,
            "R3 verified historical_keep",
            100,
        )

    if signals[
        "focused_regression_file"
    ]:
        return (
            CATEGORY_CANONICAL,
            "explicit Phase153/154 focused regression boundary",
            100,
        )

    if (
        signals[
            "core_non_phase"
        ]
        and not signals[
            "audit_name_signal"
        ]
        and not signals[
            "heavy_name_signal"
        ]
    ):
        return (
            CATEGORY_CANONICAL,
            "core non-phase test file",
            90,
        )

    if signals[
        "heavy_name_signal"
    ]:
        return (
            CATEGORY_HEAVY,
            "filename carries heavy/cross-group/full-depth signal",
            70,
        )

    if signals[
        "audit_name_signal"
    ]:
        return (
            CATEGORY_AUDIT,
            "filename carries audit/inventory/snapshot/closure signal",
            70,
        )

    phase = signals[
        "phase"
    ]
    if (
        phase is not None
        and phase >= 149
    ):
        return (
            CATEGORY_CANONICAL,
            "recent current-contract phase test; requires R4 validation",
            60,
        )

    return (
        CATEGORY_REVIEW,
        "no decisive canonical/historical/audit/heavy signal",
        40,
    )


def _collect_only(
    repo_root: Path,
    files: list[str],
) -> tuple[int, str]:
    if not files:
        return (
            0,
            "",
        )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "-p",
            "no:cacheprovider",
            *files,
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    return (
        completed.returncode,
        completed.stdout
        + completed.stderr,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--verified-pairs",
        type=Path,
        default=Path(
            "phase155_r3_2f_r1_audit_output/"
            "phase155_r3_2f_r1_verified_pairs.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r4_1_audit_output"
        ),
    )
    args = parser.parse_args()

    repo_root = (
        args.repo_root
        .resolve()
    )
    verified_path = (
        args.verified_pairs
        if args.verified_pairs.is_absolute()
        else repo_root
        / args.verified_pairs
    )

    if not verified_path.exists():
        raise SystemExit(
            "verified pair input not found: "
            + str(
                verified_path
            )
        )

    verified_pairs = _read_csv(
        verified_path
    )
    historical_ids = _historical_ids(
        verified_pairs
    )

    focused_sources = (
        _extract_focused_test_files(
            repo_root
        )
    )
    focused_files = {
        relative
        for values in (
            focused_sources.values()
        )
        for relative in values
        if (
            repo_root
            / relative
        ).exists()
    }

    rows = []
    file_categories = defaultdict(
        Counter
    )

    test_files = sorted(
        (
            repo_root
            / "tests"
        ).glob(
            "test_*.py"
        )
    )

    for path in test_files:
        relative = (
            path
            .relative_to(
                repo_root
            )
            .as_posix()
        )
        signals = _file_signals(
            relative,
            focused_files,
        )

        for function_name in _test_functions(
            path
        ):
            (
                category,
                reason,
                confidence,
            ) = _classify_test(
                relative,
                function_name,
                historical_ids,
                focused_files,
            )
            file_categories[
                relative
            ][
                category
            ] += 1
            rows.append(
                {
                    "test_id": (
                        relative
                        + "::"
                        + function_name
                    ),
                    "file_path": relative,
                    "function_name": (
                        function_name
                    ),
                    "phase": (
                        ""
                        if signals[
                            "phase"
                        ]
                        is None
                        else signals[
                            "phase"
                        ]
                    ),
                    "category": category,
                    "confidence": confidence,
                    "reason": reason,
                    "focused_regression_file": (
                        signals[
                            "focused_regression_file"
                        ]
                    ),
                    "core_non_phase": (
                        signals[
                            "core_non_phase"
                        ]
                    ),
                    "audit_name_signal": (
                        signals[
                            "audit_name_signal"
                        ]
                    ),
                    "heavy_name_signal": (
                        signals[
                            "heavy_name_signal"
                        ]
                    ),
                }
            )

    category_counts = Counter(
        row[
            "category"
        ]
        for row in rows
    )

    canonical_files = sorted(
        {
            row[
                "file_path"
            ]
            for row in rows
            if row[
                "category"
            ]
            == CATEGORY_CANONICAL
        }
    )
    historical_files = sorted(
        {
            row[
                "file_path"
            ]
            for row in rows
            if row[
                "category"
            ]
            == CATEGORY_HISTORICAL
        }
    )
    audit_files = sorted(
        {
            row[
                "file_path"
            ]
            for row in rows
            if row[
                "category"
            ]
            == CATEGORY_AUDIT
        }
    )
    heavy_files = sorted(
        {
            row[
                "file_path"
            ]
            for row in rows
            if row[
                "category"
            ]
            == CATEGORY_HEAVY
        }
    )
    review_files = sorted(
        {
            row[
                "file_path"
            ]
            for row in rows
            if row[
                "category"
            ]
            == CATEGORY_REVIEW
        }
    )

    collect_exit, collect_output = (
        _collect_only(
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
        / "phase155_r4_1_test_classification.csv"
    )
    with csv_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        fieldnames = list(
            rows[0].keys()
        ) if rows else [
            "test_id",
            "file_path",
            "function_name",
            "phase",
            "category",
            "confidence",
            "reason",
            "focused_regression_file",
            "core_non_phase",
            "audit_name_signal",
            "heavy_name_signal",
        ]
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(
            rows
        )

    file_summary = []
    for relative in sorted(
        file_categories
    ):
        counts = file_categories[
            relative
        ]
        file_summary.append(
            {
                "file_path": relative,
                "test_count": sum(
                    counts.values()
                ),
                **{
                    category: counts[
                        category
                    ]
                    for category in (
                        CATEGORY_CANONICAL,
                        CATEGORY_HISTORICAL,
                        CATEGORY_AUDIT,
                        CATEGORY_HEAVY,
                        CATEGORY_REVIEW,
                    )
                },
            }
        )

    (
        output_dir
        / "phase155_r4_1_file_classification.json"
    ).write_text(
        json.dumps(
            file_summary,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r4_1_focused_sources.json"
    ).write_text(
        json.dumps(
            focused_sources,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r4_1_canonical_collect_only.txt"
    ).write_text(
        collect_output,
        encoding="utf-8",
    )

    metadata = {
        "test_files": len(
            test_files
        ),
        "source_test_functions": len(
            rows
        ),
        "category_counts": dict(
            category_counts
        ),
        "canonical_candidate_files": len(
            canonical_files
        ),
        "historical_files": len(
            historical_files
        ),
        "audit_only_candidate_files": len(
            audit_files
        ),
        "heavy_candidate_files": len(
            heavy_files
        ),
        "review_required_files": len(
            review_files
        ),
        "focused_regression_files_found": len(
            focused_files
        ),
        "canonical_collect_only_exit_code": (
            collect_exit
        ),
        "production_changes": False,
        "existing_test_changes": False,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r4_1_metadata.json"
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
        "# Phase 155-R4-1 — canonical regression set evidence audit",
        "",
        "## Inventory",
        "",
        f"- test files: {len(test_files)}",
        f"- source test functions: {len(rows)}",
        "",
        "## Function classification",
        "",
    ]

    for category in (
        CATEGORY_CANONICAL,
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
            "## File-level boundary",
            "",
            f"- canonical candidate files: {len(canonical_files)}",
            f"- historical files: {len(historical_files)}",
            f"- audit-only candidate files: {len(audit_files)}",
            f"- heavy candidate files: {len(heavy_files)}",
            f"- review-required files: {len(review_files)}",
            f"- explicit Phase153/154 focused files found: {len(focused_files)}",
            "",
            "## Collection",
            "",
            f"- canonical candidate collect-only exit code: {collect_exit}",
            "",
            "## Boundary",
            "",
            "R4-1 is evidence classification only.",
            "No marker, file move, deletion, or production change is performed.",
            "The canonical set is not final until review-required and heavy/audit overlaps are validated in later R4 steps.",
            "Repository-wide pytest is NOT run.",
        ]
    )

    (
        output_dir
        / "phase155_r4_1_summary.md"
    ).write_text(
        "\n".join(
            lines
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R4-1 canonical-set evidence audit completed."
    )
    print(
        "test files:",
        len(
            test_files
        ),
    )
    print(
        "source test functions:",
        len(
            rows
        ),
    )
    for category in (
        CATEGORY_CANONICAL,
        CATEGORY_HISTORICAL,
        CATEGORY_AUDIT,
        CATEGORY_HEAVY,
        CATEGORY_REVIEW,
    ):
        print(
            category + ":",
            category_counts[
                category
            ],
        )
    print(
        "canonical candidate files:",
        len(
            canonical_files
        ),
    )
    print(
        "historical files:",
        len(
            historical_files
        ),
    )
    print(
        "audit-only candidate files:",
        len(
            audit_files
        ),
    )
    print(
        "heavy candidate files:",
        len(
            heavy_files
        ),
    )
    print(
        "review-required files:",
        len(
            review_files
        ),
    )
    print(
        "focused regression files found:",
        len(
            focused_files
        ),
    )
    print(
        "canonical collect-only exit code:",
        collect_exit,
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
        if collect_exit
        == 0
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
