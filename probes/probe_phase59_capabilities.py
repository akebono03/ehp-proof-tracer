from pathlib import Path
import sys

from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 59-8 の focused integration builder をそのまま representative fixture として再利用する。
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

from test_phase59_prop53_integration import (  # noqa: E402
  build_phase59_8_data,
)


def print_phase59_results(
  representative,
):
  print()
  print_separator()
  print(
    "Toda Proposition 5.3 "
    "finite-dimensional result"
  )
  print_separator()
  print()

  print(
    "  n = 2: "
    "π_4^2 = Z/2{η₂²}"
  )
  print(
    "  n = 3: "
    "π_5^3 = Z/2{η₃²}"
  )
  print(
    "  n = 4: "
    "π_6^4 = Z/2{η₄²}"
  )
  print(
    "  n ≥ 5: "
    "π_(n+2)^n = Z/2{η_n²}"
  )
  print()
  print(
    "  therefore: "
    "π_(n+2)^n = Z/2{η_n²} "
    "for n ≥ 2"
  )


def print_phase59_higher_bridge(
  representative,
):
  print()
  print_separator()
  print(
    "Higher eta-square bridge"
  )
  print_separator()
  print()

  print(
    "  E^(n-4)η₄² = η_n²"
  )
  print(
    "  bridge derived =",
    (
      representative[
        "bridge_step"
      ].rule
      == ProofRule.INFERENCE
    ),
  )
  print(
    "  higher group derived =",
    (
      representative[
        "higher_step"
      ].rule
      == ProofRule.INFERENCE
    ),
  )


def print_phase59_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / integration"
  )
  print_separator()
  print()

  integration_step = (
    representative[
      "integration_step"
    ]
  )

  print(
    "pi_4^2 branch derived =",
    (
      representative[
        "pi4_2_step"
      ].rule
      == ProofRule.INFERENCE
    ),
  )
  print(
    "pi_5^3 branch derived =",
    (
      representative[
        "pi5_3_step"
      ].rule
      == ProofRule.INFERENCE
    ),
  )
  print(
    "pi_6^4 branch derived =",
    (
      representative[
        "pi6_4_step"
      ].rule
      == ProofRule.INFERENCE
    ),
  )
  print(
    "higher transport derived =",
    (
      representative[
        "higher_transport_step"
      ].rule
      == ProofRule.INFERENCE
    ),
  )
  print(
    "higher eta-square group derived =",
    (
      representative[
        "higher_step"
      ].rule
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
    "final derived branch premises =",
    all(
      premise.rule
      == ProofRule.INFERENCE
      for premise in integration_step.premises[:4]
    ),
  )

  result = representative[
    "result"
  ]

  print(
    "Phase 59-8 round count =",
    result.round_count,
  )
  print(
    "fixed point =",
    (
      result.termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def print_phase59_boundary():
  print()
  print_separator()
  print(
    "Phase 59 completion boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  π_(n+2)^n = Z/2{η_n²}, n ≥ 2"
  )
  print(
    "  η_n² represented by Composition"
  )
  print(
    "  n=2 / n=3 / n=4 / n≥5 branches"
  )
  print(
    "  higher E^(n-4)η₄² = η_n² bridge"
  )
  print(
    "  finite-dimensional Proposition 5.3 aggregate"
  )
  print(
    "  end-to-end derived provenance"
  )

  print()
  print(
    "Still outside Phase 59:"
  )
  print(
    "  stable (G_2;2)=Z/2{η²}"
  )
  print(
    "  stable homotopy-group model"
  )
  print(
    "  generic EtaSquare representation"
  )
  print(
    "  generic cyclic-generator transport"
  )
  print(
    "  generic suspension/composition normalization"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 59 capability demonstration"
  )

  representative = (
    build_phase59_8_data()
  )

  print_phase59_results(
    representative
  )
  print_phase59_higher_bridge(
    representative
  )
  print_phase59_provenance(
    representative
  )
  print_phase59_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()
