Phase 162 R3-C: generic finite-cyclic transport reasoning.

Unzip into the repository root, then run:
  powershell -ExecutionPolicy Bypass -File .\phase162_r3c_root_reason\run_phase162_r3c.ps1

Only the public entry function and import of toda_group_proof_narrative_renderer.py
are changed. A generic inference reason module and 4 focused tests are added.
Existing Phase 161/R2 proof derivation and historical Markdown are not modified.
The existing overall narrative is still used; this Phase changes only the root
inference explanation, NOT the wider prose and Reference defects.

The patcher refuses an unexpected base function; it does not blindly edit files.
