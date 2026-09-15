from proof import ProofRule
from probes.probe_phase78_capabilities import (
  build_phase78_representative_result,
  main,
)
from toda_rules import (
  TodaStableG0ToG7Statement,
)


def test_phase78_probe_aggregate_is_derived():
  result = (
    build_phase78_representative_result()
  )

  assert isinstance(
    result[
      "statement"
    ],
    TodaStableG0ToG7Statement,
  )

  assert (
    result[
      "aggregate_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    result[
      "aggregate_derived"
    ]
    is True
  )

  assert (
    result[
      "aggregate_is_given"
    ]
    is False
  )


def test_phase78_probe_all_direct_branches_are_inference():
  result = (
    build_phase78_representative_result()
  )

  assert (
    result[
      "all_direct_branches_inference"
    ]
    is True
  )


def test_phase78_probe_all_branches_are_reachable():
  result = (
    build_phase78_representative_result()
  )

  for key in (
    "g0_reachable",
    "g1_reachable",
    "g2_reachable",
    "g3_reachable",
    "g4_reachable",
    "g5_reachable",
    "g6_reachable",
    "g7_reachable",
  ):
    assert (
      result[
        key
      ]
      is True
    )


def test_phase78_probe_graph_is_non_circular():
  result = (
    build_phase78_representative_result()
  )

  assert (
    result[
      "final_is_self_ancestor"
    ]
    is False
  )

  assert (
    result[
      "final_conclusion_in_ancestors"
    ]
    is False
  )


def test_phase78_probe_output_contains_all_results(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Stable G_0 through G_7 result"
    in output
  )

  assert "G_0 = Z{iota}" in output
  assert "(G_1;2) = Z/2{eta}" in output
  assert "(G_2;2) = Z/2{eta^2}" in output
  assert "(G_3;2) = Z/8{nu}" in output
  assert "(G_4;2) = 0" in output
  assert "(G_5;2) = 0" in output
  assert "(G_6;2) = Z/2{nu^2}" in output
  assert "(G_7;2) = Z/16{sigma}" in output


def test_phase78_probe_output_contains_derivation_chain(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert "Proof-style derivation" in output
  assert "pi_3^3=Z{iota_3}" in output
  assert "pi_4^3=Z/2{eta_3}" in output
  assert "pi_6^4=Z/2{eta_4^2}" in output
  assert "pi_8^5=Z/8{nu_5}" in output
  assert "pi_10^6=0" in output
  assert "pi_12^7=0" in output
  assert "pi_14^8=Z/2{nu_8^2}" in output
  assert "pi_16^9=Z/16{sigma_9}" in output


def test_phase78_probe_output_contains_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert "Provenance / integration" in output

  assert (
    "all eight direct branches are INFERENCE = True"
    in output
  )

  for stem in range(
    8
  ):
    assert (
      f"G_{stem} branch reachable = True"
      in output
    )

  assert (
    "aggregate derived = True"
    in output
  )

  assert (
    "aggregate is GIVEN = False"
    in output
  )


def test_phase78_probe_output_preserves_representation_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Representation boundary"
    in output
  )

  assert (
    "G_0 is ordinary StableHomotopyGroup(stem=0)."
    in output
  )

  assert (
    "G_0 is not represented as a StablePrimaryComponent."
    in output
  )

  assert (
    "eta^2 and nu^2 remain Composition expressions."
    in output
  )


def test_phase78_probe_output_contains_non_circularity(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Applicability / non-circularity"
    in output
  )

  assert (
    "final is self-ancestor = False"
    in output
  )

  assert (
    "final conclusion appears in ancestors = False"
    in output
  )


def test_phase78_probe_output_contains_completion_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 78 representative probe boundary"
    in output
  )

  assert (
    "new mathematical stable-group results"
    in output
  )

  assert (
    "generic E-infinity map object"
    in output
  )

  assert (
    "generic stable-group database"
    in output
  )

  assert (
    "automatic proof narrative generation"
    in output
  )


