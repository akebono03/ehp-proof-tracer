from expression import (
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  PrimaryComponent,
  TodaEHPExactnessWindow,
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


def build_phase45_4_symbolic_sequence(
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


def build_phase45_4_exactness_windows(
  i,
  n,
):
  sequence = (
    build_phase45_4_symbolic_sequence(
      i,
      n,
    )
  )

  first_window = (
    TodaEHPExactnessWindow(
      source_term=sequence.terms[
        0
      ],
      middle_term=sequence.terms[
        1
      ],
      target_term=sequence.terms[
        2
      ],
      first_map=sequence.maps[
        0
      ],
      second_map=sequence.maps[
        1
      ],
    )
  )

  second_window = (
    TodaEHPExactnessWindow(
      source_term=sequence.terms[
        1
      ],
      middle_term=sequence.terms[
        2
      ],
      target_term=sequence.terms[
        3
      ],
      first_map=sequence.maps[
        1
      ],
      second_map=sequence.maps[
        2
      ],
    )
  )

  third_window = (
    TodaEHPExactnessWindow(
      source_term=sequence.terms[
        2
      ],
      middle_term=sequence.terms[
        3
      ],
      target_term=sequence.terms[
        4
      ],
      first_map=sequence.maps[
        2
      ],
      second_map=sequence.maps[
        3
      ],
    )
  )

  return (
    first_window,
    second_window,
    third_window,
  )


def test_phase45_4_first_window_preserves_e_h_maps():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  first_window = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      0
    ]
  )

  assert (
    first_window.first_map
    is EHP_E_MAP
  )

  assert (
    first_window.second_map
    is EHP_H_MAP
  )


def test_phase45_4_first_window_preserves_all_three_terms():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  first_window = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      0
    ]
  )

  assert first_window.source_term == (
    TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=n,
    )
  )

  assert first_window.middle_term == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=1,
      ),
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
    )
  )

  assert first_window.target_term == (
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
    )
  )


def test_phase45_4_second_window_preserves_h_delta_maps():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  second_window = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      1
    ]
  )

  assert (
    second_window.first_map
    is EHP_H_MAP
  )

  assert (
    second_window.second_map
    is EHP_DELTA_MAP
  )


def test_phase45_4_second_window_preserves_all_three_terms():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  second_window = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      1
    ]
  )

  assert second_window.source_term == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=1,
      ),
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
    )
  )

  assert second_window.middle_term == (
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
    )
  )

  assert second_window.target_term == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=-1,
      ),
      sphere_dimension=n,
    )
  )


def test_phase45_4_third_window_preserves_delta_e_maps():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  third_window = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      2
    ]
  )

  assert (
    third_window.first_map
    is EHP_DELTA_MAP
  )

  assert (
    third_window.second_map
    is EHP_E_MAP
  )


def test_phase45_4_third_window_preserves_all_three_terms():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  third_window = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      2
    ]
  )

  assert third_window.source_term == (
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
    )
  )

  assert third_window.middle_term == (
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=-1,
      ),
      sphere_dimension=n,
    )
  )

  assert third_window.target_term == (
    TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
    )
  )


def test_phase45_4_three_windows_are_structurally_distinct():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  windows = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )
  )

  assert windows[
    0
  ] != windows[
    1
  ]

  assert windows[
    0
  ] != windows[
    2
  ]

  assert windows[
    1
  ] != windows[
    2
  ]


def test_phase45_4_same_instance_has_structural_equality():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  left = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )
  )

  right = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )
  )

  assert left == right


def test_phase45_4_different_e_h_instances_are_distinct():
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

  first = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      0
    ]
  )

  second = (
    build_phase45_4_exactness_windows(
      j,
      m,
    )[
      0
    ]
  )

  assert first != second

  assert (
    first.first_map
    == second.first_map
  )

  assert (
    first.second_map
    == second.second_map
  )


def test_phase45_4_different_h_delta_instances_are_distinct():
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

  first = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      1
    ]
  )

  second = (
    build_phase45_4_exactness_windows(
      j,
      m,
    )[
      1
    ]
  )

  assert first != second

  assert (
    first.first_map
    == second.first_map
  )

  assert (
    first.second_map
    == second.second_map
  )


def test_phase45_4_different_delta_e_instances_are_distinct():
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

  first = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      2
    ]
  )

  second = (
    build_phase45_4_exactness_windows(
      j,
      m,
    )[
      2
    ]
  )

  assert first != second

  assert (
    first.first_map
    == second.first_map
  )

  assert (
    first.second_map
    == second.second_map
  )


def test_phase45_4_window_terms_remain_toda_primary_groups():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  windows = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )
  )

  for window in windows:
    assert isinstance(
      window.source_term,
      TodaPrimaryGroup,
    )

    assert isinstance(
      window.middle_term,
      TodaPrimaryGroup,
    )

    assert isinstance(
      window.target_term,
      TodaPrimaryGroup,
    )


def test_phase45_4_window_does_not_replace_terms_with_primary_components():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  windows = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )
  )

  for window in windows:
    assert not isinstance(
      window.source_term,
      PrimaryComponent,
    )

    assert not isinstance(
      window.middle_term,
      PrimaryComponent,
    )

    assert not isinstance(
      window.target_term,
      PrimaryComponent,
    )


def test_phase45_4_window_is_not_generic_exactness_statement():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  window = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      0
    ]
  )

  assert not isinstance(
    window,
    ExactnessStatement,
  )


def test_phase45_4_window_does_not_assert_exactness():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  window = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      0
    ]
  )

  assert not hasattr(
    window,
    "is_exact",
  )

  assert not hasattr(
    window,
    "exact",
  )


def test_phase45_4_window_has_no_theorem_provenance():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  window = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      0
    ]
  )

  assert not hasattr(
    window,
    "theorem",
  )

  assert not hasattr(
    window,
    "provenance",
  )

  assert not hasattr(
    window,
    "inference_rule",
  )


def test_phase45_4_window_does_not_encode_prop42_truth():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  window = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )[
      0
    ]
  )

  assert not hasattr(
    window,
    "toda_prop_4_2",
  )

  assert not hasattr(
    window,
    "proposition",
  )


def test_phase45_4_windows_are_losslessly_recoverable_from_sequence():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  sequence = (
    build_phase45_4_symbolic_sequence(
      i,
      n,
    )
  )

  windows = (
    build_phase45_4_exactness_windows(
      i,
      n,
    )
  )

  assert windows[
    0
  ] == TodaEHPExactnessWindow(
    source_term=sequence.terms[
      0
    ],
    middle_term=sequence.terms[
      1
    ],
    target_term=sequence.terms[
      2
    ],
    first_map=sequence.maps[
      0
    ],
    second_map=sequence.maps[
      1
    ],
  )

  assert windows[
    1
  ] == TodaEHPExactnessWindow(
    source_term=sequence.terms[
      1
    ],
    middle_term=sequence.terms[
      2
    ],
    target_term=sequence.terms[
      3
    ],
    first_map=sequence.maps[
      1
    ],
    second_map=sequence.maps[
      2
    ],
  )

  assert windows[
    2
  ] == TodaEHPExactnessWindow(
    source_term=sequence.terms[
      2
    ],
    middle_term=sequence.terms[
      3
    ],
    target_term=sequence.terms[
      4
    ],
    first_map=sequence.maps[
      2
    ],
    second_map=sequence.maps[
      3
    ],
  )



