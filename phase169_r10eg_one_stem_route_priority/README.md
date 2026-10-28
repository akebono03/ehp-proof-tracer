# Phase 169 R10EG — Canonical One-Stem Route Isolation

R10EF identified two independently verified, non-equivalent derivations for the same eta-family one-stem goals. The shared backward resolver properly refuses to select one arbitrarily. This narrowly scoped patch stops proposing the redundant newer general stable-transport route for the already supported typed eta-family one-stem group goals, leaving the earlier cited eta routes to be independently proved.

Only `phase169_r10e1_general_group_transport/transport.py::expand_prior_general_group_transport` is patched. Mathematical inference rules, the database, cited statements, the proof tree and the public API are untouched. New imports remain local to the modified function.

## Apply and test (Windows PowerShell)

From the repository root, extract this archive into the root and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase169_r10eg_one_stem_route_priority\run.ps1
```

Prerequisites: local `develop` descending from reviewed commit `463880e69a4bf3a51b07654b74f3ac1c29798176`, unchanged target file blob `d60770fff1b6e14791db6b952733f4062a64c8eb`.

The runner preserves unrelated preexisting tracked modifications (including the R10EF status report), runs focused tests and a ten-goal proof verification audit, and restores the exact target bytes on failure. Run artifacts and the complete new function/source go into a fresh timestamped `output/run_*` directory; they never overwrite previously committed audit outputs.

A successful focused run does not imply complete Phase 169 certification or full-suite pytest success. See `DESIGN_JA.md` for the precise proof boundary.
