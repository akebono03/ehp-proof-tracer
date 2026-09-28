from typing import (
  get_type_hints,
)

from expression import (
  Expression,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  WhiteheadProduct,
)
from homotopy_groups import (
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
)
from map_facts import (
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
from toda_rules import (
  TodaHopfInvariantInjectiveStatement,
  TodaPi32Eta2DefinitionStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  toda_pi3_2_whitehead_square_up_to_sign_inference_rule,
)


def build_phase50_4a_data():
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )

  hopf_map = TodaHopfInvariantMap(
    source_group=pi_3_2,
    target_group=pi_3_3,
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

  whitehead_square = WhiteheadProduct(
    left=iota_2,
    right=iota_2,
  )

  prop27_statement = (
    TodaProp27HopfInvariantUpToSignStatement(
      argument=whitehead_square,
      positive_value=Multiple(
        coefficient=2,
        expression=iota_3,
      ),
    )
  )

  eta_2_definition = (
    TodaPi32Eta2DefinitionStatement(
      map=hopf_map,
      element=eta_2,
      image=iota_3,
    )
  )

  hopf_relation = Relation(
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

  expected = (
    TodaPi32WhiteheadSquareUpToSignStatement(
      whitehead_square=whitehead_square,
      positive_value=Multiple(
        coefficient=2,
        expression=eta_2,
      ),
    )
  )

  return {
    "pi_3_2": pi_3_2,
    "pi_3_3": pi_3_3,
    "hopf_map": hopf_map,
    "iota_2": iota_2,
    "iota_3": iota_3,
    "eta_2": eta_2,
    "whitehead_square": (
      whitehead_square
    ),
    "prop27_statement": (
      prop27_statement
    ),
    "eta_2_definition": (
      eta_2_definition
    ),
    "hopf_relation": (
      hopf_relation
    ),
    "hopf_injectivity": (
      hopf_injectivity
    ),
    "expected": expected,
  }


def build_phase50_4a_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "prop27_statement"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_2_definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_injectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase50_4a_statement_whitehead_square_uses_expression():
  type_hints = get_type_hints(
    TodaPi32WhiteheadSquareUpToSignStatement
  )

  assert type_hints[
    "whitehead_square"
  ] is Expression


def test_phase50_4a_statement_positive_value_uses_expression():
  type_hints = get_type_hints(
    TodaPi32WhiteheadSquareUpToSignStatement
  )

  assert type_hints[
    "positive_value"
  ] is Expression


def test_phase50_4a_statement_represents_expected_whitehead_square():
  data = build_phase50_4a_data()

  assert data[
    "expected"
  ].whitehead_square == (
    data[
      "whitehead_square"
    ]
  )


def test_phase50_4a_statement_represents_twice_eta_2():
  data = build_phase50_4a_data()

  assert data[
    "expected"
  ].positive_value == (
    Multiple(
      coefficient=2,
      expression=data[
        "eta_2"
      ],
    )
  )


def test_phase50_4a_rule_requires_four_premises():
  rule = (
    toda_pi3_2_whitehead_square_up_to_sign_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 4


def test_phase50_4a_valid_instance_matches():
  data = build_phase50_4a_data()

  assert find_inference_match(
    toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
    build_phase50_4a_steps(
      data
    ),
  ) is not None


def test_phase50_4a_valid_instance_derives_expected_result():
  data = build_phase50_4a_data()

  result = (
    run_inference_until_stable_with_history(
      toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
      build_phase50_4a_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "expected"
  ] in conclusions


def test_phase50_4a_wrong_hopf_injectivity_instance_is_rejected():
  data = build_phase50_4a_data()

  wrong_injectivity = (
    TodaHopfInvariantInjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=TodaPrimaryGroup(
          group_dimension=4,
          sphere_dimension=3,
        ),
        target_group=data[
          "pi_3_3"
        ],
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "prop27_statement"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_2_definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_injectivity,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
    steps,
  ) is None


def test_phase50_4a_wrong_h_eta_2_relation_is_rejected():
  data = build_phase50_4a_data()

  wrong_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=data[
        "eta_2"
      ],
    ),
    rhs=HomotopyElement(
      name="x",
      dimension=3,
      generator=GeneratorSymbol(
        family="x",
        index=3,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=data[
        "prop27_statement"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_2_definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_injectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
    steps,
  ) is None


def test_phase50_4a_wrong_prop27_value_is_rejected():
  data = build_phase50_4a_data()

  wrong_statement = (
    TodaProp27HopfInvariantUpToSignStatement(
      argument=data[
        "whitehead_square"
      ],
      positive_value=Multiple(
        coefficient=3,
        expression=data[
          "iota_3"
        ],
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_statement,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_2_definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_injectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
    steps,
  ) is None


def test_phase50_4a_missing_injectivity_is_rejected():
  data = build_phase50_4a_data()

  steps = build_phase50_4a_steps(
    data
  )[
    :3
  ]

  assert find_inference_match(
    toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
    steps,
  ) is None


def test_phase50_4a_derived_step_is_inference():
  data = build_phase50_4a_data()

  result = (
    run_inference_until_stable_with_history(
      toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
      build_phase50_4a_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaPi32WhiteheadSquareUpToSignStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )


def test_phase50_4a_derived_step_preserves_all_premises():
  data = build_phase50_4a_data()

  steps = build_phase50_4a_steps(
    data
  )

  result = (
    run_inference_until_stable_with_history(
      toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaPi32WhiteheadSquareUpToSignStatement,
    )
  )

  assert derived.premises == steps


def test_phase50_4a_reaches_fixed_point_in_one_round():
  data = build_phase50_4a_data()

  result = (
    run_inference_until_stable_with_history(
      toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
      build_phase50_4a_steps(
        data
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



