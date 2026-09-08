from pathlib import Path
import sys

from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)
from probes.probe_phase61_capabilities import (
  print_literature_item,
)


# Phase 63-6 の focused integration builder を
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

from test_phase63_toda56_integration import (  # noqa: E402
  build_phase63_6_data,
)


def build_phase63_representative_result():
  return build_phase63_6_data()


def print_phase63_results(
  representative,
):
  print()
  print_separator()
  print(
    "Toda (5.6) nu_4 "
    "decomposition isomorphism"
  )
  print_separator()
  print()

  print(
    "  Φ:"
  )
  print(
    "  π_(i-1)^3 ⊕ π_i^7"
  )
  print(
    "  →"
  )
  print(
    "  π_i^4"
  )
  print()
  print(
    "  Φ(α,β)"
  )
  print(
    "  = Eα + ν₄∘β"
  )
  print()
  print(
    "  Φ is an isomorphism."
  )


def print_phase63_derivation_chain(
  representative,
):
  print()
  print_separator()
  print(
    "Proof-style derivation"
  )
  print_separator()
  print()

  print(
    "Phase 60: "
    "Toda Lemma 5.4"
  )
  print()
  print(
    "  ν₄ ∈ π_7^4"
  )
  print(
    "  H(ν₄) = ι₇"
  )
  print()
  print(
    "  ↓"
  )
  print()

  print(
    "Phase 63-2: "
    "nu_4 specialization premises"
  )
  print()
  print(
    "  n = 4"
  )
  print(
    "  α = ν₄"
  )
  print(
    "  ν₄ ∈ π_7^4"
  )
  print(
    "  H(ν₄) = ι₇"
  )
  print()
  print(
    "  ↓ Toda Proposition 4.4"
  )
  print()

  print(
    "Phase 63-3: "
    "Proposition 4.4 decomposition "
    "specialization"
  )
  print()
  print(
    "  Φ:"
  )
  print(
    "  π_(i-1)^3 ⊕ π_i^7"
  )
  print(
    "  →"
  )
  print(
    "  π_i^4"
  )
  print()
  print(
    "  Φ(α,β)"
  )
  print(
    "  = Eα + ν₄∘β"
  )
  print()
  print(
    "  Φ is an isomorphism."
  )
  print()
  print(
    "  ↓"
  )
  print()

  print(
    "Phase 63-4: "
    "Toda (5.6) semantics"
  )
  print()
  print(
    "  π_(i-1)^3 ⊕ π_i^7"
  )
  print(
    "  ≅"
  )
  print(
    "  π_i^4"
  )
  print()
  print(
    "  (α,β)"
  )
  print(
    "  ↦"
  )
  print(
    "  Eα + ν₄∘β"
  )
  print()
  print(
    "  ↓"
  )
  print()

  print(
    "Phase 63-6: "
    "Toda (5.6) literature-aware "
    "aggregate"
  )
  print()
  print(
    "  Toda (5.6) semantics"
  )
  print(
    "  +"
  )
  print(
    "  Toda Lemma 5.4 provenance"
  )
  print(
    "  +"
  )
  print(
    "  Equation (5.6) literature"
  )
  print()
  print(
    "  ↓"
  )
  print()
  print(
    "  Toda (5.6) final aggregate"
  )


def print_phase63_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / integration"
  )
  print_separator()
  print()

  phase63_4 = (
    representative[
      "phase63_4"
    ]
  )

  phase63_3 = (
    representative[
      "phase63_3"
    ]
  )

  phase63_2 = (
    representative[
      "phase63_2"
    ]
  )

  phase60_9 = (
    phase63_2[
      "phase60_9"
    ]
  )

  integration_step = (
    representative[
      "integration_step"
    ]
  )

  decomposition_step = (
    representative[
      "decomposition_step"
    ]
  )

  lemma54_step = (
    representative[
      "lemma54_step"
    ]
  )

  prop44_step = (
    phase63_4[
      "prop44_isomorphism_step"
    ]
  )

  specialization_step = (
    phase63_3[
      "specialization_step"
    ]
  )

  decomposition_map_step = (
    phase63_3[
      "decomposition_map_step"
    ]
  )

  membership_step = (
    phase60_9[
      "membership_step"
    ]
  )

  hopf_step = (
    phase60_9[
      "hopf_step"
    ]
  )

  double_step = (
    phase60_9[
      "double_step"
    ]
  )

  print(
    "nu_4 membership derived =",
    (
      membership_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "H(nu_4)=iota_7 derived =",
    (
      hopf_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "2E nu_4=E^2 nu-prime derived =",
    (
      double_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "Lemma 5.4 aggregate derived =",
    (
      lemma54_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "nu_4 specialization derived =",
    (
      specialization_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "decomposition map is GIVEN =",
    (
      decomposition_map_step.rule
      == ProofRule.GIVEN
    ),
  )

  print(
    "Prop.4.4 specialization "
    "isomorphism derived =",
    (
      prop44_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "Toda (5.6) semantics derived =",
    (
      decomposition_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "final aggregate derived =",
    (
      integration_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "final aggregate is GIVEN =",
    (
      integration_step.rule
      == ProofRule.GIVEN
    ),
  )

  print(
    "theorem dependencies are "
    "INFERENCE =",
    all(
      step.rule
      == ProofRule.INFERENCE
      for step in (
        membership_step,
        hopf_step,
        double_step,
        lemma54_step,
        specialization_step,
        prop44_step,
        decomposition_step,
        integration_step,
      )
    ),
  )

  print(
    "structural decomposition map "
    "remains GIVEN =",
    (
      decomposition_map_step.rule
      == ProofRule.GIVEN
    ),
  )

  print(
    "final aggregate uses exactly "
    "two Phase 63-6 premises =",
    (
      integration_step.premises
      == (
        decomposition_step,
        lemma54_step,
      )
    ),
  )

  result = (
    representative[
      "result"
    ]
  )

  print(
    "Phase 63-6 round count =",
    result.round_count,
  )

  print(
    "fixed point =",
    (
      result.termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def phase63_literature_usage():
  return {
    "Equation (5.6)": (
      (
        "Phase 63-3: "
        "n=4, alpha=nu_4 "
        "Proposition 4.4 specialization"
      ),
      (
        "Phase 63-4: "
        "Toda (5.6) "
        "map / isomorphism semantics"
      ),
      (
        "Phase 63-6: "
        "Toda (5.6) "
        "literature-aware aggregate"
      ),
    ),
  }


def print_phase63_literature_statements(
  representative,
):
  print()
  print_separator()
  print(
    "Literature statements used"
  )
  print_separator()
  print()

  statement = (
    representative[
      "integration_step"
    ]
    .conclusion
  )

  usage_by_locator = (
    phase63_literature_usage()
  )

  print(
    "Phase 63 direct literature:"
  )
  print()

  for item in (
    statement
    .literature_statements
  ):
    print_literature_item(
      item,
      usage_by_locator,
    )

  print(
    "Inherited through "
    "Toda Lemma 5.4:"
  )
  print()

  for item in (
    statement
    .lemma54_statement
    .literature_statements
  ):
    print_literature_item(
      item,
      {},
    )


def print_phase63_boundary():
  print()
  print_separator()
  print(
    "Phase 63 completion boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  Phase 60 nu_4 provenance reuse"
  )
  print(
    "  n=4, alpha=nu_4 "
    "specialization bridge"
  )
  print(
    "  nu_4 in pi_7^4 "
    "Toda-primary membership bridge"
  )
  print(
    "  H(nu_4)=iota_7 "
    "specialization premise"
  )
  print(
    "  Proposition 4.4 concrete "
    "decomposition specialization"
  )
  print(
    "  pi_(i-1)^3 direct sum pi_i^7"
  )
  print(
    "  to pi_i^4"
  )
  print(
    "  (alpha,beta) "
    "maps to E alpha + nu_4 composed "
    "with beta"
  )
  print(
    "  Toda (5.6) "
    "isomorphism semantics"
  )
  print(
    "  Toda (5.6) "
    "literature-aware aggregate"
  )
  print(
    "  Phase 60 inherited literature"
  )
  print(
    "  applicability / acyclic "
    "provenance regression"
  )
  print(
    "  proof-style derivation display"
  )

  print()
  print(
    "Still outside Phase 63:"
  )
  print(
    "  generic Proposition 4.4 "
    "specialization framework"
  )
  print(
    "  generic scalar normalization"
  )
  print(
    "  generic membership normalization"
  )
  print(
    "  generic direct-sum simplification"
  )
  print(
    "  automatic proof narrative "
    "generation"
  )
  print(
    "  later Toda consequences "
    "after Equation (5.6)"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 63 capability demonstration"
  )

  representative = (
    build_phase63_representative_result()
  )

  print_phase63_results(
    representative
  )

  print_phase63_derivation_chain(
    representative
  )

  print_phase63_provenance(
    representative
  )

  print_phase63_literature_statements(
    representative
  )

  print_phase63_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()


