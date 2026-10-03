from __future__ import annotations

from pathlib import Path


TEST = Path(
  "tests/test_phase157_r5_r4_generic_reference_selection.py"
)

OLD_FIXED_RULE = (
  "'Toda Proposition 5.3 finite-dimensional integration'"
)
OLD_FIXED_LOCATOR = (
  "'Proposition 5.3'"
)

NEW_FIXED_RULE = (
  "'Toda Proposition 5.8 pi_9^5 group relation'"
)
NEW_FIXED_LOCATOR = (
  "'Proposition 5.8'"
)


def main() -> None:
  if not TEST.exists():
    raise SystemExit(
      "target test not found: "
      + str(
        TEST
      )
    )

  text = TEST.read_text(
    encoding="utf-8"
  )

  occurrences = text.count(
    OLD_FIXED_RULE
  )

  if occurrences < 2:
    raise SystemExit(
      "expected at least two stale fixed-rule occurrences; found "
      + str(
        occurrences
      )
    )

  text = text.replace(
    OLD_FIXED_RULE,
    NEW_FIXED_RULE,
  )
  text = text.replace(
    OLD_FIXED_LOCATOR,
    NEW_FIXED_LOCATOR,
  )

  TEST.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R5-R4 repair1 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Updated test fixed component source:"
  )
  print(
    "  Proposition 5.3 aggregate -> Proposition 5.8 concrete fixed component"
  )
  print(
    "updated: "
    + str(
      TEST.resolve()
    )
  )


if __name__ == "__main__":
  main()
