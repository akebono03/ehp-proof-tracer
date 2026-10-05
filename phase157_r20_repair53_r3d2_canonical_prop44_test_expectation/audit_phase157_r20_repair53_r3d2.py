from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase157_r20_repair53_r3_fixed_reference_attribution.py"
)

TEST_NAME = (
  "test_phase157_r20_repair53_r3_public_pi15_8_restores_prop44_reference"
)


def main() -> int:
  source = TARGET.read_text(
    encoding="utf-8",
  )

  start_marker = (
    "def "
    + TEST_NAME
    + "():"
  )
  start = source.find(
    start_marker
  )

  if start < 0:
    raise RuntimeError(
      "target test function not found"
    )

  next_def = source.find(
    "\ndef ",
    start + len(
      start_marker
    ),
  )

  function_source = (
    source[
      start:
    ]
    if next_def < 0
    else source[
      start:
      next_def
    ]
  )

  print(
    "=" * 96
  )
  print(
    "UPDATED TEST FUNCTION"
  )
  print(
    "=" * 96
  )
  print(
    function_source.rstrip()
  )
  print()

  stale = (
    r'\left(α, \beta\right) \mapsto '
    r'Eα + \sigma_{8}\beta'
  )
  canonical = (
    r'(α, \beta) \mapsto '
    r'Eα + \sigma_{8}\beta'
  )

  if stale in function_source:
    raise RuntimeError(
      "stale Prop.4.4 expectation remains"
    )

  if canonical not in function_source:
    raise RuntimeError(
      "canonical Prop.4.4 expectation is missing"
    )

  print(
    "AUDIT PASS: canonical Prop.4.4 expectation is present."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
