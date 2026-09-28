from functools import lru_cache

from proof import (
  ProofRule,
)
from probes.probe_phase73_capabilities import (
  build_phase73_representative_result,
  main,
)
from toda_rules import (
  TodaProp511FiniteDimensionalStatement,
  TodaProp511NuSquaredFiniteDimensionalStatement,
)


@lru_cache(maxsize=1)
def build_phase73_probe_data():
  return (
    build_phase73_representative_result()
  )


def test_phase73_probe_derives_prop511_aggregate():
  data = build_phase73_probe_data()

  step = (
    data[
      "final_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaProp511FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase73_probe_final_aggregate_is_not_given():
  data = build_phase73_probe_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase73_probe_pi8_2_is_derived():
  data = build_phase73_probe_data()

  assert (
    data[
      "pi8_2_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_probe_pi9_3_zero_is_derived():
  data = build_phase73_probe_data()

  assert (
    data[
      "pi9_3_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_probe_pi10_4_is_derived():
  data = build_phase73_probe_data()

  assert (
    data[
      "pi10_4_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_probe_nu_squared_aggregate_is_derived():
  data = build_phase73_probe_data()

  step = (
    data[
      "nu_squared_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaProp511NuSquaredFiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase73_probe_final_premises_are_expected():
  data = build_phase73_probe_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi8_2_step"
      ],
      data[
        "pi9_3_zero_step"
      ],
      data[
        "pi10_4_step"
      ],
      data[
        "nu_squared_step"
      ],
    )
  )


def test_phase73_probe_builder_reuses_integration_step():
  data = build_phase73_probe_data()

  direct = (
    build_phase73_representative_result()
  )

  assert (
    data[
      "final_step"
    ]
    is direct[
      "final_step"
    ]
  )


def test_phase73_probe_output_contains_heading(
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
    "Phase 73 capability demonstration"
    in output
  )

  assert (
    "Toda Proposition 5.11 "
    "finite-dimensional result"
    in output
  )


def test_phase73_probe_output_contains_final_results(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_8^2 = "
    "Z/2{η₂ν′η₆²}"
    in output
  )

  assert (
    "π_9^3 = 0"
    in output
  )

  assert (
    "π_10^4 = "
    "Z/8{ν₄²}"
    in output
  )

  assert (
    "π_(n+6)^n = "
    "Z/2{ν_n²}  "
    "(n ≥ 5)"
    in output
  )


def test_phase73_probe_output_contains_aggregate_type(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "aggregate type = "
    "TodaProp511FiniteDimensionalStatement"
    in output
  )


def test_phase73_probe_output_contains_proof_style_heading(
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


def test_phase73_probe_output_contains_pi8_2_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[1] π_8^2"
    in output
  )

  assert (
    "π_8^3 = Z/2{ν′η₆²}"
    in output
  )

  assert (
    "η₂∘- : π_8^3 ≅ π_8^2"
    in output
  )

  assert (
    "π_8^2 = Z/2{η₂ν′η₆²}"
    in output
  )


def test_phase73_probe_output_contains_pi9_3_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[2] π_9^3"
    in output
  )

  assert (
    "Phase 73-4:"
    in output
  )

  assert (
    "π_9^3 = 0"
    in output
  )


def test_phase73_probe_output_contains_pi10_4_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[3] π_10^4"
    in output
  )

  assert (
    "ν₄² := ν₄∘ν₇"
    in output
  )

  assert (
    "π_10^4 = Z/8{ν₄²}"
    in output
  )


def test_phase73_probe_output_contains_513_relations(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[4] Toda (5.13) supporting relations"
    in output
  )

  assert (
    "Δ(ν₉) = ±2ν₄²"
    in output
  )

  assert (
    "Δ(η₁₁²) = 0"
    in output
  )

  assert (
    "Δ(η₁₃) = 0"
    in output
  )


def test_phase73_probe_output_contains_n5_n6_n7_branches(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_11^5 = Z/2{ν₅²}"
    in output
  )

  assert (
    "π_12^6 = Z/2{ν₆²}"
    in output
  )

  assert (
    "π_13^7 = Z/2{ν₇²}"
    in output
  )


def test_phase73_probe_output_contains_n8_transport(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[6] n=8"
    in output
  )

  assert (
    "π_13^7 ⊕ π_14^15 ≅ π_14^8"
    in output
  )

  assert (
    "π_14^15 = 0"
    in output
  )

  assert (
    "E: π_13^7 ≅ π_14^8"
    in output
  )

  assert (
    "π_14^8 = Z/2{ν₈²}"
    in output
  )


def test_phase73_probe_output_contains_stable_range_transport(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[7] n≥9"
    in output
  )

  assert (
    "E^(n-8): "
    "π_14^8 ≅ π_(n+6)^n"
    in output
  )

  assert (
    "π_(n+6)^n = Z/2{ν_n²}  "
    "(n ≥ 9)"
    in output
  )


def test_phase73_probe_output_contains_six_stem_aggregate(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[8] finite-dimensional "
    "six-stem aggregate"
    in output
  )

  assert (
    "π_(n+6)^n = Z/2{ν_n²}  "
    "(n ≥ 5)"
    in output
  )


def test_phase73_probe_output_contains_final_integration(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[9] Toda Proposition 5.11 "
    "finite-dimensional integration"
    in output
  )

  assert (
    "Toda Proposition 5.11 "
    "finite-dimensional aggregate"
    in output
  )


def test_phase73_probe_output_contains_provenance_heading(
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


def test_phase73_probe_output_contains_branch_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_8^2 result derived = True"
    in output
  )

  assert (
    "π_9^3 zero derived = True"
    in output
  )

  assert (
    "π_10^4 result derived = True"
    in output
  )

  assert (
    "ν_n² finite-dimensional aggregate "
    "derived = True"
    in output
  )

  assert (
    "all four direct Proposition 5.11 "
    "branches are INFERENCE = True"
    in output
  )


def test_phase73_probe_output_contains_final_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
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
    "final premise count = 4"
    in output
  )


def test_phase73_probe_output_defers_stable_branch(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "stable branch included = False"
    in output
  )

  assert (
    "stable (G_6;2) remains deferred = True"
    in output
  )


def test_phase73_probe_output_contains_staged_boundary(
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


def test_phase73_probe_output_contains_literature(
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
    "[Toda Proposition 5.11]"
    in output
  )

  assert (
    "Locator: Proposition 5.11"
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


def test_phase73_probe_output_contains_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 73 representative probe boundary"
    in output
  )

  assert (
    "Not added in Phase 73-8E3:"
    in output
  )

  assert (
    "new mathematical inference rules"
    in output
  )

  assert (
    "new theorem representation"
    in output
  )


def test_phase73_probe_boundary_defers_stable_g6(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "stable (G_6;2)=Z/2{ν²}"
    in output
  )

  assert (
    "stable homotopy-group model"
    in output
  )

  assert (
    "Not added in Phase 73-8E3:"
    in output
  )


def test_phase73_probe_does_not_claim_automatic_narrative(
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


def test_phase73_probe_does_not_claim_proof_record_added(
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


