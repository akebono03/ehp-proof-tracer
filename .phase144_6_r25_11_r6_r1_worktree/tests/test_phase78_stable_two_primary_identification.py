import pytest

from homotopy_groups import (
  StableHomotopyGroup,
  StablePrimaryComponent,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
)
from toda_rules import (
  Toda45StableTwoPrimaryIdentificationStatement,
  toda_45_stable_two_primary_identification_inference_rule,
)


def given_step(
  conclusion,
):
  return ProofStep(
    conclusion=conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )


@pytest.mark.parametrize(
  (
    "stem",
    "sphere_dimension",
  ),
  (
    (1, 3),
    (2, 4),
    (3, 5),
    (4, 6),
    (5, 7),
    (6, 8),
    (7, 9),
  ),
)
def test_phase78_5_stable_range_anchor_is_accepted(
  stem,
  sphere_dimension,
):
  source_group = TodaPrimaryGroup(
    group_dimension=(
      sphere_dimension
      + stem
    ),
    sphere_dimension=(
      sphere_dimension
    ),
  )

  source_step = given_step(
    source_group
  )

  rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  assert rule.match_guard(
    (
      source_step,
    ),
    {},
  )


@pytest.mark.parametrize(
  (
    "stem",
    "sphere_dimension",
  ),
  (
    (1, 3),
    (2, 4),
    (3, 5),
    (4, 6),
    (5, 7),
    (6, 8),
    (7, 9),
  ),
)
def test_phase78_5_stable_range_anchor_builds_expected_component(
  stem,
  sphere_dimension,
):
  source_group = TodaPrimaryGroup(
    group_dimension=(
      sphere_dimension
      + stem
    ),
    sphere_dimension=(
      sphere_dimension
    ),
  )

  source_step = given_step(
    source_group
  )

  rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  conclusion = rule.conclusion_builder(
    (
      source_step,
    )
  )

  assert conclusion == (
    Toda45StableTwoPrimaryIdentificationStatement(
      source_group=source_group,
      target_component=StablePrimaryComponent(
        group=StableHomotopyGroup(
          stem=stem,
        ),
        prime=2,
      ),
    )
  )


def test_phase78_5_g7_anchor_is_pi16_9():
  source_group = TodaPrimaryGroup(
    group_dimension=16,
    sphere_dimension=9,
  )

  source_step = given_step(
    source_group
  )

  rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  conclusion = rule.conclusion_builder(
    (
      source_step,
    )
  )

  assert conclusion.source_group == (
    TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=9,
    )
  )

  assert conclusion.target_component == (
    StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=7,
      ),
      prime=2,
    )
  )


def test_phase78_5_rejects_below_stable_range():
  source_group = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  source_step = given_step(
    source_group
  )

  rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  assert not rule.match_guard(
    (
      source_step,
    ),
    {},
  )


def test_phase78_5_rejects_diagonal_g0_branch():
  source_group = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=9,
  )

  source_step = given_step(
    source_group
  )

  rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  assert not rule.match_guard(
    (
      source_step,
    ),
    {},
  )


def test_phase78_5_rejects_negative_stem():
  source_group = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=9,
  )

  source_step = given_step(
    source_group
  )

  rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  assert not rule.match_guard(
    (
      source_step,
    ),
    {},
  )


def test_phase78_5_statement_has_no_e_infinity_map():
  statement = (
    Toda45StableTwoPrimaryIdentificationStatement(
      source_group=TodaPrimaryGroup(
        group_dimension=16,
        sphere_dimension=9,
      ),
      target_component=StablePrimaryComponent(
        group=StableHomotopyGroup(
          stem=7,
        ),
        prime=2,
      ),
    )
  )

  assert not hasattr(
    statement,
    "map",
  )

  assert not hasattr(
    statement,
    "exponent",
  )

  assert not hasattr(
    statement,
    "generator",
  )

  assert not hasattr(
    statement,
    "group_structure",
  )


def test_phase78_5_statement_is_distinct_from_finite_stage_toda45():
  statement = (
    Toda45StableTwoPrimaryIdentificationStatement(
      source_group=TodaPrimaryGroup(
        group_dimension=16,
        sphere_dimension=9,
      ),
      target_component=StablePrimaryComponent(
        group=StableHomotopyGroup(
          stem=7,
        ),
        prime=2,
      ),
    )
  )

  assert statement.__class__.__name__ == (
    "Toda45StableTwoPrimaryIdentificationStatement"
  )


