from pathlib import Path


TARGET = Path(
  "tests/test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py"
)


OLD_ASSERTION = '  assert b"\\\\\\\\tag{1}" in response.data\n'

NEW_ASSERTION = '  assert b"\\\\tag{1}" in response.data\n'


def main() -> int:
  text = TARGET.read_text(
    encoding="utf-8"
  )

  if NEW_ASSERTION in text and OLD_ASSERTION not in text:
    print(
      "R4.2-R2 Web TeX assertion already repaired."
    )
    return 0

  if text.count(
    OLD_ASSERTION
  ) != 1:
    raise RuntimeError(
      "Expected exactly one stale double-backslash "
      "Web TeX assertion."
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
    "R4.2-R2 test-only repair applied."
  )
  print(
    "Production changes: none."
  )
  print(
    "Web HTML assertion now searches for one literal "
    "TeX backslash."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
