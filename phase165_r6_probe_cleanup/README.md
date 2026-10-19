# Phase 165 R6 — Scoped Legacy Probe Test Cleanup

This package performs a narrowly bounded, reversible cleanup of failed legacy **probe-only tests**. It does not restore obsolete APIs, change production code, change proof rendering, or run the full test suite.

Eligibility requires all of: the test is listed in the original 497-error triage report for the removed group-specific rule; its name matches `test_phase*_probe.py`; it directly imports an older `probes.probe_phase*` module; no other parseable test imports its test module; and every root test module can be parsed. Any uncertainty retains the file.

Every eligible test is backed up and SHA-256 verified before removal. The run creates a timestamped report under `phase165_r6_audit_results/probe_cleanup`. To restore a run, execute `rollback.ps1 -SessionDirectory "<full path printed by the runner, omitting /backup>"`.

The audit is deliberately conservative. Remaining errors require separate contract-based evaluation. Phase 165 is not closed by this operation.
