from types import SimpleNamespace

import pytest

import main as cli_main
from toda_calculation_result import (
  TodaCalculationStatus,
)


def test_phase102_7_explore_proof_dispatches_to_production_scope_facade(
  monkeypatch,
  capsys,
):
  calls = []

  fake_result = SimpleNamespace(
    generator=object(),
  )

  def fake_facade(
    generator_input: str,
  ):
    calls.append(
      generator_input
    )
    return fake_result

  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_repository_"
      "generator_proof_scope_input"
    ),
    fake_facade,
  )

  monkeypatch.setattr(
    cli_main,
    (
      "render_repository_proof_scope_"
      "exploration_markdown"
    ),
    lambda result: "PROOF SCOPE REPORT\n",
  )

  exit_code = cli_main.main(
    [
      "explore-proof",
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

  assert (
    captured.out
    == "PROOF SCOPE REPORT\n"
  )

  assert captured.err == ""


def test_phase102_7_actual_explore_proof_renders_production_semantics(
  capsys,
):
  exit_code = cli_main.main(
    [
      "explore-proof",
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
    "## Toda memberships"
    in captured.out
  )

  assert (
    "## Map relations"
    in captured.out
  )

  assert (
    "Root: standard.toda."
    in captured.out
  )

  assert captured.err == ""


def test_phase102_7_explore_proof_zero_result_is_normal_zero_exit(
  capsys,
):
  exit_code = cli_main.main(
    [
      "explore-proof",
      "eta_999",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0

  assert (
    "Proof-scope occurrences: 0"
    in captured.out
  )

  assert (
    "Toda memberships: 0"
    in captured.out
  )

  assert (
    "Map relations: 0"
    in captured.out
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
def test_phase102_7_explore_proof_invalid_generator_is_argparse_error(
  capsys,
  value,
  message,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore-proof",
        value,
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert exc_info.value.code == 2
  assert captured.out == ""
  assert message in captured.err
  assert "Traceback" not in captured.err


def test_phase102_7_explore_proof_missing_generator_is_argparse_error(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore-proof",
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert exc_info.value.code == 2
  assert captured.out == ""
  assert "generator" in captured.err
  assert "Traceback" not in captured.err


def test_phase102_7_explore_proof_help_is_stdout_zero_exit(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore-proof",
        "--help",
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert exc_info.value.code == 0

  assert (
    "main.py explore-proof"
    in captured.out
  )

  assert (
    "generator"
    in captured.out
  )

  assert captured.err == ""


def test_phase102_7_existing_explore_command_is_unchanged(
  monkeypatch,
  capsys,
):
  calls = []

  fake_report = SimpleNamespace(
    markdown=(
      "EXISTING EXPLORE REPORT\n"
    ),
  )

  def fake_existing_facade(
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
    fake_existing_facade,
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

  assert (
    captured.out
    == fake_report.markdown
  )

  assert captured.err == ""


def test_phase102_7_legacy_n_k_path_is_unchanged(
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

  def fake_calculation(
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
    fake_calculation,
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

  assert (
    captured.out
    == "LEGACY REPORT\n"
  )

  assert captured.err == ""
