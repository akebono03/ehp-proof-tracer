from pathlib import Path
import sys

from proof import (
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 70-10 の focused integration builder を
# representative fixture としてそのまま再利用する。
# theorem logic は probe 側へ複製しない。
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

from test_phase70_prop59_integration import (  # noqa: E402
  build_phase70_10_data,
)


def build_phase70_representative_result():
  return build_phase70_10_data()


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


def print_phase70_results(
  representative,
):
  statement = (
    representative[
      "integration_step"
    ].conclusion
  )

  print_section(
    "Toda Proposition 5.9 "
    "finite-dimensional result"
  )

  print(
    "π_7^2 = Z/2{η₂ν′η₆}"
  )
  print(
    "π_8^3 = Z/2{ν′η₆²}"
  )
  print(
    "π_9^4 = "
    "Z/2{ν₄η₇²} ⊕ "
    "Z/2{Eν′η₇²}"
  )
  print(
    "π_10^5 = Z/2{ν₅η₈²}"
  )
  print(
    "π_11^6 = Z{Δι₁₃}"
  )
  print(
    "π_(n+5)^n = 0  "
    "(n ≥ 7)"
  )
  print()

  print(
    "aggregate type = "
    f"{type(statement).__name__}"
  )


def print_phase70_derivation_chain(
  representative,
):
  print_section(
    "Proof-style derivation"
  )

  print(
    "[1] π_7^2"
  )
  print()
  print(
    "Phase 68:"
  )
  print(
    "π_6^2 = Z/4{η₂ν′}"
  )
  print()
  print(
    "Phase 70 suspension/composition branch:"
  )
  print(
    "η₂ν′η₆ has order 2"
  )
  print("↓")
  print(
    "π_7^2 = Z/2{η₂ν′η₆}"
  )
  print()

  print(
    "[2] π_8^3"
  )
  print()
  print(
    "π_7^2 = Z/2{η₂ν′η₆}"
  )
  print(
    "ν′η₆² is the corresponding "
    "π_8^3 generator"
  )
  print("↓")
  print(
    "π_8^3 = Z/2{ν′η₆²}"
  )
  print()

  print(
    "[3] π_9^4"
  )
  print()
  print(
    "Toda (5.6) decomposition "
    "and the Phase 70 lower branches"
  )
  print("↓")
  print(
    "π_9^4 = "
    "Z/2{ν₄η₇²} ⊕ "
    "Z/2{Eν′η₇²}"
  )
  print()

  print(
    "[4] π_10^5"
  )
  print()
  print(
    "π_9^4 = "
    "Z/2{ν₄η₇²} ⊕ "
    "Z/2{Eν′η₇²}"
  )
  print()
  print(
    "Phase 70-5:"
  )
  print(
    "Δ(η₉²) = Eν′η₇²"
  )
  print("↓")
  print(
    "ker(E) = "
    "Z/2{Eν′η₇²}"
  )
  print()
  print(
    "E: π_9^4 → π_10^5 "
    "is surjective"
  )
  print()
  print(
    "E(ν₄η₇²) = ν₅η₈²"
  )
  print("↓")
  print(
    "π_10^5 = Z/2{ν₅η₈²}"
  )
  print()

  print(
    "[5] π_11^6"
  )
  print()
  print(
    "Phase 70-7:"
  )
  print(
    "E(ν₅η₈²) = 0"
  )
  print(
    "π_10^5 = Z/2{ν₅η₈²}"
  )
  print("↓")
  print(
    "H: π_11^6 → π_11^11 "
    "is injective"
  )
  print()

  print(
    "π_11^11 = Z{ι₁₁}"
  )
  print(
    "π_9^5 = Z/2{ν₅η₈}"
  )
  print(
    "Δ(ι₁₁) = ν₅η₈"
  )
  print("↓")
  print(
    "ker(Δ) = Z{2ι₁₁}"
  )
  print()

  print(
    "Toda Proposition 2.7:"
  )
  print(
    "H(Δι₁₃) = ±2ι₁₁"
  )
  print("↓")
  print(
    "π_11^6 = Z{Δι₁₃}"
  )
  print()

  print(
    "[6] π_(n+5)^n"
  )
  print()
  print(
    "π_13^13 = Z{ι₁₃}"
  )
  print(
    "π_11^6 = Z{Δι₁₃}"
  )
  print("↓")
  print(
    "Δ: π_13^13 → π_11^6 "
    "is surjective"
  )
  print()

  print(
    "π_13^13 --Δ--> "
    "π_11^6 --E--> π_12^7"
  )
  print(
    "is exact"
  )
  print("↓")
  print(
    "E: π_11^6 → π_12^7 "
    "is zero"
  )
  print()

  print(
    "π_11^6 --E--> "
    "π_12^7 --H--> π_12^13"
  )
  print(
    "is exact"
  )
  print(
    "π_12^13 = 0"
  )
  print("↓")
  print(
    "E: π_11^6 → π_12^7 "
    "is surjective"
  )
  print()
  print(
    "E is zero and surjective"
  )
  print("↓")
  print(
    "π_12^7 = 0"
  )
  print()

  print(
    "Toda (4.5):"
  )
  print(
    "E^(n-7): "
    "π_12^7 ≅ π_(n+5)^n"
  )
  print("↓")
  print(
    "π_(n+5)^n = 0  "
    "(n ≥ 7)"
  )


def print_phase70_provenance(
  representative,
):
  print_section(
    "Provenance / integration"
  )

  pi7_2_step = (
    representative[
      "pi7_2_step"
    ]
  )

  pi8_3_step = (
    representative[
      "pi8_3_step"
    ]
  )

  pi9_4_step = (
    representative[
      "pi9_4_step"
    ]
  )

  pi10_5_step = (
    representative[
      "pi10_5_step"
    ]
  )

  pi11_6_step = (
    representative[
      "pi11_6_step"
    ]
  )

  higher_zero_step = (
    representative[
      "higher_zero_step"
    ]
  )

  range_step = (
    representative[
      "higher_range_step"
    ]
  )

  integration_step = (
    representative[
      "integration_step"
    ]
  )

  print(
    "π_7^2 result derived = "
    f"{pi7_2_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_8^3 result derived = "
    f"{pi8_3_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_9^4 result derived = "
    f"{pi9_4_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_10^5 result derived = "
    f"{pi10_5_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_11^6 result derived = "
    f"{pi11_6_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "higher five-stem zero derived = "
    f"{higher_zero_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "n>=7 scope remains GIVEN = "
    f"{range_step.rule == ProofRule.GIVEN}"
  )

  print(
    "final aggregate derived = "
    f"{integration_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "final aggregate is GIVEN = "
    f"{integration_step.rule == ProofRule.GIVEN}"
  )

  theorem_dependencies = (
    pi7_2_step,
    pi8_3_step,
    pi9_4_step,
    pi10_5_step,
    pi11_6_step,
    higher_zero_step,
  )

  theorem_dependencies_are_inference = all(
    step.rule == ProofRule.INFERENCE
    for step in theorem_dependencies
  )

  print(
    "all six theorem branches are "
    "INFERENCE = "
    f"{theorem_dependencies_are_inference}"
  )

  print(
    "final premise count = "
    f"{len(integration_step.premises)}"
  )

  print(
    "staged one-shot aggregate = True"
  )


def print_phase70_literature(
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


def print_phase70_boundary():
  print_section(
    "Phase 70 representative probe boundary"
  )

  print(
    "Displayed:"
  )
  print(
    "  π_7^2 = Z/2{η₂ν′η₆}"
  )
  print(
    "  π_8^3 = Z/2{ν′η₆²}"
  )
  print(
    "  π_9^4 = "
    "Z/2{ν₄η₇²} ⊕ "
    "Z/2{Eν′η₇²}"
  )
  print(
    "  π_10^5 = Z/2{ν₅η₈²}"
  )
  print(
    "  π_11^6 = Z{Δι₁₃}"
  )
  print(
    "  π_(n+5)^n = 0, n>=7"
  )
  print(
    "  representative proof-style display"
  )
  print(
    "  machine provenance status"
  )
  print(
    "  Proposition 5.9 literature metadata"
  )
  print()

  print(
    "Not added in Phase 70-12:"
  )
  print(
    "  new mathematical inference rules"
  )
  print(
    "  proof record documentation"
  )
  print(
    "  stable (G_5;2)=0 aggregate"
  )
  print(
    "  automatic proof narrative generation"
  )
  print(
    "  generic theorem explanation engine"
  )
  print(
    "  persistent Proof Repository"
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
    "Phase 70 capability demonstration"
  )

  representative = (
    build_phase70_representative_result()
  )

  print_phase70_results(
    representative
  )

  print_phase70_derivation_chain(
    representative
  )

  print_phase70_provenance(
    representative
  )

  print_phase70_literature(
    representative
  )

  print_phase70_boundary()


if __name__ == "__main__":
  main()



