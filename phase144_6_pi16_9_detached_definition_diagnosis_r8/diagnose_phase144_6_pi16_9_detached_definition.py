from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def build_arguments(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  return build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )


def compact_subject(
  argument,
):
  subject = (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
  )

  if subject is None:
    return "None"

  fields = []

  for name in (
    "name",
    "group_dimension",
    "sphere_dimension",
  ):
    value = getattr(
      subject,
      name,
      None,
    )
    if value is not None:
      fields.append(
        f"{name}={value}"
      )

  if fields:
    return ",".join(
      fields
    )

  return type(
    subject
  ).__name__


def main():
  arguments = build_arguments(
    9,
    7,
  )

  print(
    "pi_16^9 detached-definition diagnosis"
  )
  print("=" * 72)
  print(
    f"argument_count={len(arguments)}"
  )

  for index, argument in enumerate(
    arguments
  ):
    print(
      f"{index}: "
      f"role={argument.role.value} "
      f"conclusion={argument.conclusion_block.role.value} "
      f"children={argument.child_argument_indices} "
      f"subject={compact_subject(argument)} "
      f"supporting_block_count={len(argument.supporting_blocks)}"
    )

  print()
  print(
    "Root child indices="
    f"{arguments[0].child_argument_indices}"
  )
  print(
    "Detached indices="
    f"{tuple(index for index in range(1, len(arguments)) if index not in arguments[0].child_argument_indices)}"
  )


if __name__ == "__main__":
  main()
