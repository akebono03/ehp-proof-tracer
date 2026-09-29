Phase 145-2 Archive Implementation

Purpose
-------
Move the exact 553-artifact population audited in Phase 145-2 Stage 1 into
archive/phases/ using git mv.

Source of truth
---------------
phase145_2_stage1_archiving_audit/output/phase145_2_stage1_archiving_audit.csv

Expected audited population
---------------------------
Artifacts: 553
Tracked files: 1811
Baseline HEAD: 4737d71e339b704b787668f493201e4aebeeb991

Changes
-------
1. Historical artifact directories:
   <artifact>/ -> archive/phases/<artifact>/

2. Historical standalone root files:
   <file> -> archive/phases/_root_files/<file>

3. New archive policy:
   archive/phases/README.md

No historical artifact contents are rewritten.

Execution policy
----------------
Archived artifacts are historical snapshots. Their old runner/apply execution
contract is not maintained after relocation.

Tests
-----
The runner performs:
1. exact move-population verification;
2. canonical Python syntax preflight;
3. repository-wide pytest: python -m pytest tests -q;
4. final Git status/reporting.

The full pytest run is intentionally included because this is the Phase 145-2
final implementation gate.
