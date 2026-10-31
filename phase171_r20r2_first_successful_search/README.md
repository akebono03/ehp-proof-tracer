# Phase 171 R20R2 — First Successful Proof Search

This package changes the canonical recursive proof engine to accept the first fully checked inference proof rather than requiring a unique derivation route. It does not add statements, trusted leaves, proof rules, database entries, or rendering behavior.

## Preconditions

- Extract the ZIP directly into the EHP Proof Tracer repository root.
- Use the `develop` branch. The installer checks the known source blobs from local commit `9fca3a6e39940215e66dd6ad6a16343118d63339`, which match the inspected GitHub version.
- Preserve any unrelated working-tree changes. The uncommitted R20 edit to `phase165_r52_r9_shared_math.py` is isolated and backed up before restoration. An unrecognized edit causes a safe stop.

## Commands

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R20R2_FIRST_SUCCESSFUL_SEARCH.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r2_first_successful_search\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r2_first_successful_search\run.ps1"
```

By default, the installer restores the exact HEAD version of the shared provider only when it can safely identify the isolated R20 eta-specific diff. It always backs up both source files before writing. If the R20 diff fails its signature check, stop and review the working-tree diff. The explicit `-KeepR20` switch leaves the provider unchanged for a diagnostic-only installation; it is not the recommended final configuration.

Only focused tests run. No full-suite testing, commit, push, or automatic database migration occurs.

The success condition for this package is the recursive search contract, **not** a claim that $\pi_6^3$ is already `complete`. The latter requires subsequent verified group-specific audits.
