# Phase 166 R3 — Internal Proof Reuse Audit

This package checks existing internal proof reuse and proof-use ordering controls. It makes no production changes and grants no proof permissions.

## Run

Extract this directory in the EHP Proof Tracer repository root and run `phase166_r3_internal_reuse_audit/run.ps1` in PowerShell. The command runs a read-only audit and five targeted pytest checks. It does not run the full suite.

The output is `phase166_r3_internal_reuse_audit/results/summary.json`. A reported missing direct search order gate is an audit finding, not an automatically authorized code change.
