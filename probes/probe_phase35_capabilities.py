from barratt_hilton_rules import (
  TODA_PROP_3_1_REFERENCE,
  HomotopyGroupMembershipStatement,
  barratt_hilton_first_inference_rule,
)
from composition_scalar_rules import (
  TODA_2_1_REFERENCE,
  IdentityMapStatement,
  right_identity_composition_inference_rule,
  toda_2_1_right_multiple_inference_rule,
)
from expression import (
  Composition,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  Multiple,
  ScalarPower,
  ScalarProduct,
  SmashProduct,
  Suspension,
)
from homomorphism_rules import (
  homomorphism_preserves_multiple_inference_rule,
  suspension_is_homomorphism_inference_rule,
  suspension_multiple_bridge_inference_rule,
)
from hopf_facts import (
  ETA_2,
  ETA_2_HOPF_INVARIANT_FACT,
  IOTA_3,
  TODA_PROP_5_1_REFERENCE,
)
from hopf_rules import (
  ehp_h_preserves_equality_inference_rule,
  hopf_invariant_proof_step,
  hopf_invariant_statement_to_ehp_h_equality_inference_rule,
  toda_prop22_left_inference_rule,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_preserved_under_left_composition_inference_rule,
  equality_preserved_under_multiple_inference_rule,
  equality_preserved_under_right_composition_inference_rule,
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
  iterated_suspension_one_bridge_inference_rule,
  nested_integer_multiple_inference_rule,
  suspension_composition_functoriality_inference_rule,
  suspension_preserves_equality_inference_rule,
)
from scalar_rules import (
  EvenScalarStatement,
  even_scalar_evaluates_minus_one_power_inference_rule,
  scalar_sign_evaluation_applies_to_multiple_inference_rule,
)
from suspension_facts import (
  IOTA_1,
  IOTA_1_SUSPENSION_FACT,
  IOTA_2,
  IOTA_2_SUSPENSION_FACT,
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
    Suspension,
  ):
    return (
      "E("
      f"{expression_text(expression.expression)}"
      ")"
    )

  if isinstance(
    expression,
    IteratedSuspension,
  ):
    return (
      "E^"
      f"{expression.exponent}"
      "("
      f"{expression_text(expression.expression)}"
      ")"
    )

  if isinstance(
    expression,
    SmashProduct,
  ):
    return (
      "("
      f"{expression_text(expression.left)}"
      "∧"
      f"{expression_text(expression.right)}"
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
    HomotopyGroupMembershipStatement,
  ):
    return (
      f"{expression_text(statement.element)}"
      " ∈ "
      "π_"
      f"{statement.group_dimension}"
      "("
      "S^"
      f"{statement.sphere_dimension}"
      ")"
    )

  if isinstance(
    statement,
    EvenScalarStatement,
  ):
    return (
      f"{statement.scalar}"
      " is even"
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


def derive_double_suspension_multiple(
  source,
  target,
  suspension_fact,
):
  homomorphism_rule = (
    suspension_is_homomorphism_inference_rule()
  )

  homomorphism_step = require_match(
    homomorphism_rule,
    (),
    (
      "Phase 35 Suspension "
      "homomorphism rule did not match"
    ),
  )

  multiple_rule = (
    homomorphism_preserves_multiple_inference_rule(
      coefficient=2,
      expression=source,
    )
  )

  generic_multiple_step = require_match(
    multiple_rule,
    (
      homomorphism_step,
    ),
    (
      "Phase 35 Suspension "
      "multiple rule did not match"
    ),
  )

  bridge_rule = (
    suspension_multiple_bridge_inference_rule(
      coefficient=2,
      expression=source,
    )
  )

  bridge_step = require_match(
    bridge_rule,
    (
      generic_multiple_step,
    ),
    (
      "Phase 35 Suspension "
      "multiple bridge did not match"
    ),
  )

  suspension_fact_step = ProofStep(
    conclusion=suspension_fact,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  multiple_equality_rule = (
    equality_preserved_under_multiple_inference_rule(
      coefficient=2,
    )
  )

  target_multiple_step = require_match(
    multiple_equality_rule,
    (
      suspension_fact_step,
    ),
    (
      "Phase 35 multiple equality "
      "transport did not match"
    ),
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  final_step = require_match(
    transitivity_rule,
    (
      bridge_step,
      target_multiple_step,
    ),
    (
      "Phase 35 Suspension "
      "multiple transitivity did not match"
    ),
  )

  expected = Relation(
    lhs=Suspension(
      expression=Multiple(
        coefficient=2,
        expression=source,
      ),
    ),
    rhs=Multiple(
      coefficient=2,
      expression=target,
    ),
    relation_type=RelationType.EQUALITY,
  )

  if final_step.conclusion != expected:
    raise RuntimeError(
      "Phase 35 Suspension "
      "multiple calculation was unexpected"
    )

  return final_step


def derive_reduced_barratt_hilton_step(
  two_iota_1,
):
  alpha_membership_step = ProofStep(
    conclusion=HomotopyGroupMembershipStatement(
      element=two_iota_1,
      group_dimension=1,
      sphere_dimension=1,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  beta_membership_step = ProofStep(
    conclusion=HomotopyGroupMembershipStatement(
      element=two_iota_1,
      group_dimension=1,
      sphere_dimension=1,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  barratt_hilton_rule = (
    barratt_hilton_first_inference_rule(
      alpha=two_iota_1,
      beta=two_iota_1,
      p=1,
      q=1,
      k=0,
      h=0,
    )
  )

  barratt_hilton_step = require_match(
    barratt_hilton_rule,
    (
      alpha_membership_step,
      beta_membership_step,
    ),
    (
      "Phase 35 concrete "
      "Barratt-Hilton rule did not match"
    ),
  )

  exponent = ScalarProduct(
    left=1,
    right=0,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=two_iota_1,
      exponent=1,
    ),
    right=IteratedSuspension(
      expression=two_iota_1,
      exponent=1,
    ),
  )

  parity_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sign_rule = (
    even_scalar_evaluates_minus_one_power_inference_rule()
  )

  sign_step = require_match(
    sign_rule,
    (
      parity_step,
    ),
    (
      "Phase 35 concrete sign "
      "evaluation did not match"
    ),
  )

  reduction_rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=sign,
      expression=composition,
    )
  )

  reduction_step = require_match(
    reduction_rule,
    (
      sign_step,
    ),
    (
      "Phase 35 signed Multiple "
      "reduction did not match"
    ),
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  reduced_step = require_match(
    transitivity_rule,
    (
      barratt_hilton_step,
      reduction_step,
    ),
    (
      "Phase 35 Barratt-Hilton "
      "sign transitivity did not match"
    ),
  )

  return (
    barratt_hilton_step,
    parity_step,
    sign_step,
    reduction_step,
    reduced_step,
  )


def derive_two_iota_3_composition_to_four_iota_3(
  two_iota_3,
):
  right_multiple_rule = (
    toda_2_1_right_multiple_inference_rule(
      left=two_iota_3,
      right=IOTA_3,
      coefficient=2,
    )
  )

  right_multiple_step = require_match(
    right_multiple_rule,
    (),
    (
      "Phase 35 Toda (2.1) "
      "right multiple did not match"
    ),
  )

  identity_step = ProofStep(
    conclusion=IdentityMapStatement(
      element=IOTA_3,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  identity_rule = (
    right_identity_composition_inference_rule(
      expression=two_iota_3,
    )
  )

  identity_composition_step = require_match(
    identity_rule,
    (
      identity_step,
    ),
    (
      "Phase 35 right identity "
      "composition did not match"
    ),
  )

  multiple_rule = (
    equality_preserved_under_multiple_inference_rule(
      coefficient=2,
    )
  )

  multiplied_identity_step = require_match(
    multiple_rule,
    (
      identity_composition_step,
    ),
    (
      "Phase 35 identity multiple "
      "transport did not match"
    ),
  )

  nested_rule = (
    nested_integer_multiple_inference_rule(
      outer_coefficient=2,
      inner_coefficient=2,
      expression=IOTA_3,
    )
  )

  nested_step = require_match(
    nested_rule,
    (),
    (
      "Phase 35 nested integer "
      "multiple did not match"
    ),
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  first_step = require_match(
    transitivity_rule,
    (
      right_multiple_step,
      multiplied_identity_step,
    ),
    (
      "Phase 35 composition "
      "multiple transitivity did not match"
    ),
  )

  final_step = require_match(
    transitivity_rule,
    (
      first_step,
      nested_step,
    ),
    (
      "Phase 35 four-iota "
      "transitivity did not match"
    ),
  )

  return (
    right_multiple_step,
    identity_step,
    final_step,
  )


def build_phase35_end_to_end():
  two_iota_1 = Multiple(
    coefficient=2,
    expression=IOTA_1,
  )

  two_iota_2 = Multiple(
    coefficient=2,
    expression=IOTA_2,
  )

  two_iota_3 = Multiple(
    coefficient=2,
    expression=IOTA_3,
  )

  four_iota_3 = Multiple(
    coefficient=4,
    expression=IOTA_3,
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  suspension_rule = (
    suspension_preserves_equality_inference_rule()
  )

  e_two_iota_1_step = (
    derive_double_suspension_multiple(
      source=IOTA_1,
      target=IOTA_2,
      suspension_fact=(
        IOTA_1_SUSPENSION_FACT
      ),
    )
  )

  e_two_iota_2_step = (
    derive_double_suspension_multiple(
      source=IOTA_2,
      target=IOTA_3,
      suspension_fact=(
        IOTA_2_SUSPENSION_FACT
      ),
    )
  )

  (
    barratt_hilton_step,
    parity_step,
    sign_step,
    reduction_step,
    reduced_smash_step,
  ) = derive_reduced_barratt_hilton_step(
    two_iota_1
  )

  reduced_smash_symmetry_step = (
    require_match(
      symmetry_rule,
      (
        reduced_smash_step,
      ),
      (
        "Phase 35 Barratt-Hilton "
        "symmetry did not match"
      ),
    )
  )

  suspended_smash_step = require_match(
    suspension_rule,
    (
      reduced_smash_step,
    ),
    (
      "Phase 35 suspension of "
      "Barratt-Hilton equality did not match"
    ),
  )

  functoriality_rule = (
    suspension_composition_functoriality_inference_rule()
  )

  functoriality_step = require_match(
    functoriality_rule,
    (
      reduced_smash_symmetry_step,
    ),
    (
      "Phase 35 Suspension-composition "
      "functoriality did not match"
    ),
  )

  suspended_smash_to_components_step = (
    require_match(
      transitivity_rule,
      (
        suspended_smash_step,
        functoriality_step,
      ),
      (
        "Phase 35 suspended smash "
        "transitivity did not match"
      ),
    )
  )

  iterated_bridge_rule = (
    iterated_suspension_one_bridge_inference_rule(
      two_iota_1
    )
  )

  iterated_bridge_step = require_match(
    iterated_bridge_rule,
    (),
    (
      "Phase 35 E^1-to-E "
      "bridge did not match"
    ),
  )

  suspended_iterated_step = require_match(
    suspension_rule,
    (
      iterated_bridge_step,
    ),
    (
      "Phase 35 suspension of "
      "E^1-to-E bridge did not match"
    ),
  )

  suspended_e_two_iota_1_step = (
    require_match(
      suspension_rule,
      (
        e_two_iota_1_step,
      ),
      (
        "Phase 35 suspension of "
        "E(2ι₁)=2ι₂ did not match"
      ),
    )
  )

  iterated_to_e_two_iota_2_step = (
    require_match(
      transitivity_rule,
      (
        suspended_iterated_step,
        suspended_e_two_iota_1_step,
      ),
      (
        "Phase 35 iterated Suspension "
        "transitivity did not match"
      ),
    )
  )

  iterated_to_two_iota_3_step = (
    require_match(
      transitivity_rule,
      (
        iterated_to_e_two_iota_2_step,
        e_two_iota_2_step,
      ),
      (
        "Phase 35 iterated Suspension "
        "to 2ι₃ did not match"
      ),
    )
  )

  suspended_iterated_expression = (
    Suspension(
      expression=IteratedSuspension(
        expression=two_iota_1,
        exponent=1,
      ),
    )
  )

  first_component_rule = (
    equality_preserved_under_right_composition_inference_rule(
      suspended_iterated_expression,
    )
  )

  first_component_step = require_match(
    first_component_rule,
    (
      iterated_to_two_iota_3_step,
    ),
    (
      "Phase 35 first composition "
      "component transport did not match"
    ),
  )

  second_component_rule = (
    equality_preserved_under_left_composition_inference_rule(
      two_iota_3,
    )
  )

  second_component_step = require_match(
    second_component_rule,
    (
      iterated_to_two_iota_3_step,
    ),
    (
      "Phase 35 second composition "
      "component transport did not match"
    ),
  )

  component_step = require_match(
    transitivity_rule,
    (
      first_component_step,
      second_component_step,
    ),
    (
      "Phase 35 component "
      "transitivity did not match"
    ),
  )

  suspended_smash_to_two_iota_3_step = (
    require_match(
      transitivity_rule,
      (
        suspended_smash_to_components_step,
        component_step,
      ),
      (
        "Phase 35 suspended smash "
        "to 2ι₃ composition did not match"
      ),
    )
  )

  (
    right_multiple_step,
    identity_step,
    four_iota_3_step,
  ) = (
    derive_two_iota_3_composition_to_four_iota_3(
      two_iota_3
    )
  )

  suspended_smash_four_step = (
    require_match(
      transitivity_rule,
      (
        suspended_smash_to_two_iota_3_step,
        four_iota_3_step,
      ),
      (
        "Phase 35 suspended smash "
        "to 4ι₃ did not match"
      ),
    )
  )

  hopf_fact_step = hopf_invariant_proof_step(
    ETA_2_HOPF_INVARIANT_FACT
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
      "Phase 35 H(η₂)=ι₃ "
      "bridge did not match"
    ),
  )

  prop22_rule = (
    toda_prop22_left_inference_rule(
      alpha=ETA_2,
      gamma=two_iota_1,
    )
  )

  prop22_step = require_match(
    prop22_rule,
    (),
    (
      "Phase 35 Toda Prop.2.2 "
      "left rule did not match"
    ),
  )

  right_prop22_first_rule = (
    equality_preserved_under_right_composition_inference_rule(
      MapApplication(
        map=EHP_H_MAP,
        expression=ETA_2,
      ),
    )
  )

  right_prop22_first_step = require_match(
    right_prop22_first_rule,
    (
      suspended_smash_four_step,
    ),
    (
      "Phase 35 Prop.2.2 RHS "
      "first transport did not match"
    ),
  )

  right_prop22_second_rule = (
    equality_preserved_under_left_composition_inference_rule(
      four_iota_3,
    )
  )

  right_prop22_second_step = require_match(
    right_prop22_second_rule,
    (
      h_eta_2_step,
    ),
    (
      "Phase 35 Prop.2.2 RHS "
      "H(η₂) transport did not match"
    ),
  )

  four_iota_3_identity_rule = (
    right_identity_composition_inference_rule(
      expression=four_iota_3,
    )
  )

  four_iota_3_identity_step = require_match(
    four_iota_3_identity_rule,
    (
      identity_step,
    ),
    (
      "Phase 35 4ι₃ right "
      "identity did not match"
    ),
  )

  right_prop22_middle_step = (
    require_match(
      transitivity_rule,
      (
        right_prop22_first_step,
        right_prop22_second_step,
      ),
      (
        "Phase 35 Prop.2.2 RHS "
        "middle transitivity did not match"
      ),
    )
  )

  prop22_rhs_four_step = require_match(
    transitivity_rule,
    (
      right_prop22_middle_step,
      four_iota_3_identity_step,
    ),
    (
      "Phase 35 Prop.2.2 RHS "
      "to 4ι₃ did not match"
    ),
  )

  left_composition_rule = (
    equality_preserved_under_right_composition_inference_rule(
      ETA_2,
    )
  )

  left_composition_step = require_match(
    left_composition_rule,
    (
      e_two_iota_1_step,
    ),
    (
      "Phase 35 actual left "
      "composition transport did not match"
    ),
  )

  h_congruence_rule = (
    ehp_h_preserves_equality_inference_rule()
  )

  h_congruence_step = require_match(
    h_congruence_rule,
    (
      left_composition_step,
    ),
    (
      "Phase 35 actual H equality "
      "preservation did not match"
    ),
  )

  h_congruence_symmetry_step = (
    require_match(
      symmetry_rule,
      (
        h_congruence_step,
      ),
      (
        "Phase 35 actual H "
        "symmetry did not match"
      ),
    )
  )

  actual_h_to_prop22_rhs_step = (
    require_match(
      transitivity_rule,
      (
        h_congruence_symmetry_step,
        prop22_step,
      ),
      (
        "Phase 35 actual H to "
        "Prop.2.2 RHS did not match"
      ),
    )
  )

  final_step = require_match(
    transitivity_rule,
    (
      actual_h_to_prop22_rhs_step,
      prop22_rhs_four_step,
    ),
    (
      "Phase 35 final equality "
      "transitivity did not match"
    ),
  )

  expected_final = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Composition(
        left=two_iota_2,
        right=ETA_2,
      ),
    ),
    rhs=four_iota_3,
    relation_type=RelationType.EQUALITY,
  )

  if final_step.conclusion != expected_final:
    raise RuntimeError(
      "Phase 35 final result "
      "was not H((2ι₂)η₂)=4ι₃"
    )

  return {
    "e_two_iota_1_step": (
      e_two_iota_1_step
    ),
    "e_two_iota_2_step": (
      e_two_iota_2_step
    ),
    "barratt_hilton_step": (
      barratt_hilton_step
    ),
    "parity_step": parity_step,
    "sign_step": sign_step,
    "reduction_step": reduction_step,
    "reduced_smash_step": (
      reduced_smash_step
    ),
    "suspended_smash_four_step": (
      suspended_smash_four_step
    ),
    "right_multiple_step": (
      right_multiple_step
    ),
    "hopf_fact_step": (
      hopf_fact_step
    ),
    "h_eta_2_step": h_eta_2_step,
    "prop22_step": prop22_step,
    "prop22_rhs_four_step": (
      prop22_rhs_four_step
    ),
    "h_congruence_step": (
      h_congruence_step
    ),
    "final_step": final_step,
  }


def print_phase35_chain(
  result,
):
  print_separator()
  print(
    "Actual H((2ι₂)η₂) "
    "representative proof"
  )
  print_separator()
  print()

  print("[1] Suspension of the double identity")
  print(
    " ",
    statement_text(
      result[
        "e_two_iota_1_step"
      ].conclusion
    ),
  )
  print()

  print("[2] Concrete Barratt-Hilton theorem")
  print(
    " ",
    statement_text(
      result[
        "barratt_hilton_step"
      ].conclusion
    ),
  )
  print(
    "  source:",
    result[
      "barratt_hilton_step"
    ].conclusion.source.label,
  )
  print(
    "  locator:",
    result[
      "barratt_hilton_step"
    ].conclusion.source.locator,
  )
  print()

  print("[3] Explicit concrete parity")
  print(
    " ",
    statement_text(
      result[
        "parity_step"
      ].conclusion
    ),
  )
  print()

  print("[4] Sign reduction")
  print(
    " ",
    statement_text(
      result[
        "reduced_smash_step"
      ].conclusion
    ),
  )
  print()

  print("[5] Suspension / composition calculation")
  print(
    " ",
    statement_text(
      result[
        "suspended_smash_four_step"
      ].conclusion
    ),
  )
  print()

  print("[6] Toda (2.1)")
  print(
    " ",
    statement_text(
      result[
        "right_multiple_step"
      ].conclusion
    ),
  )
  print(
    "  source:",
    result[
      "right_multiple_step"
    ].conclusion.source.label,
  )
  print()

  print("[7] Toda Prop.5.1")
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
  print()

  print("[8] Toda Prop.2.2 left")
  print(
    " ",
    statement_text(
      result[
        "prop22_step"
      ].conclusion
    ),
  )
  print(
    "  inference:",
    result[
      "prop22_step"
    ].inference_rule.name,
  )
  print()

  print("[9] Prop.2.2 RHS calculation")
  print(
    " ",
    statement_text(
      result[
        "prop22_rhs_four_step"
      ].conclusion
    ),
  )
  print()

  print("[10] Actual H equality transport")
  print(
    " ",
    statement_text(
      result[
        "h_congruence_step"
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


def print_phase35_provenance(
  result,
):
  print()
  print_separator()
  print("Phase 35 provenance")
  print_separator()
  print()

  print("Literature / theorem dependencies:")
  print(
    "  Toda Prop.2.2 left:",
    result[
      "prop22_step"
    ].inference_rule.name,
  )
  print(
    "  Toda Prop.3.1:",
    result[
      "barratt_hilton_step"
    ].conclusion.source.label,
  )
  print(
    "  Toda Prop.5.1:",
    result[
      "hopf_fact_step"
    ].conclusion.source.label,
  )
  print(
    "  Toda (2.1):",
    result[
      "right_multiple_step"
    ].conclusion.source.label,
  )
  print()

  print("Reference confirmation:")
  print(
    "  Prop.3.1 reference =",
    (
      result[
        "barratt_hilton_step"
      ].conclusion.source
      == TODA_PROP_3_1_REFERENCE
    ),
  )
  print(
    "  Prop.5.1 reference =",
    (
      result[
        "hopf_fact_step"
      ].conclusion.source
      == TODA_PROP_5_1_REFERENCE
    ),
  )
  print(
    "  Toda (2.1) reference =",
    (
      result[
        "right_multiple_step"
      ].conclusion.source
      == TODA_2_1_REFERENCE
    ),
  )


def print_phase35_boundary():
  print()
  print_separator()
  print("Phase 35 completion boundary")
  print_separator()
  print()

  print("Now available:")
  print(
    "  H(η₂)=ι₃"
  )
  print(
    "  E(2ι₁)=2ι₂"
  )
  print(
    "  E(2ι₂)=2ι₃"
  )
  print(
    "  concrete Barratt-Hilton instantiation"
  )
  print(
    "  concrete parity / sign reduction"
  )
  print(
    "  directed Toda (2.1) calculation"
  )
  print(
    "  E(2ι₁∧2ι₁)=4ι₃"
  )
  print(
    "  H((2ι₂)η₂)=4ι₃"
  )
  print()

  print("Still outside Phase 35:")
  print(
    "  H(4η₂)=4ι₃"
  )
  print(
    "  H((2ι₂)η₂)=H(4η₂)"
  )
  print(
    "  injectivity reflection for this equality"
  )
  print(
    "  (2ι₂)η₂=4η₂"
  )
  print(
    "  general composition bilinearity"
  )
  print(
    "  general symbolic scalar CAS"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 35 capability demonstration")
  print()

  result = build_phase35_end_to_end()

  print_phase35_chain(
    result
  )

  print_phase35_provenance(
    result
  )

  print_phase35_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



