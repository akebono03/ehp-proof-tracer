from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys


@dataclass(frozen=True)
class AuditCase:
    name: str
    args: tuple[str, ...]
    category: str
    expected_returncodes: tuple[int, ...] = (0,)


_REPO_ROOT = Path(__file__).resolve().parent
_OUTPUT_DIR = _REPO_ROOT / "phase112_1a_audit_output"


def _run(case: AuditCase) -> tuple[subprocess.CompletedProcess[str], str]:
    command = [
        sys.executable,
        "main.py",
        *case.args,
    ]

    result = subprocess.run(
        command,
        cwd=_REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=False,
    )

    rendered_command = " ".join(
        [
            "python",
            "main.py",
            *(
                f'"{arg}"'
                if " " in arg
                else arg
                for arg in case.args
            ),
        ]
    )

    return result, rendered_command


def _classify_result(
    case: AuditCase,
    result: subprocess.CompletedProcess[str],
) -> str:
    if result.returncode == 0:
        return "PASS"

    if (
        result.returncode == 1
        and "No known repository fact found for" in result.stdout
    ):
        return "LOOKUP_MISS"

    if (
        result.returncode == 1
        and "No directly renderable repository fact found for" in result.stdout
    ):
        return "PRESENTATION_GAP"

    if result.returncode == 2:
        return "PARSER_OR_ARGUMENT_BOUNDARY"

    if result.returncode in case.expected_returncodes:
        return "EXPECTED_NONZERO"

    return "UNEXPECTED_FAILURE"


def main() -> int:
    if not (_REPO_ROOT / "main.py").exists():
        print(
            "Run this script from the repository root after copying "
            "audit_phase112_1a.py there.",
            file=sys.stderr,
        )
        return 2

    _OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    cases = (
        AuditCase(
            name="01_known_group_pi6_3",
            args=("3", "3"),
            category="baseline",
        ),
        AuditCase(
            name="02_show_proof_nu_prime_depth3",
            args=("show-proof", "nu_prime", "--depth", "3"),
            category="baseline",
        ),
        AuditCase(
            name="03_query_H_nu_prime",
            args=("query", "H(nu_prime)"),
            category="baseline",
        ),
        AuditCase(
            name="04_query_proof_H_nu_prime_fact1",
            args=(
                "query-proof",
                "H(nu_prime)",
                "--fact",
                "1",
                "--depth",
                "3",
            ),
            category="baseline",
        ),
        AuditCase(
            name="05_query_proof_H_nu_prime_fact2",
            args=(
                "query-proof",
                "H(nu_prime)",
                "--fact",
                "2",
                "--depth",
                "3",
            ),
            category="baseline",
        ),
        AuditCase(
            name="06_query_E_eta2_nu_prime",
            args=("query", "E(eta_2 o nu_prime)"),
            category="baseline",
        ),
        AuditCase(
            name="07_query_proof_E_eta2_nu_prime",
            args=(
                "query-proof",
                "E(eta_2 o nu_prime)",
                "--depth",
                "3",
            ),
            category="baseline",
        ),
        AuditCase(
            name="08_query_eta2_nu_prime",
            args=("query", "eta_2 o nu_prime"),
            category="baseline",
        ),
        AuditCase(
            name="09_query_eta2_nu_prime_eta6",
            args=("query", "eta_2 o nu_prime o eta_6"),
            category="baseline",
        ),
        AuditCase(
            name="10_explore_applicable_nu_prime",
            args=("explore-applicable", "nu_prime"),
            category="baseline",
        ),
        AuditCase(
            name="11_execute_nu_prime_candidates",
            args=("execute", "nu_prime"),
            category="baseline",
        ),
        AuditCase(
            name="12_execute_nu_prime_candidate1",
            args=("execute", "nu_prime", "--candidate", "1"),
            category="baseline",
        ),
        AuditCase(
            name="13_execute_nu_prime_candidate2",
            args=("execute", "nu_prime", "--candidate", "2"),
            category="baseline",
        ),
        AuditCase(
            name="14_pressure_query_E_nu_prime",
            args=("query", "E(nu_prime)"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="15_pressure_query_Delta_nu_prime",
            args=("query", "Delta(nu_prime)"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="16_pressure_E_three_term_composition",
            args=("query", "E(eta_2 o nu_prime o eta_6)"),
            category="pressure",
            expected_returncodes=(0, 1, 2),
        ),
    )

    rows = []
    baseline_failure = False

    for case in cases:
        result, command = _run(case)
        classification = _classify_result(
            case,
            result,
        )

        if (
            case.category == "baseline"
            and result.returncode not in case.expected_returncodes
        ):
            baseline_failure = True

        stdout_path = _OUTPUT_DIR / f"{case.name}.stdout.txt"
        stderr_path = _OUTPUT_DIR / f"{case.name}.stderr.txt"

        stdout_path.write_text(
            result.stdout,
            encoding="utf-8",
        )
        stderr_path.write_text(
            result.stderr,
            encoding="utf-8",
        )

        rows.append(
            (
                case,
                command,
                result.returncode,
                classification,
            )
        )

        print(
            f"[{classification}] {case.name}: "
            f"returncode={result.returncode}"
        )

    summary_lines = [
        "# Phase 112-1A nu_prime end-to-end mathematical workflow audit",
        "",
        "This report is observational. It does not change repository code.",
        "",
        "## Results",
        "",
        "| # | Category | Case | Return code | Classification | Command |",
        "|---:|---|---|---:|---|---|",
    ]

    for index, (
        case,
        command,
        returncode,
        classification,
    ) in enumerate(
        rows,
        start=1,
    ):
        summary_lines.append(
            "| "
            f"{index} | {case.category} | `{case.name}` | "
            f"{returncode} | `{classification}` | `{command}` |"
        )

    summary_lines.extend(
        [
            "",
            "## Interpretation guide",
            "",
            "- `PASS`: current CLI completed the requested step.",
            "- `LOOKUP_MISS`: syntax was accepted, but no existing repository fact was found.",
            "- `PRESENTATION_GAP`: lookup found something but the user-facing presentation could not render it directly.",
            "- `PARSER_OR_ARGUMENT_BOUNDARY`: the current CLI syntax or argument boundary rejected the request.",
            "- `EXPECTED_NONZERO`: a nonzero result explicitly allowed for a pressure probe.",
            "- `UNEXPECTED_FAILURE`: behavior outside the audit expectation.",
            "",
            "## Phase 112-1A boundary",
            "",
            "Baseline cases test the already-supported nu_prime workflow.",
            "Pressure cases intentionally ask the next nearby mathematical questions.",
            "Do not implement a fix from this report alone; classify the observed pressure "
            "in Phase 112-2 before choosing lookup, orchestration, inference, evaluator, "
            "or parser work.",
            "",
        ]
    )

    summary_path = _OUTPUT_DIR / "phase112_1a_summary.md"
    summary_path.write_text(
        "\n".join(summary_lines),
        encoding="utf-8",
    )

    print()
    print(
        "Summary:",
        summary_path,
    )

    return 1 if baseline_failure else 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
