from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase66_literature_aggregate import (
  build_phase66_7_data,
)
from test_phase68_pi8_4_decomposition import (
  build_phase68_4_data,
)
from toda_rules import (
  Toda58EquationStatement,
  TodaDeltaImageUpToSignStatement,
  toda_prop25_delta_eta9_composition_inference_rule,
  toda_prop58_delta_eta9_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase68_5_data():
  phase66_7 = (
    build_phase66_7_data()
  )

  phase68_4 = (
    build_phase68_4_data()
  )

  toda58_step = (
    phase66_7[
      "integration_step"
    ]
  )

  pi8_4_step = (
    phase68_4[
      "final_step"
    ]
  )

  prop25_rule = (
    toda_prop25_delta_eta9_composition_inference_rule()
  )

  final_rule = (
    toda_prop58_delta_eta9_inference_rule()
  )

  rules = (
    prop25_rule,
    final_rule,
  )

  premise_steps = (
    toda58_step,
    pi8_4_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  eta_7 = HomotopyElement(
    name="η₇",
    dimension=7,
    source=8,
    target=7,
    generator=GeneratorSymbol(
      family="η",
      index=7,
    ),
  )

  eta_9 = HomotopyElement(
    name="η₉",
    dimension=9,
    source=10,
    target=9,
    generator=GeneratorSymbol(
      family="η",
      index=9,
    ),
  )

  nu_expression = Sum(
    left=Multiple(
      coefficient=2,
      expression=nu_4,
    ),
    right=Multiple(
      coefficient=-1,
      expression=Suspension(
        expression=nu_prime,
      ),
    ),
  )

  expected_prop25 = (
    TodaDeltaImageUpToSignStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=9,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=8,
          sphere_dimension=4,
        ),
      ),
      element=eta_9,
      positive_value=Composition(
        left=nu_expression,
        right=eta_7,
      ),
    )
  )

  prop25_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_prop25
    )
  )

  e_nu_prime_eta7 = Composition(
    left=Suspension(
      expression=nu_prime,
    ),
    right=eta_7,
  )

  expected_final = Relation(
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=eta_9,
    ),
    rhs=e_nu_prime_eta7,
    relation_type=RelationType.EQUALITY,
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_final
    )
  )

  return {
    "phase66_7": phase66_7,
    "phase68_4": phase68_4,
    "toda58_step": toda58_step,
    "pi8_4_step": pi8_4_step,
    "prop25_rule": prop25_rule,
    "final_rule": final_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "nu_4": nu_4,
    "nu_prime": nu_prime,
    "eta_7": eta_7,
    "eta_9": eta_9,
    "nu_expression": nu_expression,
    "expected_prop25": (
      expected_prop25
    ),
    "prop25_step": prop25_step,
    "e_nu_prime_eta7": (
      e_nu_prime_eta7
    ),
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase68_5_reuses_phase66_toda58():
  data = build_phase68_5_data()

  assert isinstance(
    data[
      "toda58_step"
    ].conclusion,
    Toda58EquationStatement,
  )

  assert (
    data[
      "toda58_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_5_reuses_phase68_4_pi8_4():
  data = build_phase68_5_data()

  assert (
    data[
      "pi8_4_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi8_4_step"
    ].conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=4,
    )
  )


def test_phase68_5_pi8_4_has_two_order_two_summands():
  data = build_phase68_5_data()

  group = (
    data[
      "pi8_4_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    DirectSumGroup,
  )

  assert len(
    group.summands
  ) == 2

  assert all(
    isinstance(
      summand,
      FiniteCyclicGroup,
    )
    and summand.order == 2
    for summand in group.summands
  )


def test_phase68_5_prop25_derives_delta_eta9_up_to_sign():
  data = build_phase68_5_data()

  assert (
    data[
      "prop25_step"
    ].conclusion
    == data[
      "expected_prop25"
    ]
  )

  assert (
    data[
      "prop25_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_5_prop25_uses_phase66_only():
  data = build_phase68_5_data()

  assert (
    data[
      "prop25_step"
    ].premises
    == (
      data[
        "toda58_step"
      ],
    )
  )


def test_phase68_5_prop25_keeps_expression_undistributed():
  data = build_phase68_5_data()

  positive_value = (
    data[
      "prop25_step"
    ].conclusion
    .positive_value
  )

  assert isinstance(
    positive_value,
    Composition,
  )

  assert (
    positive_value.left
    == data[
      "nu_expression"
    ]
  )

  assert (
    positive_value.right
    == data[
      "eta_7"
    ]
  )


def test_phase68_5_prop25_target_is_pi8_4():
  data = build_phase68_5_data()

  assert (
    data[
      "prop25_step"
    ].conclusion.map.target_group
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=4,
    )
  )


def test_phase68_5_final_is_delta_eta9():
  data = build_phase68_5_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=data[
        "eta_9"
      ],
    )
  )


def test_phase68_5_final_value_is_e_nu_prime_eta7():
  data = build_phase68_5_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs
    == data[
      "e_nu_prime_eta7"
    ]
  )


def test_phase68_5_derives_exact_final_relation():
  data = build_phase68_5_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_final"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_5_final_uses_exact_two_dependencies():
  data = build_phase68_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "prop25_step"
      ],
      data[
        "pi8_4_step"
      ],
    )
  )


def test_phase68_5_final_is_not_up_to_sign_statement():
  data = build_phase68_5_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    Relation,
  )

  assert not isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )


def test_phase68_5_prop25_rejects_given_toda58():
  data = build_phase68_5_data()

  given_toda58 = ProofStep(
    conclusion=(
      data[
        "toda58_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "prop25_rule"
    ],
    (
      given_toda58,
    ),
  ) is None


def test_phase68_5_final_rejects_given_prop25():
  data = build_phase68_5_data()

  given_prop25 = ProofStep(
    conclusion=(
      data[
        "prop25_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      given_prop25,
      data[
        "pi8_4_step"
      ],
    ),
  ) is None


def test_phase68_5_final_rejects_given_pi8_4():
  data = build_phase68_5_data()

  given_pi8_4 = ProofStep(
    conclusion=(
      data[
        "pi8_4_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "prop25_step"
      ],
      given_pi8_4,
    ),
  ) is None


def test_phase68_5_final_rejects_wrong_eta9():
  data = build_phase68_5_data()

  eta_8 = HomotopyElement(
    name="η₈",
    dimension=8,
    source=9,
    target=8,
    generator=GeneratorSymbol(
      family="η",
      index=8,
    ),
  )

  wrong_statement = replace(
    data[
      "prop25_step"
    ].conclusion,
    element=eta_8,
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      wrong_step,
      data[
        "pi8_4_step"
      ],
    ),
  ) is None


def test_phase68_5_final_rejects_wrong_pi8_4_order():
  data = build_phase68_5_data()

  relation = (
    data[
      "pi8_4_step"
    ].conclusion
  )

  group = relation.rhs

  wrong_group = DirectSumGroup(
    summands=(
      FiniteCyclicGroup(
        order=4,
        generator=(
          group.summands[
            0
          ].generator
        ),
      ),
      group.summands[
        1
      ],
    ),
  )

  wrong_step = ProofStep(
    conclusion=replace(
      relation,
      rhs=wrong_group,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "prop25_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase68_5_final_result_is_not_given():
  data = build_phase68_5_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase68_5_reaches_fixed_point():
  data = build_phase68_5_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


