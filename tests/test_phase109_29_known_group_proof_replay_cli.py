import main as cli_main
import pytest

from expression import (
  GeneratorSymbol,
)
from repository_generator_known_group_proof_replay import (
  RepositoryGeneratorKnownGroupProofReplayResult,
  build_standard_repository_generator_known_group_proof_replay_input,
)
from repository_generator_known_group_proof_replay_presentation import (
  RepositoryGeneratorKnownGroupProofReplayPresentation,
  build_repository_generator_known_group_proof_replay_presentation,
)
from repository_generator_known_group_proof_replay_renderer import (
  render_repository_generator_known_group_proof_replay_markdown,
)
from repository_generator_user_execution_facade import (
  RepositoryGeneratorUserExecutionWorkflowStatus,
  run_standard_repository_generator_user_execution_workflow,
)


def test_phase109_29_sigma11_replay_preserves_unique_known_group_source():
  result = (
    build_standard_repository_generator_known_group_proof_replay_input(
      "sigma_11"
    )
  )

  assert isinstance(
    result,
    RepositoryGeneratorKnownGroupProofReplayResult,
  )

  assert (
    result.generator
    == GeneratorSymbol(
      family="σ",
      index=11,
    )
  )

  assert (
    result.root_step
    is result.source_node.proof_step
  )

  assert (
    result.root_step.conclusion.lhs.group_dimension
    == 18
  )

  assert (
    result.root_step.conclusion.lhs.sphere_dimension
    == 11
  )

  assert (
    result.root_step.conclusion.rhs.order
    == 16
  )


def test_phase109_29_default_replay_depth_is_result_plus_direct_premise():
  result = (
    build_standard_repository_generator_known_group_proof_replay_input(
      "sigma_11"
    )
  )

  assert result.max_depth == 1

  assert tuple(
    step.depth
    for step in result.steps
  ) == (
    0,
    1,
  )

  assert (
    result.steps[
      0
    ].proof_step
    is result.root_step
  )

  assert (
    result.steps[
      1
    ].proof_step
    is result.root_step.premises[
      0
    ]
  )


def test_phase109_29_zero_depth_replay_contains_only_result():
  result = (
    build_standard_repository_generator_known_group_proof_replay_input(
      "sigma_11",
      max_depth=0,
    )
  )

  assert len(
    result.steps
  ) == 1

  assert result.steps[
    0
  ].depth == 0

  assert (
    result.steps[
      0
    ].proof_step
    is result.root_step
  )


def test_phase109_29_depth_two_replay_keeps_existing_proofstep_identities():
  result = (
    build_standard_repository_generator_known_group_proof_replay_input(
      "sigma_11",
      max_depth=2,
    )
  )

  symbolic_step = (
    result.root_step.premises[
      0
    ]
  )

  replay_step_ids = {
    id(
      replay_step.proof_step
    )
    for replay_step in result.steps
  }

  assert id(
    result.root_step
  ) in replay_step_ids

  assert id(
    symbolic_step
  ) in replay_step_ids

  assert all(
    id(
      premise
    )
    in replay_step_ids
    for premise in symbolic_step.premises
  )


def test_phase109_29_replay_rejects_invalid_max_depth():
  with pytest.raises(
    TypeError,
    match="max_depth must be an int",
  ):
    build_standard_repository_generator_known_group_proof_replay_input(
      "sigma_11",
      max_depth=True,
    )

  with pytest.raises(
    ValueError,
    match="max_depth must be nonnegative",
  ):
    build_standard_repository_generator_known_group_proof_replay_input(
      "sigma_11",
      max_depth=-1,
    )


def test_phase109_29_presentation_preserves_replay_result_identity():
  result = (
    build_standard_repository_generator_known_group_proof_replay_input(
      "sigma_11"
    )
  )

  presentation = (
    build_repository_generator_known_group_proof_replay_presentation(
      result
    )
  )

  assert isinstance(
    presentation,
    RepositoryGeneratorKnownGroupProofReplayPresentation,
  )

  assert (
    presentation.source_result
    is result
  )

  assert (
    presentation.generator
    is result.generator
  )

  assert (
    presentation.conclusion
    is result.root_step.conclusion
  )

  assert (
    presentation.steps
    == result.steps
  )


def test_phase109_29_renderer_shows_result_and_direct_symbolic_provenance():
  result = (
    build_standard_repository_generator_known_group_proof_replay_input(
      "sigma_11"
    )
  )

  presentation = (
    build_repository_generator_known_group_proof_replay_presentation(
      result
    )
  )

  markdown = (
    render_repository_generator_known_group_proof_replay_markdown(
      presentation
    )
  )

  assert "# Generator" in markdown
  assert "# Result" in markdown
  assert "## Proof" in markdown

  assert (
    r"$\sigma_{11}$"
    in markdown
  )

  assert (
    r"$\pi_{18}^{11} = \mathbb{Z}/16\{\sigma_{11}\}$"
    in markdown
  )

  assert (
    r"$\pi_{n + 7}^{n} = \mathbb{Z}/16\{\sigma_{n}\}$"
    in markdown
  )

  assert "Depth 0" in markdown
  assert "Depth 1" in markdown


def test_phase109_29_show_proof_cli_renders_sigma11_replay(
  capsys,
):
  exit_code = cli_main.main(
    [
      "show-proof",
      "sigma_11",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  assert "# Generator" in captured.out
  assert "# Result" in captured.out
  assert "## Proof" in captured.out

  assert (
    r"$\pi_{18}^{11} = \mathbb{Z}/16\{\sigma_{11}\}$"
    in captured.out
  )

  assert (
    r"$\pi_{n + 7}^{n} = \mathbb{Z}/16\{\sigma_{n}\}$"
    in captured.out
  )


def test_phase109_29_show_proof_does_not_change_execute_sigma11_semantics(
  capsys,
):
  replay_exit_code = cli_main.main(
    [
      "show-proof",
      "sigma_11",
    ]
  )

  capsys.readouterr()

  workflow = (
    run_standard_repository_generator_user_execution_workflow(
      "sigma_11"
    )
  )

  execute_exit_code = cli_main.main(
    [
      "execute",
      "sigma_11",
    ]
  )

  captured = capsys.readouterr()

  assert replay_exit_code == 0

  assert (
    workflow.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.NONE
  )

  assert execute_exit_code == 1

  assert (
    "No executable target found for sigma_11."
    in captured.out
  )


def test_phase109_29_show_proof_also_works_for_existing_nu_prime_identity(
  capsys,
):
  exit_code = cli_main.main(
    [
      "show-proof",
      "nu_prime",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in captured.out
  )
