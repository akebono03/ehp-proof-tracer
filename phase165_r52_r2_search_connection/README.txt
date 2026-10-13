Phase 165 R52-R2 — canonical search observation to PartialProofResult
Run from the EHP Proof Tracer repository root using run.ps1.
Adds an optional progress_observer to reconstruct_registered_goal without changing default callers.
A separate adapter converts observed ProofSteps and unresolved goals to PartialProofResult.
Does not connect the current Web view or invent a typed ProofStep. No full pytest.
This installer requires phase165_r52_partial_proof.py from R52.
