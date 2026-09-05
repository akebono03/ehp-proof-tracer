from typing import (
  get_args,
  get_type_hints,
)

from expression import (
  HomotopyElement,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  DirectSumGroup,
  FreeCyclicGroup,
  PrimaryComponent,
  TodaPrimaryGroup,
)


def build_phase47_2_decomposition_groups():
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
  }


def test_phase47_2_direct_sum_group_type_contract_accepts_toda_primary_group():
  type_hints = get_type_hints(
    DirectSumGroup
  )

  summands_hint = type_hints[
    "summands"
  ]

  tuple_args = get_args(
    summands_hint
  )

  summand_type = tuple_args[
    0
  ]

  allowed_types = get_args(
    summand_type
  )

  assert TodaPrimaryGroup in (
    allowed_types
  )


def test_phase47_2_direct_sum_group_preserves_existing_free_cyclic_summand_type():
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

  assert FreeCyclicGroup in (
    allowed_types
  )


def test_phase47_2_direct_sum_group_preserves_existing_primary_component_type():
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


def test_phase47_2_first_source_summand_is_pi_i_minus_one_n_minus_one():
  data = (
    build_phase47_2_decomposition_groups()
  )

  assert data[
    "first_summand"
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


def test_phase47_2_second_source_summand_is_pi_i_two_n_minus_one():
  data = (
    build_phase47_2_decomposition_groups()
  )

  assert data[
    "second_summand"
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


def test_phase47_2_source_is_direct_sum_of_two_toda_groups():
  data = (
    build_phase47_2_decomposition_groups()
  )

  assert data[
    "source_group"
  ] == DirectSumGroup(
    summands=(
      data[
        "first_summand"
      ],
      data[
        "second_summand"
      ],
    ),
  )


def test_phase47_2_source_preserves_summand_order():
  data = (
    build_phase47_2_decomposition_groups()
  )

  assert data[
    "source_group"
  ].summands[
    0
  ] == data[
    "first_summand"
  ]

  assert data[
    "source_group"
  ].summands[
    1
  ] == data[
    "second_summand"
  ]


def test_phase47_2_reversed_source_summands_are_structurally_distinct():
  data = (
    build_phase47_2_decomposition_groups()
  )

  reversed_source = DirectSumGroup(
    summands=(
      data[
        "second_summand"
      ],
      data[
        "first_summand"
      ],
    ),
  )

  assert (
    reversed_source
    != data[
      "source_group"
    ]
  )


def test_phase47_2_target_is_pi_i_n():
  data = (
    build_phase47_2_decomposition_groups()
  )

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


def test_phase47_2_source_and_target_remain_structurally_distinct():
  data = (
    build_phase47_2_decomposition_groups()
  )

  assert (
    data[
      "source_group"
    ]
    != data[
      "target_group"
    ]
  )


def test_phase47_2_same_decomposition_source_has_structural_equality():
  first = (
    build_phase47_2_decomposition_groups()
  )

  second = (
    build_phase47_2_decomposition_groups()
  )

  assert (
    first[
      "source_group"
    ]
    == second[
      "source_group"
    ]
  )


def test_phase47_2_different_i_instance_produces_distinct_source():
  data = (
    build_phase47_2_decomposition_groups()
  )

  j = ScalarSymbol(
    name="j",
  )

  different = DirectSumGroup(
    summands=(
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=j,
          right=-1,
        ),
        sphere_dimension=data[
          "n_minus_one"
        ],
      ),
      TodaPrimaryGroup(
        group_dimension=j,
        sphere_dimension=data[
          "two_n_minus_one"
        ],
      ),
    ),
  )

  assert (
    different
    != data[
      "source_group"
    ]
  )


def test_phase47_2_different_n_instance_produces_distinct_source():
  data = (
    build_phase47_2_decomposition_groups()
  )

  m = ScalarSymbol(
    name="m",
  )

  different = DirectSumGroup(
    summands=(
      TodaPrimaryGroup(
        group_dimension=data[
          "i_minus_one"
        ],
        sphere_dimension=ScalarSum(
          left=m,
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
            right=m,
          ),
          right=-1,
        ),
      ),
    ),
  )

  assert (
    different
    != data[
      "source_group"
    ]
  )


def test_phase47_2_existing_phase44_direct_sum_shape_remains_representable():
  n = ScalarSymbol(
    name="n",
  )

  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=two_n_minus_one,
  )

  existing_shape = DirectSumGroup(
    summands=(
      FreeCyclicGroup(
        generator=alpha,
      ),
      PrimaryComponent(
        group_dimension=two_n_minus_one,
        sphere_dimension=n,
        prime=2,
      ),
    ),
  )

  assert existing_shape.summands == (
    FreeCyclicGroup(
      generator=alpha,
    ),
    PrimaryComponent(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
      prime=2,
    ),
  )


def test_phase47_2_direct_sum_group_does_not_assert_isomorphism():
  data = (
    build_phase47_2_decomposition_groups()
  )

  source = data[
    "source_group"
  ]

  assert not hasattr(
    source,
    "is_isomorphic",
  )

  assert not hasattr(
    source,
    "isomorphism",
  )

  assert not hasattr(
    source,
    "map",
  )


def test_phase47_2_source_group_has_no_prop44_theorem_semantics():
  data = (
    build_phase47_2_decomposition_groups()
  )

  source = data[
    "source_group"
  ]

  assert not hasattr(
    source,
    "toda_prop44",
  )

  assert not hasattr(
    source,
    "theorem",
  )

  assert not hasattr(
    source,
    "alpha",
  )

  assert not hasattr(
    source,
    "formula",
  )


def test_phase47_2_target_group_has_no_prop44_theorem_semantics():
  data = (
    build_phase47_2_decomposition_groups()
  )

  target = data[
    "target_group"
  ]

  assert not hasattr(
    target,
    "toda_prop44",
  )

  assert not hasattr(
    target,
    "theorem",
  )

  assert not hasattr(
    target,
    "map",
  )



