from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
)
from hopf_facts import (
  IOTA_3,
)
from proof import (
  Relation,
  RelationType,
)


IOTA_1 = HomotopyElement(
  name="ι₁",
  dimension=1,
  source=1,
  target=1,
  generator=GeneratorSymbol(
    family="ι",
    index=1,
  ),
)


IOTA_2 = HomotopyElement(
  name="ι₂",
  dimension=2,
  source=2,
  target=2,
  generator=GeneratorSymbol(
    family="ι",
    index=2,
  ),
)


IOTA_1_SUSPENSION_FACT = Relation(
  lhs=Suspension(
    expression=IOTA_1,
  ),
  rhs=IOTA_2,
  relation_type=RelationType.EQUALITY,
  note=(
    "Suspension of the identity "
    "map ι₁ is ι₂."
  ),
)


IOTA_2_SUSPENSION_FACT = Relation(
  lhs=Suspension(
    expression=IOTA_2,
  ),
  rhs=IOTA_3,
  relation_type=RelationType.EQUALITY,
  note=(
    "Suspension of the identity "
    "map ι₂ is ι₃."
  ),
)




