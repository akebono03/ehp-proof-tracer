# Phase 178 R20F1 — Historical Guard Audit

This read-only diagnostic separates the R20 isolated bridge tests from the historical Phase 169 R4C ancestry test. The reviewed develop HEAD is `6db941ca18158da23fab34eed6b259842feb2cd1`. The original R20 package must remain extracted and unchanged.

- Run all six historical R4C tests separately on the unchanged production code. Only the exact reported missing `TodaProp44UniversalStatement` assertion can be classified as an open historical guard; other failures, errors or skips stop the audit.
- Reconstruct the actual historical typed suspension isomorphism in a fresh process without importing R20. Record the inference tree and actual source links, and replay it through the existing trust gateway using the real screened context and citing assertion. This diagnostic replay is not a certificate for a group result.
- Run the 45 active isolated/regression tests and five new report classifier tests. No test is deleted or rewritten. No math rule, GIVEN, provider, or renderer is changed.
- An open-guard PASS is limited to the active isolated scope: the historical test remains failed and the complete suite has not been run. A failed replay, a different historical failure or any active test failure stops the audit. Do not infer when the historical failure first appeared from this baseline alone.

Run `run.ps1 -DryRun`, then `run.ps1` from the repository root. Review `report.json`, `historical_baseline.xml`, `historical_ancestry.json`, and `active_isolated.xml` in the emitted report directory. The audit does not install changes or commit files.
