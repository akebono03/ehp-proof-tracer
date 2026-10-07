from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase157_r20_repair43_dangling_connector_cleanup.py"
)


def main() -> int:
  source = TEST_PATH.read_text(
    encoding="utf-8",
  )

  function_name = (
    "test_phase157_r20_repair43_required_reason_sentences_remain"
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

  replacement = 'def test_phase157_r20_repair43_required_reason_sentences_remain():\n  body = _body_pi6_3_repair43()\n\n  assert (\n    "完全性より, "\n    r"$\\ker \\Delta=\\operatorname{Im}H="\n    r"\\pi_{7}^{5}$ である."\n    in body\n  )\n  assert (\n    "完全性より, "\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ "\n    "は単射."\n    in body\n  )\n  assert (\n    r"$\\operatorname{ord}(\\eta_{3}^{3})=2$ "\n    r"かつ $2\\nu\'=\\eta_{3}^{3}$ より, "\n    r"$4\\nu\'=0$ かつ $2\\nu\'\\neq0$."\n    in body\n  )\n'

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
    "Phase 159 kernel-reason stale expectation repair6c applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
