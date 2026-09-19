import pytest

import main as cli_main


@pytest.mark.parametrize(
  "argv, expected_message",
  [
    (
      [
        "0",
        "7",
      ],
      "must be positive",
    ),
    (
      [
        "-1",
        "7",
      ],
      "must be positive",
    ),
    (
      [
        "5",
        "-1",
      ],
      "must be nonnegative",
    ),
  ],
)
def test_phase100_12c4_semantically_invalid_cli_arguments_exit_two_without_facade_call(
  monkeypatch,
  capsys,
  argv,
  expected_message,
):
  calls = []

  def fail_if_called(
    n: int,
    k: int,
  ):
    calls.append(
      (
        n,
        k,
      )
    )
    raise AssertionError(
      "build_standard_toda_report must not be called"
    )

  monkeypatch.setattr(
    cli_main,
    "build_standard_toda_report",
    fail_if_called,
  )

  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      argv
    )

  captured = (
    capsys.readouterr()
  )

  assert exc_info.value.code == 2
  assert calls == []
  assert captured.out == ""
  assert (
    expected_message
    in captured.err
  )
  assert (
    "Traceback"
    not in captured.err
  )


def test_phase100_12c4_valid_boundary_values_reach_facade(
  monkeypatch,
  capsys,
):
  calls = []

  class FakeResult:
    reports = (
      "BOUNDARY REPORT",
    )

    from toda_calculation_result import (
      TodaCalculationStatus,
    )

    status = (
      TodaCalculationStatus.FOUND
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
    return FakeResult()

  monkeypatch.setattr(
    cli_main,
    "build_standard_toda_report",
    fake_build_standard_toda_report,
  )

  exit_code = cli_main.main(
    [
      "1",
      "0",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0
  assert calls == [
    (
      1,
      0,
    )
  ]
  assert captured.out == (
    "BOUNDARY REPORT\n"
  )
  assert captured.err == ""
