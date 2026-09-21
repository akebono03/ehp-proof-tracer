from types import SimpleNamespace

import pytest

import main as cli_main
from repository_generator_user_execution_facade import (
  RepositoryGeneratorUserExecutionWorkflowStatus,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)


def test_phase108_11_execute_ambiguous_renders_candidate_list(
  monkeypatch,
  capsys,
):
  calls = []

  fake_result = SimpleNamespace(
    status=(
      RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
    ),
  )

  fake_presentation = object()

  def fake_workflow(
    generator_input,
    candidate_number=None,
  ):
    calls.append(
      (
        generator_input,
        candidate_number,
      )
    )
    return fake_result

  monkeypatch.setattr(
    cli_main,
    (
      "run_standard_repository_generator_"
      "user_execution_workflow"
    ),
    fake_workflow,
  )

  monkeypatch.setattr(
    cli_main,
    (
      "build_repository_generator_user_"
      "execution_candidate_list_presentation"
    ),
    lambda result: fake_presentation,
  )

  monkeypatch.setattr(
    cli_main,
    (
      "render_repository_generator_user_"
      "execution_candidate_list_markdown"
    ),
    lambda presentation: (
      "# Executable candidates\n\n"
      "1. target one\n"
      "2. target two\n"
    ),
  )

  exit_code = cli_main.main(
    [
      "execute",
      "nu_prime",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0

  assert calls == [
    (
      "nu_prime",
      None,
    ),
  ]

  assert captured.out == (
    "# Executable candidates\n\n"
    "1. target one\n"
    "2. target two\n"
  )

  assert captured.err == ""


def test_phase108_11_execute_candidate_prints_result_and_proof(
  monkeypatch,
  capsys,
):
  calls = []

  fake_result = SimpleNamespace(
    status=(
      RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
    ),
    markdown=(
      "# Result\n\n"
      "result\n\n"
      "## Proof\n\n"
      "proof\n"
    ),
  )

  def fake_workflow(
    generator_input,
    candidate_number=None,
  ):
    calls.append(
      (
        generator_input,
        candidate_number,
      )
    )
    return fake_result

  monkeypatch.setattr(
    cli_main,
    (
      "run_standard_repository_generator_"
      "user_execution_workflow"
    ),
    fake_workflow,
  )

  exit_code = cli_main.main(
    [
      "execute",
      "nu_prime",
      "--candidate",
      "2",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0

  assert calls == [
    (
      "nu_prime",
      2,
    ),
  ]

  assert captured.out == fake_result.markdown
  assert captured.err == ""


def test_phase108_11_execute_none_is_exit_one(
  monkeypatch,
  capsys,
):
  fake_result = SimpleNamespace(
    status=(
      RepositoryGeneratorUserExecutionWorkflowStatus.NONE
    ),
  )

  monkeypatch.setattr(
    cli_main,
    (
      "run_standard_repository_generator_"
      "user_execution_workflow"
    ),
    lambda generator_input, candidate_number=None: fake_result,
  )

  exit_code = cli_main.main(
    [
      "execute",
      "eta_999",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 1
  assert captured.out == (
    "No executable target found for eta_999.\n"
  )
  assert captured.err == ""


@pytest.mark.parametrize(
  (
    "argv",
    "message",
  ),
  (
    (
      [
        "execute",
        "not_a_generator",
      ],
      "unsupported generator family",
    ),
    (
      [
        "execute",
        "nu_prime",
        "--candidate",
        "999",
      ],
      "candidate_number exceeds executable target count",
    ),
  ),
)
def test_phase108_11_execute_facade_value_error_is_argparse_error(
  monkeypatch,
  capsys,
  argv,
  message,
):
  def fake_workflow(
    generator_input,
    candidate_number=None,
  ):
    raise ValueError(
      message
    )

  monkeypatch.setattr(
    cli_main,
    (
      "run_standard_repository_generator_"
      "user_execution_workflow"
    ),
    fake_workflow,
  )

  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      argv
    )

  captured = capsys.readouterr()

  assert exc_info.value.code == 2
  assert captured.out == ""
  assert message in captured.err
  assert "Traceback" not in captured.err


def test_phase108_11_execute_candidate_zero_is_parser_error_before_facade(
  monkeypatch,
  capsys,
):
  calls = []

  def fail_if_called(
    generator_input,
    candidate_number=None,
  ):
    calls.append(
      (
        generator_input,
        candidate_number,
      )
    )
    raise AssertionError(
      "workflow must not be called"
    )

  monkeypatch.setattr(
    cli_main,
    (
      "run_standard_repository_generator_"
      "user_execution_workflow"
    ),
    fail_if_called,
  )

  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "execute",
        "nu_prime",
        "--candidate",
        "0",
      ]
    )

  captured = capsys.readouterr()

  assert exc_info.value.code == 2
  assert calls == []
  assert captured.out == ""
  assert "must be positive" in captured.err
  assert "Traceback" not in captured.err


def test_phase108_11_execute_missing_generator_is_parser_error(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "execute",
      ]
    )

  captured = capsys.readouterr()

  assert exc_info.value.code == 2
  assert captured.out == ""
  assert "generator" in captured.err
  assert "Traceback" not in captured.err


def test_phase108_11_execute_help_documents_candidate_flag(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "execute",
        "--help",
      ]
    )

  captured = capsys.readouterr()

  assert exc_info.value.code == 0
  assert "main.py execute" in captured.out
  assert "--candidate" in captured.out
  assert "generator" in captured.out
  assert captured.err == ""


def test_phase108_11_existing_explore_applicable_path_is_unchanged(
  monkeypatch,
  capsys,
):
  fake_result = SimpleNamespace()

  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_repository_"
      "generator_applicability_input"
    ),
    lambda generator_input: fake_result,
  )

  monkeypatch.setattr(
    cli_main,
    (
      "render_repository_generator_"
      "applicability_markdown"
    ),
    lambda result: "APPLICABILITY REPORT\n",
  )

  exit_code = cli_main.main(
    [
      "explore-applicable",
      "nu_prime",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.out == "APPLICABILITY REPORT\n"
  assert captured.err == ""


def test_phase108_11_legacy_n_k_path_is_unchanged(
  monkeypatch,
  capsys,
):
  fake_result = SimpleNamespace(
    status=(
      TodaCalculationStatus.FOUND
    ),
    reports=(
      "LEGACY REPORT",
    ),
  )

  monkeypatch.setattr(
    cli_main,
    "build_standard_toda_report",
    lambda n, k: fake_result,
  )

  exit_code = cli_main.main(
    [
      "5",
      "7",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.out == "LEGACY REPORT\n"
  assert captured.err == ""
