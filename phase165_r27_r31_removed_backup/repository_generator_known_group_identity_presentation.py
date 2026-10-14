from dataclasses import dataclass

from expression import GeneratorSymbol
from generator_input import (
  resolve_generator_input,
)
from repository_generator_known_group_identity_lookup import (
  find_standard_repository_generator_known_group_identity_nodes,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
)


@dataclass(frozen=True)
class RepositoryGeneratorKnownGroupIdentityPresentation:
  generator: GeneratorSymbol
  source_node: RepositoryProofScopeNode
  conclusion: object

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.generator,
      GeneratorSymbol,
    ):
      raise TypeError(
        "generator must be a GeneratorSymbol"
      )

    if not isinstance(
      self.source_node,
      RepositoryProofScopeNode,
    ):
      raise TypeError(
        "source_node must be a "
        "RepositoryProofScopeNode"
      )

    if (
      self.conclusion
      is not self.source_node.proof_step.conclusion
    ):
      raise ValueError(
        "conclusion must preserve source_node "
        "proof-step conclusion identity"
      )


def build_repository_generator_known_group_identity_presentation(
  generator: GeneratorSymbol,
  nodes: tuple[
    RepositoryProofScopeNode,
    ...,
  ],
) -> RepositoryGeneratorKnownGroupIdentityPresentation:
  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "generator must be a GeneratorSymbol"
    )

  if not isinstance(
    nodes,
    tuple,
  ):
    raise TypeError(
      "nodes must be a tuple"
    )

  for node in nodes:
    if not isinstance(
      node,
      RepositoryProofScopeNode,
    ):
      raise TypeError(
        "nodes must contain only "
        "RepositoryProofScopeNode objects"
      )

  if len(
    nodes
  ) != 1:
    raise ValueError(
      "nodes must contain exactly one "
      "known-group identity"
    )

  source_node = nodes[
    0
  ]

  return (
    RepositoryGeneratorKnownGroupIdentityPresentation(
      generator=generator,
      source_node=source_node,
      conclusion=source_node.proof_step.conclusion,
    )
  )


def build_standard_repository_generator_known_group_identity_presentation_input(
  generator_input: str,
) -> RepositoryGeneratorKnownGroupIdentityPresentation:
  generator = resolve_generator_input(
    generator_input
  )

  nodes = (
    find_standard_repository_generator_known_group_identity_nodes(
      generator
    )
  )

  return (
    build_repository_generator_known_group_identity_presentation(
      generator,
      nodes,
    )
  )
