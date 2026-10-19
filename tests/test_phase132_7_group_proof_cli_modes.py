import pytest

import main as cli_main












def test_phase132_7_group_proof_help_lists_modes(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as error:
    cli_main.main(
      [
        "group-proof",
        "--help",
      ]
    )

  captured = capsys.readouterr()

  assert error.value.code == 0
  assert "--mode" in captured.out
  assert (
    "{trace,outline,narrative}"
    in captured.out
  )


def test_phase132_7_invalid_mode_is_rejected_by_argparse(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as error:
    cli_main.main(
      [
        "group-proof",
        "9",
        "7",
        "--mode",
        "unknown",
      ]
    )

  captured = capsys.readouterr()

  assert error.value.code == 2
  assert (
    "invalid choice"
    in captured.err
  )
