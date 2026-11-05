# Phase 174 R3-R1 — First-Two-Hop Proof Frontier Audit

This package performs a read-only investigation of the three verified root
proposals observed during Phase 174 R2 for the public typed goal `pi_8^5`.
It reuses the same source-screened registry and ordinary expansion provider,
and inspects the next layer of subgoals without constructing or accepting any
new proof step. All possible source-bound obligations remain explicitly
marked as such; an exact source match is not treated as an automatic proof.

The audit first checks the saved R2 JSON report at
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r2\audit.json`, including
its original historical HEAD, three root proposals, and 27 screened source
statements. It then reconstructs the three proposals on the current
reviewed source and compares the exact root/child records to the R2 report.
Only the second level of expansions is inspected (up to 24 options per
child displayed); no recursive proof search is executed.

New output: `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r1\audit.json`.

The checked Git commits are `3558d713` and `1c6e6e59`. The later commit
adds only the completed R2 audit package. Source and test blob SHA guards
must pass for both. If either Git branch moves outside this approved pair,
the runner stops without modifying source.

This audit does not modify any production file or existing test and does not
create a named-group proof, register a citation, or alter the Narrative
Renderer. It does not run the full pytest suite.

Execute in Windows PowerShell from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r1_frontier_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r1_frontier_audit\run.ps1"
```
