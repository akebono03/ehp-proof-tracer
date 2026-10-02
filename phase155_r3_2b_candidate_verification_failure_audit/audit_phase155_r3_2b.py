from __future__ import annotations

import argparse
import ast
import csv
import inspect
import json
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


FAILING_TESTS = (
    "tests/test_phase143_1_generic_proof_order.py::"
    "test_phase143_1_generic_order_has_no_pi6_specific_hardcoding",
    "tests/test_phase143_1b_semantic_proof_order.py::"
    "test_phase143_1b_generic_order_has_no_pi6_specific_hardcoding",
)

TARGET_MODULE = "toda_group_proof_generic_narrative_renderer.py"

OCCURRENCE_ATTRIBUTE_FIELD = "attribute_field"
OCCURRENCE_STRING_LITERAL = "string_literal"
OCCURRENCE_IDENTIFIER = "identifier"
OCCURRENCE_CONTROL_FLOW = "control_flow_condition"
OCCURRENCE_OTHER = "other"

REVIEW_FAILURE_LINKED = "failure_linked"
REVIEW_SOURCE_EVIDENCE = "source_evidence_issue"
REVIEW_OTHER = "other_review_reason"


@dataclass(frozen=True)
class Pi6Occurrence:
    line: int
    column: int
    node_type: str
    classification: str
    text: str
    in_control_flow: bool


@dataclass(frozen=True)
class FailingTestAudit:
    test_id: str
    source_exists: bool
    test_contains_global_pi6_ban: bool
    target_module_pi6_occurrences: int
    target_module_control_flow_pi6_occurrences: int
    target_module_attribute_field_pi6_occurrences: int
    stale_expectation_supported: bool
    reason: str


@dataclass(frozen=True)
class NeedsReviewAudit:
    candidate_id: str
    older_test_id: str
    newer_test_id: str
    older_outcome: str
    newer_outcome: str
    function_hash_equal: str
    dependency_hash_equal: str
    review_class: str
    linked_failing_test: str
    reason: str


def _git_head(
    repo_root: Path,
) -> str:
    try:
        completed = subprocess.run(
            [
                "git",
                "rev-parse",
                "HEAD",
            ],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()
    except (
        OSError,
        subprocess.CalledProcessError,
    ):
        return "unavailable"


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


def _write_csv(
    path: Path,
    rows: Iterable[object],
) -> None:
    rows = list(rows)

    if not rows:
        path.write_text(
            "",
            encoding="utf-8",
        )
        return

    fieldnames = list(
        asdict(
            rows[0]
        ).keys()
    )

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
            writer.writerow(
                asdict(
                    row
                )
            )


def _node_text(
    source: str,
    node: ast.AST,
) -> str:
    segment = ast.get_source_segment(
        source,
        node,
    )
    return (
        segment.strip()
        if segment
        else ""
    )


def _control_flow_nodes(
    tree: ast.AST,
) -> set[int]:
    result: set[int] = set()

    for node in ast.walk(
        tree
    ):
        tests = []

        if isinstance(
            node,
            ast.If,
        ):
            tests.append(
                node.test
            )
        elif isinstance(
            node,
            ast.While,
        ):
            tests.append(
                node.test
            )
        elif isinstance(
            node,
            ast.IfExp,
        ):
            tests.append(
                node.test
            )
        elif isinstance(
            node,
            ast.comprehension,
        ):
            tests.extend(
                node.ifs
            )

        for test in tests:
            for child in ast.walk(
                test
            ):
                result.add(
                    id(
                        child
                    )
                )

    return result


def find_pi6_occurrences(
    source: str,
) -> tuple[
    Pi6Occurrence,
    ...,
]:
    tree = ast.parse(
        source
    )
    control_flow_ids = (
        _control_flow_nodes(
            tree
        )
    )
    result = []

    for node in ast.walk(
        tree
    ):
        classification = None
        text = ""

        if isinstance(
            node,
            ast.Attribute,
        ) and "pi6" in node.attr.lower():
            classification = (
                OCCURRENCE_ATTRIBUTE_FIELD
            )
            text = node.attr

        elif isinstance(
            node,
            ast.Name,
        ) and "pi6" in node.id.lower():
            classification = (
                OCCURRENCE_IDENTIFIER
            )
            text = node.id

        elif (
            isinstance(
                node,
                ast.Constant,
            )
            and isinstance(
                node.value,
                str,
            )
            and "pi6"
            in node.value.lower()
        ):
            classification = (
                OCCURRENCE_STRING_LITERAL
            )
            text = node.value

        if classification is None:
            continue

        in_control_flow = (
            id(
                node
            )
            in control_flow_ids
        )

        if in_control_flow:
            classification = (
                OCCURRENCE_CONTROL_FLOW
            )

        result.append(
            Pi6Occurrence(
                line=getattr(
                    node,
                    "lineno",
                    0,
                ),
                column=getattr(
                    node,
                    "col_offset",
                    0,
                ),
                node_type=type(
                    node
                ).__name__,
                classification=classification,
                text=text,
                in_control_flow=(
                    in_control_flow
                ),
            )
        )

    return tuple(
        sorted(
            result,
            key=lambda row: (
                row.line,
                row.column,
                row.node_type,
            ),
        )
    )


def _test_source(
    repo_root: Path,
    test_id: str,
) -> str | None:
    file_name, function_name = (
        test_id.split(
            "::",
            1,
        )
    )
    path = (
        repo_root
        / file_name
    )

    if not path.exists():
        return None

    source = path.read_text(
        encoding="utf-8-sig",
    )
    tree = ast.parse(
        source
    )

    for node in tree.body:
        if (
            isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and node.name
            == function_name
        ):
            return _node_text(
                source,
                node,
            )

    return None


def _contains_global_pi6_ban(
    test_source: str,
) -> bool:
    try:
        tree = ast.parse(
            test_source
        )
    except SyntaxError:
        return False

    has_pi6_literal = any(
        isinstance(
            node,
            ast.Constant,
        )
        and isinstance(
            node.value,
            str,
        )
        and node.value == "pi6"
        for node in ast.walk(
            tree
        )
    )

    has_negative_membership_assertion = any(
        isinstance(
            node,
            ast.Assert,
        )
        and isinstance(
            node.test,
            ast.Compare,
        )
        and any(
            isinstance(
                operator,
                ast.NotIn,
            )
            for operator in node.test.ops
        )
        for node in ast.walk(
            tree
        )
    )

    has_forbidden_fragments_name = any(
        isinstance(
            node,
            ast.Name,
        )
        and node.id
        == "forbidden_fragments"
        for node in ast.walk(
            tree
        )
    )

    return (
        has_pi6_literal
        and has_negative_membership_assertion
        and has_forbidden_fragments_name
    )


def audit_failing_tests(
    repo_root: Path,
    module_occurrences: tuple[
        Pi6Occurrence,
        ...,
    ],
) -> list[
    FailingTestAudit
]:
    control_flow_count = sum(
        occurrence.in_control_flow
        for occurrence
        in module_occurrences
    )
    attribute_count = sum(
        occurrence.classification
        == OCCURRENCE_ATTRIBUTE_FIELD
        for occurrence
        in module_occurrences
    )

    result = []

    for test_id in FAILING_TESTS:
        source = _test_source(
            repo_root,
            test_id,
        )

        contains_global_ban = (
            source is not None
            and _contains_global_pi6_ban(
                source
            )
        )

        stale_supported = (
            source is not None
            and contains_global_ban
            and len(
                module_occurrences
            )
            > 0
            and control_flow_count
            == 0
            and attribute_count
            == len(
                module_occurrences
            )
        )

        if stale_supported:
            reason = (
                "The test bans the substring 'pi6' across the entire "
                "renderer source, but every current AST-level pi6 occurrence "
                "is an attribute field reference and none participates in a "
                "control-flow condition."
            )
        else:
            reason = (
                "The available source evidence does not prove that the "
                "global pi6 ban is stale."
            )

        result.append(
            FailingTestAudit(
                test_id=test_id,
                source_exists=(
                    source is not None
                ),
                test_contains_global_pi6_ban=(
                    contains_global_ban
                ),
                target_module_pi6_occurrences=len(
                    module_occurrences
                ),
                target_module_control_flow_pi6_occurrences=(
                    control_flow_count
                ),
                target_module_attribute_field_pi6_occurrences=(
                    attribute_count
                ),
                stale_expectation_supported=(
                    stale_supported
                ),
                reason=reason,
            )
        )

    return result


def audit_needs_review(
    verified_pairs_path: Path,
) -> list[
    NeedsReviewAudit
]:
    rows = _read_csv(
        verified_pairs_path
    )
    result = []

    failing_set = set(
        FAILING_TESTS
    )

    for row in rows:
        if row.get(
            "decision"
        ) != "needs_review":
            continue

        older = row[
            "older_test_id"
        ]
        newer = row[
            "newer_test_id"
        ]

        linked = ""

        if older in failing_set:
            linked = older
        elif newer in failing_set:
            linked = newer

        if linked:
            review_class = (
                REVIEW_FAILURE_LINKED
            )
            reason = (
                "This pair is needs_review because one member is one of the "
                "two focused candidate tests that currently fails."
            )

        elif (
            row.get(
                "older_outcome"
            )
            == "missing"
            or row.get(
                "newer_outcome"
            )
            == "missing"
        ):
            review_class = (
                REVIEW_SOURCE_EVIDENCE
            )
            reason = (
                "At least one test has no recorded call-phase outcome."
            )

        else:
            review_class = (
                REVIEW_OTHER
            )
            reason = (
                "The pair is needs_review for a reason not directly linked "
                "to the two known failing tests."
            )

        result.append(
            NeedsReviewAudit(
                candidate_id=row[
                    "candidate_id"
                ],
                older_test_id=older,
                newer_test_id=newer,
                older_outcome=row.get(
                    "older_outcome",
                    "",
                ),
                newer_outcome=row.get(
                    "newer_outcome",
                    "",
                ),
                function_hash_equal=row.get(
                    "function_hash_equal",
                    "",
                ),
                dependency_hash_equal=row.get(
                    "dependency_hash_equal",
                    "",
                ),
                review_class=review_class,
                linked_failing_test=linked,
                reason=reason,
            )
        )

    return result


def write_summary(
    path: Path,
    repo_root: Path,
    occurrences: tuple[
        Pi6Occurrence,
        ...,
    ],
    failing_audit: list[
        FailingTestAudit
    ],
    review_audit: list[
        NeedsReviewAudit
    ],
) -> None:
    occurrence_counts = Counter(
        row.classification
        for row
        in occurrences
    )
    review_counts = Counter(
        row.review_class
        for row
        in review_audit
    )

    stale_count = sum(
        row.stale_expectation_supported
        for row
        in failing_audit
    )

    lines = [
        "# Phase 155-R3-2B — candidate verification failure audit",
        "",
        "## Boundary",
        "",
        "This step audits the two focused candidate-test failures and the seven R3-2 `needs_review` pairs.",
        "It changes no production code and no existing test.",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Failing tests audited: {len(failing_audit)}",
        f"- Failing tests supported as stale expectation: {stale_count}",
        f"- R3-2 needs-review pairs audited: {len(review_audit)}",
        "",
        "## `pi6` occurrence classification in generic renderer",
        "",
        "| AST classification | occurrences |",
        "| --- | ---: |",
    ]

    for category in (
        OCCURRENCE_ATTRIBUTE_FIELD,
        OCCURRENCE_IDENTIFIER,
        OCCURRENCE_STRING_LITERAL,
        OCCURRENCE_CONTROL_FLOW,
        OCCURRENCE_OTHER,
    ):
        lines.append(
            f"| `{category}` | {occurrence_counts[category]} |"
        )

    lines.extend(
        [
            "",
            "A `pi6` substring in a statement-field name is not by itself evidence of a pi6-specific renderer branch.",
            "The relevant distinction is whether the occurrence participates in control-flow selection or is merely data access.",
            "",
            "## Failing-test audit",
            "",
            "| test | stale expectation supported | control-flow pi6 | attribute-field pi6 |",
            "| --- | --- | ---: | ---: |",
        ]
    )

    for row in failing_audit:
        lines.append(
            "| `"
            + row.test_id
            + "` | "
            + str(
                row.stale_expectation_supported
            ).lower()
            + " | "
            + str(
                row.target_module_control_flow_pi6_occurrences
            )
            + " | "
            + str(
                row.target_module_attribute_field_pi6_occurrences
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## `needs_review` decomposition",
            "",
            "| review class | pairs |",
            "| --- | ---: |",
        ]
    )

    for category in (
        REVIEW_FAILURE_LINKED,
        REVIEW_SOURCE_EVIDENCE,
        REVIEW_OTHER,
    ):
        lines.append(
            f"| `{category}` | {review_counts[category]} |"
        )

    lines.extend(
        [
            "",
            "## Completion interpretation",
            "",
            "R3-2B is an audit-only step.",
            "If both failing tests are supported as stale expectations and every `needs_review` pair is failure-linked, the next step can repair those two expectations and re-run the candidate-focused verification.",
            "If any `needs_review` pair has another cause, that cause must be resolved before R3-3 consolidation.",
            "",
            "Repository-wide pytest remains deferred until Phase 155 closure.",
        ]
    )

    path.write_text(
        "\n".join(
            lines
        )
        + "\n",
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
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_2b_audit_output"
        ),
    )

    args = parser.parse_args()

    repo_root = (
        args.repo_root.resolve()
    )

    verified_pairs_path = (
        args.verified_pairs
        if args.verified_pairs.is_absolute()
        else repo_root
        / args.verified_pairs
    )

    if not verified_pairs_path.exists():
        raise SystemExit(
            "R3-2 verified-pairs CSV not found: "
            + str(
                verified_pairs_path
            )
        )

    module_path = (
        repo_root
        / TARGET_MODULE
    )

    if not module_path.exists():
        raise SystemExit(
            "generic renderer source not found: "
            + str(
                module_path
            )
        )

    module_source = (
        module_path.read_text(
            encoding="utf-8-sig",
        )
    )

    occurrences = (
        find_pi6_occurrences(
            module_source
        )
    )

    failing_audit = (
        audit_failing_tests(
            repo_root,
            occurrences,
        )
    )

    review_audit = (
        audit_needs_review(
            verified_pairs_path
        )
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

    _write_csv(
        output_dir
        / "phase155_r3_2b_pi6_occurrences.csv",
        occurrences,
    )
    _write_csv(
        output_dir
        / "phase155_r3_2b_failing_test_audit.csv",
        failing_audit,
    )
    _write_csv(
        output_dir
        / "phase155_r3_2b_needs_review_audit.csv",
        review_audit,
    )

    write_summary(
        output_dir
        / "phase155_r3_2b_summary.md",
        repo_root,
        occurrences,
        failing_audit,
        review_audit,
    )

    review_counts = Counter(
        row.review_class
        for row
        in review_audit
    )

    metadata = {
        "phase": "155-R3-2B",
        "git_head": _git_head(
            repo_root
        ),
        "failing_tests_audited": len(
            failing_audit
        ),
        "stale_expectation_supported": sum(
            row.stale_expectation_supported
            for row
            in failing_audit
        ),
        "pi6_occurrences": len(
            occurrences
        ),
        "pi6_control_flow_occurrences": sum(
            row.in_control_flow
            for row
            in occurrences
        ),
        "needs_review_pairs": len(
            review_audit
        ),
        "needs_review_classes": dict(
            review_counts
        ),
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_2b_metadata.json"
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
        "Phase 155-R3-2B candidate verification failure audit completed."
    )
    print(
        "failing tests audited:",
        len(
            failing_audit
        ),
    )
    print(
        "stale expectation supported:",
        sum(
            row.stale_expectation_supported
            for row
            in failing_audit
        ),
    )
    print(
        "pi6 AST occurrences:",
        len(
            occurrences
        ),
    )
    print(
        "pi6 control-flow occurrences:",
        sum(
            row.in_control_flow
            for row
            in occurrences
        ),
    )
    print(
        "needs review pairs:",
        len(
            review_audit
        ),
    )
    print(
        "failure-linked needs review:",
        review_counts[
            REVIEW_FAILURE_LINKED
        ],
    )
    print(
        "other needs review:",
        (
            review_counts[
                REVIEW_SOURCE_EVIDENCE
            ]
            + review_counts[
                REVIEW_OTHER
            ]
        ),
    )
    print(
        "output:",
        output_dir,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
