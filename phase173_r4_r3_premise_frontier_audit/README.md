# Phase 173 R4-R3 — Read-only Prerequisite Frontier Audit

This package inspects Toda (5.2) and Toda (5.6) **without adding proof rules or modifying production code**. It preserves the completed public proof for `pi_7^4`.

## Purpose

- Check the typed database presentations of `pi_i^3`, `pi_i^2`, `pi_{i-1}^3`, `pi_i^7`, and `pi_i^4` for `i=7,8,9,10`.
- Report abstract direct-sum compatibility, **not** mathematical derivation or generator images.
- Distinguish existing Toda (5.2) direction from a hypothetical reverse direction, including the strict DB prior order.
- Inspect live public search outcomes for the four supporting groups `pi_7^7`, `pi_8^7`, `pi_9^7`, and `pi_10^7`.
- Produce JSON and Markdown reports outside the repository, without running the full pytest suite.

## Safety

The package requires the reviewed `develop` HEAD `8be7b92a12bb3a58119d13491db5dbcffd71eb91`, clean tracked files, and exact source Git blob identities. A head mismatch is a deliberate refusal, not a request to reset or force-update Git. The existing R4-R2 folder may remain untracked.

## Usage

From the repository root in Windows PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r3_premise_frontier_audit\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r3_premise_frontier_audit\run.ps1'
```

The report is written to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r4_r3_<timestamp>\audit.json`. The source worker logs are written alongside it. If any preflight or worker fails, the command exits nonzero and preserves its report.

## Interpretation

`abstract_structure_compatible=true` is only a necessary compatibility observation. It cannot establish the generator transport, Hopf invariant, proof of zero groups, or a valid source citation. `admitted_db_step` designates an adopted database **hypothesis**, not an independently derived theorem. The original `pi_7^4` source-bound rule is not generalized by this package.
