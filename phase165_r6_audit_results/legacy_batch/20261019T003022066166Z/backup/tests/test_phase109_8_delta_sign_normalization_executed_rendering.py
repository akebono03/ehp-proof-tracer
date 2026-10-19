from functools import lru_cache

from expression import (
  Multiple,
  Sum,
  Suspension,
)
from repository_generator_user_execution_facade import (
  RepositoryGeneratorUserExecutionWorkflowStatus,
  run_standard_repository_generator_user_execution_workflow,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)


@lru_cache(maxsize=1)
def _phase109_8_candidate_two_result():
  result = (
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime",
      candidate_number=2,
    )
  )

  assert (
    result.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
  )

  return result


def test_phase109_8_multiple_minus_one_omits_literal_minus_one():
  result = _phase109_8_candidate_two_result()

  positive_value = (
    result
    .selected_target
    .goal
    .positive_value
  )

  assert isinstance(
    positive_value,
    Sum,
  )
  assert isinstance(
    positive_value.right,
    Multiple,
  )
  assert (
    positive_value.right.coefficient
    == -1
  )

  rendered = (
    render_toda_expression_latex(
      positive_value.right
    )
  )

  assert rendered.startswith(
    "-"
  )
  assert "-1" not in rendered


def test_phase109_8_sum_with_negative_multiple_renders_subtraction():
  result = _phase109_8_candidate_two_result()

  positive_value = (
    result
    .selected_target
    .goal
    .positive_value
  )

  rendered = (
    render_toda_expression_latex(
      positive_value
    )
  )

  assert " + -1" not in rendered
  assert " - " in rendered
  assert (
    rendered
    == r"2\nu_{4} - E\nu'"
  )


def test_phase109_8_candidate_two_result_renders_delta_mathematically():
  result = _phase109_8_candidate_two_result()

  assert result.markdown is not None

  assert (
    r"$\Delta\left(\iota_{9}\right) = "
    r"\pm \left(2\nu_{4} - E\nu'\right)$"
    in result.markdown
  )


def test_phase109_8_candidate_two_result_hides_internal_delta_repr():
  result = _phase109_8_candidate_two_result()

  assert result.markdown is not None

  assert (
    "TodaDeltaImageUpToSignStatement"
    not in result.markdown
  )
  assert (
    "TodaDeltaMap("
    not in result.markdown
  )


def test_phase109_8_candidate_two_conclusion_matches_result_rendering():
  result = _phase109_8_candidate_two_result()

  assert result.markdown is not None

  expected = (
    r"$\Delta\left(\iota_{9}\right) = "
    r"\pm \left(2\nu_{4} - E\nu'\right)$"
  )

  assert (
    result.markdown.count(
      expected
    )
    == 2
  )


def test_phase109_8_candidate_one_execution_remains_available():
  result = (
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime",
      candidate_number=1,
    )
  )

  assert (
    result.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
  )
  assert result.markdown is not None
  assert (
    r"$\pi_{6}^{2} = "
    r"\mathbb{Z}/4\{\eta_{2}\nu'\}$"
    in result.markdown
  )
