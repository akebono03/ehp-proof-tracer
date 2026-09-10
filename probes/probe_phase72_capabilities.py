from pathlib import Path
import sys

from homotopy_groups import (
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
)


# Phase 72-5 の provenance builder を
# representative fixture としてそのまま再利用する。
# theorem logic や provenance traversal を
# probe 側へ複製しない。
_TESTS_DIR = (
  Path(__file__)
  .resolve()
  .parents[1]
  / "tests"
)

if str(_TESTS_DIR) not in sys.path:
  sys.path.insert(
    0,
    str(_TESTS_DIR),
  )

from test_phase72_applicability_provenance import (  # noqa: E402
  build_phase72_5_data,
)


def build_phase72_representative_result():
  return build_phase72_5_data()


def print_section(
  title,
):
  print()
  print_separator()
  print(
    title
  )
  print_separator()
  print()


def print_phase72_results(
  representative,
):
  final_step = (
    representative[
      "final_step"
    ]
  )

  statement = (
    final_step
    .conclusion
  )

  print_section(
    "Toda Lemma 5.10 result"
  )

  print(
    "Δ(ι₁₃)"
  )
  print(
    "∈"
  )
  print(
    "{ν₆, η₉, 2ι₁₀}"
  )
  print(
    "mod 2π₁₁(S⁶)"
  )
  print()

  print(
    "statement type = "
    f"{type(statement).__name__}"
  )
  print(
    "derived = "
    f"{final_step.rule == ProofRule.INFERENCE}"
  )


def print_phase72_derivation_chain(
  representative,
):
  print_section(
    "Proof-style derivation"
  )

  print(
    "[1] Toda bracket indeterminacy"
  )
  print()

  print(
    "Toda Proposition 5.3 / (5.9):"
  )
  print(
    "π₁₁⁹ = Z/2{η₉²}"
  )
  print()

  print(
    "Phase 68:"
  )
  print(
    "ν₆η₉ = 0"
  )
  print()

  print(
    "Phase 70:"
  )
  print(
    "π₁₁⁶ = Z{Δι₁₃}"
  )
  print()

  print(
    "Toda (4.7) indeterminacy:"
  )
  print(
    "ν₆∘π₁₁⁹ + 2π₁₁⁶"
  )
  print("↓")
  print(
    "ν₆∘π₁₁⁹ = 0"
  )
  print("↓")
  print(
    "Indeterminacy"
  )
  print(
    "= 2π₁₁⁶"
  )
  print()

  print(
    "[2] Hopf image of the bracket"
  )
  print()

  print(
    "Phase 69 / Toda (5.10):"
  )
  print(
    "Δ(ι₁₁) = ν₅η₈"
  )
  print()

  print(
    "Toda Proposition 2.6:"
  )
  print(
    "H{ν₆,η₉,2ι₁₀}"
  )
  print(
    "contains 2ι₁₁"
  )
  print()

  print(
    "[3] E-H exactness core"
  )
  print()

  print(
    "Phase 70:"
  )
  print(
    "H(Δι₁₃) = ±2ι₁₁"
  )
  print()

  print(
    "Exact sequence:"
  )
  print(
    "π₁₀(S⁵)"
  )
  print(
    "  --E-->"
  )
  print(
    "π₁₁(S⁶)"
  )
  print(
    "  --H-->"
  )
  print(
    "π₁₁(S¹¹)"
  )
  print()

  print(
    "The bracket and Δ(ι₁₃)"
  )
  print(
    "have the same Hopf value "
    "up to sign"
  )
  print("↓")
  print(
    "Δ(ι₁₃)"
  )
  print(
    "∈"
  )
  print(
    "{ν₆,η₉,2ι₁₀}"
  )
  print(
    "+ Eπ₁₀(S⁵)"
  )
  print()

  print(
    "[4] Suspension-image containment"
  )
  print()

  print(
    "Phase 70:"
  )
  print(
    "π₁₀⁵ = Z/2{ν₅η₈²}"
  )
  print(
    "π₁₁⁶ = Z{Δι₁₃}"
  )
  print()

  print(
    "The suspension image from the "
    "finite order-two source"
  )
  print(
    "into the free cyclic target "
    "is contained in"
  )
  print(
    "2π₁₁(S⁶)"
  )
  print()

  print(
    "[5] Toda Lemma 5.10"
  )
  print()

  print(
    "Δ(ι₁₃)"
  )
  print(
    "∈"
  )
  print(
    "{ν₆,η₉,2ι₁₀}"
  )
  print(
    "+ Eπ₁₀(S⁵)"
  )
  print()

  print(
    "Indeterminacy = 2π₁₁(S⁶)"
  )
  print(
    "Eπ₁₀(S⁵) ⊂ 2π₁₁(S⁶)"
  )
  print("↓")
  print(
    "Δ(ι₁₃)"
  )
  print(
    "∈"
  )
  print(
    "{ν₆,η₉,2ι₁₀}"
  )
  print(
    "mod 2π₁₁(S⁶)"
  )
  print()


def print_phase72_source_reuse(
  representative,
):
  print_section(
    "Representative source objects"
  )

  prop53_is_inference = (
    representative[
      "prop53_step"
    ].rule
    == ProofRule.INFERENCE
  )

  nu6_eta9_is_inference = (
    representative[
      "nu6_eta9_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  delta_iota11_is_inference = (
    representative[
      "delta_iota11_step"
    ].rule
    == ProofRule.INFERENCE
  )

  hopf_delta_is_inference = (
    representative[
      "hopf_delta_step"
    ].rule
    == ProofRule.INFERENCE
  )

  exactness_is_inference = (
    representative[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )

  pi10_5_is_inference = (
    representative[
      "pi10_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  pi11_6_is_inference = (
    representative[
      "pi11_6_step"
    ].rule
    == ProofRule.INFERENCE
  )

  print(
    "Proposition 5.3 reused = "
    f"{prop53_is_inference}"
  )

  print(
    "ν₆η₉=0 reused = "
    f"{nu6_eta9_is_inference}"
  )

  print(
    "Δ(ι₁₁)=ν₅η₈ reused = "
    f"{delta_iota11_is_inference}"
  )

  print(
    "H(Δι₁₃)=±2ι₁₁ reused = "
    f"{hopf_delta_is_inference}"
  )

  print(
    "E-H exactness reused = "
    f"{exactness_is_inference}"
  )

  print(
    "π₁₀⁵ reused = "
    f"{pi10_5_is_inference}"
  )

  print(
    "π₁₁⁶ reused = "
    f"{pi11_6_is_inference}"
  )


def print_phase72_provenance(
  representative,
):
  print_section(
    "Provenance / integration"
  )

  final_step = (
    representative[
      "final_step"
    ]
  )

  core_step = (
    representative[
      "core_step"
    ]
  )

  indeterminacy_step = (
    representative[
      "indeterminacy_step"
    ]
  )

  image_step = (
    representative[
      "image_step"
    ]
  )

  final_is_inference = (
    final_step.rule
    == ProofRule.INFERENCE
  )

  final_is_given = (
    final_step.rule
    == ProofRule.GIVEN
  )

  core_is_inference = (
    core_step.rule
    == ProofRule.INFERENCE
  )

  indeterminacy_is_inference = (
    indeterminacy_step.rule
    == ProofRule.INFERENCE
  )

  image_is_inference = (
    image_step.rule
    == ProofRule.INFERENCE
  )

  exact_three_direct_premises = (
    final_step.premises
    == (
      core_step,
      indeterminacy_step,
      image_step,
    )
  )

  final_is_acyclic = (
    id(
      final_step
    )
    not in representative[
      "final_ancestor_ids"
    ]
  )

  phase71_n6_statement = (
    TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=13,
          sphere_dimension=13,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
      )
    )
  )

  phase71_n6_absent = all(
    ancestor.conclusion
    != phase71_n6_statement
    for ancestor
    in representative[
      "final_ancestors"
    ]
  )

  print(
    "final modulo statement derived = "
    f"{final_is_inference}"
  )

  print(
    "final modulo statement is GIVEN = "
    f"{final_is_given}"
  )

  print(
    "core branch derived = "
    f"{core_is_inference}"
  )

  print(
    "indeterminacy branch derived = "
    f"{indeterminacy_is_inference}"
  )

  print(
    "suspension-image branch derived = "
    f"{image_is_inference}"
  )

  print(
    "exact three direct premises = "
    f"{exact_three_direct_premises}"
  )

  print(
    "final graph acyclic = "
    f"{final_is_acyclic}"
  )

  print(
    "Phase 71 Delta injectivity "
    "absent from ancestry = "
    f"{phase71_n6_absent}"
  )


def print_phase72_boundary():
  print_section(
    "Phase 72 representative probe boundary"
  )

  print(
    "Displayed:"
  )
  print(
    "  Toda Lemma 5.10"
  )
  print(
    "  bracket indeterminacy reduction"
  )
  print(
    "  Hopf image consequence"
  )
  print(
    "  E-H exactness core"
  )
  print(
    "  suspension-image containment"
  )
  print(
    "  final modulo statement"
  )
  print(
    "  representative proof-style display"
  )
  print(
    "  machine provenance status"
  )
  print(
    "  non-circularity status"
  )
  print()

  print(
    "Not added in Phase 72-6:"
  )
  print(
    "  new mathematical inference rules"
  )
  print(
    "  new theorem representation"
  )
  print(
    "  generic Toda-bracket coset algebra"
  )
  print(
    "  generic quotient normalization"
  )
  print(
    "  generic finite-subgroup solver"
  )
  print(
    "  automatic proof narrative generation"
  )
  print(
    "  persistent Proof Repository"
  )
  print(
    "  completion documentation"
  )
  print(
    "  next Toda theorem"
  )
  print()

  print(
    "The proof-style derivation above is "
    "hand-authored presentation code."
  )
  print(
    "It is not yet generated "
    "automatically from the ProofStep graph."
  )


def main():
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 72 capability demonstration"
  )

  representative = (
    build_phase72_representative_result()
  )

  print_phase72_results(
    representative
  )

  print_phase72_derivation_chain(
    representative
  )

  print_phase72_source_reuse(
    representative
  )

  print_phase72_provenance(
    representative
  )

  print_phase72_boundary()


if __name__ == "__main__":
  main()


