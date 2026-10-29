# Phase 171 R2C: pi_6^3 source-frontier audit

This read-only package inspects current, typed literature assertions relevant to the unresolved 3-stem goal pi_6^3. It starts from the completed R2B report, examines the actual shared statement registry and source-linked `GIVEN` steps, and **does not create proofs, alter application code, equate generator aliases, or certify Toda Proposition 5.6**.

Run from the repository root with Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2C.zip" -DestinationPath "." -Force
$Report = Join-Path $env:LOCALAPPDATA "EHPProofTracerRecovery\phase171_r2b_prop56_20261029_073131_311779\dependency.json"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2c_pi63_source_frontier_audit\run.ps1" -ReportPath $Report -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2c_pi63_source_frontier_audit\run.ps1" -ReportPath $Report
git status -sb
```

The dry run checks the R2B report and Git safety boundary. The normal run imports the existing registry through `python -m`, inventories exact literature locators, and reports source assertions and their actual links. Artifacts are saved under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2c_pi63_*` as `frontier.json` and `frontier.md`.

A `matching_given_count` means only that a source-linked `GIVEN` matches its registered assertion. It **does not** establish the target group theorem, the printed source's edition, or correctness of a new inference. The original text's uncertain `(5.6)?` reference remains unverified. Only focused tests run; no entire-suite test is performed.
