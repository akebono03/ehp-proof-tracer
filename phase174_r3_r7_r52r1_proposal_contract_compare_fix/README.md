# Phase 174 R3-R7-R52R1 — Stable Proposal Contract Comparison Fix

This package fixes a false positive in the read-only R52 audit. `InferenceRule` objects contain generated `match_guard` closures, so separate calls to a provider can return semantically equivalent expansion proposals that are not dataclass-equal.

Only the R52 audit and its focused tests are replaced. The R35 mathematical rule, public provider, search engine, source registry, proof verification, and renderer remain unchanged. Every replaced file is SHA-256 pinned and the patch is idempotent. The latest reviewed GitHub `develop` HEAD is `0d0b6b31582ff3e505d14fdde5eaf5e9a0b343d7`.

From the repository root, unpack the ZIP, then run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r52r1_proposal_contract_compare_fix\run.ps1 -DryRun` followed by the same command without `-DryRun`.

This does not assert that the public proof completes. The R52 audit reports the actual result of its ordinary source-first recursive search. Full pytest is not run.
