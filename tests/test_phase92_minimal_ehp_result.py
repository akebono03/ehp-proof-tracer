from dataclasses import (
  FrozenInstanceError,
)

import pytest

from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaEHPSequence,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from toda_ehp_result import (
  TodaEHPExactnessWindowResult,
  TodaEHPSequenceResult,
)


def build_phase92_2_fixture():
  pi10_9 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=9,
  )

  pi8_4 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=4,
  )

  pi9_5 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  pi9_9 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=9,
  )

  pi7_4 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=4,
  )

  sequence = TodaEHPSequence(
    terms=(
      pi10_9,
      pi8_4,
      pi9_5,
      pi9_9,
      pi7_4,
    ),
    maps=(
      EHP_DELTA_MAP,
      EHP_E_MAP,
      EHP_H_MAP,
      EHP_DELTA_MAP,
    ),
  )

  delta_e_window = (
    TodaEHPExactnessWindow(
      source_term=pi10_9,
      middle_term=pi8_4,
      target_term=pi9_5,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )

  e_h_window = (
    TodaEHPExactnessWindow(
      source_term=pi8_4,
      middle_term=pi9_5,
      target_term=pi9_9,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    )
  )

  h_delta_window = (
    TodaEHPExactnessWindow(
      source_term=pi9_5,
      middle_term=pi9_9,
      target_term=pi7_4,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    )
  )

  delta_e_result = (
    TodaEHPExactnessWindowResult(
      window=delta_e_window,
    )
  )

  e_h_result = (
    TodaEHPExactnessWindowResult(
      window=e_h_window,
    )
  )

  h_delta_result = (
    TodaEHPExactnessWindowResult(
      window=h_delta_window,
    )
  )

  sequence_result = TodaEHPSequenceResult(
    target=pi9_5,
    sequence=sequence,
    windows=(
      delta_e_result,
      e_h_result,
      h_delta_result,
    ),
  )

  return {
    "pi10_9": pi10_9,
    "pi8_4": pi8_4,
    "pi9_5": pi9_5,
    "pi9_9": pi9_9,
    "pi7_4": pi7_4,
    "sequence": sequence,
    "delta_e_window": (
      delta_e_window
    ),
    "e_h_window": e_h_window,
    "h_delta_window": (
      h_delta_window
    ),
    "delta_e_result": (
      delta_e_result
    ),
    "e_h_result": e_h_result,
    "h_delta_result": (
      h_delta_result
    ),
    "sequence_result": (
      sequence_result
    ),
  }


def test_phase92_2_window_result_preserves_structural_window_identity():
  data = build_phase92_2_fixture()

  assert (
    data[
      "e_h_result"
    ].window
    is data[
      "e_h_window"
    ]
  )


def test_phase92_2_sequence_result_preserves_target():
  data = build_phase92_2_fixture()

  assert (
    data[
      "sequence_result"
    ].target
    == data[
      "pi9_5"
    ]
  )


def test_phase92_2_sequence_result_preserves_sequence_identity():
  data = build_phase92_2_fixture()

  assert (
    data[
      "sequence_result"
    ].sequence
    is data[
      "sequence"
    ]
  )


def test_phase92_2_sequence_result_preserves_window_result_order():
  data = build_phase92_2_fixture()

  assert (
    data[
      "sequence_result"
    ].windows
    == (
      data[
        "delta_e_result"
      ],
      data[
        "e_h_result"
      ],
      data[
        "h_delta_result"
      ],
    )
  )


def test_phase92_2_sequence_preserves_concrete_pi9_5_ehp_chain():
  data = build_phase92_2_fixture()

  sequence = data[
    "sequence_result"
  ].sequence

  assert sequence.terms == (
    data[
      "pi10_9"
    ],
    data[
      "pi8_4"
    ],
    data[
      "pi9_5"
    ],
    data[
      "pi9_9"
    ],
    data[
      "pi7_4"
    ],
  )

  assert sequence.maps == (
    EHP_DELTA_MAP,
    EHP_E_MAP,
    EHP_H_MAP,
    EHP_DELTA_MAP,
  )


def test_phase92_2_sequence_result_allows_subset_of_sequence_windows():
  data = build_phase92_2_fixture()

  result = TodaEHPSequenceResult(
    target=data[
      "pi9_5"
    ],
    sequence=data[
      "sequence"
    ],
    windows=(
      data[
        "e_h_result"
      ],
    ),
  )

  assert result.windows == (
    data[
      "e_h_result"
    ],
  )


def test_phase92_2_window_result_is_frozen():
  data = build_phase92_2_fixture()

  with pytest.raises(
    FrozenInstanceError,
  ):
    data[
      "e_h_result"
    ].window = data[
      "h_delta_window"
    ]


def test_phase92_2_sequence_result_is_frozen():
  data = build_phase92_2_fixture()

  with pytest.raises(
    FrozenInstanceError,
  ):
    data[
      "sequence_result"
    ].target = data[
      "pi8_4"
    ]


def test_phase92_2_rejects_non_window():
  with pytest.raises(
    TypeError,
    match=(
      "window must be "
      "a TodaEHPExactnessWindow"
    ),
  ):
    TodaEHPExactnessWindowResult(
      window="not a window",
    )


def test_phase92_2_rejects_non_toda_target():
  data = build_phase92_2_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "target must be "
      "a TodaPrimaryGroup"
    ),
  ):
    TodaEHPSequenceResult(
      target="not a target",
      sequence=data[
        "sequence"
      ],
      windows=(),
    )


def test_phase92_2_rejects_non_sequence():
  data = build_phase92_2_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "sequence must be "
      "a TodaEHPSequence"
    ),
  ):
    TodaEHPSequenceResult(
      target=data[
        "pi9_5"
      ],
      sequence="not a sequence",
      windows=(),
    )


def test_phase92_2_requires_window_tuple():
  data = build_phase92_2_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "windows must be a tuple"
    ),
  ):
    TodaEHPSequenceResult(
      target=data[
        "pi9_5"
      ],
      sequence=data[
        "sequence"
      ],
      windows=[
        data[
          "e_h_result"
        ],
      ],
    )


def test_phase92_2_rejects_non_window_result_member():
  data = build_phase92_2_fixture()

  with pytest.raises(
    TypeError,
    match=(
      "windows must contain only "
      "TodaEHPExactnessWindowResult "
      "objects"
    ),
  ):
    TodaEHPSequenceResult(
      target=data[
        "pi9_5"
      ],
      sequence=data[
        "sequence"
      ],
      windows=(
        data[
          "e_h_window"
        ],
      ),
    )


def test_phase92_2_rejects_target_outside_sequence():
  data = build_phase92_2_fixture()

  unrelated_target = (
    TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=5,
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "target must occur in "
      "sequence.terms"
    ),
  ):
    TodaEHPSequenceResult(
      target=unrelated_target,
      sequence=data[
        "sequence"
      ],
      windows=(),
    )


def test_phase92_2_rejects_window_not_contained_in_sequence():
  data = build_phase92_2_fixture()

  unrelated_group = (
    TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )

  unrelated_window = (
    TodaEHPExactnessWindow(
      source_term=data[
        "pi8_4"
      ],
      middle_term=data[
        "pi9_5"
      ],
      target_term=unrelated_group,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    )
  )

  unrelated_result = (
    TodaEHPExactnessWindowResult(
      window=unrelated_window,
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "each window must be "
      "a contiguous window of sequence"
    ),
  ):
    TodaEHPSequenceResult(
      target=data[
        "pi9_5"
      ],
      sequence=data[
        "sequence"
      ],
      windows=(
        unrelated_result,
      ),
    )
