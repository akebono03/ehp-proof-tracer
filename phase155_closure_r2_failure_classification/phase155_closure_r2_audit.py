from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


FAILED_RE = re.compile(
    r"^FAILED\s+(?P<nodeid>tests/[^\s]+::[^\s]+)\s*$"
)

SLOW_RE = re.compile(
    r"^(?P<seconds>\d+(?:\.\d+)?)s\s+"
    r"(?P<phase>call|setup|teardown)\s+"
    r"(?P<nodeid>tests/[^\s]+::[^\s]+)\s*$"
)

SAFE_STALE_PREFIXES = (
    "tests/test_phase132_",
    "tests/test_phase133_",
    "tests/test_phase143_",
    "tests/test_phase150_",
)

HISTORICAL_HEAVY_PREFIXES = (
    "tests/test_phase144_",
)

CONTRACT_SENSITIVE_PREFIXES = (
    "tests/test_phase153_",
    "tests/test_phase95_",
    "tests/test_phase96_",
    "tests/test_phase97_",
    "tests/test_phase98_",
)


@dataclass(frozen=True)
class FailureRecord:
    nodeid: str
    file: str
    phase_family: str
    category: str
    reason: str


def _phase_family(file_path: str) -> str:
    match = re.search(
        r"test_phase(\d+)",
        file_path,
    )
    if not match:
        return "non_phase"
    return "phase" + match.group(1)


def _classify(
    nodeid: str,
) -> FailureRecord:
    file_path = nodeid.split(
        "::",
        1,
    )[0]

    if file_path.startswith(
        SAFE_STALE_PREFIXES
    ):
        return FailureRecord(
            nodeid=nodeid,
            file=file_path,
            phase_family=_phase_family(
                file_path
            ),
            category="SAFE_STALE",
            reason=(
                "Historical presentation/rendering/reference "
                "expectation predates the current generic route."
            ),
        )

    if file_path.startswith(
        HISTORICAL_HEAVY_PREFIXES
    ):
        return FailureRecord(
            nodeid=nodeid,
            file=file_path,
            phase_family=_phase_family(
                file_path
            ),
            category="HISTORICAL_HEAVY",
            reason=(
                "Historical cross-group/contribution audit with "
                "fixed population or renderer-internal assumptions; "
                "requires redundancy/heavy-test review before change."
            ),
        )

    if file_path.startswith(
        CONTRACT_SENSITIVE_PREFIXES
    ):
        return FailureRecord(
            nodeid=nodeid,
            file=file_path,
            phase_family=_phase_family(
                file_path
            ),
            category="CONTRACT_SENSITIVE",
            reason=(
                "Touches Reference ownership, provenance, source metadata, "
                "or aggregate-result semantics; do not auto-repair."
            ),
        )

    return FailureRecord(
        nodeid=nodeid,
        file=file_path,
        phase_family=_phase_family(
            file_path
        ),
        category="UNKNOWN",
        reason=(
            "No reviewed Phase155 Closure-R2 classification rule."
        ),
    )


def _extract_failures(
    log_text: str,
) -> tuple[FailureRecord, ...]:
    nodeids = []

    for line in log_text.splitlines():
        match = FAILED_RE.match(
            line.strip()
        )
        if match:
            nodeids.append(
                match.group(
                    "nodeid"
                )
            )

    return tuple(
        _classify(
            nodeid
        )
        for nodeid in nodeids
    )


def _extract_slow_rows(
    log_text: str,
) -> tuple[dict[str, object], ...]:
    result = []

    for line in log_text.splitlines():
        match = SLOW_RE.match(
            line.strip()
        )
        if not match:
            continue

        result.append(
            {
                "seconds": float(
                    match.group(
                        "seconds"
                    )
                ),
                "phase": match.group(
                    "phase"
                ),
                "nodeid": match.group(
                    "nodeid"
                ),
            }
        )

    return tuple(
        sorted(
            result,
            key=lambda row: (
                -float(
                    row[
                        "seconds"
                    ]
                ),
                str(
                    row[
                        "nodeid"
                    ]
                ),
            ),
        )
    )


def _write_manifest(
    path: Path,
    records: tuple[
        FailureRecord,
        ...,
    ],
) -> None:
    path.write_text(
        "".join(
            record.nodeid
            + "\n"
            for record in records
        ),
        encoding="utf-8",
    )


def _markdown_report(
    records: tuple[
        FailureRecord,
        ...,
    ],
    slow_rows: tuple[
        dict[str, object],
        ...,
    ],
) -> str:
    counts = Counter(
        record.category
        for record in records
    )

    phases = Counter(
        record.phase_family
        for record in records
    )

    category_phases: dict[
        str,
        Counter[str],
    ] = defaultdict(
        Counter
    )

    for record in records:
        category_phases[
            record.category
        ][
            record.phase_family
        ] += 1

    lines = [
        "# Phase 155 Closure-R2 failure classification",
        "",
        "## Summary",
        "",
        "```text",
        f"failed nodeids: {len(records)}",
        f"SAFE_STALE: {counts['SAFE_STALE']}",
        f"HISTORICAL_HEAVY: {counts['HISTORICAL_HEAVY']}",
        f"CONTRACT_SENSITIVE: {counts['CONTRACT_SENSITIVE']}",
        f"UNKNOWN: {counts['UNKNOWN']}",
        "```",
        "",
        "## Phase-family breakdown",
        "",
        "```text",
    ]

    for phase, count in sorted(
        phases.items()
    ):
        lines.append(
            f"{phase}: {count}"
        )

    lines.extend(
        [
            "```",
            "",
            "## Category meaning",
            "",
            "- `SAFE_STALE`: historical display/string expectation; "
            "eligible for focused stale-expectation repair.",
            "- `HISTORICAL_HEAVY`: old cross-group/population/internal audit; "
            "review redundancy and runtime before deciding repair/delete/archive.",
            "- `CONTRACT_SENSITIVE`: Reference ownership/provenance/source metadata/"
            "aggregate-result semantics; requires contract diagnosis.",
            "- `UNKNOWN`: no reviewed rule. Closure-R2 must end with zero.",
            "",
            "## Category / phase matrix",
            "",
            "```text",
        ]
    )

    for category in (
        "SAFE_STALE",
        "HISTORICAL_HEAVY",
        "CONTRACT_SENSITIVE",
        "UNKNOWN",
    ):
        detail = ", ".join(
            f"{phase}={count}"
            for phase, count
            in sorted(
                category_phases[
                    category
                ].items()
            )
        )
        lines.append(
            f"{category}: {detail}"
        )

    lines.extend(
        [
            "```",
            "",
            "## Slowest failed-test evidence",
            "",
            "The full-suite log is used only as measured evidence; "
            "Closure-R2 does not rerun these tests.",
            "",
            "```text",
        ]
    )

    failed_nodeids = {
        record.nodeid
        for record in records
    }

    count = 0
    for row in slow_rows:
        nodeid = str(
            row[
                "nodeid"
            ]
        )
        if nodeid not in failed_nodeids:
            continue

        lines.append(
            f"{row['seconds']:8.2f}s "
            f"{row['phase']:8s} "
            f"{nodeid}"
        )
        count += 1
        if count >= 20:
            break

    lines.extend(
        [
            "```",
            "",
            "## Repair boundary",
            "",
            "Closure-R2 does not modify production code and does not rerun "
            "the 10,421-test repository suite.",
            "",
            "`SAFE_STALE` is the only automatic repair candidate lane.",
            "",
            "`HISTORICAL_HEAVY` and `CONTRACT_SENSITIVE` remain unchanged "
            "until their own focused review.",
            "",
        ]
    )

    return "\n".join(
        lines
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=Path(
            "phase155_closure_output/"
            "phase155_full_pytest.log"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_closure_r2_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    log_path = (
        args.log
        if args.log.is_absolute()
        else repo_root
        / args.log
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

    if not log_path.exists():
        raise SystemExit(
            "Closure full-suite log not found: "
            + str(
                log_path
            )
        )

    log_text = log_path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    records = _extract_failures(
        log_text
    )
    slow_rows = _extract_slow_rows(
        log_text
    )

    counts = Counter(
        record.category
        for record in records
    )

    expected = {
        "SAFE_STALE": 38,
        "HISTORICAL_HEAVY": 36,
        "CONTRACT_SENSITIVE": 24,
        "UNKNOWN": 0,
    }

    actual = {
        key: counts[
            key
        ]
        for key in expected
    }

    print(
        "Phase 155 Closure-R2 static classification"
    )
    print(
        "Repository tests: NOT executed"
    )
    print(
        "Production changes: none"
    )
    print("")
    print(
        "failed nodeids:",
        len(
            records
        ),
    )

    for key in expected:
        print(
            f"{key}: {actual[key]}"
        )

    if len(
        records
    ) != 98:
        raise SystemExit(
            "Expected 98 failed nodeids; "
            f"found {len(records)}"
        )

    if actual != expected:
        raise SystemExit(
            "Classification counts changed: "
            f"actual={actual}, expected={expected}"
        )

    by_category = {
        category: tuple(
            record
            for record in records
            if record.category
            == category
        )
        for category in expected
    }

    for category, category_records in by_category.items():
        _write_manifest(
            output_dir
            / (
                category.lower()
                + "_nodeids.txt"
            ),
            category_records,
        )

    json_payload = {
        "source_log": str(
            log_path
        ),
        "failure_count": len(
            records
        ),
        "counts": actual,
        "records": [
            asdict(
                record
            )
            for record in records
        ],
        "slow_rows": list(
            slow_rows
        ),
        "closure_r2_validated": True,
        "repository_tests_executed": False,
        "production_changes": False,
    }

    (
        output_dir
        / "phase155_closure_r2_classification.json"
    ).write_text(
        json.dumps(
            json_payload,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_closure_r2_classification.md"
    ).write_text(
        _markdown_report(
            records,
            slow_rows,
        ),
        encoding="utf-8",
    )

    repair_plan = """# Phase 155 Closure-R2 repair plan

1. SAFE_STALE (38)
   - Repair historical presentation/rendering/reference expectations only.
   - Use focused tests; do not run repository-wide pytest.

2. HISTORICAL_HEAVY (36)
   - Review redundancy, fixed-count assumptions, internal renderer coupling,
     and measured runtime.
   - Do not automatically update counts or old snapshots.
   - Prefer delete/archive/split/lightweight replacement when justified.

3. CONTRACT_SENSITIVE (24)
   - Diagnose Reference ownership/provenance/source metadata/current
     aggregate-result contract.
   - No automatic stale repair.

4. Closure regression
   - Introduce sharded/checkpointed regression before final closure.
   - Do not return to one 40-minute monolithic retry loop.
"""

    (
        output_dir
        / "phase155_closure_r2_repair_plan.md"
    ).write_text(
        repair_plan,
        encoding="utf-8",
    )

    print("")
    print(
        "Closure-R2 classification validated: True"
    )
    print(
        "Output:",
        output_dir,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
