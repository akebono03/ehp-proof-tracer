Phase 144-6-R5-43-10-R2 phase-boundary test update

Production code changes: none.

Why this repair is needed:
R5-43-7 intentionally asserted that the contribution renderer did not yet import
hidden-bridge semantics. R5-43-10 intentionally connects those production
semantics to the contribution renderer, so that historical phase-boundary
assertion is obsolete.

Changed test:
tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py

The first four R5-43-7 semantic tests are unchanged.
Only the final boundary test is updated to the R5-43-10 boundary:
- production hidden-bridge semantics are connected to the contribution renderer;
- the renderer does not inspect inference_rule;
- no pi_6^3-specific n/k branch exists.

No public CLI/Web route is switched by this repair.
No full test suite is run.
