from dataclasses import dataclass
from enum import Enum

from toda_group_proof_narrative_aggregate_semantics import (
  TodaGroupProofNarrativeAggregateSemanticKind,
  TodaGroupProofNarrativeAggregateSemanticSidecar,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


class TodaGroupProofNarrativeProofChainProviderKind(
  Enum
):
  SUPPORTING_BLOCK = "supporting_block"
  CHILD_ARGUMENT = "child_argument"


@dataclass(frozen=True)
class TodaGroupProofNarrativeProofChainProvider:
  kind: TodaGroupProofNarrativeProofChainProviderKind
  supporting_block: TodaGroupProofNarrativeBlock | None = None
  child_argument_index: int | None = None
  aggregate_semantic_kinds: tuple[
    TodaGroupProofNarrativeAggregateSemanticKind,
    ...,
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.kind,
      TodaGroupProofNarrativeProofChainProviderKind,
    ):
      raise TypeError(
        "kind must be a "
        "TodaGroupProofNarrativeProofChainProviderKind"
      )

    if not isinstance(
      self.aggregate_semantic_kinds,
      tuple,
    ):
      raise TypeError(
        "aggregate_semantic_kinds must be a tuple"
      )

    for semantic_kind in self.aggregate_semantic_kinds:
      if not isinstance(
        semantic_kind,
        TodaGroupProofNarrativeAggregateSemanticKind,
      ):
        raise TypeError(
          "aggregate_semantic_kinds must contain only "
          "TodaGroupProofNarrativeAggregateSemanticKind objects"
        )

    if len(
      set(
        self.aggregate_semantic_kinds
      )
    ) != len(
      self.aggregate_semantic_kinds
    ):
      raise ValueError(
        "aggregate_semantic_kinds must not contain duplicates"
      )

    if (
      self.kind
      is TodaGroupProofNarrativeProofChainProviderKind
      .SUPPORTING_BLOCK
    ):
      if not isinstance(
        self.supporting_block,
        TodaGroupProofNarrativeBlock,
      ):
        raise TypeError(
          "supporting_block provider must have a "
          "TodaGroupProofNarrativeBlock"
        )
      if self.child_argument_index is not None:
        raise ValueError(
          "supporting_block provider must not have "
          "child_argument_index"
        )
      return

    if self.supporting_block is not None:
      raise ValueError(
        "child_argument provider must not have "
        "supporting_block"
      )

    if (
      not isinstance(
        self.child_argument_index,
        int,
      )
      or isinstance(
        self.child_argument_index,
        bool,
      )
      or self.child_argument_index < 0
    ):
      raise TypeError(
        "child_argument provider must have a "
        "non-negative integer child_argument_index"
      )

    if self.aggregate_semantic_kinds:
      raise ValueError(
        "child_argument provider must not have "
        "aggregate_semantic_kinds"
      )


@dataclass(frozen=True)
class TodaGroupProofNarrativeProofChain:
  argument_index: int
  argument: TodaGroupProofNarrativeArgument
  providers: tuple[
    TodaGroupProofNarrativeProofChainProvider,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if (
      not isinstance(
        self.argument_index,
        int,
      )
      or isinstance(
        self.argument_index,
        bool,
      )
      or self.argument_index < 0
    ):
      raise TypeError(
        "argument_index must be a non-negative integer"
      )

    if not isinstance(
      self.argument,
      TodaGroupProofNarrativeArgument,
    ):
      raise TypeError(
        "argument must be a "
        "TodaGroupProofNarrativeArgument"
      )

    if not isinstance(
      self.providers,
      tuple,
    ):
      raise TypeError(
        "providers must be a tuple"
      )

    for provider in self.providers:
      if not isinstance(
        provider,
        TodaGroupProofNarrativeProofChainProvider,
      ):
        raise TypeError(
          "providers must contain only "
          "TodaGroupProofNarrativeProofChainProvider objects"
        )


def _validate_proof_chain_inputs(
  presentation: TodaGroupProofPresentation,
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  aggregate_semantic_sidecar: (
    TodaGroupProofNarrativeAggregateSemanticSidecar
    | None
  ),
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> None:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    semantic_sidecar,
    TodaGroupProofNarrativeSemanticSidecar,
  ):
    raise TypeError(
      "semantic_sidecar must be a "
      "TodaGroupProofNarrativeSemanticSidecar"
    )

  if semantic_sidecar.presentation is not presentation:
    raise ValueError(
      "semantic_sidecar must belong to presentation"
    )

  if (
    aggregate_semantic_sidecar is not None
    and not isinstance(
      aggregate_semantic_sidecar,
      TodaGroupProofNarrativeAggregateSemanticSidecar,
    )
  ):
    raise TypeError(
      "aggregate_semantic_sidecar must be a "
      "TodaGroupProofNarrativeAggregateSemanticSidecar "
      "or None"
    )

  if (
    aggregate_semantic_sidecar is not None
    and aggregate_semantic_sidecar.presentation
    is not presentation
  ):
    raise ValueError(
      "aggregate_semantic_sidecar must belong "
      "to presentation"
    )

  if not isinstance(
    arguments,
    tuple,
  ):
    raise TypeError(
      "arguments must be a tuple"
    )

  for argument in arguments:
    if not isinstance(
      argument,
      TodaGroupProofNarrativeArgument,
    ):
      raise TypeError(
        "arguments must contain only "
        "TodaGroupProofNarrativeArgument objects"
      )

  for argument in arguments:
    for child_argument_index in argument.child_argument_indices:
      if child_argument_index >= len(arguments):
        raise ValueError(
          "child_argument_index must refer to arguments"
        )


def _aggregate_semantic_kinds_for_block(
  block: TodaGroupProofNarrativeBlock,
  aggregate_semantic_sidecar: (
    TodaGroupProofNarrativeAggregateSemanticSidecar
    | None
  ),
) -> tuple[
  TodaGroupProofNarrativeAggregateSemanticKind,
  ...,
]:
  if aggregate_semantic_sidecar is None:
    return ()

  block_step_ids = {
    id(
      proof_step
    )
    for proof_step in block.steps
  }
  kinds = []

  for semantic in aggregate_semantic_sidecar.step_semantics:
    if id(semantic.proof_step) not in block_step_ids:
      continue
    if semantic.kind in kinds:
      continue
    kinds.append(
      semantic.kind
    )

  return tuple(
    kinds
  )


def build_toda_group_proof_narrative_proof_chains(
  presentation: TodaGroupProofPresentation,
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  aggregate_semantic_sidecar: (
    TodaGroupProofNarrativeAggregateSemanticSidecar
    | None
  ) = None,
) -> tuple[
  TodaGroupProofNarrativeProofChain,
  ...,
]:
  _validate_proof_chain_inputs(
    presentation,
    semantic_sidecar,
    aggregate_semantic_sidecar,
    arguments,
  )

  chains = []

  for argument_index, argument in enumerate(
    arguments
  ):
    providers = []

    for supporting_block in argument.supporting_blocks:
      providers.append(
        TodaGroupProofNarrativeProofChainProvider(
          kind=(
            TodaGroupProofNarrativeProofChainProviderKind
            .SUPPORTING_BLOCK
          ),
          supporting_block=supporting_block,
          aggregate_semantic_kinds=(
            _aggregate_semantic_kinds_for_block(
              supporting_block,
              aggregate_semantic_sidecar,
            )
          ),
        )
      )

    for child_argument_index in argument.child_argument_indices:
      providers.append(
        TodaGroupProofNarrativeProofChainProvider(
          kind=(
            TodaGroupProofNarrativeProofChainProviderKind
            .CHILD_ARGUMENT
          ),
          child_argument_index=child_argument_index,
        )
      )

    chains.append(
      TodaGroupProofNarrativeProofChain(
        argument_index=argument_index,
        argument=argument,
        providers=tuple(
          providers
        ),
      )
    )

  return tuple(
    chains
  )
