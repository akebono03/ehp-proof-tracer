from functools import lru_cache

import main as cli_main
from repository_generator_user_execution_facade import (
  RepositoryGeneratorUserExecutionWorkflowStatus,
  run_standard_repository_generator_user_execution_workflow,
)


@lru_cache(maxsize=1)
def _phase109_5_ambiguous_result():
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


def test_phase109_5_execute_nu_prime_shows_identity_before_candidates(
  capsys,
):
  exit_code = cli_main.main(
    [
      "execute",
      "nu_prime",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  generator_position = captured.out.index(
    "# Generator"
  )
  known_group_position = captured.out.index(
    "# Known group"
  )
  candidates_position = captured.out.index(
    "# Executable candidates"
  )

  assert (
    generator_position
    < known_group_position
    < candidates_position
  )

  assert (
    r"$\nu'$"
    in captured.out
  )
  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in captured.out
  )


def test_phase109_5_execute_nu_prime_preserves_existing_candidate_numbering(
  capsys,
):
  result = _phase109_5_ambiguous_result()

  exit_code = cli_main.main(
    [
      "execute",
      "nu_prime",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0

  numbered_lines = tuple(
    line
    for line in captured.out.splitlines()
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
    result.resolution.targets
  )

  assert tuple(
    int(
      line.split(
        ".",
        maxsplit=1,
      )[
        0
      ]
    )
    for line in numbered_lines
  ) == tuple(
    range(
      1,
      len(
        result.resolution.targets
      ) + 1,
    )
  )


def test_phase109_5_execute_candidate_path_does_not_prepend_identity(
  capsys,
):
  exit_code = cli_main.main(
    [
      "execute",
      "nu_prime",
      "--candidate",
      "1",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  assert "# Generator" not in captured.out
  assert "# Known group" not in captured.out
  assert "# Executable candidates" not in captured.out

  assert "# Result" in captured.out
