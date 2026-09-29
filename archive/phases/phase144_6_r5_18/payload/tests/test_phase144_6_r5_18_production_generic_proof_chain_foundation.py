import pytest

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_aggregate_semantics import (
  build_toda_group_proof_narrative_aggregate_semantic_sidecar,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChainProviderKind,
  build_toda_group_proof_narrative_proof_chains,
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
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _context(n, k):
  report = build_standard_toda_report(n=n, k=k)
  group_result = report.candidates[0].source_candidate.group_result
  provenance = extract_toda_recursive_proof_provenance(group_result)
  max_depth = max(node.shortest_depth for node in provenance.nodes)
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=max_depth,
  )
  presentation = build_toda_group_proof_presentation(replay)
  semantic_sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  aggregate_semantic_sidecar = (
    build_toda_group_proof_narrative_aggregate_semantic_sidecar(
      presentation
    )
  )
  chains = build_toda_group_proof_narrative_proof_chains(
    presentation,
    semantic_sidecar,
    arguments,
    aggregate_semantic_sidecar=aggregate_semantic_sidecar,
  )
  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    chains,
  )


def test_phase144_6_r5_18_builds_one_proof_chain_per_argument():
  for n, k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments, aggregate, chains = (
      _context(n, k)
    )

    assert len(chains) == len(arguments)
    assert all(
      chain.argument is arguments[chain.argument_index]
      for chain in chains
    )


def test_phase144_6_r5_18_preserves_direct_argument_provider_counts():
  for n, k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments, aggregate, chains = (
      _context(n, k)
    )

    for argument, chain in zip(arguments, chains):
      assert len(chain.providers) == (
        len(argument.supporting_blocks)
        + len(argument.child_argument_indices)
      )


def test_phase144_6_r5_18_preserves_supporting_block_identity_and_order():
  for n, k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments, aggregate, chains = (
      _context(n, k)
    )

    for argument, chain in zip(arguments, chains):
      supporting_providers = tuple(
        provider
        for provider in chain.providers
        if (
          provider.kind
          is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
        )
      )

      assert tuple(
        provider.supporting_block
        for provider in supporting_providers
      ) == argument.supporting_blocks


def test_phase144_6_r5_18_preserves_child_argument_indices_and_order():
  total_child_arguments = 0

  for n, k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments, aggregate, chains = (
      _context(n, k)
    )

    for argument, chain in zip(arguments, chains):
      child_providers = tuple(
        provider
        for provider in chain.providers
        if (
          provider.kind
          is TodaGroupProofNarrativeProofChainProviderKind.CHILD_ARGUMENT
        )
      )

      child_indices = tuple(
        provider.child_argument_index
        for provider in child_providers
      )
      assert child_indices == argument.child_argument_indices
      total_child_arguments += len(child_indices)

  assert total_child_arguments == 20


def test_phase144_6_r5_18_preserves_aggregate_semantics_as_annotation():
  aggregate_provider_count = 0

  for n, k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments, aggregate, chains = (
      _context(n, k)
    )

    for chain in chains:
      for provider in chain.providers:
        if provider.aggregate_semantic_kinds:
          aggregate_provider_count += 1
          assert (
            provider.kind
            is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
          )

  assert aggregate_provider_count > 0


def test_phase144_6_r5_18_supports_semantic_only_argument_dependency():
  presentation, semantic_sidecar, blocks, arguments, aggregate, chains = (
    _context(3, 3)
  )

  definition_chains = tuple(
    chain
    for chain in chains
    if chain.argument.role.value == "establish_definition"
  )

  assert len(definition_chains) == 1
  definition_chain = definition_chains[0]
  supporting_roles = tuple(
    provider.supporting_block.role.value
    for provider in definition_chain.providers
    if provider.supporting_block is not None
  )

  assert "precondition" in supporting_roles


def test_phase144_6_r5_18_rejects_foreign_semantic_sidecar():
  presentation, semantic_sidecar, blocks, arguments, aggregate, chains = (
    _context(3, 3)
  )
  foreign_semantic_sidecar = _context(5, 3)[1]

  with pytest.raises(
    ValueError,
    match="semantic_sidecar must belong to presentation",
  ):
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      foreign_semantic_sidecar,
      arguments,
      aggregate_semantic_sidecar=aggregate,
    )


def test_phase144_6_r5_18_rejects_foreign_aggregate_sidecar():
  presentation, semantic_sidecar, blocks, arguments, aggregate, chains = (
    _context(3, 3)
  )
  foreign_aggregate = _context(5, 3)[4]

  with pytest.raises(
    ValueError,
    match="aggregate_semantic_sidecar must belong to presentation",
  ):
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
      aggregate_semantic_sidecar=foreign_aggregate,
    )
