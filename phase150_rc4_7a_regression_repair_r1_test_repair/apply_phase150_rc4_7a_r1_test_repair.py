from pathlib import Path

TARGET = Path(
  "phase150_rc4_7a_regression_repair_r1"
  "/test_phase150_rc4_7a_regression_repair_r1.py"
)

OLD = """  assert rendered.startswith(
    "$\\\\pi_{15}^{8}$ の群構造を決定する."
  )
"""

NEW = """  assert "使用する結果を先にまとめる." not in rendered
  assert "**[R1]" not in rendered
  assert "$\\\\pi_{15}^{8}" in rendered
  assert "$\\\\sigma\'\'\'$ を定める." in rendered
"""


def main():
  text = TARGET.read_text(
    encoding="utf-8"
  )

  if OLD in text:
    TARGET.write_text(
      text.replace(
        OLD,
        NEW,
        1,
      ),
      encoding="utf-8",
    )
    print(
      "RC4-7A R1 focused-test expectation repaired."
    )
    print(
      "Production files were not changed."
    )
    return

  if NEW in text:
    print(
      "RC4-7A R1 focused-test expectation is already repaired."
    )
    return

  raise SystemExit(
    "Target assertion was not found; no file was changed."
  )


if __name__ == "__main__":
  main()
