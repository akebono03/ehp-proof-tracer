from typing import (
  get_type_hints,
)

from expression import (
  MapSymbol,
  ScalarSum,
  ScalarSymbol,
  Suspension,
  HomotopyElement,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_E_MAP,
)
from map_property_rules import (
  InjectiveMapStatement,
)


def build_phase48_2_suspension_map(
  i_name="i",
  n_name="n",
):
  i = ScalarSymbol(
    name=i_name,
  )

  n = ScalarSymbol(
    name=n_name,
  )

  source_group = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=i,
      right=-1,
    ),
    sphere_dimension=ScalarSum(
      left=n,
      right=-1,
    ),
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  suspension_map = TodaSuspensionMap(
    source_group=source_group,
    target_group=target_group,
  )

  return {
    "i": i,
    "n": n,
    "source_group": source_group,
    "target_group": target_group,
    "suspension_map": suspension_map,
  }


def test_phase48_2_suspension_map_source_group_uses_toda_primary_group():
  type_hints = get_type_hints(
    TodaSuspensionMap
  )

  assert type_hints[
    "source_group"
  ] is TodaPrimaryGroup


def test_phase48_2_suspension_map_target_group_uses_toda_primary_group():
  type_hints = get_type_hints(
    TodaSuspensionMap
  )

  assert type_hints[
    "target_group"
  ] is TodaPrimaryGroup


def test_phase48_2_represents_e_from_pi_i_minus_one_n_minus_one_to_pi_i_n():
  data = build_phase48_2_suspension_map()

  assert data[
    "suspension_map"
  ] == TodaSuspensionMap(
    source_group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "i"
        ],
        right=-1,
      ),
      sphere_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=-1,
      ),
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=data[
        "i"
      ],
      sphere_dimension=data[
        "n"
      ],
    ),
  )


def test_phase48_2_suspension_map_preserves_source_group():
  data = build_phase48_2_suspension_map()

  assert data[
    "suspension_map"
  ].source_group == (
    data[
      "source_group"
    ]
  )


def test_phase48_2_suspension_map_preserves_target_group():
  data = build_phase48_2_suspension_map()

  assert data[
    "suspension_map"
  ].target_group == (
    data[
      "target_group"
    ]
  )


def test_phase48_2_same_symbolic_instance_has_structural_equality():
  first = build_phase48_2_suspension_map()

  second = build_phase48_2_suspension_map()

  assert (
    first[
      "suspension_map"
    ]
    == second[
      "suspension_map"
    ]
  )


def test_phase48_2_different_i_instance_is_structurally_distinct():
  first = build_phase48_2_suspension_map(
    i_name="i",
  )

  second = build_phase48_2_suspension_map(
    i_name="j",
  )

  assert (
    first[
      "suspension_map"
    ]
    != second[
      "suspension_map"
    ]
  )


def test_phase48_2_different_n_instance_is_structurally_distinct():
  first = build_phase48_2_suspension_map(
    n_name="n",
  )

  second = build_phase48_2_suspension_map(
    n_name="m",
  )

  assert (
    first[
      "suspension_map"
    ]
    != second[
      "suspension_map"
    ]
  )


def test_phase48_2_suspension_map_is_not_map_symbol():
  data = build_phase48_2_suspension_map()

  assert not isinstance(
    data[
      "suspension_map"
    ],
    MapSymbol,
  )


def test_phase48_2_suspension_map_is_not_canonical_e_map_symbol():
  data = build_phase48_2_suspension_map()

  assert (
    data[
      "suspension_map"
    ]
    != EHP_E_MAP
  )


def test_phase48_2_suspension_map_is_not_iterated_suspension_map():
  data = build_phase48_2_suspension_map()

  assert not isinstance(
    data[
      "suspension_map"
    ],
    TodaIteratedSuspensionMap,
  )


def test_phase48_2_iterated_suspension_map_contract_remains_unchanged():
  type_hints = get_type_hints(
    TodaIteratedSuspensionMap
  )

  assert "exponent" in type_hints

  assert type_hints[
    "source_group"
  ] is TodaPrimaryGroup

  assert type_hints[
    "target_group"
  ] is TodaPrimaryGroup


def test_phase48_2_suspension_map_is_not_element_level_suspension():
  data = build_phase48_2_suspension_map()

  beta = HomotopyElement(
    name="β",
    dimension=ScalarSum(
      left=data[
        "i"
      ],
      right=-1,
    ),
  )

  element_suspension = Suspension(
    expression=beta,
  )

  assert (
    data[
      "suspension_map"
    ]
    != element_suspension
  )

  assert not isinstance(
    data[
      "suspension_map"
    ],
    Suspension,
  )


def test_phase48_2_suspension_map_is_not_prop44_decomposition_map():
  data = build_phase48_2_suspension_map()

  source_group = DirectSumGroup(
    summands=(
      data[
        "source_group"
      ],
      TodaPrimaryGroup(
        group_dimension=data[
          "i"
        ],
        sphere_dimension=data[
          "n"
        ],
      ),
    ),
  )

  beta = HomotopyElement(
    name="β",
    dimension=ScalarSum(
      left=data[
        "i"
      ],
      right=-1,
    ),
  )

  gamma = HomotopyElement(
    name="γ",
    dimension=data[
      "i"
    ],
  )

  alpha = HomotopyElement(
    name="α",
    dimension=data[
      "i"
    ],
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=source_group,
      target_group=data[
        "target_group"
      ],
      alpha=alpha,
      beta=beta,
      gamma=gamma,
      formula=Suspension(
        expression=beta,
      ),
    )
  )

  assert not isinstance(
    data[
      "suspension_map"
    ],
    TodaProp44DecompositionMap,
  )

  assert (
    data[
      "suspension_map"
    ]
    != decomposition_map
  )


def test_phase48_2_suspension_map_does_not_assert_injectivity():
  data = build_phase48_2_suspension_map()

  suspension_map = data[
    "suspension_map"
  ]

  assert not hasattr(
    suspension_map,
    "injective",
  )

  assert not hasattr(
    suspension_map,
    "is_injective",
  )

  assert not hasattr(
    suspension_map,
    "injectivity",
  )


def test_phase48_2_suspension_map_does_not_assert_isomorphism():
  data = build_phase48_2_suspension_map()

  suspension_map = data[
    "suspension_map"
  ]

  assert not hasattr(
    suspension_map,
    "isomorphism",
  )

  assert not hasattr(
    suspension_map,
    "is_isomorphism",
  )


def test_phase48_2_suspension_map_has_no_prop44_theorem_semantics():
  data = build_phase48_2_suspension_map()

  suspension_map = data[
    "suspension_map"
  ]

  assert not hasattr(
    suspension_map,
    "toda_prop44",
  )

  assert not hasattr(
    suspension_map,
    "theorem",
  )


def test_phase48_2_suspension_map_has_no_first_summand_semantics():
  data = build_phase48_2_suspension_map()

  suspension_map = data[
    "suspension_map"
  ]

  assert not hasattr(
    suspension_map,
    "first_summand",
  )

  assert not hasattr(
    suspension_map,
    "inclusion",
  )

  assert not hasattr(
    suspension_map,
    "restriction",
  )


def test_phase48_2_suspension_map_is_distinct_from_generic_injectivity():
  data = build_phase48_2_suspension_map()

  generic_injectivity = (
    InjectiveMapStatement(
      map=EHP_E_MAP,
    )
  )

  assert (
    data[
      "suspension_map"
    ]
    != generic_injectivity
  )


def test_phase48_2_constructor_does_not_validate_suspension_dimensions():
  arbitrary_source = TodaPrimaryGroup(
    group_dimension=1,
    sphere_dimension=100,
  )

  arbitrary_target = TodaPrimaryGroup(
    group_dimension=999,
    sphere_dimension=2,
  )

  suspension_map = TodaSuspensionMap(
    source_group=arbitrary_source,
    target_group=arbitrary_target,
  )

  assert suspension_map.source_group == (
    arbitrary_source
  )

  assert suspension_map.target_group == (
    arbitrary_target
  )


def test_phase48_2_specific_map_retains_instance_lost_by_generic_e_symbol():
  first = build_phase48_2_suspension_map(
    i_name="i",
    n_name="n",
  )

  second = build_phase48_2_suspension_map(
    i_name="j",
    n_name="m",
  )

  assert (
    first[
      "suspension_map"
    ]
    != second[
      "suspension_map"
    ]
  )

  assert EHP_E_MAP == (
    EHP_E_MAP
  )


def test_phase48_2_specific_map_retains_instance_lost_by_generic_injectivity():
  first = build_phase48_2_suspension_map(
    i_name="i",
    n_name="n",
  )

  second = build_phase48_2_suspension_map(
    i_name="j",
    n_name="m",
  )

  assert (
    first[
      "suspension_map"
    ]
    != second[
      "suspension_map"
    ]
  )

  assert (
    InjectiveMapStatement(
      map=EHP_E_MAP,
    )
    == InjectiveMapStatement(
      map=EHP_E_MAP,
    )
  )



