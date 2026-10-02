Phase 155 Closure-R2 — 98 failure classification / stale expectation consolidation

Purpose
-------
Use the already-completed Phase155 Closure full-suite log as evidence.
Do not rerun the repository suite.

Reviewed classification
-----------------------
SAFE_STALE
  Phase132 / Phase133 / Phase143 / Phase150
  Historical Narrative wrapper, Reference-name, wording, punctuation, and
  semantic-rendering expectations that predate the current generic route.

HISTORICAL_HEAVY
  Phase144
  Historical cross-group/contribution/transport audit tests with fixed counts,
  population snapshots, or renderer-internal assumptions. These require
  runtime/redundancy review before any repair or deletion.

CONTRACT_SENSITIVE
  Phase153 and Phase95–98
  Reference ownership, provenance, source metadata, aggregate-result behavior.
  These are deliberately not auto-classified as stale.

Expected counts
---------------
SAFE_STALE: 38
HISTORICAL_HEAVY: 36
CONTRACT_SENSITIVE: 24
UNKNOWN: 0

Execution
---------
Only five tiny classifier tests run.
No repository test body runs.
No production file changes.
No repository test changes.
