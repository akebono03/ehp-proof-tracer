from pathlib import Path


TARGET = Path(
  "tests/test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py"
)


OLD_ASSERTION = """  assert b"Selected depth: 2" in response.data
"""

NEW_ASSERTION = """  assert (
    b"Selected depth:\\n          2"
    in response.data
  )
"""


def main() -> int:
  text = TARGET.read_text(
    encoding="utf-8"
  )

  if NEW_ASSERTION in text:
    print(
      "R4.2-R1 Web depth assertion already repaired."
    )
    return 0

  if text.count(
    OLD_ASSERTION
  ) != 1:
    raise RuntimeError(
      "Expected exactly one stale "
      "'Selected depth: 2' assertion."
    )

  TARGET.write_text(
    text.replace(
      OLD_ASSERTION,
      NEW_ASSERTION,
      1,
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "R4.2-R1 test-only repair applied."
  )
  print(
    "Production changes: none."
  )
  print(
    "Web depth assertion now matches the existing "
    "template contract used by Phase 118 tests."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
