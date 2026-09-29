from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_PATH = (
  ROOT
  / "phase144_6_r25_22_r2_web_numbered_equation_adapter"
  / "test_phase144_6_r25_22_r2.py"
)


def main() -> int:
  text = TEST_PATH.read_text(
    encoding="utf-8",
  )

  replacements = (
    (
      'assert b"\\\\\\\\tag{1}" in response.data',
      'assert rb"\\tag{1}" in response.data',
    ),
    (
      'assert b"\\\\\\\\tag{2}" in response.data',
      'assert rb"\\tag{2}" in response.data',
    ),
    (
      'assert b"\\\\\\\\tag{3}" in response.data',
      'assert rb"\\tag{3}" in response.data',
    ),
  )

  for old, new in replacements:
    count = text.count(
      old
    )
    if count != 1:
      raise RuntimeError(
        "Expected exactly one R25-22-R2 "
        f"assertion match for {old!r}; "
        f"found {count}."
      )
    text = text.replace(
      old,
      new,
      1,
    )

  TEST_PATH.write_text(
    text,
    encoding="utf-8",
  )

  print("R25-22-R3 focused-test assertion repair applied.")
  print("Production code changes: none.")
  print(
    "Corrected HTML LaTeX assertions: "
    r'rb"\tag{1}", rb"\tag{2}", rb"\tag{3}".'
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
