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
_OUTPUT_DIR = _REPO_ROOT / "phase112_1b_audit_output"


def _run(
    case: AuditCase,
) -> tuple[subprocess.CompletedProcess[str], str]:
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
        and "No directly renderable repository fact found for"
        in result.stdout
    ):
        return "PRESENTATION_GAP"

    if (
        result.returncode == 1
        and "No executable target found for" in result.stdout
    ):
        return "NO_EXECUTABLE_TARGET"

    if result.returncode == 2:
        return "PARSER_OR_ARGUMENT_BOUNDARY"

    if result.returncode in case.expected_returncodes:
        return "EXPECTED_NONZERO"

    return "UNEXPECTED_FAILURE"


def main() -> int:
    if not (_REPO_ROOT / "main.py").exists():
        print(
            "Run this script from the repository root after copying "
            "audit_phase112_1b.py there.",
            file=sys.stderr,
        )
        return 2

    _OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    cases = (
        AuditCase(
            name="01_known_group_pi8_5",
            args=("5", "3"),
            category="baseline",
        ),
        AuditCase(
            name="02_show_proof_nu5_depth3",
            args=("show-proof", "nu_5", "--depth", "3"),
            category="baseline",
        ),
        AuditCase(
            name="03_query_Delta_nu5",
            args=("query", "Delta(nu_5)"),
            category="baseline",
        ),
        AuditCase(
            name="04_query_proof_Delta_nu5",
            args=(
                "query-proof",
                "Delta(nu_5)",
                "--depth",
                "3",
            ),
            category="baseline",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="05_query_nu5_eta8",
            args=("query", "nu_5 o eta_8"),
            category="baseline",
        ),
        AuditCase(
            name="06_query_nu5_eta8_eta9",
            args=("query", "nu_5 o eta_8 o eta_9"),
            category="baseline",
        ),
        AuditCase(
            name="07_query_nu5_nu8",
            args=("query", "nu_5 o nu_8"),
            category="baseline",
        ),
        AuditCase(
            name="08_explore_applicable_nu5",
            args=("explore-applicable", "nu_5"),
            category="baseline",
        ),
        AuditCase(
            name="09_execute_nu5",
            args=("execute", "nu_5"),
            category="observation",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="10_pressure_query_E_nu5",
            args=("query", "E(nu_5)"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="11_pressure_query_H_nu5",
            args=("query", "H(nu_5)"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="12_pressure_E_nu5_eta8",
            args=("query", "E(nu_5 o eta_8)"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="13_pressure_E_three_term_nu5_eta8_eta9",
            args=("query", "E(nu_5 o eta_8 o eta_9)"),
            category="pressure",
            expected_returncodes=(0, 1, 2),
        ),
        AuditCase(
            name="14_pressure_four_term_continuation",
            args=("query", "nu_5 o eta_8 o eta_9 o eta_10"),
            category="pressure",
            expected_returncodes=(0, 1, 2),
        ),
    )

    rows = []
    baseline_failure = False

    for case in cases:
        result, command = _run(
            case
        )
        classification = _classify_result(
            case,
            result,
        )

        if (
            case.category == "baseline"
            and result.returncode not in case.expected_returncodes
        ):
            baseline_failure = True

        stdout_path = (
            _OUTPUT_DIR
            / f"{case.name}.stdout.txt"
        )
        stderr_path = (
            _OUTPUT_DIR
            / f"{case.name}.stderr.txt"
        )

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
        "# Phase 112-1B nu_5 end-to-end mathematical workflow audit",
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
            "- `NO_EXECUTABLE_TARGET`: generator workflow found no currently executable qualified target.",
            "- `PARSER_OR_ARGUMENT_BOUNDARY`: current CLI syntax or argument boundary rejected the request.",
            "- `EXPECTED_NONZERO`: a nonzero result explicitly allowed for an observational/pressure probe.",
            "- `UNEXPECTED_FAILURE`: behavior outside the audit expectation.",
            "",
            "## Mathematical path under audit",
            "",
            "The intended path is:",
            "",
            "pi_8^5 = Z/8{nu_5}",
            "-> proof replay",
            "-> Delta(nu_5)",
            "-> nu_5 eta_8",
            "-> nu_5 eta_8^2",
            "-> nu_5^2",
            "-> applicable theorem discovery",
            "-> execution availability",
            "-> nearby operation pressure probes.",
            "",
            "## Phase 112-1B boundary",
            "",
            "Do not implement parser, evaluator, lookup, or inference changes from a single miss.",
            "Use this report together with Phase 112-1A and the later sigma_11 audit to identify repeated pressure.",
            "",
        ]
    )

    summary_path = (
        _OUTPUT_DIR
        / "phase112_1b_summary.md"
    )
    summary_path.write_text(
        "\n".join(
            summary_lines
        ),
        encoding="utf-8",
    )

    print()
    print(
        "Summary:",
        summary_path,
    )

    return (
        1
        if baseline_failure
        else 0
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
