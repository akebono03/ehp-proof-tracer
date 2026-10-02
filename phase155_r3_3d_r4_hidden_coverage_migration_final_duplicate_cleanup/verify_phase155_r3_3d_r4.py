
from __future__ import annotations

import argparse
import ast
import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


def _read_csv(path: Path) -> list[dict[str, str]]:
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


def _load_json(path: Path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
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


def _top_level_test_counts(
    path: Path,
) -> Counter[str]:
    tree = ast.parse(
        path.read_text(
            encoding="utf-8-sig"
        )
    )
    return Counter(
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
    )


def _exists(
    repo_root: Path,
    test_id: str,
) -> bool:
    file_path, function_name = (
        _split_test_id(
            test_id
        )
    )
    path = repo_root / file_path
    if not path.exists():
        return False
    return (
        _top_level_test_counts(
            path
        ).get(
            function_name,
            0,
        )
        > 0
    )


def _source_duplicate_groups(
    repo_root: Path,
) -> list[
    dict[
        str,
        object,
    ]
]:
    result = []
    for path in sorted(
        (
            repo_root
            / "tests"
        ).glob(
            "test_*.py"
        )
    ):
        counts = _top_level_test_counts(
            path
        )
        for function_name, count in counts.items():
            if count > 1:
                result.append(
                    {
                        "file_path": (
                            path
                            .relative_to(
                                repo_root
                            )
                            .as_posix()
                        ),
                        "function_name": function_name,
                        "definition_count": count,
                    }
                )
    return result


def _run_pytest(
    repo_root: Path,
    test_ids: list[str],
) -> int:
    if not test_ids:
        return 0

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            *test_ids,
        ],
        cwd=repo_root,
    )
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--cleanup-output",
        type=Path,
        default=Path(
            "phase155_r3_3d_r4_cleanup_output"
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
        "--verified-pairs",
        type=Path,
        default=Path(
            "phase155_r3_2f_r1_audit_output/"
            "phase155_r3_2f_r1_verified_pairs.csv"
        ),
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
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_3d_r4_verification_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    def resolve(path: Path) -> Path:
        return (
            path
            if path.is_absolute()
            else repo_root
            / path
        )

    cleanup_dir = resolve(
        args.cleanup_output
    )
    manifest_path = (
        cleanup_dir
        / "phase155_r3_3d_r4_cleanup_manifest.json"
    )
    graph_path = resolve(
        args.graph_nodes
    )
    verified_path = resolve(
        args.verified_pairs
    )
    safety_path = resolve(
        args.candidate_safety
    )

    for path in (
        manifest_path,
        graph_path,
        verified_path,
        safety_path,
    ):
        if not path.exists():
            raise SystemExit(
                "required verification input not found: "
                + str(path)
            )

    manifest = _load_json(
        manifest_path
    )
    graph_rows = _read_csv(
        graph_path
    )
    verified_rows = _read_csv(
        verified_path
    )
    safety_rows = _read_csv(
        safety_path
    )

    older_ids = set(
        manifest[
            "older_test_ids"
        ]
    )
    newer_ids = set(
        manifest[
            "newer_test_ids"
        ]
    )
    renamed_ids = set(
        manifest[
            "renamed_test_ids"
        ]
    )

    original_safe_deletion_ids = {
        row["test_id"]
        for row in safety_rows
        if (
            row.get(
                "function_status"
            )
            == "safe_function_deletion"
        )
    }

    effective_deletion_ids = (
        original_safe_deletion_ids
        | older_ids
    )

    deletion_ids_still_present = sorted(
        test_id
        for test_id in effective_deletion_ids
        if _exists(
            repo_root,
            test_id,
        )
    )

    missing_newer_ids = sorted(
        test_id
        for test_id in newer_ids
        if not _exists(
            repo_root,
            test_id,
        )
    )

    missing_renamed_ids = sorted(
        test_id
        for test_id in renamed_ids
        if not _exists(
            repo_root,
            test_id,
        )
    )

    duplicate_groups = (
        _source_duplicate_groups(
            repo_root
        )
    )

    original_survivor_ids = {
        row["test_id"]
        for row in graph_rows
        if row.get(
            "deletion_candidate",
            "",
        ).strip().lower()
        not in (
            "true",
            "1",
            "yes",
        )
    }
    repaired_survivor_ids = (
        original_survivor_ids
        - older_ids
    )
    missing_repaired_survivors = sorted(
        test_id
        for test_id in repaired_survivor_ids
        if not _exists(
            repo_root,
            test_id,
        )
    )

    historical_ids = {
        test_id
        for row in verified_rows
        if row.get(
            "decision"
        )
        == "historical_keep"
        for test_id in (
            row["older_test_id"],
            row["newer_test_id"],
        )
    }
    missing_historical_ids = sorted(
        test_id
        for test_id in historical_ids
        if not _exists(
            repo_root,
            test_id,
        )
    )

    unresolved_removable_pairs = []
    for row in verified_rows:
        if (
            row.get(
                "decision"
            )
            != "removable_duplicate"
        ):
            continue
        older_exists = _exists(
            repo_root,
            row["older_test_id"],
        )
        newer_exists = _exists(
            repo_root,
            row["newer_test_id"],
        )
        if (
            older_exists
            and newer_exists
        ):
            unresolved_removable_pairs.append(
                row.get(
                    "candidate_id",
                    "",
                )
            )

    focused_ids = sorted(
        renamed_ids
        | newer_ids
        | {
            test_id
            for test_id in original_survivor_ids
            if (
                _split_test_id(
                    test_id
                )[0]
                in set(
                    manifest[
                        "changed_files"
                    ]
                )
                and test_id
                not in older_ids
            )
        }
    )

    print(
        "Focused pytest for changed duplicate/pair surfaces:"
    )
    pytest_exit = _run_pytest(
        repo_root,
        focused_ids,
    )

    completion = {
        "effective_deletion_ids_absent": (
            not deletion_ids_still_present
        ),
        "newer_pair_tests_present": (
            not missing_newer_ids
        ),
        "renamed_hidden_tests_present": (
            not missing_renamed_ids
        ),
        "source_level_duplicate_test_names_zero": (
            not duplicate_groups
        ),
        "repaired_graph_survivors_present": (
            not missing_repaired_survivors
        ),
        "historical_keep_ids_present": (
            not missing_historical_ids
        ),
        "unresolved_removable_pairs_zero": (
            not unresolved_removable_pairs
        ),
        "focused_pytest_exit_zero": (
            pytest_exit
            == 0
        ),
    }
    closure = all(
        completion.values()
    )

    output_dir = resolve(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = {
        "completion": completion,
        "closure_satisfied": closure,
        "effective_deletion_ids": len(
            effective_deletion_ids
        ),
        "effective_deletion_ids_still_present": (
            deletion_ids_still_present
        ),
        "missing_newer_ids": missing_newer_ids,
        "missing_renamed_ids": missing_renamed_ids,
        "source_level_duplicate_groups": (
            duplicate_groups
        ),
        "repaired_survivor_count": len(
            repaired_survivor_ids
        ),
        "missing_repaired_survivors": (
            missing_repaired_survivors
        ),
        "missing_historical_ids": (
            missing_historical_ids
        ),
        "unresolved_removable_pairs": (
            unresolved_removable_pairs
        ),
        "focused_test_ids": focused_ids,
        "focused_pytest_exit_code": pytest_exit,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_3d_r4_verification.json"
    ).write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    summary_lines = [
        "# Phase 155-R3-3D-r4 — repaired closure verification",
        "",
        f"- effective deletion IDs still present: {len(deletion_ids_still_present)}",
        f"- missing newer pair tests: {len(missing_newer_ids)}",
        f"- missing renamed hidden-coverage tests: {len(missing_renamed_ids)}",
        f"- source-level duplicate test names: {len(duplicate_groups)}",
        f"- missing repaired graph survivors: {len(missing_repaired_survivors)}",
        f"- missing historical_keep IDs: {len(missing_historical_ids)}",
        f"- unresolved removable pairs: {len(unresolved_removable_pairs)}",
        f"- focused pytest exit code: {pytest_exit}",
        "",
        "## Completion conditions",
        "",
    ]

    for key, value in completion.items():
        summary_lines.append(
            "- "
            + key
            + ": "
            + (
                "PASS"
                if value
                else "FAIL"
            )
        )

    summary_lines.extend(
        [
            "",
            "## Conclusion",
            "",
            (
                "**Phase 155 R3 closure satisfied: True**"
                if closure
                else "**Phase 155 R3 closure satisfied: False**"
            ),
            "",
            "Repository-wide pytest was NOT run.",
        ]
    )

    (
        output_dir
        / "phase155_r3_3d_r4_summary.md"
    ).write_text(
        "\n".join(
            summary_lines
        )
        + "\n",
        encoding="utf-8",
    )

    print("")
    print(
        "Phase 155-R3-3D-r4 repaired closure verification completed."
    )
    print(
        "effective deletion IDs still present:",
        len(
            deletion_ids_still_present
        ),
    )
    print(
        "missing newer pair tests:",
        len(
            missing_newer_ids
        ),
    )
    print(
        "missing renamed hidden-coverage tests:",
        len(
            missing_renamed_ids
        ),
    )
    print(
        "source-level duplicate test names:",
        len(
            duplicate_groups
        ),
    )
    print(
        "missing repaired graph survivors:",
        len(
            missing_repaired_survivors
        ),
    )
    print(
        "missing historical_keep IDs:",
        len(
            missing_historical_ids
        ),
    )
    print(
        "unresolved removable pairs:",
        len(
            unresolved_removable_pairs
        ),
    )
    print(
        "focused pytest exit code:",
        pytest_exit,
    )
    print(
        "R3 closure condition satisfied:",
        closure,
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
        if closure
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
