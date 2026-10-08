# Phase 162 R3-2 — repair3

This repair changes the lower validated group proof only. It keeps the upper Group proof unchanged and preserves the Phase 162 R1-R3 interfaces.

The R3-2 Web entry previously reconstructed the target cyclic generator from eta-family definition elements. The Phase 59 bridge rule derives the actual suspension-image relation, and the independently reconstructed target was not structurally identical to that derived relation. The goal is now taken directly from the executed bridge inference, with checks of its source expression and target eta-family composition. R2 independently reexecutes and validates the bridge before proving the goal.

The repair also fixes the bundled Web path test to locate the repository root from the bundle's nested tests directory. No legacy-reference reclassification is included (R3-3).

Run `run_phase162_r3_2_repair3.ps1` after extracting the folder into the repository root. It backs up the locally installed Web integration before applying the narrow patch. Only focused tests are run; the full suite is not run.
