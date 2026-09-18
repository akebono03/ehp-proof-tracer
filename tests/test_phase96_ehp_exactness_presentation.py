import pytest

from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import ProofStep
from test_phase92_exactness_use_provenance import (
  build_phase92_5_data,
)
from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
  get_single_candidate,
)
from toda_ehp_exactness_provenance import (
  TodaEHPExactnessUseResult,
)
from toda_ehp_presentation import (
  TodaEHPExactnessPresentation,
  TodaEHPExactnessUsePresentation,
  TodaEHPExactnessWindowPresentation,
  TodaEHPMapPresentation,
  TodaEHPSequencePresentation,
  build_toda_ehp_exactness_presentation,
  build_toda_ehp_exactness_use_presentation,
  build_toda_ehp_exactness_window_presentation,
  build_toda_ehp_map_presentation,
  build_toda_ehp_sequence_presentation,
)
from toda_presentation import (
  TodaTargetPresentation,
)


def test_phase96_4_map_presentation_preserves_map_identity():
  presentation = (
    build_toda_ehp_map_presentation(
      EHP_E_MAP
    )
  )

  assert isinstance(
    presentation,
    TodaEHPMapPresentation,
  )
  assert (
    presentation.source_map
    is EHP_E_MAP
  )
  assert (
    presentation.name
    == EHP_E_MAP.name
  )


def test_phase96_4_actual_pi9_5_sequence_preserves_result_identity():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  ehp_result = (
    candidate
    .explanation
    .ehp_result
  )

  presentation = (
    build_toda_ehp_sequence_presentation(
      ehp_result
    )
  )

  assert isinstance(
    presentation,
    TodaEHPSequencePresentation,
  )
  assert (
    presentation.source_result
    is ehp_result
  )
  assert (
    presentation.target.source_target
    is ehp_result.target
  )


def test_phase96_4_actual_pi9_5_sequence_preserves_term_identity_and_order():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  ehp_result = (
    candidate
    .explanation
    .ehp_result
  )

  presentation = (
    build_toda_ehp_sequence_presentation(
      ehp_result
    )
  )

  assert all(
    isinstance(
      term,
      TodaTargetPresentation,
    )
    for term in presentation.terms
  )

  assert all(
    presented.source_target
    is source
    for presented, source in zip(
      presentation.terms,
      ehp_result.sequence.terms,
    )
  )


def test_phase96_4_actual_pi9_5_sequence_preserves_delta_e_h_delta_map_order():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  presentation = (
    build_toda_ehp_sequence_presentation(
      candidate
      .explanation
      .ehp_result
    )
  )

  assert tuple(
    presented_map.source_map
    for presented_map in (
      presentation.maps
    )
  ) == (
    EHP_DELTA_MAP,
    EHP_E_MAP,
    EHP_H_MAP,
    EHP_DELTA_MAP,
  )


def test_phase96_4_actual_pi9_5_windows_preserve_window_result_identity():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  ehp_result = (
    candidate
    .explanation
    .ehp_result
  )

  presentation = (
    build_toda_ehp_sequence_presentation(
      ehp_result
    )
  )

  assert len(
    presentation.windows
  ) == 3

  assert all(
    isinstance(
      window,
      TodaEHPExactnessWindowPresentation,
    )
    for window in presentation.windows
  )

  assert all(
    presented.source_window_result
    is source
    for presented, source in zip(
      presentation.windows,
      ehp_result.windows,
    )
  )


def test_phase96_4_window_presentation_preserves_term_and_map_identity():
  data = build_phase92_5_data()

  window_result = (
    data[
      "provenance"
    ].uses[
      0
    ].window_result
  )

  window = (
    window_result.window
  )

  presentation = (
    build_toda_ehp_exactness_window_presentation(
      window_result
    )
  )

  assert (
    presentation.source_term.source_target
    is window.source_term
  )
  assert (
    presentation.middle_term.source_target
    is window.middle_term
  )
  assert (
    presentation.target_term.source_target
    is window.target_term
  )
  assert (
    presentation.first_map.source_map
    is window.first_map
  )
  assert (
    presentation.second_map.source_map
    is window.second_map
  )


def test_phase96_4_exactness_use_preserves_actual_step_and_consumer_identity():
  data = build_phase92_5_data()

  source_use = (
    data[
      "provenance"
    ].uses[
      2
    ]
  )

  presentation = (
    build_toda_ehp_exactness_use_presentation(
      source_use
    )
  )

  assert isinstance(
    presentation,
    TodaEHPExactnessUsePresentation,
  )
  assert (
    presentation.source_use
    is source_use
  )
  assert (
    presentation.exactness_step
    is source_use.exactness_step
  )
  assert all(
    presented is source
    for presented, source in zip(
      presentation.consumer_steps,
      source_use.consumer_steps,
    )
  )


def test_phase96_4_h_delta_exactness_still_exposes_hopf_zero_consumer():
  data = build_phase92_5_data()

  source_use = (
    data[
      "provenance"
    ].uses[
      2
    ]
  )

  presentation = (
    build_toda_ehp_exactness_use_presentation(
      source_use
    )
  )

  assert any(
    consumer
    is data[
      "phase68"
    ][
      "hopf_zero_step"
    ]
    for consumer in (
      presentation.consumer_steps
    )
  )


def test_phase96_4_integrated_exactness_presentation_preserves_provenance_identity():
  data = build_phase92_5_data()

  provenance = data[
    "provenance"
  ]

  presentation = (
    build_toda_ehp_exactness_presentation(
      provenance
    )
  )

  assert isinstance(
    presentation,
    TodaEHPExactnessPresentation,
  )
  assert (
    presentation.source_provenance
    is provenance
  )
  assert (
    presentation.sequence.source_result
    is provenance.ehp_result
  )


def test_phase96_4_integrated_exactness_presentation_preserves_use_order():
  data = build_phase92_5_data()

  provenance = data[
    "provenance"
  ]

  presentation = (
    build_toda_ehp_exactness_presentation(
      provenance
    )
  )

  assert len(
    presentation.uses
  ) == len(
    provenance.uses
  )

  assert all(
    presented.source_use
    is source
    for presented, source in zip(
      presentation.uses,
      provenance.uses,
    )
  )


def test_phase96_4_integrated_windows_match_sequence_windows_by_source_identity():
  data = build_phase92_5_data()

  presentation = (
    build_toda_ehp_exactness_presentation(
      data[
        "provenance"
      ]
    )
  )

  assert all(
    use.window.source_window_result
    is sequence_window.source_window_result
    for use, sequence_window in zip(
      presentation.uses,
      presentation.sequence.windows,
    )
  )


def test_phase96_4_exactness_use_keeps_raw_proof_steps_for_phase96_5():
  data = build_phase92_5_data()

  presentation = (
    build_toda_ehp_exactness_presentation(
      data[
        "provenance"
      ]
    )
  )

  assert all(
    isinstance(
      use.exactness_step,
      ProofStep,
    )
    for use in presentation.uses
  )

  assert all(
    all(
      isinstance(
        consumer,
        ProofStep,
      )
      for consumer in (
        use.consumer_steps
      )
    )
    for use in presentation.uses
  )


def test_phase96_4_map_builder_rejects_non_map_symbol():
  with pytest.raises(
    TypeError,
    match=(
      "map_symbol must be a MapSymbol"
    ),
  ):
    build_toda_ehp_map_presentation(
      "not-a-map"
    )


def test_phase96_4_window_builder_rejects_non_window_result():
  with pytest.raises(
    TypeError,
    match=(
      "window_result must be "
      "a TodaEHPExactnessWindowResult"
    ),
  ):
    build_toda_ehp_exactness_window_presentation(
      "not-a-window-result"
    )


def test_phase96_4_sequence_builder_rejects_non_ehp_result():
  with pytest.raises(
    TypeError,
    match=(
      "ehp_result must be "
      "a TodaEHPSequenceResult"
    ),
  ):
    build_toda_ehp_sequence_presentation(
      "not-an-ehp-result"
    )


def test_phase96_4_use_builder_rejects_non_use_result():
  with pytest.raises(
    TypeError,
    match=(
      "use must be "
      "a TodaEHPExactnessUseResult"
    ),
  ):
    build_toda_ehp_exactness_use_presentation(
      "not-a-use"
    )


def test_phase96_4_exactness_builder_rejects_non_provenance():
  with pytest.raises(
    TypeError,
    match=(
      "provenance must be "
      "a TodaEHPExactnessUseProvenanceResult"
    ),
  ):
    build_toda_ehp_exactness_presentation(
      "not-a-provenance"
    )


def test_phase96_4_use_presentation_rejects_wrong_exactness_step_identity():
  data = build_phase92_5_data()

  source_use = (
    data[
      "provenance"
    ].uses[
      0
    ]
  )

  other_use = (
    data[
      "provenance"
    ].uses[
      1
    ]
  )

  window = (
    build_toda_ehp_exactness_window_presentation(
      source_use.window_result
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "exactness_step identity must match "
      "source_use"
    ),
  ):
    TodaEHPExactnessUsePresentation(
      source_use=source_use,
      window=window,
      exactness_step=(
        other_use.exactness_step
      ),
      consumer_steps=(
        source_use.consumer_steps
      ),
    )


def test_phase96_4_use_presentation_rejects_wrong_window_identity():
  data = build_phase92_5_data()

  source_use = (
    data[
      "provenance"
    ].uses[
      0
    ]
  )

  other_use = (
    data[
      "provenance"
    ].uses[
      1
    ]
  )

  wrong_window = (
    build_toda_ehp_exactness_window_presentation(
      other_use.window_result
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "window source identity must match "
      "source_use.window_result"
    ),
  ):
    TodaEHPExactnessUsePresentation(
      source_use=source_use,
      window=wrong_window,
      exactness_step=(
        source_use.exactness_step
      ),
      consumer_steps=(
        source_use.consumer_steps
      ),
    )


def test_phase96_4_use_result_type_remains_source_model():
  data = build_phase92_5_data()

  presentation = (
    build_toda_ehp_exactness_presentation(
      data[
        "provenance"
      ]
    )
  )

  assert all(
    isinstance(
      use.source_use,
      TodaEHPExactnessUseResult,
    )
    for use in presentation.uses
  )
