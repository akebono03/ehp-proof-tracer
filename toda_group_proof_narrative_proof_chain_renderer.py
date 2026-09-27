from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChain,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


def _validate_toda_group_proof_narrative_proof_chain_integration(
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  proof_chains: tuple[
    TodaGroupProofNarrativeProofChain,
    ...,
  ],
) -> None:
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

  if not isinstance(
    proof_chains,
    tuple,
  ):
    raise TypeError(
      "proof_chains must be a tuple"
    )

  for proof_chain in proof_chains:
    if not isinstance(
      proof_chain,
      TodaGroupProofNarrativeProofChain,
    ):
      raise TypeError(
        "proof_chains must contain only "
        "TodaGroupProofNarrativeProofChain objects"
      )

  if len(
    proof_chains
  ) != len(
    arguments
  ):
    raise ValueError(
      "proof_chains must contain exactly one chain "
      "for each argument"
    )

  seen_argument_indices = set()

  for proof_chain in proof_chains:
    argument_index = (
      proof_chain.argument_index
    )

    if argument_index >= len(
      arguments
    ):
      raise ValueError(
        "proof_chain argument_index must refer "
        "to arguments"
      )

    if argument_index in seen_argument_indices:
      raise ValueError(
        "proof_chains must not contain duplicate "
        "argument_index values"
      )

    if (
      proof_chain.argument
      is not arguments[
        argument_index
      ]
    ):
      raise ValueError(
        "proof_chain argument must be the argument "
        "at proof_chain argument_index"
      )

    seen_argument_indices.add(
      argument_index
    )

  if seen_argument_indices != set(
    range(
      len(
        arguments
      )
    )
  ):
    raise ValueError(
      "proof_chains must cover every argument exactly once"
    )


def render_toda_group_proof_narrative_from_proof_chains_markdown(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  proof_chains: tuple[
    TodaGroupProofNarrativeProofChain,
    ...,
  ],
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    blocks,
    tuple,
  ):
    raise TypeError(
      "blocks must be a tuple"
    )

  for block in blocks:
    if not isinstance(
      block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "blocks must contain only "
        "TodaGroupProofNarrativeBlock objects"
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

  _validate_toda_group_proof_narrative_proof_chain_integration(
    arguments,
    proof_chains,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
