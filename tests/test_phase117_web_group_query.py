import pytest

from toda_calculation_result import (
  TodaCalculationStatus,
)
from web_group_query import (
  build_standard_web_group_query_view,
)


def test_phase117_1_sigma11_group_query_returns_web_latex():
  view = (
    build_standard_web_group_query_view(
      n=11,
      k=7,
    )
  )

  assert (
    view.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    view.result_latex
    == (
      r"\pi_{18}^{11} \cong "
      r"\mathbb{Z}/16\{\sigma_{11}\}"
    )
  )


def test_phase117_1_not_found_query_has_no_web_latex():
  view = (
    build_standard_web_group_query_view(
      n=20,
      k=20,
    )
  )

  assert (
    view.status
    is TodaCalculationStatus.NOT_FOUND
  )
  assert (
    view.result_latex
    is None
  )


def test_phase117_1_web_adapter_preserves_positive_n_validation():
  with pytest.raises(
    ValueError,
    match="n must be positive",
  ):
    build_standard_web_group_query_view(
      n=0,
      k=7,
    )


def test_phase117_1_web_adapter_preserves_nonnegative_k_validation():
  with pytest.raises(
    ValueError,
    match="k must be nonnegative",
  ):
    build_standard_web_group_query_view(
      n=11,
      k=-1,
    )
