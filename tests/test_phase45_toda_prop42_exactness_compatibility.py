from expression import (
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaEHPSequence,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ExactnessStatement,
)


def build_phase45_3_symbolic_sequence(
  i,
  n,
):
  i_plus_one = ScalarSum(
    left=i,
    right=1,
  )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  two_n_plus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=1,
  )

  return TodaEHPSequence(
    terms=(
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=n,
      ),
      TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=n_plus_one,
      ),
      TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=two_n_plus_one,
      ),
      TodaPrimaryGroup(
        group_dimension=i_minus_one,
        sphere_dimension=n,
      ),
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=n_plus_one,
      ),
    ),
    maps=(
      EHP_E_MAP,
      EHP_H_MAP,
      EHP_DELTA_MAP,
      EHP_E_MAP,
    ),
  )


def build_phase45_3_exactness_statements():
  return (
    ExactnessStatement(
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
      is_exact=True,
    ),
    ExactnessStatement(
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
      is_exact=True,
    ),
    ExactnessStatement(
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
      is_exact=True,
    ),
  )


def test_phase45_3_first_exactness_pair_e_h_is_representable():
  first_statement = (
    build_phase45_3_exactness_statements()[
      0
    ]
  )

  assert first_statement == (
    ExactnessStatement(
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
      is_exact=True,
    )
  )


def test_phase45_3_second_exactness_pair_h_delta_is_representable():
  second_statement = (
    build_phase45_3_exactness_statements()[
      1
    ]
  )

  assert second_statement == (
    ExactnessStatement(
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
      is_exact=True,
    )
  )


def test_phase45_3_third_exactness_pair_delta_e_is_representable():
  third_statement = (
    build_phase45_3_exactness_statements()[
      2
    ]
  )

  assert third_statement == (
    ExactnessStatement(
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
      is_exact=True,
    )
  )


def test_phase45_3_three_exactness_positions_are_structurally_distinct():
  statements = (
    build_phase45_3_exactness_statements()
  )

  assert statements[
    0
  ] != statements[
    1
  ]

  assert statements[
    0
  ] != statements[
    2
  ]

  assert statements[
    1
  ] != statements[
    2
  ]


def test_phase45_3_first_window_terms_are_losslessly_available_from_sequence():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  sequence = (
    build_phase45_3_symbolic_sequence(
      i,
      n,
    )
  )

  first_window = (
    sequence.terms[
      0
    ],
    sequence.terms[
      1
    ],
    sequence.terms[
      2
    ],
  )

  assert first_window == (
    TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=n,
    ),
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=1,
      ),
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
    ),
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=1,
      ),
      sphere_dimension=ScalarSum(
        left=ScalarProduct(
          left=2,
          right=n,
        ),
        right=1,
      ),
    ),
  )


def test_phase45_3_second_window_terms_are_losslessly_available_from_sequence():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  sequence = (
    build_phase45_3_symbolic_sequence(
      i,
      n,
    )
  )

  second_window = (
    sequence.terms[
      1
    ],
    sequence.terms[
      2
    ],
    sequence.terms[
      3
    ],
  )

  assert second_window == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=1,
      ),
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
    ),
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=1,
      ),
      sphere_dimension=ScalarSum(
        left=ScalarProduct(
          left=2,
          right=n,
        ),
        right=1,
      ),
    ),
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=-1,
      ),
      sphere_dimension=n,
    ),
  )


def test_phase45_3_third_window_terms_are_losslessly_available_from_sequence():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  sequence = (
    build_phase45_3_symbolic_sequence(
      i,
      n,
    )
  )

  third_window = (
    sequence.terms[
      2
    ],
    sequence.terms[
      3
    ],
    sequence.terms[
      4
    ],
  )

  assert third_window == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=1,
      ),
      sphere_dimension=ScalarSum(
        left=ScalarProduct(
          left=2,
          right=n,
        ),
        right=1,
      ),
    ),
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=-1,
      ),
      sphere_dimension=n,
    ),
    TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
    ),
  )


def test_phase45_3_exactness_statement_does_not_store_source_term():
  statement = (
    build_phase45_3_exactness_statements()[
      0
    ]
  )

  assert not hasattr(
    statement,
    "source_term",
  )

  assert not hasattr(
    statement,
    "source_group",
  )


def test_phase45_3_exactness_statement_does_not_store_middle_term():
  statement = (
    build_phase45_3_exactness_statements()[
      0
    ]
  )

  assert not hasattr(
    statement,
    "middle_term",
  )

  assert not hasattr(
    statement,
    "middle_group",
  )


def test_phase45_3_exactness_statement_does_not_store_target_term():
  statement = (
    build_phase45_3_exactness_statements()[
      0
    ]
  )

  assert not hasattr(
    statement,
    "target_term",
  )

  assert not hasattr(
    statement,
    "target_group",
  )


def test_phase45_3_exactness_statement_does_not_store_symbolic_indices():
  statement = (
    build_phase45_3_exactness_statements()[
      0
    ]
  )

  assert not hasattr(
    statement,
    "i",
  )

  assert not hasattr(
    statement,
    "n",
  )


def test_phase45_3_different_symbolic_sequences_are_structurally_distinct():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  j = ScalarSymbol(
    name="j",
  )

  m = ScalarSymbol(
    name="m",
  )

  first_sequence = (
    build_phase45_3_symbolic_sequence(
      i,
      n,
    )
  )

  second_sequence = (
    build_phase45_3_symbolic_sequence(
      j,
      m,
    )
  )

  assert (
    first_sequence
    != second_sequence
  )


def test_phase45_3_same_e_h_exactness_statement_collides_across_instances():
  first_statement = (
    ExactnessStatement(
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
      is_exact=True,
    )
  )

  second_statement = (
    ExactnessStatement(
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
      is_exact=True,
    )
  )

  assert (
    first_statement
    == second_statement
  )


def test_phase45_3_same_h_delta_exactness_statement_collides_across_instances():
  first_statement = (
    ExactnessStatement(
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
      is_exact=True,
    )
  )

  second_statement = (
    ExactnessStatement(
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
      is_exact=True,
    )
  )

  assert (
    first_statement
    == second_statement
  )


def test_phase45_3_same_delta_e_exactness_statement_collides_across_instances():
  first_statement = (
    ExactnessStatement(
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
      is_exact=True,
    )
  )

  second_statement = (
    ExactnessStatement(
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
      is_exact=True,
    )
  )

  assert (
    first_statement
    == second_statement
  )


def test_phase45_3_exactness_statement_cannot_recover_sequence_instance():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  sequence = (
    build_phase45_3_symbolic_sequence(
      i,
      n,
    )
  )

  statement = (
    build_phase45_3_exactness_statements()[
      0
    ]
  )

  assert not hasattr(
    statement,
    "sequence",
  )

  assert sequence.terms[
    1
  ] not in (
    statement.first_map,
    statement.second_map,
  )


def test_phase45_3_exactness_statement_is_not_lossless_prop42_instance():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  j = ScalarSymbol(
    name="j",
  )

  m = ScalarSymbol(
    name="m",
  )

  first_sequence = (
    build_phase45_3_symbolic_sequence(
      i,
      n,
    )
  )

  second_sequence = (
    build_phase45_3_symbolic_sequence(
      j,
      m,
    )
  )

  assert (
    first_sequence
    != second_sequence
  )

  first_exactness = (
    ExactnessStatement(
      first_map=first_sequence.maps[
        0
      ],
      second_map=first_sequence.maps[
        1
      ],
      is_exact=True,
    )
  )

  second_exactness = (
    ExactnessStatement(
      first_map=second_sequence.maps[
        0
      ],
      second_map=second_sequence.maps[
        1
      ],
      is_exact=True,
    )
  )

  assert (
    first_exactness
    == second_exactness
  )



