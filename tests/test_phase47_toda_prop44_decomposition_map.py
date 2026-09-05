from typing import (
  get_type_hints,
)

from expression import (
  Composition,
  Expression,
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
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
)


def build_phase47_3_decomposition_map(
  alpha_name="α",
  beta_name="β",
  gamma_name="γ",
):
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
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
    name=beta_name,
    dimension=i_minus_one,
  )

  gamma = HomotopyElement(
    name=gamma_name,
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
  }


def test_phase47_3_map_source_group_uses_direct_sum_group():
  type_hints = get_type_hints(
    TodaProp44DecompositionMap
  )

  assert type_hints[
    "source_group"
  ] is DirectSumGroup


def test_phase47_3_map_target_group_uses_toda_primary_group():
  type_hints = get_type_hints(
    TodaProp44DecompositionMap
  )

  assert type_hints[
    "target_group"
  ] is TodaPrimaryGroup


def test_phase47_3_map_alpha_uses_expression():
  type_hints = get_type_hints(
    TodaProp44DecompositionMap
  )

  assert type_hints[
    "alpha"
  ] is Expression


def test_phase47_3_map_beta_uses_expression():
  type_hints = get_type_hints(
    TodaProp44DecompositionMap
  )

  assert type_hints[
    "beta"
  ] is Expression


def test_phase47_3_map_gamma_uses_expression():
  type_hints = get_type_hints(
    TodaProp44DecompositionMap
  )

  assert type_hints[
    "gamma"
  ] is Expression


def test_phase47_3_map_formula_uses_expression():
  type_hints = get_type_hints(
    TodaProp44DecompositionMap
  )

  assert type_hints[
    "formula"
  ] is Expression


def test_phase47_3_source_is_prop44_direct_sum():
  data = (
    build_phase47_3_decomposition_map()
  )

  assert data[
    "decomposition_map"
  ].source_group == DirectSumGroup(
    summands=(
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
      ),
      TodaPrimaryGroup(
        group_dimension=data[
          "i"
        ],
        sphere_dimension=ScalarSum(
          left=ScalarProduct(
            left=2,
            right=data[
              "n"
            ],
          ),
          right=-1,
        ),
      ),
    ),
  )


def test_phase47_3_target_is_pi_i_n():
  data = (
    build_phase47_3_decomposition_map()
  )

  assert data[
    "decomposition_map"
  ].target_group == (
    TodaPrimaryGroup(
      group_dimension=data[
        "i"
      ],
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase47_3_map_preserves_alpha():
  data = (
    build_phase47_3_decomposition_map()
  )

  assert data[
    "decomposition_map"
  ].alpha == data[
    "alpha"
  ]


def test_phase47_3_map_preserves_beta():
  data = (
    build_phase47_3_decomposition_map()
  )

  assert data[
    "decomposition_map"
  ].beta == data[
    "beta"
  ]


def test_phase47_3_map_preserves_gamma():
  data = (
    build_phase47_3_decomposition_map()
  )

  assert data[
    "decomposition_map"
  ].gamma == data[
    "gamma"
  ]


def test_phase47_3_formula_is_e_beta_plus_alpha_composed_gamma():
  data = (
    build_phase47_3_decomposition_map()
  )

  assert data[
    "decomposition_map"
  ].formula == Sum(
    left=Suspension(
      expression=data[
        "beta"
      ],
    ),
    right=Composition(
      left=data[
        "alpha"
      ],
      right=data[
        "gamma"
      ],
    ),
  )


def test_phase47_3_formula_uses_same_alpha_instance():
  data = (
    build_phase47_3_decomposition_map()
  )

  formula = data[
    "decomposition_map"
  ].formula

  assert isinstance(
    formula,
    Sum,
  )

  assert isinstance(
    formula.right,
    Composition,
  )

  assert formula.right.left == (
    data[
      "decomposition_map"
    ].alpha
  )


def test_phase47_3_formula_uses_same_beta_instance():
  data = (
    build_phase47_3_decomposition_map()
  )

  formula = data[
    "decomposition_map"
  ].formula

  assert isinstance(
    formula.left,
    Suspension,
  )

  assert formula.left.expression == (
    data[
      "decomposition_map"
    ].beta
  )


def test_phase47_3_formula_uses_same_gamma_instance():
  data = (
    build_phase47_3_decomposition_map()
  )

  formula = data[
    "decomposition_map"
  ].formula

  assert isinstance(
    formula.right,
    Composition,
  )

  assert formula.right.right == (
    data[
      "decomposition_map"
    ].gamma
  )


def test_phase47_3_same_map_instance_has_structural_equality():
  first = (
    build_phase47_3_decomposition_map()
  )

  second = (
    build_phase47_3_decomposition_map()
  )

  assert (
    first[
      "decomposition_map"
    ]
    == second[
      "decomposition_map"
    ]
  )


def test_phase47_3_different_alpha_instance_is_structurally_distinct():
  first = (
    build_phase47_3_decomposition_map()
  )

  second = (
    build_phase47_3_decomposition_map(
      alpha_name="α'",
    )
  )

  assert (
    first[
      "decomposition_map"
    ]
    != second[
      "decomposition_map"
    ]
  )


def test_phase47_3_different_beta_instance_is_structurally_distinct():
  first = (
    build_phase47_3_decomposition_map()
  )

  second = (
    build_phase47_3_decomposition_map(
      beta_name="β'",
    )
  )

  assert (
    first[
      "decomposition_map"
    ]
    != second[
      "decomposition_map"
    ]
  )


def test_phase47_3_different_gamma_instance_is_structurally_distinct():
  first = (
    build_phase47_3_decomposition_map()
  )

  second = (
    build_phase47_3_decomposition_map(
      gamma_name="γ'",
    )
  )

  assert (
    first[
      "decomposition_map"
    ]
    != second[
      "decomposition_map"
    ]
  )


def test_phase47_3_different_source_group_is_structurally_distinct():
  data = (
    build_phase47_3_decomposition_map()
  )

  different = (
    TodaProp44DecompositionMap(
      source_group=DirectSumGroup(
        summands=(
          data[
            "second_summand"
          ],
          data[
            "first_summand"
          ],
        ),
      ),
      target_group=data[
        "target_group"
      ],
      alpha=data[
        "alpha"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=data[
        "formula"
      ],
    )
  )

  assert (
    different
    != data[
      "decomposition_map"
    ]
  )


def test_phase47_3_different_target_group_is_structurally_distinct():
  data = (
    build_phase47_3_decomposition_map()
  )

  different = (
    TodaProp44DecompositionMap(
      source_group=data[
        "source_group"
      ],
      target_group=TodaPrimaryGroup(
        group_dimension=ScalarSymbol(
          name="j",
        ),
        sphere_dimension=data[
          "n"
        ],
      ),
      alpha=data[
        "alpha"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=data[
        "formula"
      ],
    )
  )

  assert (
    different
    != data[
      "decomposition_map"
    ]
  )


def test_phase47_3_map_is_not_map_symbol():
  data = (
    build_phase47_3_decomposition_map()
  )

  assert not isinstance(
    data[
      "decomposition_map"
    ],
    MapSymbol,
  )


def test_phase47_3_map_is_not_iterated_suspension_map():
  data = (
    build_phase47_3_decomposition_map()
  )

  assert not isinstance(
    data[
      "decomposition_map"
    ],
    TodaIteratedSuspensionMap,
  )


def test_phase47_3_map_does_not_assert_isomorphism():
  data = (
    build_phase47_3_decomposition_map()
  )

  decomposition_map = data[
    "decomposition_map"
  ]

  assert not hasattr(
    decomposition_map,
    "is_isomorphism",
  )

  assert not hasattr(
    decomposition_map,
    "isomorphic",
  )

  assert not hasattr(
    decomposition_map,
    "isomorphism",
  )


def test_phase47_3_map_has_no_prop44_theorem_semantics():
  data = (
    build_phase47_3_decomposition_map()
  )

  decomposition_map = data[
    "decomposition_map"
  ]

  assert not hasattr(
    decomposition_map,
    "toda_prop44",
  )

  assert not hasattr(
    decomposition_map,
    "theorem",
  )


def test_phase47_3_constructor_does_not_validate_formula():
  data = (
    build_phase47_3_decomposition_map()
  )

  arbitrary_formula = HomotopyElement(
    name="δ",
    dimension=data[
      "i"
    ],
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=data[
        "source_group"
      ],
      target_group=data[
        "target_group"
      ],
      alpha=data[
        "alpha"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=arbitrary_formula,
    )
  )

  assert decomposition_map.formula == (
    arbitrary_formula
  )


def test_phase47_3_constructor_does_not_validate_group_formula_compatibility():
  data = (
    build_phase47_3_decomposition_map()
  )

  arbitrary_source = DirectSumGroup(
    summands=(
      TodaPrimaryGroup(
        group_dimension=1,
        sphere_dimension=2,
      ),
      TodaPrimaryGroup(
        group_dimension=3,
        sphere_dimension=4,
      ),
    ),
  )

  arbitrary_target = TodaPrimaryGroup(
    group_dimension=100,
    sphere_dimension=200,
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=arbitrary_source,
      target_group=arbitrary_target,
      alpha=data[
        "alpha"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=data[
        "formula"
      ],
    )
  )

  assert decomposition_map.source_group == (
    arbitrary_source
  )

  assert decomposition_map.target_group == (
    arbitrary_target
  )



