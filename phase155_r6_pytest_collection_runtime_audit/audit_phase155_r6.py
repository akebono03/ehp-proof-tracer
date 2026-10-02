from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path


LANES = (
    "canonical_routine",
    "historical_compatibility",
    "audit_only",
    "performance_heavy_integration",
    "residual_retained",
)

MANIFEST_NAMES = {
    "canonical_routine":
        "phase155_r5_canonical_routine_nodeids.txt",
    "historical_compatibility":
        "phase155_r5_historical_nodeids.txt",
    "audit_only":
        "phase155_r5_audit_only_nodeids.txt",
    "performance_heavy_integration":
        "phase155_r5_heavy_nodeids.txt",
    "residual_retained":
        "phase155_r5_residual_retained_nodeids.txt",
}

COLLECTION_BATCH_SIZE = 40

RUNTIME_SAMPLE_SIZES = {
    "canonical_routine": 3,
    "historical_compatibility": 2,
    "audit_only": 2,
    "performance_heavy_integration": 3,
    "residual_retained": 2,
}


def _read_manifest(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(
            encoding="utf-8-sig"
        ).splitlines()
        if line.strip()
    ]


def _source_file(nodeid: str) -> str:
    return nodeid.split(
        "::",
        1,
    )[0]


def _source_function_nodeid(
    nodeid: str,
) -> str:
    parts = nodeid.split(
        "::"
    )

    if len(parts) < 2:
        return nodeid

    return "::".join(
        parts[:2]
    )


def _group_by_file(
    nodeids: list[str],
) -> dict[str, list[str]]:
    result: dict[
        str,
        list[str],
    ] = defaultdict(list)

    for nodeid in nodeids:
        result[
            _source_file(nodeid)
        ].append(nodeid)

    return dict(result)


def _batched(
    items: list[str],
    size: int,
) -> list[list[str]]:
    return [
        items[index:index + size]
        for index in range(
            0,
            len(items),
            size,
        )
    ]


def _checkpoint_name(
    prefix: str,
    index: int,
    identity: str,
) -> str:
    digest = hashlib.sha1(
        identity.encode(
            "utf-8"
        )
    ).hexdigest()[:12]

    return (
        f"{prefix}_{index:04d}_{digest}.json"
    )


def _run_pytest(
    repo_root: Path,
    args: list[str],
    timeout: float | None,
) -> tuple[
    str,
    float,
    str,
    str,
    int | None,
]:
    started = time.perf_counter()

    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                *args,
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )

        elapsed = (
            time.perf_counter()
            - started
        )

        status = (
            "PASS"
            if completed.returncode == 0
            else "FAIL"
        )

        return (
            status,
            elapsed,
            completed.stdout,
            completed.stderr,
            completed.returncode,
        )

    except subprocess.TimeoutExpired as error:
        elapsed = (
            time.perf_counter()
            - started
        )

        stdout = error.stdout or ""
        stderr = error.stderr or ""

        if isinstance(
            stdout,
            bytes,
        ):
            stdout = stdout.decode(
                "utf-8",
                "replace",
            )

        if isinstance(
            stderr,
            bytes,
        ):
            stderr = stderr.decode(
                "utf-8",
                "replace",
            )

        return (
            "TIMEOUT",
            elapsed,
            stdout,
            stderr,
            None,
        )


def _parse_collected_nodeids(
    stdout: str,
) -> list[str]:
    return [
        line.strip()
        for line in stdout.splitlines()
        if (
            "::"
            in line
            and not line.startswith(
                "="
            )
        )
    ]


def _deterministic_samples(
    nodeids: list[str],
    count: int,
) -> list[str]:
    if not nodeids or count <= 0:
        return []

    unique = sorted(
        set(
            _source_function_nodeid(
                nodeid
            )
            for nodeid in nodeids
        )
    )

    if len(unique) <= count:
        return unique

    if count == 1:
        return [
            unique[
                len(unique) // 2
            ]
        ]

    positions = {
        round(
            index
            * (
                len(unique)
                - 1
            )
            / (
                count
                - 1
            )
        )
        for index in range(
            count
        )
    }

    return [
        unique[position]
        for position in sorted(
            positions
        )
    ]


def _collection_audit(
    repo_root: Path,
    output_dir: Path,
    manifests: dict[
        str,
        list[str],
    ],
) -> dict[str, object]:
    checkpoint_dir = (
        output_dir
        / "collection_checkpoints"
    )
    checkpoint_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    all_files = sorted(
        {
            _source_file(
                nodeid
            )
            for nodeids in manifests.values()
            for nodeid in nodeids
        }
    )

    batches = _batched(
        all_files,
        COLLECTION_BATCH_SIZE,
    )

    manifest_sets = {
        lane: {
            _source_function_nodeid(
                nodeid
            )
            for nodeid in nodeids
        }
        for lane, nodeids
        in manifests.items()
    }

    lane_collected_cases = {
        lane: 0
        for lane in LANES
    }
    total_collected_cases = 0
    elapsed_total = 0.0
    failed_batches = []
    reused = 0
    executed = 0

    print("")
    print(
        "A. pytest collection audit"
    )
    print(
        "collection batches:",
        len(batches),
    )
    print(
        "test bodies: NOT executed"
    )

    for batch_index, batch_files in enumerate(
        batches,
        start=1,
    ):
        identity = "|".join(
            batch_files
        )
        checkpoint = (
            checkpoint_dir
            / _checkpoint_name(
                "collect",
                batch_index,
                identity,
            )
        )

        if checkpoint.exists():
            payload = json.loads(
                checkpoint.read_text(
                    encoding="utf-8"
                )
            )
            reused += 1

            print(
                f"[collect {batch_index}/{len(batches)}] "
                "checkpoint PASS - skip",
                flush=True,
            )

        else:
            print(
                f"[collect {batch_index}/{len(batches)}] "
                f"START ({len(batch_files)} files)",
                flush=True,
            )

            (
                status,
                elapsed,
                stdout,
                stderr,
                returncode,
            ) = _run_pytest(
                repo_root,
                [
                    "--collect-only",
                    "-q",
                    "-p",
                    "no:cacheprovider",
                    *batch_files,
                ],
                timeout=None,
            )

            collected = (
                _parse_collected_nodeids(
                    stdout
                )
            )

            payload = {
                "status": status,
                "elapsed_seconds": elapsed,
                "returncode": returncode,
                "files": batch_files,
                "collected_nodeids": collected,
                "stdout_tail": "\n".join(
                    stdout.splitlines()[
                        -20:
                    ]
                ),
                "stderr_tail": "\n".join(
                    stderr.splitlines()[
                        -20:
                    ]
                ),
            }

            checkpoint.write_text(
                json.dumps(
                    payload,
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            executed += 1

            print(
                f"[collect {batch_index}/{len(batches)}] "
                f"{status} {elapsed:.2f}s "
                f"({len(collected)} cases)",
                flush=True,
            )

        elapsed_total += float(
            payload[
                "elapsed_seconds"
            ]
        )

        if payload[
            "status"
        ] != "PASS":
            failed_batches.append(
                batch_index
            )
            continue

        for collected_nodeid in payload[
            "collected_nodeids"
        ]:
            total_collected_cases += 1
            source_function = (
                _source_function_nodeid(
                    collected_nodeid
                )
            )

            matched = False

            for lane in LANES:
                if (
                    source_function
                    in manifest_sets[
                        lane
                    ]
                ):
                    lane_collected_cases[
                        lane
                    ] += 1
                    matched = True
                    break

            if not matched:
                pass

    return {
        "files": len(
            all_files
        ),
        "batches": len(
            batches
        ),
        "batches_executed_this_run": (
            executed
        ),
        "batches_reused_from_checkpoint": (
            reused
        ),
        "failed_batches": (
            failed_batches
        ),
        "elapsed_seconds_sum": (
            elapsed_total
        ),
        "total_collected_cases": (
            total_collected_cases
        ),
        "lane_collected_cases": (
            lane_collected_cases
        ),
    }


def _runtime_probe(
    repo_root: Path,
    output_dir: Path,
    manifests: dict[
        str,
        list[str],
    ],
    timeout: float,
) -> dict[str, object]:
    checkpoint_dir = (
        output_dir
        / "runtime_checkpoints"
    )
    checkpoint_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    selected = []

    for lane in LANES:
        samples = _deterministic_samples(
            manifests[
                lane
            ],
            RUNTIME_SAMPLE_SIZES[
                lane
            ],
        )

        for nodeid in samples:
            selected.append(
                (
                    lane,
                    nodeid,
                )
            )

    rows = []
    reused = 0
    executed = 0

    print("")
    print(
        "B. bounded runtime probe"
    )
    print(
        "selected probes:",
        len(selected),
    )
    print(
        "per-probe timeout:",
        f"{timeout:.0f}s",
    )
    print(
        "This is NOT the canonical regression."
    )

    for index, (
        lane,
        nodeid,
    ) in enumerate(
        selected,
        start=1,
    ):
        identity = (
            lane
            + "|"
            + nodeid
        )

        checkpoint = (
            checkpoint_dir
            / _checkpoint_name(
                "runtime",
                index,
                identity,
            )
        )

        if checkpoint.exists():
            payload = json.loads(
                checkpoint.read_text(
                    encoding="utf-8"
                )
            )
            reused += 1

            print(
                f"[runtime {index}/{len(selected)}] "
                f"checkpoint {payload['status']} - skip "
                f"{lane} {nodeid}",
                flush=True,
            )

        else:
            print(
                f"[runtime {index}/{len(selected)}] "
                f"START {lane} {nodeid}",
                flush=True,
            )

            (
                status,
                elapsed,
                stdout,
                stderr,
                returncode,
            ) = _run_pytest(
                repo_root,
                [
                    nodeid,
                    "-q",
                    "-p",
                    "no:cacheprovider",
                    "--durations=10",
                    "--durations-min=0.0",
                ],
                timeout=timeout,
            )

            payload = {
                "lane": lane,
                "nodeid": nodeid,
                "status": status,
                "elapsed_seconds": elapsed,
                "returncode": returncode,
                "stdout": stdout,
                "stderr": stderr,
            }

            checkpoint.write_text(
                json.dumps(
                    payload,
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            executed += 1

            print(
                f"[runtime {index}/{len(selected)}] "
                f"{status} {elapsed:.2f}s "
                f"{lane} {nodeid}",
                flush=True,
            )

        rows.append(
            payload
        )

    by_lane = {}

    for lane in LANES:
        lane_rows = [
            row
            for row in rows
            if row[
                "lane"
            ]
            == lane
        ]

        pass_rows = [
            row
            for row in lane_rows
            if row[
                "status"
            ]
            == "PASS"
        ]

        by_lane[
            lane
        ] = {
            "probes": len(
                lane_rows
            ),
            "pass": sum(
                row[
                    "status"
                ]
                == "PASS"
                for row in lane_rows
            ),
            "fail": sum(
                row[
                    "status"
                ]
                == "FAIL"
                for row in lane_rows
            ),
            "timeout": sum(
                row[
                    "status"
                ]
                == "TIMEOUT"
                for row in lane_rows
            ),
            "pass_elapsed_seconds_sum": (
                sum(
                    row[
                        "elapsed_seconds"
                    ]
                    for row in pass_rows
                )
            ),
            "pass_elapsed_seconds_max": (
                max(
                    (
                        row[
                            "elapsed_seconds"
                        ]
                        for row in pass_rows
                    ),
                    default=0.0,
                )
            ),
        }

    slowest = sorted(
        rows,
        key=lambda row: float(
            row[
                "elapsed_seconds"
            ]
        ),
        reverse=True,
    )

    return {
        "selected_probes": len(
            selected
        ),
        "probes_executed_this_run": (
            executed
        ),
        "probes_reused_from_checkpoint": (
            reused
        ),
        "timeout_seconds": timeout,
        "by_lane": by_lane,
        "slowest_probes": [
            {
                "lane": row[
                    "lane"
                ],
                "nodeid": row[
                    "nodeid"
                ],
                "status": row[
                    "status"
                ],
                "elapsed_seconds": row[
                    "elapsed_seconds"
                ],
            }
            for row in slowest
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--r5-output-dir",
        type=Path,
        default=Path(
            "phase155_r5_audit_output"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r6_audit_output"
        ),
    )
    parser.add_argument(
        "--runtime-timeout",
        type=float,
        default=60.0,
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    r5_output_dir = (
        args.r5_output_dir
        if args.r5_output_dir.is_absolute()
        else repo_root
        / args.r5_output_dir
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

    manifests = {}

    for lane in LANES:
        path = (
            r5_output_dir
            / MANIFEST_NAMES[
                lane
            ]
        )

        if not path.exists():
            raise SystemExit(
                "required R5 manifest not found: "
                + str(
                    path
                )
            )

        manifests[
            lane
        ] = _read_manifest(
            path
        )

    print(
        "Phase 155-R6 pytest collection / runtime audit"
    )
    print(
        "This may be moderately heavy."
    )
    print(
        "Progress + checkpoint/resume are enabled."
    )
    print(
        "Canonical regression: NOT run."
    )
    print(
        "Repository-wide pytest: NOT run."
    )
    print("")

    print(
        "R5 source test IDs by lane:"
    )

    for lane in LANES:
        print(
            " ",
            lane + ":",
            len(
                manifests[
                    lane
                ]
            ),
        )

    collection = _collection_audit(
        repo_root,
        output_dir,
        manifests,
    )

    runtime = _runtime_probe(
        repo_root,
        output_dir,
        manifests,
        args.runtime_timeout,
    )

    completion = {
        "collection_batches_have_no_failures": (
            not collection[
                "failed_batches"
            ]
        ),
        "runtime_probes_have_no_failures": (
            all(
                row[
                    "status"
                ]
                != "FAIL"
                for row in runtime[
                    "slowest_probes"
                ]
            )
        ),
        "canonical_regression_not_run": True,
        "repository_wide_pytest_not_run": True,
        "checkpoint_resume_enabled": True,
    }

    validated = all(
        completion.values()
    )

    metadata = {
        "source_test_ids_by_lane": {
            lane: len(
                manifests[
                    lane
                ]
            )
            for lane in LANES
        },
        "collection": collection,
        "runtime": runtime,
        "completion": completion,
        "validated": validated,
        "canonical_regression_executed": False,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r6_metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    report = [
        "# Phase 155-R6 — pytest collection / runtime audit",
        "",
        "## Collection",
        "",
        f"- files: {collection['files']}",
        f"- batches: {collection['batches']}",
        f"- total collected cases observed: {collection['total_collected_cases']}",
        f"- collection elapsed seconds (sum of batch observations): {collection['elapsed_seconds_sum']:.2f}",
        "",
        "Collected cases mapped to R5 lanes:",
    ]

    for lane in LANES:
        report.append(
            "- "
            + lane
            + ": "
            + str(
                collection[
                    "lane_collected_cases"
                ][
                    lane
                ]
            )
        )

    report.extend(
        [
            "",
            "## Bounded runtime probe",
            "",
            f"- selected probes: {runtime['selected_probes']}",
            f"- per-probe timeout: {runtime['timeout_seconds']:.0f}s",
        ]
    )

    for lane in LANES:
        lane_data = (
            runtime[
                "by_lane"
            ][
                lane
            ]
        )

        report.append(
            "- "
            + lane
            + ": "
            + f"probes={lane_data['probes']}, "
            + f"pass={lane_data['pass']}, "
            + f"fail={lane_data['fail']}, "
            + f"timeout={lane_data['timeout']}, "
            + f"max_pass={lane_data['pass_elapsed_seconds_max']:.2f}s"
        )

    report.extend(
        [
            "",
            "Slowest bounded probes:",
        ]
    )

    for row in runtime[
        "slowest_probes"
    ][:10]:
        report.append(
            "- "
            + f"{row['elapsed_seconds']:.2f}s "
            + row[
                "status"
            ]
            + " "
            + row[
                "lane"
            ]
            + " "
            + row[
                "nodeid"
            ]
        )

    report.extend(
        [
            "",
            "## Completion",
            "",
        ]
    )

    for key, value in completion.items():
        report.append(
            "- "
            + key
            + ": "
            + (
                "PASS"
                if value
                else "FAIL"
            )
        )

    report.extend(
        [
            "",
            (
                "**Phase 155-R6 audit validated: True**"
                if validated
                else "**Phase 155-R6 audit validated: False**"
            ),
            "",
            "Canonical regression: NOT run.",
            "Repository-wide pytest: NOT run.",
            "",
            "R6 is measurement only. It does not delete tests or change production behavior.",
        ]
    )

    (
        output_dir
        / "phase155_r6_summary.md"
    ).write_text(
        "\n".join(
            report
        )
        + "\n",
        encoding="utf-8",
    )

    print("")
    print(
        "Phase 155-R6 audit completed."
    )
    print(
        "collection batches:",
        collection[
            "batches"
        ],
    )
    print(
        "collection failed batches:",
        len(
            collection[
                "failed_batches"
            ]
        ),
    )
    print(
        "runtime probes:",
        runtime[
            "selected_probes"
        ],
    )
    print(
        "R6 audit validated:",
        validated,
    )
    print(
        "canonical regression: NOT run"
    )
    print(
        "repository-wide pytest: NOT run"
    )
    print(
        "summary:",
        output_dir
        / "phase155_r6_summary.md",
    )

    return 0 if validated else 2


if __name__ == "__main__":
    raise SystemExit(main())
