from types import SimpleNamespace

import pytest

import main as cli_main


def test_phase103_6_explore_applicable_dispatches_to_facade(
  monkeypatch,
  capsys,
):
  calls = []

  fake_result = SimpleNamespace(
    generator=object(),
  )

  def fake_facade(
    generator_input,
  ):
    calls.append(
      generator_input
    )
    return fake_result

  monkeypatch.setattr(
    cli_main,
    (
      "explore_standard_repository_"
      "generator_applicability_input"
    ),
    fake_facade,
  )

  monkeypatch.setattr(
    cli_main,
    (
      "render_repository_generator_"
      "applicability_markdown"
    ),
    lambda result: (
      "APPLICABILITY REPORT\n"
    ),
  )

  exit_code = cli_main.main(
    [
      "explore-applicable",
      "nu_prime",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert (
    exit_code
    == 0
  )

  assert calls == [
    "nu_prime",
  ]

  assert (
    captured.out
    == "APPLICABILITY REPORT\n"
  )

  assert (
    captured.err
    == ""
  )

def test_phase103_6_actual_explore_applicable_renders_production_result(
  capsys,
):
  exit_code = cli_main.main(
    [
      "explore-applicable",
      "nu_prime",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert exit_code == 0

  assert (
    "# Applicable theorem / lemma candidates for $\\nu'$"
    in captured.out
  )

  assert (
    "Proof-scope occurrences:"
    in captured.out
  )

  assert (
    "Applicability candidates:"
    in captured.out
  )

  assert (
    "Source statements with candidates:"
    in captured.out
  )

  assert (
    "Rule groups:"
    in captured.out
  )

  assert (
    "Rule families:"
    in captured.out
  )

  assert (
    "## Candidates"
    in captured.out
  )

  assert (
    "### Toda memberships"
    in captured.out
  )

  assert (
    "Rule: Toda 5.3 nu-prime Lemma 5.2 bracket specialization"
    in captured.out
  )

  assert (
    "Catalog entries:"
    in captured.out
  )

  assert (
    "Premise index:"
    not in captured.out
  )

  assert (
    "Bindings:"
    not in captured.out
  )

  assert (
    "Fixed-point safe:"
    not in captured.out
  )

  assert captured.err == ""

def test_phase103_6_explore_applicable_zero_result_is_zero_exit(
  capsys,
):
  exit_code = cli_main.main(
    [
      "explore-applicable",
      "eta_999",
    ]
  )

  captured = (
    capsys.readouterr()
  )

  assert (
    exit_code
    == 0
  )

  assert (
    "Proof-scope occurrences: 0"
    in captured.out
  )

  assert (
    "Applicability candidates: 0"
    in captured.out
  )

  assert (
    "## Candidates"
    not in captured.out
  )

  assert (
    captured.err
    == ""
  )


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
def test_phase103_6_explore_applicable_invalid_generator_is_argparse_error(
  capsys,
  value,
  message,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore-applicable",
        value,
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert (
    exc_info.value.code
    == 2
  )

  assert (
    captured.out
    == ""
  )

  assert (
    message
    in captured.err
  )

  assert (
    "Traceback"
    not in captured.err
  )


def test_phase103_6_explore_applicable_missing_generator_is_argparse_error(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "explore-applicable",
      ]
    )

  captured = (
    capsys.readouterr()
  )

  assert (
    exc_info.value.code
    == 2
  )

  assert (
    captured.out
    == ""
  )

  assert (
    "generator"
    in captured.err
  )


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
