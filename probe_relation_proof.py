from expression import (
  Multiple,
  Zero,
  eta,
)
from formatter import format_proof
from proof import (
  LiteratureReference,
  Relation,
  RelationType,
  relation_inference_proof,
)


source = LiteratureReference(
  label="Toda",
  author="H. Toda",
  title=(
    "Composition Methods in "
    "Homotopy Groups of Spheres"
  ),
  year=1962,
  locator="Proposition X",
)

relation = Relation(
  lhs=Multiple(
    2,
    eta(3),
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
  source=source,
  note="classical eta relation",
)

proof = relation_inference_proof(
  relation,
  "η_3 has order dividing 2",
  note="derived from the zero relation",
)

print(
  format_proof(
    proof
  )
)



