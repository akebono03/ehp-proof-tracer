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
) -> list[str]:
    source = path.read_text(
        encoding="utf-8-sig",
    )
    tree = ast.parse(
        source
    )

    return [
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
    ]


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


def _importer_files(
    file_rows: list[
        dict[
            str,
            str,
        ]
    ],
) -> list[str]:
    result = set()

    for row in file_rows:
        for field in (
            "external_symbol_imports",
            "whole_module_importers",
        ):
            for item in filter(
                None,
                row.get(
                    field,
                    "",
                ).split(
                    "\x1f"
                ),
            ):
                file_path = item.split(
                    ":",
                    1,
                )[
                    0
                ]

                if file_path.endswith(
                    ".py"
                ):
                    result.add(
                        file_path
                    )

    return sorted(
        result
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
            "phase155_r3_3c_r1_removal_output"
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
    remaining_files = [
        relative
        for relative in affected_files
        if relative
        not in whole_files
    ]

    errors = []

    for relative in sorted(
        whole_files
    ):
        if (
            repo_root
            / relative
        ).exists():
            errors.append(
                "whole-file target still exists: "
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
            errors.append(
                "remaining affected file is missing: "
                + relative
            )
            continue

        names = (
            _top_level_test_names(
                path
            )
        )

        if function_name in names:
            errors.append(
                "deleted test name still exists: "
                + row[
                    "test_id"
                ]
            )

    if errors:
        print(
            "Static deletion verification failed:"
        )

        for error in errors:
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

    print(
        "Focused verification A: graph survivors"
    )
    survivor_exit = _run_pytest(
        repo_root,
        survivor_ids,
    )

    if survivor_exit != 0:
        return survivor_exit

    importer_files = (
        _importer_files(
            file_rows
        )
    )
    importer_tests = [
        relative
        for relative in importer_files
        if (
            relative.startswith(
                "tests/"
            )
            and Path(
                relative
            ).name.startswith(
                "test_"
            )
        )
    ]
    non_test_importers = [
        relative
        for relative in importer_files
        if relative
        not in importer_tests
    ]

    compile_targets = sorted(
        set(
            remaining_files
            + non_test_importers
        )
    )

    for relative in compile_targets:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "py_compile",
                str(
                    repo_root
                    / relative
                ),
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )

        if completed.returncode != 0:
            print(
                "Compile verification failed:",
                relative,
            )
            print(
                completed.stderr
                or completed.stdout
            )
            return 3

    focused_files = sorted(
        set(
            remaining_files
            + importer_tests
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
        "phase": "155-R3-3C-r1",
        "removed_test_ids": len(
            safe_candidates
        ),
        "whole_files_deleted": len(
            whole_files
        ),
        "remaining_affected_test_files": len(
            remaining_files
        ),
        "survivor_test_ids_verified": len(
            survivor_ids
        ),
        "importer_test_files_verified": len(
            importer_tests
        ),
        "non_test_importers_compiled": len(
            non_test_importers
        ),
        "survivor_pytest_exit_code": (
            survivor_exit
        ),
        "affected_files_pytest_exit_code": (
            affected_exit
        ),
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_3c_r1_verification.json"
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
        "Phase 155-R3-3C-r1 verification completed."
    )
    print(
        "removed test IDs:",
        len(
            safe_candidates
        ),
    )
    print(
        "whole files deleted:",
        len(
            whole_files
        ),
    )
    print(
        "remaining affected test files:",
        len(
            remaining_files
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
            importer_tests
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
