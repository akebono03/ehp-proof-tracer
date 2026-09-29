from expression import (
  HomotopyElement,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaProp44FirstSummandRestrictionStatement,
)
import runpy


def main():
  print("=" * 78)
  print("Phase 143-75AF completion audit")
  print("=" * 78)

  first = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=5,
  )
  second = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=9,
  )
  target = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=6,
  )
  beta = HomotopyElement(
    name="β",
    dimension=11,
  )
  delta = HomotopyElement(
    name="δ",
    dimension=12,
  )
  formula = Sum(
    left=Suspension(
      expression=beta,
    ),
    right=delta,
  )

  statement = TodaProp44FirstSummandRestrictionStatement(
    decomposition_map=TodaProp44DecompositionMap(
      source_group=DirectSumGroup(
        summands=(
          first,
          second,
        )
      ),
      target_group=target,
      alpha=delta,
      beta=beta,
      gamma=delta,
      formula=formula,
    ),
    suspension_map=TodaSuspensionMap(
      source_group=first,
      target_group=target,
    ),
  )

  print("Focused semantic rendering")
  print("-" * 78)
  print(
    render_toda_proof_statement_latex(
      statement
    )
  )
  print("")
  print("Remaining fallback inventory")
  print("-" * 78)

  runpy.run_path(
    "phase143_75u/"
    "audit_phase143_75u_remaining_fallbacks.py",
    run_name="__main__",
  )

  print("")
  print("=" * 78)
  print("Expected completion conditions")
  print("=" * 78)
  print("rule-name fallback occurrences: 152")
  print("statement types: 23")
  print("distinct fallback rule names: 24")
  print(
    "TodaProp44FirstSummandRestrictionStatement "
    "absent from remaining statement inventory"
  )
  print(
    "Toda Proposition 4.4 first-summand restriction "
    "absent from fallback rule-name inventory"
  )
  print("render errors: 0")
  print("")
  print("No source files were changed.")
  print("No pytest was run.")
  print("")
  print(
    "Phase 143-75AF completion audit finished."
  )
  print(
    "Do not run the full pytest suite yet."
  )


if __name__ == "__main__":
  main()
