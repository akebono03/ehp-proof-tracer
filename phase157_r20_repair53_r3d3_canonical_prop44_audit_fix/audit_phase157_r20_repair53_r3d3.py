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

STALE_LINE_1 = '    r"\\left(α, \\beta\\right) \\mapsto "'
STALE_LINE_2 = '    r"Eα + \\sigma_{8}\\beta"'

CANONICAL_LINE_1 = '    r"(α, \\beta) \\mapsto "'
CANONICAL_LINE_2 = '    r"Eα + \\sigma_{8}\\beta"'


def main() -> int:
  if not TARGET.exists():
    raise RuntimeError(
      "missing test file: "
      + str(
        TARGET
      )
    )

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

  lines = function_source.splitlines()

  stale_pair_count = sum(
    1
    for index in range(
      len(
        lines
      )
      - 1
    )
    if (
      lines[index] == STALE_LINE_1
      and lines[index + 1] == STALE_LINE_2
    )
  )

  canonical_pair_count = sum(
    1
    for index in range(
      len(
        lines
      )
      - 1
    )
    if (
      lines[index] == CANONICAL_LINE_1
      and lines[index + 1] == CANONICAL_LINE_2
    )
  )

  print(
    "stale pair count:",
    stale_pair_count,
  )
  print(
    "canonical pair count:",
    canonical_pair_count,
  )

  if stale_pair_count != 0:
    raise RuntimeError(
      "stale Prop.4.4 expectation remains"
    )

  if canonical_pair_count != 1:
    raise RuntimeError(
      "expected exactly one canonical Prop.4.4 "
      "expectation pair, found "
      + str(
        canonical_pair_count
      )
    )

  print(
    "AUDIT PASS: canonical Prop.4.4 source expectation is present."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
