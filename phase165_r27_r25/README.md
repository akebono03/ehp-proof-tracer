# Phase 165 R27-R25

This installer retires the two remaining legacy standard generator proof-scope and known-group-identity bootstrap entrypoints without changing functions that accept explicitly provided repositories. Both retired entrypoints fail closed; they do not imply the queried mathematics is false or absent.

Run from the repository root after extracting this directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase165_r27_r25\run.ps1
```

The installer backs up original production files in `backups/` and runs only targeted pytest. Legacy proof infrastructure remains on disk until dependent callers are safely migrated. It must not be interpreted as overall Phase 165 completion.
