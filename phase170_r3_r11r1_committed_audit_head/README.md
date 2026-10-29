# Phase 170 R3-R11R1 — Committed Audit Head Closeout

This package corrects the Phase 170 active-suite closeout preflight after commit `84db682e179203dcbddc1c2c88bc3ccbb31a830f` (`3-10-1`). It changes no existing repository or mathematical proof code. The end-of-phase active pytest suite is run only after the previously completed 33-stem domain report has been validated.

## Reviewed commit boundary

The full R3-R10 domain report was created at commit `08382968b5359d6c956b48acec333f127014d4c8`. GitHub `develop` subsequently advanced by one commit, adding only files in `phase170_r3_r10_n2_33_fresh_audit/` and `phase170_r3_r10r1_committed_head_audit/`. This closeout accepts that **specific** historical audit report, not an arbitrary older one. It checks the exact present commit, exact historical audit commit, the names/status of every intervening change, fixed Git blobs of proof dependencies, and a clean tracked working tree.

The 33 rows are individually validated for search completeness, no open goals, proof steps, and a complete Trust Boundary–checked Web result. A dry-run or aggregate counts alone cannot satisfy the requirements.

## Windows execution

Extract the ZIP at the repository root, then run:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r11r1_committed_audit_head\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r11r1_committed_audit_head\run.ps1"
git status -sb
```

To explicitly select an earlier R3-R10 audit report, pass `-AuditReport "C:\path\to\audit.json"`. With no explicit path, the closeout searches the Recovery directory for the latest valid report.

Focused closeout contract tests (not the full repository suite):

```powershell
python -B -m pytest -q -p no:cacheprovider .\phase170_r3_r11r1_committed_audit_head\tests\test_contract.py
```

The full active test command, executed only after validation and only in the non-dry run, is:

```powershell
python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests
```

Output is written to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase170_r3_r11_active_closeout_*\closeout.json` and, when invoked, `full_pytest.log`. No checkout/reset/restore or application source edits are performed. If a tracked change is found after testing, closeout marks the run as failed instead of rewriting the user's files.

The whole Phase 170 is **not yet declared closed**: review the actual full-suite result first, then update the five canonical project documents. This package intentionally does not pre-record a full-suite PASS.
