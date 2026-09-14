from typing import (
  get_type_hints,
)

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  ScalarValue,
  TodaBracket,
  Zero,
)
from proof import (
  Relation,
  RelationType,
)
from scalar_rules import (
  OddScalarStatement,
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  TodaLemma516BracketSumContainmentStatement,
  TodaLemma516TypedSetupStatement,
  toda_lemma516_typed_setup_statement,
)


def build_phase77_2_data():
  t = ScalarSymbol(
    name="t",
  )

  m = ScalarSymbol(
    name="m",
  )

  beta = HomotopyElement(
    name="β",
    dimension=ScalarSum(
      left=t,
      right=4,
    ),
  )

  beta_membership = (
    HomotopyGroupMembershipStatement(
      element=beta,
      group_dimension=ScalarSum(
        left=t,
        right=4,
      ),
      sphere_dimension=m,
    )
  )

  nu_t_plus_4 = HomotopyElement(
    name="ν_(t+4)",
    dimension=ScalarSum(
      left=t,
      right=4,
    ),
    source=ScalarSum(
      left=t,
      right=7,
    ),
    target=ScalarSum(
      left=t,
      right=4,
    ),
    generator=GeneratorSymbol(
      family="ν",
      index=ScalarSum(
        left=t,
        right=4,
      ),
    ),
  )

  beta_nu_zero_relation = Relation(
    lhs=Composition(
      left=beta,
      right=nu_t_plus_4,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  t_range = ScalarGreaterEqualStatement(
    left=t,
    right=1,
  )

  setup = (
    toda_lemma516_typed_setup_statement(
      beta_membership=beta_membership,
      beta_nu_zero_relation=(
        beta_nu_zero_relation
      ),
      t_range=t_range,
    )
  )

  return {
    "t": t,
    "m": m,
    "beta": beta,
    "beta_membership": (
      beta_membership
    ),
    "beta_nu_zero_relation": (
      beta_nu_zero_relation
    ),
    "t_range": t_range,
    "setup": setup,
  }


def test_phase77_2_toda_bracket_index_uses_scalar_value():
  type_hints = get_type_hints(
    TodaBracket
  )

  assert (
    type_hints[
      "index"
    ]
    == ScalarValue | None
  )


def test_phase77_2_builds_typed_setup_statement():
  data = build_phase77_2_data()

  assert isinstance(
    data[
      "setup"
    ],
    TodaLemma516TypedSetupStatement,
  )


def test_phase77_2_setup_preserves_hypotheses():
  data = build_phase77_2_data()

  setup = data[
    "setup"
  ]

  assert (
    setup.beta
    == data[
      "beta"
    ]
  )

  assert (
    setup.beta_membership
    == data[
      "beta_membership"
    ]
  )

  assert (
    setup.beta_nu_zero_relation
    == data[
      "beta_nu_zero_relation"
    ]
  )

  assert (
    setup.t_range
    == data[
      "t_range"
    ]
  )

  assert (
    setup.m
    == data[
      "m"
    ]
  )

  assert (
    setup.t
    == data[
      "t"
    ]
  )


def test_phase77_2_e4_beta_has_expected_membership():
  data = build_phase77_2_data()

  setup = data[
    "setup"
  ]

  assert (
    setup.e4_beta
    == IteratedSuspension(
      expression=data[
        "beta"
      ],
      exponent=4,
    )
  )

  assert (
    setup.e4_beta_membership
    == HomotopyGroupMembershipStatement(
      element=setup.e4_beta,
      group_dimension=ScalarSum(
        left=data[
          "t"
        ],
        right=8,
      ),
      sphere_dimension=ScalarSum(
        left=data[
          "m"
        ],
        right=4,
      ),
    )
  )


def test_phase77_2_e7_beta_has_expected_membership():
  data = build_phase77_2_data()

  setup = data[
    "setup"
  ]

  assert (
    setup.e7_beta
    == IteratedSuspension(
      expression=data[
        "beta"
      ],
      exponent=7,
    )
  )

  assert (
    setup.e7_beta_membership
    == HomotopyGroupMembershipStatement(
      element=setup.e7_beta,
      group_dimension=ScalarSum(
        left=data[
          "t"
        ],
        right=11,
      ),
      sphere_dimension=ScalarSum(
        left=data[
          "m"
        ],
        right=7,
      ),
    )
  )


def test_phase77_2_first_bracket_uses_canonical_e7_beta():
  data = build_phase77_2_data()

  setup = data[
    "setup"
  ]

  bracket = (
    setup
    .first_bracket
  )

  assert (
    bracket.first
    == HomotopyElement(
      name="ν_(m+4)",
      dimension=ScalarSum(
        left=data[
          "m"
        ],
        right=4,
      ),
      source=ScalarSum(
        left=data[
          "m"
        ],
        right=7,
      ),
      target=ScalarSum(
        left=data[
          "m"
        ],
        right=4,
      ),
      generator=GeneratorSymbol(
        family="ν",
        index=ScalarSum(
          left=data[
            "m"
          ],
          right=4,
        ),
      ),
    )
  )

  assert (
    bracket.second
    == setup.e7_beta
  )

  assert (
    bracket.third
    == HomotopyElement(
      name="ν_(t+11)",
      dimension=ScalarSum(
        left=data[
          "t"
        ],
        right=11,
      ),
      source=ScalarSum(
        left=data[
          "t"
        ],
        right=14,
      ),
      target=ScalarSum(
        left=data[
          "t"
        ],
        right=11,
      ),
      generator=GeneratorSymbol(
        family="ν",
        index=ScalarSum(
          left=data[
            "t"
          ],
          right=11,
        ),
      ),
    )
  )

  assert bracket.index == 7


def test_phase77_2_first_bracket_does_not_preserve_unbound_source_n():
  data = build_phase77_2_data()

  bracket = (
    data[
      "setup"
    ]
    .first_bracket
  )

  assert isinstance(
    bracket.second,
    IteratedSuspension,
  )

  assert (
    bracket.second.exponent
    == 7
  )

  assert (
    bracket.second.exponent
    != ScalarSymbol(
      name="n",
    )
  )


def test_phase77_2_second_bracket_has_expected_structure():
  data = build_phase77_2_data()

  setup = data[
    "setup"
  ]

  bracket = (
    setup
    .second_bracket
  )

  assert (
    bracket.first
    == setup.e4_beta
  )

  assert (
    bracket.second
    == HomotopyElement(
      name="ν_(t+8)",
      dimension=ScalarSum(
        left=data[
          "t"
        ],
        right=8,
      ),
      source=ScalarSum(
        left=data[
          "t"
        ],
        right=11,
      ),
      target=ScalarSum(
        left=data[
          "t"
        ],
        right=8,
      ),
      generator=GeneratorSymbol(
        family="ν",
        index=ScalarSum(
          left=data[
            "t"
          ],
          right=8,
        ),
      ),
    )
  )

  assert (
    bracket.third
    == Multiple(
      coefficient=2,
      expression=HomotopyElement(
        name="ν_(t+11)",
        dimension=ScalarSum(
          left=data[
            "t"
          ],
          right=11,
        ),
        source=ScalarSum(
          left=data[
            "t"
          ],
          right=14,
        ),
        target=ScalarSum(
          left=data[
            "t"
          ],
          right=11,
        ),
        generator=GeneratorSymbol(
          family="ν",
          index=ScalarSum(
            left=data[
              "t"
            ],
            right=11,
          ),
        ),
      ),
    )
  )

  assert (
    bracket.index
    == ScalarSum(
      left=data[
        "t"
      ],
      right=3,
    )
  )


def test_phase77_2_bracket_sum_statement_keeps_brackets_outside_expression_ast():
  data = build_phase77_2_data()

  setup = data[
    "setup"
  ]

  x = ScalarSymbol(
    name="x",
  )

  statement = (
    TodaLemma516BracketSumContainmentStatement(
      element=setup.e4_beta,
      first_coefficient=ScalarProduct(
        left=1,
        right=x,
      ),
      first_bracket=(
        setup
        .first_bracket
      ),
      second_coefficient=ScalarProduct(
        left=-1,
        right=x,
      ),
      second_bracket=(
        setup
        .second_bracket
      ),
      odd_parameter=x,
      odd_parameter_statement=(
        OddScalarStatement(
          scalar=x,
        )
      ),
    )
  )

  assert isinstance(
    statement.first_bracket,
    TodaBracket,
  )

  assert isinstance(
    statement.second_bracket,
    TodaBracket,
  )

  assert (
    statement.odd_parameter_statement
    == OddScalarStatement(
      scalar=x,
    )
  )


def test_phase77_2_rejects_t_zero_scope():
  data = build_phase77_2_data()

  wrong_range = (
    ScalarGreaterEqualStatement(
      left=data[
        "t"
      ],
      right=0,
    )
  )

  try:
    toda_lemma516_typed_setup_statement(
      beta_membership=(
        data[
          "beta_membership"
        ]
      ),
      beta_nu_zero_relation=(
        data[
          "beta_nu_zero_relation"
        ]
      ),
      t_range=wrong_range,
    )
  except ValueError:
    pass
  else:
    raise AssertionError(
      "t>=0 must be rejected"
    )


def test_phase77_2_rejects_wrong_beta_membership_degree():
  data = build_phase77_2_data()

  wrong_membership = (
    HomotopyGroupMembershipStatement(
      element=data[
        "beta"
      ],
      group_dimension=ScalarSum(
        left=data[
          "t"
        ],
        right=5,
      ),
      sphere_dimension=data[
        "m"
      ],
    )
  )

  try:
    toda_lemma516_typed_setup_statement(
      beta_membership=wrong_membership,
      beta_nu_zero_relation=(
        data[
          "beta_nu_zero_relation"
        ]
      ),
      t_range=(
        data[
          "t_range"
        ]
      ),
    )
  except ValueError:
    pass
  else:
    raise AssertionError(
      "pi_(t+5)(S^m) must be rejected"
    )


def test_phase77_2_rejects_wrong_zero_composition():
  data = build_phase77_2_data()

  wrong_nu = HomotopyElement(
    name="ν_(t+5)",
    dimension=ScalarSum(
      left=data[
        "t"
      ],
      right=5,
    ),
    source=ScalarSum(
      left=data[
        "t"
      ],
      right=8,
    ),
    target=ScalarSum(
      left=data[
        "t"
      ],
      right=5,
    ),
    generator=GeneratorSymbol(
      family="ν",
      index=ScalarSum(
        left=data[
          "t"
        ],
        right=5,
      ),
    ),
  )

  wrong_zero = Relation(
    lhs=Composition(
      left=data[
        "beta"
      ],
      right=wrong_nu,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  try:
    toda_lemma516_typed_setup_statement(
      beta_membership=(
        data[
          "beta_membership"
        ]
      ),
      beta_nu_zero_relation=wrong_zero,
      t_range=(
        data[
          "t_range"
        ]
      ),
    )
  except ValueError:
    pass
  else:
    raise AssertionError(
      "beta nu_(t+5)=0 must be rejected"
    )


