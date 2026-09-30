from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST = (
  ROOT
  / "tests"
  / "test_phase150_rc4_5f_2_final_group_structure_reason.py"
)


def main() -> None:
  text = TEST.read_text(encoding="utf-8")

  old_order = '  assert "中央の群の位数は $2\\\\cdot2=4$" in sentence\n'
  new_order = '  assert r"中央の群の位数は $2\\\\cdot2=4$" in sentence\n'

  old_conclusion = '  conclusion = "$\\\\pi_{6}^{3} = \\\\mathbb{Z}/4\\\\{\\\\nu\\'\\\\}$"\n'
  new_conclusion = '  conclusion = r"$\\\\pi_{6}^{3} = \\\\mathbb{Z}/4\\\\{\\\\nu\\'\\\\}$"\n'

  if old_order not in text:
    if new_order not in text:
      raise RuntimeError(
        "Expected order assertion was not found."
      )
  else:
    text = text.replace(
      old_order,
      new_order,
      1,
    )

  if old_conclusion not in text:
    if new_conclusion not in text:
      raise RuntimeError(
        "Expected conclusion assertion was not found."
      )
  else:
    text = text.replace(
      old_conclusion,
      new_conclusion,
      1,
    )

  TEST.write_text(
    text,
    encoding="utf-8",
  )

  print("RC4-5F-2-R1 test escaping repaired.")
  print("Production changes: none.")
  print("Changed existing RC4-5F-2 test only:")
  print(
    "  tests/"
    "test_phase150_rc4_5f_2_final_group_structure_reason.py"
  )


if __name__ == "__main__":
  main()
