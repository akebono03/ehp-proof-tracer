from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_frontier_step_ids,
  _toda_group_proof_narrative_reference_internal_step_ids,
  _toda_group_proof_narrative_root_fixed_statement_internal_step_ids,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
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


def _phase161_r4_r3_pi4_2_data():
  report = build_standard_toda_report(
    n=2,
    k=2,
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      entries,
      presentation.root_step,
    )
  )
  statement_lines = {
    entry.number: ()
    for entry in entries
  }
  entries, _ = (
    exclude_toda_group_proof_narrative_root_reference(
      entries,
      statement_lines,
      presentation.root_step,
    )
  )

  return (
    raw,
    presentation,
    entries,
  )


def test_phase161_r4_r3_prop44_steps_are_internal_to_root_fixed_toda52_boundary():
  (
    _,
    presentation,
    entries,
  ) = _phase161_r4_r3_pi4_2_data()

  root_fixed_internal_step_ids = (
    _toda_group_proof_narrative_root_fixed_statement_internal_step_ids(
      presentation
    )
  )
  internal_step_ids = (
    _toda_group_proof_narrative_reference_internal_step_ids(
      presentation,
      entries,
    )
  )

  prop44_step = next(
    node.proof_step
    for node in presentation.nodes
    if (
      node.proof_step.inference_rule
      is not None
      and node.proof_step.inference_rule.name
      == "Toda Proposition 4.4 eta_2 n=2 specialization"
    )
  )
  restriction_step = next(
    node.proof_step
    for node in presentation.nodes
    if (
      node.proof_step.inference_rule
      is not None
      and node.proof_step.inference_rule.name
      == "Toda Proposition 4.4 eta_2 second-summand restriction"
    )
  )

  assert id(
    prop44_step
  ) in root_fixed_internal_step_ids
  assert id(
    restriction_step
  ) in root_fixed_internal_step_ids

  assert id(
    prop44_step
  ) in internal_step_ids
  assert id(
    restriction_step
  ) in internal_step_ids


def test_phase161_r4_r3_pi4_2_keeps_global_frontier_and_public_body_stops_at_toda52():
  (
    raw,
    presentation,
    entries,
  ) = _phase161_r4_r3_pi4_2_data()

  frontier_step_ids = (
    _toda_group_proof_narrative_reference_frontier_step_ids(
      presentation,
      entries,
    )
  )
  toda52 = next(
    entry
    for entry in entries
    if entry.reference.locator == "(5.2)"
  )

  assert any(
    id(
      proof_step
    )
    in frontier_step_ids
    for proof_step in toda52.proof_steps
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw
    )
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "**[R1] (5.2).**" in reference
  assert "Proposition 4.4" not in reference

  assert (
    r"\pi_{i - 1}^{1} \oplus "
    r"\pi_{i}^{3} \to "
    r"\pi_{i}^{2}"
    not in body
  )
  assert "分解写像の第二成分" not in body

  assert "[R1]" in body
  assert "$i=4$" in body
  assert (
    r"\pi_{4}^{3} \to \pi_{4}^{2}"
    in body
  )
  assert "同型" in body

  assert (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}"
    in body
  )
  assert (
    r"\eta_{3} \mapsto "
    r"\eta_{2}\eta_{3}"
    in body
  )
  assert (
    r"\pi_{4}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
    in body
  )
  assert "□" in body
