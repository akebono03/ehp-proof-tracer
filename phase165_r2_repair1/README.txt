Phase 165 R2 repair1

The failure arose because the positive test fixture did not set LiteratureEntry.source_id.
The Phase 163 assess_citation policy requires both source and target references
in the same known source document for publication-order eligibility.

Changed: tests/test_phase165_r2_registry_lookup.py (complete replacement).
Added: a negative test for missing/mismatched source document identifiers.
Unchanged: phase165_r2_registry_lookup.py and all production modules.

PowerShell from repository root:
Expand-Archive -Path "$HOME\Downloads\phase165_r2_repair1.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r2_repair1\run.ps1"

Expected targeted tests: 5 passed.
This is a test fixture repair, NOT completion of Goal-only proof construction.
Full suite should be run only at the end of Phase 165.
