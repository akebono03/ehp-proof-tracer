from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _select_toda_group_proof_narrative_reference_entries_and_statement_lines,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
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


def _phase161_r4_r5_repair13_data():
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
    max_depth=3,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )

  return (
    raw,
    presentation,
  )


def test_phase161_r4_r5_repair13_reference_selection_binds_prop51_component_source():
  _, presentation = (
    _phase161_r4_r5_repair13_data()
  )
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      entries,
      presentation.root_step,
    )
  )

  normalized_entries, statement_lines = (
    _select_toda_group_proof_narrative_reference_entries_and_statement_lines(
      presentation,
      entries,
    )
  )

  prop51_entry = next(
    entry
    for entry in normalized_entries
    if entry.reference.locator
    == "Proposition 5.1"
  )

  rule_names = tuple(
    step.inference_rule.name
    for step in prop51_entry.proof_steps
    if step.inference_rule is not None
  )

  assert (
    "Toda Proposition 5.1 higher eta group relation"
    in rule_names
  )
  assert (
    "Toda Proposition 5.1 finite-dimensional integration"
    not in rule_names
  )

  assert any(
    (
      r"\pi_{n + 1}^{n} = "
      r"\mathbb{Z}/2\{\eta_{n}\}"
    )
    in line
    for line in statement_lines[
      prop51_entry.number
    ]
  )


def test_phase161_r4_r5_repair13_public_reference_has_52_and_prop51():
  raw, _ = (
    _phase161_r4_r5_repair13_data()
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "**[R1] (5.2).**" in reference
  assert "**[R2] Proposition 5.1.**" in reference
  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    in reference
  )

  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    not in body
  )


def test_phase161_r4_r5_repair13_public_prop51_links_to_pi4_3():
  raw, _ = (
    _phase161_r4_r5_repair13_data()
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  _, body = rendered.split(
    "---",
    1,
  )

  pi4_3_paragraph = next(
    paragraph
    for paragraph in body.split(
      "\n\n"
    )
    if (
      r"\pi_{4}^{3} = "
      r"\mathbb{Z}/2\{\eta_{3}\}"
      in paragraph
    )
  )

  assert "[R2]" in pi4_3_paragraph
  assert (
    pi4_3_paragraph.count(
      "[R2]"
    )
    == 1
  )


def test_phase161_r4_r5_repair13_keeps_pi4_2_contract():
  raw, _ = (
    _phase161_r4_r5_repair13_data()
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "Proposition 4.4" not in reference
  assert "$i=4$" in body
  assert (
    r"\pi_{4}^{3} \to \pi_{4}^{2}"
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
