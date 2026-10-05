Phase157-R20 repair42

Purpose
-------
Suppress repeated pure restatements of the same fixed Reference statement
after all late contribution/dependency ordering passes.

Changed production file
-----------------------
- toda_group_proof_narrative_contribution_renderer.py

New function
------------
- suppress_toda_group_proof_narrative_repeated_reference_restatements()

Insertion point
---------------
Immediately after:
- order_toda_group_proof_narrative_short_exact_support()

Import changes
--------------
None.

Generic rule
------------
Build normalized display keys from the fixed-reference statement lines.
Keep the first body paragraph whose entire normalized display equals a fixed
Reference statement, and suppress later pure restatements of the same fixed
statement. Reference prefixes and equation tags are ignored for comparison.
Uses inside larger derivation sentences are preserved.

New test
--------
- tests/test_phase157_r20_repair42_repeated_reference_restatements.py

Phase boundary
--------------
This repair does not remove generic connector prose and does not suppress
non-reference semantic conclusions such as a repeated Delta-zero conclusion.

No documentation changes.
No repository-wide pytest.
