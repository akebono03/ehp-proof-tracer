Phase 168 R3-36A — read-only linkage audit

Scope: inspection only; no production files changed. Run from repository root using run.ps1.
The script inspects the current local working tree, not a remote snapshot.
The static checks do NOT prove that the live pi5^4 ProofStep is linked to an assertion.
Next step: use the report and a runtime trace of the actual screened bridge and Proof Tree to identify exact links, then make a separate minimal patch.
Only two tests for this audit utility run. Full pytest is not executed.

GitHub sources reviewed 2026-10-23:
phase168_r3_3_proof_narrative_model.py
phase168_r3_4_link_bridge.py
phase163_r4_r12_stable_bases.py
unified_statement_registry.py
