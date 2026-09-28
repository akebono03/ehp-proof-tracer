from proof import (
  ProofRule,
  ProofStep,
  find_inference_match,
)
from test_phase55_prop51_integration import (
  build_phase55_5_integration,
)
from toda_rules import (
  toda_prop51_finite_dimensional_integration_inference_rule,
)


def test_phase55_6_rejects_given_h_eta2_dependency():
  integration = (
    build_phase55_5_integration()
  )

  given_hopf_step = ProofStep(
    conclusion=integration[
      "eta2_hopf_step"
    ].conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    integration[
      "pi3_2_group_step"
    ],
    given_hopf_step,
    integration[
      "delta_iota5_step"
    ],
    integration[
      "higher_eta_group_step"
    ],
  )

  assert find_inference_match(
    toda_prop51_finite_dimensional_integration_inference_rule(),
    steps,
  ) is None


def test_phase55_6_rejects_given_pi3_2_dependency():
  integration = (
    build_phase55_5_integration()
  )

  given_pi3_2_step = ProofStep(
    conclusion=integration[
      "pi3_2_group_step"
    ].conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    given_pi3_2_step,
    integration[
      "eta2_hopf_step"
    ],
    integration[
      "delta_iota5_step"
    ],
    integration[
      "higher_eta_group_step"
    ],
  )

  assert find_inference_match(
    toda_prop51_finite_dimensional_integration_inference_rule(),
    steps,
  ) is None


def test_phase55_6_rejects_given_delta_dependency():
  integration = (
    build_phase55_5_integration()
  )

  given_delta_step = ProofStep(
    conclusion=integration[
      "delta_iota5_step"
    ].conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    integration[
      "pi3_2_group_step"
    ],
    integration[
      "eta2_hopf_step"
    ],
    given_delta_step,
    integration[
      "higher_eta_group_step"
    ],
  )

  assert find_inference_match(
    toda_prop51_finite_dimensional_integration_inference_rule(),
    steps,
  ) is None


def test_phase55_6_rejects_given_higher_eta_group_dependency():
  integration = (
    build_phase55_5_integration()
  )

  given_higher_eta_step = ProofStep(
    conclusion=integration[
      "higher_eta_group_step"
    ].conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    integration[
      "pi3_2_group_step"
    ],
    integration[
      "eta2_hopf_step"
    ],
    integration[
      "delta_iota5_step"
    ],
    given_higher_eta_step,
  )

  assert find_inference_match(
    toda_prop51_finite_dimensional_integration_inference_rule(),
    steps,
  ) is None


def test_phase55_6_given_prop51_statement_cannot_replace_missing_dependency():
  integration = (
    build_phase55_5_integration()
  )

  given_prop51_step = ProofStep(
    conclusion=integration[
      "expected_statement"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    integration[
      "pi3_2_group_step"
    ],
    integration[
      "delta_iota5_step"
    ],
    integration[
      "higher_eta_group_step"
    ],
    given_prop51_step,
  )

  assert find_inference_match(
    toda_prop51_finite_dimensional_integration_inference_rule(),
    steps,
  ) is None


def test_phase55_6_rejects_pre_direct_delta_result():
  integration = (
    build_phase55_5_integration()
  )

  phase52 = (
    integration[
      "phase52_phase54_dependency"
    ][
      "phase52"
    ]
  )

  wrong_delta_step = (
    phase52[
      "delta_whitehead_steps"
    ][
      0
    ]
  )

  steps = (
    integration[
      "pi3_2_group_step"
    ],
    integration[
      "eta2_hopf_step"
    ],
    wrong_delta_step,
    integration[
      "higher_eta_group_step"
    ],
  )

  assert wrong_delta_step.rule == (
    ProofRule.INFERENCE
  )

  assert find_inference_match(
    toda_prop51_finite_dimensional_integration_inference_rule(),
    steps,
  ) is None


def test_phase55_6_rejects_pre_eta_family_transport_result():
  integration = (
    build_phase55_5_integration()
  )

  phase54 = (
    integration[
      "phase52_phase54_dependency"
    ][
      "phase54"
    ]
  )

  wrong_higher_eta_step = (
    phase54[
      "transported_steps"
    ][
      0
    ]
  )

  steps = (
    integration[
      "pi3_2_group_step"
    ],
    integration[
      "eta2_hopf_step"
    ],
    integration[
      "delta_iota5_step"
    ],
    wrong_higher_eta_step,
  )

  assert wrong_higher_eta_step.rule == (
    ProofRule.INFERENCE
  )

  assert find_inference_match(
    toda_prop51_finite_dimensional_integration_inference_rule(),
    steps,
  ) is None



