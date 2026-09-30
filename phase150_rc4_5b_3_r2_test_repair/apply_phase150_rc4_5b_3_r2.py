from pathlib import Path

ROOT = Path.cwd()
PATH = (
  ROOT
  / "tests"
  / "test_phase150_rc4_5b_3_r1_beta_latex.py"
)

OLD = '  assert render_toda_expression_latex(beta) == r"\\\\beta"\n'
NEW = '  assert render_toda_expression_latex(beta) == r"\\beta"\n'


def main():
  text = PATH.read_text(encoding="utf-8")
  count = text.count(OLD)

  if count != 1:
    raise RuntimeError(
      f"{PATH}: expected one incorrect beta expectation, found {count}"
    )

  PATH.write_text(
    text.replace(OLD, NEW, 1),
    encoding="utf-8",
  )

  print(
    "Patched:",
    PATH.relative_to(ROOT),
  )
  print(
    r'Expected LaTeX corrected: r"\\beta" -> r"\beta"'
  )
  print("Production changes: none")


if __name__ == "__main__":
  main()
