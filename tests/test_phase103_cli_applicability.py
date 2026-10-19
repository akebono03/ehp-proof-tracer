from types import SimpleNamespace

import pytest

import main as cli_main






def test_phase103_6_explore_applicable_help_is_stdout_zero_exit(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore-applicable",
        "--help",
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert (
    exc_info.value.code
    == 0
  )

  assert (
    "main.py explore-applicable"
    in captured.out
  )

  assert (
    "generator"
    in captured.out
  )

  assert (
    captured.err
    == ""
  )
