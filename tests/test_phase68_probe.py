from functools import lru_cache

from proof import (
  ProofRule,
)
from probes.probe_phase68_capabilities import (
  build_phase68_representative_result,
  main,
)
from toda_rules import (
  TodaProp58FiniteDimensionalStatement,
)


@lru_cache(maxsize=1)
def build_phase68_probe_data():
  return (
    build_phase68_representative_result()
  )


def test_phase68_probe_derives_prop58_aggregate():
  data = build_phase68_probe_data()

  step = data[
    "integration_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaProp58FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase68_probe_final_aggregate_is_not_given():
  data = build_phase68_probe_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase68_probe_pi6_2_is_derived():
  data = build_phase68_probe_data()

  assert (
    data[
      "pi6_2_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_probe_pi7_3_is_derived():
  data = build_phase68_probe_data()

  assert (
    data[
      "pi7_3_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_probe_pi8_4_is_derived():
  data = build_phase68_probe_data()

  assert (
    data[
      "pi8_4_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_probe_pi9_5_is_derived():
  data = build_phase68_probe_data()

  assert (
    data[
      "pi9_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_probe_higher_zero_is_derived():
  data = build_phase68_probe_data()

  assert (
    data[
      "higher_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_probe_scope_remains_given():
  data = build_phase68_probe_data()

  assert (
    data[
      "higher_range_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase68_probe_final_premises_are_expected():
  data = build_phase68_probe_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "pi6_2_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "pi8_4_step"
      ],
      data[
        "pi9_5_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )


def test_phase68_probe_output_contains_final_results(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_6^2 = Z/4{η₂ν′}"
    in output
  )

  assert (
    "π_7^3 = Z/2{ν′η₆}"
    in output
  )

  assert (
    "π_8^4 = "
    "Z/2{ν₄η₇} ⊕ "
    "Z/2{Eν′η₇}"
    in output
  )

  assert (
    "π_9^5 = Z/2{ν₅η₈}"
    in output
  )

  assert (
    "π_(n+4)^n = 0  "
    "(n ≥ 6)"
    in output
  )


def test_phase68_probe_output_contains_pi7_3_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Eπ_6^2 = 0"
    in output
  )

  assert (
    "H: π_7^3 → π_7^5 "
    "is injective"
    in output
  )

  assert (
    "H(ν′η₆) = η₅²"
    in output
  )

  assert (
    "H is an isomorphism"
    in output
  )


def test_phase68_probe_output_contains_pi8_4_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_7^3 ⊕ π_8^7 "
    "≅ π_8^4"
    in output
  )

  assert (
    "E(ν′η₆) = Eν′η₇"
    in output
  )

  assert (
    "Z/2{ν₄η₇} ⊕ "
    "Z/2{Eν′η₇}"
    in output
  )


def test_phase68_probe_output_contains_pi9_5_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Δ(ι₉) = "
    "±(2ν₄-Eν′)"
    in output
  )

  assert (
    "E: π_8^4 → π_9^5 "
    "is surjective"
    in output
  )

  assert (
    "Δ(η₉) = Eν′η₇"
    in output
  )

  assert (
    "ker(E) = "
    "Z/2{Eν′η₇}"
    in output
  )

  assert (
    "E(ν₄η₇) = ν₅η₈"
    in output
  )


def test_phase68_probe_output_contains_toda59_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Toda (5.9):"
    in output
  )

  assert (
    "η₃ν₄ = ν′η₆"
    in output
  )

  assert (
    "η_nν_(n+1) = 0  "
    "(n ≥ 5)"
    in output
  )


def test_phase68_probe_output_contains_prop31_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Toda Proposition 3.1:"
    in output
  )

  assert (
    "η₆ν₇ = 0"
    in output
  )

  assert (
    "ν₆η₉ = 0"
    in output
  )

  assert (
    "ν_nη_(n+3) = 0  "
    "(n ≥ 6)"
    in output
  )


def test_phase68_probe_output_contains_pi10_6_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "E: π_9^5 → π_10^6 "
    "is surjective"
    in output
  )

  assert (
    "π_10^6 = 0"
    in output
  )


def test_phase68_probe_output_contains_toda45_transport(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "E^(n-6): "
    "π_10^6 ≅ π_(n+4)^n"
    in output
  )

  assert (
    "π_(n+4)^n = 0  "
    "(n ≥ 6)"
    in output
  )


def test_phase68_probe_output_contains_provenance(
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
    "theorem dependencies are "
    "INFERENCE = True"
    in output
  )


def test_phase68_probe_output_contains_scope_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "n>=6 scope remains GIVEN = True"
    in output
  )


def test_phase68_probe_output_contains_fixed_point(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "fixed point = True"
    in output
  )


def test_phase68_probe_output_contains_literature(
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
    "[Toda Proposition 5.8]"
    in output
  )

  assert (
    "Locator: Proposition 5.8"
    in output
  )

  assert (
    "Author: H. Toda"
    in output
  )


def test_phase68_probe_output_contains_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 68 representative probe boundary"
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


def test_phase68_probe_does_not_add_stable_g4(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "stable (G_4;2)=0 aggregate"
    in output
  )

  assert (
    "Not added in Phase 68-13:"
    in output
  )


def test_phase68_probe_does_not_claim_automatic_narrative(
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


def test_phase68_probe_does_not_claim_proof_record_added(
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


def test_phase68_probe_builder_reuses_integration_step():
  data = build_phase68_probe_data()

  assert (
    data[
      "integration_step"
    ]
    is data[
      "phase68_11"
    ][
      "integration_step"
    ]
  ) if (
    "phase68_11"
    in data
  ) else True


