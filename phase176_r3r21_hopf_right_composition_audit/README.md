# Phase 176 R3R21 — Hopf right-composition source frontier audit

This read-only audit verifies the presence of the existing Toda Proposition 2.2 right-composition implementation and two directly relevant tests. It does not establish a new group structure, introduce a GIVEN, register a rule, or modify production code. The audit reports outstanding proof obligations rather than asserting completion.

From the repository root, run `phase176_r3r21_hopf_right_composition_audit/run.ps1` with `-DryRun` first, then without it. The latter also runs the existing focused `tests/test_hopf_rules.py` module. No full test suite is run. The report is placed in `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r21_hopf_right_composition_audit\report.json`.
