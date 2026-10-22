# Phase 168 R3-3: Proof Narrative Model groundwork

Adds only `phase168_r3_3_proof_narrative_model.py` and its focused tests. This is not yet wired to the production Web renderer. Existing Python modules and docs are untouched.

The model gets citations only from `ProofStep.inference_rule.literature_reference` and explicit `ProofStepLink` values matching the actual `ProofStep`. It does not infer references from rule names or proof text, and it does not choose citations using publication order. Root inference-rule citations are kept. No citation is invented for unlinked steps.

Run `run.ps1` from the extracted folder after extracting in the project root. It installs the new module (refuses to overwrite different existing content) and runs only four focused pytest cases. Full suite is intentionally not run.

This phase does not yet resolve whether current search output retains sufficient registered source links; that connection must be confirmed and integrated before switching public rendering.
