import main as cli_main



def test_phase131_4_group_proof_sigma9_renders_group_source_and_proof(
  capsys,
):
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
  assert "# Group result" in captured.out
  assert "## Source" in captured.out
  assert "## Proof" in captured.out
  assert "Toda Proposition 5.15" in captured.out
  assert "- Phase: 75" in captured.out
  assert "Depth 0" in captured.out
  assert "Depth 1" in captured.out
  assert (
    r"$\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}$"
    in captured.out
  )



def test_phase131_4_group_proof_zero_depth_contains_only_root(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "0",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert "Depth 0" in captured.out
  assert "Depth 1" not in captured.out



def test_phase131_4_group_proof_zero_group_does_not_require_generator(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "2",
      "7",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"$\pi_{9}^{2} = 0$" in captured.out
  assert "Toda Proposition 5.15" in captured.out
  assert "Depth 0" in captured.out



def test_phase131_4_group_proof_not_found_is_explicit(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "20",
      "20",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 1
  assert (
    "No proof-backed group result found for pi_{40}^{20}."
    in captured.out
  )



def test_phase131_4_group_proof_connectivity_zero_is_replayed(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "11",
      "-1",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"$\pi_{10}^{11} = 0$" in captured.out
  assert "Sphere connectivity" in captured.out
  assert "- Phase: 130" in captured.out
  assert "Depth 0" in captured.out
  assert "Depth 1" not in captured.out



def test_phase131_4_existing_group_query_semantics_remain_unchanged(
  capsys,
):
  exit_code = cli_main.main(
    [
      "9",
      "7",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert (
    r"\pi_{16}^{9} \cong \mathbb{Z}/16\{\sigma_{9}\}"
    in captured.out
  )
