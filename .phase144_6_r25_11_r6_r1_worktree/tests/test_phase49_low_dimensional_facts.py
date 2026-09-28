from typing import (
  get_type_hints,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from low_dimensional_facts import (
  e_pi_1_1_to_pi_2_2_isomorphism_fact,
  pi_2_1_zero_fact,
  pi_3_3_free_cyclic_fact,
)
from map_facts import (
  EHP_E_MAP,
)
from map_property_rules import (
  IsomorphismStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)


def test_phase49_2_zero_group_statement_uses_toda_primary_group():
  type_hints = get_type_hints(
    TodaPrimaryGroupZeroStatement
  )

  assert type_hints[
    "group"
  ] is TodaPrimaryGroup


def test_phase49_2_pi_2_1_zero_fact_has_expected_group():
  fact = pi_2_1_zero_fact()

  assert fact == (
    TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=2,
        sphere_dimension=1,
      ),
    )
  )


def test_phase49_2_pi_2_1_zero_fact_preserves_group_dimension():
  fact = pi_2_1_zero_fact()

  assert fact.group.group_dimension == 2


def test_phase49_2_pi_2_1_zero_fact_preserves_sphere_dimension():
  fact = pi_2_1_zero_fact()

  assert fact.group.sphere_dimension == 1


def test_phase49_2_pi_2_1_zero_fact_is_not_expression_zero_relation():
  fact = pi_2_1_zero_fact()

  assert not isinstance(
    fact,
    Relation,
  )


def test_phase49_2_pi_3_3_fact_is_equality_relation():
  fact = pi_3_3_free_cyclic_fact()

  assert isinstance(
    fact,
    Relation,
  )

  assert fact.relation_type == (
    RelationType.EQUALITY
  )


def test_phase49_2_pi_3_3_fact_has_expected_group():
  fact = pi_3_3_free_cyclic_fact()

  assert fact.lhs == (
    TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    )
  )


def test_phase49_2_pi_3_3_fact_has_free_cyclic_target():
  fact = pi_3_3_free_cyclic_fact()

  assert isinstance(
    fact.rhs,
    FreeCyclicGroup,
  )


def test_phase49_2_pi_3_3_generator_is_iota_3():
  fact = pi_3_3_free_cyclic_fact()

  assert fact.rhs.generator == (
    HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )
  )


def test_phase49_2_pi_3_3_generator_has_dimension_three():
  fact = pi_3_3_free_cyclic_fact()

  assert fact.rhs.generator.dimension == 3


def test_phase49_2_pi_3_3_generator_preserves_generator_family():
  fact = pi_3_3_free_cyclic_fact()

  assert fact.rhs.generator.generator == (
    GeneratorSymbol(
      family="ι",
      index=3,
    )
  )


def test_phase49_2_suspension_isomorphism_statement_uses_specific_map():
  type_hints = get_type_hints(
    TodaSuspensionIsomorphismStatement
  )

  assert type_hints[
    "map"
  ] is TodaSuspensionMap


def test_phase49_2_e_isomorphism_fact_has_expected_source():
  fact = (
    e_pi_1_1_to_pi_2_2_isomorphism_fact()
  )

  assert fact.map.source_group == (
    TodaPrimaryGroup(
      group_dimension=1,
      sphere_dimension=1,
    )
  )


def test_phase49_2_e_isomorphism_fact_has_expected_target():
  fact = (
    e_pi_1_1_to_pi_2_2_isomorphism_fact()
  )

  assert fact.map.target_group == (
    TodaPrimaryGroup(
      group_dimension=2,
      sphere_dimension=2,
    )
  )


def test_phase49_2_e_isomorphism_fact_preserves_specific_map():
  suspension_map = TodaSuspensionMap(
    source_group=TodaPrimaryGroup(
      group_dimension=1,
      sphere_dimension=1,
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=2,
      sphere_dimension=2,
    ),
  )

  assert (
    e_pi_1_1_to_pi_2_2_isomorphism_fact()
    == TodaSuspensionIsomorphismStatement(
      map=suspension_map,
    )
  )


def test_phase49_2_specific_e_isomorphism_is_not_generic_isomorphism():
  specific = (
    e_pi_1_1_to_pi_2_2_isomorphism_fact()
  )

  generic = IsomorphismStatement(
    map=EHP_E_MAP,
  )

  assert specific != generic


def test_phase49_2_specific_e_isomorphism_retains_instance_lost_by_generic():
  first = (
    e_pi_1_1_to_pi_2_2_isomorphism_fact()
  )

  other = TodaSuspensionIsomorphismStatement(
    map=TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=2,
        sphere_dimension=2,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=3,
        sphere_dimension=3,
      ),
    ),
  )

  assert first != other

  assert (
    IsomorphismStatement(
      map=EHP_E_MAP,
    )
    == IsomorphismStatement(
      map=EHP_E_MAP,
    )
  )


def test_phase49_2_low_dimensional_facts_can_be_given_steps():
  facts = (
    pi_2_1_zero_fact(),
    pi_3_3_free_cyclic_fact(),
    e_pi_1_1_to_pi_2_2_isomorphism_fact(),
  )

  steps = tuple(
    ProofStep(
      conclusion=fact,
      premises=(),
      rule=ProofRule.GIVEN,
    )
    for fact in facts
  )

  assert len(
    steps
  ) == 3

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in steps
  )


def test_phase49_2_low_dimensional_facts_are_structurally_distinct():
  facts = (
    pi_2_1_zero_fact(),
    pi_3_3_free_cyclic_fact(),
    e_pi_1_1_to_pi_2_2_isomorphism_fact(),
  )

  assert len(
    set(
      facts
    )
  ) == 3




