from pathlib import Path
import sys

from proof import (
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 74-9 の applicability / provenance builder を
# representative fixture としてそのまま再利用する。
#
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

from test_phase74_lemma512_applicability_provenance import (  # noqa: E402
  build_phase74_9_data,
)


def build_phase74_representative_result():
  return build_phase74_9_data()


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


def print_phase74_results(
  representative,
):
  final_step = (
    representative[
      "final_step"
    ]
  )

  statement = (
    final_step.conclusion
  )

  print_section(
    "Toda Lemma 5.12 result"
  )

  print(
    "{η_n, ν_(n+1), η_(n+4)}"
  )
  print(
    "="
  )
  print(
    "{ν_n²}"
  )
  print(
    "for n >= 6"
  )
  print()

  print(
    "ν_n² = "
    "ν_n composed with ν_(n+3)"
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

  print(
    "is GIVEN = "
    f"{final_step.rule == ProofRule.GIVEN}"
  )


def print_phase74_derivation_chain(
  representative,
):
  print_section(
    "Proof-style derivation"
  )

  print(
    "[1] Bracket defined"
  )
  print()
  print(
    "Phase 68:"
  )
  print(
    "η_n ν_(n+1) = 0"
  )
  print(
    "ν_n η_(n+3) = 0"
  )
  print(
    "(n >= 6)"
  )
  print()
  print(
    "shift n -> n+1 in the second relation"
  )
  print("↓")
  print(
    "ν_(n+1) η_(n+4) = 0"
  )
  print("↓")
  print(
    "{η_n, ν_(n+1), η_(n+4)} "
    "is defined"
  )
  print()

  print(
    "[2] First indeterminacy"
  )
  print()
  print(
    "η_n composed with "
    "π_(n+6)(S^(n+1))"
  )
  print()
  print(
    "Toda (3.2) + Toda (4.7)"
  )
  print(
    "and Proposition 5.9"
  )
  print("↓")
  print(
    "first indeterminacy = 0"
  )
  print()

  print(
    "[3] Second indeterminacy"
  )
  print()
  print(
    "π_(n+5)(S^n) composed with "
    "η_(n+5)"
  )
  print()

  print(
    "n >= 7:"
  )
  print(
    "Proposition 5.9 gives "
    "π_(n+5)^n = 0"
  )
  print("↓")
  print(
    "second indeterminacy = 0"
  )
  print()

  print(
    "n = 6:"
  )
  print(
    "π_11^6 = Z{Δι₁₃}"
  )
  print(
    "Δ(η₁₃) = 0"
  )
  print(
    "Δι₁₃ composed with η₁₁ "
    "= Δ(η₁₃)"
  )
  print("↓")
  print(
    "second indeterminacy = 0"
  )
  print()

  print(
    "[4] Singleton mod two"
  )
  print()
  print(
    "first indeterminacy = 0"
  )
  print(
    "second indeterminacy = 0"
  )
  print("↓")
  print(
    "the bracket is a singleton"
  )
  print()

  print(
    "Toda Proposition 5.11:"
  )
  print(
    "π_(n+6)^n = Z/2{ν_n²}"
  )
  print(
    "(n >= 5)"
  )
  print("↓")
  print(
    "{η_n, ν_(n+1), η_(n+4)}"
  )
  print(
    "= {x_n ν_n²}"
  )
  print(
    "x_n in {0,1}"
  )
  print(
    "(n >= 6)"
  )
  print()

  print(
    "[5] Coefficient stability"
  )
  print()
  print(
    "Toda Proposition 1.3 "
    "+ Toda (1.15)"
  )
  print(
    "+ E(ν_n²) = ν_(n+1)²"
  )
  print("↓")
  print(
    "x_n = x_(n+1)"
  )
  print(
    "(n >= 6)"
  )
  print()

  print(
    "[6] Nonzero anchor"
  )
  print()
  print(
    "Toda Lemma 5.5"
  )
  print(
    "m=6, t=7, β=ν₆"
  )
  print()
  print(
    "Phase 68:"
  )
  print(
    "ν₆η₉ = 0"
  )
  print("↓")
  print(
    "{η₈, ν₉, η₁₂}_3"
  )
  print(
    "contains ±ν₈²"
  )
  print()

  print(
    "Toda (1.15)"
  )
  print("↓")
  print(
    "{η₈, ν₉, η₁₂}"
  )
  print(
    "contains ±ν₈²"
  )
  print()

  print(
    "the ambient group has order two"
  )
  print("↓")
  print(
    "{η₈, ν₉, η₁₂}"
  )
  print(
    "= {ν₈²}"
  )
  print("↓")
  print(
    "x_8 = 1"
  )
  print()

  print(
    "[7] Toda Lemma 5.12"
  )
  print()
  print(
    "x_n = x_(n+1)"
  )
  print(
    "and"
  )
  print(
    "x_8 = 1"
  )
  print("↓")
  print(
    "x_n = 1 for every n >= 6"
  )
  print("↓")
  print(
    "{η_n, ν_(n+1), η_(n+4)}"
  )
  print(
    "= {ν_n²}"
  )
  print(
    "(n >= 6)"
  )


def print_phase74_provenance(
  representative,
):
  print_section(
    "Provenance / integration"
  )

  singleton_step = (
    representative[
      "singleton_step"
    ]
  )

  stability_step = (
    representative[
      "stability_step"
    ]
  )

  anchor_step = (
    representative[
      "anchor_step"
    ]
  )

  final_step = (
    representative[
      "final_step"
    ]
  )

  prop511_step = (
    representative[
      "prop511_step"
    ]
  )

  nu_family_step = (
    representative[
      "nu_family_step"
    ]
  )

  nu6_eta9_zero_step = (
    representative[
      "nu6_eta9_zero_step"
    ]
  )

  lemma55_inclusion_step = (
    representative[
      "lemma55_inclusion_step"
    ]
  )

  exact_three_direct_premises = (
    final_step.premises
    == (
      singleton_step,
      stability_step,
      anchor_step,
    )
  )

  print(
    "singleton-mod-two branch derived = "
    f"{singleton_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "coefficient-stability branch derived = "
    f"{stability_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "nonzero-anchor branch derived = "
    f"{anchor_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "final Lemma 5.12 derived = "
    f"{final_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "final Lemma 5.12 is GIVEN = "
    f"{final_step.rule == ProofRule.GIVEN}"
  )

  print()

  print(
    "exact three direct final premises = "
    f"{exact_three_direct_premises}"
  )

  print()

  print(
    "Proposition 5.11 reachable = "
    f"{prop511_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "nu-family reachable = "
    f"{nu_family_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "ν₆η₉=0 reachable = "
    f"{nu6_eta9_zero_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "Lemma 5.5 indexed inclusion reachable = "
    f"{lemma55_inclusion_step.rule == ProofRule.INFERENCE}"
  )


def print_phase74_applicability(
  representative,
):
  print_section(
    "Applicability / non-circularity"
  )

  final_step = (
    representative[
      "final_step"
    ]
  )

  statement = (
    final_step.conclusion
  )

  stability_ancestor_ids = (
    representative[
      "stability_ancestor_ids"
    ]
  )

  anchor_ancestor_ids = (
    representative[
      "anchor_ancestor_ids"
    ]
  )

  stability_step = (
    representative[
      "stability_step"
    ]
  )

  anchor_step = (
    representative[
      "anchor_step"
    ]
  )

  print(
    "range lower bound = "
    f"{statement.n_range.right}"
  )

  print(
    "range is n>=6 = "
    f"{statement.n_range.right == 6}"
  )

  print(
    "anchor dimension = "
    f"{anchor_step.conclusion.anchor_dimension}"
  )

  print(
    "anchor dimension is exactly 8 = "
    f"{anchor_step.conclusion.anchor_dimension == 8}"
  )

  print()

  print(
    "stability does not depend on anchor = "
    f"{id(anchor_step) not in stability_ancestor_ids}"
  )

  print(
    "anchor does not depend on stability = "
    f"{id(stability_step) not in anchor_ancestor_ids}"
  )

  print()

  print(
    "final generator representation = "
    f"{type(statement.generator).__name__}"
  )

  print(
    "ν_n² remains Composition = "
    f"{type(statement.generator).__name__ == 'Composition'}"
  )

  print(
    "explicit coefficient field present = "
    f"{hasattr(statement, 'coefficient')}"
  )

  print(
    "stable branch field present = "
    f"{hasattr(statement, 'stable_group')}"
  )


def print_phase74_boundary():
  print_section(
    "Phase 74 representative probe boundary"
  )

  print(
    "Displayed:"
  )
  print(
    "  Toda Lemma 5.12"
  )
  print(
    "  {η_n,ν_(n+1),η_(n+4)}"
  )
  print(
    "  = {ν_n²}"
  )
  print(
    "  n>=6"
  )
  print(
    "  bracket definedness"
  )
  print(
    "  both indeterminacy-zero branches"
  )
  print(
    "  singleton-mod-two reduction"
  )
  print(
    "  coefficient stability"
  )
  print(
    "  n=8 nonzero anchor"
  )
  print(
    "  final integration"
  )
  print(
    "  machine provenance status"
  )
  print(
    "  applicability / non-circularity status"
  )
  print()

  print(
    "Not added in Phase 74-10:"
  )
  print(
    "  new mathematical inference rules"
  )
  print(
    "  new theorem semantics"
  )
  print(
    "  generic Toda-bracket coset algebra"
  )
  print(
    "  generic coefficient object"
  )
  print(
    "  generic induction engine"
  )
  print(
    "  generic suspension normalizer"
  )
  print(
    "  stable (G_6;2) result"
  )
  print(
    "  proof record documentation"
  )
  print(
    "  automatic proof narrative generation"
  )
  print(
    "  persistent Proof Repository"
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
    "Phase 74 capability demonstration"
  )

  representative = (
    build_phase74_representative_result()
  )

  print_phase74_results(
    representative
  )

  print_phase74_derivation_chain(
    representative
  )

  print_phase74_provenance(
    representative
  )

  print_phase74_applicability(
    representative
  )

  print_phase74_boundary()


if __name__ == "__main__":
  main()


