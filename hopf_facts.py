from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from hopf_rules import (
  HopfInvariantStatement,
)
from proof import (
  LiteratureReference,
)


TODA_PROP_5_1_REFERENCE = LiteratureReference(
  label="Toda Prop.5.1",
  author="H. Toda",
  title=(
    "Composition Methods in "
    "Homotopy Groups of Spheres"
  ),
  year=1962,
  locator="Proposition 5.1",
)


ETA_2 = HomotopyElement(
  name="η₂",
  dimension=2,
  source=3,
  target=2,
  generator=GeneratorSymbol(
    family="η",
    index=2,
  ),
)


IOTA_3 = HomotopyElement(
  name="ι₃",
  dimension=3,
  source=3,
  target=3,
  generator=GeneratorSymbol(
    family="ι",
    index=3,
  ),
)


ETA_2_HOPF_INVARIANT_FACT = (
  HopfInvariantStatement(
    expression=ETA_2,
    value=IOTA_3,
    source=TODA_PROP_5_1_REFERENCE,
    note=(
      "Toda Prop.5.1 "
      "H(η₂)=ι₃."
    ),
  )
)



