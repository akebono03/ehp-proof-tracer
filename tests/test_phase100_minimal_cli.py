from io import StringIO

from cli import run_cli
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
)
from test_phase99_actual_repository_element_lookup_validation import (
  build_phase99_5_actual_repository,
)


def test_phase100_4_group_command_renders_found_report():
  data = build_phase95_20_data()
  stdout = StringIO()
  stderr = StringIO()

  exit_code = run_cli(
    data[
      "repository"
    ],
    (
      "group",
      "5",
      "4",
    ),
    stdout=stdout,
    stderr=stderr,
  )

  assert exit_code == 0
  assert (
    "# $\\pi_{9}^{5}$"
    in stdout.getvalue()
  )
  assert stderr.getvalue() == ""


def test_phase100_4_group_not_found_is_normal_zero_exit():
  stdout = StringIO()
  stderr = StringIO()

  exit_code = run_cli(
    ProofRepository(),
    (
      "group",
      "9",
      "7",
    ),
    stdout=stdout,
    stderr=stderr,
  )

  assert exit_code == 0
  assert (
    stdout.getvalue()
    == (
      "No theorem-backed result found for "
      "pi_16^9.\n"
    )
  )
  assert stderr.getvalue() == ""


def test_phase100_4_group_multiple_results_preserve_all_reports_and_order():
  phase65 = build_phase65_9_data()

  repository = ProofRepository()

  first_entry = ProofRepositoryEntry(
    key="phase100.cli.first",
    step=phase65[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 first",
  )

  second_entry = ProofRepositoryEntry(
    key="phase100.cli.second",
    step=phase65[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 second",
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  stdout = StringIO()
  stderr = StringIO()

  exit_code = run_cli(
    repository,
    (
      "group",
      "4",
      "3",
    ),
    stdout=stdout,
    stderr=stderr,
  )

  output = stdout.getvalue()

  assert exit_code == 0
  assert (
    output.count(
      "# $\\pi_{7}^{4}$"
    )
    == 2
  )
  assert "\n---\n\n" in output
  assert stderr.getvalue() == ""


def test_phase100_4_group_reuses_existing_query_validation():
  stdout = StringIO()
  stderr = StringIO()

  exit_code = run_cli(
    ProofRepository(),
    (
      "group",
      "0",
      "4",
    ),
    stdout=stdout,
    stderr=stderr,
  )

  assert exit_code == 2
  assert stdout.getvalue() == ""
  assert (
    "n must be positive"
    in stderr.getvalue()
  )


def test_phase100_4_element_command_resolves_ascii_alias_and_renders_markdown():
  data = (
    build_phase99_5_actual_repository()
  )
  stdout = StringIO()
  stderr = StringIO()

  exit_code = run_cli(
    data[
      "repository"
    ],
    (
      "element",
      "nu_prime",
    ),
    stdout=stdout,
    stderr=stderr,
  )

  output = stdout.getvalue()

  assert exit_code == 0
  assert "# $\\nu'$" in output
  assert "Occurrences: 4" in output
  assert "## Group generators" in output
  assert stderr.getvalue() == ""


def test_phase100_4_element_zero_occurrence_is_normal_zero_exit():
  stdout = StringIO()
  stderr = StringIO()

  exit_code = run_cli(
    ProofRepository(),
    (
      "element",
      "eta_2",
    ),
    stdout=stdout,
    stderr=stderr,
  )

  assert exit_code == 0
  assert (
    "Occurrences: 0"
    in stdout.getvalue()
  )
  assert stderr.getvalue() == ""


def test_phase100_4_element_invalid_generator_is_input_error():
  stdout = StringIO()
  stderr = StringIO()

  exit_code = run_cli(
    ProofRepository(),
    (
      "element",
      "not_a_generator",
    ),
    stdout=stdout,
    stderr=stderr,
  )

  assert exit_code == 2
  assert stdout.getvalue() == ""
  assert (
    "error:"
    in stderr.getvalue()
  )


def test_phase100_4_unknown_command_uses_argparse_error_exit():
  stdout = StringIO()
  stderr = StringIO()

  exit_code = run_cli(
    ProofRepository(),
    (
      "unknown",
    ),
    stdout=stdout,
    stderr=stderr,
  )

  assert exit_code == 2
  assert stdout.getvalue() == ""
  assert (
    "invalid choice"
    in stderr.getvalue()
  )


def test_phase100_4_help_uses_zero_exit_and_stdout():
  stdout = StringIO()
  stderr = StringIO()

  exit_code = run_cli(
    ProofRepository(),
    (
      "--help",
    ),
    stdout=stdout,
    stderr=stderr,
  )

  assert exit_code == 0
  assert (
    "group"
    in stdout.getvalue()
  )
  assert (
    "element"
    in stdout.getvalue()
  )
  assert stderr.getvalue() == ""


def test_phase100_4_cli_does_not_mutate_repository():
  data = (
    build_phase99_5_actual_repository()
  )

  repository = data[
    "repository"
  ]

  before = (
    repository.entries()
  )

  stdout = StringIO()
  stderr = StringIO()

  exit_code = run_cli(
    repository,
    (
      "element",
      "nu_prime",
    ),
    stdout=stdout,
    stderr=stderr,
  )

  after = (
    repository.entries()
  )

  assert exit_code == 0
  assert after == before

  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase100_4_rejects_non_repository_programmer_input():
  stdout = StringIO()
  stderr = StringIO()

  try:
    run_cli(
      "not-a-repository",
      (
        "group",
        "5",
        "4",
      ),
      stdout=stdout,
      stderr=stderr,
    )
  except TypeError as error:
    assert (
      str(
        error
      )
      == (
        "repository must be "
        "a ProofRepository"
      )
    )
  else:
    raise AssertionError(
      "TypeError was not raised"
    )
