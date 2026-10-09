# Phase 162 R4-B3 Full-Text Inspection — Repair 1

This patch fixes only the Windows PowerShell launcher. Python is run with the repository root on `PYTHONPATH`, allowing `tests.test_phase143_19_method_evidence` to be imported when the audit script lives in a subdirectory.

Unzip the patch into the EHP Proof Tracer repository root and execute `phase162_r4_b3_full_text_check_repair1/run_phase162_r4_b3_full_text_check_repair1.ps1` from there. The original `phase162_r4_b3_full_text_check/check_phase162_r4_b3_full_text.py` must already be installed.

The launcher preserves the previous `PYTHONPATH` and restores it after completion or failure. It does not modify production code, tests, or the public renderer. The original audit saves both Markdown files and `check.json` in its `audit_output` directory. No full-suite tests are run.
