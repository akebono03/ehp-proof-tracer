# Phase 165 R52-R17: Reuse proven internal dependencies

Adds an opt-in `completed_internal_proofs` argument to the shared backward search. Each input is a `CompletedInternalProof` wrapping an existing `ProofStep` with an `INFERENCE` root. This module does not independently certify mathematical correctness. Reuse as a subgoal is allowed only if it is distinct from the current root and its proof ancestry does not depend on the current root. References and literary publication positions are unchanged.

Run `run.ps1` from the repository root after extracting the archive. Only targeted pytest is executed.
