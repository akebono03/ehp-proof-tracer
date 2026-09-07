from homotopy_groups import (
  FiniteCyclicGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_until_stable_with_history,
)
from probes.probe_phase50_capabilities import (
  print_separator,
)
from probes.probe_phase53_capabilities import (
  build_phase53_representative_result,
)
from toda_rules import (
  toda_eta_family_definition_statement,
  toda_higher_eta_family_bridge_inference_rule,
  toda_higher_eta_finite_cyclic_generator_inference_rule,
)


def build_phase54_representative_result():
  phase53 = (
    build_phase53_representative_result()
  )

  n = phase53[
    "n"
  ]

  eta_n_definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  eta_n_definition_step = ProofStep(
    conclusion=eta_n_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  premise_steps = (
    phase53[
      "premise_steps"
    ]
    + (
      eta_n_definition_step,
    )
  )

  rules = (
    phase53[
      "rules"
    ]
    + (
      toda_higher_eta_family_bridge_inference_rule(),
      toda_higher_eta_finite_cyclic_generator_inference_rule(),
    )
  )

  transported_generator = (
    phase53[
      "target_relation"
    ]
    .rhs
    .generator
  )

  higher_eta_relation = Relation(
    lhs=transported_generator,
    rhs=eta_n_definition.element,
    relation_type=RelationType.EQUALITY,
  )

  final_relation = Relation(
    lhs=phase53[
      "target_group"
    ],
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_n_definition.element,
    ),
    relation_type=RelationType.EQUALITY,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  phase50_final_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == phase53[
        "phase50_final_steps"
      ][
        0
      ].conclusion
    )
  )

  toda45_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == phase53[
        "toda45_steps"
      ][
        0
      ].conclusion
    )
  )

  transported_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == phase53[
        "target_relation"
      ]
    )
  )

  higher_eta_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == higher_eta_relation
    )
  )

  final_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == final_relation
    )
  )

  return {
    "phase53": phase53,
    "n": n,
    "eta_n_definition": (
      eta_n_definition
    ),
    "higher_eta_relation": (
      higher_eta_relation
    ),
    "final_relation": (
      final_relation
    ),
    "premise_steps": premise_steps,
    "rules": rules,
    "result": result,
    "phase50_final_steps": (
      phase50_final_steps
    ),
    "toda45_steps": toda45_steps,
    "transported_steps": (
      transported_steps
    ),
    "higher_eta_steps": (
      higher_eta_steps
    ),
    "final_steps": final_steps,
  }


def print_phase54_eta_bridge(
  representative,
):
  print()
  print_separator()
  print(
    "Phase 54 higher eta-family bridge"
  )
  print_separator()
  print()

  print(
    "  η_n = E^(n-2)η₂"
  )

  print(
    "  η₃ = Eη₂"
  )

  print()
  print(
    "  ↓"
  )

  print()
  print(
    "  E^(n-3)η₃ = η_n"
  )


def print_phase54_final_group(
  representative,
):
  print()
  print_separator()
  print(
    "Phase 54 finite-cyclic integration"
  )
  print_separator()
  print()

  print(
    "  π_(n+1)^n "
    "= Z/2{E^(n-3)η₃}"
  )

  print()

  print(
    "  E^(n-3)η₃ = η_n"
  )

  print()
  print(
    "  ↓"
  )

  print()
  print(
    "  π_(n+1)^n "
    "= Z/2{η_n}"
  )


def print_phase54_rounds(
  representative,
):
  print()
  print_separator()
  print(
    "Inference rounds"
  )
  print_separator()
  print()

  result = representative[
    "result"
  ]

  for index, round_result in enumerate(
    result.round_results,
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


def print_phase54_provenance(
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

  source_step = (
    representative[
      "phase50_final_steps"
    ][
      0
    ]
  )

  transport_step = (
    representative[
      "transported_steps"
    ][
      0
    ]
  )

  eta_bridge_step = (
    representative[
      "higher_eta_steps"
    ][
      0
    ]
  )

  final_step = (
    representative[
      "final_steps"
    ][
      0
    ]
  )

  derived_steps = tuple(
    step
    for step in result.steps
    if step.rule
    == ProofRule.INFERENCE
  )

  print(
    "source group result is derived =",
    (
      source_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "transport result is derived =",
    (
      transport_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "higher eta bridge is derived =",
    (
      eta_bridge_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "higher eta bridge rule =",
    eta_bridge_step
    .inference_rule
    .name,
  )

  print(
    "final group result is derived =",
    (
      final_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "final group rule =",
    final_step
    .inference_rule
    .name,
  )

  print(
    "final premise count =",
    len(
      final_step.premises
    ),
  )

  print(
    "final premises are derived =",
    all(
      premise.rule
      == ProofRule.INFERENCE
      for premise in (
        final_step.premises
      )
    ),
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


def print_phase54_boundary():
  print()
  print_separator()
  print(
    "Phase 54 boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )

  print(
    "  eta_n = E^(n-2)eta_2"
  )

  print(
    "  E^(n-3)eta_3 = eta_n"
  )

  print(
    "  pi_(n+1)^n "
    "= Z/2{E^(n-3)eta_3}"
  )

  print(
    "  pi_(n+1)^n "
    "= Z/2{eta_n}"
  )

  print()
  print(
    "Still outside Phase 54:"
  )

  print(
    "  generic iterated-suspension "
    "composition"
  )

  print(
    "  generic suspension normalization"
  )

  print(
    "  generic scalar normalization"
  )

  print(
    "  generic cyclic-generator rewrite"
  )

  print(
    "  Proposition 5.1 integration"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 54 capability demonstration"
  )

  representative = (
    build_phase54_representative_result()
  )

  print_phase54_eta_bridge(
    representative
  )

  print_phase54_final_group(
    representative
  )

  print_phase54_rounds(
    representative
  )

  print_phase54_provenance(
    representative
  )

  print_phase54_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()



