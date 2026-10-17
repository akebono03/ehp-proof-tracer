from typing import (
  get_type_hints,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  WhiteheadProduct,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from low_dimensional_facts import (
  pi_4_5_zero_fact,
  pi_5_5_free_cyclic_fact,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


def build_phase50_4c_data():
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )

  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_4_3 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  pi_4_5 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=5,
  )

  iota_5 = HomotopyElement(
    name="ι_5",
    dimension=5,
    generator=GeneratorSymbol(
      family="ι",
      index=5,
    ),
  )

  iota_2 = HomotopyElement(
    name="ι_2",
    dimension=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  whitehead_square = WhiteheadProduct(
    left=iota_2,
    right=iota_2,
  )

  two_eta_2 = Multiple(
    coefficient=2,
    expression=eta_2,
  )

  delta_map = TodaDeltaMap(
    source_group=pi_5_5,
    target_group=pi_3_2,
  )

  delta_up_to_sign = (
    TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=iota_5,
      positive_value=whitehead_square,
    )
  )

  whitehead_up_to_sign = (
    TodaPi32WhiteheadSquareUpToSignStatement(
      whitehead_square=whitehead_square,
      positive_value=two_eta_2,
    )
  )

  delta_image = (
    TodaDeltaImageFreeCyclicStatement(
      map=delta_map,
      image_group=FreeCyclicGroup(
        generator=two_eta_2,
      ),
    )
  )

  delta_e_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_5_5,
        middle_term=pi_3_2,
        target_term=pi_4_3,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      ),
    )
  )

  suspension_map = TodaSuspensionMap(
    source_group=pi_3_2,
    target_group=pi_4_3,
  )

  suspension_kernel = (
    TodaSuspensionKernelFreeCyclicStatement(
      map=suspension_map,
      kernel_group=FreeCyclicGroup(
        generator=two_eta_2,
      ),
    )
  )

  e_h_exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_3_2,
        middle_term=pi_4_3,
        target_term=pi_4_5,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      ),
    )
  )

  suspension_surjective = (
    TodaSuspensionSurjectiveStatement(
      map=suspension_map,
    )
  )

  return {
    "pi_5_5": pi_5_5,
    "pi_3_2": pi_3_2,
    "pi_4_3": pi_4_3,
    "pi_4_5": pi_4_5,
    "iota_5": iota_5,
    "iota_2": iota_2,
    "eta_2": eta_2,
    "whitehead_square": (
      whitehead_square
    ),
    "two_eta_2": two_eta_2,
    "delta_map": delta_map,
    "delta_up_to_sign": (
      delta_up_to_sign
    ),
    "whitehead_up_to_sign": (
      whitehead_up_to_sign
    ),
    "delta_image": delta_image,
    "delta_e_exactness": (
      delta_e_exactness
    ),
    "suspension_map": (
      suspension_map
    ),
    "suspension_kernel": (
      suspension_kernel
    ),
    "e_h_exactness": (
      e_h_exactness
    ),
    "suspension_surjective": (
      suspension_surjective
    ),
  }


def test_phase50_4c_delta_image_statement_uses_specific_delta_map():
  type_hints = get_type_hints(
    TodaDeltaImageFreeCyclicStatement
  )

  assert type_hints[
    "map"
  ] is TodaDeltaMap


def test_phase50_4c_delta_image_statement_uses_free_cyclic_group():
  type_hints = get_type_hints(
    TodaDeltaImageFreeCyclicStatement
  )

  assert type_hints[
    "image_group"
  ] is FreeCyclicGroup


def test_phase50_4c_kernel_statement_uses_specific_suspension_map():
  type_hints = get_type_hints(
    TodaSuspensionKernelFreeCyclicStatement
  )

  assert type_hints[
    "map"
  ] is TodaSuspensionMap


def test_phase50_4c_surjective_statement_uses_specific_suspension_map():
  type_hints = get_type_hints(
    TodaSuspensionSurjectiveStatement
  )

  assert type_hints[
    "map"
  ] is TodaSuspensionMap






def test_phase50_4c_delta_image_is_generated_by_two_eta_2():
  data = build_phase50_4c_data()

  assert data[
    "delta_image"
  ].image_group == (
    FreeCyclicGroup(
      generator=data[
        "two_eta_2"
      ],
    )
  )








def test_phase50_4c_kernel_preserves_two_eta_2():
  data = build_phase50_4c_data()

  assert data[
    "suspension_kernel"
  ].kernel_group == (
    FreeCyclicGroup(
      generator=data[
        "two_eta_2"
      ],
    )
  )
















