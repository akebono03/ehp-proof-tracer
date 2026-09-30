from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path.cwd()
OUT = ROOT / "phase150_finalization_repair_r1" / "local_snapshot"

FILES = (
    "toda_group_proof_narrative_renderer.py",
    "toda_group_proof_narrative_references.py",
    "toda_group_proof_narrative_argument_multi_renderer.py",
    "toda_group_proof_narrative_contribution_renderer.py",
    "tests/test_phase132_6_group_proof_narrative_renderer.py",
    "tests/test_phase132_7_group_proof_cli_modes.py",
    "tests/test_phase132_8_group_proof_narrative_dedup.py",
    "tests/test_phase132_9_web_group_proof_modes.py",
    "tests/test_phase133_10_sigma_label_wording.py",
    "tests/test_phase133_6_group_proof_narrative_labels.py",
    "tests/test_phase133_9_group_proof_narrative_labels.py",
    "tests/test_phase144_6_r3_production_references.py",
    "tests/test_phase144_6_r3_structured_references.py",
    "tests/test_phase144_6_r4_supporting_fact_filtering.py",
)

FOCUSED_TESTS = (
    "tests/test_phase132_6_group_proof_narrative_renderer.py",
    "tests/test_phase132_7_group_proof_cli_modes.py",
    "tests/test_phase132_8_group_proof_narrative_dedup.py",
    "tests/test_phase132_9_web_group_proof_modes.py",
    "tests/test_phase133_10_sigma_label_wording.py",
    "tests/test_phase133_6_group_proof_narrative_labels.py",
    "tests/test_phase133_9_group_proof_narrative_labels.py",
    "tests/test_phase144_6_r3_production_references.py",
    "tests/test_phase144_6_r3_structured_references.py",
    "tests/test_phase144_6_r4_supporting_fact_filtering.py",
)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    missing = []
    copied = []
    for relative in FILES:
        source = ROOT / relative
        if not source.exists():
            missing.append(relative)
            continue
        destination = OUT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append(relative)

    report = [
        "Phase 150 Finalization Repair R1 local snapshot",
        "",
        "Production changes: none",
        "Existing test changes: none",
        "Full regression: not run",
        "",
        "Copied files:",
        *[f"- {name}" for name in copied],
    ]
    if missing:
        report.extend(("", "Missing files:", *[f"- {name}" for name in missing]))

    command = [sys.executable, "-m", "pytest", *FOCUSED_TESTS, "-q"]
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    test_output = result.stdout
    (OUT / "focused_pytest.txt").write_text(test_output, encoding="utf-8")
    report.extend((
        "",
        "Focused pytest exit code: " + str(result.returncode),
        "Focused pytest command:",
        "  " + " ".join(command),
        "",
        "Focused pytest tail:",
        *test_output.splitlines()[-80:],
    ))
    (OUT / "REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")

    print("Local snapshot written to:")
    print(OUT)
    print()
    print("Focused pytest exit code:", result.returncode)
    print("This R1 audit intentionally makes no production/test changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
