from proof import (
  ExactnessStatement,
  ImageStatement,
  InferenceRule,
  KernelStatement,
  PatternVariable,
  PremisePattern,
  ProofRule,
  ehp_exactness_proof_step,
  lookup_variable_binding,
)


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







