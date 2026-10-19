from functools import lru_cache

from proof import (
  ProofRule,
)
from probes.probe_phase70_capabilities import (
  build_phase70_representative_result,
  main,
)
from toda_rules import (
  TodaProp59FiniteDimensionalStatement,
)


@lru_cache(maxsize=1)
def build_phase70_probe_data():
  return (
    build_phase70_representative_result()
  )


def test_phase70_probe_derives_prop59_aggregate():
  data = build_phase70_probe_data()

  step = data[
    "integration_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaProp59FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase70_probe_final_aggregate_is_not_given():
  data = build_phase70_probe_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase70_probe_pi7_2_is_derived():
  data = build_phase70_probe_data()

  assert (
    data[
      "pi7_2_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_probe_pi8_3_is_derived():
  data = build_phase70_probe_data()

  assert (
    data[
      "pi8_3_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_probe_pi9_4_is_derived():
  data = build_phase70_probe_data()

  assert (
    data[
      "pi9_4_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_probe_pi10_5_is_derived():
  data = build_phase70_probe_data()

  assert (
    data[
      "pi10_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_probe_pi11_6_is_derived():
  data = build_phase70_probe_data()

  assert (
    data[
      "pi11_6_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_probe_higher_zero_is_derived():
  data = build_phase70_probe_data()

  assert (
    data[
      "higher_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_probe_scope_remains_given():
  data = build_phase70_probe_data()

  assert (
    data[
      "higher_range_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "higher_range_step"
    ].conclusion.right
    == 7
  )


def test_phase70_probe_final_premises_are_expected():
  data = build_phase70_probe_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "pi7_2_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "pi9_4_step"
      ],
      data[
        "pi10_5_step"
      ],
      data[
        "pi11_6_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )


def test_phase70_probe_builder_reuses_integration_step():
  data = build_phase70_probe_data()

  direct = (
    build_phase70_representative_result()
  )

  assert (
    data[
      "integration_step"
    ]
    is direct[
      "integration_step"
    ]
  )


def test_phase70_probe_output_contains_heading(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "EHP Proof Tracer"
    in output
  )

  assert (
    "Phase 70 capability demonstration"
    in output
  )

  assert (
    "Toda Proposition 5.9 "
    "finite-dimensional result"
    in output
  )


def test_phase70_probe_output_contains_final_results(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_7^2 = Z/2{η₂ν′η₆}"
    in output
  )

  assert (
    "π_8^3 = Z/2{ν′η₆²}"
    in output
  )

  assert (
    "π_9^4 = "
    "Z/2{ν₄η₇²} ⊕ "
    "Z/2{Eν′η₇²}"
    in output
  )

  assert (
    "π_10^5 = Z/2{ν₅η₈²}"
    in output
  )

  assert (
    "π_11^6 = Z{Δι₁₃}"
    in output
  )

  assert (
    "π_(n+5)^n = 0  "
    "(n ≥ 7)"
    in output
  )


def test_phase70_probe_output_contains_proof_style_heading(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Proof-style derivation"
    in output
  )


def test_phase70_probe_output_contains_pi10_5_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[4] π_10^5"
    in output
  )

  assert (
    "Δ(η₉²) = Eν′η₇²"
    in output
  )

  assert (
    "ker(E) = "
    "Z/2{Eν′η₇²}"
    in output
  )

  assert (
    "E: π_9^4 → π_10^5 "
    "is surjective"
    in output
  )

  assert (
    "E(ν₄η₇²) = ν₅η₈²"
    in output
  )

  assert (
    "π_10^5 = Z/2{ν₅η₈²}"
    in output
  )


def test_phase70_probe_output_contains_pi11_6_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[5] π_11^6"
    in output
  )

  assert (
    "E(ν₅η₈²) = 0"
    in output
  )

  assert (
    "H: π_11^6 → π_11^11 "
    "is injective"
    in output
  )

  assert (
    "π_11^11 = Z{ι₁₁}"
    in output
  )

  assert (
    "Δ(ι₁₁) = ν₅η₈"
    in output
  )

  assert (
    "ker(Δ) = Z{2ι₁₁}"
    in output
  )

  assert (
    "H(Δι₁₃) = ±2ι₁₁"
    in output
  )

  assert (
    "π_11^6 = Z{Δι₁₃}"
    in output
  )


def test_phase70_probe_output_contains_pi12_7_zero_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Δ: π_13^13 → π_11^6 "
    "is surjective"
    in output
  )

  assert (
    "E: π_11^6 → π_12^7 "
    "is zero"
    in output
  )

  assert (
    "π_12^13 = 0"
    in output
  )

  assert (
    "E: π_11^6 → π_12^7 "
    "is surjective"
    in output
  )

  assert (
    "π_12^7 = 0"
    in output
  )


def test_phase70_probe_output_contains_toda45_transport(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Toda (4.5):"
    in output
  )

  assert (
    "E^(n-7): "
    "π_12^7 ≅ π_(n+5)^n"
    in output
  )

  assert (
    "π_(n+5)^n = 0  "
    "(n ≥ 7)"
    in output
  )


def test_phase70_probe_output_contains_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Provenance / integration"
    in output
  )

  assert (
    "final aggregate derived = True"
    in output
  )

  assert (
    "final aggregate is GIVEN = False"
    in output
  )

  assert (
    "all six theorem branches are "
    "INFERENCE = True"
    in output
  )


def test_phase70_probe_output_contains_branch_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_7^2 result derived = True"
    in output
  )

  assert (
    "π_8^3 result derived = True"
    in output
  )

  assert (
    "π_9^4 result derived = True"
    in output
  )

  assert (
    "π_10^5 result derived = True"
    in output
  )

  assert (
    "π_11^6 result derived = True"
    in output
  )

  assert (
    "higher five-stem zero derived = True"
    in output
  )


def test_phase70_probe_output_contains_scope_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "n>=7 scope remains GIVEN = True"
    in output
  )


def test_phase70_probe_output_contains_seven_premises(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "final premise count = 7"
    in output
  )


def test_phase70_probe_output_contains_staged_one_shot_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "staged one-shot aggregate = True"
    in output
  )

  assert (
    "fixed point = True"
    not in output
  )


def test_phase70_probe_output_contains_literature(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Literature statements used"
    in output
  )

  assert (
    "[Toda Proposition 5.9]"
    in output
  )

  assert (
    "Locator: Proposition 5.9"
    in output
  )

  assert (
    "Author: H. Toda"
    in output
  )

  assert (
    "Source: Composition Methods in "
    "Homotopy Groups of Spheres"
    in output
  )

  assert (
    "Year: 1962"
    in output
  )


def test_phase70_probe_output_contains_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 70 representative probe boundary"
    in output
  )

  assert (
    "Not added in Phase 70-12:"
    in output
  )

  assert (
    "new mathematical inference rules"
    in output
  )

  assert (
    "proof record documentation"
    in output
  )


def test_phase70_probe_does_not_add_stable_g5(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "stable (G_5;2)=0 aggregate"
    in output
  )

  assert (
    "Not added in Phase 70-12:"
    in output
  )


def test_phase70_probe_does_not_claim_automatic_narrative(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "hand-authored presentation code"
    in output
  )

  assert (
    "not yet generated "
    "automatically from the ProofStep graph"
    in output
  )


def test_phase70_probe_does_not_claim_proof_record_added(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Proof record"
    not in output
  )

  assert (
    "docs/proof_records.md"
    not in output
  )


def test_phase70_probe_does_not_claim_next_theorem_implemented(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "next Toda theorem"
    in output
  )

  assert (
    "Not added in Phase 70-12:"
    in output
  )


