from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase157_r5_r6_53_bracket_definition_reference.py"
)
BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"

FUNCTION_NAME = (
  "test_phase157_r5_r6_pi6_reference_53_displays_bracket_definition"
)

NEW_FUNCTION = r'''def test_phase157_r5_r6_pi6_reference_53_displays_bracket_definition():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi6_3_presentation()
    )
  )
  reference_part = (
    rendered.split(
      "---\n\n## 証明",
      1,
    )[
      0
    ]
  )

  assert (
    re.search(
      r"\*\*\[R\d+\] \(5\.3\)\.\*\*",
      reference_part,
    )
    is not None
  )
  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    in reference_part
    or
    r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}"
    in reference_part
  )
'''


def extract_function(
  text: str,
  function_name: str,
) -> str:
  marker = "def " + function_name + "("
  start = text.find(marker)

  if start < 0:
    raise RuntimeError(
      "function not found: " + function_name
    )

  next_function = text.find(
    "\ndef ",
    start + len(marker),
  )

  if next_function < 0:
    return text[start:]

  return text[start:next_function + 1]


def main() -> None:
  if not TARGET.exists():
    raise FileNotFoundError(
      f"test file not found: {TARGET}"
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  if not source.startswith(
    "import re\n"
  ):
    raise RuntimeError(
      "repair4 repair1 is expected to have added import re"
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  backup = BACKUP_DIR / TARGET.name

  if not backup.exists():
    shutil.copy2(
      TARGET,
      backup,
    )

  current_function = extract_function(
    source,
    FUNCTION_NAME,
  )

  source = source.replace(
    current_function,
    NEW_FUNCTION.rstrip() + "\n",
    1,
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
  )

  print(
    "Phase 159 R1-7c R3 repair4 repair3 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Updated test:",
    TARGET,
  )
  print(
    "Current contract: (5.3) title, arbitrary [Rk] number."
  )


if __name__ == "__main__":
  main()
