# Phase 174 R3-R7-R1 — Zero-root source-first diagnostic

This package audits, but does not implement, the unresolved zero-group target
`pi_12^7 = 0` discovered in the completed Phase 174 R3-R7 report.

The old report did **not** measure any backward candidates at the zero root;
its `source_screened_frontier` explicitly skipped targets with no registered
`Relation` root. This package fixes the diagnostic gap by probing the actual
typed `TodaPrimaryGroupZeroStatement` through the production source-screened
expansion provider. It also inspects the precursor `pi_11^6` and checks the
printed Proposition 5.9 exact-sequence route without treating the text as a
direct target GIVEN.

The audit does not register a new theorem, change production source code,
replay archived proofs, or produce any verified proof step. It makes no claim
that a source-screened inference candidate is already a proof.

## Run

From the repository root, extract the ZIP, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r1_zero_root_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r1_zero_root_audit\run.ps1"
```

The GitHub `develop` remote must match the reviewed commit. The local
`develop` branch may be at either the old Phase 174 R3-R7 commit or the newly
reviewed commit; the package will never automatically checkout, fetch, clean,
or commit changes.

The JSON result is written outside the Git repository:
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r1\zero_root_audit.json`.

Only five related focused pytest modules are run; **the full suite is not run**.

## Source limits

The source check uses the repository's Toda Japanese TeX transcription, not an
independently verified printed edition. The proof sketch requires certified
EHP exactness, the dimension-correct Delta isomorphism, and below-diagonal
vanishing before a zero-group inference can be implemented.
