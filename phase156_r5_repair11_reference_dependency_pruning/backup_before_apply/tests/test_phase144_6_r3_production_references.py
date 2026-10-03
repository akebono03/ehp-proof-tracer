from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
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


def _phase144_6_r3_pi6_3_data():
  report = build_standard_toda_report(n=3, k=3)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(replay)
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
  return presentation, sidecar, blocks, arguments


def test_phase144_6_r3_pi6_3_references_are_structured_and_deduplicated():
  presentation, _, _, _ = _phase144_6_r3_pi6_3_data()
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  locators = tuple(entry.reference.locator for entry in entries)

  assert "(5.3)" in locators
  assert "Lemma 5.2" not in locators
  assert "(5.3) / Lemma 5.2" not in locators
  assert locators.count("(5.3)") == 1
  assert "(5.2)" in locators
  assert "Proposition 4.4" in locators
  assert "Proposition 5.1" in locators
  assert locators.count("Proposition 4.4") == 1
  assert "Proposition 2.2" not in locators


def test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section():
  presentation, sidecar, blocks, arguments = _phase144_6_r3_pi6_3_data()
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  reference_section = rendered.split(
    "まず",
    1,
  )[0]

  assert "使用する結果を先にまとめる." in reference_section
  assert "(5.3) / Lemma 5.2" not in reference_section
  assert "(5.3)" in reference_section
  assert "Lemma 5.2" not in reference_section
  assert "(5.2)" in reference_section
  assert "Proposition 4.4" in reference_section
  assert "Proposition 5.1" in reference_section
  assert "Proposition 2.2" not in reference_section


def test_phase144_6_r3_reference_section_does_not_parse_internal_rule_names():
  presentation, sidecar, blocks, arguments = _phase144_6_r3_pi6_3_data()
  rendered = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )
  reference_section = rendered.split("まず、", 1)[0]

  assert "eta_2 n=2 specialization" not in reference_section
  assert "finite-dimensional integration" not in reference_section
