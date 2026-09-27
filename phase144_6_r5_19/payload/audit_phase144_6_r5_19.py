from tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_proof_chain_renderer import (
  render_toda_group_proof_narrative_from_proof_chains_markdown,
)


def main():
  print("=" * 78)
  print("Phase 144-6-R5-19 Generic ProofChain -> Narrative integration audit")
  print("=" * 78)

  exact_matches = 0

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)

    current_generic = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )
    proof_chain_generic = (
      render_toda_group_proof_narrative_from_proof_chains_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        proof_chains,
      )
    )

    exact = proof_chain_generic == current_generic
    exact_matches += int(exact)

    print(
      f"pi_{n + k}^{n}: "
      f"arguments={len(arguments)} "
      f"proof_chains={len(proof_chains)} "
      f"chars={len(proof_chain_generic)} "
      f"exact_current_generic={exact}"
    )

  print("\\nSummary")
  print("-" * 78)
  print(f"groups={len(TARGETS)}")
  print(f"exact_current_generic_matches={exact_matches}")
  print(
    "proof_chain_entrypoint_preserves_current_generic_output="
    f"{exact_matches == len(TARGETS)}"
  )

  print("\\nIntegration boundary")
  print("-" * 78)
  print(
    "ProofChain is now a required, validated input to a production Narrative "
    "entrypoint."
  )
  print(
    "The entrypoint intentionally delegates rendering to the current generic "
    "multi-Argument renderer after validating one-to-one Argument/ProofChain "
    "coverage."
  )
  print(
    "Phase 19 does not yet use ProofChain providers to change local-body "
    "selection, does not switch the public Narrative route, and does not "
    "remove the dedicated pi_6^3 renderer."
  )
  print(
    "Those parity and route-replacement decisions remain Phase 20 work."
  )


if __name__ == "__main__":
  main()
