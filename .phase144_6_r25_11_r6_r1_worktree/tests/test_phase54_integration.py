from expression import (
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
)
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
from test_phase53_integration import (
  build_phase53_5_integration,
)
from toda_rules import (
  toda_eta3_suspension_relation_inference_rule,
  toda_eta_family_definition_statement,
  toda_higher_eta_family_bridge_inference_rule,
  toda_higher_eta_finite_cyclic_generator_inference_rule,
)


def build_phase54_5_integration():
  phase53 = (
    build_phase53_5_integration()
  )

  n = phase53[
    "n"
  ]

  eta_n_definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  eta_3_definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  eta_n_definition_step = ProofStep(
    conclusion=eta_n_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta_3_definition_step = ProofStep(
    conclusion=eta_3_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  premise_steps = (
    phase53[
      "premise_steps"
    ]
    + (
      eta_n_definition_step,
      eta_3_definition_step,
    )
  )

  rules = (
    phase53[
      "rules"
    ]
    + (
      toda_eta3_suspension_relation_inference_rule(),
      toda_higher_eta_family_bridge_inference_rule(),
      toda_higher_eta_finite_cyclic_generator_inference_rule(),
    )
  )

  transported_generator = (
    IteratedSuspension(
      expression=phase53[
        "phase50"
      ][
        "eta_3"
      ],
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
    )
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

  higher_eta_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == higher_eta_relation
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
    "eta_3_definition": (
      eta_3_definition
    ),
    "premise_steps": premise_steps,
    "rules": rules,
    "higher_eta_relation": (
      higher_eta_relation
    ),
    "final_relation": (
      final_relation
    ),
    "result": result,
    "higher_eta_steps": (
      higher_eta_steps
    ),
    "transported_steps": (
      transported_steps
    ),
    "final_steps": final_steps,
  }


def test_phase54_5_derives_phase53_transported_group_inside_same_run():
  integration = (
    build_phase54_5_integration()
  )

  steps = integration[
    "transported_steps"
  ]

  assert len(
    steps
  ) == 1

  assert steps[
    0
  ].rule == (
    ProofRule.INFERENCE
  )


def test_phase54_5_derives_higher_eta_bridge_inside_same_run():
  integration = (
    build_phase54_5_integration()
  )

  steps = integration[
    "higher_eta_steps"
  ]

  assert len(
    steps
  ) == 1

  assert steps[
    0
  ].rule == (
    ProofRule.INFERENCE
  )

  assert steps[
    0
  ].inference_rule is not None

  assert (
    steps[
      0
    ].inference_rule.name
    == (
      "Toda higher eta-family "
      "iterated suspension bridge"
    )
  )


def test_phase54_5_derives_pi_n_plus_1_n_generated_by_eta_n():
  integration = (
    build_phase54_5_integration()
  )

  steps = integration[
    "final_steps"
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
      "final_relation"
    ]
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 2

  assert (
    relation.rhs.generator
    == integration[
      "eta_n_definition"
    ].element
  )


def test_phase54_5_final_generator_bridge_depends_on_two_derived_premises():
  integration = (
    build_phase54_5_integration()
  )

  step = integration[
    "final_steps"
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
      "Toda higher eta-family "
      "finite-cyclic generator bridge"
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
      "transported_steps"
    ][
      0
    ]
    in step.premises
  )

  assert (
    integration[
      "higher_eta_steps"
    ][
      0
    ]
    in step.premises
  )


def test_phase54_5_final_group_is_pi_n_plus_1_n():
  integration = (
    build_phase54_5_integration()
  )

  relation = (
    integration[
      "final_steps"
    ][
      0
    ].conclusion
  )

  assert (
    relation.lhs
    == integration[
      "phase53"
    ][
      "target_group"
    ]
  )


def test_phase54_5_final_generator_is_eta_n_not_iterated_suspension():
  integration = (
    build_phase54_5_integration()
  )

  generator = (
    integration[
      "final_steps"
    ][
      0
    ]
    .conclusion
    .rhs
    .generator
  )

  assert (
    generator
    == integration[
      "eta_n_definition"
    ].element
  )

  assert not isinstance(
    generator,
    IteratedSuspension,
  )


def test_phase54_5_reaches_fixed_point():
  integration = (
    build_phase54_5_integration()
  )

  result = integration[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert len(
    integration[
      "final_steps"
    ]
  ) == 1


