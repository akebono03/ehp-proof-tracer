from expression import (
  HomotopyElement,
  MapApplication,
  Multiple,
)
from homomorphism_rules import (
  HomomorphismStatement,
  homomorphism_preserves_multiple_inference_rule,
)
from hopf_facts import (
  ETA_2,
  ETA_2_HOPF_INVARIANT_FACT,
  IOTA_3,
  TODA_PROP_5_1_REFERENCE,
)
from hopf_rules import (
  ehp_h_homomorphism_proof_step,
  hopf_invariant_proof_step,
  hopf_invariant_statement_to_ehp_h_equality_inference_rule,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_preserved_under_multiple_inference_rule,
  equality_transitivity_inference_rule,
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

  if isinstance(
    statement,
    HomomorphismStatement,
  ):
    return (
      "Homomorphism("
      f"{statement.map.name}"
      ")"
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


def build_phase36_end_to_end():
  four_eta_2 = Multiple(
    coefficient=4,
    expression=ETA_2,
  )

  four_iota_3 = Multiple(
    coefficient=4,
    expression=IOTA_3,
  )

  homomorphism_step = (
    ehp_h_homomorphism_proof_step()
  )

  h_multiple_rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=4,
      expression=ETA_2,
    )
  )

  h_four_eta_2_step = require_match(
    h_multiple_rule,
    (
      homomorphism_step,
    ),
    (
      "Phase 36 actual H multiple "
      "rule did not match"
    ),
  )

  hopf_fact_step = (
    hopf_invariant_proof_step(
      ETA_2_HOPF_INVARIANT_FACT
    )
  )

  hopf_bridge_rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  h_eta_2_step = require_match(
    hopf_bridge_rule,
    (
      hopf_fact_step,
    ),
    (
      "Phase 36 H(η₂)=ι₃ "
      "bridge did not match"
    ),
  )

  multiple_rule = (
    equality_preserved_under_multiple_inference_rule(
      coefficient=4,
    )
  )

  four_h_eta_2_step = require_match(
    multiple_rule,
    (
      h_eta_2_step,
    ),
    (
      "Phase 36 equality under "
      "Multiple did not match"
    ),
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  final_step = require_match(
    transitivity_rule,
    (
      h_four_eta_2_step,
      four_h_eta_2_step,
    ),
    (
      "Phase 36 final equality "
      "transitivity did not match"
    ),
  )

  expected_final = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    rhs=four_iota_3,
    relation_type=RelationType.EQUALITY,
  )

  if final_step.conclusion != expected_final:
    raise RuntimeError(
      "Phase 36 final result "
      "was not H(4η₂)=4ι₃"
    )

  return {
    "homomorphism_step": (
      homomorphism_step
    ),
    "h_four_eta_2_step": (
      h_four_eta_2_step
    ),
    "hopf_fact_step": (
      hopf_fact_step
    ),
    "h_eta_2_step": (
      h_eta_2_step
    ),
    "four_h_eta_2_step": (
      four_h_eta_2_step
    ),
    "final_step": (
      final_step
    ),
  }


def print_phase36_chain(
  result,
):
  print_separator()
  print(
    "Actual H(4η₂) "
    "representative proof"
  )
  print_separator()
  print()

  print("[1] Actual H homomorphism")
  print(
    " ",
    statement_text(
      result[
        "homomorphism_step"
      ].conclusion
    ),
  )
  print()

  print("[2] H multiple calculation")
  print(
    " ",
    statement_text(
      result[
        "h_four_eta_2_step"
      ].conclusion
    ),
  )
  print()

  print("[3] Toda Prop.5.1")
  print(
    " ",
    statement_text(
      result[
        "h_eta_2_step"
      ].conclusion
    ),
  )
  print(
    "  source:",
    result[
      "hopf_fact_step"
    ].conclusion.source.label,
  )
  print(
    "  locator:",
    result[
      "hopf_fact_step"
    ].conclusion.source.locator,
  )
  print()

  print("[4] Equality under Multiple")
  print(
    " ",
    statement_text(
      result[
        "four_h_eta_2_step"
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


def print_phase36_provenance(
  result,
):
  print()
  print_separator()
  print("Phase 36 provenance")
  print_separator()
  print()

  print("Dependencies:")
  print(
    "  actual H homomorphism:",
    statement_text(
      result[
        "homomorphism_step"
      ].conclusion
    ),
  )
  print(
    "  generic multiple inference:",
    result[
      "h_four_eta_2_step"
    ].inference_rule.name,
  )
  print(
    "  Toda Prop.5.1:",
    result[
      "hopf_fact_step"
    ].conclusion.source.label,
  )
  print(
    "  equality under Multiple:",
    result[
      "four_h_eta_2_step"
    ].inference_rule.name,
  )
  print(
    "  final closure:",
    result[
      "final_step"
    ].inference_rule.name,
  )
  print()

  print("Reference confirmation:")
  print(
    "  Prop.5.1 reference =",
    (
      result[
        "hopf_fact_step"
      ].conclusion.source
      == TODA_PROP_5_1_REFERENCE
    ),
  )


def print_phase36_boundary():
  print()
  print_separator()
  print("Phase 36 completion boundary")
  print_separator()
  print()

  print("Now available:")
  print(
    "  actual Homomorphism(H)"
  )
  print(
    "  H(4η₂)=4H(η₂)"
  )
  print(
    "  H(η₂)=ι₃"
  )
  print(
    "  4H(η₂)=4ι₃"
  )
  print(
    "  H(4η₂)=4ι₃"
  )
  print()

  print("Still outside Phase 36:")
  print(
    "  H((2ι₂)η₂)=H(4η₂)"
  )
  print(
    "  injectivity reflection "
    "for that H-side equality"
  )
  print(
    "  (2ι₂)η₂=4η₂"
  )
  print(
    "  automatic Isomorphism "
    "to Homomorphism conversion"
  )
  print(
    "  arbitrary-map automatic "
    "homomorphism inference"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 36 capability demonstration")
  print()

  result = build_phase36_end_to_end()

  print_phase36_chain(
    result
  )

  print_phase36_provenance(
    result
  )

  print_phase36_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



