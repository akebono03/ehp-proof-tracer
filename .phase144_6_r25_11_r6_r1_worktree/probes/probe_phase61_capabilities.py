from pathlib import Path
import sys

from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 61-6 の focused integration builder を
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

from test_phase61_lemma55_integration import (  # noqa: E402
  build_phase61_6_data,
)


def build_phase61_representative_result():
  return build_phase61_6_data()


def print_phase61_results(
  representative,
):
  print()
  print_separator()
  print(
    "Toda Lemma 5.5"
  )
  print_separator()
  print()

  print(
    "Hypotheses:"
  )
  print(
    "  β ∈ π_(t+2)(S^m)"
  )
  print(
    "  β∘η_(t+2) = 0"
  )
  print(
    "  t > 0"
  )
  print()

  print(
    "Result:"
  )
  print()
  print(
    "  {η_(m+2), E³β, η_(t+5)}_3"
  )
  print(
    "  contains"
  )
  print(
    "  ±(E²β∘E^tν₄)"
  )


def print_phase61_derivation_chain():
  print()
  print_separator()
  print(
    "Proof-style derivation"
  )
  print_separator()
  print()

  print(
    "Phase 61-3: "
    "alpha-star bracket inclusion"
  )
  print()

  print(
    "  β ∈ π_(t+2)(S^m)"
  )
  print(
    "  β∘η_(t+2) = 0"
  )
  print(
    "  t > 0"
  )
  print()
  print(
    "  ↓ Toda Lemma 5.5 proof"
  )
  print()
  print(
    "  {η_(m+2), E³β, η_(t+5)}_3"
  )
  print(
    "  contains"
  )
  print(
    "  ±(E²β∘E^tα*)"
  )
  print()

  print(
    "Phase 61-4: "
    "nu_4 suspension correction"
  )
  print()

  print(
    "  From Toda Lemma 5.4,"
  )
  print()
  print(
    "  ν₄"
  )
  print(
    "  = α* "
    "- (-1)^u s[ι₄,ι₄]"
  )
  print(
    "  or"
  )
  print(
    "  ν₄"
  )
  print(
    "  = -α* "
    "+ (-1)^u(s+1)[ι₄,ι₄]"
  )
  print()
  print(
    "  E[ι₄,ι₄] = 0"
  )
  print(
    "  and t > 0"
  )
  print()
  print(
    "  ↓"
  )
  print()
  print(
    "  E^tν₄ = ±E^tα*"
  )
  print()

  print(
    "Phase 61-5: "
    "alpha-star to nu_4 composition bridge"
  )
  print()

  print(
    "  bracket contains"
  )
  print(
    "  ±(E²β∘E^tα*)"
  )
  print()
  print(
    "  E^tν₄ = ±E^tα*"
  )
  print()
  print(
    "  ↓"
  )
  print()
  print(
    "  {η_(m+2), E³β, η_(t+5)}_3"
  )
  print(
    "  contains"
  )
  print(
    "  ±(E²β∘E^tν₄)"
  )
  print()

  print(
    "Phase 61-6: "
    "Toda Lemma 5.5 integration"
  )
  print()

  print(
    "  Lemma 5.4 ν₄ provenance"
  )
  print(
    "  +"
  )
  print(
    "  Lemma 5.5 hypotheses"
  )
  print(
    "  +"
  )
  print(
    "  final bracket inclusion"
  )
  print()
  print(
    "  ↓"
  )
  print()
  print(
    "  Toda Lemma 5.5 aggregate"
  )


def print_phase61_provenance(
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

  beta_membership_step = (
    representative[
      "beta_membership_step"
    ]
  )

  beta_eta_zero_step = (
    representative[
      "beta_eta_zero_step"
    ]
  )

  t_range_step = (
    representative[
      "t_range_step"
    ]
  )

  final_inclusion_step = (
    representative[
      "final_inclusion_step"
    ]
  )

  integration_step = (
    representative[
      "integration_step"
    ]
  )

  phase61_5 = (
    representative[
      "phase61_5"
    ]
  )

  alpha_star_inclusion_step = (
    phase61_5[
      "alpha_star_inclusion_step"
    ]
  )

  suspension_step = (
    phase61_5[
      "suspension_step"
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
    "alpha-star bracket inclusion derived =",
    (
      alpha_star_inclusion_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "E^tν₄=±E^tα* derived =",
    (
      suspension_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "final ν₄ bracket inclusion derived =",
    (
      final_inclusion_step.rule
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
        final_inclusion_step,
      )
    ),
  )

  print(
    "Lemma 5.5 hypotheses remain GIVEN =",
    all(
      step.rule
      == ProofRule.GIVEN
      for step in (
        beta_membership_step,
        beta_eta_zero_step,
        t_range_step,
      )
    ),
  )

  print(
    "final aggregate uses exactly "
    "five Phase 61-6 premises =",
    (
      integration_step.premises
      == (
        lemma54_step,
        beta_membership_step,
        beta_eta_zero_step,
        t_range_step,
        final_inclusion_step,
      )
    ),
  )

  result = (
    representative[
      "result"
    ]
  )

  print(
    "Phase 61-6 round count =",
    result.round_count,
  )

  print(
    "fixed point =",
    (
      result.termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def phase61_literature_usage():
  return {
    "Lemma 5.5": (
      (
        "Phase 61-6: "
        "Toda Lemma 5.5 final aggregate"
      ),
    ),
    "Lemma 5.5 proof": (
      (
        "Phase 61-3: "
        "±(E²β∘E^tα*) の "
        "bracket inclusion consequence"
      ),
      (
        "Phase 61-4: "
        "E[ι₄,ι₄]=0 を使った "
        "E^tν₄=±E^tα* bridge"
      ),
      (
        "Phase 61-5: "
        "α* representative から "
        "ν₄ representative への transport"
      ),
    ),
  }


def print_literature_item(
  item,
  usage_by_locator,
):
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


def print_phase61_literature_statements(
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
    phase61_literature_usage()
  )

  print(
    "Phase 61 direct literature:"
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


def print_phase61_boundary():
  print()
  print_separator()
  print(
    "Phase 61 completion boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  Toda Lemma 5.5 "
    "minimum contains-up-to-sign semantics"
  )
  print(
    "  β ∈ π_(t+2)(S^m) applicability"
  )
  print(
    "  β∘η_(t+2)=0 applicability"
  )
  print(
    "  t>0 applicability"
  )
  print(
    "  alpha-star bracket inclusion"
  )
  print(
    "  E^tν₄ = ±E^tα*"
  )
  print(
    "  alpha-star to ν₄ "
    "composition bridge"
  )
  print(
    "  {η_(m+2), E³β, η_(t+5)}_3"
  )
  print(
    "  contains ±(E²β∘E^tν₄)"
  )
  print(
    "  Toda Lemma 5.5 aggregate"
  )
  print(
    "  literature references with "
    "statement text"
  )
  print(
    "  Phase 60 → Phase 61 "
    "derived provenance"
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
    "Still outside Phase 61:"
  )
  print(
    "  generic Toda-bracket "
    "containment algebra"
  )
  print(
    "  generic up-to-sign transitivity"
  )
  print(
    "  generic sign solver"
  )
  print(
    "  generic Whitehead correction algebra"
  )
  print(
    "  full Theorem 3.6 formalization"
  )
  print(
    "  automatic proof narrative generation"
  )
  print(
    "  Toda (5.5) ν-family calculation"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 61 capability demonstration"
  )

  representative = (
    build_phase61_representative_result()
  )

  print_phase61_results(
    representative
  )

  print_phase61_derivation_chain()

  print_phase61_provenance(
    representative
  )

  print_phase61_literature_statements(
    representative
  )

  print_phase61_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()



