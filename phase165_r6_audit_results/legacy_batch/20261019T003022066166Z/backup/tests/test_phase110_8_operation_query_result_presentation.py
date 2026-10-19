from repository_operation_query_facade import (
  query_standard_repository_operation_input,
)
from repository_operation_query_presentation import (
  build_repository_operation_query_presentation,
)
from repository_operation_query_renderer import (
  render_repository_operation_query_markdown,
)


def test_phase110_8_h_nu_prime_deduplicates_to_two_mathematical_facts():
  result = (
    query_standard_repository_operation_input(
      "H(nu_prime)"
    )
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

  assert len(
    result.matches
  ) > len(
    presentation.items
  )

  assert len(
    presentation.items
  ) == 2

  assert (
    presentation.items[
      0
    ].statement_latex
    == r"H\left(\nu'\right) = \eta_{5}"
  )

  assert (
    presentation.items[
      1
    ].statement_latex
    == r"H\left(\nu'\right) = E^{2}\eta_{3}"
  )

  assert (
    presentation.items[
      0
    ].provenance_count
    > 1
  )

  assert (
    presentation.items[
      1
    ].provenance_count
    > 1
  )


def test_phase110_8_h_nu_prime_prioritizes_shallower_fact():
  result = (
    query_standard_repository_operation_input(
      "H(nu_prime)"
    )
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

  assert (
    presentation.items[
      0
    ].primary_match
    .scope_node
    .shortest_depth
    == 3
  )

  assert (
    presentation.items[
      1
    ].primary_match
    .scope_node
    .shortest_depth
    == 4
  )


def test_phase110_8_delta_iota9_deduplicates_to_two_facts():
  result = (
    query_standard_repository_operation_input(
      "Delta(iota_9)"
    )
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

  assert len(
    presentation.items
  ) == 2

  latex_values = tuple(
    item.statement_latex
    for item in presentation.items
  )

  assert (
    r"\Delta\left(\iota_{9}\right) = "
    r"\pm \left(2\nu_{4} - E\nu'\right)"
  ) in latex_values

  assert (
    r"\Delta\left(\iota_{9}\right) = "
    r"\pm [\iota_{4}, \iota_{4}]"
  ) in latex_values


def test_phase110_8_e_eta2_nu_prime_deduplicates_to_one_fact():
  result = (
    query_standard_repository_operation_input(
      "E(eta_2 o nu_prime)"
    )
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

  assert len(
    result.matches
  ) > 1

  assert len(
    presentation.items
  ) == 1

  assert (
    presentation.items[
      0
    ].statement_latex
    == r"E\eta_{2}\nu' = 0"
  )


def test_phase110_8_composition_suppresses_unrenderable_container_statement():
  result = (
    query_standard_repository_operation_input(
      "eta_2 o nu_prime"
    )
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

  markdown = (
    render_repository_operation_query_markdown(
      presentation
    )
  )

  assert (
    "TodaProp58FiniteDimensionalStatement("
    not in markdown
  )

  assert (
    r"$\pi_{6}^{2} = "
    r"\mathbb{Z}/4\{\eta_{2}\nu'\}$"
    in markdown
  )

  assert (
    r"$E\eta_{2}\nu' = 0$"
    in markdown
  )

  assert (
    r"$\Delta\left(\nu_{5}\right) = "
    r"\pm \eta_{2}\nu'$"
    in markdown
  )


def test_phase110_8_composition_deduplicates_renderable_statements():
  result = (
    query_standard_repository_operation_input(
      "eta_2 o nu_prime"
    )
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

  assert len(
    result.matches
  ) > len(
    presentation.items
  )

  statement_latex_values = tuple(
    item.statement_latex
    for item in presentation.items
  )

  assert len(
    statement_latex_values
  ) == len(
    set(
      statement_latex_values
    )
  )


def test_phase110_8_presentation_preserves_raw_lookup_result():
  result = (
    query_standard_repository_operation_input(
      "H(nu_prime)"
    )
  )

  before_matches = (
    result.matches
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

  assert (
    presentation.source_result
    is result
  )

  assert (
    result.matches
    is before_matches
  )

  assert len(
    result.matches
  ) > len(
    presentation.items
  )


def test_phase110_8_presentation_is_deterministic():
  first = (
    build_repository_operation_query_presentation(
      query_standard_repository_operation_input(
        "eta_2 o nu_prime"
      )
    )
  )

  second = (
    build_repository_operation_query_presentation(
      query_standard_repository_operation_input(
        "eta_2 o nu_prime"
      )
    )
  )

  assert tuple(
    (
      item.statement_latex,
      item.primary_match.scope_node.shortest_depth,
      item.provenance_count,
    )
    for item in first.items
  ) == tuple(
    (
      item.statement_latex,
      item.primary_match.scope_node.shortest_depth,
      item.provenance_count,
    )
    for item in second.items
  )
