from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _pi6_3_data():
  report = build_standard_toda_report(
    n=3,
    k=3,
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
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )

  return (
    presentation,
    sidecar,
    blocks,
    arguments,
  )


def _pi6_3_rendered():
  (
    presentation,
    sidecar,
    blocks,
    arguments,
  ) = _pi6_3_data()

  return (
    presentation,
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    ),
  )


def test_phase153_r11_pi6_3_generic_section_excludes_root_self_reference():
  presentation, rendered = _pi6_3_rendered()

  root_reference = (
    extract_toda_group_proof_step_literature_reference(
      presentation.root_step
    )
  )
  reference_part = rendered.split(
    "\n## 証明\n",
    1,
  )[0]

  assert root_reference is not None
  assert root_reference.locator == "Proposition 5.6"
  assert "## 使用する結果" in reference_part
  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    not in reference_part
  )
  assert (
    r"$\pi_{5}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$"
    in reference_part
  )


def test_phase153_r11_pi6_3_depth2_keeps_used_external_references():
  _, rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "まず",
    1,
  )[0]

  assert "(5.3)" in reference_part
  assert "Proposition 5.3" in reference_part
