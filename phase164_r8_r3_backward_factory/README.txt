Phase 164 R8-R3 — backward proof inference factory connection

Changes:
- phase161_r5_backward_proof_reconstruction.py: its full import section and the entire reconstruct_phase161_r5_goal function are modified to delegate its two inference sites to derive_inference_proof_step.
- tests/test_phase164_r8_r3_backward_factory.py: adds 3 targeted tests.
- CHANGED_CODE.md is produced by the installer with the complete post-change import section and function.
- proof.py, hopf_rules.py, map_facts.py, replay, web renderer and existing factory untouched.

The wrapper delegates to apply_inference_match and checks premise identities/rule; it does not create GIVEN facts. The unchanged reconstruction still supplies four existing GIVEN exactness witnesses and requires seven derived inferences.
No full pytest until the end of Phase 164.

On Windows PowerShell:
Expand-Archive -Path "$HOME\Downloads\phase164_r8_r3_backward_factory.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase164_r8_r3_backward_factory\run.ps1"
