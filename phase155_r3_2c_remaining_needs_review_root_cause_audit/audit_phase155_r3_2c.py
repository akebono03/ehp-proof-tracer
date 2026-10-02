from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ROOT_FAILED_MEMBER = "failed_member_not_recognized_as_known_failure"
ROOT_MISSING_EXECUTION = "missing_execution_record"
ROOT_SOURCE_UNAVAILABLE = "source_evidence_unavailable"
ROOT_CLASSIFIER_CONSERVATIVE = "classifier_conservative_boundary"
ROOT_UNRESOLVED = "unresolved"

FAILING_TESTS = {
    "tests/test_phase143_1_generic_proof_order.py::"
    "test_phase143_1_generic_order_has_no_pi6_specific_hardcoding",
    "tests/test_phase143_1b_semantic_proof_order.py::"
    "test_phase143_1b_generic_order_has_no_pi6_specific_hardcoding",
}


@dataclass(frozen=True)
class RootCauseRecord:
    candidate_id: str
    candidate_category: str
    older_test_id: str
    newer_test_id: str
    older_outcome: str
    newer_outcome: str
    older_source_available: str
    newer_source_available: str
    function_hash_equal: str
    semantic_function_hash_equal: str
    dependency_hash_equal: str
    root_cause: str
    linked_failing_test: str
    repair_target: str
    reason: str


def _git_head(repo_root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: Iterable[object]) -> None:
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(asdict(rows[0]).keys())
    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def _source_by_test_id(
    source_rows: list[dict[str, str]],
) -> dict[str, dict[str, str]]:
    return {
        row["test_id"]: row
        for row in source_rows
    }


def classify_root_causes(
    verified_rows: list[dict[str, str]],
    review_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
) -> list[RootCauseRecord]:
    verified_by_id = {
        row["candidate_id"]: row
        for row in verified_rows
    }
    source_by_test = _source_by_test_id(
        source_rows
    )

    result: list[RootCauseRecord] = []

    for review in review_rows:
        if review.get("review_class") != "other_review_reason":
            continue

        candidate_id = review["candidate_id"]
        verified = verified_by_id[
            candidate_id
        ]

        older = verified[
            "older_test_id"
        ]
        newer = verified[
            "newer_test_id"
        ]

        older_outcome = verified.get(
            "older_outcome",
            "",
        )
        newer_outcome = verified.get(
            "newer_outcome",
            "",
        )

        older_source = source_by_test.get(
            older,
            {},
        )
        newer_source = source_by_test.get(
            newer,
            {},
        )

        older_source_available = (
            older_source.get(
                "source_available",
                "",
            )
        )
        newer_source_available = (
            newer_source.get(
                "source_available",
                "",
            )
        )

        linked_failing_test = ""

        if (
            older in FAILING_TESTS
            and older_outcome == "failed"
        ):
            linked_failing_test = older
        elif (
            newer in FAILING_TESTS
            and newer_outcome == "failed"
        ):
            linked_failing_test = newer

        if linked_failing_test:
            root_cause = (
                ROOT_FAILED_MEMBER
            )
            repair_target = (
                linked_failing_test
            )
            reason = (
                "The pair contains one of the two known stale hardcoding "
                "tests and its pytest outcome is failed. It was not labeled "
                "failure_linked by R3-2B only because the prior linkage rule "
                "matched exact pair membership conservatively."
            )

        elif (
            older_outcome == "missing"
            or newer_outcome == "missing"
        ):
            root_cause = (
                ROOT_MISSING_EXECUTION
            )
            repair_target = (
                "R3-2 execution/result recording"
            )
            reason = (
                "At least one pair member has no recorded call-phase "
                "pytest outcome."
            )

        elif (
            older_source_available.lower()
            not in ("true", "1")
            or newer_source_available.lower()
            not in ("true", "1")
        ):
            root_cause = (
                ROOT_SOURCE_UNAVAILABLE
            )
            repair_target = (
                "R3-2 source evidence"
            )
            reason = (
                "At least one pair member lacks source evidence, so "
                "coverage replacement cannot be classified."
            )

        elif (
            older_outcome == "passed"
            and newer_outcome == "passed"
        ):
            root_cause = (
                ROOT_CLASSIFIER_CONSERVATIVE
            )
            repair_target = (
                "none"
            )
            reason = (
                "Both tests pass and source evidence is available. The pair "
                "remained needs_review because R3-2 intentionally requires "
                "stronger proof than the available fingerprint relation. "
                "This is not a test-suite failure and should remain retained "
                "unless a later manual proof establishes redundancy."
            )

        else:
            root_cause = (
                ROOT_UNRESOLVED
            )
            repair_target = (
                "manual review"
            )
            reason = (
                "The available execution and source evidence do not fit a "
                "known R3-2C root-cause class."
            )

        result.append(
            RootCauseRecord(
                candidate_id=(
                    candidate_id
                ),
                candidate_category=(
                    verified.get(
                        "candidate_category",
                        "",
                    )
                ),
                older_test_id=older,
                newer_test_id=newer,
                older_outcome=(
                    older_outcome
                ),
                newer_outcome=(
                    newer_outcome
                ),
                older_source_available=(
                    older_source_available
                ),
                newer_source_available=(
                    newer_source_available
                ),
                function_hash_equal=(
                    verified.get(
                        "function_hash_equal",
                        "",
                    )
                ),
                semantic_function_hash_equal=(
                    verified.get(
                        "semantic_function_hash_equal",
                        "",
                    )
                ),
                dependency_hash_equal=(
                    verified.get(
                        "dependency_hash_equal",
                        "",
                    )
                ),
                root_cause=(
                    root_cause
                ),
                linked_failing_test=(
                    linked_failing_test
                ),
                repair_target=(
                    repair_target
                ),
                reason=(
                    reason
                ),
            )
        )

    return result


def write_summary(
    path: Path,
    repo_root: Path,
    records: list[
        RootCauseRecord
    ],
) -> None:
    counts = Counter(
        row.root_cause
        for row in records
    )

    lines = [
        "# Phase 155-R3-2C — remaining needs-review root-cause audit",
        "",
        "## Boundary",
        "",
        "This audit classifies only the six R3-2B `other_review_reason` pairs.",
        "It modifies no production code and no existing test.",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Other needs-review pairs audited: {len(records)}",
        "",
        "## Root causes",
        "",
        "| root cause | pairs |",
        "| --- | ---: |",
    ]

    for category in (
        ROOT_FAILED_MEMBER,
        ROOT_MISSING_EXECUTION,
        ROOT_SOURCE_UNAVAILABLE,
        ROOT_CLASSIFIER_CONSERVATIVE,
        ROOT_UNRESOLVED,
    ):
        lines.append(
            f"| `{category}` | {counts[category]} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `failed_member_not_recognized_as_known_failure`: the pair is blocked only by one of the two already-proven stale hardcoding tests.",
            "- `missing_execution_record`: R3-2 execution/result recording must be repaired before classification.",
            "- `source_evidence_unavailable`: source extraction must be repaired before classification.",
            "- `classifier_conservative_boundary`: both tests pass and source evidence exists, but the conservative classifier intentionally does not authorize removal. These pairs should be retained, not treated as failures.",
            "- `unresolved`: additional manual/source audit is required.",
            "",
            "## Next-step gate",
            "",
            "If all non-conservative pairs are explained by the two stale hardcoding tests and there are no missing/source/unresolved causes, R3-2 can be closed by repairing those two test expectations and re-running candidate verification.",
            "Pairs at the conservative classifier boundary remain retained and do not block R3-2 closure.",
            "",
            "Repository-wide pytest remains deferred until Phase 155 closure.",
        ]
    )

    path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
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
            "phase155_r3_2_audit_output/"
            "phase155_r3_2_verified_pairs.csv"
        ),
    )
    parser.add_argument(
        "--source-evidence",
        type=Path,
        default=Path(
            "phase155_r3_2_audit_output/"
            "phase155_r3_2_source_evidence.csv"
        ),
    )
    parser.add_argument(
        "--needs-review-audit",
        type=Path,
        default=Path(
            "phase155_r3_2b_audit_output/"
            "phase155_r3_2b_needs_review_audit.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_2c_audit_output"
        ),
    )

    args = parser.parse_args()
    repo_root = args.repo_root.resolve()

    def resolve(path: Path) -> Path:
        return (
            path
            if path.is_absolute()
            else repo_root / path
        )

    verified_path = resolve(
        args.verified_pairs
    )
    source_path = resolve(
        args.source_evidence
    )
    review_path = resolve(
        args.needs_review_audit
    )

    for required in (
        verified_path,
        source_path,
        review_path,
    ):
        if not required.exists():
            raise SystemExit(
                "required audit input not found: "
                + str(required)
            )

    records = classify_root_causes(
        _read_csv(
            verified_path
        ),
        _read_csv(
            review_path
        ),
        _read_csv(
            source_path
        ),
    )

    output_dir = resolve(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    _write_csv(
        output_dir
        / "phase155_r3_2c_root_causes.csv",
        records,
    )

    write_summary(
        output_dir
        / "phase155_r3_2c_summary.md",
        repo_root,
        records,
    )

    counts = Counter(
        row.root_cause
        for row in records
    )

    metadata = {
        "phase": "155-R3-2C",
        "git_head": _git_head(
            repo_root
        ),
        "other_needs_review_pairs": len(
            records
        ),
        "root_cause_counts": dict(
            counts
        ),
        "blocking_pair_count": (
            counts[
                ROOT_MISSING_EXECUTION
            ]
            + counts[
                ROOT_SOURCE_UNAVAILABLE
            ]
            + counts[
                ROOT_UNRESOLVED
            ]
        ),
        "stale_failure_linked_pair_count": (
            counts[
                ROOT_FAILED_MEMBER
            ]
        ),
        "conservative_retain_pair_count": (
            counts[
                ROOT_CLASSIFIER_CONSERVATIVE
            ]
        ),
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_2c_metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R3-2C remaining needs-review root-cause audit completed."
    )
    print(
        "other needs-review pairs:",
        len(records),
    )
    print(
        "stale-failure-linked:",
        counts[
            ROOT_FAILED_MEMBER
        ],
    )
    print(
        "missing execution:",
        counts[
            ROOT_MISSING_EXECUTION
        ],
    )
    print(
        "source unavailable:",
        counts[
            ROOT_SOURCE_UNAVAILABLE
        ],
    )
    print(
        "classifier conservative boundary:",
        counts[
            ROOT_CLASSIFIER_CONSERVATIVE
        ],
    )
    print(
        "unresolved:",
        counts[
            ROOT_UNRESOLVED
        ],
    )
    print(
        "blocking pairs:",
        (
            counts[
                ROOT_MISSING_EXECUTION
            ]
            + counts[
                ROOT_SOURCE_UNAVAILABLE
            ]
            + counts[
                ROOT_UNRESOLVED
            ]
        ),
    )
    print(
        "output:",
        output_dir,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
