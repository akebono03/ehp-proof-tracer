from typing import (
  get_type_hints,
)

from expression import (
  Composition,
  HomotopyElement,
  MapSymbol,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_E_MAP,
)
from map_property_rules import (
  InjectiveMapStatement,
  IsomorphismStatement,
  isomorphism_implies_injective_inference_rule,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaProp44FirstSummandRestrictionStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SuspensionInjectiveStatement,
  toda_prop44_suspension_injective_inference_rule,
)


def build_phase48_4_data(
  i_name="i",
  n_name="n",
  alpha_name="α",
):
  i = ScalarSymbol(
    name=i_name,
  )

  n = ScalarSymbol(
    name=n_name,
  )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  first_summand = TodaPrimaryGroup(
    group_dimension=i_minus_one,
    sphere_dimension=n_minus_one,
  )

  second_summand = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=two_n_minus_one,
  )

  source_group = DirectSumGroup(
    summands=(
      first_summand,
      second_summand,
    ),
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  alpha = HomotopyElement(
    name=alpha_name,
    dimension=two_n_minus_one,
  )

  beta = HomotopyElement(
    name="β",
    dimension=i_minus_one,
  )

  gamma = HomotopyElement(
    name="γ",
    dimension=i,
  )

  formula = Sum(
    left=Suspension(
      expression=beta,
    ),
    right=Composition(
      left=alpha,
      right=gamma,
    ),
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=source_group,
      target_group=target_group,
      alpha=alpha,
      beta=beta,
      gamma=gamma,
      formula=formula,
    )
  )

  suspension_map = TodaSuspensionMap(
    source_group=first_summand,
    target_group=target_group,
  )

  isomorphism = (
    TodaProp44IsomorphismStatement(
      map=decomposition_map,
    )
  )

  restriction = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=decomposition_map,
      suspension_map=suspension_map,
    )
  )

  return {
    "i": i,
    "n": n,
    "i_minus_one": i_minus_one,
    "n_minus_one": n_minus_one,
    "two_n_minus_one": (
      two_n_minus_one
    ),
    "first_summand": first_summand,
    "second_summand": second_summand,
    "source_group": source_group,
    "target_group": target_group,
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
    "suspension_map": suspension_map,
    "isomorphism": isomorphism,
    "restriction": restriction,
  }


def build_phase48_4_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "restriction"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase48_4_injective_statement_map_type():
  type_hints = get_type_hints(
    TodaProp44SuspensionInjectiveStatement
  )

  assert type_hints[
    "map"
  ] is TodaSuspensionMap


def test_phase48_4_injective_statement_preserves_specific_suspension_map():
  data = build_phase48_4_data()

  statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=data[
        "suspension_map"
      ],
    )
  )

  assert statement.map == (
    data[
      "suspension_map"
    ]
  )


def test_phase48_4_injective_statement_preserves_source_instance():
  data = build_phase48_4_data()

  statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=data[
        "suspension_map"
      ],
    )
  )

  assert statement.map.source_group == (
    data[
      "first_summand"
    ]
  )


def test_phase48_4_injective_statement_preserves_target_instance():
  data = build_phase48_4_data()

  statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=data[
        "suspension_map"
      ],
    )
  )

  assert statement.map.target_group == (
    data[
      "target_group"
    ]
  )


def test_phase48_4_different_i_instances_are_distinct():
  first = build_phase48_4_data(
    i_name="i",
  )

  second = build_phase48_4_data(
    i_name="j",
  )

  first_statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=first[
        "suspension_map"
      ],
    )
  )

  second_statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=second[
        "suspension_map"
      ],
    )
  )

  assert (
    first_statement
    != second_statement
  )


def test_phase48_4_different_n_instances_are_distinct():
  first = build_phase48_4_data(
    n_name="n",
  )

  second = build_phase48_4_data(
    n_name="m",
  )

  first_statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=first[
        "suspension_map"
      ],
    )
  )

  second_statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=second[
        "suspension_map"
      ],
    )
  )

  assert (
    first_statement
    != second_statement
  )


def test_phase48_4_statement_is_not_generic_injective_statement():
  data = build_phase48_4_data()

  statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=data[
        "suspension_map"
      ],
    )
  )

  assert not isinstance(
    statement,
    InjectiveMapStatement,
  )


def test_phase48_4_statement_is_not_generic_isomorphism_statement():
  data = build_phase48_4_data()

  statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=data[
        "suspension_map"
      ],
    )
  )

  assert not isinstance(
    statement,
    IsomorphismStatement,
  )


def test_phase48_4_statement_is_not_decomposition_isomorphism_statement():
  data = build_phase48_4_data()

  statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=data[
        "suspension_map"
      ],
    )
  )

  assert (
    statement
    != data[
      "isomorphism"
    ]
  )


def test_phase48_4_rule_requires_isomorphism_and_restriction():
  rule = (
    toda_prop44_suspension_injective_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 2

  assert (
    rule.premise_patterns[
      0
    ].statement_type
    is TodaProp44IsomorphismStatement
  )

  assert (
    rule.premise_patterns[
      1
    ].statement_type
    is TodaProp44FirstSummandRestrictionStatement
  )


def test_phase48_4_rule_matches_valid_instance():
  data = build_phase48_4_data()

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    build_phase48_4_steps(
      data
    ),
  ) is not None


def test_phase48_4_rule_derives_specific_e_injectivity():
  data = build_phase48_4_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_suspension_injective_inference_rule(),
      build_phase48_4_steps(
        data
      ),
    )
  )

  expected = (
    TodaProp44SuspensionInjectiveStatement(
      map=data[
        "suspension_map"
      ],
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase48_4_valid_instance_derives_exactly_one_injectivity_statement():
  data = build_phase48_4_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_suspension_injective_inference_rule(),
      build_phase48_4_steps(
        data
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44SuspensionInjectiveStatement,
    )
  )

  assert len(
    derived
  ) == 1


def test_phase48_4_derived_statement_preserves_provenance():
  data = build_phase48_4_data()

  steps = build_phase48_4_steps(
    data
  )

  rule = (
    toda_prop44_suspension_injective_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44SuspensionInjectiveStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )

  assert derived.premises == steps

  assert derived.inference_rule == (
    rule
  )


def test_phase48_4_valid_instance_reaches_fixed_point_in_one_round():
  data = build_phase48_4_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_suspension_injective_inference_rule(),
      build_phase48_4_steps(
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


def test_phase48_4_rule_rejects_missing_isomorphism():
  data = build_phase48_4_data()

  steps = build_phase48_4_steps(
    data
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    (
      steps[
        1
      ],
    ),
  ) is None


def test_phase48_4_rule_rejects_missing_restriction():
  data = build_phase48_4_data()

  steps = build_phase48_4_steps(
    data
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    (
      steps[
        0
      ],
    ),
  ) is None


def test_phase48_4_rule_rejects_different_decomposition_map_instance():
  data = build_phase48_4_data()

  other = build_phase48_4_data(
    i_name="j",
  )

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other[
        "restriction"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_4_rule_rejects_cross_n_instance():
  data = build_phase48_4_data(
    n_name="n",
  )

  other = build_phase48_4_data(
    n_name="m",
  )

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other[
        "restriction"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_4_rule_rejects_cross_alpha_instance():
  data = build_phase48_4_data(
    alpha_name="α",
  )

  other = build_phase48_4_data(
    alpha_name="α'",
  )

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other[
        "restriction"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_4_rule_rejects_wrong_suspension_source():
  data = build_phase48_4_data()

  wrong_suspension = TodaSuspensionMap(
    source_group=data[
      "second_summand"
    ],
    target_group=data[
      "target_group"
    ],
  )

  wrong_restriction = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=wrong_suspension,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_restriction,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_4_rule_rejects_wrong_suspension_target():
  data = build_phase48_4_data()

  wrong_target = TodaPrimaryGroup(
    group_dimension=ScalarSymbol(
      name="j",
    ),
    sphere_dimension=data[
      "n"
    ],
  )

  wrong_suspension = TodaSuspensionMap(
    source_group=data[
      "first_summand"
    ],
    target_group=wrong_target,
  )

  wrong_restriction = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=wrong_suspension,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_restriction,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_4_generic_isomorphism_rule_does_not_match_specific_toda_isomorphism():
  data = build_phase48_4_data()

  step = ProofStep(
    conclusion=data[
      "isomorphism"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    isomorphism_implies_injective_inference_rule(),
    (
      step,
    ),
  ) is None


def test_phase48_4_specific_e_injectivity_does_not_create_generic_injectivity():
  data = build_phase48_4_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_suspension_injective_inference_rule(),
      build_phase48_4_steps(
        data
      ),
    )
  )

  generic_injectivity = (
    InjectiveMapStatement(
      map=EHP_E_MAP,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert (
    generic_injectivity
    not in conclusions
  )


def test_phase48_4_specific_e_injectivity_map_is_not_map_symbol():
  data = build_phase48_4_data()

  statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=data[
        "suspension_map"
      ],
    )
  )

  assert not isinstance(
    statement.map,
    MapSymbol,
  )


def test_phase48_4_statement_has_no_generic_bridge():
  data = build_phase48_4_data()

  statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=data[
        "suspension_map"
      ],
    )
  )

  assert not hasattr(
    statement,
    "generic_injectivity",
  )

  assert not hasattr(
    statement,
    "injective_map_statement",
  )

  assert not hasattr(
    statement,
    "generic_map",
  )



