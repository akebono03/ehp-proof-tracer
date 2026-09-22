from web_operation_query import (
  build_standard_web_operation_query_view,
)


def test_phase118_2_h_nu_prime_exposes_two_existing_facts():
  view = (
    build_standard_web_operation_query_view(
      "H(nu_prime)"
    )
  )

  assert view.found

  assert len(
    view.items
  ) == 2

  assert (
    view.items[
      0
    ].statement_latex
    == r"H\left(\nu'\right) = \eta_{5}"
  )

  assert (
    view.items[
      1
    ].statement_latex
    == r"H\left(\nu'\right) = E^{2}\eta_{3}"
  )


def test_phase118_2_h_nu_prime_preserves_provenance_counts():
  view = (
    build_standard_web_operation_query_view(
      "H(nu_prime)"
    )
  )

  assert all(
    item.provenance_count > 1
    for item in view.items
  )


def test_phase118_2_delta_iota9_exposes_multiple_facts_without_selection():
  view = (
    build_standard_web_operation_query_view(
      "Delta(iota_9)"
    )
  )

  assert view.found

  assert len(
    view.items
  ) == 2

  latex_values = tuple(
    item.statement_latex
    for item in view.items
  )

  assert (
    r"\Delta\left(\iota_{9}\right) = "
    r"\pm \left(2\nu_{4} - E\nu'\right)"
  ) in latex_values

  assert (
    r"\Delta\left(\iota_{9}\right) = "
    r"\pm [\iota_{4}, \iota_{4}]"
  ) in latex_values


def test_phase118_2_e_nu5_uses_existing_handoff():
  view = (
    build_standard_web_operation_query_view(
      "E(nu_5)"
    )
  )

  assert view.found

  assert len(
    view.items
  ) == 1

  assert (
    r"\nu_{5}"
    in view.items[
      0
    ].statement_latex
  )

  assert (
    r"\nu_{6}"
    in view.items[
      0
    ].statement_latex
  )


def test_phase118_2_e_sigma11_uses_existing_handoff():
  view = (
    build_standard_web_operation_query_view(
      "E(sigma_11)"
    )
  )

  assert view.found

  assert len(
    view.items
  ) == 1

  assert (
    r"\sigma_{11}"
    in view.items[
      0
    ].statement_latex
  )

  assert (
    r"\sigma_{12}"
    in view.items[
      0
    ].statement_latex
  )


def test_phase118_2_missing_operation_query_is_rejected():
  try:
    build_standard_web_operation_query_view(
      "   "
    )
  except ValueError as error:
    assert (
      str(
        error
      )
      == "operation query is required"
    )
  else:
    raise AssertionError(
      "blank operation query must be rejected"
    )


def test_phase118_2_not_found_query_has_no_items():
  view = (
    build_standard_web_operation_query_view(
      "H(sigma_11)"
    )
  )

  assert not view.found
  assert view.items == ()
