from functools import lru_cache

from proof import (
  ProofRule,
  apply_inference_match,
  find_inference_match,
)
from test_phase73_pi8_2_eta2_nu_prime_eta6_squared import (
  build_phase73_3_data,
)
from test_phase73_pi9_3_zero import (
  build_phase73_4_data,
)
from test_phase73_pi10_4_nu4_squared import (
  build_phase73_5_data,
)
from test_phase73_prop511_nu_squared_finite_dimensional import (
  build_phase73_8c_data,
)
from toda_rules import (
  TodaProp511FiniteDimensionalStatement,
  toda_prop511_finite_dimensional_integration_inference_rule,
  toda_prop511_finite_dimensional_literature_statements,
)


@lru_cache(maxsize=1)
def build_phase73_8e_data():
  phase73_3 = (
    build_phase73_3_data()
  )

  phase73_4 = (
    build_phase73_4_data()
  )

  phase73_5 = (
    build_phase73_5_data()
  )

  phase73_8c = (
    build_phase73_8c_data()
  )

  pi8_2_step = (
    phase73_3[
      "final_step"
    ]
  )

  pi9_3_zero_step = (
    phase73_4[
      "final_step"
    ]
  )

  pi10_4_step = (
    phase73_5[
      "final_step"
    ]
  )

  nu_squared_step = (
    phase73_8c[
      "final_step"
    ]
  )

  rule = (
    toda_prop511_finite_dimensional_integration_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      pi8_2_step,
      pi9_3_zero_step,
      pi10_4_step,
      nu_squared_step,
    ),
  )

  assert (
    match
    is not None
  )

  final_step = (
    apply_inference_match(
      match
    )
  )

  return {
    "phase73_3": phase73_3,
    "phase73_4": phase73_4,
    "phase73_5": phase73_5,
    "phase73_8c": phase73_8c,
    "pi8_2_step": pi8_2_step,
    "pi9_3_zero_step": (
      pi9_3_zero_step
    ),
    "pi10_4_step": pi10_4_step,
    "nu_squared_step": (
      nu_squared_step
    ),
    "rule": rule,
    "final_step": final_step,
  }


def test_phase73_8e_derives_prop511_finite_dimensional_aggregate():
  data = build_phase73_8e_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaProp511FiniteDimensionalStatement,
  )


def test_phase73_8e_preserves_pi8_2_branch():
  data = build_phase73_8e_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .pi8_2_group_relation
    == data[
      "pi8_2_step"
    ].conclusion
  )


def test_phase73_8e_preserves_pi9_3_zero_branch():
  data = build_phase73_8e_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .pi9_3_zero
    == data[
      "pi9_3_zero_step"
    ].conclusion
  )


def test_phase73_8e_preserves_pi10_4_branch():
  data = build_phase73_8e_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .pi10_4_group_relation
    == data[
      "pi10_4_step"
    ].conclusion
  )


def test_phase73_8e_preserves_nu_squared_aggregate():
  data = build_phase73_8e_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .nu_squared_finite_dimensional
    == data[
      "nu_squared_step"
    ].conclusion
  )


def test_phase73_8e_attaches_prop511_literature():
  data = build_phase73_8e_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .literature_statements
    == (
      toda_prop511_finite_dimensional_literature_statements()
    )
  )


def test_phase73_8e_final_is_inference():
  data = build_phase73_8e_data()

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_8e_has_exact_four_direct_premises():
  data = build_phase73_8e_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi8_2_step"
      ],
      data[
        "pi9_3_zero_step"
      ],
      data[
        "pi10_4_step"
      ],
      data[
        "nu_squared_step"
      ],
    )
  )



