from main import (
  _run_group_proof_command,
)


def test_phase144_6_r25_17_cli_depth2_narrative_is_complete(
  capsys,
):
  exit_code = _run_group_proof_command(
    3,
    3,
    max_depth=2,
    mode="narrative",
  )
  output = capsys.readouterr().out

  assert exit_code == 0
  assert r"$\nu'$ を定める." in output
  assert "(1) と (2) より、" in output
  assert "(4) と (5) より、" in output
  assert (
    "以上より、\n\n"
    r"$\operatorname{ord}\left(\nu'\right) = 4$"
    in output
  )
  assert (
    "以上より、\n\n"
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in output
  )


def test_phase144_6_r25_17_cli_depth2_narrative_has_no_raw_rule_fallback(
  capsys,
):
  exit_code = _run_group_proof_command(
    3,
    3,
    max_depth=2,
    mode="narrative",
  )
  output = capsys.readouterr().out

  assert exit_code == 0
  assert (
    "Toda 5.3 nu-prime Lemma 5.2 "
    "bracket specialization"
    not in output
  )
  assert (
    "Toda Proposition 5.1 "
    "finite-dimensional integration"
    not in output
  )
