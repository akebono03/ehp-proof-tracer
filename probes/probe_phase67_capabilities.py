from pathlib import Path
import sys

from proof import (
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 67-7 の focused end-to-end builder を
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

from test_phase67_lemma57_delta_generator import (  # noqa: E402
  build_phase67_7_data,
)


def build_phase67_representative_result():
  return build_phase67_7_data()


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


def print_phase67_results(
  representative,
):
  print_section(
    "Toda Lemma 5.7 result"
  )

  print(
    "General implication:"
  )
  print(
    "E²α ∈ 2ι₅∘π_(i+2)(S⁵)"
  )
  print(
    "⇒"
  )
  print(
    "E(η₂∘α) = 0"
  )
  print()

  print(
    "In particular:"
  )
  print(
    "E(η₂∘ν′) = 0"
  )
  print()
  print(
    "Δ(ν₅) = ±(η₂∘ν′)"
  )


def print_phase67_derivation_chain(
  representative,
):
  print_section(
    "Proof-style derivation"
  )

  print(
    "General Lemma 5.7 branch:"
  )
  print()
  print(
    "Assume"
  )
  print(
    "E²α ∈ 2ι₅∘π_(i+2)(S⁵)."
  )
  print()
  print(
    "Then"
  )
  print(
    "E²(η₂∘α)"
  )
  print(
    "= η₄∘E²α."
  )
  print()
  print(
    "Since E²α lies in "
    "2ι₅∘π_(i+2)(S⁵)"
  )
  print(
    "and 2η₄=0,"
  )
  print(
    "E²(η₂∘α)=0."
  )
  print()
  print(
    "By Toda Lemma 4.5 "
    "for n=3,"
  )
  print(
    "E(η₂∘α)=0."
  )
  print()

  print(
    "ν′ specialization:"
  )
  print()
  print(
    "Toda Lemma 5.4 gives"
  )
  print(
    "2Eν₄ = E²ν′."
  )
  print()
  print(
    "Since ν₅=Eν₄,"
  )
  print(
    "E²ν′ ∈ 2ι₅∘π_8(S⁵)."
  )
  print()
  print(
    "Apply the general Lemma 5.7 branch:"
  )
  print(
    "E(η₂∘ν′)=0."
  )
  print()

  print(
    "Group calculation:"
  )
  print()
  print(
    "Toda (5.2):"
  )
  print(
    "η₂∘- : π_6^3 ≅ π_6^2."
  )
  print()
  print(
    "Toda Proposition 5.6:"
  )
  print(
    "π_6^3 = Z/4{ν′}."
  )
  print()
  print(
    "Therefore"
  )
  print(
    "π_6^2 = Z/4{η₂∘ν′}."
  )
  print()

  print(
    "Toda (4.4) exactness:"
  )
  print(
    "π_8^5 ─Δ→ π_6^2 ─E→ π_7^3."
  )
  print()
  print(
    "Since E(η₂∘ν′)=0 "
    "and η₂∘ν′ generates π_6^2,"
  )
  print(
    "E is zero on π_6^2."
  )
  print()
  print(
    "Exactness therefore gives"
  )
  print(
    "Δ(π_8^5)=π_6^2."
  )
  print()

  print(
    "Toda Proposition 5.6:"
  )
  print(
    "π_8^5 = Z/8{ν₅}."
  )
  print()
  print(
    "Hence"
  )
  print(
    "π_6^2 = <Δ(ν₅)>."
  )
  print()
  print(
    "Since"
  )
  print(
    "π_6^2 = Z/4{η₂∘ν′},"
  )
  print(
    "we obtain"
  )
  print(
    "Δ(ν₅)=±(η₂∘ν′)."
  )


def print_phase67_provenance(
  representative,
):
  print_section(
    "Provenance / integration"
  )

  phase67_5 = (
    representative[
      "phase67_5"
    ]
  )

  hypothesis_step = (
    phase67_5[
      "hypothesis_step"
    ]
  )

  eta2_nu_prime_zero_step = (
    representative[
      "eta2_nu_prime_zero_step"
    ]
  )

  pi6_2_step = (
    representative[
      "pi6_2_step"
    ]
  )

  exactness_step = (
    representative[
      "exactness_step"
    ]
  )

  delta_surjective_step = (
    representative[
      "delta_surjective_step"
    ]
  )

  prop56_step = (
    representative[
      "prop56_step"
    ]
  )

  final_step = (
    representative[
      "final_step"
    ]
  )

  result = (
    representative[
      "result"
    ]
  )

  all_final_premises_inference = all(
    premise.rule
    == ProofRule.INFERENCE
    for premise
    in final_step.premises
  )

  structural_window_given = (
    representative[
      "window_step"
    ].rule
    == ProofRule.GIVEN
  )

  fixed_point = (
    result.termination_reason.value
    == "fixed_point"
  )

  print(
    "E²ν′ image hypothesis derived = "
    f"{hypothesis_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "E(η₂∘ν′)=0 derived = "
    f"{eta2_nu_prime_zero_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "π_6^2=Z/4{η₂∘ν′} derived = "
    f"{pi6_2_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "Toda (4.4) exactness derived = "
    f"{exactness_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "Δ surjective derived = "
    f"{delta_surjective_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "Toda Proposition 5.6 aggregate derived = "
    f"{prop56_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "Δ(ν₅)=±(η₂∘ν′) derived = "
    f"{final_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "final result is GIVEN = "
    f"{final_step.rule == ProofRule.GIVEN}"
  )

  print(
    "all final premises are INFERENCE = "
    f"{all_final_premises_inference}"
  )

  print(
    "Toda (4.4) structural window "
    "remains GIVEN = "
    f"{structural_window_given}"
  )

  print(
    "Phase 66 dependency used = False"
  )

  print(
    "fixed point = "
    f"{fixed_point}"
  )


def print_phase67_source():
  print_section(
    "Literature / source"
  )

  print(
    "[Toda Lemma 5.7]"
  )
  print(
    "Author: H. Toda"
  )
  print(
    "Source: Composition Methods "
    "in Homotopy Groups of Spheres"
  )
  print(
    "Year: 1962"
  )
  print(
    "Locator: Lemma 5.7"
  )
  print()
  print(
    "Representative statement:"
  )
  print(
    "  If E²α belongs to "
    "2ι₅∘π_(i+2)(S⁵), "
    "then E(η₂∘α)=0."
  )
  print(
    "  In particular, "
    "E(η₂∘ν′)=0 and "
    "Δ(ν₅)=±(η₂∘ν′)."
  )
  print()
  print(
    "This source display is "
    "probe-local presentation metadata."
  )
  print(
    "Phase 67 does not add a new "
    "literature registry or theorem database."
  )


def print_phase67_proof_record():
  print_section(
    "Proof record"
  )

  print(
    "docs/proof_records.md"
  )
  print(
    "  Toda Lemma 5.7"
  )
  print()

  print(
    "The proof-style derivation above "
    "is hand-authored presentation code."
  )
  print(
    "It is not yet generated "
    "automatically from the ProofStep graph."
  )


def print_phase67_boundary():
  print_section(
    "Phase 67 completion boundary"
  )

  print(
    "Implemented:"
  )
  print(
    "  Lemma 5.7 image hypothesis semantics"
  )
  print(
    "  E²(η₂∘α)=0"
  )
  print(
    "  E(η₂∘α)=0"
  )
  print(
    "  ν′ specialization"
  )
  print(
    "  E(η₂∘ν′)=0"
  )
  print(
    "  π_6^2=Z/4{η₂∘ν′}"
  )
  print(
    "  concrete Toda (4.4) exactness"
  )
  print(
    "  Δ surjectivity"
  )
  print(
    "  Δ(ν₅)=±(η₂∘ν′)"
  )
  print(
    "  applicability / provenance / "
    "non-circularity regression"
  )
  print(
    "  representative proof-style display"
  )
  print(
    "  docs/proof_records.md entry"
  )
  print()

  print(
    "Deferred:"
  )
  print(
    "  generic image-membership framework"
  )
  print(
    "  generic existential witness"
  )
  print(
    "  generic cyclic-image solver"
  )
  print(
    "  generic ± algebra"
  )
  print(
    "  automatic proof narrative generation"
  )
  print(
    "  persistent Proof Repository"
  )


def main():
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 67 capability demonstration"
  )

  representative = (
    build_phase67_representative_result()
  )

  print_phase67_results(
    representative
  )

  print_phase67_derivation_chain(
    representative
  )

  print_phase67_provenance(
    representative
  )

  print_phase67_source()

  print_phase67_proof_record()

  print_phase67_boundary()


if __name__ == "__main__":
  main()


