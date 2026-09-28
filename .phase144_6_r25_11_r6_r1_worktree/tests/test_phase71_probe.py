from functools import lru_cache

from proof import (
  ProofRule,
)
from probes.probe_phase71_capabilities import (
  build_phase71_representative_result,
  main,
)
from toda_rules import (
  Toda512DeltaInjectivityStatement,
  TodaDeltaInjectiveStatement,
)


@lru_cache(maxsize=1)
def build_phase71_probe_data():
  return (
    build_phase71_representative_result()
  )


def test_phase71_probe_derives_toda512_aggregate():
  data = build_phase71_probe_data()

  step = (
    data[
      "integration_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    Toda512DeltaInjectivityStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase71_probe_final_aggregate_is_not_given():
  data = build_phase71_probe_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase71_probe_n4_is_derived():
  data = build_phase71_probe_data()

  assert isinstance(
    data[
      "n4_step"
    ].conclusion,
    TodaDeltaInjectiveStatement,
  )

  assert (
    data[
      "n4_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase71_probe_n5_is_derived():
  data = build_phase71_probe_data()

  assert isinstance(
    data[
      "n5_step"
    ].conclusion,
    TodaDeltaInjectiveStatement,
  )

  assert (
    data[
      "n5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase71_probe_n6_is_derived():
  data = build_phase71_probe_data()

  assert isinstance(
    data[
      "n6_step"
    ].conclusion,
    TodaDeltaInjectiveStatement,
  )

  assert (
    data[
      "n6_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase71_probe_final_premises_are_expected():
  data = build_phase71_probe_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "n4_step"
      ],
      data[
        "n5_step"
      ],
      data[
        "n6_step"
      ],
    )
  )


def test_phase71_probe_builder_reuses_phase71_6_data():
  data = build_phase71_probe_data()

  direct = (
    build_phase71_representative_result()
  )

  assert (
    data[
      "integration_step"
    ]
    is direct[
      "integration_step"
    ]
  )


def test_phase71_probe_output_contains_heading(
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
    "Phase 71 capability demonstration"
    in output
  )

  assert (
    "Toda (5.12) Delta injectivity"
    in output
  )


def test_phase71_probe_output_contains_three_cases(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Δ: π_11^9 → π_9^4 "
    "is injective  (n=4)"
    in output
  )

  assert (
    "Δ: π_12^11 → π_10^5 "
    "is injective  (n=5)"
    in output
  )

  assert (
    "Δ: π_13^13 → π_11^6 "
    "is injective  (n=6)"
    in output
  )


def test_phase71_probe_output_contains_aggregate_type(
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
    "Toda512DeltaInjectivityStatement"
    in output
  )


def test_phase71_probe_output_contains_proof_style_heading(
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


def test_phase71_probe_output_contains_n4_derivation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[1] n=4"
    in output
  )

  assert (
    "π_11^9 = Z/2{η₉²}"
    in output
  )

  assert (
    "π_9^4 = "
    "Z/2{ν₄η₇²} ⊕ "
    "Z/2{Eν′η₇²}"
    in output
  )

  assert (
    "Δ(η₉²) = Eν′η₇²"
    in output
  )

  assert (
    "Δ: π_11^9 → π_9^4 "
    "is injective"
    in output
  )


def test_phase71_probe_output_contains_n5_derivation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[2] n=5"
    in output
  )

  assert (
    "π_12^11 = Z/2{η₁₁}"
    in output
  )

  assert (
    "π_10^5 = Z/2{ν₅η₈²}"
    in output
  )

  assert (
    "Δ(η₁₁) = ν₅η₈²"
    in output
  )

  assert (
    "Δ: π_12^11 → π_10^5 "
    "is injective"
    in output
  )


def test_phase71_probe_output_contains_n6_derivation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[3] n=6"
    in output
  )

  assert (
    "π_13^13 = Z{ι₁₃}"
    in output
  )

  assert (
    "π_11^6 = Z{Δι₁₃}"
    in output
  )

  assert (
    "Δ: π_13^13 → π_11^6 "
    "is injective"
    in output
  )


def test_phase71_probe_output_contains_integration_derivation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[4] Toda (5.12)"
    in output
  )

  assert (
    "n=4 injectivity"
    in output
  )

  assert (
    "n=5 injectivity"
    in output
  )

  assert (
    "n=6 injectivity"
    in output
  )

  assert (
    "Δ: π_(n+7)^(2n+1) "
    "→ π_(n+5)^n"
    in output
  )

  assert (
    "is injective for n=4,5,6"
    in output
  )


def test_phase71_probe_output_contains_upstream_reuse(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "n=4 Delta value reused = True"
    in output
  )

  assert (
    "n=5 Delta value reused = True"
    in output
  )

  assert (
    "n=6 target group reused = True"
    in output
  )


def test_phase71_probe_output_contains_provenance_heading(
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


def test_phase71_probe_output_contains_branch_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "n=4 injectivity derived = True"
    in output
  )

  assert (
    "n=5 injectivity derived = True"
    in output
  )

  assert (
    "n=6 injectivity derived = True"
    in output
  )

  assert (
    "all three Toda (5.12) cases "
    "are INFERENCE = True"
    in output
  )


def test_phase71_probe_output_contains_final_provenance(
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
    "final premise count = 3"
    in output
  )


def test_phase71_probe_output_contains_upstream_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "n=4 upstream facts are "
    "INFERENCE = True"
    in output
  )

  assert (
    "n=5 upstream facts are "
    "INFERENCE = True"
    in output
  )

  assert (
    "n=6 π_13^13 remains GIVEN = True"
    in output
  )

  assert (
    "n=6 π_11^6 is INFERENCE = True"
    in output
  )


def test_phase71_probe_output_contains_non_circularity(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "final graph acyclic = True"
    in output
  )

  assert (
    "all three branch graphs "
    "acyclic = True"
    in output
  )


def test_phase71_probe_output_contains_staged_boundary(
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


def test_phase71_probe_output_contains_literature(
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
    "[Toda (5.12)]"
    in output
  )

  assert (
    "Locator: Equation (5.12)"
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


def test_phase71_probe_output_contains_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 71 representative probe boundary"
    in output
  )

  assert (
    "Not added in Phase 71-7:"
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


def test_phase71_probe_boundary_defers_lemma510(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Toda Lemma 5.10"
    in output
  )

  assert (
    "bracket coset modulo subgroup "
    "representation"
    in output
  )

  assert (
    "Not added in Phase 71-7:"
    in output
  )


def test_phase71_probe_does_not_claim_automatic_narrative(
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


def test_phase71_probe_boundary_keeps_generic_solvers_deferred(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "generic cyclic-map injectivity solver"
    in output
  )

  assert (
    "generic free-cyclic map solver"
    in output
  )

  assert (
    "persistent Proof Repository"
    in output
  )


