Phase 144-6 R25-20
Six-group generic production Narrative visibility

Purpose
-------
Make the actual generic production Narrative visible for the six representative
groups before further Narrative repairs.

Representative groups
---------------------
pi_6^3   : n=3, k=3
pi_8^5   : n=5, k=3
pi_10^4  : n=4, k=6
pi_12^5  : n=5, k=7
pi_15^8  : n=8, k=7
pi_16^9  : n=9, k=7

Production changes
------------------
None.

R25-19 already routes an explicit depth Narrative request through
build_complete_toda_group_result_proof_replay() for presentation, while Trace
keeps the existing explicit replay-depth semantics. R25-20 does not add a
six-group special case. It verifies that all six groups use that same public
production route and prints/saves the resulting Narrative text.

Files added by the runner
-------------------------
tests/test_phase144_6_r25_20_six_group_generic_production_narrative.py
phase144_6_r25_20_six_group_generic_production_narrative/show_phase144_6_r25_20_six_group_narratives.py

Generated outputs
-----------------
phase144_6_r25_20_six_group_generic_production_narrative/outputs/
  pi_6^3_generic_narrative.txt
  pi_8^5_generic_narrative.txt
  pi_10^4_generic_narrative.txt
  pi_12^5_generic_narrative.txt
  pi_15^8_generic_narrative.txt
  pi_16^9_generic_narrative.txt
  six_group_generic_narratives.txt

Focused checks only
-------------------
1. All six depth=2 Narrative CLI requests call complete replay.
2. Trace depth=2 preserves the old explicit-depth route.
3. Phase 131 replay regressions remain green.
4. R25-9B depth=2 semantic-closure contract remains green.
5. All six actual production Narratives are printed and saved for inspection.

The repository-wide pytest suite is intentionally not run in R25-20.
