# Phase 175 R4R11 — Signed Delta image normalization via proved eta two-torsion

This package connects one reusable, strictly conditional inference rule to the common backward proof search. It does not change or rederive Toda (5.8) or Proposition 2.5; those source-level prerequisites were registered in Phase 175 R4R10.

The rule turns a proved signed image `Delta(gamma) = +/-( (2k*a-b) composed with eta_n )` into the exact image `Delta(gamma) = b composed with eta_n`, **only** after obtaining a separate proved `2 eta_n = 0` relation and the cited universal eta-family definition (`n >= 3`, ensuring the right factor is a suspension). No group structure, new literature statement, or direct root result is registered.

## Files

- `rule.py`: source-neutral, typed mathematical inference.
- `provider.py`: backwards candidates screened by the already registered Toda (5.8) citation.
- `installer.py`: Git-pinned, whole-function replacement of `shared_expansion_provider` only.
- `audit.py`: reviewed HEAD, prior report, source hashes, and public provider verification.
- `tests/`: focused tests for inference, provenance, history, and installation.
- `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `TEST_RESULTS_JA.md`: Japanese audit documentation and complete new code.

## R4R11R1 test-fixture correction

The earlier package had a test-only argument binding error: its `cited_bridge()` fixture passed a `ProofStep` as the second positional argument of `ProofStepLink`, which is `repository_key`. The corrected test fixture passes the proof step explicitly as `step=...`. No production module, mathematical rule, source statement, or PowerShell runner is modified by this correction. The original user run stopped at focused pytest (4 failures and 124 passes), before the audit.

The corrected fixture and existing R4R11/R4R10 focused tests pass in the authoring compatibility environment (94 passed). Real-repository validation remains required.

## Running on the repository

Unzip at the project root, then run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r11_signed_eta_torsion_public\run.ps1 -DryRun -R4R10Report <path>` and then the same command without `-DryRun`. Full replacement source files are exported to the audit output directory for independent inspection. No full test suite is run.

The expected final gate is `PASS_R4R11_SIGNED_ETA_TORSION_SHARED_CONNECTED_PI95_PENDING`. This gate does **not** claim a complete proof of `pi_9^5`.


## R4R11R2 source-guard line-ending correction

The R4R11R1 package passed 128 focused tests in the user's repository but DryRun failed with `R4R11_SOURCE_DRIFT: expression.py`. GitHub stores `expression.py` and the two pinned Toda TeX sources with CRLF newlines. The old audit incorrectly compared only a normalized LF-byte Git blob with the committed, CRLF-byte Git blob SHA. The corrected audit checks the exact pinned Git blob against three equivalent whole-file representations: original bytes, LF-normalized bytes, and CRLF-normalized bytes. Content changes still fail closed.

Only `audit.py` and the associated `tests/test_audit.py` change. The existing R4R11R1 fixture repair remains. No production changes are made to mathematical rules, registry sources, or the runner by this correction. The new regression test checks both line-ending directions and rejects altered contents. Real-repository DryRun and real execution are not yet confirmed for R4R11R2.
