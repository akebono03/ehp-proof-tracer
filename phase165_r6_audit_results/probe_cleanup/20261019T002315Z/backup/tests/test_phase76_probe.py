from functools import (
  lru_cache,
)

from proof import (
  ProofRule,
)
from probes.probe_phase76_capabilities import (
  build_phase76_representative_result,
  main,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)


@lru_cache(maxsize=1)
def build_phase76_probe_data():
  return (
    build_phase76_representative_result()
  )


def test_phase76_probe_reuses_phase76_5_final_step():
  data = build_phase76_probe_data()

  assert (
    data[
      "final_step"
    ]
    is build_phase76_representative_result()[
      "final_step"
    ]
  )


def test_phase76_probe_kernel_is_derived():
  data = build_phase76_probe_data()

  assert isinstance(
    data[
      "kernel_step"
    ].conclusion,
    TodaSuspensionKernelFreeCyclicStatement,
  )

  assert (
    data[
      "kernel_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase76_probe_exactness_is_derived():
  data = build_phase76_probe_data()

  assert isinstance(
    data[
      "exactness_step"
    ].conclusion,
    TodaProp42ExactnessStatement,
  )

  assert (
    data[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase76_probe_delta_image_is_derived():
  data = build_phase76_probe_data()

  assert isinstance(
    data[
      "delta_image_step"
    ].conclusion,
    TodaDeltaImageFreeCyclicStatement,
  )

  assert (
    data[
      "delta_image_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase76_probe_final_is_derived():
  data = build_phase76_probe_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase76_probe_structural_window_remains_given():
  data = build_phase76_probe_data()

  assert (
    data[
      "window_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase76_probe_pi17_17_fact_remains_given():
  data = build_phase76_probe_data()

  assert (
    data[
      "pi17_17_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase76_probe_output_contains_heading(
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
    "Phase 76 capability demonstration"
    in output
  )

  assert (
    "Toda Equation (5.16) result"
    in output
  )


def test_phase76_probe_output_contains_kernel(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Ker("
    in output
  )

  assert (
    "E: π_15^8 -> π_16^9"
    in output
  )

  assert (
    "= Z{2σ₈-Eσ'}"
    in output
  )


def test_phase76_probe_output_contains_delta_image(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Im("
    in output
  )

  assert (
    "Δ: π_17^17 -> π_15^8"
    in output
  )

  assert (
    "= Z{2σ₈-Eσ'}"
    in output
  )


def test_phase76_probe_output_contains_final_relation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_17^17 = Z{ι₁₇}"
    in output
  )

  assert (
    "Δ(ι₁₇)"
    in output
  )

  assert (
    "= ±(2σ₈-Eσ')"
    in output
  )


def test_phase76_probe_output_contains_derivation(
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

  assert (
    "[1] Phase 75 input"
    in output
  )

  assert (
    "[2] Suspension kernel"
    in output
  )

  assert (
    "[3] Toda Proposition 4.2 exactness"
    in output
  )

  assert (
    "[4] Diagonal source generator"
    in output
  )

  assert (
    "[5] Toda Equation (5.16)"
    in output
  )


def test_phase76_probe_output_contains_provenance(
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
    "Phase 76-2 kernel derived = True"
    in output
  )

  assert (
    "concrete exactness derived = True"
    in output
  )

  assert (
    "Phase 76-3 Delta image derived = True"
    in output
  )

  assert (
    "final Equation (5.16) derived = True"
    in output
  )

  assert (
    "final Equation (5.16) is GIVEN = False"
    in output
  )


def test_phase76_probe_output_contains_phase75_reachability(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 75 σ₈ reachable = True"
    in output
  )

  assert (
    "Phase 75 σ₉ definition reachable = True"
    in output
  )

  assert (
    "Phase 75 π_15^8 reachable = True"
    in output
  )

  assert (
    "Phase 75 π_16^9 reachable = True"
    in output
  )

  assert (
    "Phase 75 final aggregate required = False"
    in output
  )


def test_phase76_probe_output_contains_non_circularity(
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

  assert (
    "π_17^17 is used to derive kernel = False"
    in output
  )

  assert (
    "π_17^17 is used to derive exactness = False"
    in output
  )


def test_phase76_probe_output_contains_source(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Literature / source"
    in output
  )

  assert (
    "[Toda Equation (5.16)]"
    in output
  )

  assert (
    "Locator: Equation (5.16)"
    in output
  )

  assert (
    "Author: H. Toda"
    in output
  )


def test_phase76_probe_output_contains_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 76 representative probe boundary"
    in output
  )

  assert (
    "generic mixed free/torsion kernel solver"
    in output
  )

  assert (
    "generic sign algebra"
    in output
  )

  assert (
    "automatic proof narrative generation"
    in output
  )

  assert (
    "persistent Proof Repository"
    in output
  )


def test_phase76_probe_output_contains_next_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Next mathematical boundary:"
    in output
  )

  assert (
    "Toda Lemma 5.16"
    in output
  )


def test_phase76_probe_does_not_claim_automatic_narrative(
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
