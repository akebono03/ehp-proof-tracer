from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r4_4_audit_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root / args.output_dir
    )

    metadata_path = (
        output_dir
        / "phase155_r4_4_metadata.json"
    )
    runner_path = (
        output_dir
        / "run_phase155_canonical_regression.py"
    )
    manifest_path = (
        output_dir
        / "phase155_r4_4_canonical_nodeids.txt"
    )

    for path in (
        metadata_path,
        runner_path,
        manifest_path,
    ):
        if not path.exists():
            raise SystemExit(
                "required R4-4 output missing: "
                + str(path)
            )

    metadata = json.loads(
        metadata_path.read_text(
            encoding="utf-8"
        )
    )

    print(
        "Canonical collect-only validation may be moderately heavy."
    )
    print(
        "Progress is printed batch by batch."
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(runner_path),
            "--collect-only",
            "--batch-files",
            "40",
        ],
        cwd=repo_root,
    )

    completion = {
        "canonical_manifest_nonempty": (
            metadata[
                "canonical_source_test_ids"
            ]
            > 0
        ),
        "residual_lane_explicit": (
            metadata[
                "residual_validation_lane"
            ]
            >= 0
        ),
        "canonical_collect_only_exit_zero": (
            completed.returncode
            == 0
        ),
        "canonical_command_defined": bool(
            metadata[
                "canonical_command"
            ]
        ),
        "repository_wide_pytest_not_run": (
            metadata[
                "repository_wide_pytest_executed"
            ]
            is False
        ),
        "canonical_regression_not_run": (
            metadata[
                "canonical_regression_executed"
            ]
            is False
        ),
    }

    validated = all(
        completion.values()
    )

    result = {
        "completion": completion,
        "validated": validated,
        "collect_only_exit_code": (
            completed.returncode
        ),
        "canonical_source_test_ids": (
            metadata[
                "canonical_source_test_ids"
            ]
        ),
        "canonical_files": (
            metadata[
                "canonical_files"
            ]
        ),
        "residual_validation_lane": (
            metadata[
                "residual_validation_lane"
            ]
        ),
        "module_boundary": (
            metadata[
                "module_boundary"
            ]
        ),
    }

    (
        output_dir
        / "phase155_r4_4_verification.json"
    ).write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Phase 155-R4-4 — verification",
        "",
        f"- canonical source test IDs: {result['canonical_source_test_ids']}",
        f"- canonical files: {result['canonical_files']}",
        f"- residual validation lane: {result['residual_validation_lane']}",
        f"- collect-only exit code: {completed.returncode}",
        "",
        "## Completion conditions",
        "",
    ]

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
                "**Phase 155 R4 canonical boundary validated: True**"
                if validated
                else "**Phase 155 R4 canonical boundary validated: False**"
            ),
            "",
            "Canonical regression itself was NOT run.",
            "Repository-wide pytest was NOT run.",
        ]
    )

    (
        output_dir
        / "phase155_r4_4_verification_summary.md"
    ).write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("")
    print(
        "Phase 155-R4-4 verification completed."
    )
    print(
        "canonical source test IDs:",
        result[
            "canonical_source_test_ids"
        ],
    )
    print(
        "canonical files:",
        result[
            "canonical_files"
        ],
    )
    print(
        "residual validation lane:",
        result[
            "residual_validation_lane"
        ],
    )
    print(
        "canonical collect-only exit code:",
        completed.returncode,
    )
    print(
        "R4 canonical boundary validated:",
        validated,
    )
    print(
        "canonical regression: NOT run"
    )
    print(
        "repository-wide pytest: NOT run"
    )

    return 0 if validated else 2


if __name__ == "__main__":
    raise SystemExit(main())
