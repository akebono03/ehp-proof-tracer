Phase 158-R5-5c — Generic public ordering cross-audit

Purpose
=======
Verify that the R5-5b generic ordering repair is not limited to the
representative groups.

Architectural rule
==================
This audit does NOT define the architecture by a fixed number of groups.

The current historical coordinate window n=2..15, k=0..7 is used only as a
temporary audit corpus because it is the repository's established cross-audit
window at this point in development.

New groups must satisfy the same generic invariants automatically.

Audited invariants
==================
1. Visible direct/support premises precede their visible Argument conclusion.
2. A numbered derivation connector references tags that already occurred.
3. A numbered derivation connector is followed by a tagged derivation target.
4. The public root target occurs before QED.
5. No visible content remains between the root target and QED.
6. Web Narrative depth=2 renders without exceptions.

Outputs
=======
audit_output/summary.txt
audit_output/groups.csv
audit_output/argument_order_defects.csv
audit_output/equation_chain_defects.csv
audit_output/target_position_defects.csv
audit_output/exceptions.csv

Production code changes
=======================
None.

Existing repository test changes
================================
None.

Pytest
======
Only two lightweight audit-harness tests are run.

Repository-wide pytest is NOT run.

Interpretation
==============
A finding is diagnostic and is not automatically a production defect.
Any finding must be classified before a repair is proposed.
