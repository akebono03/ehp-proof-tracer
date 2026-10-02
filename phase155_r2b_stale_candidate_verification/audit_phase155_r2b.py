from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pytest


STATUS_HIGH = "stale_candidate_high"

CLASS_CONFIRMED_STALE = "confirmed_stale"
CLASS_CURRENT_CONTRACT = "current_contract"
CLASS_HISTORICAL_COMPATIBILITY = "historical_compatibility"
CLASS_FALSE_POSITIVE = "false_positive"
CLASS_INCONCLUSIVE = "verification_inconclusive"

FINAL_CLASSES = (
    CLASS_CONFIRMED_STALE,
    CLASS_CURRENT_CONTRACT,
    CLASS_HISTORICAL_COMPATIBILITY,
    CLASS_FALSE_POSITIVE,
    CLASS_INCONCLUSIVE,
)


@dataclass(frozen=True)
class R2Finding:
    finding_id: str
    test_id: str
    file: str
    function: str
    line: int
    phase: str
    r1_category: str
    status: str
    contract: str
    assertion_kind: str
    expected_literal: str
    reason: str


@dataclass(frozen=True)
class TestExecution:
    test_id: str
    outcome: str
    duration_seconds: float
    longrepr: str


@dataclass(frozen=True)
class VerifiedFinding:
    finding_id: str
    test_id: str
    file: str
    function: str
    line: int
    phase: str
    r1_category: str
    contract: str
    assertion_kind: str
    expected_literal: str
    pytest_outcome: str
    verification_class: str
    verification_reason: str


@dataclass(frozen=True)
class FileCoverageDifference:
    file: str
    in_r1: bool
    in_r2: bool
    on_disk: bool
    explanation: str


class ResultRecorder:
    def __init__(self) -> None:
        self.records: dict[str, TestExecution] = {}
        self.collection_errors: list[str] = []

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report) -> None:
        if report.when != "call":
            return
        longrepr = ""
        if report.failed:
            longrepr = str(report.longrepr)
        self.records[report.nodeid] = TestExecution(
            test_id=report.nodeid,
            outcome=report.outcome,
            duration_seconds=float(report.duration),
            longrepr=longrepr[:4000],
        )

    @pytest.hookimpl
    def pytest_collectreport(self, report) -> None:
        if report.failed:
            self.collection_errors.append(str(report.longrepr)[:4000])


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
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_r2_high_findings(path: Path) -> list[R2Finding]:
    result: list[R2Finding] = []
    for row in _read_csv(path):
        if row["status"] != STATUS_HIGH:
            continue
        result.append(
            R2Finding(
                finding_id=row["finding_id"],
                test_id=row["test_id"],
                file=row["file"],
                function=row["function"],
                line=int(row["line"]),
                phase=row["phase"],
                r1_category=row["r1_category"],
                status=row["status"],
                contract=row["contract"],
                assertion_kind=row["assertion_kind"],
                expected_literal=row["expected_literal"],
                reason=row["reason"],
            )
        )
    return result


def unique_test_ids(findings: Iterable[R2Finding]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(item.test_id for item in findings))


def classify(
    finding: R2Finding,
    execution: TestExecution | None,
) -> tuple[str, str]:
    if execution is None:
        return (
            CLASS_INCONCLUSIVE,
            "The selected test produced no call-phase result; collection/setup must be inspected.",
        )

    if execution.outcome == "failed":
        if "AssertionError" in execution.longrepr or "assert " in execution.longrepr:
            return (
                CLASS_CONFIRMED_STALE,
                "The high-candidate test fails with an assertion against the current production behavior.",
            )
        return (
            CLASS_INCONCLUSIVE,
            "The selected test failed for a non-assertion reason, so stale expectation is not proven.",
        )

    if execution.outcome == "skipped":
        return (
            CLASS_INCONCLUSIVE,
            "The selected test was skipped, so the current expectation was not verified.",
        )

    if execution.outcome != "passed":
        return (
            CLASS_INCONCLUSIVE,
            f"Unexpected pytest outcome: {execution.outcome}.",
        )

    if finding.r1_category == "historical_compatibility":
        return (
            CLASS_HISTORICAL_COMPATIBILITY,
            "The expectation passes current behavior and R1 already classified the test as historical compatibility.",
        )

    phase_number = int(finding.phase) if finding.phase.isdigit() else None
    if finding.r1_category == "current_contract" or (
        phase_number is not None and phase_number >= 153
    ):
        return (
            CLASS_CURRENT_CONTRACT,
            "The expectation passes current behavior and belongs to the current Phase 153-154 contract boundary.",
        )

    return (
        CLASS_FALSE_POSITIVE,
        "The static R2 rule marked this expectation high, but the complete test passes current behavior; it is not proven stale.",
    )


def verify_findings(
    repo_root: Path,
    findings: list[R2Finding],
) -> tuple[list[VerifiedFinding], list[TestExecution], list[str], int]:
    nodeids = list(unique_test_ids(findings))
    recorder = ResultRecorder()

    previous = Path.cwd()
    try:
        import os
        os.chdir(repo_root)
        exit_code = pytest.main(
            [
                *nodeids,
                "-q",
                "--tb=short",
                "-p",
                "no:cacheprovider",
            ],
            plugins=[recorder],
        )
    finally:
        os.chdir(previous)

    executions: list[TestExecution] = []
    verified: list[VerifiedFinding] = []

    for test_id in nodeids:
        execution = recorder.records.get(test_id)
        if execution is None:
            execution = TestExecution(
                test_id=test_id,
                outcome="missing",
                duration_seconds=0.0,
                longrepr="No call-phase report was recorded.",
            )
        executions.append(execution)

    execution_by_id = {item.test_id: item for item in executions}

    for finding in findings:
        execution = execution_by_id.get(finding.test_id)
        verification_class, verification_reason = classify(
            finding,
            execution,
        )
        verified.append(
            VerifiedFinding(
                finding_id=finding.finding_id,
                test_id=finding.test_id,
                file=finding.file,
                function=finding.function,
                line=finding.line,
                phase=finding.phase,
                r1_category=finding.r1_category,
                contract=finding.contract,
                assertion_kind=finding.assertion_kind,
                expected_literal=finding.expected_literal,
                pytest_outcome=execution.outcome if execution else "missing",
                verification_class=verification_class,
                verification_reason=verification_reason,
            )
        )

    return verified, executions, recorder.collection_errors, int(exit_code)


def _write_dataclass_csv(path: Path, rows: Iterable[object]) -> None:
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def _r1_files(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {row["file"] for row in _read_csv(path)}


def _r2_files(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {row["file"] for row in _read_csv(path)}


def compare_file_coverage(
    repo_root: Path,
    r1_inventory: Path,
    r2_file_summary: Path,
) -> list[FileCoverageDifference]:
    on_disk = {
        path.relative_to(repo_root).as_posix()
        for path in (repo_root / "tests").glob("test_*.py")
    }
    r1 = _r1_files(r1_inventory)
    r2 = _r2_files(r2_file_summary)
    universe = sorted(on_disk | r1 | r2)

    result: list[FileCoverageDifference] = []
    for file in universe:
        in_r1 = file in r1
        in_r2 = file in r2
        exists = file in on_disk
        if in_r1 == in_r2 == exists:
            continue

        if exists and in_r1 and not in_r2:
            explanation = (
                "Present on disk and in R1 but absent from the R2 file summary. "
                "R2 file_summary counts only files containing a top-level test function recognized by its AST walker; "
                "this is a reporting-coverage difference, not evidence that the source file disappeared."
            )
        elif exists and not in_r1:
            explanation = "Present on disk but absent from the R1 inventory; inspect R1 collection logic."
        elif not exists:
            explanation = "Recorded by an earlier audit but not present on disk now."
        else:
            explanation = "Coverage mismatch requires review."

        result.append(
            FileCoverageDifference(
                file=file,
                in_r1=in_r1,
                in_r2=in_r2,
                on_disk=exists,
                explanation=explanation,
            )
        )
    return result


def write_summary(
    path: Path,
    repo_root: Path,
    findings: list[R2Finding],
    verified: list[VerifiedFinding],
    executions: list[TestExecution],
    coverage: list[FileCoverageDifference],
    collection_errors: list[str],
    pytest_exit_code: int,
) -> None:
    class_counts = Counter(item.verification_class for item in verified)
    outcome_counts = Counter(item.outcome for item in executions)
    contract_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for item in verified:
        contract_counts[item.contract][item.verification_class] += 1

    lines = [
        "# Phase 155-R2B — stale candidate verification",
        "",
        "## Boundary",
        "",
        "R2B executes only the unique test functions referenced by the R2 `stale_candidate_high` findings.",
        "It does not execute the repository-wide test suite, rewrite production code, rewrite existing tests, or delete tests.",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- R2 high findings: {len(findings)}",
        f"- Unique focused tests executed: {len(executions)}",
        f"- Focused pytest exit code: {pytest_exit_code}",
        f"- Collection errors: {len(collection_errors)}",
        "",
        "## Verification classes",
        "",
        "| class | findings |",
        "| --- | ---: |",
    ]
    for name in FINAL_CLASSES:
        lines.append(f"| `{name}` | {class_counts[name]} |")

    lines.extend(
        [
            "",
            "## Focused pytest outcomes",
            "",
            "| outcome | tests |",
            "| --- | ---: |",
        ]
    )
    for outcome, count in sorted(outcome_counts.items()):
        lines.append(f"| `{outcome}` | {count} |")

    lines.extend(
        [
            "",
            "## Contract-by-class matrix",
            "",
            "| contract | confirmed stale | current contract | historical compatibility | false positive | inconclusive |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for contract in sorted(contract_counts):
        counts = contract_counts[contract]
        lines.append(
            f"| `{contract}` | "
            f"{counts[CLASS_CONFIRMED_STALE]} | "
            f"{counts[CLASS_CURRENT_CONTRACT]} | "
            f"{counts[CLASS_HISTORICAL_COMPATIBILITY]} | "
            f"{counts[CLASS_FALSE_POSITIVE]} | "
            f"{counts[CLASS_INCONCLUSIVE]} |"
        )

    lines.extend(
        [
            "",
            "## R1 / R2 file coverage difference",
            "",
        ]
    )
    if coverage:
        for item in coverage:
            lines.append(
                f"- `{item.file}` — R1={item.in_r1}, R2={item.in_r2}, on_disk={item.on_disk}: {item.explanation}"
            )
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `confirmed_stale`: current code causes the selected test to fail with an assertion. This is evidence for an R2 repair candidate, not an instruction to delete the test.",
            "- `current_contract`: the high static rule was over-broad; the test passes and is on the current Phase 153-154 contract boundary.",
            "- `historical_compatibility`: the test passes and R1 intentionally classified it as compatibility coverage.",
            "- `false_positive`: the static rule fired, but current behavior satisfies the test and it is not otherwise identified as a current-contract or compatibility test.",
            "- `verification_inconclusive`: collection/setup/non-assertion failure or skip prevented proof of staleness.",
            "",
            "## R2B completion gate",
            "",
            "R2B is complete when every R2 high finding is mapped to a focused test outcome and only assertion-backed failures are carried forward as `confirmed_stale` repair candidates.",
            "No existing test is deleted or rewritten in R2B.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Phase 155-R2B focused verification of R2 high stale candidates."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--r2-findings",
        type=Path,
        default=Path("phase155_r2_audit_output/phase155_r2_expectation_findings.csv"),
    )
    parser.add_argument(
        "--r1-inventory",
        type=Path,
        default=Path("phase155_r1_audit_output/phase155_r1_test_inventory.csv"),
    )
    parser.add_argument(
        "--r2-file-summary",
        type=Path,
        default=Path("phase155_r2_audit_output/phase155_r2_file_summary.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("phase155_r2b_audit_output"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    r2_findings_path = (repo_root / args.r2_findings).resolve() if not args.r2_findings.is_absolute() else args.r2_findings
    r1_inventory_path = (repo_root / args.r1_inventory).resolve() if not args.r1_inventory.is_absolute() else args.r1_inventory
    r2_file_summary_path = (repo_root / args.r2_file_summary).resolve() if not args.r2_file_summary.is_absolute() else args.r2_file_summary
    output_dir = (repo_root / args.output_dir).resolve() if not args.output_dir.is_absolute() else args.output_dir

    for required in (r2_findings_path, r1_inventory_path, r2_file_summary_path):
        if not required.exists():
            raise SystemExit(f"required Phase 155 audit input not found: {required}")

    findings = load_r2_high_findings(r2_findings_path)
    if not findings:
        raise SystemExit("no stale_candidate_high findings found in the R2 CSV")

    output_dir.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    verified, executions, collection_errors, pytest_exit_code = verify_findings(
        repo_root,
        findings,
    )
    elapsed = time.perf_counter() - started

    coverage = compare_file_coverage(
        repo_root,
        r1_inventory_path,
        r2_file_summary_path,
    )

    _write_dataclass_csv(
        output_dir / "phase155_r2b_verified_findings.csv",
        verified,
    )
    _write_dataclass_csv(
        output_dir / "phase155_r2b_test_executions.csv",
        executions,
    )
    _write_dataclass_csv(
        output_dir / "phase155_r2b_file_coverage_difference.csv",
        coverage,
    )
    (output_dir / "phase155_r2b_collection_errors.txt").write_text(
        "\n\n".join(collection_errors) + ("\n" if collection_errors else ""),
        encoding="utf-8",
    )
    write_summary(
        output_dir / "phase155_r2b_summary.md",
        repo_root,
        findings,
        verified,
        executions,
        coverage,
        collection_errors,
        pytest_exit_code,
    )

    class_counts = Counter(item.verification_class for item in verified)
    metadata = {
        "git_head": _git_head(repo_root),
        "r2_high_findings": len(findings),
        "unique_focused_tests": len(executions),
        "pytest_exit_code": pytest_exit_code,
        "collection_errors": len(collection_errors),
        "verification_class_counts": dict(class_counts),
        "elapsed_seconds": round(elapsed, 3),
        "repository_wide_pytest_executed": False,
        "existing_tests_modified": False,
        "production_code_modified": False,
    }
    (output_dir / "phase155_r2b_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Phase 155-R2B stale candidate verification completed.")
    print(f"R2 high findings: {len(findings)}")
    print(f"unique focused tests executed: {len(executions)}")
    print(f"confirmed stale: {class_counts[CLASS_CONFIRMED_STALE]}")
    print(f"current contract: {class_counts[CLASS_CURRENT_CONTRACT]}")
    print(f"historical compatibility: {class_counts[CLASS_HISTORICAL_COMPATIBILITY]}")
    print(f"false positives: {class_counts[CLASS_FALSE_POSITIVE]}")
    print(f"inconclusive: {class_counts[CLASS_INCONCLUSIVE]}")
    print(f"R1/R2 file coverage differences: {len(coverage)}")
    print(f"output: {output_dir}")

    # A non-zero focused pytest exit code is expected if stale assertions are confirmed.
    # The audit itself succeeds if it completed and recorded the outcomes.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
