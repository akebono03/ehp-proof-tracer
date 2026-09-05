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
from proof import (
  Relation,
  RelationType,
)


def pi_2_1_zero_fact():
  return TodaPrimaryGroupZeroStatement(
    group=TodaPrimaryGroup(
      group_dimension=2,
      sphere_dimension=1,
    ),
  )


def pi_3_3_free_cyclic_fact():
  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  return Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    ),
    rhs=FreeCyclicGroup(
      generator=iota_3,
    ),
    relation_type=RelationType.EQUALITY,
  )


def e_pi_1_1_to_pi_2_2_isomorphism_fact():
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

  return TodaSuspensionIsomorphismStatement(
    map=suspension_map,
  )




