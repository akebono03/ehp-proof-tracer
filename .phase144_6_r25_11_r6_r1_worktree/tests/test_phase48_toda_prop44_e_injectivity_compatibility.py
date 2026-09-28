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
)
from map_facts import (
  EHP_E_MAP,
)
from map_property_rules import (
  InjectiveMapStatement,
  IsomorphismStatement,
)
from toda_rules import (
  TodaProp44IsomorphismStatement,
)


def build_phase48_1_data(
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

  theorem = (
    TodaProp44IsomorphismStatement(
      map=decomposition_map,
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
    "theorem": theorem,
  }


def test_phase48_1_canonical_e_map_is_map_symbol():
  assert isinstance(
    EHP_E_MAP,
    MapSymbol,
  )

  assert EHP_E_MAP == MapSymbol(
    name="E",
  )


def test_phase48_1_generic_injective_statement_accepts_canonical_e():
  statement = InjectiveMapStatement(
    map=EHP_E_MAP,
  )

  assert statement.map == (
    EHP_E_MAP
  )


def test_phase48_1_generic_injective_statement_map_type_remains_map_symbol():
  type_hints = get_type_hints(
    InjectiveMapStatement
  )

  assert type_hints[
    "map"
  ] is MapSymbol


def test_phase48_1_generic_isomorphism_statement_map_type_remains_map_symbol():
  type_hints = get_type_hints(
    IsomorphismStatement
  )

  assert type_hints[
    "map"
  ] is MapSymbol


def test_phase48_1_generic_e_injectivity_has_no_source_group():
  statement = InjectiveMapStatement(
    map=EHP_E_MAP,
  )

  assert not hasattr(
    statement,
    "source_group",
  )


def test_phase48_1_generic_e_injectivity_has_no_target_group():
  statement = InjectiveMapStatement(
    map=EHP_E_MAP,
  )

  assert not hasattr(
    statement,
    "target_group",
  )


def test_phase48_1_generic_e_injectivity_has_no_symbolic_i_instance():
  statement = InjectiveMapStatement(
    map=EHP_E_MAP,
  )

  assert not hasattr(
    statement,
    "i",
  )

  assert not hasattr(
    statement,
    "group_dimension",
  )


def test_phase48_1_generic_e_injectivity_has_no_symbolic_n_instance():
  statement = InjectiveMapStatement(
    map=EHP_E_MAP,
  )

  assert not hasattr(
    statement,
    "n",
  )

  assert not hasattr(
    statement,
    "sphere_dimension",
  )


def test_phase48_1_generic_e_injectivity_collides_across_symbolic_instances():
  first = build_phase48_1_data(
    i_name="i",
    n_name="n",
  )

  second = build_phase48_1_data(
    i_name="j",
    n_name="m",
  )

  assert (
    first[
      "first_summand"
    ]
    != second[
      "first_summand"
    ]
  )

  assert (
    first[
      "target_group"
    ]
    != second[
      "target_group"
    ]
  )

  first_injectivity = (
    InjectiveMapStatement(
      map=EHP_E_MAP,
    )
  )

  second_injectivity = (
    InjectiveMapStatement(
      map=EHP_E_MAP,
    )
  )

  assert (
    first_injectivity
    == second_injectivity
  )


def test_phase48_1_prop44_theorem_preserves_specific_decomposition_instance():
  data = build_phase48_1_data()

  assert data[
    "theorem"
  ].map == data[
    "decomposition_map"
  ]

  assert data[
    "theorem"
  ].map.source_group == (
    data[
      "source_group"
    ]
  )

  assert data[
    "theorem"
  ].map.target_group == (
    data[
      "target_group"
    ]
  )


def test_phase48_1_prop44_theorem_preserves_first_summand_instance():
  data = build_phase48_1_data()

  first_summand = (
    data[
      "theorem"
    ].map.source_group.summands[
      0
    ]
  )

  assert first_summand == (
    TodaPrimaryGroup(
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
    )
  )


def test_phase48_1_prop44_theorem_preserves_target_instance():
  data = build_phase48_1_data()

  assert data[
    "theorem"
  ].map.target_group == (
    TodaPrimaryGroup(
      group_dimension=data[
        "i"
      ],
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase48_1_first_summand_and_target_determine_required_e_instance():
  data = build_phase48_1_data()

  source = (
    data[
      "decomposition_map"
    ].source_group.summands[
      0
    ]
  )

  target = (
    data[
      "decomposition_map"
    ].target_group
  )

  assert source == (
    data[
      "first_summand"
    ]
  )

  assert target == (
    data[
      "target_group"
    ]
  )

  assert source == TodaPrimaryGroup(
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
  )

  assert target == TodaPrimaryGroup(
    group_dimension=data[
      "i"
    ],
    sphere_dimension=data[
      "n"
    ],
  )


def test_phase48_1_prop44_formula_first_term_is_element_level_suspension():
  data = build_phase48_1_data()

  formula = data[
    "decomposition_map"
  ].formula

  assert isinstance(
    formula,
    Sum,
  )

  assert isinstance(
    formula.left,
    Suspension,
  )

  assert formula.left.expression == (
    data[
      "beta"
    ]
  )


def test_phase48_1_element_level_suspension_is_not_map_symbol():
  data = build_phase48_1_data()

  suspension = data[
    "decomposition_map"
  ].formula.left

  assert isinstance(
    suspension,
    Suspension,
  )

  assert not isinstance(
    suspension,
    MapSymbol,
  )


def test_phase48_1_prop44_decomposition_map_is_not_canonical_e_map():
  data = build_phase48_1_data()

  assert (
    data[
      "decomposition_map"
    ]
    != EHP_E_MAP
  )

  assert not isinstance(
    data[
      "decomposition_map"
    ],
    MapSymbol,
  )


def test_phase48_1_prop44_isomorphism_is_not_generic_e_injectivity():
  data = build_phase48_1_data()

  generic_injectivity = (
    InjectiveMapStatement(
      map=EHP_E_MAP,
    )
  )

  assert (
    data[
      "theorem"
    ]
    != generic_injectivity
  )


def test_phase48_1_decomposition_isomorphism_does_not_mean_e_isomorphism():
  data = build_phase48_1_data()

  e_isomorphism = IsomorphismStatement(
    map=EHP_E_MAP,
  )

  assert (
    data[
      "theorem"
    ]
    != e_isomorphism
  )


def test_phase48_1_prop44_theorem_has_no_existing_e_injectivity_projection():
  data = build_phase48_1_data()

  statement = data[
    "theorem"
  ]

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


def test_phase48_1_prop44_map_has_no_first_summand_inclusion_semantics():
  data = build_phase48_1_data()

  decomposition_map = data[
    "decomposition_map"
  ]

  assert not hasattr(
    decomposition_map,
    "first_summand_inclusion",
  )

  assert not hasattr(
    decomposition_map,
    "inclusion",
  )

  assert not hasattr(
    decomposition_map,
    "restriction",
  )


def test_phase48_1_current_api_cannot_losslessly_represent_specific_e_injectivity():
  first = build_phase48_1_data(
    i_name="i",
    n_name="n",
  )

  second = build_phase48_1_data(
    i_name="j",
    n_name="m",
  )

  assert (
    first[
      "first_summand"
    ],
    first[
      "target_group"
    ],
  ) != (
    second[
      "first_summand"
    ],
    second[
      "target_group"
    ],
  )

  assert (
    InjectiveMapStatement(
      map=EHP_E_MAP,
    )
    == InjectiveMapStatement(
      map=EHP_E_MAP,
    )
  )



