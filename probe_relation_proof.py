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
)

relation1 = Relation(
  lhs=Multiple(
    2,
    eta(3),
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
  source=source,
  note="first example relation",
)

relation2 = Relation(
  lhs=Multiple(
    2,
    eta(4),
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
  source=source,
  note="second example relation",
)

proof = relation_inference_proof(
  (
    relation1,
    relation2,
  ),
  "combined result",
  note=(
    "derived from two relations"
  ),
)

print(
  format_proof(
    proof
  )
)



