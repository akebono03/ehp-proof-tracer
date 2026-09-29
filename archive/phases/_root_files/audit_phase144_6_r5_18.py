from collections import Counter

from tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChainProviderKind,
)


def main():
  group_count = 0
  argument_count = 0
  provider_count = 0
  supporting_block_count = 0
  child_argument_count = 0
  aggregate_annotated_provider_count = 0
  chain_type_counts = Counter()

  print("=" * 78)
  print("Phase 144-6-R5-18 production Generic ProofChain foundation audit")
  print("=" * 78)

  for n, k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments, aggregate, chains = (
      _context(n, k)
    )
    group_count += 1
    argument_count += len(chains)

    print(f"\\npi_{n + k}^{n}")
    print("-" * 78)
    print(f"arguments={len(arguments)} chains={len(chains)}")

    for chain in chains:
      for provider in chain.providers:
        provider_count += 1

        if (
          provider.kind
          is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
        ):
          supporting_block_count += 1
          provider_role = provider.supporting_block.role.value
          aggregate_kinds = ",".join(
            kind.value
            for kind in provider.aggregate_semantic_kinds
          )
          if provider.aggregate_semantic_kinds:
            aggregate_annotated_provider_count += 1
        else:
          child_argument_count += 1
          provider_role = (
            arguments[provider.child_argument_index].role.value
          )
          aggregate_kinds = ""

        chain_type_counts[
          (
            chain.argument.conclusion_block.role.value,
            provider.kind.value,
            provider_role,
          )
        ] += 1

        print(
          f"A{chain.argument_index + 1:02d} "
          f"{chain.argument.conclusion_block.role.value} <- "
          f"{provider.kind.value}:{provider_role}"
          + (
            f" aggregate=[{aggregate_kinds}]"
            if aggregate_kinds
            else ""
          )
        )

  print("\\nSummary")
  print("-" * 78)
  print(f"groups={group_count}")
  print(f"arguments={argument_count}")
  print(f"providers={provider_count}")
  print(f"supporting_blocks={supporting_block_count}")
  print(f"child_arguments={child_argument_count}")
  print(
    "aggregate_annotated_providers="
    f"{aggregate_annotated_provider_count}"
  )
  print(f"unique_chain_types={len(chain_type_counts)}")

  print("\\nChain type inventory")
  print("-" * 78)
  for chain_type, count in sorted(chain_type_counts.items()):
    claim_role, provider_kind, provider_role = chain_type
    print(
      f"{count:>3} x {claim_role} <- "
      f"{provider_kind}:{provider_role}"
    )

  print("\\nProduction boundary")
  print("-" * 78)
  print(
    "ProofChain is now a production representation of the direct "
    "NarrativeArgument provider skeleton."
  )
  print(
    "No Narrative renderer consumes ProofChain yet; no legacy renderer "
    "has been removed or bypassed."
  )


if __name__ == "__main__":
  main()
