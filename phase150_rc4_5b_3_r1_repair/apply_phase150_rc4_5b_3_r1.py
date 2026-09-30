from pathlib import Path

ROOT = Path.cwd()


def replace_once(path, old, new):
  text = path.read_text(encoding="utf-8-sig")
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f"{path}: expected one replacement target, found {count}"
    )
  path.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
  )


def patch_greek_latex():
  path = ROOT / "toda_human_readable_renderer.py"
  replace_once(
    path,
    '_GREEK_LATEX = {\n'
    '  "η": r"\\eta",\n',
    '_GREEK_LATEX = {\n'
    '  "β": r"\\beta",\n'
    '  "η": r"\\eta",\n',
  )
  print("Patched: toda_human_readable_renderer.py")


def patch_visible_reason_test():
  path = ROOT / "tests" / "test_phase150_rc4_5_visible_reasons.py"
  old = (
    '  assert rendered.count(\n'
    '    "この前提条件を満たすので、"\n'
    '    "次の定義を用いる."\n'
    '  ) == len(expected_sentences)\n'
  )
  new = (
    '  assert sum(\n'
    '    rendered.count(sentence)\n'
    '    for sentence in expected_sentences\n'
    '  ) == len(expected_sentences)\n'
    '\n'
    '  for sentence in expected_sentences:\n'
    '    assert rendered.count(sentence) == 1\n'
  )
  replace_once(path, old, new)
  print("Patched: tests/test_phase150_rc4_5_visible_reasons.py")


def main():
  patch_greek_latex()
  patch_visible_reason_test()
  print("RC4-5B-3-R1 repair applied.")


if __name__ == "__main__":
  main()
