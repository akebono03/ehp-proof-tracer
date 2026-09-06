from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  Suspension,
  WhiteheadProduct,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
)
from low_dimensional_facts import (
  pi_4_5_zero_fact,
  pi_5_5_free_cyclic_fact,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaPi32Eta2DefinitionStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
  toda_delta_iota5_whitehead_square_inference_rule,
  toda_eta3_suspension_relation_inference_rule,
  toda_eta_family_definition_statement,
  toda_pi3_2_whitehead_square_up_to_sign_inference_rule,
  toda_pi4_3_delta_image_free_cyclic_inference_rule,
  toda_pi4_3_eta3_generator_inference_rule,
  toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule,
  toda_pi4_3_finite_cyclic_inference_rule,
  toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule,
  toda_prop27_iota2_whitehead_hopf_invariant_inference_rule,
)


def print_separator():
  print("=" * 72)


def group_text(
  group,
):
  return (
    "π_"
    + str(
      group.group_dimension
    )
    + "^"
    + str(
      group.sphere_dimension
    )
  )


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
    Multiple,
  ):
    return (
      str(
        expression.coefficient
      )
      + expression_text(
        expression.expression
      )
    )

  if isinstance(
    expression,
    Suspension,
  ):
    return (
      "E"
      + expression_text(
        expression.expression
      )
    )

  if isinstance(
    expression,
    WhiteheadProduct,
  ):
    return (
      "["
      + expression_text(
        expression.left
      )
      + ","
      + expression_text(
        expression.right
      )
      + "]"
    )

  return str(
    expression
  )


def free_cyclic_text(
  relation,
):
  return (
    group_text(
      relation.lhs
    )
    + " = Z{"
    + expression_text(
      relation.rhs.generator
    )
    + "}"
  )


def finite_cyclic_text(
  relation,
):
  return (
    group_text(
      relation.lhs
    )
    + " = Z/"
    + str(
      relation.rhs.order
    )
    + "{"
    + expression_text(
      relation.rhs.generator
    )
    + "}"
  )


def exactness_text(
  statement,
):
  window = statement.window

  return (
    group_text(
      window.source_term
    )
    + " -"
    + window.first_map.name
    + "→ "
    + group_text(
      window.middle_term
    )
    + " -"
    + window.second_map.name
    + "→ "
    + group_text(
      window.target_term
    )
    + " exact"
  )


def build_phase50_representative_result():
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )

  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )

  pi_4_3 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  pi_4_5 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=5,
  )

  iota_2 = HomotopyElement(
    name="ι_2",
    dimension=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  whitehead_square = WhiteheadProduct(
    left=iota_2,
    right=iota_2,
  )

  hopf_map = TodaHopfInvariantMap(
    source_group=pi_3_2,
    target_group=pi_3_3,
  )

  eta_2_definition = (
    TodaPi32Eta2DefinitionStatement(
      map=hopf_map,
      element=eta_2,
      image=iota_3,
    )
  )

  eta_2_hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=eta_2,
    ),
    rhs=iota_3,
    relation_type=RelationType.EQUALITY,
  )

  hopf_injectivity = (
    TodaHopfInvariantInjectiveStatement(
      map=hopf_map,
    )
  )

  pi_3_2_relation = Relation(
    lhs=pi_3_2,
    rhs=FreeCyclicGroup(
      generator=eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  delta_map = TodaDeltaMap(
    source_group=pi_5_5,
    target_group=pi_3_2,
  )

  delta_e_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_5_5,
        middle_term=pi_3_2,
        target_term=pi_4_3,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      ),
    )
  )

  e_h_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_3_2,
        middle_term=pi_4_3,
        target_term=pi_4_5,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      ),
    )
  )

  eta_3_definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  premise_steps = (
    ProofStep(
      conclusion=whitehead_square,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=eta_2_definition,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=eta_2_hopf_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=hopf_injectivity,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=pi_5_5_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=pi_4_5_zero_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=delta_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=delta_e_exactness,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=e_h_exactness,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=pi_3_2_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=eta_3_definition,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  rules = (
    toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
    toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
    toda_delta_iota5_whitehead_square_inference_rule(),
    toda_pi4_3_delta_image_free_cyclic_inference_rule(),
    toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
    toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
    toda_pi4_3_finite_cyclic_inference_rule(),
    toda_eta3_suspension_relation_inference_rule(),
    toda_pi4_3_eta3_generator_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  prop27_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp27HopfInvariantUpToSignStatement,
    )
  )

  whitehead_square_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaPi32WhiteheadSquareUpToSignStatement,
    )
  )

  delta_up_to_sign_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaDeltaImageUpToSignStatement,
    )
  )

  delta_image_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaDeltaImageFreeCyclicStatement,
    )
  )

  suspension_kernel_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaSuspensionKernelFreeCyclicStatement,
    )
  )

  suspension_surjective_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaSuspensionSurjectiveStatement,
    )
  )

  eta_3_relation_steps = tuple(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == eta_3
      and step.conclusion.rhs
      == Suspension(
        expression=eta_2,
      )
    )
  )

  intermediate_group_steps = tuple(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi_4_3
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 2
      and step.conclusion.rhs.generator
      == Suspension(
        expression=eta_2,
      )
    )
  )

  final_group_steps = tuple(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi_4_3
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 2
      and step.conclusion.rhs.generator
      == eta_3
    )
  )

  return {
    "pi_5_5": pi_5_5,
    "pi_3_2": pi_3_2,
    "pi_3_3": pi_3_3,
    "pi_4_3": pi_4_3,
    "pi_4_5": pi_4_5,
    "iota_2": iota_2,
    "iota_3": iota_3,
    "eta_2": eta_2,
    "eta_3": eta_3,
    "whitehead_square": (
      whitehead_square
    ),
    "eta_2_definition": (
      eta_2_definition
    ),
    "eta_2_hopf_relation": (
      eta_2_hopf_relation
    ),
    "hopf_injectivity": (
      hopf_injectivity
    ),
    "pi_3_2_relation": (
      pi_3_2_relation
    ),
    "delta_map": delta_map,
    "delta_e_exactness": (
      delta_e_exactness
    ),
    "e_h_exactness": (
      e_h_exactness
    ),
    "eta_3_definition": (
      eta_3_definition
    ),
    "premise_steps": premise_steps,
    "rules": rules,
    "result": result,
    "prop27_steps": prop27_steps,
    "whitehead_square_steps": (
      whitehead_square_steps
    ),
    "delta_up_to_sign_steps": (
      delta_up_to_sign_steps
    ),
    "delta_image_steps": (
      delta_image_steps
    ),
    "suspension_kernel_steps": (
      suspension_kernel_steps
    ),
    "suspension_surjective_steps": (
      suspension_surjective_steps
    ),
    "eta_3_relation_steps": (
      eta_3_relation_steps
    ),
    "intermediate_group_steps": (
      intermediate_group_steps
    ),
    "final_group_steps": (
      final_group_steps
    ),
  }


def print_phase50_premises(
  representative,
):
  print()
  print_separator()
  print(
    "Phase 50 prerequisites"
  )
  print_separator()
  print()

  print(
    "Phase 49 results reused:"
  )
  print(
    " ",
    free_cyclic_text(
      representative[
        "pi_3_2_relation"
      ]
    ),
  )
  print(
    " ",
    "H(η₂) = ι_3",
  )
  print(
    " ",
    "H: π_3^2 → π_3^3 is injective",
  )

  print()
  print(
    "Low-dimensional facts:"
  )
  print(
    " ",
    free_cyclic_text(
      pi_5_5_free_cyclic_fact()
    ),
  )
  print(
    " ",
    group_text(
      pi_4_5_zero_fact().group
    ),
    "= 0",
  )

  print()
  print(
    "Exactness:"
  )
  print(
    " ",
    exactness_text(
      representative[
        "delta_e_exactness"
      ]
    ),
  )
  print(
    " ",
    exactness_text(
      representative[
        "e_h_exactness"
      ]
    ),
  )


def print_phase50_inference(
  representative,
):
  print()
  print_separator()
  print(
    "Phase 50 concrete pi_4^3 inference"
  )
  print_separator()
  print()

  prop27 = representative[
    "prop27_steps"
  ][
    0
  ].conclusion

  print(
    " Toda Prop.2.7:"
  )
  print(
    "  H("
    + expression_text(
      prop27.argument
    )
    + ") = ±"
    + expression_text(
      prop27.positive_value
    )
  )

  whitehead = representative[
    "whitehead_square_steps"
  ][
    0
  ].conclusion

  print(
    "  "
    + expression_text(
      whitehead.whitehead_square
    )
    + " = ±"
    + expression_text(
      whitehead.positive_value
    )
  )

  delta = representative[
    "delta_up_to_sign_steps"
  ][
    0
  ].conclusion

  print(
    "  Δ("
    + expression_text(
      delta.element
    )
    + ") = ±"
    + expression_text(
      delta.positive_value
    )
  )

  delta_image = representative[
    "delta_image_steps"
  ][
    0
  ].conclusion

  print(
    "  Im(Δ) = Z{"
    + expression_text(
      delta_image
      .image_group
      .generator
    )
    + "}"
  )

  kernel = representative[
    "suspension_kernel_steps"
  ][
    0
  ].conclusion

  print(
    "  Ker(E) = Z{"
    + expression_text(
      kernel
      .kernel_group
      .generator
    )
    + "}"
  )

  print(
    "  E: π_3^2 → π_4^3 is surjective"
  )

  intermediate = representative[
    "intermediate_group_steps"
  ][
    0
  ].conclusion

  print(
    "  ",
    finite_cyclic_text(
      intermediate
    ),
  )

  eta_relation = representative[
    "eta_3_relation_steps"
  ][
    0
  ].conclusion

  print(
    "  "
    + expression_text(
      eta_relation.lhs
    )
    + " = "
    + expression_text(
      eta_relation.rhs
    )
  )

  final_relation = representative[
    "final_group_steps"
  ][
    0
  ].conclusion

  print(
    "  ",
    finite_cyclic_text(
      final_relation
    ),
  )


def print_phase50_rounds(
  representative,
):
  print()
  print_separator()
  print(
    "Inference rounds"
  )
  print_separator()
  print()

  for index, round_result in enumerate(
    representative[
      "result"
    ].round_results,
    start=1,
  ):
    print(
      "round",
      index,
      "new step count =",
      len(
        round_result.new_steps
      ),
    )


def print_phase50_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / fixed point"
  )
  print_separator()
  print()

  result = representative[
    "result"
  ]

  derived_steps = tuple(
    step
    for step in result.steps
    if step.rule
    == ProofRule.INFERENCE
  )

  print(
    "given premise count =",
    len(
      representative[
        "premise_steps"
      ]
    ),
  )

  print(
    "derived step count =",
    len(
      derived_steps
    ),
  )

  print(
    "Prop.2.7 consequence count =",
    len(
      representative[
        "prop27_steps"
      ]
    ),
  )

  print(
    "Whitehead-square relation count =",
    len(
      representative[
        "whitehead_square_steps"
      ]
    ),
  )

  print(
    "Delta up-to-sign count =",
    len(
      representative[
        "delta_up_to_sign_steps"
      ]
    ),
  )

  print(
    "Delta image count =",
    len(
      representative[
        "delta_image_steps"
      ]
    ),
  )

  print(
    "E kernel count =",
    len(
      representative[
        "suspension_kernel_steps"
      ]
    ),
  )

  print(
    "E surjectivity count =",
    len(
      representative[
        "suspension_surjective_steps"
      ]
    ),
  )

  print(
    "eta_3 relation count =",
    len(
      representative[
        "eta_3_relation_steps"
      ]
    ),
  )

  print(
    "intermediate pi_4^3 count =",
    len(
      representative[
        "intermediate_group_steps"
      ]
    ),
  )

  print(
    "final pi_4^3 count =",
    len(
      representative[
        "final_group_steps"
      ]
    ),
  )

  print(
    "derived round count =",
    result.round_count,
  )

  print(
    "fixed point =",
    (
      result.termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def print_phase50_boundary():
  print()
  print_separator()
  print(
    "Phase 50 boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  minimum Toda Proposition 2.7 consequence"
  )
  print(
    "  H([iota_2,iota_2]) = ±2iota_3"
  )
  print(
    "  [iota_2,iota_2] = ±2eta_2"
  )
  print(
    "  Delta(iota_5) = ±[iota_2,iota_2]"
  )
  print(
    "  Im(Delta) = Z{2eta_2}"
  )
  print(
    "  Ker(E) = Z{2eta_2}"
  )
  print(
    "  E: pi_3^2 -> pi_4^3 surjective"
  )
  print(
    "  pi_4^3 = Z/2{E eta_2}"
  )
  print(
    "  eta_n = E^(n-2) eta_2 notation"
  )
  print(
    "  eta_3 = E eta_2"
  )
  print(
    "  pi_4^3 = Z/2{eta_3}"
  )
  print()

  print(
    "Still outside Phase 50:"
  )
  print(
    "  general up-to-sign algebra"
  )
  print(
    "  general quotient simplification"
  )
  print(
    "  general first-isomorphism theorem engine"
  )
  print(
    "  general suspension normalization"
  )
  print(
    "  full Toda Proposition 2.7 formalization"
  )
  print(
    "  Toda Proposition 5.1 proof completion"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 50 capability demonstration"
  )

  representative = (
    build_phase50_representative_result()
  )

  print_phase50_premises(
    representative
  )

  print_phase50_inference(
    representative
  )

  print_phase50_rounds(
    representative
  )

  print_phase50_provenance(
    representative
  )

  print_phase50_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()


