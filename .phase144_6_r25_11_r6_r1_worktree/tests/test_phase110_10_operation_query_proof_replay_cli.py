from types import SimpleNamespace

import pytest

import main as cli_main


def test_phase110_10_query_proof_single_fact_runs_without_fact(
  monkeypatch,
  capsys,
):
  calls = []

  fake_result = SimpleNamespace(
    found=True,
  )

  fake_query_presentation = SimpleNamespace(
    items=(
      object(),
    ),
  )

  fake_replay = object()
  fake_replay_presentation = object()

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
          "query-presentation",
          result,
        )
      )
      or fake_query_presentation
    ),
  )

  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_proof_replay",
    lambda presentation, fact_number=None: (
      calls.append(
        (
          "replay",
          presentation,
          fact_number,
        )
      )
      or fake_replay
    ),
  )

  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_proof_replay_presentation",
    lambda replay: (
      calls.append(
        (
          "replay-presentation",
          replay,
        )
      )
      or fake_replay_presentation
    ),
  )

  monkeypatch.setattr(
    cli_main,
    "render_repository_operation_query_proof_replay_markdown",
    lambda presentation: (
      calls.append(
        (
          "render",
          presentation,
        )
      )
      or "# Query fact\n\nfact\n\n## Proof\n\nproof\n"
    ),
  )

  exit_code = cli_main.main(
    [
      "query-proof",
      "E(eta_2 o nu_prime)",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0

  assert calls == [
    (
      "query",
      "E(eta_2 o nu_prime)",
    ),
    (
      "query-presentation",
      fake_result,
    ),
    (
      "replay",
      fake_query_presentation,
      None,
    ),
    (
      "replay-presentation",
      fake_replay,
    ),
    (
      "render",
      fake_replay_presentation,
    ),
  ]

  assert captured.out == (
    "# Query fact\n\n"
    "fact\n\n"
    "## Proof\n\n"
    "proof\n"
  )

  assert captured.err == ""


def test_phase110_10_query_proof_multiple_facts_lists_and_requires_fact(
  monkeypatch,
  capsys,
):
  fake_result = SimpleNamespace(
    found=True,
  )

  fake_query_presentation = SimpleNamespace(
    items=(
      object(),
      object(),
    ),
  )

  monkeypatch.setattr(
    cli_main,
    "query_standard_repository_operation_input",
    lambda query_input: fake_result,
  )

  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_presentation",
    lambda result: fake_query_presentation,
  )

  monkeypatch.setattr(
    cli_main,
    "render_repository_operation_query_markdown",
    lambda presentation: (
      "# Known repository facts\n\n"
      "1. fact one\n\n"
      "2. fact two\n"
    ),
  )

  exit_code = cli_main.main(
    [
      "query-proof",
      "H(nu_prime)",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 1

  assert captured.out == (
    "# Known repository facts\n\n"
    "1. fact one\n\n"
    "2. fact two\n"
    "\n"
    "Specify --fact N to replay one fact.\n"
  )

  assert captured.err == ""


def test_phase110_10_query_proof_fact_is_forwarded(
  monkeypatch,
  capsys,
):
  calls = []

  fake_result = SimpleNamespace(
    found=True,
  )

  fake_query_presentation = SimpleNamespace(
    items=(
      object(),
      object(),
    ),
  )

  fake_replay = object()
  fake_replay_presentation = object()

  monkeypatch.setattr(
    cli_main,
    "query_standard_repository_operation_input",
    lambda query_input: fake_result,
  )

  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_presentation",
    lambda result: fake_query_presentation,
  )

  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_proof_replay",
    lambda presentation, fact_number=None: (
      calls.append(
        fact_number
      )
      or fake_replay
    ),
  )

  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_proof_replay_presentation",
    lambda replay: fake_replay_presentation,
  )

  monkeypatch.setattr(
    cli_main,
    "render_repository_operation_query_proof_replay_markdown",
    lambda presentation: "REPLAY\n",
  )

  exit_code = cli_main.main(
    [
      "query-proof",
      "H(nu_prime)",
      "--fact",
      "2",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert calls == [
    2,
  ]
  assert captured.out == "REPLAY\n"
  assert captured.err == ""


def test_phase110_10_query_proof_fact_zero_is_parser_error(
  monkeypatch,
  capsys,
):
  calls = []

  monkeypatch.setattr(
    cli_main,
    "query_standard_repository_operation_input",
    lambda query_input: (
      calls.append(
        query_input
      )
      or None
    ),
  )

  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "query-proof",
        "H(nu_prime)",
        "--fact",
        "0",
      ]
    )

  captured = capsys.readouterr()

  assert exc_info.value.code == 2
  assert calls == []
  assert captured.out == ""
  assert "must be positive" in captured.err
  assert "Traceback" not in captured.err


def test_phase110_10_query_proof_help_documents_fact(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "query-proof",
        "--help",
      ]
    )

  captured = capsys.readouterr()

  assert exc_info.value.code == 0
  assert "main.py query-proof" in captured.out
  assert "--fact" in captured.out
  assert "H(nu_prime)" in captured.out
  assert captured.err == ""


def test_phase110_10_existing_query_command_is_unchanged(
  monkeypatch,
  capsys,
):
  fake_result = SimpleNamespace(
    found=False,
  )

  monkeypatch.setattr(
    cli_main,
    "query_standard_repository_operation_input",
    lambda query_input: fake_result,
  )

  exit_code = cli_main.main(
    [
      "query",
      "H(eta_999)",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 1
  assert captured.out == (
    "No known repository fact found for "
    "H(eta_999).\n"
  )
  assert captured.err == ""
