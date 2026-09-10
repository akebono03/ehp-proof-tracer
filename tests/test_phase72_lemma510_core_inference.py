from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  TodaBracket,
  Zero,
)
from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase70_pi11_6_delta_iota13 import (
  build_phase70_8_data,
)
from toda_rules import (
  TodaBracketDefinedStatement,
  TodaLemma510BracketPlusSuspensionImageStatement,
  TodaLemma510HopfBracketContainsStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
  toda_bracket_defined_by_zero_compositions_inference_rule,
  toda_eta_family_definition_statement,
  toda_lemma510_exactness_core_inference_rule,
  toda_lemma510_hopf_bracket_contains_inference_rule,
  toda_nu_family_definition_statement,
)


@lru_cache(maxsize=1)
def build_phase72_3_data():
  phase70_8 = (
    build_phase70_8_data()
  )

  delta_iota11_step = (
    phase70_8[
      "phase70_7"
    ][
      "delta_iota11_step"
    ]
  )

  hopf_delta_step = (
    phase70_8[
      "hopf_value_step"
    ]
  )

  exactness_step = (
    phase70_8[
      "e_h_exactness_step"
    ]
  )

  nu_6 = (
    toda_nu_family_definition_statement(
      6
    ).element
  )

  eta_9 = (
    toda_eta_family_definition_statement(
      9
    ).element
  )

  iota_10 = HomotopyElement(
    name="ι_10",
    dimension=10,
    generator=GeneratorSymbol(
      family="ι",
      index=10,
    ),
  )

  bracket = TodaBracket(
    first=nu_6,
    second=eta_9,
    third=Multiple(
      coefficient=2,
      expression=iota_10,
    ),
  )

  first_zero_step = ProofStep(
    conclusion=Relation(
      lhs=Composition(
        left=nu_6,
        right=eta_9,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_zero_step = ProofStep(
    conclusion=Relation(
      lhs=Composition(
        left=eta_9,
        right=Multiple(
          coefficient=2,
          expression=iota_10,
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  defined_match = find_inference_match(
    defined_rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  assert (
    defined_match
    is not None
  )

  bracket_defined_step = (
    apply_inference_match(
      defined_match
    )
  )

  hopf_bracket_rule = (
    toda_lemma510_hopf_bracket_contains_inference_rule()
  )

  hopf_bracket_match = (
    find_inference_match(
      hopf_bracket_rule,
      (
        bracket_defined_step,
        delta_iota11_step,
      ),
    )
  )

  assert (
    hopf_bracket_match
    is not None
  )

  hopf_bracket_step = (
    apply_inference_match(
      hopf_bracket_match
    )
  )

  core_rule = (
    toda_lemma510_exactness_core_inference_rule()
  )

  core_premises = (
    hopf_bracket_step,
    hopf_delta_step,
    exactness_step,
  )

  core_match = (
    find_inference_match(
      core_rule,
      core_premises,
    )
  )

  assert (
    core_match
    is not None
  )

  final_step = (
    apply_inference_match(
      core_match
    )
  )

  return {
    "phase70_8": phase70_8,
    "delta_iota11_step": (
      delta_iota11_step
    ),
    "hopf_delta_step": (
      hopf_delta_step
    ),
    "exactness_step": (
      exactness_step
    ),
    "nu_6": nu_6,
    "eta_9": eta_9,
    "iota_10": iota_10,
    "bracket": bracket,
    "first_zero_step": (
      first_zero_step
    ),
    "second_zero_step": (
      second_zero_step
    ),
    "bracket_defined_step": (
      bracket_defined_step
    ),
    "hopf_bracket_rule": (
      hopf_bracket_rule
    ),
    "hopf_bracket_step": (
      hopf_bracket_step
    ),
    "core_rule": core_rule,
    "core_premises": (
      core_premises
    ),
    "final_step": final_step,
  }


def test_phase72_3_reuses_derived_toda510():
  data = build_phase72_3_data()

  assert (
    data[
      "delta_iota11_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_3_delta_iota11_is_expected():
  data = build_phase72_3_data()

  relation = (
    data[
      "delta_iota11_step"
    ].conclusion
  )

  assert isinstance(
    relation,
    Relation,
  )

  assert (
    relation.relation_type
    == RelationType.EQUALITY
  )


def test_phase72_3_bracket_defined_is_inference():
  data = build_phase72_3_data()

  assert (
    data[
      "bracket_defined_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "bracket_defined_step"
    ].conclusion,
    TodaBracketDefinedStatement,
  )

  assert (
    data[
      "bracket_defined_step"
    ].conclusion.bracket
    == data[
      "bracket"
    ]
  )


def test_phase72_3_hopf_bracket_is_inference():
  data = build_phase72_3_data()

  step = (
    data[
      "hopf_bracket_step"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    TodaLemma510HopfBracketContainsStatement,
  )


def test_phase72_3_hopf_bracket_value_is_two_iota11():
  data = build_phase72_3_data()

  value = (
    data[
      "hopf_bracket_step"
    ].conclusion.value
  )

  assert isinstance(
    value,
    Multiple,
  )

  assert (
    value.coefficient
    == 2
  )

  assert (
    value.expression.generator
    == GeneratorSymbol(
      family="ι",
      index=11,
    )
  )


def test_phase72_3_reuses_derived_hopf_delta_iota13():
  data = build_phase72_3_data()

  assert (
    data[
      "hopf_delta_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "hopf_delta_step"
    ].conclusion,
    TodaProp27HopfInvariantUpToSignStatement,
  )


def test_phase72_3_hopf_values_agree_up_to_sign():
  data = build_phase72_3_data()

  assert (
    data[
      "hopf_bracket_step"
    ].conclusion.value
    == data[
      "hopf_delta_step"
    ].conclusion.positive_value
  )


def test_phase72_3_reuses_e_h_exactness():
  data = build_phase72_3_data()

  assert (
    data[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "exactness_step"
    ].conclusion,
    TodaProp42ExactnessStatement,
  )


def test_phase72_3_exactness_is_pi10_5_pi11_6_pi11_11():
  data = build_phase72_3_data()

  window = (
    data[
      "exactness_step"
    ].conclusion.window
  )

  assert (
    window
    == TodaEHPExactnessWindow(
      source_term=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      middle_term=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
      target_term=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=11,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    )
  )


def test_phase72_3_derives_bracket_plus_e_image():
  data = build_phase72_3_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaLemma510BracketPlusSuspensionImageStatement,
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_3_final_is_not_given():
  data = build_phase72_3_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase72_3_final_reuses_delta_iota13():
  data = build_phase72_3_data()

  assert (
    data[
      "final_step"
    ].conclusion.element
    is data[
      "hopf_delta_step"
    ].conclusion.argument
  )


def test_phase72_3_final_reuses_bracket():
  data = build_phase72_3_data()

  assert (
    data[
      "final_step"
    ].conclusion.bracket
    is data[
      "hopf_bracket_step"
    ].conclusion.bracket
  )


def test_phase72_3_final_suspension_map_is_expected():
  data = build_phase72_3_data()

  assert (
    data[
      "final_step"
    ].conclusion.suspension_map
    == TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
    )
  )


def test_phase72_3_final_uses_exact_three_dependencies():
  data = build_phase72_3_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "hopf_bracket_step"
      ],
      data[
        "hopf_delta_step"
      ],
      data[
        "exactness_step"
      ],
    )
  )


def test_phase72_3_rejects_given_delta_iota11():
  data = build_phase72_3_data()

  wrong_step = ProofStep(
    conclusion=(
      data[
        "delta_iota11_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "hopf_bracket_rule"
    ],
    (
      data[
        "bracket_defined_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase72_3_rejects_wrong_hopf_bracket_value():
  data = build_phase72_3_data()

  wrong_step = ProofStep(
    conclusion=replace(
      data[
        "hopf_bracket_step"
      ].conclusion,
      value=Multiple(
        coefficient=4,
        expression=(
          data[
            "hopf_bracket_step"
          ].conclusion.value.expression
        ),
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "core_rule"
    ],
    (
      wrong_step,
      data[
        "hopf_delta_step"
      ],
      data[
        "exactness_step"
      ],
    ),
  ) is None


def test_phase72_3_rejects_given_hopf_delta():
  data = build_phase72_3_data()

  wrong_step = ProofStep(
    conclusion=(
      data[
        "hopf_delta_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "core_rule"
    ],
    (
      data[
        "hopf_bracket_step"
      ],
      wrong_step,
      data[
        "exactness_step"
      ],
    ),
  ) is None


def test_phase72_3_rejects_wrong_exactness_window():
  data = build_phase72_3_data()

  wrong_exactness = ProofStep(
    conclusion=TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
        middle_term=TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=7,
        ),
        target_term=TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=13,
        ),
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      )
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "core_rule"
    ],
    (
      data[
        "hopf_bracket_step"
      ],
      data[
        "hopf_delta_step"
      ],
      wrong_exactness,
    ),
  ) is None


