from functools import lru_cache

from proof import (
  ProofRule,
)
from probes.probe_phase67_capabilities import (
  build_phase67_representative_result,
  main,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaSurjectiveStatement,
  TodaLemma57TwoIota5ImageMembershipStatement,
  TodaProp42ExactnessStatement,
)


@lru_cache(maxsize=1)
def build_phase67_probe_data():
  return (
    build_phase67_representative_result()
  )


def test_phase67_probe_reuses_nu_prime_hypothesis():
  data = build_phase67_probe_data()

  step = (
    data[
      "phase67_5"
    ][
      "hypothesis_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma57TwoIota5ImageMembershipStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase67_probe_reuses_eta2_nu_prime_zero():
  data = build_phase67_probe_data()

  assert (
    data[
      "eta2_nu_prime_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_probe_reuses_pi6_2_result():
  data = build_phase67_probe_data()

  assert (
    data[
      "pi6_2_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_probe_reuses_exactness_result():
  data = build_phase67_probe_data()

  step = data[
    "exactness_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaProp42ExactnessStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase67_probe_reuses_delta_surjectivity():
  data = build_phase67_probe_data()

  step = data[
    "delta_surjective_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaDeltaSurjectiveStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase67_probe_final_delta_relation_is_derived():
  data = build_phase67_probe_data()

  step = data[
    "final_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase67_probe_final_result_is_not_given():
  data = build_phase67_probe_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase67_probe_final_premises_are_derived():
  data = build_phase67_probe_data()

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise
    in data[
      "final_step"
    ].premises
  )


def test_phase67_probe_structural_window_remains_given():
  data = build_phase67_probe_data()

  assert (
    data[
      "window_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase67_probe_output_contains_general_result(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 67 capability demonstration"
    in output
  )

  assert (
    "Toda Lemma 5.7 result"
    in output
  )

  assert (
    "E²α ∈ 2ι₅∘π_(i+2)(S⁵)"
    in output
  )

  assert (
    "E(η₂∘α) = 0"
    in output
  )


def test_phase67_probe_output_contains_special_results(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "E(η₂∘ν′) = 0"
    in output
  )

  assert (
    "Δ(ν₅) = ±(η₂∘ν′)"
    in output
  )


def test_phase67_probe_output_contains_general_derivation(
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
    "E²(η₂∘α)"
    in output
  )

  assert (
    "= η₄∘E²α."
    in output
  )

  assert (
    "2η₄=0"
    in output
  )

  assert (
    "By Toda Lemma 4.5 "
    "for n=3"
    in output
  )


def test_phase67_probe_output_contains_nu_prime_specialization(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "2Eν₄ = E²ν′."
    in output
  )

  assert (
    "Since ν₅=Eν₄"
    in output
  )

  assert (
    "E²ν′ ∈ 2ι₅∘π_8(S⁵)."
    in output
  )


def test_phase67_probe_output_contains_pi6_2_calculation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "η₂∘- : π_6^3 ≅ π_6^2."
    in output
  )

  assert (
    "π_6^3 = Z/4{ν′}."
    in output
  )

  assert (
    "π_6^2 = Z/4{η₂∘ν′}."
    in output
  )


def test_phase67_probe_output_contains_delta_exactness_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_8^5 ─Δ→ π_6^2 ─E→ π_7^3."
    in output
  )

  assert (
    "Δ(π_8^5)=π_6^2."
    in output
  )

  assert (
    "π_8^5 = Z/8{ν₅}."
    in output
  )

  assert (
    "π_6^2 = <Δ(ν₅)>."
    in output
  )


def test_phase67_probe_output_contains_provenance(
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
    "E²ν′ image hypothesis derived = True"
    in output
  )

  assert (
    "E(η₂∘ν′)=0 derived = True"
    in output
  )

  assert (
    "π_6^2=Z/4{η₂∘ν′} derived = True"
    in output
  )

  assert (
    "Δ surjective derived = True"
    in output
  )

  assert (
    "Δ(ν₅)=±(η₂∘ν′) derived = True"
    in output
  )


def test_phase67_probe_output_contains_given_inference_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "final result is GIVEN = False"
    in output
  )

  assert (
    "all final premises are INFERENCE = True"
    in output
  )

  assert (
    "structural window "
    "remains GIVEN = True"
    in output
  )

  assert (
    "Phase 66 dependency used = False"
    in output
  )

  assert (
    "fixed point = True"
    in output
  )


def test_phase67_probe_output_contains_source(
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
    "[Toda Lemma 5.7]"
    in output
  )

  assert (
    "Locator: Lemma 5.7"
    in output
  )

  assert (
    "Author: H. Toda"
    in output
  )


def test_phase67_probe_output_contains_proof_record(
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
    in output
  )

  assert (
    "docs/proof_records.md"
    in output
  )

  assert (
    "Toda Lemma 5.7"
    in output
  )


def test_phase67_probe_does_not_claim_automatic_narrative(
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


def test_phase67_probe_output_contains_completion_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 67 completion boundary"
    in output
  )

  assert (
    "generic image-membership framework"
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


