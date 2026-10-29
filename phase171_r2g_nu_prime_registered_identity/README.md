# Phase 171 R2G — Registered nu-prime generator identity

This package extends the existing `HyoujiGen.csv`-backed presentation identity to recognize an unindexed, decorated `GeneratorSymbol(family="ν", index=None, decoration="′")` at the registered nu-prime ID 3. The database spelling `GeneratorSymbol(family="\\nu'")` and the earlier indexed spelling remain supported.

It modifies only the complete `_factor_identity()` function in `phase168_r2_8_3_generator_identity/identity.py`. The existing imports, API, theorem registry, proof inference rules, database, citation screening and renderer remain untouched. It does not prove a group order, cyclic structure, or a Proposition 5.6 conclusion.

The installation first verifies the `develop` branch, the known committed file blob, the exact reviewed function and the absence of local edits to the target file. It preserves unrelated uncommitted or untracked files. Before applying the patch, it writes an exact backup and metadata under `%LOCALAPPDATA%\EHPProofTracerRecovery` (or the home directory if `LOCALAPPDATA` is unset). Re-execution is safe when the reviewed patch is already present. Conflicting content is rejected rather than overwritten.

## Windows PowerShell

Extract the ZIP into the repository root, keeping all existing R2E/R2F files. Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2g_nu_prime_registered_identity\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2g_nu_prime_registered_identity\run.ps1"
```

The normal run executes only selected existing and new pytest files, then checks the real screened (5.3) source against the database's π₆³ generator ID. A raw dataclass inequality is expected; only registered presentation identity becomes true. Full pytest is deferred to the Phase 171 closeout.
