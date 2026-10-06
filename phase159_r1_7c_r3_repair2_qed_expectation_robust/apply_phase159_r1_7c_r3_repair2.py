from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TEST_FILE = (
  REPO_ROOT
  / "tests"
  / "test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py"
)

FUNCTION_HEADER = (
  "def "
  "test_phase159_r1_7c_r3_pi11_4_renders_i11_decomposition_specialization():"
)


def main() -> None:
  if not TEST_FILE.exists():
    raise FileNotFoundError(
      f"focused test not found: {TEST_FILE}"
    )

  source = TEST_FILE.read_text(
    encoding="utf-8"
  )

  start = source.find(
    FUNCTION_HEADER
  )

  if start < 0:
    raise RuntimeError(
      "target test function was not found"
    )

  next_function = source.find(
    "\ndef ",
    start + len(
      FUNCTION_HEADER
    ),
  )

  end = (
    len(
      source
    )
    if next_function < 0
    else next_function + 1
  )

  function_source = source[
    start:end
  ]

  if '"□"' in function_source:
    print(
      "R3 repair2 already applied."
    )
    print(
      "Production code changes: none"
    )
    return

  stale_literal = 'r"$\\square$"'

  if stale_literal not in function_source:
    raise RuntimeError(
      "stale QED literal was not found "
      "inside the target test function"
    )

  repaired_function = (
    function_source.replace(
      stale_literal,
      '"□"',
      1,
    )
  )

  repaired_source = (
    source[
      :start
    ]
    + repaired_function
    + source[
      end:
    ]
  )

  TEST_FILE.write_text(
    repaired_source,
    encoding="utf-8",
  )

  print(
    "Phase 159 R1-7c R3 repair2 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Updated test:",
    TEST_FILE,
  )


if __name__ == "__main__":
  main()
