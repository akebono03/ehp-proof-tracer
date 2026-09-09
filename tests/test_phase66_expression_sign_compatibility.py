from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Sum,
  Suspension,
)
from homotopy_groups import (
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from test_phase65_pi7_4_decomposition import (
  build_phase65_5_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
)


@lru_cache(maxsize=1)
def build_phase66_2_data():
  phase65_5 = (
    build_phase65_5_data()
  )

  nu_4 = (
    phase65_5[
      "nu_4"
    ]
  )

  nu_prime = (
    phase65_5[
      "nu_prime"
    ]
  )

  e_nu_prime = (
    phase65_5[
      "e_nu_prime"
    ]
  )

  two_nu_4 = Multiple(
    coefficient=2,
    expression=nu_4,
  )

  minus_e_nu_prime = Multiple(
    coefficient=-1,
    expression=e_nu_prime,
  )

  two_nu_4_minus_e_nu_prime = Sum(
    left=two_nu_4,
    right=minus_e_nu_prime,
  )

  pi_9_9 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=9,
  )

  pi_7_4 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=4,
  )

  delta_map = TodaDeltaMap(
    source_group=pi_9_9,
    target_group=pi_7_4,
  )

  iota_9 = HomotopyElement(
    name="ι_9",
    dimension=9,
    generator=GeneratorSymbol(
      family="ι",
      index=9,
    ),
  )

  up_to_sign_statement = (
    TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=iota_9,
      positive_value=(
        two_nu_4_minus_e_nu_prime
      ),
    )
  )

  return {
    "phase65_5": phase65_5,
    "nu_4": nu_4,
    "nu_prime": nu_prime,
    "e_nu_prime": e_nu_prime,
    "two_nu_4": two_nu_4,
    "minus_e_nu_prime": (
      minus_e_nu_prime
    ),
    "expression": (
      two_nu_4_minus_e_nu_prime
    ),
    "pi_9_9": pi_9_9,
    "pi_7_4": pi_7_4,
    "delta_map": delta_map,
    "iota_9": iota_9,
    "up_to_sign_statement": (
      up_to_sign_statement
    ),
  }


def test_phase66_2_reuses_phase65_nu4():
  data = build_phase66_2_data()

  assert (
    data[
      "nu_4"
    ]
    is data[
      "phase65_5"
    ][
      "nu_4"
    ]
  )


def test_phase66_2_reuses_phase65_nu_prime():
  data = build_phase66_2_data()

  assert (
    data[
      "nu_prime"
    ]
    is data[
      "phase65_5"
    ][
      "nu_prime"
    ]
  )


def test_phase66_2_reuses_phase65_e_nu_prime():
  data = build_phase66_2_data()

  assert (
    data[
      "e_nu_prime"
    ]
    is data[
      "phase65_5"
    ][
      "e_nu_prime"
    ]
  )

  assert (
    data[
      "e_nu_prime"
    ]
    == Suspension(
      expression=data[
        "nu_prime"
      ],
    )
  )


def test_phase66_2_two_nu4_is_multiple():
  data = build_phase66_2_data()

  assert (
    data[
      "two_nu_4"
    ]
    == Multiple(
      coefficient=2,
      expression=data[
        "nu_4"
      ],
    )
  )


def test_phase66_2_minus_e_nu_prime_is_negative_multiple():
  data = build_phase66_2_data()

  assert (
    data[
      "minus_e_nu_prime"
    ]
    == Multiple(
      coefficient=-1,
      expression=data[
        "e_nu_prime"
      ],
    )
  )


def test_phase66_2_expression_is_sum_of_two_terms():
  data = build_phase66_2_data()

  assert (
    data[
      "expression"
    ]
    == Sum(
      left=Multiple(
        coefficient=2,
        expression=data[
          "nu_4"
        ],
      ),
      right=Multiple(
        coefficient=-1,
        expression=Suspension(
          expression=data[
            "nu_prime"
          ],
        ),
      ),
    )
  )


def test_phase66_2_expression_preserves_subtraction_structure():
  data = build_phase66_2_data()

  expression = data[
    "expression"
  ]

  assert isinstance(
    expression,
    Sum,
  )

  assert isinstance(
    expression.right,
    Multiple,
  )

  assert expression.right.coefficient == -1

  assert (
    expression.right.expression
    == data[
      "e_nu_prime"
    ]
  )


def test_phase66_2_nu4_has_expected_typing():
  data = build_phase66_2_data()

  assert data[
    "nu_4"
  ].source == 7

  assert data[
    "nu_4"
  ].target == 4


def test_phase66_2_nu_prime_has_expected_typing():
  data = build_phase66_2_data()

  assert data[
    "nu_prime"
  ].source == 6

  assert data[
    "nu_prime"
  ].target == 3


def test_phase66_2_delta_map_has_equation58_groups():
  data = build_phase66_2_data()

  assert (
    data[
      "delta_map"
    ].source_group
    == TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=9,
    )
  )

  assert (
    data[
      "delta_map"
    ].target_group
    == TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    )
  )


def test_phase66_2_up_to_sign_statement_accepts_composite_value():
  data = build_phase66_2_data()

  statement = data[
    "up_to_sign_statement"
  ]

  assert isinstance(
    statement,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    statement.positive_value
    == data[
      "expression"
    ]
  )


def test_phase66_2_up_to_sign_statement_preserves_delta_instance():
  data = build_phase66_2_data()

  statement = data[
    "up_to_sign_statement"
  ]

  assert (
    statement.map
    == data[
      "delta_map"
    ]
  )

  assert (
    statement.element
    == data[
      "iota_9"
    ]
  )


