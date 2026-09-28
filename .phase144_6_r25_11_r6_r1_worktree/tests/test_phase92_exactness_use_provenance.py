from functools import lru_cache

from proof import ProofStep
from test_phase92_actual_ehp_extraction import (
  build_phase92_3_data,
)
from toda_ehp_exactness_provenance import (
  TodaEHPExactnessUseProvenanceResult,
  TodaEHPExactnessUseResult,
  extract_toda_ehp_exactness_use_provenance,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


@lru_cache(maxsize=1)
def build_phase92_5_data():
  phase92_3 = (
    build_phase92_3_data()
  )

  provenance = (
    extract_toda_ehp_exactness_use_provenance(
      phase92_3[
        "group_result"
      ],
      phase92_3[
        "ehp_result"
      ],
    )
  )

  return {
    "phase92_3": phase92_3,
    "phase68": phase92_3[
      "phase68"
    ],
    "provenance": provenance,
  }


def test_phase92_5_returns_exactness_use_provenance_result():
  data = build_phase92_5_data()

  assert isinstance(
    data[
      "provenance"
    ],
    TodaEHPExactnessUseProvenanceResult,
  )


def test_phase92_5_preserves_ehp_result_identity():
  data = build_phase92_5_data()

  assert (
    data[
      "provenance"
    ].ehp_result
    is data[
      "phase92_3"
    ][
      "ehp_result"
    ]
  )


def test_phase92_5_has_one_use_record_per_ehp_window():
  data = build_phase92_5_data()

  provenance = data[
    "provenance"
  ]

  assert len(
    provenance.uses
  ) == len(
    provenance
    .ehp_result
    .windows
  )

  assert all(
    isinstance(
      use,
      TodaEHPExactnessUseResult,
    )
    for use in provenance.uses
  )


def test_phase92_5_preserves_window_order():
  data = build_phase92_5_data()

  provenance = data[
    "provenance"
  ]

  assert tuple(
    use.window_result.window
    for use in provenance.uses
  ) == tuple(
    window_result.window
    for window_result in (
      provenance
      .ehp_result
      .windows
    )
  )


def test_phase92_5_exactness_steps_are_actual_phase68_steps():
  data = build_phase92_5_data()

  phase68 = data[
    "phase68"
  ]

  expected_steps = (
    phase68[
      "delta_e_exactness_step"
    ],
    phase68[
      "e_h_exactness_step"
    ],
    phase68[
      "h_delta_exactness_step"
    ],
  )

  actual_steps = tuple(
    use.exactness_step
    for use in (
      data[
        "provenance"
      ].uses
    )
  )

  assert all(
    actual is expected
    for actual, expected in zip(
      actual_steps,
      expected_steps,
    )
  )


def test_phase92_5_each_exactness_step_has_expected_statement():
  data = build_phase92_5_data()

  assert all(
    isinstance(
      use.exactness_step.conclusion,
      TodaProp42ExactnessStatement,
    )
    for use in (
      data[
        "provenance"
      ].uses
    )
  )


def test_phase92_5_consumers_are_direct_proof_consumers():
  data = build_phase92_5_data()

  for use in (
    data[
      "provenance"
    ].uses
  ):
    assert all(
      isinstance(
        consumer,
        ProofStep,
      )
      for consumer in (
        use.consumer_steps
      )
    )

    assert all(
      any(
        premise
        is use.exactness_step
        for premise in (
          consumer.premises
        )
      )
      for consumer in (
        use.consumer_steps
      )
    )


def test_phase92_5_h_delta_exactness_records_hopf_zero_use():
  data = build_phase92_5_data()

  phase68 = data[
    "phase68"
  ]

  h_delta_use = (
    data[
      "provenance"
    ].uses[
      2
    ]
  )

  assert (
    h_delta_use.exactness_step
    is phase68[
      "h_delta_exactness_step"
    ]
  )

  assert any(
    consumer
    is phase68[
      "hopf_zero_step"
    ]
    for consumer in (
      h_delta_use.consumer_steps
    )
  )


def test_phase92_5_delta_e_exactness_has_actual_direct_consumer():
  data = build_phase92_5_data()

  delta_e_use = (
    data[
      "provenance"
    ].uses[
      0
    ]
  )

  assert (
    delta_e_use.consumer_steps
  )


def test_phase92_5_e_h_exactness_has_actual_direct_consumer():
  data = build_phase92_5_data()

  e_h_use = (
    data[
      "provenance"
    ].uses[
      1
    ]
  )

  assert (
    e_h_use.consumer_steps
  )


def test_phase92_5_does_not_replace_final_group_proof_step():
  data = build_phase92_5_data()

  phase92_3 = data[
    "phase92_3"
  ]

  assert (
    phase92_3[
      "group_result"
    ].proof_step
    is phase92_3[
      "entry"
    ].step
  )


def test_phase92_5_provenance_is_non_destructive():
  data = build_phase92_5_data()

  phase68 = data[
    "phase68"
  ]

  assert (
    phase68[
      "delta_e_exactness_step"
    ].conclusion.window
    is data[
      "provenance"
    ].uses[
      0
    ].window_result.window
  )

  assert (
    phase68[
      "e_h_exactness_step"
    ].conclusion.window
    is data[
      "provenance"
    ].uses[
      1
    ].window_result.window
  )

  assert (
    phase68[
      "h_delta_exactness_step"
    ].conclusion.window
    is data[
      "provenance"
    ].uses[
      2
    ].window_result.window
  )
