from expression import (
  Composition,
  HomotopyElement,
  MapApplication,
  Multiple,
)
from hopf_facts import (
  ETA_2,
)
from map_facts import (
  EHP_H_MAP_ISOMORPHISM_FACT,
)
from map_property_rules import (
  injective_map_reflects_equality_inference_rule,
  isomorphism_implies_injective_inference_rule,
)
from probes.probe_phase37_capabilities import (
  build_phase37_end_to_end,
)
from proof import (
  ProofStep,
  Relation,
  apply_inference_match,
  find_inference_match,
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


def build_phase38_end_to_end():
  isomorphism_step = (
    EHP_H_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  injectivity_rule = (
    isomorphism_implies_injective_inference_rule()
  )

  injective_step = require_match(
    injectivity_rule,
    (
      isomorphism_step,
    ),
    (
      "Phase 38 actual "
      "Isomorphism(H) did not "
      "derive Injective(H)"
    ),
  )

  phase37_result = (
    build_phase37_end_to_end()
  )

  h_side_equality_step = (
    phase37_result[
      "final_step"
    ]
  )

  reflection_rule = (
    injective_map_reflects_equality_inference_rule()
  )

  final_step = require_match(
    reflection_rule,
    (
      injective_step,
      h_side_equality_step,
    ),
    (
      "Phase 38 injective "
      "reflection did not match"
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
    lhs=two_iota_2_eta_2,
    rhs=four_eta_2,
    relation_type=(
      final_step
      .conclusion
      .relation_type
    ),
  )

  if final_step.conclusion != expected_final:
    raise RuntimeError(
      "Phase 38 final result was not "
      "(2ι₂)η₂=4η₂"
    )

  return {
    "isomorphism_step": (
      isomorphism_step
    ),
    "injective_step": (
      injective_step
    ),
    "phase37_result": (
      phase37_result
    ),
    "h_side_equality_step": (
      h_side_equality_step
    ),
    "final_step": (
      final_step
    ),
  }


def print_phase38_chain(
  result,
):
  print_separator()
  print(
    "Actual Injective(H) "
    "reflection representative proof"
  )
  print_separator()
  print()

  print("[1] Actual Isomorphism(H)")
  print(
    " ",
    statement_text(
      result[
        "isomorphism_step"
      ].conclusion
    ),
  )
  print()

  print(
    "[2] Existing "
    "isomorphism-to-injectivity"
  )
  print(
    " ",
    statement_text(
      result[
        "injective_step"
      ].conclusion
    ),
  )
  print()

  print("[3] Phase 37 H-side equality")
  print(
    " ",
    statement_text(
      result[
        "h_side_equality_step"
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


def print_phase38_provenance(
  result,
):
  print()
  print_separator()
  print("Phase 38 provenance")
  print_separator()
  print()

  print("Dependencies:")
  print(
    "  actual isomorphism:",
    statement_text(
      result[
        "isomorphism_step"
      ].conclusion
    ),
  )
  print(
    "  injectivity rule:",
    result[
      "injective_step"
    ].inference_rule.name,
  )
  print(
    "  Phase 37 final:",
    statement_text(
      result[
        "h_side_equality_step"
      ].conclusion
    ),
  )
  print(
    "  reflection rule:",
    result[
      "final_step"
    ].inference_rule.name,
  )
  print()

  print("Proof graph confirmation:")
  print(
    "  Injective(H) includes "
    "Isomorphism(H) =",
    (
      result[
        "injective_step"
      ].premises[0]
      is result[
        "isomorphism_step"
      ]
    ),
  )
  print(
    "  final includes "
    "Injective(H) =",
    (
      result[
        "final_step"
      ].premises[0]
      is result[
        "injective_step"
      ]
    ),
  )
  print(
    "  final includes "
    "Phase 37 =",
    (
      result[
        "final_step"
      ].premises[1]
      is result[
        "h_side_equality_step"
      ]
    ),
  )
  print(
    "  Phase 37 includes "
    "Phase 35 =",
    (
      result[
        "h_side_equality_step"
      ].premises[0]
      is result[
        "phase37_result"
      ][
        "phase35_step"
      ]
    ),
  )
  print(
    "  Phase 37 symmetry "
    "includes Phase 36 =",
    (
      result[
        "phase37_result"
      ][
        "reversed_phase36_step"
      ].premises[0]
      is result[
        "phase37_result"
      ][
        "phase36_step"
      ]
    ),
  )


def print_phase38_boundary():
  print()
  print_separator()
  print("Phase 38 completion boundary")
  print_separator()
  print()

  print("Now available:")
  print(
    "  Isomorphism(H)"
  )
  print(
    "  Injective(H)"
  )
  print(
    "  H((2ι₂)η₂)=H(4η₂)"
  )
  print(
    "  (2ι₂)η₂=4η₂"
  )
  print()

  print("Not introduced by Phase 38:")
  print(
    "  new H-specific "
    "reflection theorem"
  )
  print(
    "  direct "
    "Isomorphism(H) reflection"
  )
  print(
    "  unrestricted arbitrary-map "
    "equality reflection"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 38 capability demonstration")
  print()

  result = build_phase38_end_to_end()

  print_phase38_chain(
    result
  )

  print_phase38_provenance(
    result
  )

  print_phase38_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()


