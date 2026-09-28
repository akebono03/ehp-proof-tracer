from pathlib import Path
import sys

from proof import (
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 65-9 の focused integration builder を
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

from test_phase65_prop56_integration import (  # noqa: E402
  build_phase65_9_data,
)


def build_phase65_representative_result():
  return build_phase65_9_data()


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


def print_phase65_results(
  representative,
):
  statement = (
    representative[
      "integration_step"
    ].conclusion
  )

  print_section(
    "Toda Proposition 5.6 "
    "finite-dimensional result"
  )

  print(
    "π_5^2 = Z/2{η₂³}"
  )
  print(
    "π_6^3 = Z/4{ν′}"
  )
  print(
    "π_7^4 = "
    "Z{ν₄} ⊕ Z/4{Eν′}"
  )
  print(
    "π_8^5 = Z/8{ν₅}"
  )
  print(
    "π_(n+3)^n = "
    "Z/8{ν_n}  (n ≥ 6)"
  )
  print()
  print(
    "Therefore:"
  )
  print(
    "π_(n+3)^n = "
    "Z/8{ν_n}  (n ≥ 5)"
  )
  print()

  print(
    "aggregate type = "
    f"{type(statement).__name__}"
  )


def print_phase65_exact_sequence():
  print_section(
    "EHP exact sequence used"
  )

  print(
    "π_7^3 ─H→ "
    "π_7^5 ─Δ→ "
    "π_5^2 ─E→ "
    "π_6^3 ─H→ "
    "π_6^5"
  )


def print_phase65_derivation_chain(
  representative,
):
  print_section(
    "Proof-style derivation"
  )

  print(
    "π_5^2 = Z/2{η₂³}"
  )
  print(
    "  [Toda (5.2), "
    "Proposition 5.3]"
  )
  print()

  print(
    "H(ν′∘η₆) = η₅²"
  )
  print(
    "π_7^5 = Z/2{η₅²}"
  )
  print("↓")
  print(
    "H: π_7^3 → π_7^5 "
    "is surjective"
  )
  print()

  print_phase65_exact_sequence()
  print()

  print(
    "H surjective"
  )
  print("↓")
  print(
    "Δ: π_7^5 → π_5^2 "
    "is zero"
  )
  print("↓")
  print(
    "E: π_5^2 → π_6^3 "
    "is injective"
  )
  print()

  print(
    "π_5^2 = Z/2{η₂³}"
  )
  print(
    "E injective"
  )
  print("↓")
  print(
    "ord(η₃³) = 2"
  )
  print()

  print(
    "2ν′ = η₃³"
  )
  print("↓")
  print(
    "ord(ν′) = 4"
  )
  print("↓")
  print(
    "π_6^3 = Z/4{ν′}"
  )
  print()

  print(
    "Toda (5.6), i=7:"
  )
  print(
    "π_6^3 ⊕ π_7^7 "
    "≅ π_7^4"
  )
  print(
    "(α,β) ↦ "
    "Eα + ν₄∘β"
  )
  print()
  print(
    "ν′ ↦ Eν′"
  )
  print(
    "ι₇ ↦ ν₄"
  )
  print("↓")
  print(
    "π_7^4 = "
    "Z{ν₄} ⊕ Z/4{Eν′}"
  )
  print()

  print(
    "Toda Proposition 5.6, "
    "n=5 branch:"
  )
  print(
    "π_8^5 / E²π_6^3 "
    "≅ Z/2"
  )
  print(
    "E²: π_6^3 → π_8^5 "
    "is injective"
  )
  print()

  print(
    "π_6^3 = Z/4{ν′}"
  )
  print(
    "E² injective"
  )
  print("↓")
  print(
    "ord(E²ν′) = 4"
  )
  print()

  print(
    "2ν₅ = E²ν′"
  )
  print("↓")
  print(
    "ord(ν₅) = 8"
  )
  print()

  print(
    "π_8^5 / E²π_6^3 "
    "≅ Z/2"
  )
  print(
    "|E²π_6^3| = 4"
  )
  print("↓")
  print(
    "|π_8^5| = 8"
  )
  print(
    "ord(ν₅) = 8"
  )
  print("↓")
  print(
    "π_8^5 = Z/8{ν₅}"
  )
  print()

  print(
    "Toda (4.5), n ≥ 6:"
  )
  print(
    "E^(n-5): "
    "π_8^5 ≅ π_(n+3)^n"
  )
  print("↓")
  print(
    "π_(n+3)^n = "
    "Z/8{E^(n-5)ν₅}"
  )
  print()

  print(
    "E^(n-5)ν₅ = ν_n"
  )
  print("↓")
  print(
    "π_(n+3)^n = "
    "Z/8{ν_n}  (n ≥ 6)"
  )
  print()

  print(
    "n=5 branch + n≥6 branch"
  )
  print("↓")
  print(
    "π_(n+3)^n = "
    "Z/8{ν_n}  (n ≥ 5)"
  )


def print_phase65_provenance(
  representative,
):
  print_section(
    "Provenance / integration"
  )

  pi5_2_step = (
    representative[
      "pi5_2_step"
    ]
  )

  pi6_3_step = (
    representative[
      "pi6_3_step"
    ]
  )

  pi7_4_step = (
    representative[
      "pi7_4_step"
    ]
  )

  pi8_5_step = (
    representative[
      "pi8_5_step"
    ]
  )

  higher_step = (
    representative[
      "higher_step"
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
    "π_5^2 result derived = "
    f"{pi5_2_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_6^3 result derived = "
    f"{pi6_3_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_7^4 result derived = "
    f"{pi7_4_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_8^5 result derived = "
    f"{pi8_5_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "higher ν-family result derived = "
    f"{higher_step.rule == ProofRule.INFERENCE}"
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
    pi5_2_step,
    pi6_3_step,
    pi7_4_step,
    pi8_5_step,
    higher_step,
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


def print_phase65_literature(
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
    reference = statement.reference

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


def print_phase65_boundary():
  print_section(
    "Phase 65 completion boundary"
  )

  print(
    "Implemented:"
  )
  print(
    "  π_5^2 = Z/2{η₂³}"
  )
  print(
    "  π_6^3 = Z/4{ν′}"
  )
  print(
    "  π_7^4 = "
    "Z{ν₄} ⊕ Z/4{Eν′}"
  )
  print(
    "  π_(n+3)^n = "
    "Z/8{ν_n}, n>=5"
  )
  print(
    "  representative proof-style display"
  )
  print(
    "  full provenance regression"
  )
  print()

  print(
    "Deferred:"
  )
  print(
    "  stable ν"
  )
  print(
    "  stable 4ν=η³"
  )
  print(
    "  Equation (5.8)"
  )
  print(
    "  automatic proof narrative generation"
  )


def main():
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 65 capability demonstration"
  )

  representative = (
    build_phase65_representative_result()
  )

  print_phase65_results(
    representative
  )

  print_phase65_derivation_chain(
    representative
  )

  print_phase65_provenance(
    representative
  )

  print_phase65_literature(
    representative
  )

  print_phase65_boundary()


if __name__ == "__main__":
  main()


