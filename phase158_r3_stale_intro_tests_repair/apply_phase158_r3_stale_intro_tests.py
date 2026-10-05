from __future__ import annotations

from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = (
  REPO_ROOT
  / "phase158_r3_stale_intro_tests_backup"
)

REPLACEMENTS = {
  "tests/test_phase132_7_group_proof_cli_modes.py": (
    (
      '  assert "使用する結果を先にまとめる." in captured.out\n',
      (
        '  assert "## 使用する結果" in captured.out\n'
        '  assert "使用する結果を先にまとめる." not in captured.out\n'
      ),
      2,
    ),
  ),
  "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py": (
    (
      '  assert "使用する結果を先にまとめる." in rendered\n',
      (
        '  assert "## 使用する結果" in rendered\n'
        '  assert "使用する結果を先にまとめる." not in rendered\n'
      ),
      3,
    ),
  ),
  "tests/test_phase153_r3_4_reference_statement_rendering_connection.py": (
    (
      '  assert legacy == (\n'
      '    "使用する結果を先にまとめる.\\n\\n"\n'
      '    "**[R1] Proposition X.**"\n'
      '  )\n'
      '  assert connected == (\n'
      '    "使用する結果を先にまとめる.\\n\\n"\n'
      '    "**[R1] Proposition X.**\\n"\n'
      '    "$A = B$"\n'
      '  )\n',
      (
        '  assert legacy == (\n'
        '    "**[R1] Proposition X.**"\n'
        '  )\n'
        '  assert connected == (\n'
        '    "**[R1] Proposition X.**\\n"\n'
        '    "$A = B$"\n'
        '  )\n'
      ),
      1,
    ),
  ),
  "tests/test_phase144_6_r3_production_references.py": (
    (
      '  assert "使用する結果を先にまとめる." in rendered\n',
      (
        '  assert "使用する結果を先にまとめる." not in rendered\n'
        '  assert rendered.startswith("**[R1] ")\n'
      ),
      1,
    ),
  ),
  "tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py": (
    (
      '  assert rendered.startswith(\n'
      '    "使用する結果を先にまとめる."\n'
      '  )\n',
      (
        '  assert rendered.startswith(\n'
        '    "**[R1] "\n'
        '  )\n'
        '  assert "使用する結果を先にまとめる." not in rendered\n'
      ),
      1,
    ),
  ),
  "tests/test_phase153_r11_generic_reference_attribution_filtering.py": (
    (
      '  assert "使用する結果を先にまとめる." in reference_part\n',
      (
        '  assert "使用する結果を先にまとめる." not in reference_part\n'
        '  assert "[R1]" in reference_part\n'
      ),
      1,
    ),
  ),
}


def main() -> int:
  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  changed_files = []

  for relative_path, replacements in REPLACEMENTS.items():
    target = (
      REPO_ROOT
      / relative_path
    )

    if not target.exists():
      raise RuntimeError(
        "Missing test file: "
        + str(
          target
        )
      )

    source = target.read_text(
      encoding="utf-8",
    )
    original_source = source

    for old, new, expected_count in replacements:
      actual_count = source.count(
        old
      )

      if actual_count != expected_count:
        raise RuntimeError(
          f"{relative_path}: expected {expected_count} occurrence(s), "
          f"found {actual_count}"
        )

      source = source.replace(
        old,
        new,
        expected_count,
      )

    backup = (
      BACKUP_DIR
      / relative_path
    )
    backup.parent.mkdir(
      parents=True,
      exist_ok=True,
    )

    if not backup.exists():
      shutil.copy2(
        target,
        backup,
      )

    target.write_text(
      source,
      encoding="utf-8",
    )

    compile(
      source,
      str(
        target
      ),
      "exec",
    )

    if source != original_source:
      changed_files.append(
        relative_path
      )

  print(
    "Phase 158-R3 stale intro test repair applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Changed test files:"
  )

  for path in changed_files:
    print(
      "  "
      + path
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
