from functools import lru_cache

from proof import (
  ProofRule,
)
from probes.probe_phase72_capabilities import (
  build_phase72_representative_result,
  main,
)
from toda_rules import (
  Toda54IndeterminacyGeneratorStatement,
  TodaLemma510BracketModuloStatement,
  TodaLemma510BracketPlusSuspensionImageStatement,
  TodaLemma510SuspensionImageInDoubleStatement,
)


@lru_cache(maxsize=1)
def build_phase72_probe_data():
  return (
    build_phase72_representative_result()
  )


def test_phase72_probe_derives_final_statement():
  data = build_phase72_probe_data()

  step = (
    data[
      "final_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma510BracketModuloStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase72_probe_final_is_not_given():
  data = build_phase72_probe_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase72_probe_core_is_derived():
  data = build_phase72_probe_data()

  assert isinstance(
    data[
      "core_step"
    ].conclusion,
    TodaLemma510BracketPlusSuspensionImageStatement,
  )

  assert (
    data[
      "core_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_probe_indeterminacy_is_derived():
  data = build_phase72_probe_data()

  assert isinstance(
    data[
      "indeterminacy_step"
    ].conclusion,
    Toda54IndeterminacyGeneratorStatement,
  )

  assert (
    data[
      "indeterminacy_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_probe_image_containment_is_derived():
  data = build_phase72_probe_data()

  assert isinstance(
    data[
      "image_step"
    ].conclusion,
    TodaLemma510SuspensionImageInDoubleStatement,
  )

  assert (
    data[
      "image_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_probe_final_premises_are_expected():
  data = build_phase72_probe_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "core_step"
      ],
      data[
        "indeterminacy_step"
      ],
      data[
        "image_step"
      ],
    )
  )


def test_phase72_probe_builder_reuses_phase72_5_data():
  data = build_phase72_probe_data()

  direct = (
    build_phase72_representative_result()
  )

  assert (
    data[
      "final_step"
    ]
    is direct[
      "final_step"
    ]
  )


def test_phase72_probe_output_contains_heading(
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
    "Phase 72 capability demonstration"
    in output
  )

  assert (
    "Toda Lemma 5.10 result"
    in output
  )


def test_phase72_probe_output_contains_final_result(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Δ(ι₁₃)"
    in output
  )

  assert (
    "{ν₆, η₉, 2ι₁₀}"
    in output
  )

  assert (
    "mod 2π₁₁(S⁶)"
    in output
  )

  assert (
    "statement type = "
    "TodaLemma510BracketModuloStatement"
    in output
  )

  assert (
    "derived = True"
    in output
  )


def test_phase72_probe_output_contains_proof_style_heading(
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


def test_phase72_probe_output_contains_indeterminacy_derivation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[1] Toda bracket indeterminacy"
    in output
  )

  assert (
    "π₁₁⁹ = Z/2{η₉²}"
    in output
  )

  assert (
    "ν₆η₉ = 0"
    in output
  )

  assert (
    "π₁₁⁶ = Z{Δι₁₃}"
    in output
  )

  assert (
    "ν₆∘π₁₁⁹ + 2π₁₁⁶"
    in output
  )

  assert (
    "Indeterminacy"
    in output
  )

  assert (
    "= 2π₁₁⁶"
    in output
  )


def test_phase72_probe_output_contains_hopf_bracket_derivation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[2] Hopf image of the bracket"
    in output
  )

  assert (
    "Δ(ι₁₁) = ν₅η₈"
    in output
  )

  assert (
    "Toda Proposition 2.6:"
    in output
  )

  assert (
    "H{ν₆,η₉,2ι₁₀}"
    in output
  )

  assert (
    "contains 2ι₁₁"
    in output
  )


def test_phase72_probe_output_contains_exactness_core(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[3] E-H exactness core"
    in output
  )

  assert (
    "H(Δι₁₃) = ±2ι₁₁"
    in output
  )

  assert (
    "π₁₀(S⁵)"
    in output
  )

  assert (
    "π₁₁(S⁶)"
    in output
  )

  assert (
    "π₁₁(S¹¹)"
    in output
  )

  assert (
    "+ Eπ₁₀(S⁵)"
    in output
  )


def test_phase72_probe_output_contains_image_containment(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[4] Suspension-image containment"
    in output
  )

  assert (
    "π₁₀⁵ = Z/2{ν₅η₈²}"
    in output
  )

  assert (
    "π₁₁⁶ = Z{Δι₁₃}"
    in output
  )

  assert (
    "2π₁₁(S⁶)"
    in output
  )


def test_phase72_probe_output_contains_final_derivation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[5] Toda Lemma 5.10"
    in output
  )

  assert (
    "Indeterminacy = 2π₁₁(S⁶)"
    in output
  )

  assert (
    "Eπ₁₀(S⁵) ⊂ 2π₁₁(S⁶)"
    in output
  )

  assert (
    "mod 2π₁₁(S⁶)"
    in output
  )


def test_phase72_probe_output_contains_source_reuse(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Representative source objects"
    in output
  )

  assert (
    "Proposition 5.3 reused = True"
    in output
  )

  assert (
    "ν₆η₉=0 reused = True"
    in output
  )

  assert (
    "Δ(ι₁₁)=ν₅η₈ reused = True"
    in output
  )

  assert (
    "H(Δι₁₃)=±2ι₁₁ reused = True"
    in output
  )

  assert (
    "E-H exactness reused = True"
    in output
  )

  assert (
    "π₁₀⁵ reused = True"
    in output
  )

  assert (
    "π₁₁⁶ reused = True"
    in output
  )


def test_phase72_probe_output_contains_provenance_heading(
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


def test_phase72_probe_output_contains_final_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "final modulo statement derived = True"
    in output
  )

  assert (
    "final modulo statement is GIVEN = False"
    in output
  )

  assert (
    "exact three direct premises = True"
    in output
  )


def test_phase72_probe_output_contains_branch_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "core branch derived = True"
    in output
  )

  assert (
    "indeterminacy branch derived = True"
    in output
  )

  assert (
    "suspension-image branch derived = True"
    in output
  )


def test_phase72_probe_output_contains_non_circularity(
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
    "Phase 71 Delta injectivity "
    "absent from ancestry = True"
    in output
  )


def test_phase72_probe_output_contains_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 72 representative probe boundary"
    in output
  )

  assert (
    "new mathematical inference rules"
    in output
  )

  assert (
    "generic Toda-bracket coset algebra"
    in output
  )

  assert (
    "automatic proof narrative generation"
    in output
  )


def test_phase72_probe_output_marks_hand_authored_presentation(
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


