from typing import (
  get_type_hints,
)

from expression import (
  Expression,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  WhiteheadProduct,
)
from homotopy_groups import (
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
)


def build_phase52_2_data():
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )

  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
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

  two_eta_2 = Multiple(
    coefficient=2,
    expression=eta_2,
  )

  whitehead_square = WhiteheadProduct(
    left=iota_2,
    right=iota_2,
  )

  delta_map = TodaDeltaMap(
    source_group=pi_5_5,
    target_group=pi_3_2,
  )

  delta_two_eta_2_up_to_sign = (
    TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=iota_5,
      positive_value=two_eta_2,
    )
  )

  delta_whitehead_up_to_sign = (
    TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=iota_5,
      positive_value=whitehead_square,
    )
  )

  return {
    "pi_5_5": pi_5_5,
    "pi_3_2": pi_3_2,
    "iota_5": iota_5,
    "iota_2": iota_2,
    "eta_2": eta_2,
    "two_eta_2": two_eta_2,
    "whitehead_square": (
      whitehead_square
    ),
    "delta_map": delta_map,
    "delta_two_eta_2_up_to_sign": (
      delta_two_eta_2_up_to_sign
    ),
    "delta_whitehead_up_to_sign": (
      delta_whitehead_up_to_sign
    ),
  }


def test_phase52_2_statement_uses_specific_delta_map():
  type_hints = get_type_hints(
    TodaDeltaImageUpToSignStatement
  )

  assert type_hints[
    "map"
  ] is TodaDeltaMap

  data = build_phase52_2_data()

  assert (
    data[
      "delta_two_eta_2_up_to_sign"
    ].map
    == data[
      "delta_map"
    ]
  )

  assert (
    data[
      "delta_map"
    ].source_group
    == data[
      "pi_5_5"
    ]
  )

  assert (
    data[
      "delta_map"
    ].target_group
    == data[
      "pi_3_2"
    ]
  )


def test_phase52_2_statement_preserves_iota5_element():
  type_hints = get_type_hints(
    TodaDeltaImageUpToSignStatement
  )

  assert type_hints[
    "element"
  ] is Expression

  data = build_phase52_2_data()

  assert (
    data[
      "delta_two_eta_2_up_to_sign"
    ].element
    == data[
      "iota_5"
    ]
  )


def test_phase52_2_statement_preserves_two_eta2_positive_value():
  type_hints = get_type_hints(
    TodaDeltaImageUpToSignStatement
  )

  assert type_hints[
    "positive_value"
  ] is Expression

  data = build_phase52_2_data()

  statement = data[
    "delta_two_eta_2_up_to_sign"
  ]

  assert (
    statement.positive_value
    == data[
      "two_eta_2"
    ]
  )

  assert isinstance(
    statement.positive_value,
    Multiple,
  )

  assert (
    statement
    .positive_value
    .coefficient
    == 2
  )

  assert (
    statement
    .positive_value
    .expression
    == data[
      "eta_2"
    ]
  )


def test_phase52_2_statement_is_structurally_distinct_from_whitehead_version():
  data = build_phase52_2_data()

  assert (
    data[
      "delta_two_eta_2_up_to_sign"
    ]
    != data[
      "delta_whitehead_up_to_sign"
    ]
  )

  assert (
    data[
      "delta_two_eta_2_up_to_sign"
    ].positive_value
    != data[
      "whitehead_square"
    ]
  )


def test_phase52_2_statement_does_not_encode_a_sign_choice():
  data = build_phase52_2_data()

  statement = data[
    "delta_two_eta_2_up_to_sign"
  ]

  negative_two_eta_2 = Multiple(
    coefficient=-2,
    expression=data[
      "eta_2"
    ],
  )

  sign_specific_negative_statement = (
    TodaDeltaImageUpToSignStatement(
      map=data[
        "delta_map"
      ],
      element=data[
        "iota_5"
      ],
      positive_value=negative_two_eta_2,
    )
  )

  assert (
    statement
    != sign_specific_negative_statement
  )

  assert (
    statement.positive_value
    == data[
      "two_eta_2"
    ]
  )


