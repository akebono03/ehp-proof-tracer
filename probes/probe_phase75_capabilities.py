from pathlib import Path
import sys

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
)
from proof import (
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 75-9 の finite-dimensional aggregate builder を
# representative fixture としてそのまま再利用する。
#
# theorem logic や group calculation を
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

from test_phase75_prop515_integration import (  # noqa: E402
  build_phase75_9_data,
)


def build_phase75_representative_result():
  return build_phase75_9_data()


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


def print_phase75_results(
  representative,
):
  aggregate_step = (
    representative[
      "aggregate_step"
    ]
  )

  print_section(
    "Toda Proposition 5.15 "
    "finite-dimensional result"
  )

  print(
    "π_9^2 = 0"
  )
  print(
    "π_10^3 = 0"
  )
  print(
    "π_11^4 = 0"
  )
  print(
    "π_12^5 = Z/2{σ'''}"
  )
  print(
    "π_13^6 = Z/4{σ''}"
  )
  print(
    "π_14^7 = Z/8{σ'}"
  )
  print(
    "π_15^8 = "
    "Z{σ₈} ⊕ Z/8{Eσ'}"
  )
  print(
    "π_(n+7)^n = "
    "Z/16{σ_n}  (n >= 9)"
  )
  print()

  print(
    "statement type = "
    f"{type(aggregate_step.conclusion).__name__}"
  )

  print(
    "derived = "
    f"{aggregate_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "is GIVEN = "
    f"{aggregate_step.rule == ProofRule.GIVEN}"
  )


def print_phase75_derivation_chain(
  representative,
):
  print_section(
    "Proof-style derivation"
  )

  print(
    "[1] Low zero branches"
  )
  print()
  print(
    "Phase 73:"
  )
  print(
    "π_9^3 = 0"
  )
  print(
    "together with Toda (5.2)"
  )
  print("↓")
  print(
    "π_9^2 = 0"
  )
  print()
  print(
    "EHP exactness and the previous "
    "zero branches"
  )
  print("↓")
  print(
    "π_10^3 = 0"
  )
  print("↓")
  print(
    "π_11^4 = 0"
  )
  print()

  print(
    "[2] σ''' and π_12^5"
  )
  print()
  print(
    "Toda Lemma 5.13 selects σ''' "
    "in π_12^5"
  )
  print()
  print(
    "H:π_12^5 -> π_12^9 "
    "identifies the order-two image"
  )
  print("↓")
  print(
    "π_12^5 = Z/2{σ'''}"
  )
  print()

  print(
    "[3] σ'' and σ'"
  )
  print()
  print(
    "Toda (5.14) first short exact sequence"
  )
  print(
    "0 -> π_12^5 -> π_13^6 "
    "-> π_13^11 -> 0"
  )
  print(
    "and"
  )
  print(
    "2σ'' = Eσ'''"
  )
  print("↓")
  print(
    "π_13^6 = Z/4{σ''}"
  )
  print()
  print(
    "Toda (5.14) second short exact sequence"
  )
  print(
    "0 -> π_13^6 -> π_14^7 "
    "-> π_14^13 -> 0"
  )
  print(
    "and"
  )
  print(
    "2σ' = Eσ''"
  )
  print("↓")
  print(
    "π_14^7 = Z/8{σ'}"
  )
  print()

  print(
    "[4] σ₈ and the sigma family"
  )
  print()
  print(
    "Toda Lemma 5.14 constructs σ₈ "
    "with"
  )
  print(
    "H(σ₈) = ι₁₅"
  )
  print(
    "and"
  )
  print(
    "2Eσ₈ = E²σ'"
  )
  print()
  print(
    "define σ_n = E^(n-8)σ₈ "
    "for n >= 8"
  )
  print()

  print(
    "[5] n=8 critical branch"
  )
  print()
  print(
    "Toda Proposition 4.4 / (5.15):"
  )
  print(
    "π_14^7 ⊕ π_15^15 "
    "≅ π_15^8"
  )
  print(
    "(α,β) ↦ Eα + σ₈∘β"
  )
  print()
  print(
    "π_14^7 = Z/8{σ'}"
  )
  print(
    "π_15^15 = Z{ι₁₅}"
  )
  print("↓")
  print(
    "σ' ↦ Eσ'"
  )
  print(
    "ι₁₅ ↦ σ₈"
  )
  print("↓")
  print(
    "π_15^8 = "
    "Z{σ₈} ⊕ Z/8{Eσ'}"
  )
  print()

  print(
    "[6] n>=9 branch"
  )
  print()
  print(
    "π_16^9 = Z/16{σ₉}"
  )
  print()
  print(
    "Toda (4.5) stable-range transport"
  )
  print("↓")
  print(
    "π_(n+7)^n = Z/16{σ_n}"
  )
  print(
    "(n >= 9)"
  )
  print()

  print(
    "[7] Proposition 5.15 integration"
  )
  print()
  print(
    "all finite-dimensional branches "
    "are independently derived"
  )
  print("↓")
  print(
    "TodaProp515FiniteDimensionalStatement"
  )


def print_phase75_provenance(
  representative,
):
  print_section(
    "Provenance / integration"
  )

  direct_math_steps = (
    representative[
      "pi9_2_step"
    ],
    representative[
      "pi10_3_step"
    ],
    representative[
      "pi11_4_step"
    ],
    representative[
      "pi12_5_step"
    ],
    representative[
      "pi13_6_step"
    ],
    representative[
      "pi14_7_step"
    ],
    representative[
      "pi15_8_step"
    ],
    representative[
      "higher_step"
    ],
  )

  aggregate_step = (
    representative[
      "aggregate_step"
    ]
  )

  higher_range_step = (
    representative[
      "higher_range_step"
    ]
  )

  exact_direct_premises = (
    aggregate_step.premises
    == representative[
      "premise_steps"
    ]
  )

  print(
    "all eight mathematical branches "
    "are INFERENCE = "
    f"{all(step.rule == ProofRule.INFERENCE for step in direct_math_steps)}"
  )

  print(
    "n>=9 range remains GIVEN = "
    f"{higher_range_step.rule == ProofRule.GIVEN}"
  )

  print(
    "final aggregate derived = "
    f"{aggregate_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "final aggregate is GIVEN = "
    f"{aggregate_step.rule == ProofRule.GIVEN}"
  )

  print(
    "exact direct aggregate premises = "
    f"{exact_direct_premises}"
  )

  print()

  print(
    "π_15^8 branch derived = "
    f"{representative['pi15_8_step'].rule == ProofRule.INFERENCE}"
  )

  print(
    "n>=9 Z/16 branch derived = "
    f"{representative['higher_step'].rule == ProofRule.INFERENCE}"
  )


def print_phase75_representation_boundary(
  representative,
):
  print_section(
    "Representation / completion boundary"
  )

  statement = (
    representative[
      "aggregate_step"
    ].conclusion
  )

  pi15_8_relation = (
    statement
    .pi15_8_group_relation
  )

  direct_sum = (
    pi15_8_relation
    .rhs
  )

  free_first = (
    isinstance(
      direct_sum,
      DirectSumGroup,
    )
    and len(
      direct_sum.summands
    )
    == 2
    and isinstance(
      direct_sum.summands[
        0
      ],
      FreeCyclicGroup,
    )
  )

  torsion_second = (
    isinstance(
      direct_sum,
      DirectSumGroup,
    )
    and len(
      direct_sum.summands
    )
    == 2
    and isinstance(
      direct_sum.summands[
        1
      ],
      FiniteCyclicGroup,
    )
    and direct_sum.summands[
      1
    ].order
    == 8
  )

  print(
    "π_15^8 uses DirectSumGroup = "
    f"{isinstance(direct_sum, DirectSumGroup)}"
  )

  print(
    "free σ₈ summand is first = "
    f"{free_first}"
  )

  print(
    "order-eight Eσ' summand is second = "
    f"{torsion_second}"
  )

  print(
    "stable group field present = "
    f"{hasattr(statement, 'stable_group_relation')}"
  )

  print(
    "stable (G_7;2) included = "
    f"{hasattr(statement, 'stable_group_relation')}"
  )

  print()

  print(
    "Phase 75 finite-dimensional "
    "Proposition 5.15 is complete."
  )

  print(
    "Toda (5.16) is not part of "
    "this Phase."
  )


def print_phase75_literature(
  representative,
):
  print_section(
    "Literature statements used"
  )

  literature = (
    representative[
      "aggregate_step"
    ].conclusion
    .literature_statements
  )

  for item in literature:
    reference = (
      item.reference
    )

    print(
      "Label: "
      f"{reference.label}"
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
      "Statement: "
      f"{item.statement}"
    )
    print()


def print_phase75_boundary():
  print_section(
    "Phase 75 representative probe boundary"
  )

  print(
    "Displayed:"
  )
  print(
    "  Proposition 5.15 "
    "finite-dimensional branches"
  )
  print(
    "  low zero groups"
  )
  print(
    "  σ''' / σ'' / σ' branches"
  )
  print(
    "  σ₈ mixed n=8 decomposition"
  )
  print(
    "  n>=9 Z/16 transport"
  )
  print(
    "  aggregate provenance"
  )
  print(
    "  literature metadata"
  )
  print()

  print(
    "Not added in Phase 75-10:"
  )
  print(
    "  new mathematical inference rules"
  )
  print(
    "  new theorem semantics"
  )
  print(
    "  stable (G_7;2) result"
  )
  print(
    "  Toda (5.16)"
  )
  print(
    "  generic direct-sum commutativity"
  )
  print(
    "  generic cyclic transport framework"
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
    "Phase 75 capability demonstration"
  )

  representative = (
    build_phase75_representative_result()
  )

  print_phase75_results(
    representative
  )

  print_phase75_derivation_chain(
    representative
  )

  print_phase75_provenance(
    representative
  )

  print_phase75_representation_boundary(
    representative
  )

  print_phase75_literature(
    representative
  )

  print_phase75_boundary()


if __name__ == "__main__":
  main()
