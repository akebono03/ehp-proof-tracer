from expression import (
  HomotopyElement,
  MapApplication,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from low_dimensional_facts import (
  e_pi_1_1_to_pi_2_2_isomorphism_fact,
  pi_2_1_zero_fact,
  pi_3_3_free_cyclic_fact,
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
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaPi32Eta2DefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
  toda_exactness_injective_right_implies_delta_zero_inference_rule,
  toda_exactness_zero_delta_implies_hopf_surjective_inference_rule,
  toda_exactness_zero_left_implies_hopf_injective_inference_rule,
  toda_hopf_injective_surjective_implies_isomorphism_inference_rule,
  toda_pi3_2_define_eta2_inference_rule,
  toda_pi3_2_eta2_hopf_relation_inference_rule,
  toda_pi3_2_free_cyclic_generator_inference_rule,
  toda_suspension_isomorphism_implies_injective_inference_rule,
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


def free_cyclic_text(
  relation,
):
  if not isinstance(
    relation.rhs,
    FreeCyclicGroup,
  ):
    raise TypeError(
      "relation rhs must be a "
      "FreeCyclicGroup"
    )

  return (
    group_text(
      relation.lhs
    )
    + " = Z{"
    + relation.rhs.generator.name
    + "}"
  )


def suspension_map_text(
  suspension_map,
):
  return (
    "E: "
    + group_text(
      suspension_map.source_group
    )
    + " → "
    + group_text(
      suspension_map.target_group
    )
  )


def hopf_map_text(
  hopf_map,
):
  return (
    "H: "
    + group_text(
      hopf_map.source_group
    )
    + " → "
    + group_text(
      hopf_map.target_group
    )
  )


def delta_map_text(
  delta_map,
):
  return (
    "Δ: "
    + group_text(
      delta_map.source_group
    )
    + " → "
    + group_text(
      delta_map.target_group
    )
  )


def exactness_text(
  exactness,
):
  window = exactness.window

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


def hopf_relation_text(
  relation,
):
  if not isinstance(
    relation.lhs,
    MapApplication,
  ):
    raise TypeError(
      "relation lhs must be a "
      "MapApplication"
    )

  return (
    relation.lhs.map.name
    + "("
    + relation.lhs.expression.name
    + ") = "
    + relation.rhs.name
  )


def build_phase49_representative_result():
  pi_2_1 = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=1,
  )

  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )

  pi_1_1 = TodaPrimaryGroup(
    group_dimension=1,
    sphere_dimension=1,
  )

  pi_2_2 = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=2,
  )

  zero_fact = (
    pi_2_1_zero_fact()
  )

  target_group_fact = (
    pi_3_3_free_cyclic_fact()
  )

  suspension_isomorphism = (
    e_pi_1_1_to_pi_2_2_isomorphism_fact()
  )

  e_h_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_2_1,
        middle_term=pi_3_2,
        target_term=pi_3_3,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      ),
    )
  )

  h_delta_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_3_2,
        middle_term=pi_3_3,
        target_term=pi_1_1,
        first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
      ),
    )
  )

  delta_e_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_3_3,
        middle_term=pi_1_1,
        target_term=pi_2_2,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      ),
    )
  )

  premise_steps = (
    ProofStep(
      conclusion=zero_fact,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=target_group_fact,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=suspension_isomorphism,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=e_h_exactness,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=h_delta_exactness,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=delta_e_exactness,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  rules = (
    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
    toda_suspension_isomorphism_implies_injective_inference_rule(),
    toda_exactness_injective_right_implies_delta_zero_inference_rule(),
    toda_exactness_zero_delta_implies_hopf_surjective_inference_rule(),
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
    toda_pi3_2_define_eta2_inference_rule(),
    toda_pi3_2_eta2_hopf_relation_inference_rule(),
    toda_pi3_2_free_cyclic_generator_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  hopf_injective_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantInjectiveStatement,
    )
  )

  suspension_injective_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaSuspensionInjectiveStatement,
    )
  )

  delta_zero_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaDeltaZeroStatement,
    )
  )

  hopf_surjective_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantSurjectiveStatement,
    )
  )

  hopf_isomorphism_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantIsomorphismStatement,
    )
  )

  eta_2_definition_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaPi32Eta2DefinitionStatement,
    )
  )

  hopf_relation_steps = tuple(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        MapApplication,
      )
      and step.conclusion.lhs.map
      == EHP_H_MAP
      and isinstance(
        step.conclusion.lhs.expression,
        HomotopyElement,
      )
      and step.conclusion.lhs.expression.name
      == "η₂"
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
      == pi_3_2
      and isinstance(
        step.conclusion.rhs,
        FreeCyclicGroup,
      )
      and step.conclusion.rhs.generator.name
      == "η₂"
    )
  )

  return {
    "pi_2_1": pi_2_1,
    "pi_3_2": pi_3_2,
    "pi_3_3": pi_3_3,
    "pi_1_1": pi_1_1,
    "pi_2_2": pi_2_2,
    "zero_fact": zero_fact,
    "target_group_fact": target_group_fact,
    "suspension_isomorphism": (
      suspension_isomorphism
    ),
    "e_h_exactness": e_h_exactness,
    "h_delta_exactness": (
      h_delta_exactness
    ),
    "delta_e_exactness": (
      delta_e_exactness
    ),
    "premise_steps": premise_steps,
    "rules": rules,
    "result": result,
    "hopf_injective_steps": (
      hopf_injective_steps
    ),
    "suspension_injective_steps": (
      suspension_injective_steps
    ),
    "delta_zero_steps": (
      delta_zero_steps
    ),
    "hopf_surjective_steps": (
      hopf_surjective_steps
    ),
    "hopf_isomorphism_steps": (
      hopf_isomorphism_steps
    ),
    "eta_2_definition_steps": (
      eta_2_definition_steps
    ),
    "hopf_relation_steps": (
      hopf_relation_steps
    ),
    "final_group_steps": (
      final_group_steps
    ),
  }


def print_phase49_premises(
  representative,
):
  print()
  print_separator()
  print(
    "Phase 49 low-dimensional premises"
  )
  print_separator()
  print()

  print(
    " ",
    group_text(
      representative[
        "zero_fact"
      ].group
    ),
    "= 0",
  )

  print(
    " ",
    free_cyclic_text(
      representative[
        "target_group_fact"
      ]
    ),
  )

  print(
    " ",
    suspension_map_text(
      representative[
        "suspension_isomorphism"
      ].map
    ),
    "is isomorphism",
  )

  print()
  print(
    "Exactness premises:"
  )
  print()

  print(
    " ",
    exactness_text(
      representative[
        "e_h_exactness"
      ]
    ),
  )

  print(
    " ",
    exactness_text(
      representative[
        "h_delta_exactness"
      ]
    ),
  )

  print(
    " ",
    exactness_text(
      representative[
        "delta_e_exactness"
      ]
    ),
  )


def print_phase49_inference(
  representative,
):
  print()
  print_separator()
  print(
    "Phase 49 inference"
  )
  print_separator()
  print()

  for step in representative[
    "hopf_injective_steps"
  ]:
    print(
      " ",
      hopf_map_text(
        step.conclusion.map
      ),
      "is injective",
    )

  for step in representative[
    "suspension_injective_steps"
  ]:
    print(
      " ",
      suspension_map_text(
        step.conclusion.map
      ),
      "is injective",
    )

  for step in representative[
    "delta_zero_steps"
  ]:
    print(
      " ",
      delta_map_text(
        step.conclusion.map
      ),
      "= 0",
    )

  for step in representative[
    "hopf_surjective_steps"
  ]:
    print(
      " ",
      hopf_map_text(
        step.conclusion.map
      ),
      "is surjective",
    )

  for step in representative[
    "hopf_isomorphism_steps"
  ]:
    print(
      " ",
      hopf_map_text(
        step.conclusion.map
      ),
      "is isomorphism",
    )

  for step in representative[
    "eta_2_definition_steps"
  ]:
    print(
      " ",
      step.conclusion.image.name,
      "has a unique preimage under H;",
    )
    print(
      "  denote it by",
      step.conclusion.element.name,
    )

  for step in representative[
    "hopf_relation_steps"
  ]:
    print(
      " ",
      hopf_relation_text(
        step.conclusion
      ),
    )

  for step in representative[
    "final_group_steps"
  ]:
    print(
      " ",
      free_cyclic_text(
        step.conclusion
      ),
    )


def print_phase49_rounds(
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


def print_phase49_provenance(
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
    "H injectivity count =",
    len(
      representative[
        "hopf_injective_steps"
      ]
    ),
  )

  print(
    "E injectivity count =",
    len(
      representative[
        "suspension_injective_steps"
      ]
    ),
  )

  print(
    "Delta zero count =",
    len(
      representative[
        "delta_zero_steps"
      ]
    ),
  )

  print(
    "H surjectivity count =",
    len(
      representative[
        "hopf_surjective_steps"
      ]
    ),
  )

  print(
    "H isomorphism count =",
    len(
      representative[
        "hopf_isomorphism_steps"
      ]
    ),
  )

  print(
    "eta_2 definition count =",
    len(
      representative[
        "eta_2_definition_steps"
      ]
    ),
  )

  print(
    "H(eta_2)=iota_3 count =",
    len(
      representative[
        "hopf_relation_steps"
      ]
    ),
  )

  print(
    "pi_3^2 free cyclic count =",
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


def print_phase49_boundary():
  print()
  print_separator()
  print(
    "Phase 49 boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  low-dimensional facts for pi_3^2"
  )
  print(
    "  exactness + zero-left -> H injective"
  )
  print(
    "  E isomorphism -> E injective"
  )
  print(
    "  Delta-E exactness + E injective -> Delta zero"
  )
  print(
    "  H-Delta exactness + Delta zero -> H surjective"
  )
  print(
    "  H injective + surjective -> H isomorphism"
  )
  print(
    "  unique preimage of iota_3 named eta_2"
  )
  print(
    "  H(eta_2)=iota_3"
  )
  print(
    "  pi_3^2 = Z{eta_2}"
  )
  print()

  print(
    "Still outside Phase 49:"
  )
  print(
    "  general existential quantification"
  )
  print(
    "  general witness / uniqueness framework"
  )
  print(
    "  general inverse-map machinery"
  )
  print(
    "  general cyclic-generator transport"
  )
  print(
    "  Toda Proposition 2.7"
  )
  print(
    "  concrete pi_4^3 calculation"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 49 capability demonstration"
  )

  representative = (
    build_phase49_representative_result()
  )

  print_phase49_premises(
    representative
  )

  print_phase49_inference(
    representative
  )

  print_phase49_rounds(
    representative
  )

  print_phase49_provenance(
    representative
  )

  print_phase49_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()




