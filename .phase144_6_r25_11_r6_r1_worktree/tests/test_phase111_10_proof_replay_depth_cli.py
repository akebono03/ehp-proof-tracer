from types import SimpleNamespace

import pytest

import main as cli_main


def test_phase111_10_show_proof_depth_is_forwarded(
  monkeypatch,
  capsys,
):
  calls = []

  fake_result = object()
  fake_presentation = object()

  def fake_build(
    generator_input,
    max_depth=1,
  ):
    calls.append(
      (
        generator_input,
        max_depth,
      )
    )
    return fake_result

  monkeypatch.setattr(
    cli_main,
    "build_standard_repository_generator_known_group_proof_replay_input",
    fake_build,
  )
  monkeypatch.setattr(
    cli_main,
    "build_repository_generator_known_group_proof_replay_presentation",
    lambda result: fake_presentation,
  )
  monkeypatch.setattr(
    cli_main,
    "render_repository_generator_known_group_proof_replay_markdown",
    lambda presentation: "SHOW PROOF\n",
  )

  exit_code = cli_main.main(
    [
      "show-proof",
      "sigma_11",
      "--depth",
      "2",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert calls == [
    (
      "sigma_11",
      2,
    ),
  ]
  assert captured.out == "SHOW PROOF\n"
  assert captured.err == ""


def test_phase111_10_query_proof_depth_is_forwarded(
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
    lambda query_input: fake_result,
  )
  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_presentation",
    lambda result: fake_query_presentation,
  )

  def fake_replay_builder(
    presentation,
    fact_number=None,
    max_depth=1,
  ):
    calls.append(
      (
        presentation,
        fact_number,
        max_depth,
      )
    )
    return fake_replay

  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_proof_replay",
    fake_replay_builder,
  )
  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_proof_replay_presentation",
    lambda replay: fake_replay_presentation,
  )
  monkeypatch.setattr(
    cli_main,
    "render_repository_operation_query_proof_replay_markdown",
    lambda presentation: "QUERY PROOF\n",
  )

  exit_code = cli_main.main(
    [
      "query-proof",
      "E(eta_2 o nu_prime)",
      "--depth",
      "2",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert calls == [
    (
      fake_query_presentation,
      None,
      2,
    ),
  ]
  assert captured.out == "QUERY PROOF\n"
  assert captured.err == ""


def test_phase111_10_query_proof_fact_and_depth_are_forwarded(
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

  def fake_replay_builder(
    presentation,
    fact_number=None,
    max_depth=1,
  ):
    calls.append(
      (
        fact_number,
        max_depth,
      )
    )
    return fake_replay

  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_proof_replay",
    fake_replay_builder,
  )
  monkeypatch.setattr(
    cli_main,
    "build_repository_operation_query_proof_replay_presentation",
    lambda replay: fake_replay_presentation,
  )
  monkeypatch.setattr(
    cli_main,
    "render_repository_operation_query_proof_replay_markdown",
    lambda presentation: "QUERY PROOF\n",
  )

  exit_code = cli_main.main(
    [
      "query-proof",
      "H(nu_prime)",
      "--fact",
      "2",
      "--depth",
      "3",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert calls == [
    (
      2,
      3,
    ),
  ]
  assert captured.out == "QUERY PROOF\n"
  assert captured.err == ""


@pytest.mark.parametrize(
  "argv",
  (
    (
      "show-proof",
      "sigma_11",
      "--depth",
      "-1",
    ),
    (
      "query-proof",
      "H(nu_prime)",
      "--depth",
      "-1",
    ),
  ),
)
def test_phase111_10_negative_depth_is_parser_error(
  argv,
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      list(
        argv
      )
    )

  captured = capsys.readouterr()

  assert exc_info.value.code == 2
  assert captured.out == ""
  assert "must be nonnegative" in captured.err
  assert "Traceback" not in captured.err


def test_phase111_10_show_proof_depth_zero_is_allowed(
  monkeypatch,
  capsys,
):
  monkeypatch.setattr(
    cli_main,
    "_run_show_proof_command",
    lambda generator_input, max_depth=None: (
      0
      if max_depth == 0
      else 99
    ),
  )

  exit_code = cli_main.main(
    [
      "show-proof",
      "sigma_11",
      "--depth",
      "0",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.out == ""
  assert captured.err == ""


def test_phase111_10_query_proof_depth_zero_is_allowed(
  monkeypatch,
  capsys,
):
  monkeypatch.setattr(
    cli_main,
    "_run_query_proof_command",
    lambda query_input, fact_number=None, max_depth=None: (
      0
      if max_depth == 0
      else 99
    ),
  )

  exit_code = cli_main.main(
    [
      "query-proof",
      "H(nu_prime)",
      "--depth",
      "0",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.out == ""
  assert captured.err == ""


@pytest.mark.parametrize(
  "argv",
  (
    (
      "show-proof",
      "--help",
    ),
    (
      "query-proof",
      "--help",
    ),
  ),
)
def test_phase111_10_help_documents_depth(
  argv,
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      list(
        argv
      )
    )

  captured = capsys.readouterr()

  assert exc_info.value.code == 0
  assert "--depth" in captured.out
  assert "default depth 1" in captured.out
  assert captured.err == ""
