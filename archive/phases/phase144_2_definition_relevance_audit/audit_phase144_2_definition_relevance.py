from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  _argument_dependency_closure_indices,
  _argument_direct_dependency_indices,
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


TARGETS = (
  (3, 3, "nu-prime reference"),
  (5, 7, "sigma triple-prime and nu_n"),
  (9, 7, "sigma_9 reference"),
)


def main():
  for n, k, label in TARGETS:
    report = build_standard_toda_report(
      n=n,
      k=k,
    )
    group_result = (
      report.candidates[
        0
      ].source_candidate.group_result
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
    arguments = (
      build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        semantic_sidecar=sidecar,
      )
    )

    direct = _argument_direct_dependency_indices(
      presentation,
      blocks,
      sidecar,
    )
    block_index_by_identity = {
      id(block): index
      for index, block in enumerate(
        blocks
      )
    }

    print("=" * 100)
    print(
      f"n={n}, k={k}, "
      f"target=pi_{n + k}^{n}, "
      f"label={label}"
    )

    for argument_index, argument in enumerate(
      arguments
    ):
      conclusion_index = block_index_by_identity[
        id(
          argument.conclusion_block
        )
      ]
      closure = (
        _argument_dependency_closure_indices(
          direct,
          conclusion_index,
        )
      )
      subject = (
        extract_toda_group_proof_narrative_argument_purpose_subject(
          argument
        )
      )

      print("-" * 100)
      print(f"argument_index={argument_index}")
      print(f"role={argument.role.value}")
      print(
        "subject="
        f"{getattr(subject, 'name', subject)!r}"
      )
      print(
        f"conclusion_block_index={conclusion_index}"
      )
      print(
        f"direct_dependency_indices="
        f"{direct[conclusion_index]}"
      )
      print(
        f"dependency_closure_indices={closure}"
      )

      definition_dependencies = []
      for dependency_index in closure:
        dependency_block = blocks[
          dependency_index
        ]
        if (
          dependency_block.role.value
          != "definition"
        ):
          continue

        matching_argument = next(
          (
            candidate
            for candidate in arguments
            if (
              candidate.conclusion_block
              is dependency_block
            )
          ),
          None,
        )

        if matching_argument is None:
          definition_dependencies.append(
            (
              dependency_index,
              None,
            )
          )
          continue

        definition_subject = (
          extract_toda_group_proof_narrative_argument_purpose_subject(
            matching_argument
          )
        )
        definition_dependencies.append(
          (
            dependency_index,
            getattr(
              definition_subject,
              "name",
              definition_subject,
            ),
          )
        )

      print(
        "definition_dependencies="
        f"{definition_dependencies}"
      )

    print()


if __name__ == "__main__":
  main()
