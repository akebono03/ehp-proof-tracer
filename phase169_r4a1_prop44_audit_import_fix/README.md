# Phase 169 R4A1: Proposition 4.4 / EHP Audit Import Fix

A read-only rerun of the Phase 169 R4A audit. The prior runner invoked `audit.py` as a file, so the repository root was absent from Python's module search path on Windows. This package invokes the **unchanged R4A audit logic** as a Python module from the repository root.

No application, registry, or existing test files are patched. This standalone archive includes the unchanged R4A audit module and its four focused tests, one new launcher regression test, and the launcher itself. Only these five local tests and the seven existing R3O tests run; no full pytest suite is run.

## Windows PowerShell

From the checked-out `develop` repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r4a1_prop44_audit_import_fix.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r4a1_prop44_audit_import_fix\run.ps1"
```

The launcher uses:

```powershell
python -m phase169_r4a1_prop44_audit_import_fix.audit
```

It writes `phase169_r4a1_prop44_audit_import_fix/output/audit.json` and `audit.md` after running the audit. An unsuccessful audit never counts as completion. See `AUDIT_JA.md` for the mathematical scope and `R4A1_CHANGELOG_JA.md` for the runner fix.
