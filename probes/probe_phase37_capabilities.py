from expression import (
  Composition,
  HomotopyElement,
  MapApplication,
  Multiple,
)
from hopf_facts import (
  ETA_2,
  IOTA_3,
)
from map_facts import (
  EHP_H_MAP,
)
from probes.probe_phase35_capabilities import (
  build_phase35_end_to_end,
)
from probes.probe_phase36_capabilities import (
  build_phase36_end_to_end,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
)
from suspension_facts import (
  IOTA_2,
)


def print_separator():
  print("=" * 72)


def expression_text(
  expression,
):
  if isinstance(
    expression,
    HomotopyElement,
  ):
    return expression.name

  if isinstance(
    expression,
    MapApplication,
  ):
    return (
      f"{expression.map.name}("
      f"{expression_text(expression.expression)}"
      ")"
    )

  if isinstance(
    expression,
    Multiple,
  ):
    return (
      f"{expression.coefficient}"
      "("
      f"{expression_text(expression.expression)}"
      ")"
    )

  if isinstance(
    expression,
    Composition,
  ):
    return (
      "("
      f"{expression_text(expression.left)}"
      "∘"
      f"{expression_text(expression.right)}"
      ")"
    )

  return str(
    expression
  )


def statement_text(
  statement,
):
  if isinstance(
    statement,
    Relation,
  ):
    return (
      f"{expression_text(statement.lhs)}"
      "="
      f"{expression_text(statement.rhs)}"
    )

  return str(
    statement
  )


def require_match(
  rule,
  premises,
  message,
):
  match = find_inference_match(
    rule,
    premises,
  )

  if match is None:
    raise RuntimeError(
      message
    )

  return apply_inference_match(
    match
  )


def build_phase37_end_to_end():
  phase35_result = (
    build_phase35_end_to_end()
  )

  phase36_result = (
    build_phase36_end_to_end()
  )

  phase35_step = phase35_result[
    "final_step"
  ]

  phase36_step = phase36_result[
    "final_step"
  ]

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  reversed_phase36_step = require_match(
    symmetry_rule,
    (
      phase36_step,
    ),
    (
      "Phase 37 symmetry of "
      "H(4η₂)=4ι₃ did not match"
    ),
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  final_step = require_match(
    transitivity_rule,
    (
      phase35_step,
      reversed_phase36_step,
    ),
    (
      "Phase 37 final H-side "
      "transitivity did not match"
    ),
  )

  two_iota_2_eta_2 = Composition(
    left=Multiple(
      coefficient=2,
      expression=IOTA_2,
    ),
    right=ETA_2,
  )

  four_eta_2 = Multiple(
    coefficient=4,
    expression=ETA_2,
  )

  expected_final = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=two_iota_2_eta_2,
    ),
    rhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  if final_step.conclusion != expected_final:
    raise RuntimeError(
      "Phase 37 final result was not "
      "H((2ι₂)η₂)=H(4η₂)"
    )

  return {
    "phase35_result": (
      phase35_result
    ),
    "phase36_result": (
      phase36_result
    ),
    "phase35_step": (
      phase35_step
    ),
    "phase36_step": (
      phase36_step
    ),
    "reversed_phase36_step": (
      reversed_phase36_step
    ),
    "final_step": (
      final_step
    ),
  }


def print_phase37_chain(
  result,
):
  print_separator()
  print(
    "Actual H-side equality "
    "representative proof"
  )
  print_separator()
  print()

  print("[1] Phase 35")
  print(
    " ",
    statement_text(
      result[
        "phase35_step"
      ].conclusion
    ),
  )
  print()

  print("[2] Phase 36")
  print(
    " ",
    statement_text(
      result[
        "phase36_step"
      ].conclusion
    ),
  )
  print()

  print("[3] Equality symmetry")
  print(
    " ",
    statement_text(
      result[
        "reversed_phase36_step"
      ].conclusion
    ),
  )
  print()

  print("[RESULT]")
  print(
    " ",
    statement_text(
      result[
        "final_step"
      ].conclusion
    ),
  )
  print(
    "  result is ProofStep:",
    isinstance(
      result[
        "final_step"
      ],
      ProofStep,
    ),
  )


def print_phase37_provenance(
  result,
):
  print()
  print_separator()
  print("Phase 37 provenance")
  print_separator()
  print()

  print("Dependencies:")
  print(
    "  Phase 35 final:",
    statement_text(
      result[
        "phase35_step"
      ].conclusion
    ),
  )
  print(
    "  Phase 36 final:",
    statement_text(
      result[
        "phase36_step"
      ].conclusion
    ),
  )
  print(
    "  symmetry:",
    result[
      "reversed_phase36_step"
    ].inference_rule.name,
  )
  print(
    "  final closure:",
    result[
      "final_step"
    ].inference_rule.name,
  )
  print()

  print("Proof graph confirmation:")
  print(
    "  final includes Phase 35 =",
    (
      result[
        "final_step"
      ].premises[0]
      is result[
        "phase35_step"
      ]
    ),
  )
  print(
    "  symmetry includes Phase 36 =",
    (
      result[
        "reversed_phase36_step"
      ].premises[0]
      is result[
        "phase36_step"
      ]
    ),
  )


def print_phase37_boundary():
  print()
  print_separator()
  print("Phase 37 completion boundary")
  print_separator()
  print()

  print("Now available:")
  print(
    "  H((2ι₂)η₂)=4ι₃"
  )
  print(
    "  H(4η₂)=4ι₃"
  )
  print(
    "  4ι₃=H(4η₂)"
  )
  print(
    "  H((2ι₂)η₂)=H(4η₂)"
  )
  print()

  print("Still outside Phase 37:")
  print(
    "  Injective(H) application "
    "to the Phase 37 equality"
  )
  print(
    "  (2ι₂)η₂=4η₂"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 37 capability demonstration")
  print()

  result = build_phase37_end_to_end()

  print_phase37_chain(
    result
  )

  print_phase37_provenance(
    result
  )

  print_phase37_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()




