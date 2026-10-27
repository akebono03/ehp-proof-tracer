# Phase 169 R10EH: Stable-range group proof and narrative boundary audit

This package audits four specific stable-range queries without editing the application, theorem registry, database, historical documents, or existing tests.

- `pi_28^22` (`n=22,k=6`) and `pi_32^22` (`n=22,k=10`): confirm searched completeness, replay the proof tree, and measure the visible one-step suspension chain and duplicate equations. Compare applicability of the existing cyclic and direct-sum projection guards.
- `pi_33^22` (`n=22,k=11`) and `pi_36^22` (`n=22,k=14`): preserve partial status, record actual open goals, and distinguish exact HyoujiGen identity metadata from reviewed cited family definitions.

## Run

From the repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10eh_stem6_10_11_14_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10eh_stem6_10_11_14_audit\run.ps1"
```

Requires the Phase 169 R10EG one-stem guard and the reviewed Git commit ancestry. The runner checks Git blob fingerprints but preserves existing uncommitted changes, performs only eight focused policy tests and four runtime searches, and stores reports under a unique `output/run_*` directory to avoid overwriting tracked reports.

A `PARTIAL` result is **never** presented as a proved homotopy group. The audit does not independently authenticate the mathematical truth of the registered Toda references. No repository-wide pytest is run.
