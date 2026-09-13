from pathlib import Path
import sys

from homotopy_groups import (
  HomotopyGroup,
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
  Toda211OrdinaryEHPExactnessStatement,
  TodaDeltaInjectiveStatement,
  TodaLemma510IndexedHopfBracketContainsStatement,
  TodaLemma510Nu6OrdinaryCompositionReductionStatement,
  TodaLemma510OrdinarySuspensionImageFiniteStatement,
  TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement,
  TodaLemma510Split115Statement,
)


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

from test_phase72r9_corrected_provenance_retirement import (  # noqa: E402
  build_phase72r9_data,
)


def build_phase72_representative_result():
  return build_phase72r9_data()


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
    "Toda Lemma 5.10 corrected result"
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
    "ambient group = ordinary π₁₁(S⁶)"
  )
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
    "Corrected proof-style derivation"
  )

  print("[1] Ordinary EHP exactness")
  print()
  print("Toda (2.11), m=5, i=10:")
  print("m>1, m odd, 10 < 3*5-1 = 14")
  print("↓")
  print("π₁₀(S⁵) --E--> π₁₁(S⁶) --H--> π₁₁(S¹¹)")
  print("is an ordinary exactness window.")
  print()

  print("[2] Proposition 2.6 and Toda (1.15)")
  print()
  print("ν₆η₉ = 0")
  print("η₈∘2ι₉ = 0")
  print("Δ(ι₁₁) = ν₅η₈")
  print("↓")
  print("H{ν₆,η₉,2ι₁₀}_1 contains 2ι₁₁")
  print()
  print("Toda (1.15), n=1, m=0:")
  print("{ν₆,η₉,2ι₁₀}_1 ⊂ {ν₆,η₉,2ι₁₀}")
  print("↓")
  print("H{ν₆,η₉,2ι₁₀} contains 2ι₁₁")
  print()

  print("[3] Ordinary E-H core")
  print()
  print("H(Δι₁₃) = ±2ι₁₁")
  print("+ ordinary E-H exactness")
  print("↓")
  print("Δ(ι₁₃) ∈ {ν₆,η₉,2ι₁₀} + Eπ₁₀(S⁵)")
  print()

  print("[4] Corrected ordinary indeterminacy")
  print()
  print("Serre (4.2): π₁₁(S⁹) is finite.")
  print("ν₆ is 2-primary.")
  print("↓")
  print("ν₆∘π₁₁(S⁹) = ν₆∘π₁₁⁹")
  print()
  print("π₁₁⁹ = Z/2{η₉²}")
  print("ν₆η₉ = 0")
  print("↓")
  print("ν₆∘π₁₁(S⁹) = 0")
  print("↓")
  print("Indeterminacy = 2π₁₁(S⁶)")
  print()

  print("[5] Corrected ordinary suspension image")
  print()
  print("Serre (4.2): π₁₀(S⁵) is finite.")
  print("↓")
  print("Eπ₁₀(S⁵) is finite.")
  print()
  print("π₁₀⁵ = Z/2{ν₅η₈²}")
  print("E(ν₅η₈²)=0")
  print("↓")
  print("the 2-primary part of Eπ₁₀(S⁵) is zero")
  print("↓")
  print("Eπ₁₀(S⁵) ⊂ 2π₁₁(S⁶)")
  print()

  print("[6] Toda Lemma 5.10")
  print()
  print("Δ(ι₁₃) ∈ {ν₆,η₉,2ι₁₀} + Eπ₁₀(S⁵)")
  print("Indeterminacy = 2π₁₁(S⁶)")
  print("Eπ₁₀(S⁵) ⊂ 2π₁₁(S⁶)")
  print("↓")
  print("Δ(ι₁₃) ∈ {ν₆,η₉,2ι₁₀} mod 2π₁₁(S⁶)")


def print_phase72_source_reuse(
  representative,
):
  print_section(
    "Corrected representative source objects"
  )

  final_ancestors = representative[
    "final_ancestors"
  ]

  checks = (
    (
      "ordinary Toda (2.11) exactness reachable",
      Toda211OrdinaryEHPExactnessStatement,
    ),
    (
      "Prop.2.6 indexed bracket reachable",
      TodaLemma510IndexedHopfBracketContainsStatement,
    ),
    (
      "Toda (1.15) split reachable",
      TodaLemma510Split115Statement,
    ),
    (
      "composition-level primary reduction reachable",
      TodaLemma510Nu6OrdinaryCompositionReductionStatement,
    ),
    (
      "ordinary finite E-image reachable",
      TodaLemma510OrdinarySuspensionImageFiniteStatement,
    ),
    (
      "ordinary E-image 2-primary zero reachable",
      TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement,
    ),
  )

  for label, statement_type in checks:
    present = any(
      isinstance(
        ancestor.conclusion,
        statement_type,
      )
      for ancestor
      in final_ancestors
    )
    print(
      f"{label} = {present}"
    )


def print_phase72_provenance(
  representative,
):
  print_section(
    "Corrected provenance / retirement audit"
  )

  final_step = representative[
    "final_step"
  ]
  core_step = representative[
    "core_step"
  ]
  indeterminacy_step = representative[
    "indeterminacy_step"
  ]
  image_step = representative[
    "image_step"
  ]

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

  legacy_core_absent = (
    id(
      representative[
        "legacy"
      ][
        "core_step"
      ]
    )
    not in representative[
      "final_ancestor_ids"
    ]
  )

  legacy_indeterminacy_absent = (
    id(
      representative[
        "legacy"
      ][
        "indeterminacy_step"
      ]
    )
    not in representative[
      "final_ancestor_ids"
    ]
  )

  legacy_image_absent = (
    id(
      representative[
        "legacy"
      ][
        "image_step"
      ]
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

  final_ordinary = (
    final_step
    .conclusion
    .ambient_group
    == HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )

  print(
    "final modulo statement derived = "
    f"{final_step.rule == ProofRule.INFERENCE}"
  )
  print(
    "final modulo statement is GIVEN = "
    f"{final_step.rule == ProofRule.GIVEN}"
  )
  print(
    "final ambient group is ordinary = "
    f"{final_ordinary}"
  )
  print(
    "core branch derived = "
    f"{core_step.rule == ProofRule.INFERENCE}"
  )
  print(
    "indeterminacy branch derived = "
    f"{indeterminacy_step.rule == ProofRule.INFERENCE}"
  )
  print(
    "suspension-image branch derived = "
    f"{image_step.rule == ProofRule.INFERENCE}"
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
    "legacy Phase 72 core step absent = "
    f"{legacy_core_absent}"
  )
  print(
    "legacy Phase 72 indeterminacy step absent = "
    f"{legacy_indeterminacy_absent}"
  )
  print(
    "legacy Phase 72 image step absent = "
    f"{legacy_image_absent}"
  )
  print(
    "Phase 71 n=6 Delta injectivity absent = "
    f"{phase71_n6_absent}"
  )


def print_phase72_boundary():
  print_section(
    "Phase 72R corrected representative probe boundary"
  )

  print("Canonical after Phase 72R:")
  print("  ordinary HomotopyGroup semantics")
  print("  Serre (4.2) finite-group applicability")
  print("  ordinary Toda (2.11) EHP exactness")
  print("  ordinary / 2-primary bridge")
  print("  composition-level primary reduction")
  print("  Prop.2.6 indexed bracket")
  print("  Toda (1.15) indexed-to-ordinary bracket inclusion")
  print("  ordinary indeterminacy")
  print("  ordinary suspension-image containment")
  print("  corrected final modulo integration")
  print()

  print("Historical only:")
  print("  original Phase 72 primary-group shortcuts")
  print("  original Phase 72 representative graph")
  print()

  print("Still not added:")
  print("  generic primary-decomposition solver")
  print("  generic Toda-bracket coset algebra")
  print("  generic quotient normalization")
  print("  generic finite-group automorphism solver")
  print("  automatic proof narrative generation")
  print("  persistent Proof Repository")
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
  print("EHP Proof Tracer")
  print("Phase 72R corrected capability demonstration")

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
