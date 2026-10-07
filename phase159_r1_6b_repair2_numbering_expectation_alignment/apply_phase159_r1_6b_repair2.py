from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "tests" / "test_phase159_r1_2_pi3_2_narrative_repair.py"

REPLACEMENT_TEST = 'def test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically():\n  presentation = _phase159_r1_2_pi3_2_presentation()\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  injective = (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3} "\n    r"\\text{ は単射}. \\tag{1}$"\n  )\n  surjective = (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3} "\n    r"\\text{ は全射}. \\tag{2}$"\n  )\n  isomorphism = (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は同型."\n  )\n\n  assert injective in rendered\n  assert surjective in rendered\n  assert isomorphism in rendered\n\n  assert rendered.index(\n    injective\n  ) < rendered.index(\n    isomorphism\n  )\n  assert rendered.index(\n    surjective\n  ) < rendered.index(\n    isomorphism\n  )\n\n  assert (\n    r"\\tag{1}$ は単射."\n    not in rendered\n  )\n  assert (\n    r"\\tag{2}$ は全射."\n    not in rendered\n  )\n\n  assert (\n    "(1), (2) より, "\n    + isomorphism\n    in rendered\n  )\n'

def replace_test_function(
  source,
  function_name,
  replacement,
):
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      "test function not found: "
      + function_name
    )

  next_function = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  end = (
    len(
      source
    )
    if next_function < 0
    else next_function + 1
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n"
    + source[end:]
  )

def main():
  if not TEST.exists():
    raise FileNotFoundError(
      TEST
    )

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_6b_repair2_backup_"
      + stamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TEST,
    backup_dir / TEST.name,
  )

  source = TEST.read_text(
    encoding="utf-8-sig"
  )

  source = replace_test_function(
    source,
    "test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically",
    REPLACEMENT_TEST,
  )

  TEST.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6b repair2 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Production code changes: none"
  )
  print(
    "Aligned stale R1-4 numbering expectation "
    "with the R1-6b full-statement tag contract."
  )

if __name__ == "__main__":
  main()
