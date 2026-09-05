from typing import (
  get_args,
  get_type_hints,
)

import homotopy_groups
import toda_rules

from expression import (
  Composition,
  HomotopyElement,
  MapApplication,
  MapSymbol,
  Multiple,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  PreimageSubgroup,
  PrimaryComponent,
  PrimaryComponentMembershipStatement,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_H_MAP,
)
from map_property_rules import (
  IsomorphismStatement,
)
from proof import (
  Relation,
  RelationType,
)
from toda_rules import (
  Toda45IsomorphismStatement,
)


def build_phase47_1_symbolic_data():
  n = ScalarSymbol(
    name="n",
  )

  i = ScalarSymbol(
    name="i",
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

  first_source_group = TodaPrimaryGroup(
    group_dimension=i_minus_one,
    sphere_dimension=n_minus_one,
  )

  second_source_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=two_n_minus_one,
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  alpha = HomotopyElement(
    name="α",
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

  iota = HomotopyElement(
    name="ι_(2n-1)",
    dimension=two_n_minus_one,
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

  return {
    "n": n,
    "i": i,
    "i_minus_one": i_minus_one,
    "n_minus_one": n_minus_one,
    "two_n_minus_one": (
      two_n_minus_one
    ),
    "first_source_group": (
      first_source_group
    ),
    "second_source_group": (
      second_source_group
    ),
    "target_group": target_group,
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "iota": iota,
    "formula": formula,
  }


def test_phase47_1_first_source_toda_group_is_losslessly_representable():
  data = build_phase47_1_symbolic_data()

  assert data[
    "first_source_group"
  ] == TodaPrimaryGroup(
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


def test_phase47_1_second_source_toda_group_is_losslessly_representable():
  data = build_phase47_1_symbolic_data()

  assert data[
    "second_source_group"
  ] == TodaPrimaryGroup(
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
  )


def test_phase47_1_target_toda_group_is_losslessly_representable():
  data = build_phase47_1_symbolic_data()

  assert data[
    "target_group"
  ] == TodaPrimaryGroup(
    group_dimension=data[
      "i"
    ],
    sphere_dimension=data[
      "n"
    ],
  )


def test_phase47_1_prop44_source_terms_are_toda_primary_groups():
  data = build_phase47_1_symbolic_data()

  assert isinstance(
    data[
      "first_source_group"
    ],
    TodaPrimaryGroup,
  )

  assert isinstance(
    data[
      "second_source_group"
    ],
    TodaPrimaryGroup,
  )


def test_phase47_1_prop44_source_terms_are_not_primary_components():
  data = build_phase47_1_symbolic_data()

  assert not isinstance(
    data[
      "first_source_group"
    ],
    PrimaryComponent,
  )

  assert not isinstance(
    data[
      "second_source_group"
    ],
    PrimaryComponent,
  )


def test_phase47_1_direct_sum_group_current_contract_includes_existing_summands():
  type_hints = get_type_hints(
    DirectSumGroup
  )

  summands_hint = type_hints[
    "summands"
  ]

  summand_type = get_args(
    summands_hint
  )[
    0
  ]

  allowed_types = get_args(
    summand_type
  )

  assert PrimaryComponent in (
    allowed_types
  )


def test_phase47_1_preimage_subgroup_remains_primary_component_structure():
  type_hints = get_type_hints(
    PreimageSubgroup
  )

  assert type_hints[
    "map"
  ] is MapSymbol

  assert type_hints[
    "subgroup"
  ] is PrimaryComponent


def test_phase47_1_preimage_subgroup_is_not_prop44_source_group():
  data = build_phase47_1_symbolic_data()

  preimage = PreimageSubgroup(
    map=MapSymbol(
      name="E",
    ),
    subgroup=PrimaryComponent(
      group_dimension=data[
        "i"
      ],
      sphere_dimension=data[
        "n"
      ],
      prime=2,
    ),
  )

  assert (
    preimage
    != data[
      "first_source_group"
    ]
  )

  assert (
    preimage
    != data[
      "second_source_group"
    ]
  )


def test_phase47_1_formula_e_beta_plus_alpha_composed_gamma_is_representable():
  data = build_phase47_1_symbolic_data()

  assert data[
    "formula"
  ] == Sum(
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


def test_phase47_1_formula_preserves_alpha_instance():
  data = build_phase47_1_symbolic_data()

  composition = data[
    "formula"
  ].right

  assert isinstance(
    composition,
    Composition,
  )

  assert composition.left == (
    data[
      "alpha"
    ]
  )

  assert composition.right == (
    data[
      "gamma"
    ]
  )


def test_phase47_1_formula_is_expression_not_map_object():
  data = build_phase47_1_symbolic_data()

  formula = data[
    "formula"
  ]

  assert not isinstance(
    formula,
    MapSymbol,
  )

  assert not hasattr(
    formula,
    "source_group",
  )

  assert not hasattr(
    formula,
    "target_group",
  )


def test_phase47_1_positive_hopf_condition_is_representable():
  data = build_phase47_1_symbolic_data()

  condition = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=data[
        "alpha"
      ],
    ),
    rhs=data[
      "iota"
    ],
    relation_type=RelationType.EQUALITY,
  )

  assert condition.lhs == (
    MapApplication(
      map=EHP_H_MAP,
      expression=data[
        "alpha"
      ],
    )
  )

  assert condition.rhs == (
    data[
      "iota"
    ]
  )


def test_phase47_1_negative_hopf_condition_is_representable():
  data = build_phase47_1_symbolic_data()

  condition = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=data[
        "alpha"
      ],
    ),
    rhs=Multiple(
      coefficient=-1,
      expression=data[
        "iota"
      ],
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert condition.rhs == (
    Multiple(
      coefficient=-1,
      expression=data[
        "iota"
      ],
    )
  )


def test_phase47_1_positive_and_negative_hopf_conditions_remain_distinct():
  data = build_phase47_1_symbolic_data()

  positive = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=data[
        "alpha"
      ],
    ),
    rhs=data[
      "iota"
    ],
    relation_type=RelationType.EQUALITY,
  )

  negative = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=data[
        "alpha"
      ],
    ),
    rhs=Multiple(
      coefficient=-1,
      expression=data[
        "iota"
      ],
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert positive != negative


def test_phase47_1_primary_membership_statement_cannot_type_toda_group():
  type_hints = get_type_hints(
    PrimaryComponentMembershipStatement
  )

  assert type_hints[
    "component"
  ] is PrimaryComponent

  assert (
    type_hints[
      "component"
    ]
    is not TodaPrimaryGroup
  )


def test_phase47_1_generic_isomorphism_statement_stores_only_map_symbol():
  type_hints = get_type_hints(
    IsomorphismStatement
  )

  assert type_hints[
    "map"
  ] is MapSymbol

  statement = IsomorphismStatement(
    map=MapSymbol(
      name="Φ",
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
    "alpha",
  )

  assert not hasattr(
    statement,
    "formula",
  )


def test_phase47_1_generic_isomorphism_collides_across_prop44_instances():
  first_data = (
    build_phase47_1_symbolic_data()
  )

  second_alpha = HomotopyElement(
    name="α'",
    dimension=first_data[
      "two_n_minus_one"
    ],
  )

  assert (
    first_data[
      "alpha"
    ]
    != second_alpha
  )

  first_statement = (
    IsomorphismStatement(
      map=MapSymbol(
        name="Φ",
      ),
    )
  )

  second_statement = (
    IsomorphismStatement(
      map=MapSymbol(
        name="Φ",
      ),
    )
  )

  assert (
    first_statement
    == second_statement
  )


def test_phase47_1_toda_iterated_suspension_map_source_is_single_toda_group():
  type_hints = get_type_hints(
    TodaIteratedSuspensionMap
  )

  assert type_hints[
    "source_group"
  ] is TodaPrimaryGroup

  assert type_hints[
    "target_group"
  ] is TodaPrimaryGroup


def test_phase47_1_toda_iterated_suspension_map_is_not_prop44_decomposition_map():
  data = build_phase47_1_symbolic_data()

  suspension_map = (
    TodaIteratedSuspensionMap(
      exponent=1,
      source_group=data[
        "first_source_group"
      ],
      target_group=data[
        "target_group"
      ],
    )
  )

  assert not hasattr(
    suspension_map,
    "alpha",
  )

  assert not hasattr(
    suspension_map,
    "formula",
  )

  assert not hasattr(
    suspension_map,
    "summands",
  )


def test_phase47_1_toda45_statement_remains_specific_to_iterated_suspension():
  data = build_phase47_1_symbolic_data()

  suspension_map = (
    TodaIteratedSuspensionMap(
      exponent=1,
      source_group=data[
        "first_source_group"
      ],
      target_group=data[
        "target_group"
      ],
    )
  )

  statement = (
    Toda45IsomorphismStatement(
      map=suspension_map,
    )
  )

  assert statement.map == (
    suspension_map
  )

  assert not isinstance(
    statement,
    IsomorphismStatement,
  )


def test_phase47_1_no_prop44_isomorphism_statement_exists_yet():
  assert not hasattr(
    toda_rules,
    "TodaProp44IsomorphismStatement",
  )

  assert not hasattr(
    toda_rules,
    "Toda44IsomorphismStatement",
  )


def test_phase47_1_no_prop44_theorem_rule_exists_yet():
  assert not hasattr(
    toda_rules,
    "toda_prop44_isomorphism_inference_rule",
  )

  assert not hasattr(
    toda_rules,
    "toda_prop44_decomposition_inference_rule",
  )



