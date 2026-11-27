# Phase 178 R18 — n=6 Source-first Audit

Read-only audit of the public proof query for $\pi_{12}^{6}=\mathbb{Z}/2\{\nu_6^2\}$. Requires the reviewed develop HEAD `de51c804796aadb88a4228e1863b329e2031ebce`, synchronized with `origin/develop`, and a clean tracked worktree.

## Scope

- Verify the adopted source transcription for (5.12) and (5.13) and the reviewed source/code blobs.
- Reuse the existing Phase 178 R1 public observer for `(n,k)=(6,6)`. Capture the same screened bridge and provider used by that query. Preserve actual public proof status, frontier, search trace and trust-boundary result.
- After the public search returns, inspect candidate availability for the root, cyclic structure, suspension isomorphism, injectivity, surjectivity, Delta zero image, the relevant exactness windows, source claims and generator image. These are diagnostics only, not additional proof searches.
- Query existing prior-DB eligibility and fixed-source linkage independently. Do not register or inject any proof premise.
- Run focused tests only and verify that Git HEAD, tracked diff, index and status are unchanged by the audit.

## Run

From the repository root, run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase178_r18_n6_source_first_audit\run.ps1 -DryRun`, then the same command without `-DryRun`. An optional `-Timeout 300` changes the observation worker timeout (seconds).

Reports are written outside the repository under `%LOCALAPPDATA%\EHPProofTracerAudit\phase178_r18_n6_source_first_audit\attempt_*\`. `report.json` contains the preflight and observation summary; `observation.json` contains detailed candidate probes; `n6_k6.json` contains the original R1 search trace. The console prints source/prior eligibility, actual frontier and diagnostic rule names.

`PASS_R18_N6_SOURCE_FIRST_AUDIT` means the observation and focused tests passed, not necessarily that the group proof is complete. A partial proof is a valid audit finding. An unobserved candidate must never be described as a successful proof. No new mathematical rule, GIVEN, public provider or renderer change is made. No full pytest run.
