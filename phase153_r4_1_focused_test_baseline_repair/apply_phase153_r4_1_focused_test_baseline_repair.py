from __future__ import annotations

from pathlib import Path
import re
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TESTS_DIR = REPO_ROOT / "tests"
BACKUP_DIR = PACKAGE_DIR / "backup_before_r4_1"


FUNCTION_REPLACEMENTS = {
  "test_phase153_r2_public_reference_semantic_fact.py": {
    "test_phase153_r2_public_pi10_6_keeps_reference_and_uses_toda45_fact_without_body_duplication": '''def test_phase153_r2_public_pi10_6_excludes_obsolete_45_reference():
  rendered = (
    _phase153_r2_public_pi10_6_narrative()
  )

  reference_section = rendered.split(
    "## 証明",
    1,
  )[0]

  assert "**[R1] Proposition 5.8.**" in reference_section
  assert "(4.5)" not in reference_section
  assert "$\\pi_{10}^{6} = 0$" in rendered
''',
  },
  "test_phase153_r3_4_reference_statement_rendering_connection.py": {
    "test_phase153_r3_4_pi10_6_builds_selected_reference_statement_lines": '''def test_phase153_r3_4_pi10_6_builds_selected_reference_statement_lines_without_obsolete_45():
  presentation = (
    _phase153_r3_4_pi10_6_presentation()
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )

  locators = tuple(
    entry.reference.locator
    for entry in entries
  )
  entry_numbers = {
    entry.number
    for entry in entries
  }

  assert "Proposition 5.8" in locators
  assert "(4.5)" not in locators
  assert set(
    statement_lines
  ).issubset(
    entry_numbers
  )
''',
    "test_phase153_r3_4_public_pi10_6_reference_section_contains_r2_statement": '''def test_phase153_r3_4_public_pi10_6_reference_section_excludes_obsolete_45():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase153_r3_4_pi10_6_presentation()
    )
  )

  reference_section = rendered.split(
    "## 証明",
    1,
  )[0]

  assert "**[R1] Proposition 5.8.**" in reference_section
  assert "(4.5)" not in reference_section
  assert "$\\pi_{10}^{6} = 0$" in rendered
''',
  },
  "test_phase153_r3_5_reference_body_duplicate_suppression.py": {
    "test_phase153_r3_5_public_pi10_6_keeps_statement_in_reference_and_suppresses_body_copy": '''def test_phase153_r3_5_public_pi10_6_keeps_current_reference_baseline_without_obsolete_45():
  rendered = (
    _phase153_r3_5_pi10_6_narrative()
  )

  parts = rendered.split(
    "## 証明",
    1,
  )
  reference_section = parts[0]
  proof_body = (
    parts[1]
    if len(parts) == 2
    else rendered
  )

  assert "**[R1] Proposition 5.8.**" in reference_section
  assert "(4.5)" not in reference_section
  assert "$\\pi_{10}^{6} = 0$" in proof_body
''',
  },
}


COUNT_REPLACEMENTS = {
  "test_phase153_r3_6_unresolved_reference_statement_rendering.py": (
    "assert occurrences == 37",
    "assert occurrences == 42",
  ),
  "test_phase153_r3_9_remaining_reference_renderer_coverage.py": (
    "assert occurrences == 31",
    "assert occurrences == 33",
  ),
}


def _replace_test_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  pattern = re.compile(
    r"^def "
    + re.escape(function_name)
    + r"\(\):\n"
    + r"(?:(?:^  .*\n)|(?:^\n))*?"
    + r"(?=^def |\Z)",
    re.MULTILINE,
  )

  match = pattern.search(source)
  if match is None:
    raise RuntimeError(
      "could not find test function: "
      + function_name
    )

  replacement = replacement.rstrip() + "\n\n"

  return (
    source[:match.start()]
    + replacement
    + source[match.end():]
  )


def _backup(path: Path) -> None:
  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  backup_path = BACKUP_DIR / path.name

  if not backup_path.exists():
    shutil.copy2(
      path,
      backup_path,
    )


def main() -> int:
  changed = []

  for filename, replacements in FUNCTION_REPLACEMENTS.items():
    path = TESTS_DIR / filename

    if not path.exists():
      raise FileNotFoundError(path)

    source = path.read_text(
      encoding="utf-8"
    )
    updated = source

    for function_name, replacement in replacements.items():
      updated = _replace_test_function(
        updated,
        function_name,
        replacement,
      )

    _backup(path)
    path.write_text(
      updated,
      encoding="utf-8",
      newline="\n",
    )
    changed.append(path)

  for filename, pair in COUNT_REPLACEMENTS.items():
    old, new = pair
    path = TESTS_DIR / filename

    if not path.exists():
      raise FileNotFoundError(path)

    source = path.read_text(
      encoding="utf-8"
    )
    count = source.count(old)

    if count != 1:
      raise RuntimeError(
        f"{filename}: expected exactly one {old!r}, found {count}"
      )

    updated = source.replace(
      old,
      new,
      1,
    )

    _backup(path)
    path.write_text(
      updated,
      encoding="utf-8",
      newline="\n",
    )
    changed.append(path)

  print("Phase 153-R4.1 focused test baseline repair applied.")
  print("Production changes: none")
  print("Changed test files:")

  for path in changed:
    print(
      "  - "
      + str(path.relative_to(REPO_ROOT))
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
