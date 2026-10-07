from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRIBUTION_RENDERER = (
    ROOT / "toda_group_proof_narrative_contribution_renderer.py"
)
PI4_TEST = (
    ROOT
    / "tests"
    / "test_phase159_pi4_3_exactness_surjectivity_unification.py"
)
PI6_TEST = (
    ROOT
    / "tests"
    / "test_phase150_rc4_5c_2_exactness_to_map_property.py"
)


PI4_FUNCTION = r'''def test_phase159_pi4_3_surjectivity_reason_is_visible_without_double_connector():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_surjectivity_reason_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
      and isinstance(
        reason.conclusion_step.conclusion,
        TodaSuspensionSurjectiveStatement,
      )
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
    "完全性より, "
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  )
  assert rendered.count(
    sentence
  ) == 1
  assert rendered.count(
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  ) == 1
  assert (
    "この完全性と "
    not in rendered
  )
  assert (
    "これより, 完全性より,"
    not in rendered
  )


'''


PI6_FUNCTION = r'''def test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion():
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
    "完全性より, "
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
  )
  assert rendered.count(
    sentence
  ) == 1
  assert rendered.count(
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
  ) == 1
  assert (
    "この完全性と $Δ=0$ より"
    not in rendered
  )


'''


def replace_function(
    text: str,
    function_name: str,
    replacement: str,
) -> str:
    marker = f"def {function_name}("
    start = text.find(marker)

    if start < 0:
        raise RuntimeError(
            f"function not found: {function_name}"
        )

    next_def = text.find(
        "\ndef ",
        start + len(marker),
    )

    if next_def < 0:
        return (
            text[:start]
            + replacement.rstrip()
            + "\n"
        )

    return (
        text[:start]
        + replacement
        + text[next_def + 1:]
    )


def ensure_connector_prefix() -> None:
    text = CONTRIBUTION_RENDERER.read_text(
        encoding="utf-8"
    )

    if '"完全性より, ",' in text:
        print(
            "connector-prefix repair: already applied."
        )
        return

    old = (
        '  connector_prefixes = (\n'
        '    "以上より, ",\n'
        '    "したがって, ",\n'
        '    "これより, ",\n'
        '    "これらより, ",\n'
        '  )\n'
    )
    new = (
        '  connector_prefixes = (\n'
        '    "以上より, ",\n'
        '    "したがって, ",\n'
        '    "これより, ",\n'
        '    "これらより, ",\n'
        '    "完全性より, ",\n'
        '  )\n'
    )

    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            "connector_prefixes block not found uniquely"
        )

    CONTRIBUTION_RENDERER.write_text(
        text.replace(
            old,
            new,
            1,
        ),
        encoding="utf-8",
    )

    print(
        "connector-prefix repair: applied."
    )


def main() -> None:
    ensure_connector_prefix()

    pi4_text = PI4_TEST.read_text(
        encoding="utf-8"
    )
    PI4_TEST.write_text(
        replace_function(
            pi4_text,
            "test_phase159_pi4_3_surjectivity_reason_is_visible_without_double_connector",
            PI4_FUNCTION,
        ),
        encoding="utf-8",
    )
    print(
        "pi_4^3 duplicate assertion function: replaced."
    )

    pi6_text = PI6_TEST.read_text(
        encoding="utf-8"
    )
    PI6_TEST.write_text(
        replace_function(
            pi6_text,
            "test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion",
            PI6_FUNCTION,
        ),
        encoding="utf-8",
    )
    print(
        "pi_6^3 duplicate assertion function: replaced."
    )

    print(
        "Phase 159 exactness map-property duplicate "
        "suppression repair5 applied."
    )


if __name__ == "__main__":
    main()
