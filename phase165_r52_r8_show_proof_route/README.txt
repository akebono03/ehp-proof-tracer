Phase 165 R52-R8 / Show proof route alignment

Purpose
- Show proof button uses the Phase 165 registered proof first.
- If and ONLY if no typed proof is registered, show the actual R52
  search failure or partial result in the SAME proof panel.
- Preserve the registered pi_3^2 proof and its common narrative.
- This DOES NOT manufacture a pi_4^3 proof. A genuine pi_4^3
  derivation still requires general typed references and expansions.

Changes
- web_app.py: import GoalSearchIncompleteError, replace only the
  group_proof route in Flask's index() function.
- test_phase165_r52_r8_show_proof_route.py: three focused tests.
- No changes to renderer, proof engine, registry or templates.

Install and run from project root:
Expand-Archive -Path "$HOME\\Downloads\\phase165_r52_r8_show_proof_route.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\\phase165_r52_r8_show_proof_route\\run.ps1"

On install, web_app.py.phase165_r52_r8_backup is retained.
Full updated import section and index() function are written to
web_app_IMPORTS_FULL.txt and web_app_index_FULL.txt.

No full pytest before the phase boundary.
