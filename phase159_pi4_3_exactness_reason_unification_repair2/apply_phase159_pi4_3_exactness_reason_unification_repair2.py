from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "tests" / "test_phase150_rc4_5c_2_exactness_to_map_property.py"


OLD_FUNCTION = r'''def test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion():
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
  assert rendered.count(sentence) == 1

  conclusion = (
    "$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ "
    "は単射である."
  )
  assert conclusion in rendered
  assert rendered.index(sentence) < rendered.index(
    conclusion
  )
'''


NEW_FUNCTION = r'''def test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion():
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
    "$\\ker E=\\operatorname{Im}Δ=0$.\n"
    "したがって, "
  )
  assert rendered.count(sentence) == 1

  conclusion = (
    "$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ "
    "は単射である."
  )
  assert conclusion in rendered
  assert rendered.index(sentence) < rendered.index(
    conclusion
  )
'''


def main() -> None:
    text = TEST.read_text(encoding="utf-8")

    if NEW_FUNCTION in text:
        print("Phase 159 repair2 already applied.")
        return

    count = text.count(OLD_FUNCTION)
    if count != 1:
        raise RuntimeError(
            "Expected exactly one stale Phase 150 exactness "
            f"test function, found {count}."
        )

    TEST.write_text(
        text.replace(
            OLD_FUNCTION,
            NEW_FUNCTION,
            1,
        ),
        encoding="utf-8",
    )

    print(
        "Phase 159 pi_4^3 exactness reason "
        "unification repair2 applied."
    )


if __name__ == "__main__":
    main()
