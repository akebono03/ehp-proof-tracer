from expression import (
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteHomotopyGroupStatement,
  HomotopyGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  apply_inference_match,
  find_inference_match,
)
from toda_rules import (
  serre_42_finite_homotopy_group_inference_rule,
)


def build_phase72r4_pi10_s5_data():
  group = HomotopyGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  group_step = ProofStep(
    conclusion=group,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    serre_42_finite_homotopy_group_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      group_step,
    ),
  )

  assert (
    match
    is not None
  )

  finite_step = (
    apply_inference_match(
      match
    )
  )

  return {
    "group": group,
    "group_step": group_step,
    "rule": rule,
    "finite_step": finite_step,
  }


def test_phase72r4_pi10_s5_is_finite():
  data = (
    build_phase72r4_pi10_s5_data()
  )

  assert isinstance(
    data[
      "finite_step"
    ].conclusion,
    FiniteHomotopyGroupStatement,
  )

  assert (
    data[
      "finite_step"
    ].conclusion.group
    == HomotopyGroup(
      group_dimension=10,
      sphere_dimension=5,
    )
  )


def test_phase72r4_pi10_s5_finiteness_is_inference():
  data = (
    build_phase72r4_pi10_s5_data()
  )

  assert (
    data[
      "finite_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r4_pi10_s5_finiteness_is_not_given():
  data = (
    build_phase72r4_pi10_s5_data()
  )

  assert (
    data[
      "finite_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase72r4_reuses_original_group_object():
  data = (
    build_phase72r4_pi10_s5_data()
  )

  assert (
    data[
      "finite_step"
    ].conclusion.group
    is data[
      "group"
    ]
  )


def test_phase72r4_rejects_i_equal_n():
  group_step = ProofStep(
    conclusion=HomotopyGroup(
      group_dimension=5,
      sphere_dimension=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    serre_42_finite_homotopy_group_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      group_step,
    ),
  ) is None


def test_phase72r4_rejects_i_equal_two_n_minus_one():
  group_step = ProofStep(
    conclusion=HomotopyGroup(
      group_dimension=9,
      sphere_dimension=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    serre_42_finite_homotopy_group_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      group_step,
    ),
  ) is None


def test_phase72r4_accepts_another_nonexceptional_group():
  group_step = ProofStep(
    conclusion=HomotopyGroup(
      group_dimension=8,
      sphere_dimension=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    serre_42_finite_homotopy_group_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      group_step,
    ),
  )

  assert (
    match
    is not None
  )

  finite_step = (
    apply_inference_match(
      match
    )
  )

  assert (
    finite_step.conclusion
    == FiniteHomotopyGroupStatement(
      group=HomotopyGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
    )
  )


def test_phase72r4_rejects_symbolic_group_dimension():
  i = ScalarSymbol(
    name="i",
  )

  group_step = ProofStep(
    conclusion=HomotopyGroup(
      group_dimension=i,
      sphere_dimension=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    serre_42_finite_homotopy_group_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      group_step,
    ),
  ) is None


def test_phase72r4_rejects_symbolic_sphere_dimension():
  n = ScalarSymbol(
    name="n",
  )

  group_step = ProofStep(
    conclusion=HomotopyGroup(
      group_dimension=10,
      sphere_dimension=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    serre_42_finite_homotopy_group_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      group_step,
    ),
  ) is None


def test_phase72r4_does_not_apply_to_toda_primary_group():
  group_step = ProofStep(
    conclusion=TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    serre_42_finite_homotopy_group_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      group_step,
    ),
  ) is None


