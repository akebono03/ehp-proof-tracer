from typing import (
  get_type_hints,
)

from expression import (
  Expression,
  GeneratorSymbol,
  HomotopyElement,
  WhiteheadProduct,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from low_dimensional_facts import (
  pi_4_5_zero_fact,
  pi_5_5_free_cyclic_fact,
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
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  toda_delta_iota5_whitehead_square_inference_rule,
)


def build_phase50_4b_data():
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )

  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_4_5 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=5,
  )

  iota_5 = HomotopyElement(
    name="ι_5",
    dimension=5,
    generator=GeneratorSymbol(
      family="ι",
      index=5,
    ),
  )

  iota_2 = HomotopyElement(
    name="ι_2",
    dimension=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  whitehead_square = WhiteheadProduct(
    left=iota_2,
    right=iota_2,
  )

  delta_map = TodaDeltaMap(
    source_group=pi_5_5,
    target_group=pi_3_2,
  )

  delta_statement = (
    TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=iota_5,
      positive_value=whitehead_square,
    )
  )

  return {
    "pi_5_5": pi_5_5,
    "pi_3_2": pi_3_2,
    "pi_4_5": pi_4_5,
    "iota_5": iota_5,
    "iota_2": iota_2,
    "whitehead_square": (
      whitehead_square
    ),
    "delta_map": delta_map,
    "delta_statement": (
      delta_statement
    ),
  }


def test_phase50_4b_pi_5_5_fact_is_equality_relation():
  fact = pi_5_5_free_cyclic_fact()

  assert isinstance(
    fact,
    Relation,
  )

  assert fact.relation_type == (
    RelationType.EQUALITY
  )


def test_phase50_4b_pi_5_5_fact_has_expected_group():
  fact = pi_5_5_free_cyclic_fact()

  assert fact.lhs == (
    TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )
  )


def test_phase50_4b_pi_5_5_fact_is_free_cyclic():
  fact = pi_5_5_free_cyclic_fact()

  assert isinstance(
    fact.rhs,
    FreeCyclicGroup,
  )


def test_phase50_4b_pi_5_5_generator_is_iota_5():
  fact = pi_5_5_free_cyclic_fact()

  assert fact.rhs.generator == (
    HomotopyElement(
      name="ι_5",
      dimension=5,
      generator=GeneratorSymbol(
        family="ι",
        index=5,
      ),
    )
  )


def test_phase50_4b_pi_4_5_fact_is_zero_group_statement():
  fact = pi_4_5_zero_fact()

  assert isinstance(
    fact,
    TodaPrimaryGroupZeroStatement,
  )


def test_phase50_4b_pi_4_5_fact_has_expected_group():
  fact = pi_4_5_zero_fact()

  assert fact.group == (
    TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=5,
    )
  )


def test_phase50_4b_low_dimensional_facts_are_distinct():
  assert (
    pi_5_5_free_cyclic_fact()
    != pi_4_5_zero_fact()
  )


def test_phase50_4b_delta_statement_map_uses_specific_delta_map():
  type_hints = get_type_hints(
    TodaDeltaImageUpToSignStatement
  )

  assert type_hints[
    "map"
  ] is TodaDeltaMap


def test_phase50_4b_delta_statement_element_uses_expression():
  type_hints = get_type_hints(
    TodaDeltaImageUpToSignStatement
  )

  assert type_hints[
    "element"
  ] is Expression


def test_phase50_4b_delta_statement_positive_value_uses_expression():
  type_hints = get_type_hints(
    TodaDeltaImageUpToSignStatement
  )

  assert type_hints[
    "positive_value"
  ] is Expression


def test_phase50_4b_delta_statement_preserves_specific_map_instance():
  data = build_phase50_4b_data()

  assert data[
    "delta_statement"
  ].map == (
    TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=5,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=3,
        sphere_dimension=2,
      ),
    )
  )


def test_phase50_4b_delta_statement_preserves_iota_5():
  data = build_phase50_4b_data()

  assert data[
    "delta_statement"
  ].element == (
    data[
      "iota_5"
    ]
  )


def test_phase50_4b_delta_statement_preserves_whitehead_square():
  data = build_phase50_4b_data()

  assert data[
    "delta_statement"
  ].positive_value == (
    data[
      "whitehead_square"
    ]
  )


def test_phase50_4b_delta_statement_is_not_sign_specific_relation():
  data = build_phase50_4b_data()

  assert not isinstance(
    data[
      "delta_statement"
    ],
    Relation,
  )


def test_phase50_4b_valid_delta_map_matches():
  data = build_phase50_4b_data()

  step = ProofStep(
    conclusion=data[
      "delta_map"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_delta_iota5_whitehead_square_inference_rule(),
    (
      step,
    ),
  ) is not None


def test_phase50_4b_valid_delta_map_derives_statement():
  data = build_phase50_4b_data()

  step = ProofStep(
    conclusion=data[
      "delta_map"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_delta_iota5_whitehead_square_inference_rule(),
      (
        step,
      ),
    )
  )

  conclusions = tuple(
    derived.conclusion
    for derived in result.steps
  )

  assert data[
    "delta_statement"
  ] in conclusions


def test_phase50_4b_wrong_delta_source_is_rejected():
  data = build_phase50_4b_data()

  wrong_map = TodaDeltaMap(
    source_group=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=5,
    ),
    target_group=data[
      "pi_3_2"
    ],
  )

  step = ProofStep(
    conclusion=wrong_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_delta_iota5_whitehead_square_inference_rule(),
    (
      step,
    ),
  ) is None


def test_phase50_4b_wrong_delta_target_is_rejected():
  data = build_phase50_4b_data()

  wrong_map = TodaDeltaMap(
    source_group=data[
      "pi_5_5"
    ],
    target_group=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    ),
  )

  step = ProofStep(
    conclusion=wrong_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_delta_iota5_whitehead_square_inference_rule(),
    (
      step,
    ),
  ) is None


def test_phase50_4b_derived_statement_is_inference():
  data = build_phase50_4b_data()

  step = ProofStep(
    conclusion=data[
      "delta_map"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_delta_iota5_whitehead_square_inference_rule(),
      (
        step,
      ),
    )
  )

  derived = next(
    derived
    for derived in result.steps
    if isinstance(
      derived.conclusion,
      TodaDeltaImageUpToSignStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )


def test_phase50_4b_derived_statement_preserves_premise():
  data = build_phase50_4b_data()

  step = ProofStep(
    conclusion=data[
      "delta_map"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_delta_iota5_whitehead_square_inference_rule(),
      (
        step,
      ),
    )
  )

  derived = next(
    derived
    for derived in result.steps
    if isinstance(
      derived.conclusion,
      TodaDeltaImageUpToSignStatement,
    )
  )

  assert derived.premises == (
    step,
  )


def test_phase50_4b_reaches_fixed_point_in_one_round():
  data = build_phase50_4b_data()

  step = ProofStep(
    conclusion=data[
      "delta_map"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_delta_iota5_whitehead_square_inference_rule(),
      (
        step,
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 1


def test_phase50_4b_low_dimensional_facts_can_be_given_steps():
  facts = (
    pi_5_5_free_cyclic_fact(),
    pi_4_5_zero_fact(),
  )

  steps = tuple(
    ProofStep(
      conclusion=fact,
      premises=(),
      rule=ProofRule.GIVEN,
    )
    for fact in facts
  )

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in steps
  )



