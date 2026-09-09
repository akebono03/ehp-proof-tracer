from functools import lru_cache

from proof import (
  ProofRule,
)
from probes.probe_phase65_capabilities import (
  build_phase65_representative_result,
  main,
)
from toda_rules import (
  TodaProp56FiniteDimensionalStatement,
)


@lru_cache(maxsize=1)
def build_phase65_probe_data():
  return (
    build_phase65_representative_result()
  )


def test_phase65_probe_derives_prop56_aggregate():
  data = build_phase65_probe_data()

  step = data[
    "integration_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaProp56FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase65_probe_final_aggregate_is_not_given():
  data = build_phase65_probe_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase65_probe_pi5_2_is_derived():
  data = build_phase65_probe_data()

  assert (
    data[
      "pi5_2_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_probe_pi6_3_is_derived():
  data = build_phase65_probe_data()

  assert (
    data[
      "pi6_3_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_probe_pi7_4_is_derived():
  data = build_phase65_probe_data()

  assert (
    data[
      "pi7_4_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_probe_pi8_5_is_derived():
  data = build_phase65_probe_data()

  assert (
    data[
      "pi8_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_probe_higher_result_is_derived():
  data = build_phase65_probe_data()

  assert (
    data[
      "higher_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_probe_scope_remains_given():
  data = build_phase65_probe_data()

  assert (
    data[
      "higher_range_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase65_probe_final_premises_are_expected():
  data = build_phase65_probe_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "pi5_2_step"
      ],
      data[
        "pi6_3_step"
      ],
      data[
        "pi7_4_step"
      ],
      data[
        "pi8_5_step"
      ],
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )


def test_phase65_probe_output_contains_final_results(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_5^2 = Z/2{η₂³}"
    in output
  )

  assert (
    "π_6^3 = Z/4{ν′}"
    in output
  )

  assert (
    "π_7^4 = "
    "Z{ν₄} ⊕ Z/4{Eν′}"
    in output
  )

  assert (
    "π_(n+3)^n = "
    "Z/8{ν_n}  (n ≥ 5)"
    in output
  )


def test_phase65_probe_output_contains_connected_exact_sequence(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_7^3 ─H→ "
    "π_7^5 ─Δ→ "
    "π_5^2 ─E→ "
    "π_6^3 ─H→ "
    "π_6^5"
    in output
  )


def test_phase65_probe_exact_sequence_is_not_split_vertically(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_7^3\n"
    "↓"
    not in output
  )

  assert (
    "π_7^5\n"
    "↓"
    not in output
  )


def test_phase65_probe_output_contains_equation57_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "H(ν′∘η₆) = η₅²"
    in output
  )

  assert (
    "H: π_7^3 → π_7^5 "
    "is surjective"
    in output
  )


def test_phase65_probe_output_contains_nu_prime_order_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "ord(η₃³) = 2"
    in output
  )

  assert (
    "ord(ν′) = 4"
    in output
  )


def test_phase65_probe_output_contains_pi7_4_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_6^3 ⊕ π_7^7 "
    "≅ π_7^4"
    in output
  )

  assert (
    "ν′ ↦ Eν′"
    in output
  )

  assert (
    "ι₇ ↦ ν₄"
    in output
  )


def test_phase65_probe_output_contains_n5_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_8^5 / E²π_6^3 "
    "≅ Z/2"
    in output
  )

  assert (
    "ord(E²ν′) = 4"
    in output
  )

  assert (
    "ord(ν₅) = 8"
    in output
  )


def test_phase65_probe_output_contains_stable_transport_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "E^(n-5): "
    "π_8^5 ≅ π_(n+3)^n"
    in output
  )

  assert (
    "E^(n-5)ν₅ = ν_n"
    in output
  )


def test_phase65_probe_output_contains_provenance(
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
    "theorem dependencies are "
    "INFERENCE = True"
    in output
  )


def test_phase65_probe_output_contains_literature(
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
    "Toda Proposition 5.6"
    in output
  )


def test_phase65_probe_output_contains_completion_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 65 completion boundary"
    in output
  )

  assert (
    "Equation (5.8)"
    in output
  )


def test_phase65_probe_does_not_claim_automatic_narrative(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "automatic proof narrative generation"
    in output
  )


