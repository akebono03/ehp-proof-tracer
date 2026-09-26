from pathlib import Path

TARGET = Path(
  "tests/"
  "test_phase143_75ab3_whitehead_correction_rendering.py"
)

text = TARGET.read_text(encoding="utf-8")

old = r"E\left([\iota_{4}, \iota_{4}]\right) = 0"
new = r"E[\iota_{4}, \iota_{4}] = 0"

count = text.count(old)
if count != 2:
  raise SystemExit(
    "Expected exactly two parenthesized suspension expectations; "
    f"found {count}."
  )

backup = TARGET.with_suffix(
  TARGET.suffix + ".phase143_75ab3_r3_backup"
)
if not backup.exists():
  backup.write_text(
    TARGET.read_text(encoding="utf-8"),
    encoding="utf-8",
  )

TARGET.write_text(
  text.replace(old, new),
  encoding="utf-8",
)

print("Phase 143-75AB-3-R3 test expectation repair applied.")
