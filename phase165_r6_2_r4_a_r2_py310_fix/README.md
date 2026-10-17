# Phase 165 R6-2 R4-A-R2: Runtime Rule Capability Audit

Run `run.ps1` from the repository root after extracting the ZIP there. It runs five targeted tests, then probes the existing R8 rule discovery in a separate Python process. Results are written to `reports/runtime_capability.json` and `reports/runtime_capability.md` inside the extracted package.

The package does not modify any production source or test files. Python is invoked with `-B` and `PYTHONDONTWRITEBYTECODE=1`. Imports may nevertheless have project-defined side effects; this is an inspection of the existing code, not a sandbox guarantee.

An instantiated rule is not a certified backward-applicable rule. A conclusion pattern and premise patterns are only structural prerequisites. This phase does not run canonical proof search, certify any goal, or run the full test suite. R4-A AST-eligible functions and runtime results are compared by module; the R8 API does not expose a reliable factory identity for every emitted rule.

## Python 3.10 compatibility fix

The Markdown row renderer no longer uses backslashes in f-string expressions. Run `run.ps1` from the repository root. This is a targeted corrective patch only.
