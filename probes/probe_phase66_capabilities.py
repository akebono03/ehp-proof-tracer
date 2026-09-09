from pathlib import Path
import sys

from proof import (
  ProofRule,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)


# Phase 66-7 の focused literature-aware aggregate builder を
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

from test_phase66_literature_aggregate import (  # noqa: E402
  build_phase66_7_data,
)


def build_phase66_representative_result():
  return build_phase66_7_data()


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


def print_phase66_results(
  representative,
):
  statement = (
    representative[
      "integration_step"
    ].conclusion
  )

  print_section(
    "Toda Equation (5.8) result"
  )

  print(
    "Δ(ι₉)"
  )
  print(
    "="
  )
  print(
    "±(2ν₄-Eν′)"
  )
  print(
    "="
  )
  print(
    "±[ι₄,ι₄]"
  )
  print()

  print(
    "aggregate type = "
    f"{type(statement).__name__}"
  )


def print_phase66_derivation_chain(
  representative,
):
  print_section(
    "Proof-style derivation"
  )

  print(
    "Phase 65:"
  )
  print(
    "π_7^4 = "
    "Z{ν₄} ⊕ Z/4{Eν′}"
  )
  print()
  print(
    "Toda (5.8):"
  )
  print(
    "Δ(ι₉)=±(2ν₄-Eν′)"
  )
  print()

  print(
    "Phase 60:"
  )
  print(
    "[ι₄,ι₄] Whitehead "
    "correction data"
  )
  print()
  print(
    "Toda (5.8):"
  )
  print(
    "[ι₄,ι₄]=±(2ν₄-Eν′)"
  )
  print()

  print(
    "same positive representative:"
  )
  print(
    "2ν₄-Eν′"
  )
  print("↓")
  print(
    "Δ(ι₉)=±[ι₄,ι₄]"
  )
  print()

  print(
    "Therefore:"
  )
  print(
    "Δ(ι₉)"
  )
  print(
    "="
  )
  print(
    "±(2ν₄-Eν′)"
  )
  print(
    "="
  )
  print(
    "±[ι₄,ι₄]"
  )


def print_phase66_provenance(
  representative,
):
  print_section(
    "Provenance / integration"
  )

  delta_nu_step = (
    representative[
      "delta_nu_step"
    ]
  )

  whitehead_nu_step = (
    representative[
      "whitehead_nu_step"
    ]
  )

  delta_whitehead_step = (
    representative[
      "delta_whitehead_step"
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
    "Δ(ι₉)=±(2ν₄-Eν′) "
    "derived = "
    f"{delta_nu_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "[ι₄,ι₄]=±(2ν₄-Eν′) "
    "derived = "
    f"{whitehead_nu_step.rule == ProofRule.INFERENCE}"
  )

  print(
    "Δ(ι₉)=±[ι₄,ι₄] "
    "derived = "
    f"{delta_whitehead_step.rule == ProofRule.INFERENCE}"
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
    delta_nu_step,
    whitehead_nu_step,
    delta_whitehead_step,
  )

  theorem_dependencies_are_inference = all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in theorem_dependencies
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


def print_phase66_literature(
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


def print_phase66_proof_record():
  print_section(
    "Proof record"
  )

  print(
    "docs/proof_records.md"
  )
  print(
    "  Toda Equation (5.8)"
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


def print_phase66_boundary():
  print_section(
    "Phase 66 completion boundary"
  )

  print(
    "Implemented:"
  )
  print(
    "  2ν₄-Eν′ structural expression"
  )
  print(
    "  Δ(ι₉)=±(2ν₄-Eν′)"
  )
  print(
    "  [ι₄,ι₄]=±(2ν₄-Eν′)"
  )
  print(
    "  Δ(ι₉)=±[ι₄,ι₄]"
  )
  print(
    "  Toda (5.8) literature-aware aggregate"
  )
  print(
    "  representative proof-style display"
  )
  print(
    "  docs/proof_records.md foundation"
  )
  print()

  print(
    "Deferred:"
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
  print(
    "  past representative proof backfill"
  )


def main():
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 66 capability demonstration"
  )

  representative = (
    build_phase66_representative_result()
  )

  print_phase66_results(
    representative
  )

  print_phase66_derivation_chain(
    representative
  )

  print_phase66_provenance(
    representative
  )

  print_phase66_literature(
    representative
  )

  print_phase66_proof_record()

  print_phase66_boundary()


if __name__ == "__main__":
  main()
