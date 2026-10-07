# Phase 160-R7 Repair 1

Fix the R7 public Narrative wrapper's previous-renderer capture.

The initial R7 apply script replaced the file starting at the Phase 159 wrapper marker. That also removed the definition of `_phase159_repair3_previous_public_narrative_renderer`, while the new R7 tail still tried to reference it during module import.

This repair changes only the R7 capture line so the renderer immediately preceding the R7 wrapper is stored directly:

`_phase160_r7_previous_public_narrative_renderer = render_toda_group_proof_narrative_markdown`

No Narrative semantics, production semantics, inference rule, or test expectation is changed. No full test suite is run.
