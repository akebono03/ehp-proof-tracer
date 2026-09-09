from pathlib import Path
import sys

from proof import (
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 68-11 の focused integration builder を
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

from test_phase68_prop58_integration import (  # noqa: E402
  build_phase68_11_data,
)


def build_phase68_representative_result():
  return build_phase68_11_data()


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


def print_phase68_results(
  representative,
):
  statement = (
    representative[
      "integration_step"
    ].conclusion
  )

  print_section(
    "Toda Proposition 5.8 "
    "finite-dimensional result"
  )

  print(
    "π_6^2 = Z/4{η₂ν′}"
  )
  print(
    "π_7^3 = Z/2{ν′η₆}"
  )
  print(
    "π_8^4 = "
    "Z/2{ν₄η₇} ⊕ "
    "Z/2{Eν′η₇}"
  )
  print(
    "π_9^5 = Z/2{ν₅η₈}"
  )
  print(
    "π_(n+4)^n = 0  "
    "(n ≥ 6)"
  )
  print()

  print(
    "aggregate type = "
    f"{type(statement).__name__}"
  )


def print_phase68_derivation_chain(
  representative,
):
  print_section(
    "Proof-style derivation"
  )

  print(
    "[1] π_6^2"
  )
  print()
  print(
    "Phase 67:"
  )
  print(
    "E(η₂ν′) = 0"
  )
  print(
    "Δ(ν₅) = ±η₂ν′"
  )
  print("↓")
  print(
    "π_6^2 = Z/4{η₂ν′}"
  )
  print()

  print(
    "[2] π_7^3"
  )
  print()
  print(
    "Eπ_6^2 = 0"
  )
  print("↓")
  print(
    "H: π_7^3 → π_7^5 "
    "is injective"
  )
  print()
  print(
    "H(ν′η₆) = η₅²"
  )
  print(
    "π_7^5 = Z/2{η₅²}"
  )
  print("↓")
  print(
    "H: π_7^3 → π_7^5 "
    "is surjective"
  )
  print("↓")
  print(
    "H is an isomorphism"
  )
  print("↓")
  print(
    "π_7^3 = Z/2{ν′η₆}"
  )
  print()

  print(
    "[3] π_8^4"
  )
  print()
  print(
    "Toda (5.6), i=8:"
  )
  print(
    "π_7^3 ⊕ π_8^7 "
    "≅ π_8^4"
  )
  print(
    "(α,β) ↦ "
    "Eα + ν₄β"
  )
  print()
  print(
    "π_7^3 = Z/2{ν′η₆}"
  )
  print(
    "π_8^7 = Z/2{η₇}"
  )
  print(
    "E(ν′η₆) = Eν′η₇"
  )
  print("↓")
  print(
    "π_8^4 = "
    "Z/2{ν₄η₇} ⊕ "
    "Z/2{Eν′η₇}"
  )
  print()

  print(
    "[4] π_9^5"
  )
  print()
  print(
    "Toda (5.8):"
  )
  print(
    "Δ(ι₉) = "
    "±(2ν₄-Eν′)"
  )
  print("↓")
  print(
    "Δ: π_9^9 → π_7^4 "
    "is injective"
  )
  print("↓")
  print(
    "H: π_9^5 → π_9^9 "
    "is zero"
  )
  print("↓")
  print(
    "E: π_8^4 → π_9^5 "
    "is surjective"
  )
  print()

  print(
    "Δ(η₉) = Eν′η₇"
  )
  print("↓")
  print(
    "ker(E) = "
    "Z/2{Eν′η₇}"
  )
  print()
  print(
    "π_8^4 = "
    "Z/2{ν₄η₇} ⊕ "
    "Z/2{Eν′η₇}"
  )
  print("↓")
  print(
    "π_9^5 = "
    "Z/2{E(ν₄η₇)}"
  )
  print(
    "E(ν₄η₇) = ν₅η₈"
  )
  print("↓")
  print(
    "π_9^5 = Z/2{ν₅η₈}"
  )
  print()

  print(
    "[5] π_(n+4)^n"
  )
  print()
  print(
    "Toda (5.9):"
  )
  print(
    "η₃ν₄ = ν′η₆"
  )
  print("↓ E²")
  print(
    "η₅ν₆ = E²ν′η₈"
  )
  print()
  print(
    "2ν₅ = E²ν′"
  )
  print(
    "π_9^5 = Z/2{ν₅η₈}"
  )
  print("↓")
  print(
    "η₅ν₆ = 0"
  )
  print("↓")
  print(
    "η_nν_(n+1) = 0  "
    "(n ≥ 5)"
  )
  print()

  print(
    "n=6 specialization:"
  )
  print(
    "η₆ν₇ = 0"
  )
  print()

  print(
    "Toda Proposition 3.1:"
  )
  print(
    "η₂∧ν₄ "
    "represents both "
    "±η₆ν₇ and ±ν₆η₉"
  )
  print("↓")
  print(
    "ν₆η₉ = 0"
  )
  print("↓")
  print(
    "ν_nη_(n+3) = 0  "
    "(n ≥ 6)"
  )
  print()

  print(
    "π_9^5 = Z/2{ν₅η₈}"
  )
  print(
    "E: π_9^5 → π_10^6 "
    "is surjective"
  )
  print(
    "ν₆η₉ = 0"
  )
  print("↓")
  print(
    "π_10^6 = 0"
  )
  print()

  print(
    "Toda (4.5):"
  )
  print(
    "E^(n-6): "
    "π_10^6 ≅ π_(n+4)^n"
  )
  print("↓")
  print(
    "π_(n+4)^n = 0  "
    "(n ≥ 6)"
  )


def print_phase68_provenance(
  representative,
):
  print_section(
    "Provenance / integration"
  )

  pi6_2_step = (
    representative[
      "pi6_2_step"
    ]
  )

  pi7_3_step = (
    representative[
      "pi7_3_step"
    ]
  )

  pi8_4_step = (
    representative[
      "pi8_4_step"
    ]
  )

  pi9_5_step = (
    representative[
      "pi9_5_step"
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

  result = (
    representative[
      "result"
    ]
  )

  print(
    "π_6^2 result derived = "
    f"{pi6_2_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_7^3 result derived = "
    f"{pi7_3_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_8^4 result derived = "
    f"{pi8_4_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_9^5 result derived = "
    f"{pi9_5_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "higher four-stem zero derived = "
    f"{higher_zero_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "n>=6 scope remains GIVEN = "
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
    pi6_2_step,
    pi7_3_step,
    pi8_4_step,
    pi9_5_step,
    higher_zero_step,
  )

  theorem_dependencies_are_inference = all(
    step.rule == ProofRule.INFERENCE
    for step in theorem_dependencies
  )

  print(
    "theorem dependencies are "
    "INFERENCE = "
    f"{theorem_dependencies_are_inference}"
  )

  print(
    "final premise count = "
    f"{len(integration_step.premises)}"
  )

  print(
    "fixed point = "
    f"{result.termination_reason.value == 'fixed_point'}"
  )


def print_phase68_literature(
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


def print_phase68_boundary():
  print_section(
    "Phase 68 representative probe boundary"
  )

  print(
    "Displayed:"
  )
  print(
    "  π_6^2 = Z/4{η₂ν′}"
  )
  print(
    "  π_7^3 = Z/2{ν′η₆}"
  )
  print(
    "  π_8^4 = "
    "Z/2{ν₄η₇} ⊕ "
    "Z/2{Eν′η₇}"
  )
  print(
    "  π_9^5 = Z/2{ν₅η₈}"
  )
  print(
    "  π_(n+4)^n = 0, n>=6"
  )
  print(
    "  representative proof-style display"
  )
  print(
    "  machine provenance status"
  )
  print(
    "  Proposition 5.8 literature metadata"
  )
  print()

  print(
    "Not added in Phase 68-13:"
  )
  print(
    "  new mathematical inference rules"
  )
  print(
    "  proof record documentation"
  )
  print(
    "  stable (G_4;2)=0 aggregate"
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
    "Phase 68 capability demonstration"
  )

  representative = (
    build_phase68_representative_result()
  )

  print_phase68_results(
    representative
  )

  print_phase68_derivation_chain(
    representative
  )

  print_phase68_provenance(
    representative
  )

  print_phase68_literature(
    representative
  )

  print_phase68_boundary()


if __name__ == "__main__":
  main()


