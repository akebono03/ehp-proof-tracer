from expression import (
  Multiple,
  Zero,
  eta,
)
from formatter import format_proof
from proof import (
  Relation,
  RelationType,
  relation_inference_proof,
)


relation = Relation(
  lhs=Multiple(
    2,
    eta(3),
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
  source="Toda",
)

proof = relation_inference_proof(
  relation,
  "η_3 has order dividing 2",
)

print(
  format_proof(
    proof
  )
)


