from proof import (
  ImageStatement,
  InferenceRule,
  KernelStatement,
  PremisePattern,
  ProofRule,
  ehp_exactness_proof_step,
)


def ehp_exactness_inference_rule(
  exact_step,
):
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
      ),
      PremisePattern(
        proof_rule=ProofRule.KERNEL_COMPUTATION,
        statement_type=KernelStatement,
      ),
    ),
    conclusion_builder=build_conclusion,
  )
