from typing import (
  get_type_hints,
)

import scalar_rules

from expression import (
  HomotopyElement,
  IteratedSuspension,
  MapSymbol,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  ScalarValue,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from map_facts import (
  MapTypingFact,
)
from map_property_rules import (
  IsomorphismStatement,
)


def build_phase46_1_symbolic_data():
  n = ScalarSymbol(
    name="n",
  )

  k = ScalarSymbol(
    name="k",
  )

  m = ScalarSymbol(
    name="m",
  )

  n_plus_k = ScalarSum(
    left=n,
    right=k,
  )

  m_plus_k = ScalarSum(
    left=m,
    right=k,
  )

  m_minus_n = ScalarSum(
    left=m,
    right=ScalarProduct(
      left=-1,
      right=n,
    ),
  )

  source_group = TodaPrimaryGroup(
    group_dimension=n_plus_k,
    sphere_dimension=n,
  )

  target_group = TodaPrimaryGroup(
    group_dimension=m_plus_k,
    sphere_dimension=m,
  )

  return {
    "n": n,
    "k": k,
    "m": m,
    "n_plus_k": n_plus_k,
    "m_plus_k": m_plus_k,
    "m_minus_n": m_minus_n,
    "source_group": source_group,
    "target_group": target_group,
  }


def test_phase46_1_scalar_value_accepts_symbolic_difference_tree():
  data = build_phase46_1_symbolic_data()

  type_hints = get_type_hints(
    IteratedSuspension
  )

  assert type_hints[
    "exponent"
  ] == ScalarValue

  assert data[
    "m_minus_n"
  ] == ScalarSum(
    left=ScalarSymbol(
      name="m",
    ),
    right=ScalarProduct(
      left=-1,
      right=ScalarSymbol(
        name="n",
      ),
    ),
  )


def test_phase46_1_n_plus_k_is_losslessly_representable():
  data = build_phase46_1_symbolic_data()

  assert data[
    "n_plus_k"
  ] == ScalarSum(
    left=data[
      "n"
    ],
    right=data[
      "k"
    ],
  )


def test_phase46_1_m_plus_k_is_losslessly_representable():
  data = build_phase46_1_symbolic_data()

  assert data[
    "m_plus_k"
  ] == ScalarSum(
    left=data[
      "m"
    ],
    right=data[
      "k"
    ],
  )


def test_phase46_1_m_minus_n_is_losslessly_representable():
  data = build_phase46_1_symbolic_data()

  assert data[
    "m_minus_n"
  ] == ScalarSum(
    left=data[
      "m"
    ],
    right=ScalarProduct(
      left=-1,
      right=data[
        "n"
      ],
    ),
  )


def test_phase46_1_source_toda_group_is_losslessly_representable():
  data = build_phase46_1_symbolic_data()

  assert data[
    "source_group"
  ] == TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=data[
        "n"
      ],
      right=data[
        "k"
      ],
    ),
    sphere_dimension=data[
      "n"
    ],
  )


def test_phase46_1_target_toda_group_is_losslessly_representable():
  data = build_phase46_1_symbolic_data()

  assert data[
    "target_group"
  ] == TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=data[
        "m"
      ],
      right=data[
        "k"
      ],
    ),
    sphere_dimension=data[
      "m"
    ],
  )


def test_phase46_1_source_and_target_toda_groups_are_structurally_distinct():
  data = build_phase46_1_symbolic_data()

  assert (
    data[
      "source_group"
    ]
    != data[
      "target_group"
    ]
  )


def test_phase46_1_iterated_suspension_accepts_m_minus_n_exponent():
  data = build_phase46_1_symbolic_data()

  alpha = HomotopyElement(
    name="α",
    dimension=data[
      "n_plus_k"
    ],
  )

  suspension = IteratedSuspension(
    expression=alpha,
    exponent=data[
      "m_minus_n"
    ],
  )

  assert suspension.expression == alpha

  assert suspension.exponent == (
    data[
      "m_minus_n"
    ]
  )


def test_phase46_1_iterated_suspension_is_element_level_expression():
  data = build_phase46_1_symbolic_data()

  alpha = HomotopyElement(
    name="α",
    dimension=data[
      "n_plus_k"
    ],
  )

  suspension = IteratedSuspension(
    expression=alpha,
    exponent=data[
      "m_minus_n"
    ],
  )

  assert not isinstance(
    suspension,
    MapSymbol,
  )

  assert not hasattr(
    suspension,
    "source_group",
  )

  assert not hasattr(
    suspension,
    "target_group",
  )


def test_phase46_1_isomorphism_statement_accepts_map_symbol():
  map_symbol = MapSymbol(
    name="f",
  )

  statement = IsomorphismStatement(
    map=map_symbol,
  )

  assert statement.map == map_symbol


def test_phase46_1_isomorphism_statement_stores_only_map_identity():
  statement = IsomorphismStatement(
    map=MapSymbol(
      name="f",
    ),
  )

  assert not hasattr(
    statement,
    "source_group",
  )

  assert not hasattr(
    statement,
    "target_group",
  )

  assert not hasattr(
    statement,
    "domain",
  )

  assert not hasattr(
    statement,
    "codomain",
  )

  assert not hasattr(
    statement,
    "exponent",
  )


def test_phase46_1_same_map_symbol_isomorphism_collides_across_group_instances():
  data = build_phase46_1_symbolic_data()

  first = IsomorphismStatement(
    map=MapSymbol(
      name="E",
    ),
  )

  second = IsomorphismStatement(
    map=MapSymbol(
      name="E",
    ),
  )

  assert first == second

  assert (
    data[
      "source_group"
    ]
    != data[
      "target_group"
    ]
  )


def test_phase46_1_map_typing_fact_remains_concrete_dimension_only():
  type_hints = get_type_hints(
    MapTypingFact
  )

  assert type_hints[
    "source_group_dimension"
  ] is int

  assert type_hints[
    "source_sphere_dimension"
  ] is int

  assert type_hints[
    "target_group_dimension"
  ] is int

  assert type_hints[
    "target_sphere_dimension"
  ] is int


def test_phase46_1_map_typing_fact_does_not_accept_toda_group_terms_as_fields():
  type_hints = get_type_hints(
    MapTypingFact
  )

  assert "source_group" not in (
    type_hints
  )

  assert "target_group" not in (
    type_hints
  )


def test_phase46_1_current_scalar_rules_do_not_encode_stable_range_premises():
  assert not hasattr(
    scalar_rules,
    "StableRangeStatement",
  )

  assert not hasattr(
    scalar_rules,
    "TodaStableRangeStatement",
  )


def test_phase46_1_toda_group_has_no_isomorphism_semantics():
  data = build_phase46_1_symbolic_data()

  for group in (
    data[
      "source_group"
    ],
    data[
      "target_group"
    ],
  ):
    assert not hasattr(
      group,
      "is_isomorphic",
    )

    assert not hasattr(
      group,
      "isomorphism",
    )

    assert not hasattr(
      group,
      "map",
    )


def test_phase46_1_current_objects_do_not_encode_toda_45_theorem():
  data = build_phase46_1_symbolic_data()

  values = (
    data[
      "source_group"
    ],
    data[
      "target_group"
    ],
    IteratedSuspension(
      expression=HomotopyElement(
        name="α",
        dimension=data[
          "n_plus_k"
        ],
      ),
      exponent=data[
        "m_minus_n"
      ],
    ),
    IsomorphismStatement(
      map=MapSymbol(
        name="E",
      ),
    ),
  )

  for value in values:
    assert not hasattr(
      value,
      "toda_4_5",
    )

    assert not hasattr(
      value,
      "theorem",
    )
