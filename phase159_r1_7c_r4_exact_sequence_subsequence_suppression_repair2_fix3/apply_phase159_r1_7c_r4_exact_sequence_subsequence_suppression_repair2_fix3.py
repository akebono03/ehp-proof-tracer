from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

TEST = ROOT / "tests" / "test_phase157_r20_repair32_exactness_intro_anchor.py"

TEST1 = 'def test_phase157_r20_repair32_full_exactness_uses_intro_sequence_anchor():\n  body = _body_pi6_3_repair32()\n\n  exact_sequence_core = (\n    r"\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3} \\xrightarrow{H} "\n    r"\\pi_{6}^{5}"\n  )\n  eta6_definition = (\n    r"$\\eta_{6}=E\\eta_{5}$."\n  )\n\n  assert (\n    "次の完全列を考える."\n    in body\n  )\n  assert exact_sequence_core in body\n  assert body.index(\n    exact_sequence_core\n  ) < body.index(\n    eta6_definition\n  )\n'
TEST2 = 'def test_phase157_r20_repair32_bare_duplicate_full_sequence_is_removed():\n  body = _body_pi6_3_repair32()\n\n  duplicate_bare_sequence = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$."\n  )\n  stale_inline_exactness = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  exact_sequence_core = (\n    r"\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3} \\xrightarrow{H} "\n    r"\\pi_{6}^{5}"\n  )\n\n  assert duplicate_bare_sequence not in body\n  assert stale_inline_exactness not in body\n  assert body.count(\n    exact_sequence_core\n  ) == 1\n'


def replace_function(
  source: str,
  function_name: str,
  new_source: str,
) -> str:
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise SystemExit(
      f"function not found: {function_name}"
    )

  next_start = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_start < 0:
    end = len(
      source
    )
  else:
    end = next_start + 1

  return (
    source[:start]
    + new_source.rstrip()
    + "\n\n"
    + source[end:]
  )


def main() -> None:
  BACKUP.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TEST,
    BACKUP / TEST.name,
  )

  source = TEST.read_text(
    encoding="utf-8"
  )

  source = replace_function(
    source,
    "test_phase157_r20_repair32_full_exactness_uses_intro_sequence_anchor",
    TEST1,
  )
  source = replace_function(
    source,
    "test_phase157_r20_repair32_bare_duplicate_full_sequence_is_removed",
    TEST2,
  )

  TEST.write_text(
    source,
    encoding="utf-8",
  )

  print(
    "Phase 159 R1-7c R4 exact-sequence suppression repair2 fix3 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Updated stale Phase157 inline-exactness expectations to the current display-math contract."
  )


if __name__ == "__main__":
  main()
