# Phase 178 R12 — typed display audit

Read-only audit at reviewed develop HEAD `4235e902a0a6eea227ab9ec8ab8ebe4529b9aae4`.

This package does not install or alter any production renderer, proof rule,
provider, source, or tracked file. It reuses the R11 actual-proof inspection to
check the complete 20-step proof and prior R10/R11 rendering invariants. It
records each model step, real premise and consumer indices, source citations,
typed generator factors, and actual rendered line when uniquely identifiable.
It previews notation-only edits in a separate Markdown file using the existing
public group-generator renderer. Duplicate typed ancestors are reported for
review, not suppressed. A passing audit is not completion of R12 display work.

Run from the repository root using `run.ps1 -DryRun` then `run.ps1`. The exact
reviewed develop HEAD and clean tracked working tree are required. Reports are
written beneath `%LOCALAPPDATA%/EHPProofTracerAudit/phase178_r12_suspension_composition_audit/`.
The audit runs only the listed focused tests, never the full suite.
