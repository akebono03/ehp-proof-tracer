from pathlib import Path

from proof import (
  ProofRule,
)
from test_phase59_pi5_3_eta3_squared import (
  build_phase59_4_data,
)
from test_phase59_prop53_integration import (
  build_phase59_8_data,
)
from test_phase60_toda48_hopf_parity import (
  build_phase60_7_data,
)
from test_phase62_toda55_integration import (
  build_phase62_6_data,
)
from test_phase63_toda56_integration import (
  build_phase63_6_data,
)
from toda_midstream_bootstrap import (
  build_phase59_hopf_surjective_step,
  build_phase59_pi5_3_step,
  build_phase59_prop53_step,
  build_phase60_pi6_5_step,
  build_phase62_toda55_step,
  build_phase63_toda56_step,
)


def test_phase100_12b1_3_production_module_has_no_test_or_probe_import():
  source = Path(
    "toda_midstream_bootstrap.py"
  ).read_text(
    encoding="utf-8",
  )

  assert "from test_phase" not in source
  assert "from probes." not in source


def test_phase100_12b1_3_pi5_3_matches_phase59():
  data = build_phase59_4_data()

  step = build_phase59_pi5_3_step(
    data[
      "pi4_2_step"
    ],
    data[
      "suspension_isomorphism_step"
    ],
  )

  assert (
    step.conclusion
    == data[
      "final_step"
    ].conclusion
  )

  assert step.rule == ProofRule.INFERENCE
  assert step is not data["final_step"]


def test_phase100_12b1_3_hopf_surjective_matches_phase59():
  data = build_phase59_8_data()

  phase59_4 = data[
    "phase59_4"
  ]
  phase59_3 = phase59_4[
    "phase59_3"
  ]

  step = build_phase59_hopf_surjective_step(
    phase59_3[
      "prop51_step"
    ],
    phase59_3[
      "hopf_eta5_step"
    ],
  )

  existing = next(
    candidate
    for candidate in phase59_3[
      "result"
    ].steps
    if (
      candidate.conclusion
      == phase59_3[
        "expected_hopf_surjective"
      ]
    )
  )

  assert step.conclusion == existing.conclusion
  assert step.rule == ProofRule.INFERENCE
  assert step is not existing


def test_phase100_12b1_3_prop53_matches_phase59():
  data = build_phase59_8_data()

  step = build_phase59_prop53_step(
    data[
      "pi4_2_step"
    ],
    data[
      "pi5_3_step"
    ],
    data[
      "pi6_4_step"
    ],
    data[
      "higher_transport_step"
    ],
    data[
      "higher_range_step"
    ],
  )

  assert (
    step.conclusion
    == data[
      "integration_step"
    ].conclusion
  )

  assert step.rule == ProofRule.INFERENCE
  assert step is not data["integration_step"]


def test_phase100_12b1_3_pi6_5_matches_phase60():
  data = build_phase60_7_data()

  step = build_phase60_pi6_5_step(
    data[
      "prop51_step"
    ],
    data[
      "theorem36_step"
    ],
    data[
      "final_double_step"
    ],
    data[
      "nu_prime_hopf_step"
    ],
  )

  assert (
    step.conclusion
    == data[
      "pi6_5_step"
    ].conclusion
  )

  assert step.rule == ProofRule.INFERENCE
  assert step is not data["pi6_5_step"]


def test_phase100_12b1_3_toda55_matches_phase62():
  data = build_phase62_6_data()

  step = build_phase62_toda55_step(
    data[
      "lemma54_step"
    ],
    data[
      "definition_step"
    ],
    data[
      "n_range_step"
    ],
    data[
      "double_nu_step"
    ],
    data[
      "quadruple_nu_step"
    ],
  )

  assert (
    step.conclusion
    == data[
      "integration_step"
    ].conclusion
  )

  assert step.rule == ProofRule.INFERENCE
  assert step is not data["integration_step"]


def test_phase100_12b1_3_toda56_matches_phase63():
  data = build_phase63_6_data()

  step = build_phase63_toda56_step(
    data[
      "decomposition_step"
    ],
    data[
      "lemma54_step"
    ],
  )

  assert (
    step.conclusion
    == data[
      "integration_step"
    ].conclusion
  )

  assert step.rule == ProofRule.INFERENCE
  assert step is not data["integration_step"]
