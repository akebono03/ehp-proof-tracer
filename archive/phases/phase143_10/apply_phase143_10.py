from pathlib import Path

path = Path("toda_group_proof_narrative_arguments.py")
text = path.read_text(encoding="utf-8")

old_class = """@dataclass(frozen=True)
class TodaGroupProofNarrativeArgument:
  role: TodaGroupProofNarrativeArgumentRole
  supporting_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ]
  conclusion_block: TodaGroupProofNarrativeBlock

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.role,
      TodaGroupProofNarrativeArgumentRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaGroupProofNarrativeArgumentRole"
      )

    if not isinstance(
      self.supporting_blocks,
      tuple,
    ):
      raise TypeError(
        "supporting_blocks must be a tuple"
      )

    for block in self.supporting_blocks:
      if not isinstance(
        block,
        TodaGroupProofNarrativeBlock,
      ):
        raise TypeError(
          "supporting_blocks must contain only "
          "TodaGroupProofNarrativeBlock objects"
        )

    if not isinstance(
      self.conclusion_block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "conclusion_block must be a "
        "TodaGroupProofNarrativeBlock"
      )

    if any(
      block is self.conclusion_block
      for block in self.supporting_blocks
    ):
      raise ValueError(
        "supporting_blocks must not contain "
        "conclusion_block"
      )

    if len(
      {
        id(
          block
        )
        for block in self.supporting_blocks
      }
    ) != len(
      self.supporting_blocks
    ):
      raise ValueError(
        "supporting_blocks must not contain "
        "duplicate blocks"
      )
"""

new_class = """@dataclass(frozen=True)
class TodaGroupProofNarrativeArgument:
  role: TodaGroupProofNarrativeArgumentRole
  supporting_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ]
  child_argument_indices: tuple[
    int,
    ...,
  ]
  conclusion_block: TodaGroupProofNarrativeBlock

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.role,
      TodaGroupProofNarrativeArgumentRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaGroupProofNarrativeArgumentRole"
      )

    if not isinstance(
      self.supporting_blocks,
      tuple,
    ):
      raise TypeError(
        "supporting_blocks must be a tuple"
      )

    for block in self.supporting_blocks:
      if not isinstance(
        block,
        TodaGroupProofNarrativeBlock,
      ):
        raise TypeError(
          "supporting_blocks must contain only "
          "TodaGroupProofNarrativeBlock objects"
        )

    if not isinstance(
      self.child_argument_indices,
      tuple,
    ):
      raise TypeError(
        "child_argument_indices must be a tuple"
      )

    for argument_index in self.child_argument_indices:
      if (
        not isinstance(
          argument_index,
          int,
        )
        or isinstance(
          argument_index,
          bool,
        )
        or argument_index < 0
      ):
        raise TypeError(
          "child_argument_indices must contain "
          "non-negative integers"
        )

    if len(
      set(
        self.child_argument_indices
      )
    ) != len(
      self.child_argument_indices
    ):
      raise ValueError(
        "child_argument_indices must not "
        "contain duplicates"
      )

    if not isinstance(
      self.conclusion_block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "conclusion_block must be a "
        "TodaGroupProofNarrativeBlock"
      )

    if any(
      block is self.conclusion_block
      for block in self.supporting_blocks
    ):
      raise ValueError(
        "supporting_blocks must not contain "
        "conclusion_block"
      )

    if len(
      {
        id(
          block
        )
        for block in self.supporting_blocks
      }
    ) != len(
      self.supporting_blocks
    ):
      raise ValueError(
        "supporting_blocks must not contain "
        "duplicate blocks"
      )
"""

old_builder_start = """  arguments = []

  for conclusion_index, conclusion_block in enumerate(
    blocks
  ):
    argument_role = (
      _ARGUMENT_ROLE_BY_CONCLUSION_BLOCK_ROLE.get(
        conclusion_block.role
      )
    )

    if argument_role is None:
      continue

    supporting_indices = (
      _argument_dependency_closure_indices(
        direct_dependencies,
        conclusion_index,
      )
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
        conclusion_block=conclusion_block,
      )
    )

  return tuple(
    arguments
  )
"""

new_builder_start = """  argument_specs = tuple(
    (
      conclusion_index,
      argument_role,
    )
    for conclusion_index, conclusion_block in enumerate(
      blocks
    )
    for argument_role in (
      _ARGUMENT_ROLE_BY_CONCLUSION_BLOCK_ROLE.get(
        conclusion_block.role
      ),
    )
    if argument_role is not None
  )

  argument_index_by_conclusion_block_index = {
    conclusion_index: argument_index
    for argument_index, (
      conclusion_index,
      _,
    ) in enumerate(
      argument_specs
    )
  }

  arguments = []

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

  return tuple(
    arguments
  )
"""

if old_class not in text:
    raise RuntimeError("Phase143-7 NarrativeArgument class not found.")
if old_builder_start not in text:
    raise RuntimeError("Phase143-7 builder body not found.")

text=text.replace(old_class,new_class,1)
text=text.replace(old_builder_start,new_builder_start,1)
path.write_text(text,encoding="utf-8")
print("Updated:", path)
