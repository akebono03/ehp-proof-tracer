# Phase 173 R4-R5 — Blocker Diagnostic

This package is read-only and does not alter mathematical rules, literature claims, the registered database, the Web renderer, or existing tests.

## Reviewed baseline

- Branch: `develop`
- HEAD: `db2a4eda2176cc1295d968079a89a2e08bd65b97`
- Prerequisite: the committed `phase173_r4_r4_typed_generator_audit` package.

## Objective

Inspect the structural difference between the image of the typed generators under the *proposed* Toda Proposition 4.4 map and the registered presentations for $\pi_8^4$, $\pi_9^4$, and $\pi_{10}^4$. Also report the exact citation-position or source-validation reason that prevents reuse of Lemma 5.4.

It does **not** prove the proposed generator identities. Typed shape equality is insufficient to certify a ProofStep.

## Run

From the repository root after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r5_blocker_diagnostic\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r5_blocker_diagnostic\run.ps1'
```

Read the `audit.json` file at the printed `PHASE173_R4_R5_REPORT` path and share the output. The script also verifies the protected $\pi_7^4$ public proof and runs focused pytest only. It refuses unreviewed branch/commit, modified tracked files, altered source blobs, and unexpected remote HEAD.

## Completion boundary

The output identifies the next *proof obligations*. The Phase 173 R4-R5 diagnostic is not a public proof connection and does not declare any new group complete.
