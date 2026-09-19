from pathlib import Path

from expression import (
  GeneratorSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  Relation,
)
from test_phase75_pi12_5_order_two import (
  build_phase75_5_data,
)
from toda_prop515_low_bootstrap import (
  TodaProp515LowBootstrapResult,
  build_toda_prop515_low_bootstrap,
)
from toda_rules import (
  TodaLemma513Statement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
)


def test_phase100_12b4_2_production_module_has_no_test_or_probe_imports():
  source = Path(
    "toda_prop515_low_bootstrap.py"
  ).read_text(
    encoding="utf-8",
  )

  assert "from test_" not in source
  assert "import test_" not in source
  assert "from probes" not in source
  assert "import probes" not in source


def test_phase100_12b4_2_builds_typed_low_bootstrap_result():
  result = (
    build_toda_prop515_low_bootstrap()
  )

  assert isinstance(
    result,
    TodaProp515LowBootstrapResult,
  )


def test_phase100_12b4_2_matches_phase75_low_branch_conclusions():
  production = (
    build_toda_prop515_low_bootstrap()
  )

  phase75 = (
    build_phase75_5_data()
  )

  phase75_4 = phase75[
    "phase75_4"
  ]

  phase75_3 = phase75_4[
    "phase75_3"
  ]

  assert (
    production
    .pi9_2_zero_step
    .conclusion
    == phase75_3[
      "phase75_2"
    ][
      "final_step"
    ].conclusion
  )

  assert (
    production
    .pi10_3_zero_step
    .conclusion
    == phase75_3[
      "final_step"
    ].conclusion
  )

  assert (
    production
    .pi11_4_zero_step
    .conclusion
    == phase75_4[
      "final_step"
    ].conclusion
  )

  assert (
    production
    .pi12_5_step
    .conclusion
    == phase75[
      "final_step"
    ].conclusion
  )


def test_phase100_12b4_2_low_mathematical_branches_are_inference():
  result = (
    build_toda_prop515_low_bootstrap()
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      result.pi9_2_zero_step,
      result.pi10_3_zero_step,
      result.pi11_4_zero_step,
      result.pi12_9_step,
      result.hopf_isomorphism_step,
      result.lemma513_step,
      result.pi12_5_step,
    )
  )


def test_phase100_12b4_2_low_groups_have_expected_targets():
  result = (
    build_toda_prop515_low_bootstrap()
  )

  assert (
    result
    .pi9_2_zero_step
    .conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=2,
      ),
    )
  )

  assert (
    result
    .pi10_3_zero_step
    .conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=3,
      ),
    )
  )

  assert (
    result
    .pi11_4_zero_step
    .conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=4,
      ),
    )
  )

  pi12_5_relation = (
    result
    .pi12_5_step
    .conclusion
  )

  assert isinstance(
    pi12_5_relation,
    Relation,
  )

  assert (
    pi12_5_relation.lhs
    == TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=5,
    )
  )

  assert isinstance(
    pi12_5_relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    pi12_5_relation.rhs.order
    == 2
  )


def test_phase100_12b4_2_derives_lemma513_sigma_triple_prime():
  result = (
    build_toda_prop515_low_bootstrap()
  )

  statement = (
    result
    .lemma513_step
    .conclusion
  )

  assert isinstance(
    statement,
    TodaLemma513Statement,
  )

  assert (
    result
    .lemma513_step
    .rule
    == ProofRule.INFERENCE
  )

  assert (
    statement
    .sigma_triple_prime
    .generator
    == GeneratorSymbol(
      family="σ",
      decoration="'''",
    )
  )

  assert (
    statement
    .sigma_triple_prime
    .source
    == 12
  )

  assert (
    statement
    .sigma_triple_prime
    .target
    == 5
  )


def test_phase100_12b4_2_lemma513_preserves_exact_phase75_provenance_shape():
  result = (
    build_toda_prop515_low_bootstrap()
  )

  assert isinstance(
    result
    .hopf_isomorphism_step
    .conclusion,
    TodaProp515Pi12_5HopfIsomorphismStatement,
  )

  assert (
    result
    .lemma513_step
    .premises
    == (
      result.hopf_isomorphism_step,
      result.toda55_step,
    )
  )

  assert (
    result
    .pi12_5_step
    .premises
    == (
      result.hopf_isomorphism_step,
      result.lemma513_step,
    )
  )


def test_phase100_12b4_2_reuses_existing_production_roots():
  result = (
    build_toda_prop515_low_bootstrap()
  )

  assert (
    result.prop56_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    result.prop58_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    result.prop511_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    result.toda52_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    result.prop59_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    result.toda56_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    result.toda55_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    result.delta_nu9_step.rule
    == ProofRule.INFERENCE
  )
