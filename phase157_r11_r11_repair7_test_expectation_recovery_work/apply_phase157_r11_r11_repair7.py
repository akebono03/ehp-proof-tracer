from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_repair7"
BACKUP.mkdir(exist_ok=True)

TEST_PATH = (
  ROOT
  / "tests"
  / "test_phase157_r5_r9_fixed_definition_body_suppression.py"
)


def backup(path: Path) -> None:
  destination = BACKUP / path.name

  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


def replace_test_function() -> None:
  text = TEST_PATH.read_text(
    encoding="utf-8"
  )

  function_name = (
    "def "
    "test_phase157_r5_r9_fixed_definition_remains_in_reference"
    "():"
  )

  start = text.find(
    function_name
  )

  if start < 0:
    raise RuntimeError(
      "could not locate fixed-definition Reference test function"
    )

  next_def = text.find(
    "\ndef ",
    start + len(
      function_name
    ),
  )

  if next_def < 0:
    end = len(
      text
    )
  else:
    end = next_def + 1

  replacement = r'''def test_phase157_r5_r9_fixed_definition_remains_in_reference():
  rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "まず",
    1,
  )[
    0
  ]

  assert (
    (
      r"$\nu' \in "
      r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$"
      " とすると,"
    )
    in reference_part
  )
  assert (
    r"$\nu' \in \pi_{6}^{3}$."
    in reference_part
  )
  assert (
    (
      r"$2\nu' = "
      r"\eta_{3}\eta_{4}\eta_{5}$."
    )
    in reference_part
  )
'''

  updated = (
    text[
      :start
    ]
    + replacement
    + text[
      end:
    ]
  )

  TEST_PATH.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Updated: "
    "test_phase157_r5_r9_fixed_definition_remains_in_reference"
  )
  print(
    "Expectation: membership Reference line ends with period"
  )


backup(
  TEST_PATH
)
replace_test_function()

print("")
print("Phase157 R11-R11 repair7 applied successfully.")
