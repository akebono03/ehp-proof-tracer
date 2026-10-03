from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_repair2"
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
    "test_phase157_r5_r9_body_starts_with_next_argument_after_reference_boundary"
    "():"
  )

  start = text.find(
    function_name
  )

  if start < 0:
    raise RuntimeError(
      "could not locate R5/R9 opener test function"
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

  replacement = """def test_phase157_r5_r9_body_starts_with_next_argument_after_reference_boundary():
  rendered = _pi6_3_rendered()
  body = rendered.split(
    "\\n## 証明\\n",
    1,
  )[
    1
  ]

  assert (
    "まず, "
    r"$\\nu'$ の位数を決定するために"
    in body
  )
"""

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
    "Repaired: "
    "tests/test_phase157_r5_r9_fixed_definition_body_suppression.py"
  )
  print(
    "Scope: one test function only"
  )


backup(
  TEST_PATH
)
replace_test_function()

print("")
print("Phase157 R11-R11 repair2 applied successfully.")
