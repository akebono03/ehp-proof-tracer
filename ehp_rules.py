from dataclasses import dataclass
from expression import (
  Composition,
  Zero,
)
from proof import (
  ExactnessStatement,
  ImageStatement,
  InferenceRule,
  KernelStatement,
  PatternVariable,
  PremisePattern,
  ProofRule,
  Relation,
  RelationType,
  ehp_exactness_proof_step,
  lookup_variable_binding,
)


@dataclass(frozen=True)
class EHPZeroCompositionStatement:
  first_map: object
  second_map: object


def ehp_exactness_inference_rule(
  exact_step=None,
):
  first_map = PatternVariable(
    name="first_map",
  )
  second_map = PatternVariable(
    name="second_map",
  )
  image_structure = PatternVariable(
    name="image_structure",
  )
  kernel_structure = PatternVariable(
    name="kernel_structure",
  )

  if exact_step is None:
    def guard(
      premises,
      bindings,
    ):
      bound_first_map = (
        lookup_variable_binding(
          first_map,
          bindings,
        )
      )

      bound_second_map = (
        lookup_variable_binding(
          second_map,
          bindings,
        )
      )

      return ehp_maps_are_consecutive(
        bound_first_map,
        bound_second_map,
      )

    image_pattern = ImageStatement(
      group_map=first_map,
      structure=image_structure,
    )
    kernel_pattern = KernelStatement(
      group_map=second_map,
      structure=kernel_structure,
    )

    return InferenceRule(
      name="EHP exactness from image and kernel",
      description=(
        "Image(E) and Kernel(H) determine "
        "exactness at the sphere term."
      ),
      premise_patterns=(
        PremisePattern(
          proof_rule=ProofRule.IMAGE_COMPUTATION,
          statement_type=ImageStatement,
          statement_pattern=image_pattern,
        ),
        PremisePattern(
          proof_rule=ProofRule.KERNEL_COMPUTATION,
          statement_type=KernelStatement,
          statement_pattern=kernel_pattern,
        ),
      ),
      conclusion_pattern=ExactnessStatement(
        first_map=first_map,
        second_map=second_map,
        is_exact=True,
      ),
      match_guard=guard,
    )

  image_pattern = ImageStatement(
    group_map=exact_step.first_map,
    structure=exact_step.first_map.image_structure(),
  )
  kernel_pattern = KernelStatement(
    group_map=exact_step.second_map,
    structure=exact_step.second_map.kernel_structure(),
  )

  def build_conclusion(premises):
    exactness_step = (
      ehp_exactness_proof_step(
        exact_step,
        premises[0],
        premises[1],
      )
    )

    return exactness_step.conclusion

  return InferenceRule(
    name="EHP exactness from image and kernel",
    description=(
      "Image(E) and Kernel(H) determine "
      "exactness at the sphere term."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.IMAGE_COMPUTATION,
        statement_type=ImageStatement,
        statement_pattern=image_pattern,
      ),
      PremisePattern(
        proof_rule=ProofRule.KERNEL_COMPUTATION,
        statement_type=KernelStatement,
        statement_pattern=kernel_pattern,
      ),
    ),
    conclusion_builder=build_conclusion,
  )


def ehp_exactness_image_implies_kernel_inference_rule():
  first_map = PatternVariable(
    name="first_map",
  )
  second_map = PatternVariable(
    name="second_map",
  )
  structure = PatternVariable(
    name="structure",
  )

  return InferenceRule(
    name=(
      "EHP exactness transfers "
      "image structure to kernel"
    ),
    description=(
      "If a consecutive map pair is exact, "
      "the image of the first map equals "
      "the kernel of the second map."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=ExactnessStatement,
        statement_pattern=(
          ExactnessStatement(
            first_map=first_map,
            second_map=second_map,
            is_exact=True,
          )
        ),
      ),
      PremisePattern(
        statement_type=ImageStatement,
        statement_pattern=(
          ImageStatement(
            group_map=first_map,
            structure=structure,
          )
        ),
      ),
    ),
    conclusion_pattern=KernelStatement(
      group_map=second_map,
      structure=structure,
    ),
  )


def ehp_exactness_kernel_implies_image_inference_rule():
  first_map = PatternVariable(
    name="first_map",
  )
  second_map = PatternVariable(
    name="second_map",
  )
  structure = PatternVariable(
    name="structure",
  )

  return InferenceRule(
    name=(
      "EHP exactness transfers "
      "kernel structure to image"
    ),
    description=(
      "If a consecutive map pair is exact, "
      "the kernel of the second map equals "
      "the image of the first map."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=ExactnessStatement,
        statement_pattern=(
          ExactnessStatement(
            first_map=first_map,
            second_map=second_map,
            is_exact=True,
          )
        ),
      ),
      PremisePattern(
        statement_type=KernelStatement,
        statement_pattern=(
          KernelStatement(
            group_map=second_map,
            structure=structure,
          )
        ),
      ),
    ),
    conclusion_pattern=ImageStatement(
      group_map=first_map,
      structure=structure,
    ),
  )


def ehp_exactness_implies_zero_composition_inference_rule():
  first_map = PatternVariable(
    name="first_map",
  )
  second_map = PatternVariable(
    name="second_map",
  )

  return InferenceRule(
    name=(
      "EHP exactness implies "
      "zero composition"
    ),
    description=(
      "If a consecutive map pair is exact, "
      "the second map composed with "
      "the first map is zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=ExactnessStatement,
        statement_pattern=(
          ExactnessStatement(
            first_map=first_map,
            second_map=second_map,
            is_exact=True,
          )
        ),
      ),
    ),
    conclusion_pattern=(
      EHPZeroCompositionStatement(
        first_map=first_map,
        second_map=second_map,
      )
    ),
  )


def ehp_zero_composition_implies_zero_relation_inference_rule():
  first_map = PatternVariable(
    name="first_map",
  )
  second_map = PatternVariable(
    name="second_map",
  )

  return InferenceRule(
    name=(
      "EHP zero composition implies "
      "zero relation"
    ),
    description=(
      "An EHP zero-composition statement "
      "is represented as a generic "
      "zero relation for the composition "
      "of the two maps."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          EHPZeroCompositionStatement
        ),
        statement_pattern=(
          EHPZeroCompositionStatement(
            first_map=first_map,
            second_map=second_map,
          )
        ),
      ),
    ),
    conclusion_pattern=Relation(
      lhs=Composition(
        left=second_map,
        right=first_map,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
  )


def ehp_maps_are_consecutive(
  first_map,
  second_map,
):
  if first_map is None or second_map is None:
    return False

  if not hasattr(
    first_map,
    "target",
  ):
    return False

  if not hasattr(
    second_map,
    "source",
  ):
    return False

  return (
    first_map.target
    == second_map.source
  )







