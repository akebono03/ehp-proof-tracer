from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
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


def _render_and_selected(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  raw_presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw_presentation
    )
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  selected = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )

  if "## 証明" in rendered:
    body = rendered.split(
      "## 証明",
      1,
    )[1]
  else:
    body = rendered

  return (
    rendered,
    body,
    selected,
  )


def test_phase156_r5_repair3_pi6_3_has_no_exact_selected_statement_body_restatement():
  _rendered, body, selected = (
    _render_and_selected(
      3,
      3,
    )
  )

  statements = tuple(
    statement
    for lines in selected.values()
    for statement in lines
  )

  assert statements

  for statement in statements:
    assert statement not in body


def test_phase156_r5_repair3_phase150_generic_routes_have_no_exact_selected_statement_body_restatement():
  for n, k in (
    (
      4,
      6,
    ),
    (
      5,
      7,
    ),
    (
      9,
      7,
    ),
  ):
    _rendered, body, selected = (
      _render_and_selected(
        n,
        k,
      )
    )

    statements = tuple(
      statement
      for lines in selected.values()
      for statement in lines
    )

    assert statements

    for statement in statements:
      assert statement not in body


def test_phase156_r5_repair3_reference_headers_remain_present():
  for n, k in (
    (
      3,
      3,
    ),
    (
      4,
      6,
    ),
    (
      5,
      7,
    ),
    (
      9,
      7,
    ),
  ):
    rendered, _body, _selected = (
      _render_and_selected(
        n,
        k,
      )
    )

    assert "**[R1]" in rendered
