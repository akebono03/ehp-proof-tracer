# Phase 168 R2-4 — Dimension-based citation source resolution

This patch updates only the existing citation-identifier resolver, without introducing a separate database citation policy. It selects a positioned, typed source group statement with the requested dimensions and verified group presentation, preserving the existing generic-eta specialization. Missing or ambiguous sources are not fabricated.

Run `run.ps1` from PowerShell after extracting this archive at the repository root. The installer backs up the original resolver module. The runner executes focused tests and a source-binding audit only. It does not run the full suite or claim the group proof is complete.

The source registry currently may lack an eligible typed Proposition 5.3 statement, in which case binding correctly stays `None`; source verification and registration are separate work.
