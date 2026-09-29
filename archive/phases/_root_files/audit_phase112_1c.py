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
_OUTPUT_DIR = _REPO_ROOT / "phase112_1c_audit_output"


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
            "audit_phase112_1c.py there.",
            file=sys.stderr,
        )
        return 2

    _OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    cases = (
        AuditCase(
            name="01_known_group_pi18_11",
            args=("11", "7"),
            category="baseline",
        ),
        AuditCase(
            name="02_show_proof_sigma11_depth1",
            args=("show-proof", "sigma_11"),
            category="baseline",
        ),
        AuditCase(
            name="03_show_proof_sigma11_depth2",
            args=("show-proof", "sigma_11", "--depth", "2"),
            category="baseline",
        ),
        AuditCase(
            name="04_explore_proof_sigma11",
            args=("explore-proof", "sigma_11"),
            category="baseline",
        ),
        AuditCase(
            name="05_explore_applicable_sigma11",
            args=("explore-applicable", "sigma_11"),
            category="baseline",
        ),
        AuditCase(
            name="06_execute_sigma11",
            args=("execute", "sigma_11"),
            category="expected_boundary",
            expected_returncodes=(1,),
        ),
        AuditCase(
            name="07_pressure_query_E_sigma11",
            args=("query", "E(sigma_11)"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="08_pressure_query_H_sigma11",
            args=("query", "H(sigma_11)"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="09_pressure_query_Delta_sigma11",
            args=("query", "Delta(sigma_11)"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="10_pressure_query_sigma11_eta18",
            args=("query", "sigma_11 o eta_18"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="11_pressure_query_eta11_sigma12",
            args=("query", "eta_11 o sigma_12"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="12_pressure_E_sigma11_eta18",
            args=("query", "E(sigma_11 o eta_18)"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="13_pressure_three_term_sigma_continuation",
            args=("query", "sigma_11 o eta_18 o eta_19"),
            category="pressure",
            expected_returncodes=(0, 1),
        ),
        AuditCase(
            name="14_pressure_E_three_term_sigma_continuation",
            args=("query", "E(sigma_11 o eta_18 o eta_19)"),
            category="pressure",
            expected_returncodes=(0, 1, 2),
        ),
    )

    rows = []
    baseline_failure = False
    expected_boundary_failure = False

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

        if (
            case.category == "expected_boundary"
            and result.returncode not in case.expected_returncodes
        ):
            expected_boundary_failure = True

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
        "# Phase 112-1C sigma_11 end-to-end mathematical workflow audit",
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
            "- `NO_EXECUTABLE_TARGET`: current qualified execution workflow has no executable target for the generator.",
            "- `PARSER_OR_ARGUMENT_BOUNDARY`: current CLI syntax or argument boundary rejected the request.",
            "- `EXPECTED_NONZERO`: a nonzero result explicitly allowed for an observational/pressure probe.",
            "- `UNEXPECTED_FAILURE`: behavior outside the audit expectation.",
            "",
            "## Mathematical path under audit",
            "",
            "The intended path is:",
            "",
            "pi_18^11 = Z/16{sigma_11}",
            "-> generic sigma specialization proof replay",
            "-> recursive proof-scope exploration",
            "-> applicable theorem discovery",
            "-> qualified execution boundary",
            "-> E / H / Delta lookup pressure",
            "-> nearby sigma-eta composition lookup pressure.",
            "",
            "## Important expected boundary",
            "",
            "`execute sigma_11` is expected to return no executable target in the current implementation.",
            "That behavior is already covered by an existing production test and is not classified as a regression here.",
            "",
            "## Phase 112-1C boundary",
            "",
            "Do not implement an evaluator, new inference rule, or broader parser from this audit alone.",
            "Compare repeated pressure across Phase 112-1A, 112-1B, and 112-1C before Phase 112-2 classification.",
            "",
        ]
    )

    summary_path = (
        _OUTPUT_DIR
        / "phase112_1c_summary.md"
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

    if baseline_failure or expected_boundary_failure:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
