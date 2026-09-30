from pathlib import Path

TARGET = Path("toda_group_proof_narrative_arguments.py")

RC4_7B_1 = """  arguments = []

  for conclusion_index, argument_role in argument_specs:
    supporting_indices = []
    child_argument_indices = []
    visited_dependency_indices = set()

    def visit_dependency_frontier(
      dependency_index: int,
    ) -> None:
      if dependency_index in visited_dependency_indices:
        return

      visited_dependency_indices.add(
        dependency_index
      )

      child_argument_index = (
        argument_index_by_conclusion_block_index.get(
          dependency_index
        )
      )

      if child_argument_index is not None:
        if (
          child_argument_index
          not in child_argument_indices
        ):
          child_argument_indices.append(
            child_argument_index
          )
        return

      for nested_dependency_index in direct_dependencies[
        dependency_index
      ]:
        visit_dependency_frontier(
          nested_dependency_index
        )

    for dependency_index in direct_dependencies[
      conclusion_index
    ]:
      child_argument_index = (
        argument_index_by_conclusion_block_index.get(
          dependency_index
        )
      )

      if child_argument_index is not None:
        if (
          child_argument_index
          not in child_argument_indices
        ):
          child_argument_indices.append(
            child_argument_index
          )
        continue

      supporting_indices.append(
        dependency_index
      )
      visit_dependency_frontier(
        dependency_index
      )

    arguments.append(
      TodaGroupProofNarrativeArgument(
        role=argument_role,
        supporting_blocks=tuple(
          blocks[
            supporting_index
          ]
          for supporting_index in supporting_indices
        ),
        child_argument_indices=tuple(
          child_argument_indices
        ),
        conclusion_block=blocks[
          conclusion_index
        ],
      )
    )
"""

BASELINE = """  arguments = []

  for conclusion_index, argument_role in argument_specs:
    supporting_indices = []
    child_argument_indices = []

    for dependency_index in direct_dependencies[
      conclusion_index
    ]:
      child_argument_index = (
        argument_index_by_conclusion_block_index.get(
          dependency_index
        )
      )

      if child_argument_index is not None:
        child_argument_indices.append(
          child_argument_index
        )
        continue

      supporting_indices.append(
        dependency_index
      )

    arguments.append(
      TodaGroupProofNarrativeArgument(
        role=argument_role,
        supporting_blocks=tuple(
          blocks[
            supporting_index
          ]
          for supporting_index in supporting_indices
        ),
        child_argument_indices=tuple(
          child_argument_indices
        ),
        conclusion_block=blocks[
          conclusion_index
        ],
      )
    )
"""

def main():
    text = TARGET.read_text(encoding="utf-8")

    if RC4_7B_1 in text:
        TARGET.write_text(
            text.replace(RC4_7B_1, BASELINE, 1),
            encoding="utf-8",
        )
        print("RC4-7B-1 frontier experiment reverted.")
        print("Restored: build_toda_group_proof_narrative_arguments baseline.")
        return

    if BASELINE in text:
        print("RC4-7B-1 frontier experiment is already reverted.")
        return

    raise SystemExit(
        "Neither the RC4-7B-1 block nor the expected baseline block was found. "
        "Current source differs; no file was changed."
    )

if __name__ == "__main__":
    main()
