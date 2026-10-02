from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import pytest


def _read_nodeids(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(
            encoding="utf-8-sig"
        ).splitlines()
        if line.strip()
    ]


def _collect_only_batched(
    nodeids: list[str],
    batch_file_count: int,
) -> int:
    by_file: dict[str, list[str]] = defaultdict(list)

    for nodeid in nodeids:
        file_path = nodeid.split(
            "::",
            1,
        )[0]
        by_file[file_path].append(nodeid)

    files = sorted(by_file)

    batches = [
        files[index:index + batch_file_count]
        for index in range(
            0,
            len(files),
            batch_file_count,
        )
    ]

    for batch_number, batch_files in enumerate(
        batches,
        start=1,
    ):
        batch_nodeids = [
            nodeid
            for file_path in batch_files
            for nodeid in by_file[file_path]
        ]

        print(
            f"collect batch {batch_number}/{len(batches)} "
            f"({len(batch_files)} files, "
            f"{len(batch_nodeids)} source test IDs)",
            flush=True,
        )

        exit_code = pytest.main(
            [
                "--collect-only",
                "-q",
                "-p",
                "no:cacheprovider",
                *batch_nodeids,
            ]
        )

        if exit_code != 0:
            return int(exit_code)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=(
            Path(__file__)
            .with_name(
                "phase155_r4_4_canonical_nodeids.txt"
            )
        ),
    )
    parser.add_argument(
        "--collect-only",
        action="store_true",
    )
    parser.add_argument(
        "--batch-files",
        type=int,
        default=40,
    )
    args = parser.parse_args()

    nodeids = _read_nodeids(args.manifest)

    if not nodeids:
        raise SystemExit("canonical manifest is empty")

    print(
        "canonical source test IDs:",
        len(nodeids),
        flush=True,
    )

    if args.collect_only:
        return _collect_only_batched(
            nodeids,
            args.batch_files,
        )

    print(
        "WARNING: canonical regression executes a large test set.",
        flush=True,
    )

    return int(
        pytest.main(
            [
                "-q",
                "-p",
                "no:cacheprovider",
                *nodeids,
            ]
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
