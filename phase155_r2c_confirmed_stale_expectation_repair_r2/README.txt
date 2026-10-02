Phase 155-R2C-r2 — remaining stale expectation repair

This repair is applied on top of the already executed Phase 155-R2C-r1 state.

Only two test functions are changed:

1. tests/test_phase132_6_group_proof_narrative_renderer.py
   test_phase132_6_sigma9_narrative_uses_fixed_japanese_leads

   The r1 repair incorrectly asserted that the entire rendered text contained
   no Japanese full stop. The current depth-1 output still contains a proof-
   purpose sentence ending in `。`. The corrected contract checks only the
   discourse leads (`まず,`, `このことから,`, `したがって,`) and rejects
   their old Japanese-comma forms.

2. tests/test_phase153_r12_root_reference_exclusion.py
   test_phase153_r12_pi11_4_body_uses_renumbered_external_references

   Current Phase 154 semantics use `[R1]を用いる.` for R1 and
   `[R2]より, ...` for the Proposition 4.4 semantic sentence. R2 is not a
   compact `を用いる.` marker at this location.

No production code is modified.
No test is deleted.
The repository-wide suite is not run.
The R2B focused verification set is re-run after the repair.
