Phase 159 — pi_4^3 focused failure decomposition audit
=======================================================

Purpose
-------
This package performs an audit only. It does not modify production code or
existing tests.

Target
------
pi_4^3, n=3, k=1, public depth=2 Narrative.

The audit traces the expected proof chain:

  pi_5^5 = Z{iota_5}
  -> Delta(iota_5) = +/- 2 eta_2
  -> Im Delta = Z{2 eta_2}
  -> exactness
  -> ker E = Z{2 eta_2}
  -> pi_3^2 = Z{eta_2}
  -> exactness with pi_4^5 = 0
  -> E is surjective
  -> pi_4^3 = Z/2{eta_3}

Pipeline checked
----------------
1. depth=2 proof replay
2. raw proof presentation
3. semantic closure presentation
4. Narrative blocks
5. Narrative Arguments
6. public Web depth=2 Narrative

Output
------
audit_output/summary.txt
audit_output/public_body.txt
audit_output/focus_chain.txt
audit_output/focus_chain.csv
audit_output/focus_edges.csv
audit_output/all_steps.csv

Focused regression
------------------
The runner executes only:

  tests/test_phase50_pi4_3_exactness_bridge.py
  tests/test_phase50_pi4_3_finite_cyclic.py
  tests/test_phase50_eta_family_notation.py

Repository-wide pytest is intentionally not run.

Interpretation
--------------
NOT_IN_RAW_DEPTH2
  The required proof step is not exposed by the current depth=2 replay.

LOST_BEFORE_BLOCKS
  The semantic closure contains the step, but Narrative block construction
  does not retain it.

NOT_OWNED_BY_ARGUMENT
  The step is in a block but is not owned by a Narrative Argument.

LOST_BEFORE_PUBLIC_BODY
  The structural Narrative pipeline retains the step, but the public renderer
  does not show it.

PUBLIC_VISIBLE
  The step is present in the public proof body.

Boundary
--------
This package does not implement a repair. The audit result should determine
the minimum general-rule repair, if one is needed.
