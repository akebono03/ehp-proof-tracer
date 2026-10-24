Phase 168 R3-41I — pytest import collection repair (2026-10-24)

Purpose
-------
Fix only the pytest module-name conflict caused by two test_audit.py files.
Confirmed against GitHub develop:
- phase168_r3_41i_renderer_closure_audit/run.ps1
- phase168_r3_41i_renderer_closure_audit/tests/test_audit.py
- phase168_r3_39f_frozen_comparison/tests/test_audit.py
- phase168_r3_19_web_model_default/tests/test_phase168_r3_19_web_model_default.py
- phase168_r3_41i_renderer_closure_audit/audit.py

Modified repository file
------------------------
phase168_r3_41i_renderer_closure_audit/run.ps1

Old command: python -m pytest -q `
New command: python -m pytest -q --import-mode=importlib `

Nothing else in the runner changes. No production, baseline, or test file
modifications are intended. full_files/ contains the complete post-fix runner.

Run (Windows PowerShell, from repository root)
------------------------------------------------
Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41i_collection_fix.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41i_collection_fix\run.ps1"

Execution
---------
1. Check hashes for six implementation files and three frozen baseline texts.
2. Run the three focused package tests, with importlib import mode.
3. Back up original R3-41I run.ps1 and insert only the importlib flag.
4. Run exactly the three existing R3-41I limited-test modules.
5. Run the existing read-only R3-41I audit, creating review_bundle.zip.
6. Verify the source and frozen baseline hashes did not change.
7. On any failure after the patch, restore run.ps1 byte-for-byte.
8. Write phase168_r3_41i_collection_fix/output/collection_fix_report.txt.

Outputs
-------
phase168_r3_41i_renderer_closure_audit/output/review_bundle.zip
phase168_r3_41i_collection_fix/output/collection_fix_report.txt
phase168_r3_41i_collection_fix/output/run.ps1.before (backup, if changed)

Interpretation
--------------
The audit may report baseline review gaps even when execution succeeds.
Successful execution DOES NOT mean fixed-baseline Narrative equivalence.
Repository-wide pytest is deliberately not run.
