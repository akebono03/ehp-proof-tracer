# Phase 162 R4-B2: Isolated Proof Replay Integration

This package creates a separate proof replay rooted in the already-derived, eta-normalized `ProofStep` for concrete 1-stem targets above the canonical stable base. It does not modify registered repository roots, their entry identities, the public renderer, or unrelated stems.

## Prerequisites

Install and pass the preceding R4-B1 path selection, R4-B2 concrete transport, and R4-B2 eta normalization (Repair 1 implementation, Repair 2 tests).

## Install and run

Extract the ZIP into the project root and run `run_phase162_r4_b2_replay_integration.ps1` from that root. The script installs the new module and focused tests and runs only the three R4-B2 focused test modules.

## Scope

`build_toda_stable_eta_proof_replay(target_result, base_result, max_depth=3)` creates an ephemeral `ProofRepositoryEntry`, normalizes it to `TodaGroupResult`, builds the standard proof replay, and builds the standard presentation. The original `TodaGroupResult` and original repository entry remain untouched. The derived root is not asserted to be byte-for-byte equal to the original root because the η-family element's display name may differ.

This phase does not switch web display, select references, repair prose, or generalize normalization beyond the eta-family 1-stem. The project-wide suite is reserved for the end of Phase 162.
