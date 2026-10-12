Phase 164 R8-R7 — targeted factory routing closure

Run from the EHP Proof Tracer project root (after extracting ZIP into .):
  powershell -ExecutionPolicy Bypass -File .\phase164_r8_r7_closure\run.ps1

Prerequisites: R8-R5 and R8-R6 applied; Python and pytest available.
Source changes: phase164_r8_proofstep_factory.py, toda_group_proof_narrative_contribution_renderer.py.
New helper is appended to factory. Renderer function routes ProofStep dataclass replace to factory; other dataclasses unchanged.

Preflight fails if the archived 65 replace calls, core 10 calls, or existing production construction routing drifts.
Logs: phase164_r8_r7_output/audit.json, replace_sites.json, CHANGED_CODE.md.
Targeted pytest only. Full suite intentionally not run until end of Phase 164.
IMPORTANT: factory routing closure is not mathematical certification of legacy GIVEN or INFERENCE steps.
