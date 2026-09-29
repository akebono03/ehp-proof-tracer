import pytest

import main as cli_main


def test_phase132_7_group_proof_default_mode_is_narrative(
  capsys,
):
  parser = cli_main.build_group_proof_argument_parser()
  args = parser.parse_args(
    [
      "9",
      "7",
    ]
  )

  assert args.mode == "narrative"
  assert args.depth == 2

  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group proof narrative" in captured.out
  assert "# Group result" not in captured.out


def test_phase132_7_group_proof_explicit_trace_remains_available(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "1",
      "--mode",
      "trace",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group result" in captured.out
  assert "Depth 0" in captured.out
  assert "Depth 1" in captured.out
  assert "# Group proof narrative" not in captured.out


def test_phase132_7_group_proof_outline_mode_uses_outline_renderer(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--mode",
      "outline",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group proof outline" in captured.out
  assert "Toda Proposition 5.15" in captured.out
  assert (
    r"$\pi_{16}^{9} = "
    r"\mathbb{Z}/16\{\sigma_{9}\}$"
    in captured.out
  )
  assert "Premise 1:" in captured.out
  assert "# Group result" not in captured.out


def test_phase132_7_group_proof_narrative_mode_uses_narrative_renderer(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group proof narrative" in captured.out
  assert (
    "Toda Proposition 5.15を用いる。"
    in captured.out
  )
  assert "したがって、" in captured.out
  assert (
    r"$\pi_{16}^{9} = "
    r"\mathbb{Z}/16\{\sigma_{9}\}$"
    in captured.out
  )
  assert "# Group result" not in captured.out


@pytest.mark.parametrize(
  (
    "mode",
    "heading",
  ),
  (
    (
      "trace",
      "# Group result",
    ),
    (
      "outline",
      "# Group proof outline",
    ),
    (
      "narrative",
      "# Group proof narrative",
    ),
  ),
)
def test_phase132_7_group_proof_depth_zero_is_shared_across_modes(
  mode,
  heading,
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "0",
      "--mode",
      mode,
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert heading in captured.out

  if mode == "trace":
    assert "Depth 0" in captured.out
    assert "Depth 1" not in captured.out
  elif mode == "outline":
    assert "Premise " not in captured.out
  else:
    assert "まず、" not in captured.out
    assert "また、" not in captured.out
    assert "さらに、" not in captured.out


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
