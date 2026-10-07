from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def replace_test_function(
  path: Path,
  function_name: str,
  replacement: str,
) -> None:
  source = path.read_text(
    encoding="utf-8",
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
      "test function not found: "
      + function_name
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

  path.write_text(
    updated,
    encoding="utf-8",
  )


def main() -> int:
  replace_test_function(
    REPO_ROOT
    / "tests"
    / "test_phase150_rc4_5c_2_exactness_to_map_property.py",
    "test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion",
    'def test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion():\n  (\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n    reason_sidecar,\n  ) = _pi6_reason_data()\n\n  reason = next(\n    reason\n    for reason in reason_sidecar.reasons\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .EXACTNESS_TO_MAP_PROPERTY\n    )\n  )\n  sentence = (\n    render_toda_group_proof_narrative_reason_sentence(\n      reason\n    )\n  )\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n\n  assert sentence == (\n    "完全性より, "\n    "$E: \\\\pi_{5}^{2} \\\\to \\\\pi_{6}^{3}$ "\n    "は単射."\n  )\n  assert rendered.count(\n    sentence\n  ) == 1\n\n  conclusion = (\n    "$E: \\\\pi_{5}^{2} \\\\to \\\\pi_{6}^{3}$ "\n    "は単射である."\n  )\n  assert conclusion in rendered\n  assert rendered.index(\n    sentence\n  ) < rendered.index(\n    conclusion\n  )\n',
  )

  replace_test_function(
    REPO_ROOT
    / "tests"
    / "test_phase157_r11_r17_residual_narrative_defects.py",
    "test_phase157_r11_r17_pi6_3_zero_map_statement_precedes_its_use",
    'def test_phase157_r11_r17_pi6_3_zero_map_statement_precedes_its_use():\n  _, body = _reference_and_body(\n    3,\n    3,\n  )\n\n  zero_map = (\n    r"$\\Delta: \\pi_{7}^{5} \\to \\pi_{5}^{2}$ "\n    "は零写像である."\n  )\n  use = (\n    "完全性より, "\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ "\n    "は単射."\n  )\n\n  assert zero_map in body\n  assert use in body\n  assert body.index(\n    zero_map\n  ) < body.index(\n    use\n  )\n',
  )

  replace_test_function(
    REPO_ROOT
    / "tests"
    / "test_phase157_r20_repair43_dangling_connector_cleanup.py",
    "test_phase157_r20_repair43_required_reason_sentences_remain",
    'def test_phase157_r20_repair43_required_reason_sentences_remain():\n  body = _body_pi6_3_repair43()\n\n  assert (\n    "完全性より, "\n    r"$\\ker \\Delta=\\operatorname{Im}H="\n    r"\\pi_{7}^{5}$."\n    in body\n  )\n  assert (\n    "完全性より, "\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ "\n    "は単射."\n    in body\n  )\n  assert (\n    r"$\\operatorname{ord}(\\eta_{3}^{3})=2$ "\n    r"かつ $2\\nu\'=\\eta_{3}^{3}$ より, "\n    r"$4\\nu\'=0$ かつ $2\\nu\'\\neq0$."\n    in body\n  )\n',
  )

  print(
    "Phase 159 exactness-reason stale expectation repair6 applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
