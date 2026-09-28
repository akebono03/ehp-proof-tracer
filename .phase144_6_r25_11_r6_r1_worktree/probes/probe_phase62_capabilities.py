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


# Phase 62-6 の focused integration builder を
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

from test_phase62_toda55_integration import (  # noqa: E402
  build_phase62_6_data,
)


def build_phase62_representative_result():
  return build_phase62_6_data()


def print_phase62_results(
  representative,
):
  print()
  print_separator()
  print(
    "Toda (5.5) finite-dimensional "
    "nu-family calculation"
  )
  print_separator()
  print()

  print(
    "Definition:"
  )
  print()
  print(
    "  ν_n := E^(n-4)ν₄"
  )
  print(
    "  n ≥ 4"
  )
  print()

  print(
    "For n ≥ 5:"
  )
  print()
  print(
    "  2ν_n = E^(n-3)ν′"
  )
  print(
    "  4ν_n = η_n³"
  )
  print()
  print(
    "  η_n³"
  )
  print(
    "  = η_n∘η_(n+1)∘η_(n+2)"
  )


def print_phase62_derivation_chain(
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
    "Phase 62-2: "
    "nu-family definition"
  )
  print()
  print(
    "  ν_n := E^(n-4)ν₄"
  )
  print(
    "  n ≥ 4"
  )
  print()

  print(
    "Phase 62-3: "
    "double-value suspension transport"
  )
  print()
  print(
    "  Toda Lemma 5.4:"
  )
  print(
    "  2Eν₄ = E²ν′"
  )
  print()
  print(
    "  ν_n = E^(n-4)ν₄"
  )
  print(
    "  n ≥ 5"
  )
  print()
  print(
    "  ↓ suspend by E^(n-5)"
  )
  print()
  print(
    "  2ν_n = E^(n-3)ν′"
  )
  print()

  print(
    "Phase 62-4: "
    "eta-cube bridge"
  )
  print()
  print(
    "  2ν_n = E^(n-3)ν′"
  )
  print()
  print(
    "  ↓ multiply by 2"
  )
  print()
  print(
    "  4ν_n = 2E^(n-3)ν′"
  )
  print()

  print(
    "  Phase 58:"
  )
  print(
    "  2ν′ = η₃∘η₄∘η₅"
  )
  print()
  print(
    "  ↓ Phase 60 triple-eta transport"
  )
  print()
  print(
    "  2E^(n-3)ν′"
  )
  print(
    "  = η_n∘η_(n+1)∘η_(n+2)"
  )
  print()
  print(
    "  ↓"
  )
  print()
  print(
    "  4ν_n"
  )
  print(
    "  = η_n∘η_(n+1)∘η_(n+2)"
  )
  print(
    "  = η_n³"
  )
  print()

  print(
    "Phase 62-6: "
    "Toda (5.5) finite-dimensional integration"
  )
  print()
  print(
    "  Lemma 5.4 ν₄ provenance"
  )
  print(
    "  +"
  )
  print(
    "  ν-family definition"
  )
  print(
    "  +"
  )
  print(
    "  n ≥ 5"
  )
  print(
    "  +"
  )
  print(
    "  2ν_n = E^(n-3)ν′"
  )
  print(
    "  +"
  )
  print(
    "  4ν_n = η_n³"
  )
  print()
  print(
    "  ↓"
  )
  print()
  print(
    "  Toda (5.5) "
    "finite-dimensional aggregate"
  )


def print_phase62_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / integration"
  )
  print_separator()
  print()

  lemma54_step = (
    representative[
      "lemma54_step"
    ]
  )

  definition_step = (
    representative[
      "definition_step"
    ]
  )

  n_range_step = (
    representative[
      "n_range_step"
    ]
  )

  double_nu_step = (
    representative[
      "double_nu_step"
    ]
  )

  quadruple_nu_step = (
    representative[
      "quadruple_nu_step"
    ]
  )

  integration_step = (
    representative[
      "integration_step"
    ]
  )

  phase62_4 = (
    representative[
      "phase62_4"
    ]
  )

  triple_eta_step = (
    phase62_4[
      "triple_eta_step"
    ]
  )

  print(
    "Lemma 5.4 aggregate derived =",
    (
      lemma54_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "nu-family definition is GIVEN =",
    (
      definition_step.rule
      == ProofRule.GIVEN
    ),
  )

  print(
    "n>=5 applicability is GIVEN =",
    (
      n_range_step.rule
      == ProofRule.GIVEN
    ),
  )

  print(
    "2ν_n=E^(n-3)ν′ derived =",
    (
      double_nu_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "Phase 60 triple-eta transport derived =",
    (
      triple_eta_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "4ν_n=η_n³ derived =",
    (
      quadruple_nu_step.rule
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
    "theorem dependencies are INFERENCE =",
    all(
      step.rule
      == ProofRule.INFERENCE
      for step in (
        lemma54_step,
        double_nu_step,
        triple_eta_step,
        quadruple_nu_step,
      )
    ),
  )

  print(
    "definition / applicability "
    "remain GIVEN =",
    all(
      step.rule
      == ProofRule.GIVEN
      for step in (
        definition_step,
        n_range_step,
      )
    ),
  )

  print(
    "final aggregate uses exactly "
    "five Phase 62-6 premises =",
    (
      integration_step.premises
      == (
        lemma54_step,
        definition_step,
        n_range_step,
        double_nu_step,
        quadruple_nu_step,
      )
    ),
  )

  result = (
    representative[
      "result"
    ]
  )

  print(
    "Phase 62-6 round count =",
    result.round_count,
  )

  print(
    "fixed point =",
    (
      result.termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def phase62_literature_usage():
  return {
    "Equation (5.5)": (
      (
        "Phase 62-2: "
        "ν_n:=E^(n-4)ν₄ definition"
      ),
      (
        "Phase 62-3: "
        "2ν_n=E^(n-3)ν′ "
        "suspension transport"
      ),
      (
        "Phase 62-4: "
        "4ν_n=η_n³ bridge"
      ),
      (
        "Phase 62-6: "
        "Toda (5.5) "
        "finite-dimensional aggregate"
      ),
    ),
  }


def print_phase62_literature_statements(
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
    phase62_literature_usage()
  )

  print(
    "Phase 62 direct literature:"
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


def print_phase62_boundary():
  print()
  print_separator()
  print(
    "Phase 62 completion boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  ν_n := E^(n-4)ν₄"
  )
  print(
    "  ν-family definition for n ≥ 4"
  )
  print(
    "  finite-dimensional "
    "Toda (5.5) applicability n ≥ 5"
  )
  print(
    "  2ν_n = E^(n-3)ν′"
  )
  print(
    "  4ν_n = η_n³"
  )
  print(
    "  η_n³ "
    "= η_n∘η_(n+1)∘η_(n+2)"
  )
  print(
    "  Phase 60 Lemma 5.4 reuse"
  )
  print(
    "  Phase 58 / Phase 60 "
    "triple-eta provenance reuse"
  )
  print(
    "  Toda (5.5) "
    "finite-dimensional aggregate"
  )
  print(
    "  literature references with "
    "statement text"
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
    "Still outside Phase 62:"
  )
  print(
    "  stable ν := E^∞ν₄"
  )
  print(
    "  stable 4ν = η³"
  )
  print(
    "  stable homotopy-group model"
  )
  print(
    "  generic ν-family framework"
  )
  print(
    "  generic suspension exponent algebra"
  )
  print(
    "  generic η-cube class"
  )
  print(
    "  automatic proof narrative generation"
  )
  print(
    "  Toda (5.6) "
    "ν₄ decomposition isomorphism"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 62 capability demonstration"
  )

  representative = (
    build_phase62_representative_result()
  )

  print_phase62_results(
    representative
  )

  print_phase62_derivation_chain(
    representative
  )

  print_phase62_provenance(
    representative
  )

  print_phase62_literature_statements(
    representative
  )

  print_phase62_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()


