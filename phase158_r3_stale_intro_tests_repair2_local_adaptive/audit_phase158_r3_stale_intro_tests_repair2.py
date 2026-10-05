from __future__ import annotations

from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parent.parent
INTRO = "使用する結果を先にまとめる."

TARGET_FILES = (
  "tests/test_phase132_7_group_proof_cli_modes.py",
  "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py",
  "tests/test_phase153_r3_4_reference_statement_rendering_connection.py",
  "tests/test_phase144_6_r3_production_references.py",
  "tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py",
  "tests/test_phase153_r11_generic_reference_attribution_filtering.py",
)


def main() -> int:
  findings = []

  positive_assertion_pattern = re.compile(
    r'(?m)^\s*assert "'
    + re.escape(
      INTRO
    )
    + r'" in '
  )

  legacy_expected_literal = (
    '"使用する結果を先にまとめる.\\n\\n"'
  )

  legacy_startswith_pattern = re.compile(
    r'\.startswith\(\s*"'
    + re.escape(
      INTRO
    )
    + r'"\s*\)',
    flags=re.MULTILINE,
  )

  for relative_path in TARGET_FILES:
    source = (
      REPO_ROOT
      / relative_path
    ).read_text(
      encoding="utf-8",
    )

    if positive_assertion_pattern.search(
      source
    ):
      findings.append(
        (
          relative_path,
          "positive assertion",
        )
      )

    if legacy_expected_literal in source:
      findings.append(
        (
          relative_path,
          "legacy exact output",
        )
      )

    if legacy_startswith_pattern.search(
      source
    ):
      findings.append(
        (
          relative_path,
          "legacy startswith",
        )
      )

  print(
    "=" * 78
  )
  print(
    "Phase 158-R3 stale intro contract audit"
  )
  print(
    "=" * 78
  )
  print(
    "target files: 6"
  )
  print(
    "remaining stale intro contracts: "
    + str(
      len(
        findings
      )
    )
  )

  for path, kind in findings:
    print(
      "  "
      + path
      + " — "
      + kind
    )

  print(
    "=" * 78
  )

  return (
    0
    if not findings
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
