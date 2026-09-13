from pathlib import Path
import sys

from proof import (
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 73-8E1 の finite-dimensional integration builder を
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

from test_phase73_prop511_finite_dimensional_integration import (  # noqa: E402
  build_phase73_8e_data,
)


def build_phase73_representative_result():
  return build_phase73_8e_data()


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


def print_phase73_results(
  representative,
):
  statement = (
    representative[
      "final_step"
    ].conclusion
  )

  print_section(
    "Toda Proposition 5.11 "
    "finite-dimensional result"
  )

  print(
    "π_8^2 = "
    "Z/2{η₂ν′η₆²}"
  )
  print(
    "π_9^3 = 0"
  )
  print(
    "π_10^4 = "
    "Z/8{ν₄²}"
  )
  print(
    "π_(n+6)^n = "
    "Z/2{ν_n²}  "
    "(n ≥ 5)"
  )
  print()

  print(
    "aggregate type = "
    f"{type(statement).__name__}"
  )


def print_phase73_derivation_chain(
  representative,
):
  print_section(
    "Proof-style derivation"
  )

  print(
    "[1] π_8^2"
  )
  print()
  print(
    "Phase 70:"
  )
  print(
    "π_8^3 = Z/2{ν′η₆²}"
  )
  print()
  print(
    "Toda (5.2):"
  )
  print(
    "η₂∘- : π_8^3 ≅ π_8^2"
  )
  print("↓")
  print(
    "π_8^2 = Z/2{η₂ν′η₆²}"
  )
  print()

  print(
    "[2] π_9^3"
  )
  print()
  print(
    "Phase 73-4:"
  )
  print(
    "the concrete n=3 branch "
    "is derived independently"
  )
  print("↓")
  print(
    "π_9^3 = 0"
  )
  print()

  print(
    "[3] π_10^4"
  )
  print()
  print(
    "Phase 73-5:"
  )
  print(
    "the concrete n=4 branch "
    "is derived independently"
  )
  print()
  print(
    "ν₄² := ν₄∘ν₇"
  )
  print("↓")
  print(
    "π_10^4 = Z/8{ν₄²}"
  )
  print()

  print(
    "[4] Toda (5.13) supporting relations"
  )
  print()
  print(
    "Phase 73-6A:"
  )
  print(
    "Δ(ν₉) = ±2ν₄²"
  )
  print()
  print(
    "Phase 73-6B:"
  )
  print(
    "Δ(η₁₁²) = 0"
  )
  print()
  print(
    "Phase 73-6C:"
  )
  print(
    "Δ(η₁₃) = 0"
  )
  print()

  print(
    "[5] n=5,6,7"
  )
  print()
  print(
    "Phase 73-7A:"
  )
  print(
    "π_11^5 = Z/2{ν₅²}"
  )
  print()
  print(
    "Phase 73-7B:"
  )
  print(
    "π_12^6 = Z/2{ν₆²}"
  )
  print()
  print(
    "Phase 73-7C:"
  )
  print(
    "π_13^7 = Z/2{ν₇²}"
  )
  print()

  print(
    "[6] n=8"
  )
  print()
  print(
    "Toda Proposition 4.4:"
  )
  print(
    "π_13^7 ⊕ π_14^15 ≅ π_14^8"
  )
  print(
    "π_14^15 = 0"
  )
  print("↓")
  print(
    "E: π_13^7 ≅ π_14^8"
  )
  print()
  print(
    "π_13^7 = Z/2{ν₇²}"
  )
  print(
    "E transports the concrete "
    "ν₇² generator to ν₈²"
  )
  print("↓")
  print(
    "π_14^8 = Z/2{ν₈²}"
  )
  print()

  print(
    "[7] n≥9"
  )
  print()
  print(
    "Toda (4.5):"
  )
  print(
    "E^(n-8): "
    "π_14^8 ≅ π_(n+6)^n"
  )
  print()
  print(
    "π_14^8 = Z/2{ν₈²}"
  )
  print(
    "E^(n-8) transports the concrete "
    "ν₈² generator to ν_n²"
  )
  print("↓")
  print(
    "π_(n+6)^n = Z/2{ν_n²}  "
    "(n ≥ 9)"
  )
  print()

  print(
    "[8] finite-dimensional six-stem aggregate"
  )
  print()
  print(
    "n=5,6,7,8"
  )
  print(
    "and"
  )
  print(
    "n≥9"
  )
  print("↓")
  print(
    "π_(n+6)^n = Z/2{ν_n²}  "
    "(n ≥ 5)"
  )
  print()

  print(
    "[9] Toda Proposition 5.11 "
    "finite-dimensional integration"
  )
  print()
  print(
    "π_8^2 = Z/2{η₂ν′η₆²}"
  )
  print(
    "π_9^3 = 0"
  )
  print(
    "π_10^4 = Z/8{ν₄²}"
  )
  print(
    "π_(n+6)^n = Z/2{ν_n²}, n≥5"
  )
  print("↓")
  print(
    "Toda Proposition 5.11 "
    "finite-dimensional aggregate"
  )


def print_phase73_provenance(
  representative,
):
  print_section(
    "Provenance / integration"
  )

  pi8_2_step = (
    representative[
      "pi8_2_step"
    ]
  )

  pi9_3_zero_step = (
    representative[
      "pi9_3_zero_step"
    ]
  )

  pi10_4_step = (
    representative[
      "pi10_4_step"
    ]
  )

  nu_squared_step = (
    representative[
      "nu_squared_step"
    ]
  )

  final_step = (
    representative[
      "final_step"
    ]
  )

  direct_branches = (
    pi8_2_step,
    pi9_3_zero_step,
    pi10_4_step,
    nu_squared_step,
  )

  all_direct_branches_are_inference = all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in direct_branches
  )

  statement = (
    final_step.conclusion
  )

  stable_group_field_absent = (
    not hasattr(
      statement,
      "stable_group",
    )
  )

  stable_nu_squared_field_absent = (
    not hasattr(
      statement,
      "stable_nu_squared",
    )
  )

  stable_branch_included = not (
    stable_group_field_absent
    and stable_nu_squared_field_absent
  )

  print(
    "π_8^2 result derived = "
    f"{pi8_2_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_9^3 zero derived = "
    f"{pi9_3_zero_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_10^4 result derived = "
    f"{pi10_4_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "ν_n² finite-dimensional aggregate "
    "derived = "
    f"{nu_squared_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "all four direct Proposition 5.11 "
    "branches are INFERENCE = "
    f"{all_direct_branches_are_inference}"
  )

  print(
    "final aggregate derived = "
    f"{final_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "final aggregate is GIVEN = "
    f"{final_step.rule == ProofRule.GIVEN}"
  )

  print(
    "final premise count = "
    f"{len(final_step.premises)}"
  )

  print(
    "stable branch included = "
    f"{stable_branch_included}"
  )

  print(
    "stable (G_6;2) remains deferred = "
    f"{not stable_branch_included}"
  )

  print(
    "staged one-shot aggregate = True"
  )


def print_phase73_literature(
  representative,
):
  print_section(
    "Literature statements used"
  )

  statements = (
    representative[
      "final_step"
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


def print_phase73_boundary():
  print_section(
    "Phase 73 representative probe boundary"
  )

  print(
    "Displayed:"
  )
  print(
    "  π_8^2 = Z/2{η₂ν′η₆²}"
  )
  print(
    "  π_9^3 = 0"
  )
  print(
    "  π_10^4 = Z/8{ν₄²}"
  )
  print(
    "  π_(n+6)^n = "
    "Z/2{ν_n²}, n>=5"
  )
  print(
    "  Toda (5.13) supporting relations"
  )
  print(
    "  finite-dimensional final aggregate"
  )
  print(
    "  representative proof-style display"
  )
  print(
    "  machine provenance status"
  )
  print(
    "  Proposition 5.11 literature metadata"
  )
  print()

  print(
    "Not added in Phase 73-8E3:"
  )
  print(
    "  new mathematical inference rules"
  )
  print(
    "  new theorem representation"
  )
  print(
    "  stable (G_6;2)=Z/2{ν²}"
  )
  print(
    "  stable homotopy-group model"
  )
  print(
    "  proof record documentation"
  )
  print(
    "  completion documentation"
  )
  print(
    "  automatic proof narrative generation"
  )
  print(
    "  generic suspension-of-composition "
    "normalizer"
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
    "Phase 73 capability demonstration"
  )

  representative = (
    build_phase73_representative_result()
  )

  print_phase73_results(
    representative
  )

  print_phase73_derivation_chain(
    representative
  )

  print_phase73_provenance(
    representative
  )

  print_phase73_literature(
    representative
  )

  print_phase73_boundary()


if __name__ == "__main__":
  main()


