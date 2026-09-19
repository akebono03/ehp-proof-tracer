from types import SimpleNamespace

import pytest

import main as cli_main
from toda_calculation_result import (
  TodaCalculationStatus,
)


def test_phase101_3_explore_command_uses_production_one_shot_facade(
  monkeypatch,
  capsys,
):
  calls = []

  fake_report = SimpleNamespace(
    markdown=(
      "# $\\nu'$"
      "\n"
      "\n"
      "Occurrences: 3"
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
    (
      fake_explore_standard_repository_generator_input
    ),
  )

  exit_code = cli_main.main(
    [
      "explore",
      "nu_prime",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0
  assert calls == [
    "nu_prime",
  ]
  assert captured.out == (
    fake_report.markdown
  )
  assert captured.err == ""


def test_phase101_3_actual_explore_command_renders_production_report(
  capsys,
):
  exit_code = cli_main.main(
    [
      "explore",
      "nu_prime",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0
  assert (
    "# $\\nu'$"
    in captured.out
  )
  assert (
    "Occurrences:"
    in captured.out
  )
  assert captured.err == ""


def test_phase101_3_explore_zero_occurrence_is_normal_zero_exit(
  capsys,
):
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
  assert (
    "Occurrences: 0"
    in captured.out
  )
  assert captured.err == ""


def test_phase101_3_invalid_generator_uses_argparse_error_exit(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore",
        "not_a_generator",
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert exc_info.value.code == 2
  assert captured.out == ""
  assert (
    "unsupported generator family"
    in captured.err
  )
  assert (
    "Traceback"
    not in captured.err
  )


def test_phase101_3_missing_generator_uses_argparse_error_exit(
  capsys,
):
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
  assert captured.out == ""
  assert (
    "generator"
    in captured.err
  )
  assert (
    "Traceback"
    not in captured.err
  )


def test_phase101_3_legacy_n_k_path_is_unchanged(
  monkeypatch,
  capsys,
):
  calls = []

  fake_result = SimpleNamespace(
    status=(
      TodaCalculationStatus.FOUND
    ),
    reports=(
      "LEGACY REPORT",
    ),
  )

  def fake_build_standard_toda_report(
    n: int,
    k: int,
  ):
    calls.append(
      (
        n,
        k,
      )
    )
    return fake_result

  monkeypatch.setattr(
    cli_main,
    "build_standard_toda_report",
    fake_build_standard_toda_report,
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
  assert calls == [
    (
      5,
      7,
    )
  ]
  assert captured.out == (
    "LEGACY REPORT\n"
  )
  assert captured.err == ""
