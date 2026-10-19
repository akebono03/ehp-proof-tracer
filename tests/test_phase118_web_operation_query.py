from web_operation_query import (
  build_standard_web_operation_query_view,
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
