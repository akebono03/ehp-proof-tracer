from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
R19_TEST = ROOT / "tests" / "test_phase157_r19_pi6_3_reference_dependency_restoration.py"
R3_TEST = ROOT / "tests" / "test_phase157_r3_pi6_3_reference_boundary.py"

R19_TEST_FUNCTION = 'def test_phase157_r19_pi6_3_has_five_named_public_references():\n  reference, _ = _reference_and_body()\n\n  assert "**[R1] Proposition 5.6.**" in reference\n  assert "**[R2] (5.3).**" in reference\n  assert "**[R3] Proposition 5.3.**" in reference\n  assert "**[R4] Proposition 5.1.**" in reference\n  assert "**[R5] Proposition 2.2.**" in reference\n\n  assert (\n    r"$\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$."\n    in reference\n  )\n  assert (\n    r"$\\nu\' \\in \\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}$ とする."\n    in reference\n  )\n  assert (\n    r"$\\nu\' \\in \\pi_{6}^{3}$."\n    in reference\n  )\n  assert (\n    r"$2\\nu\' = \\eta_{3}^{3}$."\n    in reference\n  )\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n    in reference\n  )\n  assert (\n    r"$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n    in reference\n  )\n  assert (\n    r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$."\n    in reference\n  )\n  assert (\n    r"$H(\\alpha\\circ E\\beta) = H(\\alpha)\\circ E\\beta$."\n    in reference\n  )\n'
R3_UNTRACKED_FUNCTION = 'def test_phase157_r3_pi6_3_reference_excludes_untracked_proof_machinery():\n  reference, _ = _reference_and_body(\n    _render_pi6_3(3)\n  )\n\n  assert "(5.2)" not in reference\n  assert "Lemma 5.4" not in reference\n  assert "Lemma 5.2" not in reference\n  assert (\n    r"\\nu\' \\in \\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"\n    in reference\n  )\n'
R3_BRACKET_FUNCTION = 'def test_phase157_r3_pi6_3_preserves_bracket_definition_but_hides_internal_machinery():\n  reference, body = _reference_and_body(\n    _render_pi6_3(3)\n  )\n\n  bracket_definition = (\n    r"\\nu\' \\in \\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"\n  )\n\n  assert bracket_definition in reference\n  assert bracket_definition not in body\n  assert "Lemma 5.2" not in reference\n  assert "Lemma 5.2" not in body\n'


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  marker = f"def {name}("
  start = source.find(marker)

  if start < 0:
    raise RuntimeError(
      f"function not found: {name}"
    )

  next_match = re.search(
    r"^def [A-Za-z_][A-Za-z0-9_]*\(",
    source[start + len(marker):],
    flags=re.MULTILINE,
  )

  if next_match is None:
    end = len(source)
  else:
    end = (
      start
      + len(marker)
      + next_match.start()
    )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def main() -> None:
  for path in (
    PRODUCTION,
    R19_TEST,
    R3_TEST,
  ):
    if not path.is_file():
      raise RuntimeError(
        f"missing file: {path}"
      )

  production = PRODUCTION.read_text(
    encoding="utf-8"
  )
  r19_test = R19_TEST.read_text(
    encoding="utf-8"
  )
  r3_test = R3_TEST.read_text(
    encoding="utf-8"
  )

  old_r2_lines = """    2: (
      r"$\\nu' \\in \\pi_{6}^{3}$.",
      r"$2\\nu' = \\eta_{3}^{3}$.",
      r"$H\\left(\\nu'\\right) = \\eta_{5}$.",
    ),
"""

  new_r2_lines = """    2: (
      (
        r"$\\nu' \\in "
        r"\\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}$ とする."
      ),
      r"$\\nu' \\in \\pi_{6}^{3}$.",
      r"$2\\nu' = \\eta_{3}^{3}$.",
      r"$H\\left(\\nu'\\right) = \\eta_{5}$.",
    ),
"""

  if old_r2_lines not in production:
    raise RuntimeError(
      "repair9 expects the repair6/repair8 R19 finalizer state"
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair9_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    PRODUCTION,
    R19_TEST,
    R3_TEST,
  ):
    shutil.copy2(
      path,
      backup / path.name,
    )

  production = production.replace(
    old_r2_lines,
    new_r2_lines,
    1,
  )

  r19_test = replace_function(
    r19_test,
    "test_phase157_r19_pi6_3_has_five_named_public_references",
    R19_TEST_FUNCTION,
  )

  r3_test = replace_function(
    r3_test,
    "test_phase157_r3_pi6_3_reference_excludes_untracked_proof_machinery",
    R3_UNTRACKED_FUNCTION,
  )

  r3_test = replace_function(
    r3_test,
    "test_phase157_r3_pi6_3_preserves_phase156_bracket_boundary_collapse",
    R3_BRACKET_FUNCTION,
  )

  compile(
    production,
    str(PRODUCTION),
    "exec",
  )
  compile(
    r19_test,
    str(R19_TEST),
    "exec",
  )
  compile(
    r3_test,
    str(R3_TEST),
    "exec",
  )

  PRODUCTION.write_text(
    production,
    encoding="utf-8",
    newline="\n",
  )
  R19_TEST.write_text(
    r19_test,
    encoding="utf-8",
    newline="\n",
  )
  R3_TEST.write_text(
    r3_test,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R19 repair9 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {PRODUCTION}")
  print(f"  {R19_TEST}")
  print(f"  {R3_TEST}")


if __name__ == "__main__":
  main()
