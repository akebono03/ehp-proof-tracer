from types import SimpleNamespace

import main as cli_main


def test_phase110_8_query_cli_builds_presentation_before_rendering(
  monkeypatch,
  capsys,
):
  calls = []

  fake_result = SimpleNamespace(
    found=True,
  )

  fake_presentation = SimpleNamespace(
    items=(
      object(),
    ),
  )

  monkeypatch.setattr(
    cli_main,
    "query_standard_repository_operation_input",
    lambda query_input: (
      calls.append(
        (
          "query",
          query_input,
        )
      )
      or fake_result
    ),
  )

  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_presentation",
    lambda result: (
      calls.append(
        (
          "presentation",
          result,
        )
      )
      or fake_presentation
    ),
  )

  monkeypatch.setattr(
    cli_main,
    "render_repository_operation_query_markdown",
    lambda presentation: (
      calls.append(
        (
          "render",
          presentation,
        )
      )
      or "# Known repository facts\n\n1. fact\n"
    ),
  )

  exit_code = cli_main.main(
    [
      "query",
      "H(nu_prime)",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0

  assert calls == [
    (
      "query",
      "H(nu_prime)",
    ),
    (
      "presentation",
      fake_result,
    ),
    (
      "render",
      fake_presentation,
    ),
  ]

  assert captured.out == (
    "# Known repository facts\n\n"
    "1. fact\n"
  )

  assert captured.err == ""


def test_phase110_8_query_cli_reports_no_directly_renderable_fact(
  monkeypatch,
  capsys,
):
  fake_result = SimpleNamespace(
    found=True,
  )

  fake_presentation = SimpleNamespace(
    items=(),
  )

  monkeypatch.setattr(
    cli_main,
    "query_standard_repository_operation_input",
    lambda query_input: fake_result,
  )

  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_presentation",
    lambda result: fake_presentation,
  )

  exit_code = cli_main.main(
    [
      "query",
      "eta_2 o nu_prime",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 1

  assert captured.out == (
    "No directly renderable repository fact found for "
    "eta_2 o nu_prime.\n"
  )

  assert captured.err == ""
