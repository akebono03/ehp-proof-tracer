
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
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _split_test_id(test_id: str) -> tuple[str, str]:
    file_path, function_name = test_id.split("::", 1)
    return file_path.replace("\\", "/"), function_name


def _top_level_test_counts(path: Path) -> Counter[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    return Counter(
        node.name
        for node in tree.body
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
    )


def _exists(repo_root: Path, test_id: str) -> bool:
    file_path, function_name = _split_test_id(test_id)
    path = repo_root / file_path
    if not path.exists():
        return False
    return _top_level_test_counts(path).get(function_name, 0) > 0


def _duplicate_groups(repo_root: Path):
    result = []
    for path in sorted((repo_root / "tests").glob("test_*.py")):
        counts = _top_level_test_counts(path)
        for name, count in counts.items():
            if count > 1:
                result.append(
                    {
                        "file_path": path.relative_to(repo_root).as_posix(),
                        "function_name": name,
                        "count": count,
                    }
                )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--repair-output",
        type=Path,
        default=Path("phase155_r3_3d_r4_r1_repair_output"),
    )
    parser.add_argument(
        "--r4-cleanup-output",
        type=Path,
        default=Path("phase155_r3_3d_r4_cleanup_output"),
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
            "phase155_r3_3d_r4_r1_verification_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    def resolve(path: Path) -> Path:
        return path if path.is_absolute() else repo_root / path

    repair_manifest = _load_json(
        resolve(args.repair_output)
        / "phase155_r3_3d_r4_r1_repair_manifest.json"
    )
    r4_manifest = _load_json(
        resolve(args.r4_cleanup_output)
        / "phase155_r3_3d_r4_cleanup_manifest.json"
    )
    verified = _read_csv(resolve(args.verified_pairs))
    safety = _read_csv(resolve(args.candidate_safety))

    historical_ids = {
        test_id
        for row in verified
        if row.get("decision") == "historical_keep"
        for test_id in (
            row["older_test_id"],
            row["newer_test_id"],
        )
    }

    missing_historical = sorted(
        test_id
        for test_id in historical_ids
        if not _exists(repo_root, test_id)
    )

    stale_hidden_ids = set(
        repair_manifest["removed_stale_hidden_tests"]
    )
    stale_hidden_still_present = sorted(
        test_id
        for test_id in stale_hidden_ids
        if _exists(repo_root, test_id)
    )

    original_safe_deletion_ids = {
        row["test_id"]
        for row in safety
        if row.get("function_status") == "safe_function_deletion"
    }
    safe_deletion_still_present = sorted(
        test_id
        for test_id in original_safe_deletion_ids
        if _exists(repo_root, test_id)
    )

    unresolved_removable = []
    historical_overrides = []
    for row in verified:
        if row.get("decision") != "removable_duplicate":
            continue

        older_exists = _exists(repo_root, row["older_test_id"])
        newer_exists = _exists(repo_root, row["newer_test_id"])
        if not (older_exists and newer_exists):
            continue

        if (
            row["older_test_id"] in historical_ids
            or row["newer_test_id"] in historical_ids
        ):
            historical_overrides.append(
                row.get("candidate_id", "")
            )
        else:
            unresolved_removable.append(
                row.get("candidate_id", "")
            )

    duplicates = _duplicate_groups(repo_root)

    canonical_set_rule_ids = [
        "tests/test_set_rules.py::test_image_membership_statement",
        "tests/test_set_rules.py::test_image_membership_statement_distinguishes_image",
        "tests/test_set_rules.py::test_image_membership_statement_uses_existing_image_subgroup",
        "tests/test_set_rules.py::test_kernel_membership_statement",
        "tests/test_set_rules.py::test_kernel_membership_statement_distinguishes_kernel",
        "tests/test_set_rules.py::test_kernel_membership_statement_uses_existing_kernel_subgroup",
        "tests/test_set_rules.py::test_mapped_zero_implies_kernel_membership",
        "tests/test_set_rules.py::test_mapped_zero_implies_kernel_membership_uses_explicit_group_map",
    ]

    restored_historical_ids = sorted(
        repair_manifest["restored_historical_keep_tests"]
    )

    focused_ids = canonical_set_rule_ids + restored_historical_ids

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            *focused_ids,
        ],
        cwd=repo_root,
    )

    completion = {
        "stale_hidden_tests_absent": not stale_hidden_still_present,
        "historical_keep_ids_present": not missing_historical,
        "original_safe_deletion_ids_absent": not safe_deletion_still_present,
        "source_level_duplicate_names_zero": not duplicates,
        "unresolved_nonhistorical_removable_pairs_zero": (
            not unresolved_removable
        ),
        "focused_pytest_exit_zero": completed.returncode == 0,
    }
    closure = all(completion.values())

    output_dir = resolve(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "completion": completion,
        "closure_satisfied": closure,
        "stale_hidden_tests_still_present": stale_hidden_still_present,
        "missing_historical_keep_ids": missing_historical,
        "safe_deletion_ids_still_present": safe_deletion_still_present,
        "source_level_duplicate_groups": duplicates,
        "unresolved_nonhistorical_removable_pairs": unresolved_removable,
        "historical_precedence_overrides": historical_overrides,
        "focused_test_ids": focused_ids,
        "focused_pytest_exit_code": completed.returncode,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_3d_r4_r1_verification.json"
    ).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Phase 155-R3-3D-r4-r1 — repaired closure verification",
        "",
        f"- stale hidden tests still present: {len(stale_hidden_still_present)}",
        f"- missing historical_keep IDs: {len(missing_historical)}",
        f"- original safe deletion IDs still present: {len(safe_deletion_still_present)}",
        f"- source-level duplicate test names: {len(duplicates)}",
        f"- unresolved nonhistorical removable pairs: {len(unresolved_removable)}",
        f"- historical precedence overrides: {len(historical_overrides)}",
        f"- focused pytest exit code: {completed.returncode}",
        "",
        "## Completion conditions",
        "",
    ]

    for key, value in completion.items():
        lines.append(
            "- "
            + key
            + ": "
            + ("PASS" if value else "FAIL")
        )

    lines.extend(
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
        / "phase155_r3_3d_r4_r1_summary.md"
    ).write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("")
    print("Phase 155-R3-3D-r4-r1 verification completed.")
    print(
        "stale hidden tests still present:",
        len(stale_hidden_still_present),
    )
    print(
        "missing historical_keep IDs:",
        len(missing_historical),
    )
    print(
        "original safe deletion IDs still present:",
        len(safe_deletion_still_present),
    )
    print(
        "source-level duplicate test names:",
        len(duplicates),
    )
    print(
        "unresolved nonhistorical removable pairs:",
        len(unresolved_removable),
    )
    print(
        "historical precedence overrides:",
        len(historical_overrides),
    )
    print(
        "focused pytest exit code:",
        completed.returncode,
    )
    print(
        "R3 closure condition satisfied:",
        closure,
    )
    print("repository-wide pytest: NOT run")
    print("output:", output_dir)

    return 0 if closure else 2


if __name__ == "__main__":
    raise SystemExit(main())
