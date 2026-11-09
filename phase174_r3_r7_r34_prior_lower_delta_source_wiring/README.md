# EHP Proof Tracer — Phase 174 R3-R7-R34

## Scope

Register only two independently printed, earlier Toda premises into the shared
source-first proof registry:

- Proposition 5.8: `pi_9^5 = Z/2{nu_5 o eta_8}`.
- Equation (5.10): `Delta(iota_11) = nu_5 o eta_8`, recorded conservatively with
  the existing signed-image statement type.

Both source clauses are verified against the exact adopted Toda TeX Git blob,
the publication-order manifest, and the existing structured generator. A
`Composition` is preserved; no fabricated `HomotopyElement` replaces it. The
DB is a transcription cross-check, not an independent citation.

The existing universal diagonal group rule is unchanged. This package does
**not** derive its concrete specialization, compute a kernel, prove Delta
surjectivity, or complete `pi_12^7=0`. No goal-specific proof, direct kernel
GIVEN, narrative, or renderer modifications are made.

## Changed production target

`phase165_r52_r9_shared_math.py`: add one source-builder import and source-tuple append (in a short
import and tuple append block) inside `build_shared_typed_bridge`. The full
original function is not manually reproduced here; the installer applies a
byte-guarded, exact-anchor patch and `CODE_FULL_JA.md` includes the entire
installer, its import section, and all new functions/tests. No other tracked
file is edited.

## Run

Extract this ZIP into the repository root. From PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r34_prior_lower_delta_source_wiring\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R34 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r34_prior_lower_delta_source_wiring\run.ps1"
if ($LASTEXITCODE -ne 0) { throw 'R34 audit failed' }
```

The installer is idempotent and preserves existing files, staging, commits,
and earlier-phase directories. It refuses unexpected tracked changes and
unreviewed GitHub history. Only focused pytest groups run; the full suite
remains reserved for Phase closeout. Audit reports are written under the
user's local application-data folder.
