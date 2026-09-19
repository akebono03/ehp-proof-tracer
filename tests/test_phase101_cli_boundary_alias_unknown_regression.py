from types import SimpleNamespace

import pytest

import main as cli_main
from toda_calculation_result import (
  TodaCalculationStatus,
)


@pytest.mark.parametrize(
  "value",
  (
    "ν′",
    "ν'",
    "nu'",
    "nu_prime",
  ),
)
def test_phase101_5_explore_aliases_reach_production_facade_unchanged(
  monkeypatch,
  capsys,
  value,
):
  calls = []

  fake_report = SimpleNamespace(
    markdown=(
      "# $\\nu'$"
      "\n"
      "\n"
      "Occurrences: 1"
      "\n"
    ),
  )

  def fake_explore_standard_repository_generator_input(
    generator_input: str,
  ):
    calls.append(
      generator_input
    )
    return fake_report

  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_"
      "repository_generator_input"
    ),
    fake_explore_standard_repository_generator_input,
  )

  exit_code = cli_main.main(
    [
      "explore",
      value,
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0
  assert calls == [
    value,
  ]
  assert captured.out == (
    fake_report.markdown
  )
  assert captured.err == ""


@pytest.mark.parametrize(
  "value",
  (
    "eta_2",
    "nu_5",
  ),
)
def test_phase101_5_indexed_generator_input_reaches_facade_unchanged(
  monkeypatch,
  capsys,
  value,
):
  calls = []

  fake_report = SimpleNamespace(
    markdown=(
      "# generator"
      "\n"
      "\n"
      "Occurrences: 1"
      "\n"
    ),
  )

  def fake_explore_standard_repository_generator_input(
    generator_input: str,
  ):
    calls.append(
      generator_input
    )
    return fake_report

  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_"
      "repository_generator_input"
    ),
    fake_explore_standard_repository_generator_input,
  )

  exit_code = cli_main.main(
    [
      "explore",
      value,
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0
  assert calls == [
    value,
  ]
  assert captured.out == (
    fake_report.markdown
  )
  assert captured.err == ""


def test_phase101_5_zero_occurrence_is_stdout_and_zero_exit(
  monkeypatch,
  capsys,
):
  fake_report = SimpleNamespace(
    markdown=(
      "# $\\eta_{999}$"
      "\n"
      "\n"
      "Occurrences: 0"
      "\n"
    ),
  )

  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_"
      "repository_generator_input"
    ),
    lambda generator_input: fake_report,
  )

  exit_code = cli_main.main(
    [
      "explore",
      "eta_999",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0
  assert captured.out == (
    fake_report.markdown
  )
  assert captured.err == ""


@pytest.mark.parametrize(
  (
    "value",
    "message",
  ),
  (
    (
      "not_a_generator",
      "unsupported generator family",
    ),
    (
      "nu prime",
      "unsupported generator input",
    ),
    (
      "eta_0",
      "generator index must be positive",
    ),
  ),
)
def test_phase101_5_invalid_generator_is_argparse_error_on_stderr(
  monkeypatch,
  capsys,
  value,
  message,
):
  def fake_explore_standard_repository_generator_input(
    generator_input: str,
  ):
    raise ValueError(
      message
    )

  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_"
      "repository_generator_input"
    ),
    fake_explore_standard_repository_generator_input,
  )

  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore",
        value,
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert exc_info.value.code == 2
  assert captured.out == ""
  assert message in captured.err
  assert "usage:" in captured.err
  assert "Traceback" not in captured.err


def test_phase101_5_missing_explore_argument_is_argparse_error_without_facade_call(
  monkeypatch,
  capsys,
):
  calls = []

  def fail_if_called(
    generator_input: str,
  ):
    calls.append(
      generator_input
    )
    raise AssertionError(
      "exploration facade must not be called"
    )

  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_"
      "repository_generator_input"
    ),
    fail_if_called,
  )

  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore",
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert exc_info.value.code == 2
  assert calls == []
  assert captured.out == ""
  assert "generator" in captured.err
  assert "Traceback" not in captured.err


def test_phase101_5_extra_explore_argument_is_argparse_error_without_facade_call(
  monkeypatch,
  capsys,
):
  calls = []

  def fail_if_called(
    generator_input: str,
  ):
    calls.append(
      generator_input
    )
    raise AssertionError(
      "exploration facade must not be called"
    )

  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_"
      "repository_generator_input"
    ),
    fail_if_called,
  )

  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore",
        "nu_prime",
        "extra",
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert exc_info.value.code == 2
  assert calls == []
  assert captured.out == ""
  assert (
    "unrecognized arguments: extra"
    in captured.err
  )
  assert "Traceback" not in captured.err


def test_phase101_5_explore_help_is_stdout_zero_exit_and_does_not_call_facade(
  monkeypatch,
  capsys,
):
  calls = []

  def fail_if_called(
    generator_input: str,
  ):
    calls.append(
      generator_input
    )
    raise AssertionError(
      "exploration facade must not be called"
    )

  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_"
      "repository_generator_input"
    ),
    fail_if_called,
  )

  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore",
        "--help",
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert exc_info.value.code == 0
  assert calls == []
  assert (
    "main.py explore"
    in captured.out
  )
  assert (
    "generator"
    in captured.out
  )
  assert captured.err == ""


def test_phase101_5_unknown_top_level_token_does_not_reach_either_facade(
  monkeypatch,
  capsys,
):
  calculation_calls = []
  exploration_calls = []

  def fail_calculation(
    n: int,
    k: int,
  ):
    calculation_calls.append(
      (
        n,
        k,
      )
    )
    raise AssertionError(
      "calculation facade must not be called"
    )

  def fail_exploration(
    generator_input: str,
  ):
    exploration_calls.append(
      generator_input
    )
    raise AssertionError(
      "exploration facade must not be called"
    )

  monkeypatch.setattr(
    cli_main,
    "build_standard_toda_report",
    fail_calculation,
  )
  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_"
      "repository_generator_input"
    ),
    fail_exploration,
  )

  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "unknown",
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert exc_info.value.code == 2
  assert calculation_calls == []
  assert exploration_calls == []
  assert captured.out == ""
  assert captured.err != ""
  assert "Traceback" not in captured.err


def test_phase101_5_legacy_n_k_path_still_uses_only_calculation_facade(
  monkeypatch,
  capsys,
):
  calculation_calls = []
  exploration_calls = []

  fake_result = SimpleNamespace(
    status=(
      TodaCalculationStatus.FOUND
    ),
    reports=(
      "LEGACY REPORT",
    ),
  )

  def fake_calculation(
    n: int,
    k: int,
  ):
    calculation_calls.append(
      (
        n,
        k,
      )
    )
    return fake_result

  def fail_exploration(
    generator_input: str,
  ):
    exploration_calls.append(
      generator_input
    )
    raise AssertionError(
      "exploration facade must not be called"
    )

  monkeypatch.setattr(
    cli_main,
    "build_standard_toda_report",
    fake_calculation,
  )
  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_"
      "repository_generator_input"
    ),
    fail_exploration,
  )

  exit_code = cli_main.main(
    [
      "5",
      "7",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0
  assert calculation_calls == [
    (
      5,
      7,
    )
  ]
  assert exploration_calls == []
  assert captured.out == (
    "LEGACY REPORT\n"
  )
  assert captured.err == ""


def test_phase101_5_legacy_not_found_exit_code_remains_one(
  monkeypatch,
  capsys,
):
  fake_result = SimpleNamespace(
    status=(
      TodaCalculationStatus.NOT_FOUND
    ),
    reports=(),
  )

  monkeypatch.setattr(
    cli_main,
    "build_standard_toda_report",
    lambda n, k: fake_result,
  )

  exit_code = cli_main.main(
    [
      "20",
      "20",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 1
  assert (
    captured.out
    == (
      "No proof report found for "
      "pi_{40}^{20}.\n"
    )
  )
  assert captured.err == ""
