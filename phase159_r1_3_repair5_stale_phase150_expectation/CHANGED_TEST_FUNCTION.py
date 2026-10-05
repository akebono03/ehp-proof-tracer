def test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi6_reason_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    )
  )
  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert sentence == (
    "この完全性と $Δ=0$ より, "
    "$\\ker E=\\operatorname{Im}Δ=0$ である.\n"
    "したがって, "
  )

  reason_body = (
    "この完全性と $Δ=0$ より, "
    "$\\ker E=\\operatorname{Im}Δ=0$ である."
  )
  assert rendered.count(
    reason_body
  ) == 1

  conclusion = (
    "$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ "
    "は単射である."
  )
  assert conclusion in rendered
  assert rendered.index(
    reason_body
  ) < rendered.index(
    conclusion
  )
