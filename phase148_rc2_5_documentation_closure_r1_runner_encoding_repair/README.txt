Phase 148 RC2-5 Documentation Closure R1

Runner-only encoding repair.

Cause:
The previous PowerShell runner contained Japanese literals in Select-String
patterns. Windows PowerShell decoded the UTF-8 script incorrectly and failed
during parsing before the Python documentation updater could run.

Changes:
- PowerShell runner only.
- Japanese Select-String literals removed.
- Closure verification is performed by Python reading the files as UTF-8.
- The .ps1 file is written as UTF-8 with BOM for Windows PowerShell 5.1.

Unchanged:
- documentation content
- documentation Python updater
- production code
- tests

Repository-wide pytest is NOT rerun.
