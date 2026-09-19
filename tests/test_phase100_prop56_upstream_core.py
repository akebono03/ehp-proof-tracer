from pathlib import Path

from proof import (
  ProofRule,
)
from probes.probe_phase46_capabilities import (
  build_phase46_representative_result,
)
from probes.probe_phase56_capabilities import (
  build_phase56_representative_result,
)
from probes.probe_phase58_capabilities import (
  build_phase58_representative_result,
)
from toda_upstream_bootstrap import (
  build_toda_prop56_upstream_core,
)


def build_phase100_12b1_2_data():
  production = (
    build_toda_prop56_upstream_core()
  )

  phase46 = (
    build_phase46_representative_result(
      n=5,
      k=3,
      m=(
        production[
          "stable_isomorphism_step"
        ]
        .conclusion
        .map
        .target_group
        .sphere_dimension
      ),
    )
  )

  phase56 = (
    build_phase56_representative_result()
  )

  phase58 = (
    build_phase58_representative_result()
  )

  return {
    "production": production,
    "phase46": phase46,
    "phase56": phase56,
    "phase58": phase58,
  }


def test_phase100_12b1_2_production_module_does_not_import_tests_or_probes():
  source = (
    Path(
      "toda_upstream_bootstrap.py"
    )
    .read_text(
      encoding="utf-8",
    )
  )

  assert "from probes." not in source
  assert "from test_phase" not in source


def test_phase100_12b1_2_stable_isomorphism_matches_phase46():
  data = build_phase100_12b1_2_data()

  production_step = data[
    "production"
  ][
    "stable_isomorphism_step"
  ]

  existing_step = data[
    "phase46"
  ][
    "theorem_steps"
  ][
    0
  ]

  assert (
    production_step.conclusion
    == existing_step.conclusion
  )

  assert (
    production_step.rule
    == ProofRule.INFERENCE
  )

  assert production_step is not existing_step


def test_phase100_12b1_2_toda52_matches_phase56():
  data = build_phase100_12b1_2_data()

  production_step = data[
    "production"
  ][
    "toda52_step"
  ]

  existing_step = data[
    "phase56"
  ][
    "composition_isomorphism_steps"
  ][
    0
  ]

  assert (
    production_step.conclusion
    == existing_step.conclusion
  )

  assert (
    production_step.rule
    == ProofRule.INFERENCE
  )

  assert production_step is not existing_step


def test_phase100_12b1_2_nu_prime_membership_matches_phase58():
  data = build_phase100_12b1_2_data()

  production_step = data[
    "production"
  ][
    "membership_step"
  ]

  existing_step = data[
    "phase58"
  ][
    "membership_step"
  ]

  assert (
    production_step.conclusion
    == existing_step.conclusion
  )

  assert (
    production_step.rule
    == ProofRule.INFERENCE
  )

  assert production_step is not existing_step


def test_phase100_12b1_2_nu_prime_hopf_matches_phase58():
  data = build_phase100_12b1_2_data()

  production_step = data[
    "production"
  ][
    "hopf_nu_prime_step"
  ]

  existing_step = data[
    "phase58"
  ][
    "final_hopf_step"
  ]

  assert (
    production_step.conclusion
    == existing_step.conclusion
  )

  assert (
    production_step.rule
    == ProofRule.INFERENCE
  )

  assert production_step is not existing_step


def test_phase100_12b1_2_nu_prime_double_matches_phase58():
  data = build_phase100_12b1_2_data()

  production_step = data[
    "production"
  ][
    "double_step"
  ]

  existing_step = data[
    "phase58"
  ][
    "final_double_step"
  ]

  assert (
    production_step.conclusion
    == existing_step.conclusion
  )

  assert (
    production_step.rule
    == ProofRule.INFERENCE
  )

  assert production_step is not existing_step


def test_phase100_12b1_2_core_has_exact_expected_keys():
  data = build_phase100_12b1_2_data()

  assert tuple(
    data[
      "production"
    ].keys()
  ) == (
    "toda52_step",
    "hopf_nu_prime_step",
    "double_step",
    "membership_step",
    "stable_isomorphism_step",
  )
