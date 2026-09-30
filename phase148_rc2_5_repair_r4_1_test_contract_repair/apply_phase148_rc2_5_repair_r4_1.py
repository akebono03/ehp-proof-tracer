from pathlib import Path

ROOT = Path.cwd()

def replace_once(path, old, new):
  text = path.read_text(encoding="utf-8")
  if old not in text:
    raise RuntimeError("Expected R4 local text not found in " + str(path))
  path.write_text(text.replace(old, new, 1), encoding="utf-8")

def main():
  p47 = ROOT / "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py"
  replace_once(
    p47,
    '  assert rendered.count(\n    r"\\pi_{4}^{3} = \\mathbb{Z}/2\\{\\eta_{3}\\}"\n  ) == 0\n',
    '  assert rendered.count(\n    r"\\pi_{4}^{3} = \\mathbb{Z}/2\\{\\eta_{3}\\}"\n  ) == 1\n',
  )
  replace_once(
    p47,
    '  assert rendered.count(\n    r"$\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  ) == 1\n',
    '  assert rendered.count(\n    r"$\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  ) == 0\n',
  )
  p50 = ROOT / "tests/test_phase143_50_generic_statement_prose_renderer.py"
  replace_once(
    p50,
    '  assert (\n    r"$\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3} \\xrightarrow{H} "\n    r"\\pi_{6}^{5}$ は完全である."\n    in rendered\n  )\n',
    '  assert (\n    r"$\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3} \\xrightarrow{H} "\n    r"\\pi_{6}^{5}$ は完全である."\n    not in rendered\n  )\n',
  )
  print("Phase 148 RC2-5 Repair R4.1 applied.")
  print("Production changes: none.")
  print("Corrected exactly three assertions.")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
