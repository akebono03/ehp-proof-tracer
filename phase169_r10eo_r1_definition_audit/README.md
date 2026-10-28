# Phase 169 R10EO-R1: Definition Generalization Design Audit

This package performs a **read-only design audit** of `HyoujiGen.csv`, the adopted Toda Chapter V/VI transcriptions, the existing cited-definition registry, and the unresolved `pi_41^30` typed search. It does not patch production modules, existing tests, proof trees, or references.

The audit distinguishes typed generator metadata, literal candidates in source text, approved source-backed definitions, and inferred suspension images. A literal match **never** creates a `GIVEN` proof step.

## Run on Windows

Extract the ZIP into the root of your `ehp_proof` checkout. From that root, run:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10eo_r1_definition_audit.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10eo_r1_definition_audit\run.ps1"
```

The launcher requires branch `develop` at reviewed HEAD `57f807901f87c8d66acf4ee4db16ce05b00dccd4` and refuses mismatches. It runs focused pytest only, searches `pi_41^30` with the existing engine, checks its trust boundary if complete, and writes `audit.json` and `audit.md` under a timestamped `output` directory. No full suite is run.

For metadata-only inspection without the proof search:

```powershell
python -m phase169_r10eo_r1_definition_audit.audit --output phase169_r10eo_r1_definition_audit/output/manual
```

If the upstream HEAD has changed, review the new files and regenerate a guarded package before running. Do not bypass the guard.
