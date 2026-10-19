import pytest

from web_operation_query_proof import (
  build_standard_web_operation_query_proof_view,
)
















def test_phase118_3_nonpositive_fact_number_is_rejected():
  with pytest.raises(
    ValueError,
    match="fact_number must be positive",
  ):
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=0,
    )
