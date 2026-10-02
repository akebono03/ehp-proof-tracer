from __future__ import annotations

import argparse
import ast
import csv
import json
import subprocess
import sys
from pathlib import Path


SAFE_FUNCTION = "safe_function_deletion"
SAFE_WHOLE_FILE = "safe_whole_file_deletion"


def _read_csv(
    path: Path,
) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(
            csv.DictReader(
                handle
            )
        )


def _split_test_id(
    test_id: str,
) -> tuple[str, str]:
    file_path, function_name = test_id.split(
        "::",
        1,
    )
    return (
        file_path.replace(
            "\\",
            "/",
        ),
        function_name,
    )


def _top_level_test_names(
    path: Path,
) -> set[str]:
    source = path.read_text(
        encoding="utf-8-sig",
    )
    tree = ast.parse(
        source
    )

    return {
        node.name
        for node in tree.body
        if (
            isinstance(
                node,
                ast.FunctionDef,
            )
            and node.name.startswith(
                "test_"
            )
        )
    }


def _run_pytest(
    repo_root: Path,
    targets: list[str],
) -> int:
    if not targets:
        return 0

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            *targets,
            "-q",
            "-p",
            "no:cacheprovider",
        ],
        cwd=repo_root,
    )

    return completed.returncode


def _python_files_from_import_fields(
    file_rows: list[
        dict[
            str,
            str,
        ]
    ],
) -> list[str]:
    result = set()

    for row in file_rows:
        for field_name in (
            "external_symbol_imports",
            "whole_module_importers",
        ):
            raw = row.get(
                field_name,
                "",
            )

            for item in filter(
                None,
                raw.split(
                    "\x1f"
                ),
            ):
                file_path = (
                    item.split(
                        ":",
                        1,
                    )[
                        0
                    ]
                )

                if file_path.endswith(
                    ".py"
                ):
                    result.add(
                        file_path
                    )

    return sorted(
        result
    )


def _survivor_test_ids(
    node_rows: list[
        dict[
            str,
            str,
        ]
    ],
) -> list[str]:
    return sorted(
        {
            row[
                "test_id"
            ]
            for row in node_rows
            if row.get(
                "deletion_candidate",
                "",
            ).lower()
            not in (
                "true",
                "1",
                "yes",
            )
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--candidate-safety",
        type=Path,
        default=Path(
            "phase155_r3_3b_audit_output/"
            "phase155_r3_3b_candidate_safety.csv"
        ),
    )
    parser.add_argument(
        "--file-safety",
        type=Path,
        default=Path(
            "phase155_r3_3b_audit_output/"
            "phase155_r3_3b_file_safety.csv"
        ),
    )
    parser.add_argument(
        "--graph-nodes",
        type=Path,
        default=Path(
            "phase155_r3_3a_audit_output/"
            "phase155_r3_3a_nodes.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_3c_removal_output"
        ),
    )

    args = parser.parse_args()
    repo_root = (
        args.repo_root.resolve()
    )

    def resolve(
        path: Path,
    ) -> Path:
        return (
            path
            if path.is_absolute()
            else repo_root
            / path
        )

    candidate_rows = _read_csv(
        resolve(
            args.candidate_safety
        )
    )
    file_rows = _read_csv(
        resolve(
            args.file_safety
        )
    )
    node_rows = _read_csv(
        resolve(
            args.graph_nodes
        )
    )

    safe_candidates = [
        row
        for row in candidate_rows
        if row.get(
            "function_status"
        )
        == SAFE_FUNCTION
    ]
    whole_files = {
        row[
            "file_path"
        ]
        for row in file_rows
        if row.get(
            "file_status"
        )
        == SAFE_WHOLE_FILE
    }

    affected_files = sorted(
        {
            row[
                "file_path"
            ]
            for row in safe_candidates
        }
    )

    remaining_affected_files = [
        file_path
        for file_path in affected_files
        if file_path
        not in whole_files
    ]

    static_errors = []

    for relative in sorted(
        whole_files
    ):
        if (
            repo_root
            / relative
        ).exists():
            static_errors.append(
                "whole-file deletion target still exists: "
                + relative
            )

    for row in safe_candidates:
        relative, function_name = (
            _split_test_id(
                row[
                    "test_id"
                ]
            )
        )

        if relative in whole_files:
            continue

        path = (
            repo_root
            / relative
        )

        if not path.exists():
            static_errors.append(
                "function-only file missing: "
                + relative
            )
            continue

        try:
            names = (
                _top_level_test_names(
                    path
                )
            )
        except (
            OSError,
            SyntaxError,
            UnicodeError,
        ) as exc:
            static_errors.append(
                relative
                + ": "
                + type(
                    exc
                ).__name__
                + ": "
                + str(
                    exc
                )
            )
            continue

        if function_name in names:
            static_errors.append(
                "deleted test function still exists: "
                + row[
                    "test_id"
                ]
            )

    if static_errors:
        print(
            "Static deletion verification failed:"
        )

        for error in static_errors:
            print(
                "  -",
                error,
            )

        return 2

    survivor_ids = (
        _survivor_test_ids(
            node_rows
        )
    )

    missing_survivors = [
        test_id
        for test_id in survivor_ids
        if not (
            repo_root
            / _split_test_id(
                test_id
            )[
                0
            ]
        ).exists()
    ]

    if missing_survivors:
        print(
            "Survivor source files missing:"
        )

        for test_id in (
            missing_survivors
        ):
            print(
                "  -",
                test_id,
            )

        return 3

    importer_files = (
        _python_files_from_import_fields(
            file_rows
        )
    )
    importer_test_files = [
        file_path
        for file_path in importer_files
        if (
            file_path.startswith(
                "tests/"
            )
            and Path(
                file_path
            ).name.startswith(
                "test_"
            )
        )
    ]

    non_test_importers = [
        file_path
        for file_path in importer_files
        if file_path
        not in importer_test_files
    ]

    compile_failures = []

    for relative in sorted(
        set(
            remaining_affected_files
            + non_test_importers
        )
    ):
        path = (
            repo_root
            / relative
        )

        if not path.exists():
            compile_failures.append(
                relative
                + ": missing"
            )
            continue

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "py_compile",
                str(
                    path
                ),
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )

        if completed.returncode != 0:
            compile_failures.append(
                relative
                + ": "
                + (
                    completed.stderr
                    or completed.stdout
                ).strip()
            )

    if compile_failures:
        print(
            "Compile/importer verification failed:"
        )

        for failure in (
            compile_failures
        ):
            print(
                "  -",
                failure,
            )

        return 4

    print(
        "Focused verification A: survivor tests"
    )
    survivor_exit = _run_pytest(
        repo_root,
        survivor_ids,
    )

    if survivor_exit != 0:
        return survivor_exit

    focused_files = sorted(
        set(
            remaining_affected_files
            + importer_test_files
        )
    )

    print(
        "Focused verification B: remaining affected/importer test files"
    )
    affected_exit = _run_pytest(
        repo_root,
        focused_files,
    )

    if affected_exit != 0:
        return affected_exit

    output_dir = resolve(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = {
        "phase": "155-R3-3C",
        "deleted_test_functions": len(
            safe_candidates
        ),
        "deleted_whole_files": len(
            whole_files
        ),
        "remaining_affected_test_files": len(
            remaining_affected_files
        ),
        "survivor_test_ids": len(
            survivor_ids
        ),
        "importer_python_files": len(
            importer_files
        ),
        "importer_test_files": len(
            importer_test_files
        ),
        "non_test_importers_compiled": len(
            non_test_importers
        ),
        "static_deleted_test_verification": (
            "passed"
        ),
        "survivor_pytest_exit_code": (
            survivor_exit
        ),
        "affected_files_pytest_exit_code": (
            affected_exit
        ),
        "repository_wide_pytest_executed": (
            False
        ),
    }

    (
        output_dir
        / "phase155_r3_3c_verification.json"
    ).write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R3-3C verification completed."
    )
    print(
        "deleted test functions:",
        len(
            safe_candidates
        ),
    )
    print(
        "deleted whole files:",
        len(
            whole_files
        ),
    )
    print(
        "remaining affected test files:",
        len(
            remaining_affected_files
        ),
    )
    print(
        "survivor tests verified:",
        len(
            survivor_ids
        ),
    )
    print(
        "importer test files verified:",
        len(
            importer_test_files
        ),
    )
    print(
        "repository-wide pytest: NOT run"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
