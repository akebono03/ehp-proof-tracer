# Phase 173 R4-R1 — Root Match Probe

This package is an isolated, read-only diagnostic for the source-bound Toda (5.6) proof of the group $\pi_7^4$. It inspects only the actual `ProofStep` objects accepted by the canonical typed backward search, and checks their exact compatibility with the existing four-premise inference rule.

**No production changes.** No database goal is promoted into a proof leaf, and no Toda Lemma 5.4 archive row is promoted by this package. The probe reuses the previously reviewed, source-hash-verified and publication-screened Lemma 5.4 typed source from `phase173_r4_r1_lemma54_source_bridge` and the existing Toda (5.6) root provider from `phase173_r4_r1_source_bound_56`.

## Run

1. Extract the ZIP in the EHP Proof Tracer repository root on the `develop` branch.
2. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_r4_r1_root_match_probe\run.ps1 -DryRun`.
3. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_r4_r1_root_match_probe\run.ps1`.

The script executes focused pytest with the cache plugin disabled. It never runs the full suite. The report is written to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r4_r1_root_match_probe\audit.json`.

Review `PREMISE_1_STATE` to `PREMISE_4_STATE`, `PREMISE_N_MATCH`, `LEMMA54_HOPF_PROVED`, `ROOT_GUARD_ACCEPTS`, `ROOT_MATCH_COUNT`, and `ROOT_DIAGNOSIS`. `MATCHED_PROOF_NOT_COMPLETED` is **not** a completed-proof certificate.

## Source guard

The guard checks the reviewed Git ancestor, `develop` and `origin/develop`, pinned production Git blob identities, clean production source paths, and SHA-256 of the two pre-existing, untracked Lemma 5.4 package source files. Committed changes after the reviewed ancestor must consist only of added `phase173_` audit files. The guard never modifies Git state.
