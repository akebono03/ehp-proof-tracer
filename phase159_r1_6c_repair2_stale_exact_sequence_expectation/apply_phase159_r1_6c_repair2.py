from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_2_pi3_2_narrative_repair.py"
)

REPLACEMENT = 'def test_phase159_r1_4_pi3_2_public_uses_exactly_one_exact_sequence():\n  presentation = _phase159_r1_2_pi3_2_presentation()\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  long_exact = (\n    r"$\\pi_{2}^{1} \\xrightarrow{E} "\n    r"\\pi_{3}^{2} \\xrightarrow{H} "\n    r"\\pi_{3}^{3} \\xrightarrow{\\Delta} "\n    r"\\pi_{1}^{1} \\xrightarrow{E} "\n    r"\\pi_{2}^{2}$."\n  )\n\n  proof_body = rendered.split(\n    "## 証明\\n\\n",\n    1,\n  )[1]\n\n  exactness_lines = tuple(\n    line\n    for line in proof_body.splitlines()\n    if r"\\xrightarrow{" in line\n  )\n\n  assert exactness_lines == (\n    long_exact,\n  )\n  assert "は完全である." not in proof_body\n'


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
      "phase159_r1_6c_repair2_backup_"
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
    "test_phase159_r1_4_pi3_2_public_uses_exactly_one_exact_sequence",
    REPLACEMENT,
  )

  TEST.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6c repair2 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Production code changes: none"
  )
  print(
    "Aligned stale exact-sequence expectation "
    "with the R1-6c no-redundant-exactness contract."
  )


if __name__ == "__main__":
  main()
