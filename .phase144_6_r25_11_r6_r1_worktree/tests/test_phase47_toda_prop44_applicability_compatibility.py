from typing import (
  get_type_hints,
)

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  MapSymbol,
  Multiple,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaProp44DecompositionMap,
)
from map_facts import (
  EHP_H_MAP,
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
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  TodaProp44IsomorphismStatement,
  toda_prop44_isomorphism_inference_rule,
)


def build_phase47_5_data(
  i_name="i",
  n_name="n",
  alpha_name="α",
  hopf_sign=1,
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

  iota = HomotopyElement(
    name="ι_(2n-1)",
    dimension=two_n_minus_one,
    generator=GeneratorSymbol(
      family="ι",
      index=two_n_minus_one,
    ),
  )

  membership = (
    TodaPrimaryGroupMembershipStatement(
      element=alpha,
      group=TodaPrimaryGroup(
        group_dimension=two_n_minus_one,
        sphere_dimension=n,
      ),
    )
  )

  if hopf_sign == 1:
    hopf_value = iota
  else:
    hopf_value = Multiple(
      coefficient=-1,
      expression=iota,
    )

  hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=alpha,
    ),
    rhs=hopf_value,
    relation_type=RelationType.EQUALITY,
  )

  source_group = DirectSumGroup(
    summands=(
      TodaPrimaryGroup(
        group_dimension=i_minus_one,
        sphere_dimension=n_minus_one,
      ),
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=two_n_minus_one,
      ),
    ),
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
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

  return {
    "i": i,
    "n": n,
    "i_minus_one": i_minus_one,
    "n_minus_one": n_minus_one,
    "two_n_minus_one": (
      two_n_minus_one
    ),
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "iota": iota,
    "membership": membership,
    "hopf_relation": hopf_relation,
    "source_group": source_group,
    "target_group": target_group,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
  }


def build_phase47_5_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "membership"
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
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase47_5_positive_instance_derives_exactly_one_theorem():
  data = build_phase47_5_data(
    hopf_sign=1,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_isomorphism_inference_rule(),
      build_phase47_5_steps(
        data
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44IsomorphismStatement,
    )
  )

  assert len(
    derived
  ) == 1


def test_phase47_5_negative_instance_derives_exactly_one_theorem():
  data = build_phase47_5_data(
    hopf_sign=-1,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_isomorphism_inference_rule(),
      build_phase47_5_steps(
        data
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44IsomorphismStatement,
    )
  )

  assert len(
    derived
  ) == 1


def test_phase47_5_positive_instance_preserves_full_provenance():
  data = build_phase47_5_data(
    hopf_sign=1,
  )

  steps = build_phase47_5_steps(
    data
  )

  rule = (
    toda_prop44_isomorphism_inference_rule()
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
      TodaProp44IsomorphismStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )

  assert derived.premises == steps

  assert derived.inference_rule == (
    rule
  )


def test_phase47_5_negative_instance_preserves_full_provenance():
  data = build_phase47_5_data(
    hopf_sign=-1,
  )

  steps = build_phase47_5_steps(
    data
  )

  rule = (
    toda_prop44_isomorphism_inference_rule()
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
      TodaProp44IsomorphismStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )

  assert derived.premises == steps

  assert derived.inference_rule == (
    rule
  )


def test_phase47_5_valid_instance_reaches_fixed_point_in_one_round():
  data = build_phase47_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_isomorphism_inference_rule(),
      build_phase47_5_steps(
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


def test_phase47_5_rule_rejects_membership_from_different_n_instance():
  data = build_phase47_5_data()

  other = build_phase47_5_data(
    n_name="m",
  )

  steps = (
    ProofStep(
      conclusion=other[
        "membership"
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
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_5_rule_rejects_hopf_relation_from_different_n_instance():
  data = build_phase47_5_data()

  other = build_phase47_5_data(
    n_name="m",
  )

  steps = (
    ProofStep(
      conclusion=data[
        "membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_5_rule_rejects_map_from_different_n_instance():
  data = build_phase47_5_data()

  other = build_phase47_5_data(
    n_name="m",
  )

  steps = (
    ProofStep(
      conclusion=data[
        "membership"
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
      conclusion=other[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_5_rule_rejects_cross_alpha_instance():
  data = build_phase47_5_data()

  other = build_phase47_5_data(
    alpha_name="α'",
  )

  steps = (
    ProofStep(
      conclusion=data[
        "membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_5_different_i_instances_remain_distinct():
  first = build_phase47_5_data(
    i_name="i",
  )

  second = build_phase47_5_data(
    i_name="j",
  )

  first_statement = (
    TodaProp44IsomorphismStatement(
      map=first[
        "decomposition_map"
      ],
    )
  )

  second_statement = (
    TodaProp44IsomorphismStatement(
      map=second[
        "decomposition_map"
      ],
    )
  )

  assert (
    first_statement
    != second_statement
  )


def test_phase47_5_different_n_instances_remain_distinct():
  first = build_phase47_5_data(
    n_name="n",
  )

  second = build_phase47_5_data(
    n_name="m",
  )

  first_statement = (
    TodaProp44IsomorphismStatement(
      map=first[
        "decomposition_map"
      ],
    )
  )

  second_statement = (
    TodaProp44IsomorphismStatement(
      map=second[
        "decomposition_map"
      ],
    )
  )

  assert (
    first_statement
    != second_statement
  )


def test_phase47_5_different_alpha_instances_remain_distinct():
  first = build_phase47_5_data(
    alpha_name="α",
  )

  second = build_phase47_5_data(
    alpha_name="α'",
  )

  first_statement = (
    TodaProp44IsomorphismStatement(
      map=first[
        "decomposition_map"
      ],
    )
  )

  second_statement = (
    TodaProp44IsomorphismStatement(
      map=second[
        "decomposition_map"
      ],
    )
  )

  assert (
    first_statement
    != second_statement
  )


def test_phase47_5_generic_isomorphism_statement_map_remains_map_symbol():
  type_hints = get_type_hints(
    IsomorphismStatement
  )

  assert type_hints[
    "map"
  ] is MapSymbol


def test_phase47_5_generic_injective_statement_map_remains_map_symbol():
  type_hints = get_type_hints(
    InjectiveMapStatement
  )

  assert type_hints[
    "map"
  ] is MapSymbol


def test_phase47_5_prop44_map_is_not_map_symbol():
  data = build_phase47_5_data()

  assert not isinstance(
    data[
      "decomposition_map"
    ],
    MapSymbol,
  )


def test_phase47_5_prop44_theorem_is_not_generic_isomorphism():
  data = build_phase47_5_data()

  statement = (
    TodaProp44IsomorphismStatement(
      map=data[
        "decomposition_map"
      ],
    )
  )

  assert not isinstance(
    statement,
    IsomorphismStatement,
  )


def test_phase47_5_prop44_theorem_is_distinct_from_toda45_theorem():
  data = build_phase47_5_data()

  prop44_statement = (
    TodaProp44IsomorphismStatement(
      map=data[
        "decomposition_map"
      ],
    )
  )

  suspension_map = (
    TodaIteratedSuspensionMap(
      exponent=1,
      source_group=TodaPrimaryGroup(
        group_dimension=1,
        sphere_dimension=1,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=2,
        sphere_dimension=2,
      ),
    )
  )

  toda45_statement = (
    Toda45IsomorphismStatement(
      map=suspension_map,
    )
  )

  assert (
    prop44_statement
    != toda45_statement
  )


def test_phase47_5_generic_isomorphism_rule_does_not_match_prop44_theorem():
  data = build_phase47_5_data()

  theorem_step = ProofStep(
    conclusion=(
      TodaProp44IsomorphismStatement(
        map=data[
          "decomposition_map"
        ],
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    isomorphism_implies_injective_inference_rule(),
    (
      theorem_step,
    ),
  ) is None


def test_phase47_5_prop44_theorem_does_not_create_generic_injective_statement():
  data = build_phase47_5_data()

  theorem_step = ProofStep(
    conclusion=(
      TodaProp44IsomorphismStatement(
        map=data[
          "decomposition_map"
        ],
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    isomorphism_implies_injective_inference_rule(),
    (
      theorem_step,
    ),
  )

  assert match is None


def test_phase47_5_prop44_statement_has_no_generic_bridge():
  data = build_phase47_5_data()

  statement = (
    TodaProp44IsomorphismStatement(
      map=data[
        "decomposition_map"
      ],
    )
  )

  assert not hasattr(
    statement,
    "generic_map",
  )

  assert not hasattr(
    statement,
    "generic_isomorphism",
  )

  assert not hasattr(
    statement,
    "injective",
  )


def test_phase47_5_prop44_statement_has_no_e_injectivity_consequence():
  data = build_phase47_5_data()

  statement = (
    TodaProp44IsomorphismStatement(
      map=data[
        "decomposition_map"
      ],
    )
  )

  assert not hasattr(
    statement,
    "e_injective",
  )

  assert not hasattr(
    statement,
    "suspension_injective",
  )

  assert not hasattr(
    statement,
    "injective_e",
  )



