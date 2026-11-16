# EHP Proof Tracer — Phase 175 R3R8 Public Connection

This package connects the **six genuinely inferred R3R7 proof obligations** to the ordinary Group query. The earlier isolated audit was successful but did not change the shared search provider, so the normal Web view remained `generic-partial-proof`.

## Scope

Only `phase165_r52_r9_shared_math.py::search_shared_group_goal()` is modified, with a small conditional connection for the existing `(n,k)=(3,4)` registered group goal. Its public API, top-level imports and every other function remain unchanged. All existing mathematical inference rules are reused without modification:

- The verified double-suspension relation from Toda Lemma 5.4.
- The generic even-factor membership inference from R3R7.
- The universal cited Lemma 5.7 criterion from R3R6.
- The independently proved zero-image, EHP exactness, Hopf injectivity and cyclic-lift rules.

`route.py` builds a source-screened expansion provider; it does **not** add a target-group GIVEN, a special proof result, a saved `ProofStep`, an alternative renderer or a new mathematical rule. Other `(n,k)` routes are unchanged. The package keeps the original First Successful Proof Search semantics.

## Verified source boundaries

The source registrar checks the adopted Chapter V transcription, the reviewed hashes and publication positions: Lemma 5.4 at 8300, Lemma 5.7 at 9100, Proposition 5.8 at 9200. The original printed edition has not been independently verified. A real normal R3R7 audit with **all six** obligations `INFERRED` and an unchanged tracked worktree is required.

## Running on Windows

Extract `R3R8.zip` in the root of the current `develop` checkout after running R3R7. Then run:

```powershell
$ErrorActionPreference = 'Stop'
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase175_r3r8_pi73_public_connection\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R3R8 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase175_r3r8_pi73_public_connection\run.ps1"
if ($LASTEXITCODE -ne 0) { throw 'R3R8 integration failed' }
git status -sb
```

DryRun checks reviewed Git state, exact source pins, the complete-function replacement contract, and R3R7 evidence without changing tracked files. The normal run installs the single-function insertion, executes **only focused pytest**, then starts an isolated real Group query worker. It verifies the ordinary search result, trusted proof tree, shared narrative model, and Web `generic-complete-proof` response. If any test or verification fails, the installer restores the precise original production file bytes from its external audit backup and reports failure.

Reports, backups and logs are saved outside the repository at `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r3r8_pi73_public_connection\<UTC>\`. No Git staging, commit, checkout, reset or fetch is performed.

## Completion boundary

R3R8 succeeds only when `(n,k)=(3,4)` is `complete`, the conclusion matches the registered group, the actual proof tree passes the trust boundary, there are no open goals, and the common Web renderer returns `generic-complete-proof` with references. This phase does not attempt the remaining `(n,k)=(5,4)` or `(6,4)` queries. The full pytest suite is reserved for Phase 175 closeout.
