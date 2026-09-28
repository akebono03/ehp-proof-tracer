from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  Zero,
)
from homotopy_groups import (
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase62_toda55_integration import (
  build_phase62_6_data,
)
from test_phase69_delta_iota11 import (
  build_phase69_3_data,
)
from test_phase73_513_delta_nu9 import (
  build_phase73_6a_data,
)
from toda_rules import (
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaDeltaImageUpToSignStatement,
  toda_nu_family_definition_statement,
  toda_prop511_513_delta_eta11_squared_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_6b_data():
  phase62 = (
    build_phase62_6_data()
  )

  phase69 = (
    build_phase69_3_data()
  )

  phase73_6a = (
    build_phase73_6a_data()
  )

  toda55_step = (
    phase62[
      "integration_step"
    ]
  )

  delta_iota11_step = (
    phase69[
      "final_step"
    ]
  )

  delta_nu9_step = (
    phase73_6a[
      "final_step"
    ]
  )

  eta_11 = HomotopyElement(
    name="η₁₁",
    dimension=11,
    source=12,
    target=11,
    generator=GeneratorSymbol(
      family="η",
      index=11,
    ),
  )

  eta_12 = HomotopyElement(
    name="η₁₂",
    dimension=12,
    source=13,
    target=12,
    generator=GeneratorSymbol(
      family="η",
      index=12,
    ),
  )

  eta11_squared = Composition(
    left=eta_11,
    right=eta_12,
  )

  expected_statement = Relation(
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=eta11_squared,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  rule = (
    toda_prop511_513_delta_eta11_squared_zero_inference_rule()
  )

  premise_steps = (
    delta_iota11_step,
    toda55_step,
    delta_nu9_step,
  )

  match = find_inference_match(
    rule,
    premise_steps,
  )

  assert (
    match
    is not None
  )

  final_step = (
    apply_inference_match(
      match
    )
  )

  nu5_eta8 = (
    delta_iota11_step
    .conclusion
    .rhs
  )

  nu_5 = (
    nu5_eta8.left
  )

  eta_8 = (
    nu5_eta8.right
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

  eta_10 = HomotopyElement(
    name="η₁₀",
    dimension=10,
    source=11,
    target=10,
    generator=GeneratorSymbol(
      family="η",
      index=10,
    ),
  )

  eta8_cubed = Composition(
    left=eta_8,
    right=Composition(
      left=eta_9,
      right=eta_10,
    ),
  )

  nu_8 = (
    toda_nu_family_definition_statement(
      8
    ).element
  )

  nu5_nu8 = Composition(
    left=nu_5,
    right=nu_8,
  )

  nu4_squared = (
    delta_nu9_step
    .conclusion
    .positive_value
    .expression
  )

  return {
    "phase62": phase62,
    "phase69": phase69,
    "phase73_6a": phase73_6a,
    "toda55_step": toda55_step,
    "delta_iota11_step": (
      delta_iota11_step
    ),
    "delta_nu9_step": (
      delta_nu9_step
    ),
    "eta_11": eta_11,
    "eta_12": eta_12,
    "eta11_squared": (
      eta11_squared
    ),
    "nu5_eta8": nu5_eta8,
    "nu_5": nu_5,
    "eta_8": eta_8,
    "eta_9": eta_9,
    "eta_10": eta_10,
    "eta8_cubed": eta8_cubed,
    "nu_8": nu_8,
    "nu5_nu8": nu5_nu8,
    "nu4_squared": nu4_squared,
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "match": match,
    "final_step": final_step,
  }


def test_phase73_6b_reuses_derived_toda510():
  data = build_phase73_6b_data()

  assert (
    data[
      "delta_iota11_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "delta_iota11_step"
    ].conclusion.lhs
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=(
        data[
          "phase69"
        ][
          "iota_11"
        ]
      ),
    )
  )


def test_phase73_6b_reuses_derived_toda55():
  data = build_phase73_6b_data()

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


def test_phase73_6b_reuses_derived_first_513_relation():
  data = build_phase73_6b_data()

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

  assert (
    data[
      "delta_nu9_step"
    ].conclusion.map
    == TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=12,
        sphere_dimension=9,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=4,
      ),
    )
  )


def test_phase73_6b_eta11_squared_is_composition():
  data = build_phase73_6b_data()

  assert (
    data[
      "eta11_squared"
    ]
    == Composition(
      left=data[
        "eta_11"
      ],
      right=data[
        "eta_12"
      ],
    )
  )

  assert (
    data[
      "eta11_squared"
    ].is_type_compatible()
  )


def test_phase73_6b_eta8_cube_is_right_associated():
  data = build_phase73_6b_data()

  assert (
    data[
      "eta8_cubed"
    ]
    == Composition(
      left=data[
        "eta_8"
      ],
      right=Composition(
        left=data[
          "eta_9"
        ],
        right=data[
          "eta_10"
        ],
      ),
    )
  )

  assert Composition(
    left=data[
      "eta_8"
    ],
    right=data[
      "eta_9"
    ],
  ).is_type_compatible()

  assert Composition(
    left=data[
      "eta_9"
    ],
    right=data[
      "eta_10"
    ],
  ).is_type_compatible()


def test_phase73_6b_nu5_nu8_is_type_compatible():
  data = build_phase73_6b_data()

  assert (
    data[
      "nu5_nu8"
    ]
    == Composition(
      left=data[
        "nu_5"
      ],
      right=data[
        "nu_8"
      ],
    )
  )

  assert (
    data[
      "nu5_nu8"
    ].is_type_compatible()
  )


def test_phase73_6b_first_513_value_is_twice_nu4_squared():
  data = build_phase73_6b_data()

  assert (
    data[
      "delta_nu9_step"
    ].conclusion
    .positive_value
    == Multiple(
      coefficient=2,
      expression=data[
        "nu4_squared"
      ],
    )
  )


def test_phase73_6b_rule_matches_dependencies():
  data = build_phase73_6b_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase73_6b_derives_delta_eta11_squared_zero():
  data = build_phase73_6b_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_6b_final_lhs_is_delta_eta11_squared():
  data = build_phase73_6b_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=data[
        "eta11_squared"
      ],
    )
  )


def test_phase73_6b_final_rhs_is_zero():
  data = build_phase73_6b_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs
    == Zero()
  )

  assert (
    data[
      "final_step"
    ].conclusion.relation_type
    == RelationType.ZERO
  )


def test_phase73_6b_final_uses_exact_three_dependencies():
  data = build_phase73_6b_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_iota11_step"
      ],
      data[
        "toda55_step"
      ],
      data[
        "delta_nu9_step"
      ],
    )
  )


def test_phase73_6b_rejects_given_toda510():
  data = build_phase73_6b_data()

  given = ProofStep(
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
      "rule"
    ],
    (
      given,
      data[
        "toda55_step"
      ],
      data[
        "delta_nu9_step"
      ],
    ),
  ) is None


def test_phase73_6b_rejects_given_toda55():
  data = build_phase73_6b_data()

  given = ProofStep(
    conclusion=(
      data[
        "toda55_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "delta_iota11_step"
      ],
      given,
      data[
        "delta_nu9_step"
      ],
    ),
  ) is None


def test_phase73_6b_rejects_given_first_513_relation():
  data = build_phase73_6b_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_nu9_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "delta_iota11_step"
      ],
      data[
        "toda55_step"
      ],
      given,
    ),
  ) is None


def test_phase73_6b_rejects_wrong_toda510():
  data = build_phase73_6b_data()

  wrong_iota = HomotopyElement(
    name="ι₁₀",
    dimension=10,
    generator=GeneratorSymbol(
      family="ι",
      index=10,
    ),
  )

  relation = (
    data[
      "delta_iota11_step"
    ].conclusion
  )

  wrong_relation = replace(
    relation,
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=wrong_iota,
    ),
  )

  wrong = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong,
      data[
        "toda55_step"
      ],
      data[
        "delta_nu9_step"
      ],
    ),
  ) is None


def test_phase73_6b_rejects_wrong_first_513_coefficient():
  data = build_phase73_6b_data()

  statement = (
    data[
      "delta_nu9_step"
    ].conclusion
  )

  wrong_statement = replace(
    statement,
    positive_value=Multiple(
      coefficient=4,
      expression=data[
        "nu4_squared"
      ],
    ),
  )

  wrong = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "delta_iota11_step"
      ],
      data[
        "toda55_step"
      ],
      wrong,
    ),
  ) is None


def test_phase73_6b_final_is_not_given():
  data = build_phase73_6b_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


