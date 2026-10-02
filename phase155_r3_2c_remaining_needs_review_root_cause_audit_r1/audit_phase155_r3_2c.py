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

REVIEW_FAILURE_LINKED = "failure_linked"
REVIEW_SOURCE_EVIDENCE = "source_evidence_issue"
REVIEW_OTHER = "other_review_reason"

FAILING_TESTS = {
    "tests/test_phase143_1_generic_proof_order.py::"
    "test_phase143_1_generic_order_has_no_pi6_specific_hardcoding",
    "tests/test_phase143_1b_semantic_proof_order.py::"
    "test_phase143_1b_generic_order_has_no_pi6_specific_hardcoding",
}


@dataclass(frozen=True)
class RootCauseRecord:
    candidate_id: str
    original_review_class: str
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


def _is_true(value: str) -> bool:
    return value.strip().lower() in {
        "true",
        "1",
        "yes",
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
        original_review_class = review.get(
            "review_class",
            "",
        )

        if original_review_class == REVIEW_FAILURE_LINKED:
            continue

        if original_review_class not in {
            REVIEW_SOURCE_EVIDENCE,
            REVIEW_OTHER,
        }:
            continue

        candidate_id = review["candidate_id"]
        verified = verified_by_id.get(
            candidate_id
        )

        if verified is None:
            result.append(
                RootCauseRecord(
                    candidate_id=candidate_id,
                    original_review_class=original_review_class,
                    candidate_category="",
                    older_test_id=review.get(
                        "older_test_id",
                        "",
                    ),
                    newer_test_id=review.get(
                        "newer_test_id",
                        "",
                    ),
                    older_outcome=review.get(
                        "older_outcome",
                        "",
                    ),
                    newer_outcome=review.get(
                        "newer_outcome",
                        "",
                    ),
                    older_source_available="",
                    newer_source_available="",
                    function_hash_equal=review.get(
                        "function_hash_equal",
                        "",
                    ),
                    semantic_function_hash_equal="",
                    dependency_hash_equal=review.get(
                        "dependency_hash_equal",
                        "",
                    ),
                    root_cause=ROOT_UNRESOLVED,
                    linked_failing_test="",
                    repair_target="R3-2 candidate-id join",
                    reason=(
                        "The R3-2B review row has no matching "
                        "R3-2 verified-pair row."
                    ),
                )
            )
            continue

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
            root_cause = ROOT_FAILED_MEMBER
            repair_target = linked_failing_test
            reason = (
                "The pair is blocked by one of the two already-proven "
                "stale Phase 143 hardcoding tests."
            )

        elif (
            older_outcome == "missing"
            or newer_outcome == "missing"
        ):
            root_cause = ROOT_MISSING_EXECUTION
            repair_target = "R3-2 execution/result recording"
            reason = (
                "At least one pair member has no recorded call-phase "
                "pytest outcome."
            )

        elif (
            not _is_true(
                older_source_available
            )
            or not _is_true(
                newer_source_available
            )
        ):
            root_cause = ROOT_SOURCE_UNAVAILABLE
            repair_target = "R3-2 source evidence"
            reason = (
                "At least one pair member lacks usable source evidence."
            )

        elif (
            older_outcome == "passed"
            and newer_outcome == "passed"
        ):
            root_cause = ROOT_CLASSIFIER_CONSERVATIVE
            repair_target = "none"
            reason = (
                "Both tests pass and source evidence is available. "
                "The conservative R3-2 classifier did not prove enough "
                "identity/coverage to authorize deletion, so the pair "
                "should be retained rather than treated as a failure."
            )

        else:
            root_cause = ROOT_UNRESOLVED
            repair_target = "manual review"
            reason = (
                "The available execution and source evidence do not fit "
                "a known R3-2C root-cause class."
            )

        result.append(
            RootCauseRecord(
                candidate_id=candidate_id,
                original_review_class=(
                    original_review_class
                ),
                candidate_category=(
                    verified.get(
                        "candidate_category",
                        "",
                    )
                ),
                older_test_id=older,
                newer_test_id=newer,
                older_outcome=older_outcome,
                newer_outcome=newer_outcome,
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
                root_cause=root_cause,
                linked_failing_test=(
                    linked_failing_test
                ),
                repair_target=repair_target,
                reason=reason,
            )
        )

    return result


def write_summary(
    path: Path,
    repo_root: Path,
    records: list[RootCauseRecord],
) -> None:
    counts = Counter(
        row.root_cause
        for row in records
    )
    input_counts = Counter(
        row.original_review_class
        for row in records
    )

    blocking = (
        counts[ROOT_MISSING_EXECUTION]
        + counts[ROOT_SOURCE_UNAVAILABLE]
        + counts[ROOT_UNRESOLVED]
    )

    lines = [
        "# Phase 155-R3-2C-r1 — remaining needs-review root-cause audit",
        "",
        "## Correction from R3-2C",
        "",
        "The original R3-2C incorrectly filtered only `other_review_reason`.",
        "R3-2B printed `other needs review` as the sum of "
        "`source_evidence_issue` and `other_review_reason`.",
        "This repaired audit includes both classes.",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Remaining review pairs audited: {len(records)}",
        "",
        "## Input review classes",
        "",
        "| class | pairs |",
        "| --- | ---: |",
        f"| `{REVIEW_SOURCE_EVIDENCE}` | {input_counts[REVIEW_SOURCE_EVIDENCE]} |",
        f"| `{REVIEW_OTHER}` | {input_counts[REVIEW_OTHER]} |",
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
            f"- Blocking pairs: {blocking}",
            "",
            "## Interpretation",
            "",
            "- `failed_member_not_recognized_as_known_failure`: blocked only by one of the two stale Phase 143 hardcoding expectations.",
            "- `missing_execution_record`: R3-2 result recording issue.",
            "- `source_evidence_unavailable`: source extraction/evidence issue.",
            "- `classifier_conservative_boundary`: both tests pass with source evidence, but deletion is not proven; retain the pair.",
            "- `unresolved`: additional audit required.",
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
            "phase155_r3_2c_r1_audit_output"
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
        / "phase155_r3_2c_r1_root_causes.csv",
        records,
    )

    write_summary(
        output_dir
        / "phase155_r3_2c_r1_summary.md",
        repo_root,
        records,
    )

    counts = Counter(
        row.root_cause
        for row in records
    )
    input_counts = Counter(
        row.original_review_class
        for row in records
    )
    blocking = (
        counts[
            ROOT_MISSING_EXECUTION
        ]
        + counts[
            ROOT_SOURCE_UNAVAILABLE
        ]
        + counts[
            ROOT_UNRESOLVED
        ]
    )

    metadata = {
        "phase": "155-R3-2C-r1",
        "git_head": _git_head(
            repo_root
        ),
        "remaining_review_pairs": len(
            records
        ),
        "input_review_class_counts": dict(
            input_counts
        ),
        "root_cause_counts": dict(
            counts
        ),
        "blocking_pair_count": (
            blocking
        ),
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_2c_r1_metadata.json"
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
        "Phase 155-R3-2C-r1 remaining needs-review root-cause audit completed."
    )
    print(
        "remaining review pairs:",
        len(records),
    )
    print(
        "source-evidence review pairs:",
        input_counts[
            REVIEW_SOURCE_EVIDENCE
        ],
    )
    print(
        "other-review pairs:",
        input_counts[
            REVIEW_OTHER
        ],
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
        blocking,
    )
    print(
        "output:",
        output_dir,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
