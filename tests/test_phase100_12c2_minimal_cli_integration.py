from types import SimpleNamespace

import pytest

import main as cli_main
from toda_calculation_result import (
  TodaCalculationStatus,
)


def test_phase100_12c2_cli_found_uses_production_one_shot_path(
  capsys,
):
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
  assert (
    "# $\\pi_{12}^{5}$"
    in captured.out
  )
  assert "## Result" in captured.out
  assert "## Source" in captured.out
  assert (
    "## Proof flow"
    in captured.out
  )
  assert (
    "## Readable proof narrative"
    in captured.out
  )
  assert captured.err == ""


def test_phase100_12c2_cli_passes_raw_n_k_to_standard_facade(
  monkeypatch,
  capsys,
):
  calls = []

  fake_result = SimpleNamespace(
    status=(
      TodaCalculationStatus.FOUND
    ),
    reports=(
      "FAKE REPORT",
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
      "4",
      "6",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0
  assert calls == [
    (
      4,
      6,
    )
  ]
  assert captured.out == (
    "FAKE REPORT\n"
  )
  assert captured.err == ""


def test_phase100_12c2_cli_not_found_is_explicit_and_nonzero(
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
  assert captured.out == (
    "No proof report found for "
    "pi_{40}^{20}.\n"
  )
  assert captured.err == ""


def test_phase100_12c2_cli_multiple_results_prints_all_reports_in_order(
  monkeypatch,
  capsys,
):
  fake_result = SimpleNamespace(
    status=(
      TodaCalculationStatus
      .MULTIPLE_RESULTS
    ),
    reports=(
      "FIRST REPORT",
      "SECOND REPORT",
    ),
  )

  monkeypatch.setattr(
    cli_main,
    "build_standard_toda_report",
    lambda n, k: fake_result,
  )

  exit_code = cli_main.main(
    [
      "4",
      "3",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0
  assert captured.out == (
    "FIRST REPORT"
    "\n\n---\n\n"
    "SECOND REPORT\n"
  )
  assert captured.err == ""


def test_phase100_12c2_cli_rejects_noninteger_arguments():
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "five",
        "7",
      ]
    )

  assert exc_info.value.code == 2
