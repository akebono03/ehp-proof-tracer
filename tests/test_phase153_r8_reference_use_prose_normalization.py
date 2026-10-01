from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_reference_body_duplicates,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _pi6_2_body():
  report = build_standard_toda_report(
    n=2,
    k=4,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )
  marker = "## 証明\n\n"

  if marker not in rendered:
    return rendered

  return rendered.split(
    marker,
    1,
  )[1]


def test_phase153_r8_normalizes_replaced_reference_derivation_to_use_sentence():
  statement = r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
  body = (
    "このことから, "
    + statement
    + "を得る."
  )

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert rendered == "[R2]を用いる."


def test_phase153_r8_normalizes_existing_reference_marker_to_use_sentence():
  statement = r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
  body = (
    "まず, [R2] により, "
    + statement
    + "を得る."
  )

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert rendered == "[R2]を用いる."


def test_phase153_r8_does_not_change_non_reference_derivation_sentence():
  body = r"このことから, $γ \mapsto \eta_{2}γ$を得る."

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$",
        ),
      },
    )
  )

  assert rendered == body


def test_phase153_r8_pi6_2_reference_use_is_not_written_as_obtained():
  body = _pi6_2_body()

  assert "[R2]を用いる." in body
  assert "[R2]を得る." not in body
  assert "このことから, [R2]を得る." not in body


def test_phase153_r8_pi6_2_keeps_final_conclusion():
  body = _pi6_2_body()

  assert (
    r"\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}"
    in body
  )
