# Phase 165 R6-2 R4-A-R6

Read-only audit of four existing pi4^3 adapter branches and their underlying inference-rule factories. No changes to production source files. The tool inspects factory definitions, instantiates zero-argument rules when possible, and distinguishes structural suitability from proof of actual generic applicability.

Run `powershell -ExecutionPolicy Bypass -File .\phase165_r6_2_r4_a_r6\run.ps1` from the repository root. Python 3.10 or newer is supported. Results appear in `reports/r6_capability.json` and `reports/r6_capability.md` inside the package directory. Targeted tests only; no full pytest.
