from expression import (
  Zero,
)
from proof import (
  Relation,
  RelationType,
  relation_proof_step,
)
from probes.probe_phase42_capabilities import (
  build_phase42_representative_whitehead_product,
  whitehead_product_text,
)


def print_separator():
  print("=" * 72)


def phase43_relation_text(
  relation,
):
  if (
    relation.relation_type
    == RelationType.ZERO
  ):
    symbol = "="
  elif (
    relation.relation_type
    == RelationType.INEQUALITY
  ):
    symbol = "!="
  else:
    symbol = relation.relation_type.value

  if isinstance(
    relation.rhs,
    Zero,
  ):
    rhs_text = "0"
  else:
    rhs_text = str(
      relation.rhs
    )

  return (
    f"{whitehead_product_text(relation.lhs)} "
    f"{symbol} "
    f"{rhs_text}"
  )


def build_phase43_representative_premises():
  phase42 = (
    build_phase42_representative_whitehead_product()
  )

  product = phase42[
    "whitehead_product"
  ]

  zero_premise = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  nonzero_premise = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.INEQUALITY,
  )

  zero_step = relation_proof_step(
    zero_premise
  )

  nonzero_step = relation_proof_step(
    nonzero_premise
  )

  return {
    "whitehead_product": product,
    "zero_premise": zero_premise,
    "nonzero_premise": nonzero_premise,
    "zero_step": zero_step,
    "nonzero_step": nonzero_step,
  }


def print_phase43_representation(
  result,
):
  print_separator()
  print(
    "Toda Lemma 4.1 "
    "premise minimum representation"
  )
  print_separator()
  print()

  print(
    "[1] Representative Whitehead product"
  )
  print(
    " ",
    whitehead_product_text(
      result[
        "whitehead_product"
      ]
    ),
  )

  print()
  print(
    "[2] Zero premise"
  )
  print(
    " ",
    phase43_relation_text(
      result[
        "zero_premise"
      ]
    ),
  )

  print()
  print(
    "[3] Nonzero premise"
  )
  print(
    " ",
    phase43_relation_text(
      result[
        "nonzero_premise"
      ]
    ),
  )


def print_phase43_distinction(
  result,
):
  print()
  print_separator()
  print("Structural / relation distinction")
  print_separator()
  print()

  zero_premise = result[
    "zero_premise"
  ]

  nonzero_premise = result[
    "nonzero_premise"
  ]

  print(
    "ZERO != INEQUALITY =",
    zero_premise
    != nonzero_premise,
  )

  print(
    "zero relation type =",
    zero_premise.relation_type.value,
  )

  print(
    "nonzero relation type =",
    nonzero_premise.relation_type.value,
  )

  print(
    "same WhiteheadProduct lhs =",
    zero_premise.lhs
    == nonzero_premise.lhs,
  )

  print(
    "same Zero rhs =",
    zero_premise.rhs
    == nonzero_premise.rhs,
  )


def print_phase43_proof_premises(
  result,
):
  print()
  print_separator()
  print("Explicit proof premises")
  print_separator()
  print()

  print(
    "zero premise proof step =",
    phase43_relation_text(
      result[
        "zero_step"
      ].conclusion
    ),
  )

  print(
    "nonzero premise proof step =",
    phase43_relation_text(
      result[
        "nonzero_step"
      ].conclusion
    ),
  )


def print_phase43_boundary(
  result,
):
  print()
  print_separator()
  print("Phase 43 completion boundary")
  print_separator()
  print()

  product = result[
    "whitehead_product"
  ]

  zero_premise = result[
    "zero_premise"
  ]

  nonzero_premise = result[
    "nonzero_premise"
  ]

  print("Now representable:")
  print(
    "  [ι₄,ι₄] = 0"
  )
  print(
    "  [ι₄,ι₄] != 0"
  )
  print()

  print("Not encoded:")
  print(
    "  automatic zero inference =",
    hasattr(
      zero_premise,
      "derive_zero",
    ),
  )

  print(
    "  automatic nonzero inference =",
    hasattr(
      nonzero_premise,
      "derive_nonzero",
    ),
  )

  print(
    "  contradiction detection =",
    (
      hasattr(
        zero_premise,
        "contradicts",
      )
      or hasattr(
        nonzero_premise,
        "contradicts",
      )
    ),
  )

  print(
    "  bilinearity =",
    hasattr(
      product,
      "bilinearity",
    ),
  )

  print(
    "  antisymmetry =",
    hasattr(
      product,
      "antisymmetry",
    ),
  )

  print(
    "  Toda Lemma 4.1 evaluation =",
    (
      hasattr(
        zero_premise,
        "toda_lemma_4_1",
      )
      or hasattr(
        nonzero_premise,
        "toda_lemma_4_1",
      )
    ),
  )


def main():
  print()
  print("EHP Proof Tracer")
  print(
    "Phase 43 capability demonstration"
  )
  print()

  result = (
    build_phase43_representative_premises()
  )

  print_phase43_representation(
    result
  )

  print_phase43_distinction(
    result
  )

  print_phase43_proof_premises(
    result
  )

  print_phase43_boundary(
    result
  )

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



