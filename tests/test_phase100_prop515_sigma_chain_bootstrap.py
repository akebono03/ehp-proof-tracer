from pathlib import Path

from expression import (
  GeneratorSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  Relation,
)
from test_phase75_lemma514_sigma8 import (
  build_phase75_8a_data,
)
from toda_prop515_sigma_chain_bootstrap import (
  TodaProp515SigmaChainBootstrapResult,
  build_toda_prop515_sigma_chain_bootstrap,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda514FirstShortExactStatement,
  Toda514SecondShortExactStatement,
  TodaLemma514SigmaDoublePrimeStatement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma514Sigma8Statement,
)


def test_phase100_12b4_3_production_module_has_no_test_or_probe_imports():
  source = Path(
    "toda_prop515_sigma_chain_bootstrap.py"
  ).read_text(
    encoding="utf-8",
  )

  assert "from test_" not in source
  assert "import test_" not in source
  assert "from probes" not in source
  assert "import probes" not in source


def test_phase100_12b4_3_builds_typed_sigma_chain_result():
  result = (
    build_toda_prop515_sigma_chain_bootstrap()
  )

  assert isinstance(
    result,
    TodaProp515SigmaChainBootstrapResult,
  )


def test_phase100_12b4_3_sigma_chain_steps_are_inference():
  result = (
    build_toda_prop515_sigma_chain_bootstrap()
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      result.first_short_exact_step,
      result.bridge_step,
      result.sigma_double_prime_step,
      result.pi13_6_step,
      result.pi14_13_step,
      result.second_short_exact_step,
      result.sigma_prime_step,
      result.pi14_7_step,
      result.sigma8_step,
    )
  )


def test_phase100_12b4_3_derives_both_short_exact_sequences():
  result = (
    build_toda_prop515_sigma_chain_bootstrap()
  )

  assert isinstance(
    result
    .first_short_exact_step
    .conclusion,
    Toda514FirstShortExactStatement,
  )

  assert isinstance(
    result
    .second_short_exact_step
    .conclusion,
    Toda514SecondShortExactStatement,
  )


def test_phase100_12b4_3_derives_sigma_double_prime_and_pi13_6():
  result = (
    build_toda_prop515_sigma_chain_bootstrap()
  )

  assert isinstance(
    result
    .bridge_step
    .conclusion,
    Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  )

  assert isinstance(
    result
    .sigma_double_prime_step
    .conclusion,
    TodaLemma514SigmaDoublePrimeStatement,
  )

  sigma_double_prime = (
    result
    .sigma_double_prime_step
    .conclusion
    .sigma_double_prime
  )

  assert (
    sigma_double_prime.generator
    == GeneratorSymbol(
      family="σ",
      decoration="''",
    )
  )

  relation = (
    result
    .pi13_6_step
    .conclusion
  )

  assert isinstance(
    relation,
    Relation,
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=6,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 4
  assert (
    relation.rhs.generator
    == sigma_double_prime
  )


def test_phase100_12b4_3_derives_sigma_prime_and_pi14_7():
  result = (
    build_toda_prop515_sigma_chain_bootstrap()
  )

  assert isinstance(
    result
    .sigma_prime_step
    .conclusion,
    TodaLemma514SigmaPrimeStatement,
  )

  sigma_prime = (
    result
    .sigma_prime_step
    .conclusion
    .sigma_prime
  )

  assert (
    sigma_prime.generator
    == GeneratorSymbol(
      family="σ",
      decoration="'",
    )
  )

  relation = (
    result
    .pi14_7_step
    .conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=7,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 8
  assert (
    relation.rhs.generator
    == sigma_prime
  )


def test_phase100_12b4_3_derives_sigma8_with_theorem36_provenance():
  result = (
    build_toda_prop515_sigma_chain_bootstrap()
  )

  statement = (
    result
    .sigma8_step
    .conclusion
  )

  assert isinstance(
    statement,
    TodaLemma514Sigma8Statement,
  )

  assert (
    statement.sigma8.generator
    == GeneratorSymbol(
      family="σ",
      index=8,
    )
  )

  assert (
    statement.theorem36_bridge
    == result
    .bridge_step
    .conclusion
  )

  assert (
    statement.sigma_prime_statement
    == result
    .sigma_prime_step
    .conclusion
  )


def test_phase100_12b4_3_sigma8_matches_phase75_conclusion():
  production = (
    build_toda_prop515_sigma_chain_bootstrap()
  )

  phase75 = (
    build_phase75_8a_data()
  )

  assert (
    production
    .sigma8_step
    .conclusion
    == phase75[
      "sigma8_step"
    ].conclusion
  )


def test_phase100_12b4_3_preserves_phase75_terminal_provenance_shapes():
  result = (
    build_toda_prop515_sigma_chain_bootstrap()
  )

  assert (
    result
    .sigma_double_prime_step
    .premises
    == (
      result.bridge_step,
      result.first_short_exact_step,
      result.low_result.pi12_5_step,
      result.pi13_11_step,
    )
  )

  assert (
    result
    .sigma_prime_step
    .premises
    == (
      result.sigma_double_prime_step,
      result.second_short_exact_step,
      result.pi13_6_step,
      result.pi14_13_step,
    )
  )

  assert (
    result
    .sigma8_step
    .premises
    == (
      result.bridge_step,
      result.sigma_prime_step,
      result.pi14_7_step,
    )
  )
