from pathlib import Path
import sys

from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 60-9 の focused integration builder を
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

from test_phase60_lemma54_integration import (  # noqa: E402
  build_phase60_9_data,
)


def build_phase60_representative_result():
  return build_phase60_9_data()


def print_phase60_results(
  representative,
):
  print()
  print_separator()
  print(
    "Toda Lemma 5.4"
  )
  print_separator()
  print()

  print(
    "  ν₄ ∈ π_7^4"
  )
  print(
    "  H(ν₄) = ι₇"
  )
  print(
    "  2Eν₄ = E²ν′"
  )


def print_phase60_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / integration"
  )
  print_separator()
  print()

  membership_step = (
    representative[
      "membership_step"
    ]
  )

  hopf_step = (
    representative[
      "hopf_step"
    ]
  )

  double_step = (
    representative[
      "double_step"
    ]
  )

  integration_step = (
    representative[
      "integration_step"
    ]
  )

  print(
    "ν₄ membership derived =",
    (
      membership_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "H(ν₄)=ι₇ derived =",
    (
      hopf_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "2Eν₄=E²ν′ derived =",
    (
      double_step.rule
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
    "all final premises are INFERENCE =",
    all(
      premise.rule
      == ProofRule.INFERENCE
      for premise in (
        integration_step
        .premises
      )
    ),
  )

  print(
    "final aggregate uses exactly "
    "three Phase 60-8 conclusions =",
    (
      integration_step.premises
      == (
        membership_step,
        hopf_step,
        double_step,
      )
    ),
  )

  result = (
    representative[
      "result"
    ]
  )

  print(
    "Phase 60-9 round count =",
    result.round_count,
  )

  print(
    "fixed point =",
    (
      result.termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def phase60_literature_usage():
  return {
    "Proposition 1.3": (
      (
        "Phase 60-4: "
        "ν′ の定義 bracket から "
        "higher bracket への suspension transport"
      ),
    ),
    "Equation (1.15)": (
      (
        "Phase 60-4: "
        "E^(n-3)ν′ の bracket inclusion transport"
      ),
      (
        "Phase 60-5: "
        "positive-index bracket と "
        "t=0 bracket の比較"
      ),
    ),
    "Equation (3.2)": (
      (
        "Phase 60-5: "
        "E: π_(n+2)^n → π_(n+3)^(n+1) "
        "の surjectivity を使った t=0 bridge"
      ),
    ),
    "Theorem 3.6": (
      (
        "Phase 60-6: "
        "α=η₂, β=2ι₃, t=1 の specialization"
      ),
      (
        "Phase 60-6: "
        "α*∈π_7^4 と "
        "2Eα*∈-{η₅,2ι₆,η₆}_3 の導出"
      ),
    ),
    "Equation (4.7)": (
      (
        "Phase 60-3: "
        "Toda (5.4) bracket の "
        "indeterminacy calculation"
      ),
    ),
    "Proposition 5.3": (
      (
        "Phase 60-3: "
        "π_(n+2)^n=Z/2{η_n²} を使った "
        "indeterminacy reduction"
      ),
    ),
    "Equation (5.3)": (
      (
        "Phase 60-3: "
        "2ν′=η₃∘η₄∘η₅ の "
        "higher η-family transport"
      ),
      (
        "Phase 60-4: "
        "ν′∈{η₃,2ι₄,η₄}_1 を起点とする "
        "bracket inclusion"
      ),
    ),
    "Equation (5.4)": (
      (
        "Phase 60-5: "
        "{η_n,2ι_(n+1),η_(n+1)}_t "
        "= {±E^(n-3)ν′} の完成"
      ),
      (
        "Phase 60-6: "
        "n=5, t=3 specialization により "
        "{η₅,2ι₆,η₆}_3={±E²ν′}"
      ),
    ),
    "Equation (4.8)": (
      (
        "Phase 60-7: "
        "H(α*)=(2s+1)ι₇ の "
        "Hopf invariant / parity consequence"
      ),
    ),
    "Lemma 5.4 proof": (
      (
        "Phase 60-8: "
        "H[ι₄,ι₄]=(-1)^u2ι₇ と "
        "E[ι₄,ι₄]=0 を使った "
        "Whitehead correction"
      ),
      (
        "Phase 60-8: "
        "ν₄ の構成と "
        "H(ν₄)=ι₇, 2Eν₄=E²ν′ の導出"
      ),
    ),
  }


def print_phase60_literature_statements(
  representative,
):
  print()
  print_separator()
  print(
    "Literature statements used"
  )
  print_separator()
  print()

  literature_statements = (
    representative[
      "integration_step"
    ]
    .conclusion
    .literature_statements
  )

  usage_by_locator = (
    phase60_literature_usage()
  )

  for item in literature_statements:
    reference = item.reference

    print(
      f"[{reference.label}]"
    )

    if reference.locator:
      print(
        f"Locator: {reference.locator}"
      )

    if reference.author:
      print(
        f"Author: {reference.author}"
      )

    if reference.title:
      print(
        f"Source: {reference.title}"
      )

    if reference.year is not None:
      print(
        f"Year: {reference.year}"
      )

    usages = usage_by_locator.get(
      reference.locator,
      (),
    )

    if usages:
      print(
        "Used in:"
      )

      for usage in usages:
        print(
          f"  - {usage}"
        )

    print(
      "Statement:"
    )
    print(
      item.statement
    )
    print()


def print_phase60_boundary():
  print()
  print_separator()
  print(
    "Phase 60 completion boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  Toda (5.4) t≥1 "
    "up-to-sign bracket value"
  )
  print(
    "  Toda (5.4) t=0 bridge"
  )
  print(
    "  Theorem 3.6 Lemma 5.4 "
    "specialization"
  )
  print(
    "  2Eα* = ±E²ν′"
  )
  print(
    "  H(α*) = (2s+1)ι₇"
  )
  print(
    "  Whitehead correction branches"
  )
  print(
    "  ν₄ ∈ π_7^4"
  )
  print(
    "  H(ν₄) = ι₇"
  )
  print(
    "  2Eν₄ = E²ν′"
  )
  print(
    "  Toda Lemma 5.4 aggregate"
  )
  print(
    "  literature references with "
    "statement text"
  )
  print(
    "  end-to-end derived provenance"
  )

  print()
  print(
    "Still outside Phase 60:"
  )
  print(
    "  generic Toda-bracket coset algebra"
  )
  print(
    "  generic sign solver"
  )
  print(
    "  generic divisibility framework"
  )
  print(
    "  generic existential witness framework"
  )
  print(
    "  generic Whitehead correction algebra"
  )
  print(
    "  full Theorem 3.6 formalization"
  )
  print(
    "  full Toda (4.8) formalization"
  )
  print(
    "  theorem statement repository / search"
  )
  print(
    "  Toda Lemma 5.5"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 60 capability demonstration"
  )

  representative = (
    build_phase60_representative_result()
  )

  print_phase60_results(
    representative
  )

  print_phase60_provenance(
    representative
  )

  print_phase60_literature_statements(
    representative
  )

  print_phase60_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()


