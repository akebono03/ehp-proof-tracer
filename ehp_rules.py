from proof import (
  ImageStatement,
  InferenceRule,
  KernelStatement,
  PatternVariable,
  PremisePattern,
  ProofRule,
  ehp_exactness_proof_step,
)
from algebra import ExactSequenceStep


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
    image_pattern = ImageStatement(
      group_map=first_map,
      structure=image_structure,
    )
    kernel_pattern = KernelStatement(
      group_map=second_map,
      structure=kernel_structure,
    )
  else:
    image_pattern = ImageStatement(
      group_map=exact_step.first_map,
      structure=exact_step.first_map.image_structure(),
    )
    kernel_pattern = KernelStatement(
      group_map=exact_step.second_map,
      structure=exact_step.second_map.kernel_structure(),
    )

  def build_conclusion(premises):
    conclusion_exact_step = exact_step

    if conclusion_exact_step is None:
      conclusion_exact_step = ExactSequenceStep(
        first_map=premises[0].conclusion.group_map,
        second_map=premises[1].conclusion.group_map,
      )

    exactness_step = (
      ehp_exactness_proof_step(
        conclusion_exact_step,
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
