# R10ET-R6B — pi10_8 audit diagnosis

This is a read-only diagnostics bundle for a previously generated R10ET-R6 report. Run `run.ps1` after extracting at the EHP Proof Tracer repository root. The script finds the latest `audit.json`, reads the pi10_8 proof trace, and prints the actual R6 reason for REVIEW_REQUIRED. It does not rerun proof search, patch the provider, change the Git staging area, write an output report, or run the full pytest suite.

Review criteria are unchanged. A successful diagnostic exit is not R6 mathematical acceptance. The R6B script must be used only against an existing R6 report; it fails if the report is absent or not from R10ET-R6.

Tests: `python -m pytest -q phase169_r10et_r6b_pi10_review_diagnostics/tests/test_r6b_diagnose.py`.
