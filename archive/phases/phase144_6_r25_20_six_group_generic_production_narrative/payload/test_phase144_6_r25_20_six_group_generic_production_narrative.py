import main as cli_main


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def test_phase144_6_r25_20_six_groups_use_complete_replay_for_depth2_narrative(
  monkeypatch,
  capsys,
):
  original = cli_main.build_complete_toda_group_result_proof_replay
  calls = []

  def recording_complete_replay(group_result):
    calls.append(group_result)
    return original(group_result)

  monkeypatch.setattr(
    cli_main,
    "build_complete_toda_group_result_proof_replay",
    recording_complete_replay,
  )

  for n, k in TARGETS:
    exit_code = cli_main._run_group_proof_command(
      n,
      k,
      max_depth=2,
      mode="narrative",
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert output.strip()
    assert f"\\pi_{{{n + k}}}^{{{n}}}" in output

  assert len(calls) == len(TARGETS)


def test_phase144_6_r25_20_trace_depth2_does_not_use_complete_replay(
  monkeypatch,
  capsys,
):
  def forbidden_complete_replay(group_result):
    raise AssertionError(
      "trace must preserve explicit depth semantics"
    )

  monkeypatch.setattr(
    cli_main,
    "build_complete_toda_group_result_proof_replay",
    forbidden_complete_replay,
  )

  exit_code = cli_main._run_group_proof_command(
    3,
    3,
    max_depth=2,
    mode="trace",
  )
  output = capsys.readouterr().out

  assert exit_code == 0
  assert output.strip()
