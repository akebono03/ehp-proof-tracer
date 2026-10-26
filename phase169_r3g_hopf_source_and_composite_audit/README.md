# Phase 169 R3G — Hopf relation and composite provenance audit

This is **AUDIT_ONLY**. It requires the R3F3 terminal provider installed in the
repository, but does not patch production sources, tests, or project documents.

From the PowerShell repository root, extract the package and run its `run.ps1`.
The script performs preflight validation, focused pytest, and an on-demand
citation-screened search for `pi_4^2` and `pi_5^3`. Its report is written to
`output/source_and_composite.json` inside the extracted package.

The audit distinguishes literal text in Toda equation (5.3), registry metadata,
exact typed assertions, screened GIVEN steps, backward expansions, and
verified INFERENCE steps. It does not manufacture a Hopf relation proof or
promote a GIVEN composite into an inferred composite to bypass old rules.

The repository-wide suite is intentionally not run.
