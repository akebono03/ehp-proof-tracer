from expression import (
  ScalarSymbol,
)
from homotopy_groups import (
  HomotopyEHPExactnessWindow,
  HomotopyGroup,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  apply_inference_match,
  find_inference_match,
)
from toda_rules import (
  Toda211OrdinaryEHPApplicabilityStatement,
  Toda211OrdinaryEHPExactnessStatement,
  toda_211_ordinary_ehp_applicability_inference_rule,
  toda_211_ordinary_ehp_exactness_inference_rule,
)


def build_phase72r5_pi10_s5_data():
  window = HomotopyEHPExactnessWindow(
    source_term=HomotopyGroup(
      group_dimension=10,
      sphere_dimension=5,
    ),
    middle_term=HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    ),
    target_term=HomotopyGroup(
      group_dimension=11,
      sphere_dimension=11,
    ),
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  window_step = ProofStep(
    conclusion=window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  applicability_rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  applicability_match = find_inference_match(
    applicability_rule,
    (
      window_step,
    ),
  )

  assert (
    applicability_match
    is not None
  )

  applicability_step = (
    apply_inference_match(
      applicability_match
    )
  )

  exactness_rule = (
    toda_211_ordinary_ehp_exactness_inference_rule()
  )

  exactness_match = find_inference_match(
    exactness_rule,
    (
      applicability_step,
    ),
  )

  assert (
    exactness_match
    is not None
  )

  exactness_step = (
    apply_inference_match(
      exactness_match
    )
  )

  return {
    "window": window,
    "window_step": window_step,
    "applicability_rule": (
      applicability_rule
    ),
    "applicability_step": (
      applicability_step
    ),
    "exactness_rule": exactness_rule,
    "exactness_step": exactness_step,
  }


def test_phase72r5_pi10_s5_applicability_is_inference():
  data = build_phase72r5_pi10_s5_data()

  assert isinstance(
    data[
      "applicability_step"
    ].conclusion,
    Toda211OrdinaryEHPApplicabilityStatement,
  )

  assert (
    data[
      "applicability_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r5_pi10_s5_m_is_odd():
  data = build_phase72r5_pi10_s5_data()

  assert (
    data[
      "applicability_step"
    ].conclusion
    .m_is_odd
    is True
  )


def test_phase72r5_pi10_s5_is_below_three_m_minus_one():
  data = build_phase72r5_pi10_s5_data()

  assert (
    data[
      "applicability_step"
    ].conclusion
    .i_less_than_3m_minus_1
    is True
  )


def test_phase72r5_pi10_s5_exactness_is_inference():
  data = build_phase72r5_pi10_s5_data()

  assert isinstance(
    data[
      "exactness_step"
    ].conclusion,
    Toda211OrdinaryEHPExactnessStatement,
  )

  assert (
    data[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r5_pi10_s5_exactness_is_not_given():
  data = build_phase72r5_pi10_s5_data()

  assert (
    data[
      "exactness_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase72r5_exactness_reuses_original_window():
  data = build_phase72r5_pi10_s5_data()

  assert (
    data[
      "exactness_step"
    ].conclusion.window
    is data[
      "window"
    ]
  )


def test_phase72r5_exactness_provenance_reaches_window():
  data = build_phase72r5_pi10_s5_data()

  assert (
    data[
      "exactness_step"
    ].premises
    == (
      data[
        "applicability_step"
      ],
    )
  )

  assert (
    data[
      "applicability_step"
    ].premises
    == (
      data[
        "window_step"
      ],
    )
  )


def test_phase72r5_accepts_odd_m_above_threshold():
  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=HomotopyGroup(
        group_dimension=10,
        sphere_dimension=3,
      ),
      middle_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=4,
      ),
      target_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=7,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      window_step,
    ),
  )

  assert (
    match
    is not None
  )

  step = apply_inference_match(
    match
  )

  assert (
    step.conclusion.m_is_odd
    is True
  )

  assert (
    step.conclusion
    .i_less_than_3m_minus_1
    is False
  )


def test_phase72r5_accepts_even_m_below_threshold():
  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=HomotopyGroup(
        group_dimension=10,
        sphere_dimension=4,
      ),
      middle_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=5,
      ),
      target_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=9,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      window_step,
    ),
  )

  assert (
    match
    is not None
  )

  step = apply_inference_match(
    match
  )

  assert (
    step.conclusion.m_is_odd
    is False
  )

  assert (
    step.conclusion
    .i_less_than_3m_minus_1
    is True
  )


def test_phase72r5_rejects_even_m_at_threshold():
  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=4,
      ),
      middle_term=HomotopyGroup(
        group_dimension=12,
        sphere_dimension=5,
      ),
      target_term=HomotopyGroup(
        group_dimension=12,
        sphere_dimension=9,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      window_step,
    ),
  ) is None


def test_phase72r5_rejects_even_m_above_threshold():
  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=HomotopyGroup(
        group_dimension=12,
        sphere_dimension=4,
      ),
      middle_term=HomotopyGroup(
        group_dimension=13,
        sphere_dimension=5,
      ),
      target_term=HomotopyGroup(
        group_dimension=13,
        sphere_dimension=9,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      window_step,
    ),
  ) is None


def test_phase72r5_rejects_m_equal_one():
  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=HomotopyGroup(
        group_dimension=2,
        sphere_dimension=1,
      ),
      middle_term=HomotopyGroup(
        group_dimension=3,
        sphere_dimension=2,
      ),
      target_term=HomotopyGroup(
        group_dimension=3,
        sphere_dimension=3,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      window_step,
    ),
  ) is None


def test_phase72r5_rejects_wrong_middle_term():
  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=HomotopyGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      middle_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=7,
      ),
      target_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=11,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      window_step,
    ),
  ) is None


def test_phase72r5_rejects_wrong_target_term():
  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=HomotopyGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      middle_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
      target_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=12,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      window_step,
    ),
  ) is None


def test_phase72r5_rejects_wrong_first_map():
  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=HomotopyGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      middle_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
      target_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=11,
      ),
      first_map=EHP_H_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      window_step,
    ),
  ) is None


def test_phase72r5_rejects_wrong_second_map():
  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=HomotopyGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      middle_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
      target_term=HomotopyGroup(
        group_dimension=11,
        sphere_dimension=11,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_DELTA_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      window_step,
    ),
  ) is None


def test_phase72r5_rejects_symbolic_i():
  i = ScalarSymbol(
    name="i",
  )

  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=HomotopyGroup(
        group_dimension=i,
        sphere_dimension=5,
      ),
      middle_term=HomotopyGroup(
        group_dimension=i,
        sphere_dimension=6,
      ),
      target_term=HomotopyGroup(
        group_dimension=i,
        sphere_dimension=11,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      window_step,
    ),
  ) is None


def test_phase72r5_rejects_primary_group_terms():
  window_step = ProofStep(
    conclusion=HomotopyEHPExactnessWindow(
      source_term=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      middle_term=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
      target_term=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=11,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_211_ordinary_ehp_applicability_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      window_step,
    ),
  ) is None


def test_phase72r5_exactness_rejects_given_applicability():
  data = build_phase72r5_pi10_s5_data()

  given_applicability = ProofStep(
    conclusion=(
      data[
        "applicability_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "exactness_rule"
    ],
    (
      given_applicability,
    ),
  ) is None


