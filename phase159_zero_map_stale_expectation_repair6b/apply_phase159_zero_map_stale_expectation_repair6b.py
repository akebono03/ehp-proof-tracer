from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase157_r11_r17_residual_narrative_defects.py"
)


def main() -> int:
  source = TEST_PATH.read_text(
    encoding="utf-8",
  )

  function_name = (
    "test_phase157_r11_r17_pi6_3_zero_map_statement_precedes_its_use"
  )
  start_marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    start_marker
  )

  if start < 0:
    raise RuntimeError(
      "target test function not found"
    )

  next_def = source.find(
    "\ndef ",
    start + len(
      start_marker
    ),
  )

  if next_def < 0:
    end = len(
      source
    )
  else:
    end = next_def + 1

  replacement = 'def test_phase157_r11_r17_pi6_3_zero_map_statement_precedes_its_use():\n  _, body = _reference_and_body(\n    3,\n    3,\n  )\n\n  zero_map = (\n    r"$\\Delta: \\pi_{7}^{5} \\to \\pi_{5}^{2}$ "\n    "は零写像."\n  )\n  use = (\n    "完全性より, "\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ "\n    "は単射."\n  )\n\n  assert zero_map in body\n  assert use in body\n  assert body.index(\n    zero_map\n  ) < body.index(\n    use\n  )\n'

  updated = (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + source[
      end:
    ].lstrip(
      "\n"
    )
  )

  TEST_PATH.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Phase 159 zero-map stale expectation repair6b applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
