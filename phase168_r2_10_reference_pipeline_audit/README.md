# Phase 168 R2-10: Reference pipeline architecture audit

This package performs a read-only AST inventory of the common narrative renderer and its reference helpers. It does not patch production code or run the entire test suite. Run it from the repository root.

## Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r2_10_reference_pipeline_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r2_10_reference_pipeline_audit\run.ps1"
```

Outputs: `output/reference_pipeline.json` and `output/reference_pipeline_report.md` inside the extracted package.

The audit enumerates related tests, but does not run them; reference-specific tests should be run only after reviewing the local version and any intended behavior change. The program never edits source files.
