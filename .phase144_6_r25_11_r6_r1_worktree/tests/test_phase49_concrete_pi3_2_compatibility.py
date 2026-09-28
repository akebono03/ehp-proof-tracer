from typing import (
  get_type_hints,
)

import map_property_rules

from expression import (
  MapSymbol,
)
from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from map_property_rules import (
  InjectiveMapStatement,
  IsomorphismStatement,
  isomorphism_implies_injective_inference_rule,
)
from proof import (
  ExactnessStatement,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from set_rules import (
  ImageSubgroupReference,
  KernelSubgroupReference,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
  TodaProp44SuspensionInjectiveStatement,
)


def test_phase49_1_generic_injective_statement_uses_map_symbol():
  type_hints = get_type_hints(
    InjectiveMapStatement
  )

  assert type_hints[
    "map"
  ] is MapSymbol


def test_phase49_1_generic_isomorphism_statement_uses_map_symbol():
  type_hints = get_type_hints(
    IsomorphismStatement
  )

  assert type_hints[
    "map"
  ] is MapSymbol


def test_phase49_1_generic_h_injectivity_is_representable():
  statement = InjectiveMapStatement(
    map=EHP_H_MAP,
  )

  assert statement.map == EHP_H_MAP


def test_phase49_1_generic_e_isomorphism_is_representable():
  statement = IsomorphismStatement(
    map=EHP_E_MAP,
  )

  assert statement.map == EHP_E_MAP


def test_phase49_1_existing_isomorphism_rule_matches_e_isomorphism():
  step = ProofStep(
    conclusion=IsomorphismStatement(
      map=EHP_E_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    isomorphism_implies_injective_inference_rule(),
    (
      step,
    ),
  )

  assert match is not None


def test_phase49_1_existing_isomorphism_rule_derives_e_injectivity():
  step = ProofStep(
    conclusion=IsomorphismStatement(
      map=EHP_E_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      isomorphism_implies_injective_inference_rule(),
      (
        step,
      ),
    )
  )

  assert InjectiveMapStatement(
    map=EHP_E_MAP,
  ) in tuple(
    derived.conclusion
    for derived in result.steps
  )


def test_phase49_1_surjective_map_statement_does_not_exist_yet():
  assert not hasattr(
    map_property_rules,
    "SurjectiveMapStatement",
  )


def test_phase49_1_no_isomorphism_to_surjective_rule_exists_yet():
  assert not hasattr(
    map_property_rules,
    "isomorphism_implies_surjective_inference_rule",
  )


def test_phase49_1_no_injective_surjective_to_isomorphism_rule_exists_yet():
  assert not hasattr(
    map_property_rules,
    "injective_and_surjective_implies_isomorphism_inference_rule",
  )


def test_phase49_1_exactness_statement_accepts_e_h_map_symbols():
  statement = ExactnessStatement(
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
    is_exact=True,
  )

  assert statement.first_map == EHP_E_MAP
  assert statement.second_map == EHP_H_MAP
  assert statement.is_exact


def test_phase49_1_exactness_statement_accepts_h_delta_map_symbols():
  statement = ExactnessStatement(
    first_map=EHP_H_MAP,
    second_map=EHP_DELTA_MAP,
    is_exact=True,
  )

  assert statement.first_map == EHP_H_MAP
  assert statement.second_map == EHP_DELTA_MAP
  assert statement.is_exact


def test_phase49_1_exactness_statement_accepts_delta_e_map_symbols():
  statement = ExactnessStatement(
    first_map=EHP_DELTA_MAP,
    second_map=EHP_E_MAP,
    is_exact=True,
  )

  assert statement.first_map == EHP_DELTA_MAP
  assert statement.second_map == EHP_E_MAP
  assert statement.is_exact


def test_phase49_1_generic_exactness_does_not_preserve_group_instance():
  statement = ExactnessStatement(
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
    is_exact=True,
  )

  assert not hasattr(
    statement,
    "source_group",
  )

  assert not hasattr(
    statement,
    "middle_group",
  )

  assert not hasattr(
    statement,
    "target_group",
  )


def test_phase49_1_toda_exactness_statement_preserves_low_dimensional_window():
  window = TodaEHPExactnessWindow(
    source_term=TodaPrimaryGroup(
      group_dimension=2,
      sphere_dimension=1,
    ),
    middle_term=TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    ),
    target_term=TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    ),
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  statement = TodaProp42ExactnessStatement(
    window=window,
  )

  assert statement.window == window

  assert statement.window.source_term == (
    TodaPrimaryGroup(
      group_dimension=2,
      sphere_dimension=1,
    )
  )

  assert statement.window.middle_term == (
    TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )
  )

  assert statement.window.target_term == (
    TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    )
  )


def test_phase49_1_image_subgroup_reference_requires_concrete_group_map_contract():
  type_hints = get_type_hints(
    ImageSubgroupReference
  )

  assert type_hints[
    "group_map"
  ].__name__ == "GroupMap"


def test_phase49_1_kernel_subgroup_reference_requires_concrete_group_map_contract():
  type_hints = get_type_hints(
    KernelSubgroupReference
  )

  assert type_hints[
    "group_map"
  ].__name__ == "GroupMap"


def test_phase49_1_symbolic_e_map_is_not_concrete_image_group_map():
  type_hints = get_type_hints(
    ImageSubgroupReference
  )

  assert not isinstance(
    EHP_E_MAP,
    type_hints[
      "group_map"
    ],
  )


def test_phase49_1_symbolic_h_map_is_not_concrete_kernel_group_map():
  type_hints = get_type_hints(
    KernelSubgroupReference
  )

  assert not isinstance(
    EHP_H_MAP,
    type_hints[
      "group_map"
    ],
  )


def test_phase49_1_phase48_specific_e_injectivity_is_not_generic_injectivity():
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

  specific = (
    TodaProp44SuspensionInjectiveStatement(
      map=suspension_map,
    )
  )

  generic = InjectiveMapStatement(
    map=EHP_E_MAP,
  )

  assert specific != generic


def test_phase49_1_phase48_specific_injectivity_preserves_group_instance():
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

  statement = (
    TodaProp44SuspensionInjectiveStatement(
      map=suspension_map,
    )
  )

  assert statement.map.source_group == (
    TodaPrimaryGroup(
      group_dimension=1,
      sphere_dimension=1,
    )
  )

  assert statement.map.target_group == (
    TodaPrimaryGroup(
      group_dimension=2,
      sphere_dimension=2,
    )
  )



