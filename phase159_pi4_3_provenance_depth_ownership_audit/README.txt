Phase 159 — pi_4^3 provenance depth / ownership audit
======================================================

Purpose
-------
Follow-up to the focused failure decomposition audit.

This package separates two possible defects:

1. proof ancestry / replay-depth truncation
2. Narrative Argument ownership

It also checks whether the existing direct bridge

  Delta(iota_5) = +/- 2 eta_2

is actually connected to the current pi_4^3 group-result ancestry.

No production code or existing tests are modified.

Outputs
-------
audit_output/summary.txt
audit_output/all_provenance_nodes.csv
audit_output/focus_nodes.csv
audit_output/provenance_edges.csv
audit_output/depth_matrix.csv

Focused pytest
--------------
tests/test_phase50_pi4_3_exactness_bridge.py
tests/test_phase50_pi4_3_finite_cyclic.py
tests/test_phase52_delta_direct_bridge.py

Repository-wide pytest is not run.
