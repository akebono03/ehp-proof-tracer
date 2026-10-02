from __future__ import annotations

import argparse
from pathlib import Path


TARGETS = (
    "README.md",
    "docs/design.md",
    "docs/development_log.md",
    "docs/roadmap.md",
    "docs/proof_records.md",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output_dir = (
        repo_root
        / "phase155_closure_output"
        / "full_documents"
    )

    checks = {}

    for relative_path in TARGETS:
        repo_path = (
            repo_root
            / relative_path
        )
        copy_path = (
            output_dir
            / relative_path
        )

        checks[
            relative_path
        ] = (
            copy_path.exists()
            and repo_path.read_bytes()
            == copy_path.read_bytes()
        )

    roadmap = (
        repo_root
        / "docs/roadmap.md"
    ).read_text(
        encoding="utf-8-sig"
    )

    readme = (
        repo_root
        / "README.md"
    ).read_text(
        encoding="utf-8-sig"
    )

    checks[
        "roadmap_phase155_complete"
    ] = (
        "Phase 155"
        in roadmap
        and "COMPLETE"
        in roadmap
        and "Phase 156"
        in roadmap
    )

    checks[
        "readme_english_phase155"
    ] = (
        "Phase 155 test-suite consolidation"
        in readme
        and "new tests should be lightweight by default"
        in readme
    )

    for name, value in checks.items():
        print(
            name + ":",
            "PASS"
            if value
            else "FAIL",
        )

    validated = all(
        checks.values()
    )

    print(
        "Phase 155 closure documents validated:",
        validated,
    )

    return (
        0
        if validated
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
