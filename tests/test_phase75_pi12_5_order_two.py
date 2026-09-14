from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
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
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase62_toda55_integration import (
  build_phase62_6_data,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase73_513_delta_nu9 import (
  build_phase73_6a_data,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from test_phase75_pi11_4_zero import (
  build_phase75_4_data,
)
from toda_rules import (
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaDeltaImageUpToSignStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  toda_exactness_zero_left_implies_hopf_injective_inference_rule,
  toda_nu_family_definition_statement,
  toda_prop511_pi12_9_nu9_inference_rule,
  toda_prop515_pi12_5_concrete_exactness_inference_rule,
  toda_prop515_pi12_5_finite_cyclic_inference_rule,
  toda_prop515_pi12_5_hopf_isomorphism_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_5_data():
  phase75_4 = (
    build_phase75_4_data()
  )

  phase62_6 = (
    build_phase62_6_data()
  )

  phase65_9 = (
    build_phase65_9_data()
  )

  phase73_6a = (
    build_phase73_6a_data()
  )

  phase73_8e = (
    build_phase73_8e_data()
  )

  pi11_4_zero_step = (
    phase75_4[
      "final_step"
    ]
  )

  toda55_step = (
    phase62_6[
      "integration_step"
    ]
  )

  prop56_step = (
    phase65_9[
      "integration_step"
    ]
  )

  delta_nu9_step = (
    phase73_6a[
      "final_step"
    ]
  )

  prop511_step = (
    phase73_8e[
      "final_step"
    ]
  )

  pi12_9_rule = (
    toda_prop511_pi12_9_nu9_inference_rule()
  )

  pi12_9_result = (
    run_inference_until_stable_with_history(
      (
        pi12_9_rule,
      ),
      (
        prop56_step,
      ),
    )
  )

  pi12_9 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=9,
  )

  pi12_9_step = next(
    step
    for step in pi12_9_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi12_9
    )
  )

  pi11_4 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=4,
  )

  pi12_5 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=5,
  )

  pi10_4 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=4,
  )

  e_h_window_step = ProofStep(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi11_4,
      middle_term=pi12_5,
      target_term=pi12_9,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  h_delta_window_step = ProofStep(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi12_5,
      middle_term=pi12_9,
      target_term=pi10_4,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_prop515_pi12_5_concrete_exactness_inference_rule()
  )

  hopf_injective_rule = (
    toda_exactness_zero_left_implies_hopf_injective_inference_rule()
  )

  hopf_isomorphism_rule = (
    toda_prop515_pi12_5_hopf_isomorphism_inference_rule()
  )

  finite_cyclic_rule = (
    toda_prop515_pi12_5_finite_cyclic_inference_rule()
  )

  rules = (
    exactness_rule,
    hopf_injective_rule,
    hopf_isomorphism_rule,
    finite_cyclic_rule,
  )

  premise_steps = (
    pi11_4_zero_step,
    toda55_step,
    delta_nu9_step,
    prop511_step,
    pi12_9_step,
    e_h_window_step,
    h_delta_window_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  e_h_exactness_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == TodaProp42ExactnessStatement(
        window=(
          e_h_window_step
          .conclusion
        ),
      )
    )
  )

  h_delta_exactness_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == TodaProp42ExactnessStatement(
        window=(
          h_delta_window_step
          .conclusion
        ),
      )
    )
  )

  expected_hopf_injective = (
    TodaHopfInvariantInjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=pi12_5,
        target_group=pi12_9,
      ),
    )
  )

  hopf_injective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_hopf_injective
    )
  )

  hopf_isomorphism_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp515Pi12_5HopfIsomorphismStatement,
    )
  )

  sigma_triple_prime = (
    hopf_isomorphism_step
    .conclusion
    .source_generator
  )

  expected_final = Relation(
    lhs=pi12_5,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=sigma_triple_prime,
    ),
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
    "phase75_4": phase75_4,
    "phase62_6": phase62_6,
    "phase65_9": phase65_9,
    "phase73_6a": phase73_6a,
    "phase73_8e": phase73_8e,
    "pi11_4_zero_step": (
      pi11_4_zero_step
    ),
    "toda55_step": toda55_step,
    "prop56_step": prop56_step,
    "delta_nu9_step": (
      delta_nu9_step
    ),
    "prop511_step": prop511_step,
    "pi12_9_step": pi12_9_step,
    "e_h_window_step": (
      e_h_window_step
    ),
    "h_delta_window_step": (
      h_delta_window_step
    ),
    "e_h_exactness_step": (
      e_h_exactness_step
    ),
    "h_delta_exactness_step": (
      h_delta_exactness_step
    ),
    "hopf_injective_step": (
      hopf_injective_step
    ),
    "hopf_isomorphism_step": (
      hopf_isomorphism_step
    ),
    "sigma_triple_prime": (
      sigma_triple_prime
    ),
    "expected_final": expected_final,
    "final_step": final_step,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
  }


def test_phase75_5_reuses_pi11_4_zero():
  data = build_phase75_5_data()

  assert (
    data[
      "pi11_4_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_5_reuses_toda55():
  data = build_phase75_5_data()

  assert isinstance(
    data[
      "toda55_step"
    ].conclusion,
    Toda55NuFamilyFiniteDimensionalStatement,
  )

  assert (
    data[
      "toda55_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_5_reuses_delta_nu9():
  data = build_phase75_5_data()

  assert isinstance(
    data[
      "delta_nu9_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    data[
      "delta_nu9_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_5_reuses_prop511():
  data = build_phase75_5_data()

  assert isinstance(
    data[
      "prop511_step"
    ].conclusion,
    TodaProp511FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop511_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_5_pi12_9_is_z8_nu9():
  data = build_phase75_5_data()

  relation = (
    data[
      "pi12_9_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=9,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 8
  )

  assert (
    relation.rhs.generator
    == toda_nu_family_definition_statement(
      9
    ).element
  )


def test_phase75_5_derives_two_exactness_statements():
  data = build_phase75_5_data()

  assert (
    data[
      "e_h_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "h_delta_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_5_derives_hopf_injective():
  data = build_phase75_5_data()

  assert (
    data[
      "hopf_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_5_derives_hopf_isomorphism_to_order_two_image():
  data = build_phase75_5_data()

  statement = (
    data[
      "hopf_isomorphism_step"
    ].conclusion
  )

  assert (
    statement.image_group.order
    == 2
  )

  assert (
    statement.image_generator
    == Multiple(
      coefficient=4,
      expression=(
        toda_nu_family_definition_statement(
          9
        ).element
      ),
    )
  )


def test_phase75_5_sigma_triple_prime_has_expected_type():
  data = build_phase75_5_data()

  sigma = (
    data[
      "sigma_triple_prime"
    ]
  )

  assert (
    sigma.source
    == 12
  )

  assert (
    sigma.target
    == 5
  )

  assert (
    sigma.generator
    == GeneratorSymbol(
      family="σ",
      decoration="'''",
    )
  )


def test_phase75_5_derives_pi12_5_z2():
  data = build_phase75_5_data()

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


def test_phase75_5_final_group_is_pi12_5():
  data = build_phase75_5_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=5,
    )
  )


def test_phase75_5_final_group_order_is_two():
  data = build_phase75_5_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .order
    == 2
  )


def test_phase75_5_final_generator_is_sigma_triple_prime():
  data = build_phase75_5_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "sigma_triple_prime"
    ]
  )


def test_phase75_5_final_statement_not_present_initially():
  data = build_phase75_5_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_5_hopf_injective_uses_derived_pi11_4_zero():
  data = build_phase75_5_data()

  assert (
    data[
      "pi11_4_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "hopf_injective_step"
    ].premises
    == (
      data[
        "pi11_4_zero_step"
      ],
      data[
        "e_h_exactness_step"
      ],
    )
  )

  assert (
    data[
      "hopf_injective_step"
    ].premises[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_5_rejects_given_hopf_injective_for_hopf_isomorphism():
  data = build_phase75_5_data()

  given_hopf_injective = ProofStep(
    conclusion=(
      data[
        "hopf_injective_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_prop515_pi12_5_hopf_isomorphism_inference_rule(),
    (
      given_hopf_injective,
      data[
        "h_delta_exactness_step"
      ],
      data[
        "pi12_9_step"
      ],
      data[
        "prop511_step"
      ],
      data[
        "delta_nu9_step"
      ],
      data[
        "toda55_step"
      ],
    ),
  ) is None


def test_phase75_5_reaches_fixed_point():
  data = build_phase75_5_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase75_5_sigma_triple_prime_is_unique_hopf_preimage_definition():
  data = build_phase75_5_data()

  statement = (
    data[
      "hopf_isomorphism_step"
    ].conclusion
  )

  nu_9 = (
    toda_nu_family_definition_statement(
      9
    ).element
  )

  assert (
    statement.image_generator
    == Multiple(
      coefficient=4,
      expression=nu_9,
    )
  )

  assert (
    statement.source_generator
    == data[
      "sigma_triple_prime"
    ]
  )

  assert (
    data[
      "hopf_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )


