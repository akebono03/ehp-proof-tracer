from __future__ import annotations

from pathlib import Path


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
  remaining = []

  for relative_path in TARGET_FILES:
    source = (
      REPO_ROOT
      / relative_path
    ).read_text(
      encoding="utf-8",
    )

    if (
      f'assert "{INTRO}" in '
      in source
    ):
      remaining.append(
        relative_path
      )

    if (
      f'"{INTRO}\\n\\n"'
      in source
    ):
      remaining.append(
        relative_path
      )

  print(
    "=" * 78
  )
  print(
    "Phase 158-R3 stale intro test contract audit"
  )
  print(
    "=" * 78
  )
  print(
    "target files: 6"
  )
  print(
    "remaining positive intro expectations: "
    + str(
      len(
        set(
          remaining
        )
      )
    )
  )
  print(
    "=" * 78
  )

  return (
    0
    if not remaining
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
