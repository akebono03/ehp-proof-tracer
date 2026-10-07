from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase150_rc4_5c_2_exactness_to_map_property.py"
)


def main() -> int:
  source = TEST_PATH.read_text(
    encoding="utf-8",
  )

  old_name = (
    "def "
    "test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion"
    "("
  )
  start = source.find(
    old_name
  )

  if start < 0:
    raise RuntimeError(
      "target test function not found"
    )

  next_def = source.find(
    "\ndef ",
    start + len(
      old_name
    ),
  )

  if next_def < 0:
    end = len(
      source
    )
  else:
    end = next_def + 1

  replacement = 'def test_phase150_rc4_5c_2_exactness_reason_is_visible_without_verbose_duplicate():\n  (\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n    reason_sidecar,\n  ) = _pi6_reason_data()\n\n  reason = next(\n    reason\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .EXACTNESS_TO_MAP_PROPERTY\n    )\n  )\n  sentence = (\n    render_toda_group_proof_narrative_reason_sentence(\n      reason\n    )\n  )\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n\n  assert sentence == (\n    "完全性より, "\n    "$E: \\\\pi_{5}^{2} \\\\to \\\\pi_{6}^{3}$ "\n    "は単射."\n  )\n  assert rendered.count(\n    sentence\n  ) == 1\n\n  verbose_duplicate = (\n    "$E: \\\\pi_{5}^{2} \\\\to \\\\pi_{6}^{3}$ "\n    "は単射である."\n  )\n  assert verbose_duplicate not in rendered\n'

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
    "Phase 159 exactness-reason stale expectation repair6a applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
