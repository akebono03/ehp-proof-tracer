from expression import (
  Composition,
  HomotopyElement,
  Suspension,
  Zero,
)
from generator_facts import (
  ETA_3_GENERATOR,
  NU_PRIME_GENERATOR,
)
from proof import (
  Relation,
  RelationType,
)


ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT = Relation(
  lhs=Composition(
    left=HomotopyElement(
      name="η₃",
      dimension=3,
      generator=ETA_3_GENERATOR,
    ),
    right=Suspension(
      expression=HomotopyElement(
        name="ν′",
        dimension=3,
        generator=NU_PRIME_GENERATOR,
      ),
    ),
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)




