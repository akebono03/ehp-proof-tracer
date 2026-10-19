from types import SimpleNamespace

import pytest

import main as cli_main










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


