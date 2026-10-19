from functools import lru_cache

import pytest

from repository_generator_user_execution_candidate_presentation import (
  RepositoryGeneratorUserExecutionCandidateListPresentation,
  RepositoryGeneratorUserExecutionCandidatePresentation,
  build_repository_generator_user_execution_candidate_list_presentation,
)
from repository_generator_user_execution_candidate_renderer import (
  render_repository_generator_user_execution_candidate_list_markdown,
)
from repository_generator_user_execution_facade import (
  RepositoryGeneratorUserExecutionWorkflowStatus,
  run_standard_repository_generator_user_execution_workflow,
)


@lru_cache(maxsize=1)
def _phase108_10_ambiguous_result():
  result = (
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime"
    )
  )

  assert (
    result.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
  )

  return result


def test_phase108_10_builds_candidate_list_from_ambiguous_workflow():
  result = (
    _phase108_10_ambiguous_result()
  )

  presentation = (
    build_repository_generator_user_execution_candidate_list_presentation(
      result
    )
  )

  assert isinstance(
    presentation,
    RepositoryGeneratorUserExecutionCandidateListPresentation,
  )

  assert (
    presentation.source_result
    is result
  )

  assert len(
    presentation.candidates
  ) == len(
    result.resolution.targets
  )


def test_phase108_10_preserves_target_identity_and_order():
  result = (
    _phase108_10_ambiguous_result()
  )

  presentation = (
    build_repository_generator_user_execution_candidate_list_presentation(
      result
    )
  )

  assert all(
    candidate.source_target
    is source_target
    for candidate, source_target in zip(
      presentation.candidates,
      result.resolution.targets,
    )
  )


def test_phase108_10_candidate_numbers_are_consecutive_and_one_based():
  presentation = (
    build_repository_generator_user_execution_candidate_list_presentation(
      _phase108_10_ambiguous_result()
    )
  )

  assert tuple(
    candidate.candidate_number
    for candidate in presentation.candidates
  ) == tuple(
    range(
      1,
      len(
        presentation.candidates
      ) + 1,
    )
  )


def test_phase108_10_candidate_conclusion_preserves_target_goal_identity():
  presentation = (
    build_repository_generator_user_execution_candidate_list_presentation(
      _phase108_10_ambiguous_result()
    )
  )

  assert all(
    candidate.conclusion
    is candidate.source_target.goal
    for candidate in presentation.candidates
  )


def test_phase108_10_renders_numbered_candidate_list():
  presentation = (
    build_repository_generator_user_execution_candidate_list_presentation(
      _phase108_10_ambiguous_result()
    )
  )

  markdown = (
    render_repository_generator_user_execution_candidate_list_markdown(
      presentation
    )
  )

  assert markdown.startswith(
    "# Executable candidates\n"
  )

  numbered_lines = tuple(
    line
    for line in markdown.splitlines()
    if (
      len(
        line
      ) >= 3
      and line[
        0
      ].isdigit()
      and ". " in line
    )
  )

  assert len(
    numbered_lines
  ) == len(
    presentation.candidates
  )

  assert markdown.endswith(
    "Select a candidate number to execute.\n"
  )


def test_phase108_10_renderer_does_not_expose_internal_addressing():
  result = (
    _phase108_10_ambiguous_result()
  )

  presentation = (
    build_repository_generator_user_execution_candidate_list_presentation(
      result
    )
  )

  markdown = (
    render_repository_generator_user_execution_candidate_list_markdown(
      presentation
    )
  )

  assert all(
    target.family_name not in markdown
    for target in result.resolution.targets
  )

  assert all(
    target.root_entry.key not in markdown
    for target in result.resolution.targets
  )

  assert "catalog" not in markdown.lower()
  assert "binding" not in markdown.lower()


def test_phase108_10_rejects_non_ambiguous_workflow_result():
  executed_result = (
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime",
      candidate_number=1,
    )
  )

  with pytest.raises(
    ValueError,
    match="result must have AMBIGUOUS status",
  ):
    build_repository_generator_user_execution_candidate_list_presentation(
      executed_result
    )


def test_phase108_10_rejects_non_workflow_result():
  with pytest.raises(
    TypeError,
    match=(
      "result must be a "
      "RepositoryGeneratorUserExecutionWorkflowResult"
    ),
  ):
    build_repository_generator_user_execution_candidate_list_presentation(
      object()
    )


def test_phase108_10_renderer_rejects_non_presentation():
  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "RepositoryGeneratorUserExecutionCandidateListPresentation"
    ),
  ):
    render_repository_generator_user_execution_candidate_list_markdown(
      object()
    )


def test_phase108_10_candidate_presentation_rejects_zero_number():
  result = (
    _phase108_10_ambiguous_result()
  )

  target = result.resolution.targets[
    0
  ]

  with pytest.raises(
    ValueError,
    match="candidate_number must be positive",
  ):
    RepositoryGeneratorUserExecutionCandidatePresentation(
      source_target=target,
      candidate_number=0,
      conclusion=target.goal,
    )
