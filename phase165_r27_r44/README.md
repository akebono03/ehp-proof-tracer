# Phase 165 R27-R44

Connect Web Generator Applicability and CLI `explore-applicable` to the shared typed applicability matcher introduced in R27-R43. Only verified `ProofStep` evidence is used. Matches are not executed or certified conclusions. The old catalog and group calculation are unchanged.

Unzip into the project root and run `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r44\run.ps1`.

The installer stages both replacements, makes backups, and runs only its targeted tests. Full pytest remains deferred until the end of Phase 165.
