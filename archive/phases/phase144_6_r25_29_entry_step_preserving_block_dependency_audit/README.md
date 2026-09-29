# Phase 144-6 R25-29 Entry-Step-Preserving Block Dependency Audit

## Purpose

R25-28 showed that block-level dependency traversal can greatly enlarge Narrative argument local bodies. R25-29 simulates preserving ProofStep identity until dependency traversal is complete and projecting selected steps back to the existing NarrativeBlocks only afterward.

## Production changes

None.

## Simulation

For each representative group the audit keeps proof-edge and semantic dependencies at ProofStep level, starts from the actual dependency steps of each argument conclusion, stops at steps belonging to other argument conclusion blocks, traverses without switching to another step merely because it shares a block, and finally projects the selected steps to the existing NarrativeBlocks.

The NarrativeBlock model, argument API, renderer, and current local-body implementation are unchanged.

## Preservation check

The audit checks that the pi_6^3 group-structure and order arguments retain their primary exactness material.

## Interpretation

Substantial reduction for pi_15^8 and pi_16^9 together with pi_6^3 preservation supports entry-step-preserving traversal as the candidate minimal production repair for the next revision.

Repository-wide pytest remains deferred until the end of Phase 144-6.
