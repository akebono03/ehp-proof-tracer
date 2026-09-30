from pathlib import Path

ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_reason_renderer.py"
TEST = ROOT / "tests" / "test_phase150_rc4_5d_3_multiple_relation_to_order.py"


def replace_once(text, old, new, label):
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one replacement target, found {count}"
    )
  return text.replace(old, new, 1)


def patch_renderer():
  text = RENDERER.read_text(encoding="utf-8")
  old = '      f"$2{target_latex}\\\\neq0$ である.\\\\n"\n'
  new = '      f"$2{target_latex}\\\\neq0$ である.\\n"\n'
  text = replace_once(text, old, new, "reason newline")
  RENDERER.write_text(text, encoding="utf-8")


def patch_test():
  text = TEST.read_text(encoding="utf-8")
  old = (
    '  assert rendered.count(sentence) == 1\n'
    '  assert rendered.index(sentence) < rendered.index(\n'
    '    "$\\\\operatorname{ord}(\\\\nu\')=4$."\n'
    '  )\n'
  )
  new = (
    '  assert rendered.count(sentence) == 1\n'
    '  conclusion_line = (\n'
    '    "$\\\\operatorname{ord}\\\\left(\\\\nu\'\\\\right) = 4$"\n'
    '  )\n'
    '  assert conclusion_line in rendered\n'
    '  assert rendered.index(sentence) < rendered.index(\n'
    '    conclusion_line\n'
    '  )\n'
  )
  text = replace_once(text, old, new, "canonical order-four expectation")
  TEST.write_text(text, encoding="utf-8")


def main():
  patch_renderer()
  patch_test()
  print("RC4-5D-3-R1 renderer/test repair applied.")
  print("Reason classification is unchanged.")
  print("Contribution ordering is unchanged.")


if __name__ == "__main__":
  main()
