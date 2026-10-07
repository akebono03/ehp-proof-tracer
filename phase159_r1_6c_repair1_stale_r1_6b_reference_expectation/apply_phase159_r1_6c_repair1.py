from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_6b_toda51_attribution.py"
)

REPLACEMENT = 'def test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry():\n  presentation = (\n    _phase159_r1_6b_pi3_2_presentation()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n  reference_section = (\n    rendered.split(\n      "## 使用する結果\\n\\n",\n      1,\n    )[1].split(\n      "\\n---\\n",\n      1,\n    )[0]\n  )\n\n  assert (\n    reference_section.count(\n      "**[R1] (5.1).**"\n    )\n    == 1\n  )\n  assert "[F1]" not in reference_section\n  assert "[F2]" not in reference_section\n  assert "[F3]" not in reference_section\n\n  assert (\n    r"\\pi_{3}^{2} = "\n    r"\\mathbb{Z}\\{\\eta_{2}\\}"\n    not in reference_section\n  )\n  assert (\n    "Proposition 5.1"\n    not in reference_section\n  )\n'


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
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


def main() -> None:
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
      "phase159_r1_6c_repair1_backup_"
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

  source = replace_function(
    source,
    "test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry",
    REPLACEMENT,
  )

  TEST.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6c repair1 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Production code changes: none"
  )
  print(
    "Aligned stale R1-6b Reference expectation "
    "with the R1-6c source-faithful contract."
  )


if __name__ == "__main__":
  main()
