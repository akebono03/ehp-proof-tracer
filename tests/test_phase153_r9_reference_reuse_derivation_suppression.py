from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  build_toda_group_proof_narrative_reference_reuse_marker_by_step_id,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
)


def _pi6_2_presentation():
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

  return (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )


def _pi6_2_body():
  rendered = render_toda_group_proof_narrative_markdown(
    _pi6_2_presentation()
  )
  marker = "## 証明\n\n"

  if marker not in rendered:
    return rendered

  return rendered.split(
    marker,
    1,
  )[1]


def test_phase153_r9_selected_toda52_step_is_reference_reuse_boundary():
  presentation = _pi6_2_presentation()
  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  marker_by_step_id = (
    build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(
      presentation,
      reference_entries,
    )
  )

  toda52_steps = tuple(
    proof_step
    for entry in reference_entries
    for proof_step in entry.proof_steps
    if isinstance(
      proof_step.conclusion,
      Toda52CompositionIsomorphismStatement,
    )
  )

  assert len(
    toda52_steps
  ) == 1
  assert marker_by_step_id[
    id(
      toda52_steps[0]
    )
  ] == "[R3]"


def test_phase153_r9_pi6_2_reuses_selected_references_without_rederiving_ancestry():
  body = _pi6_2_body()

  assert "[R1]を用いる." in body
  assert "[R2]を用いる." in body

  for forbidden in (
    r"\pi_{i - 1}^{1} = 0",
    "Proposition 4.4",
    r"γ \mapsto \eta_{2}γ",
    "Toda (5.2) の η₂ 合成同型を得る.",
  ):
    assert forbidden not in body


def test_phase153_r9_pi6_2_keeps_final_conclusion():
  body = _pi6_2_body()

  assert (
    r"\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}"
    in body
  )
