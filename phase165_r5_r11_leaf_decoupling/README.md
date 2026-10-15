# Phase 165 R5-R11 — Decouple historical EHP leaves

This guarded patch extracts the unmodified `_phase162_ehp_leaves()` function from the historical Phase 162 Web Narrative module into `phase162_ehp_leaf_inputs.py`. The Web replay imports it directly, while the historical module re-exports it to preserve compatibility.

Only the leaf dependency is migrated. Historical Narrative, Proof Chain, Concrete Transport, and existing APIs are preserved. No proof status is promoted; the historical Phase 59 fixture issue remains unresolved.

## Install and test

Extract `phase165_r5_r11_leaf_decoupling.zip` into the project root; then run:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
powershell -ExecutionPolicy Bypass -File ".\phase165_r5_r11_leaf_decoupling\run.ps1"
```

The installer refuses unrecognized local source and existing backups. It copies both modified sources into `.phase165_r5_r11_backup`, installs the new module, then runs scoped pytest. If tests fail, the runner restores both original files and removes the new module. The full suite is not run.

## Manual restore

```powershell
python ".\phase165_r5_r11_leaf_decoupling\restore.py"
```

The restore script uses the backup created by this phase. Do not run it if no backup exists.
