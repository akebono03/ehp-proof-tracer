from expression import (
  GeneratorSymbol,
  HomotopyElement,
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
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  toda_45_isomorphism_inference_rule,
)


def build_phase53_2_data():
  n = ScalarSymbol(
    name="n",
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  pi_4_3 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  pi_n_plus_1_n = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=n,
      right=1,
    ),
    sphere_dimension=n,
  )

  source_relation = Relation(
    lhs=pi_4_3,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_3,
    ),
    relation_type=RelationType.EQUALITY,
  )

  transport_map = (
    TodaIteratedSuspensionMap(
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
      source_group=pi_4_3,
      target_group=pi_n_plus_1_n,
    )
  )

  isomorphism = (
    Toda45IsomorphismStatement(
      map=transport_map,
    )
  )

  transported_generator = (
    IteratedSuspension(
      expression=eta_3,
      exponent=(
        transport_map.exponent
      ),
    )
  )

  target_relation = Relation(
    lhs=pi_n_plus_1_n,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=transported_generator,
    ),
    relation_type=RelationType.EQUALITY,
  )

  return {
    "n": n,
    "eta_3": eta_3,
    "pi_4_3": pi_4_3,
    "pi_n_plus_1_n": (
      pi_n_plus_1_n
    ),
    "source_relation": (
      source_relation
    ),
    "transport_map": (
      transport_map
    ),
    "isomorphism": (
      isomorphism
    ),
    "transported_generator": (
      transported_generator
    ),
    "target_relation": (
      target_relation
    ),
  }


def build_phase53_3_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "source_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase53_2_source_relation_represents_pi4_3_eta3_group():
  data = build_phase53_2_data()

  relation = data[
    "source_relation"
  ]

  assert relation.lhs == (
    data[
      "pi_4_3"
    ]
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 2

  assert relation.rhs.generator == (
    data[
      "eta_3"
    ]
  )

  assert (
    relation.relation_type
    == RelationType.EQUALITY
  )


def test_phase53_2_transport_map_represents_e_n_minus_3():
  data = build_phase53_2_data()

  transport_map = data[
    "transport_map"
  ]

  assert (
    transport_map.exponent
    == ScalarSum(
      left=data[
        "n"
      ],
      right=ScalarProduct(
        left=-1,
        right=3,
      ),
    )
  )


def test_phase53_2_transport_map_preserves_specific_source_and_target():
  data = build_phase53_2_data()

  transport_map = data[
    "transport_map"
  ]

  assert (
    transport_map.source_group
    == data[
      "pi_4_3"
    ]
  )

  assert (
    transport_map.target_group
    == data[
      "pi_n_plus_1_n"
    ]
  )


def test_phase53_2_toda45_statement_preserves_same_transport_map():
  data = build_phase53_2_data()

  assert (
    data[
      "isomorphism"
    ].map
    == data[
      "transport_map"
    ]
  )


def test_phase53_2_target_relation_represents_transported_finite_cyclic_group():
  data = build_phase53_2_data()

  relation = data[
    "target_relation"
  ]

  assert relation.lhs == (
    data[
      "pi_n_plus_1_n"
    ]
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 2

  assert (
    relation.rhs.generator
    == data[
      "transported_generator"
    ]
  )

  assert (
    relation.relation_type
    == RelationType.EQUALITY
  )


def test_phase53_2_transported_generator_is_iterated_suspension_of_eta3():
  data = build_phase53_2_data()

  generator = (
    data[
      "target_relation"
    ].rhs.generator
  )

  assert isinstance(
    generator,
    IteratedSuspension,
  )

  assert generator.expression == (
    data[
      "eta_3"
    ]
  )

  assert generator.exponent == (
    data[
      "transport_map"
    ].exponent
  )


def test_phase53_2_target_group_is_pi_n_plus_1_n():
  data = build_phase53_2_data()

  target = data[
    "target_relation"
  ].lhs

  assert target == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=1,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase53_2_does_not_normalize_transported_generator_to_eta_n():
  data = build_phase53_2_data()

  eta_n = HomotopyElement(
    name="η_n",
    dimension=data[
      "n"
    ],
    source=ScalarSum(
      left=data[
        "n"
      ],
      right=1,
    ),
    target=data[
      "n"
    ],
    generator=GeneratorSymbol(
      family="η",
      index=data[
        "n"
      ],
    ),
  )

  assert (
    data[
      "target_relation"
    ].rhs.generator
    != eta_n
  )














def build_phase53_4_toda45_steps(
  data,
):
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
      left=data[
        "n"
      ],
      right=3,
    )
  )

  suspension_map = (
    TodaIteratedSuspensionMap(
      exponent=ScalarSum(
        left=data[
          "n"
        ],
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
      target_group=data[
        "pi_n_plus_1_n"
      ],
    )
  )

  return (
    ProofStep(
      conclusion=stable_range,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=suspension_range,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=suspension_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "source_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )
























