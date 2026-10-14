# Phase 165 R27-R31

Batch-remove only repository_* Python modules that cannot be reached through static imports from any non-repository top-level production module. Preserve all typed search, registry, proof and rules code. The audit JSON records retained files and their entrypoint import dependencies. Root-level tests and historical archival scripts are deliberately not used as production roots; old tests may need subsequent migration. Backups are preserved before deletion. No full pytest is run.

Extract this folder into the project root and execute run.ps1 from PowerShell.
