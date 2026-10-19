from types import SimpleNamespace

import pytest

import main as cli_main








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
