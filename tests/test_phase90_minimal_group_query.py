import pytest

from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_group_query import (
  TodaGroupQuery,
)


def test_phase90_2_query_preserves_n_and_k():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  assert query.n == 4
  assert query.k == 6


def test_phase90_2_query_constructs_toda_primary_group_target():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  assert (
    query.target
    == TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=4,
    )
  )


def test_phase90_2_query_supports_zero_stem_boundary():
  query = TodaGroupQuery(
    n=5,
    k=0,
  )

  assert (
    query.target
    == TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )
  )


@pytest.mark.parametrize(
  ("field_name", "value"),
  (
    ("n", True),
    ("n", 4.0),
    ("n", "4"),
    ("k", False),
    ("k", 6.0),
    ("k", "6"),
  ),
)
def test_phase90_2_query_rejects_non_integer_inputs(
  field_name,
  value,
):
  kwargs = {
    "n": 4,
    "k": 6,
  }
  kwargs[field_name] = value

  with pytest.raises(
    TypeError,
  ):
    TodaGroupQuery(
      **kwargs
    )


@pytest.mark.parametrize(
  "n",
  (
    0,
    -1,
  ),
)
def test_phase90_2_query_requires_positive_n(
  n,
):
  with pytest.raises(
    ValueError,
  ):
    TodaGroupQuery(
      n=n,
      k=0,
    )


@pytest.mark.parametrize(
  "k",
  (
    -1,
    -6,
  ),
)
def test_phase90_2_query_requires_nonnegative_k(
  k,
):
  with pytest.raises(
    ValueError,
  ):
    TodaGroupQuery(
      n=4,
      k=k,
    )
