# Phase 167 R1 Read-only Audit

Run `run.ps1` from the root of the EHP Proof Tracer repository after extracting this ZIP into that directory. It reads source code and earlier audit artifacts, writes `r1_report.json` inside the extracted audit directory, and does not modify production code, tests, or repository documents. It does not run pytest or prove live Web rendering behavior.
