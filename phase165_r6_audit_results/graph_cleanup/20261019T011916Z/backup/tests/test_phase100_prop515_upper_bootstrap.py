from pathlib import Path

from expression import (
  GeneratorSymbol,
  ScalarSum,
  ScalarSymbol,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase75_prop515_integration import (
  build_phase75_9_data,
)
from toda_prop515_upper_bootstrap import (
  TodaProp515UpperBootstrapResult,
  build_toda_prop515_upper_bootstrap,
)
from toda_rules import (
  Toda515Sigma8Prop44SpecializationStatement,
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp515FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
)


def test_phase100_12b4_4_production_module_has_no_test_or_probe_imports():
  source = Path(
    "toda_prop515_upper_bootstrap.py"
  ).read_text(
    encoding="utf-8",
  )

  assert "from test_" not in source
  assert "import test_" not in source
  assert "from probes" not in source
  assert "import probes" not in source


def test_phase100_12b4_4_builds_typed_upper_result():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  assert isinstance(
    result,
    TodaProp515UpperBootstrapResult,
  )


def test_phase100_12b4_4_upper_mathematical_steps_are_inference():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      result.specialization_step,
      result.prop44_isomorphism_step,
      result.transported_decomposition_step,
      result.pi15_8_step,
      result.sigma_family_step,
      result.sigma9_definition_step,
      result.prop48_step,
      result.pi16_9_step,
      result.stable_isomorphism_step,
      result.higher_step,
      result.aggregate_step,
    )
  )


def test_phase100_12b4_4_preserves_structural_given_boundary():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  assert (
    result.decomposition_map_step.rule
    == ProofRule.GIVEN
  )

  assert (
    result.pi15_15_step.rule
    == ProofRule.GIVEN
  )

  assert (
    result.higher_range_step.rule
    == ProofRule.GIVEN
  )


def test_phase100_12b4_4_derives_sigma8_prop44_transport():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  assert isinstance(
    result
    .specialization_step
    .conclusion,
    Toda515Sigma8Prop44SpecializationStatement,
  )

  assert isinstance(
    result
    .transported_decomposition_step
    .conclusion,
    Toda515Sigma8TransportedDecompositionStatement,
  )


def test_phase100_12b4_4_derives_pi15_8_expected_mixed_group():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  relation = (
    result.pi15_8_step.conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=8,
    )
  )

  assert isinstance(
    relation.rhs,
    DirectSumGroup,
  )

  assert isinstance(
    relation.rhs.summands[0],
    FreeCyclicGroup,
  )

  assert (
    relation.rhs
    .summands[0]
    .generator
    .generator
    == GeneratorSymbol(
      family="σ",
      index=8,
    )
  )

  assert isinstance(
    relation.rhs.summands[1],
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs
    .summands[1]
    .order
    == 8
  )

  assert isinstance(
    relation.rhs
    .summands[1]
    .generator,
    Suspension,
  )


def test_phase100_12b4_4_derives_sigma_family_and_pi16_9():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  assert isinstance(
    result
    .sigma_family_step
    .conclusion,
    TodaSigmaFamilyDefinitionStatement,
  )

  assert isinstance(
    result
    .sigma9_definition_step
    .conclusion,
    TodaSigmaFamilyDefinitionStatement,
  )

  assert (
    result
    .sigma9_definition_step
    .conclusion
    .index
    == 9
  )

  relation = (
    result.pi16_9_step.conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=9,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 16

  assert (
    relation.rhs
    .generator
    .generator
    == GeneratorSymbol(
      family="σ",
      index=9,
    )
  )


def test_phase100_12b4_4_derives_stable_higher_seven_stem():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  relation = (
    result.higher_step.conclusion
  )

  n = ScalarSymbol(
    name="n",
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=7,
      ),
      sphere_dimension=n,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 16

  assert (
    relation.rhs
    .generator
    .generator
    == GeneratorSymbol(
      family="σ",
      index=n,
    )
  )

  assert (
    result
    .higher_range_step
    .conclusion
    == ScalarGreaterEqualStatement(
      left=n,
      right=9,
    )
  )


def test_phase100_12b4_4_derives_prop515_aggregate():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  assert isinstance(
    result
    .aggregate_step
    .conclusion,
    TodaProp515FiniteDimensionalStatement,
  )

  assert (
    result.aggregate_step.premises
    == (
      result
      .sigma_chain_result
      .low_result
      .pi9_2_zero_step,
      result
      .sigma_chain_result
      .low_result
      .pi10_3_zero_step,
      result
      .sigma_chain_result
      .low_result
      .pi11_4_zero_step,
      result
      .sigma_chain_result
      .low_result
      .pi12_5_step,
      result
      .sigma_chain_result
      .pi13_6_step,
      result
      .sigma_chain_result
      .pi14_7_step,
      result.pi15_8_step,
      result.higher_step,
      result.higher_range_step,
    )
  )


def test_phase100_12b4_4_matches_phase75_terminal_conclusions():
  production = (
    build_toda_prop515_upper_bootstrap()
  )

  phase75 = (
    build_phase75_9_data()
  )

  assert (
    production.pi15_8_step.conclusion
    == phase75[
      "pi15_8_step"
    ].conclusion
  )

  assert (
    production.higher_step.conclusion
    == phase75[
      "higher_step"
    ].conclusion
  )

  assert (
    production.aggregate_step.conclusion
    == phase75[
      "aggregate_step"
    ].conclusion
  )
