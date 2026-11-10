# Phase 174 R56 — Reusable Cyclic Generator and Delta Surjectivity

This package connects two mathematical inference rules to the existing shared,
source-first backward proof search. It does not add source facts, direct group
GIVEN assertions, special-case prose, saved completed proofs, or a second search
engine. The previously certified R37 four-premise rule remains available as a
backward-compatible fallback.

The first new rule derives a free cyclic group generator from the established
four typed Hopf/EHP premises. The second derives Delta surjectivity from the
independently established cyclic presentation and the independently derived
Proposition 2.7 typed Delta application. Both rules apply uniformly at eligible
even EHP indices, not just one named homotopy group.

Extract the ZIP directly in the `ehp_proof` repository root on the `develop`
branch. Run the following commands from PowerShell:

```powershell
$ErrorActionPreference = 'Stop'
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r56_cyclic_generator_bridge\run.ps1' -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R56 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r56_cyclic_generator_bridge\run.ps1'
if ($LASTEXITCODE -ne 0) { throw 'R56 failed' }
```

A source guard pins the committed shared provider's Git object and refuses
unreviewed local changes. No destructive Git commands are used. The install
writes full replacement code and complete modified functions into `output/`.

## Scope

- Modified existing production module: `phase165_r52_r9_shared_math.py`
- New inference module: `phase174_r3_r7_r56_cyclic_generator_bridge/rule.py`
- New focused tests, installer and public audit in this package
- No changes to global project documents or math-source registries

The production audit independently searches `pi_11^6` and `pi_12^7`. A completed
`pi_12^7` proof must reuse its earlier admitted `pi_11^6` database result
without recomputing that group proof. These are runtime assertions, not
claims about an unexecuted checkout. Full pytest is deferred to Phase closeout.
