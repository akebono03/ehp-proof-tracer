from pathlib import Path


TARGET = Path(
  "phase148_rc2_1_repair_r1"
) / "test_phase148_rc2_1_repair_r1.py"


def main():
  if not TARGET.exists():
    raise SystemExit(
      f"target audit test not found: {TARGET}"
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  old = "assert primary is components[0]"
  new = "assert primary == components[0]"

  count = source.count(old)

  if count != 2:
    raise SystemExit(
      "expected exactly two identity assertions, "
      f"found {count}"
    )

  source = source.replace(
    old,
    new,
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "RC2-1 Repair R2 applied: "
    "two audit-only identity assertions changed to value equality."
  )
  print("Production code changes: none.")
  print("Existing repository test changes: none.")


if __name__ == "__main__":
  main()
