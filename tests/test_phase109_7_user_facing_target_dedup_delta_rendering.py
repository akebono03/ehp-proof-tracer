from functools import lru_cache

from repository_generator_user_execution_candidate_presentation import (
  build_repository_generator_user_execution_candidate_list_presentation,
)
from repository_generator_user_execution_candidate_renderer import (
  render_repository_generator_user_execution_candidate_list_markdown,
)
from repository_generator_user_execution_facade import (
  RepositoryGeneratorUserExecutionWorkflowStatus,
  run_standard_repository_generator_user_execution_workflow,
)
from repository_generator_user_execution_resolver import (
  resolve_standard_repository_generator_executable_targets_input,
)


@lru_cache(maxsize=1)
def _phase109_7_resolution():
  return (
    resolve_standard_repository_generator_executable_targets_input(
      "nu_prime"
    )
  )


@lru_cache(maxsize=1)
def _phase109_7_workflow():
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


def test_phase109_7_nu_prime_user_facing_targets_are_deduplicated_to_two():
  resolution = _phase109_7_resolution()

  assert len(
    resolution.targets
  ) == 2


def test_phase109_7_nu_prime_user_facing_targets_have_distinct_goals():
  resolution = _phase109_7_resolution()

  first_goal = (
    resolution.targets[
      0
    ].goal
  )
  second_goal = (
    resolution.targets[
      1
    ].goal
  )

  assert first_goal != second_goal


def test_phase109_7_dedup_preserves_original_family_group_identity():
  resolution = _phase109_7_resolution()

  original_group_ids = {
    id(
      group
    )
    for group in resolution.family_grouping.groups
  }

  assert all(
    id(
      target.group
    )
    in original_group_ids
    for target in resolution.targets
  )


def test_phase109_7_candidate_numbers_are_one_and_two_after_dedup():
  presentation = (
    build_repository_generator_user_execution_candidate_list_presentation(
      _phase109_7_workflow()
    )
  )

  assert tuple(
    candidate.candidate_number
    for candidate in presentation.candidates
  ) == (
    1,
    2,
  )


def test_phase109_7_candidate_renderer_uses_human_readable_delta_statement():
  presentation = (
    build_repository_generator_user_execution_candidate_list_presentation(
      _phase109_7_workflow()
    )
  )

  markdown = (
    render_repository_generator_user_execution_candidate_list_markdown(
      presentation
    )
  )

  assert (
    r"\Delta\left(\iota_{9}\right)"
    in markdown
  )
  assert (
    r"= \pm "
    in markdown
  )


def test_phase109_7_candidate_renderer_hides_delta_dataclass_repr():
  presentation = (
    build_repository_generator_user_execution_candidate_list_presentation(
      _phase109_7_workflow()
    )
  )

  markdown = (
    render_repository_generator_user_execution_candidate_list_markdown(
      presentation
    )
  )

  assert (
    "TodaDeltaImageUpToSignStatement"
    not in markdown
  )
  assert (
    "TodaDeltaMap("
    not in markdown
  )
  assert (
    "HomotopyElement("
    not in markdown
  )


def test_phase109_7_candidate_one_still_executes_after_dedup():
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
  assert result.selected_target is not None
  assert (
    result.selected_target
    is result.resolution.targets[
      0
    ]
  )


def test_phase109_7_candidate_two_still_executes_after_dedup():
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
  assert result.selected_target is not None
  assert (
    result.selected_target
    is result.resolution.targets[
      1
    ]
  )
