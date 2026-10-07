from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_r1_2_pi3_2_narrative_repair.py"
)


def main() -> int:
  source = TEST_PATH.read_text(
    encoding="utf-8-sig",
  )

  function_name = (
    "test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically"
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

  replacement = 'def test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically():\n  presentation = _phase159_r1_2_pi3_2_presentation()\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  injective = (\n    "完全性より, "\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は単射."\n  )\n  surjective = (\n    "完全性より, "\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は全射."\n  )\n  isomorphism = (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は同型."\n  )\n\n  assert injective in rendered\n  assert surjective in rendered\n  assert isomorphism in rendered\n\n  assert rendered.index(\n    injective\n  ) < rendered.index(\n    isomorphism\n  )\n  assert rendered.index(\n    surjective\n  ) < rendered.index(\n    isomorphism\n  )\n\n  assert (\n    r"\\quad\\text{は単射}. \\qquad"\n    not in rendered\n  )\n  assert (\n    r"\\quad\\text{は全射}. \\qquad"\n    not in rendered\n  )\n'

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
    "Phase 159 pi3_2 numbered-map-property stale expectation repair9a applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
