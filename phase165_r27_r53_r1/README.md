# Phase 165 R27-R53-R1 installer repair

This package fixes the overly strict installation guard in R27-R53. It preserves the complete bodies of the pre-existing legacy report functions and moves runtime legacy imports into the appropriate functions. It postpones type annotation evaluation for repository-only annotation classes. It retains the R50/R52 typed interfaces.

Run `run.ps1` from the repository after extracting the archive at repository root. Only the package's focused pytest tests are run. No full pytest runs here.

Before modification, the installer creates `phase165_r27_r53_r1_backup/toda_calculation_facade.py`; the audit report is `phase165_r27_r53_r1_audit.json`. No repository modules are deleted. Legacy report APIs remain legacy and must eventually be retired separately.
