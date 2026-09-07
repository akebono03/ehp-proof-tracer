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
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  toda_45_isomorphism_inference_rule,
  toda_45_pi4_3_finite_cyclic_transport_inference_rule,
)


def build_phase53_5_integration():
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

  stable_range_step = ProofStep(
    conclusion=stable_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_range_step = ProofStep(
    conclusion=suspension_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_map_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  premise_steps = (
    phase50[
      "premise_steps"
    ]
    + (
      stable_range_step,
      suspension_range_step,
      suspension_map_step,
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


def test_phase53_5_derives_phase50_pi4_3_relation_inside_same_run():
  integration = (
    build_phase53_5_integration()
  )

  steps = integration[
    "phase50_final_steps"
  ]

  assert len(
    steps
  ) == 1

  assert steps[
    0
  ].rule == (
    ProofRule.INFERENCE
  )


def test_phase53_5_derives_toda45_isomorphism_inside_same_run():
  integration = (
    build_phase53_5_integration()
  )

  steps = integration[
    "toda45_steps"
  ]

  assert len(
    steps
  ) == 1

  assert steps[
    0
  ].rule == (
    ProofRule.INFERENCE
  )

  assert len(
    steps[
      0
    ].premises
  ) == 3


def test_phase53_5_derives_transported_finite_cyclic_group():
  integration = (
    build_phase53_5_integration()
  )

  steps = integration[
    "transported_steps"
  ]

  assert len(
    steps
  ) == 1

  relation = (
    steps[
      0
    ].conclusion
  )

  assert relation == (
    integration[
      "target_relation"
    ]
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 2

  assert relation.rhs.generator == (
    IteratedSuspension(
      expression=(
        integration[
          "phase50"
        ][
          "eta_3"
        ]
      ),
      exponent=(
        integration[
          "suspension_map"
        ].exponent
      ),
    )
  )


def test_phase53_5_transport_depends_on_two_derived_premises():
  integration = (
    build_phase53_5_integration()
  )

  step = integration[
    "transported_steps"
  ][
    0
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule is not None

  assert (
    step.inference_rule.name
    == (
      "Toda 4.5 pi_4^3 "
      "finite-cyclic transport"
    )
  )

  assert len(
    step.premises
  ) == 2

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in step.premises
  )

  assert (
    integration[
      "phase50_final_steps"
    ][
      0
    ]
    in step.premises
  )

  assert (
    integration[
      "toda45_steps"
    ][
      0
    ]
    in step.premises
  )


def test_phase53_5_does_not_normalize_generator_to_eta_n():
  integration = (
    build_phase53_5_integration()
  )

  relation = (
    integration[
      "transported_steps"
    ][
      0
    ]
    .conclusion
  )

  assert isinstance(
    relation.rhs.generator,
    IteratedSuspension,
  )

  assert (
    relation
    .rhs
    .generator
    .expression
    == integration[
      "phase50"
    ][
      "eta_3"
    ]
  )


def test_phase53_5_reaches_fixed_point_in_seven_rounds():
  integration = (
    build_phase53_5_integration()
  )

  result = integration[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 7

  assert (
    integration[
      "transported_steps"
    ][
      0
    ]
    in result
    .round_results[
      6
    ]
    .new_steps
  )



