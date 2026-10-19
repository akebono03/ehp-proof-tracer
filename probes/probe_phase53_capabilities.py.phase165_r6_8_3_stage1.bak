from expression import (
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
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
  build_phase50_representative_result,
  print_separator,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  toda_45_isomorphism_inference_rule,
  toda_45_pi4_3_finite_cyclic_transport_inference_rule,
)


def build_phase53_representative_result():
  phase50 = (
    build_phase50_representative_result()
  )

  n = ScalarSymbol(
    name="n",
  )

  stable_range = (
    ScalarGreaterEqualStatement(
      left=3,
      right=ScalarSum(
        left=1,
        right=2,
      ),
    )
  )

  suspension_range = (
    ScalarGreaterEqualStatement(
      left=n,
      right=3,
    )
  )

  target_group = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=n,
      right=1,
    ),
    sphere_dimension=n,
  )

  suspension_map = (
    TodaIteratedSuspensionMap(
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=3,
          right=1,
        ),
        sphere_dimension=3,
      ),
      target_group=target_group,
    )
  )

  premise_steps = (
    phase50[
      "premise_steps"
    ]
    + (
      ProofStep(
        conclusion=stable_range,
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      ProofStep(
        conclusion=suspension_range,
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      ProofStep(
        conclusion=suspension_map,
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    )
  )

  rules = (
    phase50[
      "rules"
    ]
    + (
      toda_45_isomorphism_inference_rule(),
      toda_45_pi4_3_finite_cyclic_transport_inference_rule(),
    )
  )

  target_relation = Relation(
    lhs=target_group,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=IteratedSuspension(
        expression=phase50[
          "eta_3"
        ],
        exponent=(
          suspension_map.exponent
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  phase50_final_relation = (
    phase50[
      "final_group_steps"
    ][
      0
    ]
    .conclusion
  )

  phase50_final_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == phase50_final_relation
    )
  )

  toda45_steps = tuple(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Toda45IsomorphismStatement,
      )
      and step.conclusion.map
      == suspension_map
    )
  )

  transported_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == target_relation
    )
  )

  return {
    "phase50": phase50,
    "n": n,
    "stable_range": stable_range,
    "suspension_range": (
      suspension_range
    ),
    "suspension_map": (
      suspension_map
    ),
    "target_group": target_group,
    "target_relation": (
      target_relation
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
  }


def print_phase53_transport(
  representative,
):
  print()
  print_separator()
  print(
    "Phase 53 Toda (4.5) finite-cyclic transport"
  )
  print_separator()
  print()

  print(
    "  π_4^3 = Z/2{η₃}"
  )

  print()
  print(
    "  Toda (4.5):"
  )
  print(
    "  E^(n-3): "
    "π_4^3 ≅ π_(n+1)^n"
  )

  print()
  print(
    "  ↓"
  )

  print()
  print(
    "  π_(n+1)^n "
    "= Z/2{E^(n-3)η₃}"
  )


def print_phase53_rounds(
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


def print_phase53_provenance(
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

  isomorphism_step = (
    representative[
      "toda45_steps"
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
    "Toda45 isomorphism is derived =",
    (
      isomorphism_step.rule
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
    "transport rule =",
    transport_step
    .inference_rule
    .name,
  )

  print(
    "transport premise count =",
    len(
      transport_step.premises
    ),
  )

  print(
    "transport premises are derived =",
    all(
      premise.rule
      == ProofRule.INFERENCE
      for premise in (
        transport_step.premises
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


def print_phase53_boundary():
  print()
  print_separator()
  print(
    "Phase 53 boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )

  print(
    "  pi_4^3 = Z/2{eta_3}"
  )

  print(
    "  Toda (4.5) stable-range isomorphism"
  )

  print(
    "  finite-cyclic transport"
  )

  print(
    "  pi_(n+1)^n "
    "= Z/2{E^(n-3)eta_3}"
  )

  print()
  print(
    "Still outside Phase 53:"
  )

  print(
    "  E^(n-3)eta_3 = eta_n"
  )

  print(
    "  generic isomorphism transport"
  )

  print(
    "  generic generator transport"
  )

  print(
    "  generic suspension normalization"
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
    "Phase 53 capability demonstration"
  )

  representative = (
    build_phase53_representative_result()
  )

  print_phase53_transport(
    representative
  )

  print_phase53_rounds(
    representative
  )

  print_phase53_provenance(
    representative
  )

  print_phase53_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()



