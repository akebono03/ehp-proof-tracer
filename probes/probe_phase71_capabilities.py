from pathlib import Path
import sys

from proof import (
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 71-6 の provenance builder を
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

from test_phase71_applicability_provenance import (  # noqa: E402
  build_phase71_6_data,
)


def build_phase71_representative_result():
  return build_phase71_6_data()


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


def print_phase71_results(
  representative,
):
  statement = (
    representative[
      "integration_step"
    ].conclusion
  )

  print_section(
    "Toda (5.12) "
    "Delta injectivity"
  )

  print(
    "Δ: π_11^9 → π_9^4 "
    "is injective  (n=4)"
  )
  print(
    "Δ: π_12^11 → π_10^5 "
    "is injective  (n=5)"
  )
  print(
    "Δ: π_13^13 → π_11^6 "
    "is injective  (n=6)"
  )
  print()

  print(
    "aggregate type = "
    f"{type(statement).__name__}"
  )


def print_phase71_derivation_chain(
  representative,
):
  print_section(
    "Proof-style derivation"
  )

  phase71_2 = (
    representative[
      "phase71_2"
    ]
  )

  phase71_3 = (
    representative[
      "phase71_3"
    ]
  )

  phase71_4 = (
    representative[
      "phase71_4"
    ]
  )

  print(
    "[1] n=4"
  )
  print()
  print(
    "Toda Proposition 5.3:"
  )
  print(
    "π_11^9 = Z/2{η₉²}"
  )
  print()
  print(
    "Phase 70:"
  )
  print(
    "π_9^4 = "
    "Z/2{ν₄η₇²} ⊕ "
    "Z/2{Eν′η₇²}"
  )
  print(
    "Δ(η₉²) = Eν′η₇²"
  )
  print("↓")
  print(
    "the nonzero generator of "
    "π_11^9 maps to an "
    "order-two summand generator"
  )
  print("↓")
  print(
    "Δ: π_11^9 → π_9^4 "
    "is injective"
  )
  print()

  print(
    "[2] n=5"
  )
  print()
  print(
    "Toda Proposition 5.1:"
  )
  print(
    "π_12^11 = Z/2{η₁₁}"
  )
  print()
  print(
    "Phase 70:"
  )
  print(
    "π_10^5 = Z/2{ν₅η₈²}"
  )
  print(
    "Δ(η₁₁) = ν₅η₈²"
  )
  print("↓")
  print(
    "the source generator maps "
    "to the target generator"
  )
  print("↓")
  print(
    "Δ: π_12^11 → π_10^5 "
    "is injective"
  )
  print()

  print(
    "[3] n=6"
  )
  print()
  print(
    "Phase 70:"
  )
  print(
    "π_13^13 = Z{ι₁₃}"
  )
  print(
    "π_11^6 = Z{Δι₁₃}"
  )
  print("↓")
  print(
    "ι₁₃ maps to the free "
    "generator Δι₁₃"
  )
  print("↓")
  print(
    "Δ: π_13^13 → π_11^6 "
    "is injective"
  )
  print()

  print(
    "[4] Toda (5.12)"
  )
  print()
  print(
    "n=4 injectivity"
  )
  print(
    "n=5 injectivity"
  )
  print(
    "n=6 injectivity"
  )
  print("↓")
  print(
    "Δ: π_(n+7)^(2n+1) "
    "→ π_(n+5)^n"
  )
  print(
    "is injective for n=4,5,6"
  )
  print()

  print(
    "Representative source objects:"
  )
  print(
    "  n=4 Delta value reused = "
    f"{phase71_2['delta_eta9_squared_step'].rule == ProofRule.INFERENCE}"
  )
  print(
    "  n=5 Delta value reused = "
    f"{phase71_3['delta_eta11_step'].rule == ProofRule.INFERENCE}"
  )
  print(
    "  n=6 target group reused = "
    f"{phase71_4['pi11_6_step'].rule == ProofRule.INFERENCE}"
  )


def print_phase71_provenance(
  representative,
):
  print_section(
    "Provenance / integration"
  )

  n4_step = (
    representative[
      "n4_step"
    ]
  )

  n5_step = (
    representative[
      "n5_step"
    ]
  )

  n6_step = (
    representative[
      "n6_step"
    ]
  )

  integration_step = (
    representative[
      "integration_step"
    ]
  )

  all_three_cases_are_inference = all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in (
      n4_step,
      n5_step,
      n6_step,
    )
  )

  n4_upstream_are_inference = all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in representative[
      "n4_direct_dependencies"
    ]
  )

  n5_upstream_are_inference = all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in representative[
      "n5_direct_dependencies"
    ]
  )

  n6_pi13_13_is_given = (
    representative[
      "n6_pi13_13_step"
    ].rule
    == ProofRule.GIVEN
  )

  n6_pi11_6_is_inference = (
    representative[
      "n6_pi11_6_step"
    ].rule
    == ProofRule.INFERENCE
  )

  final_is_acyclic = (
    id(
      integration_step
    )
    not in representative[
      "integration_ancestor_ids"
    ]
  )

  branches_are_acyclic = all(
    id(
      step
    )
    not in representative[
      "branch_ancestor_ids"
    ][
      id(
        step
      )
    ]
    for step
    in (
      n4_step,
      n5_step,
      n6_step,
    )
  )

  print(
    "n=4 injectivity derived = "
    f"{n4_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "n=5 injectivity derived = "
    f"{n5_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "n=6 injectivity derived = "
    f"{n6_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "all three Toda (5.12) cases "
    "are INFERENCE = "
    f"{all_three_cases_are_inference}"
  )

  print(
    "final aggregate derived = "
    f"{integration_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "final aggregate is GIVEN = "
    f"{integration_step.rule == ProofRule.GIVEN}"
  )

  print(
    "final premise count = "
    f"{len(integration_step.premises)}"
  )

  print(
    "n=4 upstream facts are "
    "INFERENCE = "
    f"{n4_upstream_are_inference}"
  )

  print(
    "n=5 upstream facts are "
    "INFERENCE = "
    f"{n5_upstream_are_inference}"
  )

  print(
    "n=6 π_13^13 remains GIVEN = "
    f"{n6_pi13_13_is_given}"
  )

  print(
    "n=6 π_11^6 is INFERENCE = "
    f"{n6_pi11_6_is_inference}"
  )

  print(
    "final graph acyclic = "
    f"{final_is_acyclic}"
  )

  print(
    "all three branch graphs "
    "acyclic = "
    f"{branches_are_acyclic}"
  )

  print(
    "staged one-shot aggregate = True"
  )


def print_phase71_literature(
  representative,
):
  print_section(
    "Literature statements used"
  )

  statements = (
    representative[
      "integration_step"
    ]
    .conclusion
    .literature_statements
  )

  for statement in statements:
    reference = (
      statement.reference
    )

    print(
      f"[{reference.label}]"
    )
    print(
      "Locator: "
      f"{reference.locator}"
    )
    print(
      "Author: "
      f"{reference.author}"
    )
    print(
      "Source: "
      f"{reference.title}"
    )
    print(
      "Year: "
      f"{reference.year}"
    )
    print(
      "Statement:"
    )
    print(
      f"  {statement.statement}"
    )
    print()


def print_phase71_boundary():
  print_section(
    "Phase 71 representative probe boundary"
  )

  print(
    "Displayed:"
  )
  print(
    "  Toda (5.12)"
  )
  print(
    "  n=4 Delta injectivity"
  )
  print(
    "  n=5 Delta injectivity"
  )
  print(
    "  n=6 Delta injectivity"
  )
  print(
    "  three-case aggregate"
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
  print(
    "  Toda (5.12) literature metadata"
  )
  print()

  print(
    "Not added in Phase 71-7:"
  )
  print(
    "  new mathematical inference rules"
  )
  print(
    "  new theorem representation"
  )
  print(
    "  proof record documentation"
  )
  print(
    "  Toda Lemma 5.10"
  )
  print(
    "  bracket coset modulo subgroup "
    "representation"
  )
  print(
    "  automatic proof narrative generation"
  )
  print(
    "  generic cyclic-map injectivity solver"
  )
  print(
    "  generic free-cyclic map solver"
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
    "Phase 71 capability demonstration"
  )

  representative = (
    build_phase71_representative_result()
  )

  print_phase71_results(
    representative
  )

  print_phase71_derivation_chain(
    representative
  )

  print_phase71_provenance(
    representative
  )

  print_phase71_literature(
    representative
  )

  print_phase71_boundary()


if __name__ == "__main__":
  main()



