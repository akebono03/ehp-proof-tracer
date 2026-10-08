from homotopy_groups import (
  TodaPrimaryGroup,
)
from proof import (
  Relation,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan,
  _toda_group_proof_narrative_reference_frontier_step_ids,
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


def _phase161_r4_repair1_pi4_2_presentations():
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
  semantic = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )

  return (
    raw,
    semantic,
  )


def _phase161_r4_repair1_entries():
  _, presentation = (
    _phase161_r4_repair1_pi4_2_presentations()
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
    presentation,
    entries,
  )


def test_phase161_r4_repair1_toda52_runtime_fields_drive_specialization():
  presentation, entries = (
    _phase161_r4_repair1_entries()
  )
  plan = (
    _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan(
      presentation,
      entries,
    )
  )

  assert plan is not None

  (
    _,
    fixed_step,
    source_step,
    specialized_source,
    specialized_target,
    _,
    _,
    target_dimension,
  ) = plan

  assert getattr(
    fixed_step.conclusion,
    "source_group",
    None,
  ) is not None
  assert getattr(
    fixed_step.conclusion,
    "target_group",
    None,
  ) is not None
  assert getattr(
    fixed_step.conclusion,
    "composition",
    None,
  ) is not None

  assert target_dimension == 4
  assert specialized_source == TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )
  assert specialized_target == TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=2,
  )

  assert isinstance(
    source_step.conclusion,
    Relation,
  )


def test_phase161_r4_repair1_fixed_toda52_is_frontier_but_prop44_is_not():
  presentation, entries = (
    _phase161_r4_repair1_entries()
  )
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
  prop44 = next(
    entry
    for entry in entries
    if entry.reference.locator == "Proposition 4.4"
  )

  assert any(
    id(
      proof_step
    )
    in frontier_step_ids
    for proof_step in toda52.proof_steps
  )
  assert all(
    id(
      proof_step
    )
    not in frontier_step_ids
    for proof_step in prop44.proof_steps
  )


def test_phase161_r4_repair1_public_pi4_2_has_general_reference_and_specialized_body():
  raw, _ = (
    _phase161_r4_repair1_pi4_2_presentations()
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
  assert (
    r"$\eta_{2}\circ -: "
    r"\pi_{i}^{3} \to \pi_{i}^{2}$"
    in reference
  )

  assert "Proposition 4.4" not in reference

  assert (
    r"[R1]を $i=4$ に適用すると, "
    r"$\eta_{2}\circ -: "
    r"\pi_{4}^{3} \to \pi_{4}^{2}$ "
    r"は同型である."
    in body
  )
  assert (
    r"\eta_{3} \mapsto"
    in body
  )

  assert r"\pi_{i}^{3}" not in body
  assert r"\pi_{i}^{2}" not in body
  assert r"\pi_{i - 1}^{1}" not in body
  assert "分解写像の第二成分" not in body
  assert "Proposition 4.4" not in body


def test_phase161_r4_repair1_keeps_target_and_qed():
  raw, _ = (
    _phase161_r4_repair1_pi4_2_presentations()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw
    )
  )

  assert (
    r"\pi_{4}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
    in rendered
  )
  assert "□" in rendered
