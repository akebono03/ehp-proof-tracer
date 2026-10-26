# Phase 169 R3E1 — Audit module import fix

This package reruns the original Phase 169 R3E production patch and focused checks without changing the mathematical implementation. The earlier R3E run passed 22 focused pytest cases but then stopped before the live audit with `ModuleNotFoundError: No module named 'homotopy_groups'`; the guarded installer restored the original production file.

## Scope

The **only correction** relative to R3E is in the PowerShell audit launcher. Instead of running the audit file directly as `python -B "$package\audit.py"`, it runs `python -B -m phase169_r3e1_ehp_audit_module_fix.audit` from the repository root, where the project modules are importable. The original `apply.py`, complete replacement `shared_expansion_provider()` function, `audit.py`, and all six new focused tests are retained without modification.

The installer changes one production function in `phase165_r52_r9_shared_math.py`, under the same Git blob guard as R3E. It saves the complete pre-change production file and the complete post-change production file under the `output/` directory. The patch does not create GIVEN facts, literary claims, or completed proof roots.

## Run on Windows PowerShell

Extract the ZIP into the repository root. Run:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
powershell -ExecutionPolicy Bypass -File ".\phase169_r3e1_ehp_audit_module_fix\run.ps1"
```

The script applies the guarded patch, runs the same focused pytest modules, and then runs the live audit as a Python module. On any test/audit failure it attempts a byte-guarded restore and reports the failure. It **does not** run the full pytest suite. To restore explicitly after a successful run, execute `python -B .\phase169_r3e1_ehp_audit_module_fix\apply.py restore` while the patched file is unchanged.

## Completion criteria

Check `R3E1_AUDIT_EXIT_CODE=0`, `CONNECTED_ISO_PROPOSALS=1`, four exactness proposals and two unresolved terminal goals in `output/ehp_provider_connection.json`. The result for pi5^3 must remain incomplete; this Phase does not certify a suspension isomorphism. If a different error occurs, report its full stdout without marking completion.
