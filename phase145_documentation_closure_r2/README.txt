Phase 145 Documentation Closure R2

This package repairs only the PowerShell runner from the previous package.

Cause:
- Windows PowerShell 5.1 interpreted the UTF-8 no-BOM runner incorrectly.
- Japanese text inside the .ps1 file caused parser errors before the Python updater ran.

R2:
- Uses an ASCII-only PowerShell runner.
- Reuses phase145_documentation_closure/apply_phase145_documentation_closure.py
  from the already extracted previous package.
- Does not change production code or tests.
- Does not rerun the repository-wide pytest suite.
