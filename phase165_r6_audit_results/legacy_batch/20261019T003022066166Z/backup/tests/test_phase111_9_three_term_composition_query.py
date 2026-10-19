import pytest

from expression import (
  Composition,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from repository_operation_query import (
  RepositoryThreeTermCompositionQuery,
  parse_repository_operation_query,
)
from repository_operation_query_facade import (
  query_standard_repository_operation_input,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryMatchKind,
)
from repository_operation_query_presentation import (
  build_repository_operation_query_presentation,
)
from repository_operation_query_renderer import (
  render_repository_operation_query_markdown,
)


def test_phase111_9_parses_flat_three_term_composition():
  query = (
    parse_repository_operation_query(
      "eta_2 o nu_prime o eta_6"
    )
  )

  assert isinstance(
    query,
    RepositoryThreeTermCompositionQuery,
  )

  assert query.first.generator.family == "η"
  assert query.first.generator.index == 2
  assert query.second.generator.family == "ν"
  assert query.second.generator.decoration == "′"
  assert query.third.generator.family == "η"
  assert query.third.generator.index == 6


def test_phase111_9_three_term_query_finds_existing_pi7_2_fact():
  result = (
    query_standard_repository_operation_input(
      "eta_2 o nu_prime o eta_6"
    )
  )

  assert result.found

  match = next(
    match
    for match in result.matches
    if (
      isinstance(
        match.statement,
        Relation,
      )
      and (
        match.statement.relation_type
        is RelationType.EQUALITY
      )
      and (
        match.statement.lhs
        == TodaPrimaryGroup(
          group_dimension=7,
          sphere_dimension=2,
        )
      )
      and isinstance(
        match.statement.rhs,
        FiniteCyclicGroup,
      )
      and match.statement.rhs.order == 2
      and isinstance(
        match.statement.rhs.generator,
        Composition,
      )
      and isinstance(
        match.statement.rhs.generator.right,
        Composition,
      )
    )
  )

  assert (
    match.match_kind
    is RepositoryOperationQueryMatchKind.COMPOSITION_CONTAINMENT
  )

  generator = match.statement.rhs.generator

  assert generator.left.generator.family == "η"
  assert generator.left.generator.index == 2
  assert generator.right.left.generator.family == "ν"
  assert generator.right.left.generator.decoration == "′"
  assert generator.right.right.generator.family == "η"
  assert generator.right.right.generator.index == 6


def test_phase111_9_three_term_query_renders_pi7_2_fact():
  result = (
    query_standard_repository_operation_input(
      "eta_2 o nu_prime o eta_6"
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
    r"$\pi_{7}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\}$"
    in markdown
  )


def test_phase111_9_map_operation_three_term_operand_remains_out_of_scope():
  with pytest.raises(
    ValueError,
    match=(
      "map-operation composition operands support "
      "exactly two generators"
    ),
  ):
    parse_repository_operation_query(
      "E(eta_2 o nu_prime o eta_6)"
    )


def test_phase111_9_four_term_composition_remains_out_of_scope():
  with pytest.raises(
    ValueError,
    match=(
      "composition query supports exactly two "
      "or three generators"
    ),
  ):
    parse_repository_operation_query(
      "eta_2 o nu_prime o eta_6 o eta_7"
    )
