Phase 164 R8-R6

Run run.ps1 from the project root after Expand-Archive.

Changes:
- phase164_r8_proofstep_factory.py: two constrained adapters for reference annotation and temporary display projection.
- phase162_reference_boundary.py: replaces dataclasses.replace of ProofStep with factory helper.
- toda_group_proof_narrative_contribution_renderer.py: routes temporary ProofStep projection to factory.

Writes backup plus audit.json, replace_sites.json, and CHANGED_CODE.md to phase164_r8_r6_output.
This is NOT a mathematical certification of legacy GIVEN. R8 closure requires further classification of non-ProofStep replace candidates and core-engine direct constructors.
