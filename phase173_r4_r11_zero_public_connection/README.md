# EHP Proof Tracer — Phase 173 R4-R11 Zero-Group Public Connection

This package connects the previously reviewed, general Toda Proposition 4.4 typed inference core to the standard **zero-group** query path. It is deliberately limited to zero-group goals with two independently admissible earlier zero-group database priors. The eligibility test contains **no list of target dimensions**. Other unsupported generator-image families continue to fail closed.

## Reviewed baseline and scope

The reviewed upstream `develop` baseline is commit `924888b257f9fed1e2d34790127b4ff108a7badb` (R4-R9 audit files only relative to the prior baseline). A later commit may be accepted only when it descends from the baseline and all production file blobs remain exactly reviewed. The local and GitHub branch heads must be equal, and unreviewed tracked edits are rejected.

The local R4-R10 `core.py` must match the original reviewed package. This package does not alter that core, the R4-R7 bounded rule, the R4-R8 public connector, or any narrative projector.

## Changed files, classes and functions

One existing production function is replaced as a complete function:

- `phase165_r55_nk_only_goal.py`: `search_group_from_registered_goal()` — only its zero-group branch changes to try the screened general Toda (5.6) connector; existing fallback behavior is retained. See `search_group_from_registered_goal_FULL.py.txt` for the complete replacement function. The module's import block is **unchanged**, as the new connector is imported locally inside that function.

All other files are newly created under `phase173_r4_r11_zero_public_connection/`:

- `source.py`: `screened_zero_toda56_context()` — source archive validation, authentic fixed-source screening and prior-link exclusion with ambiguity checks.
- `route.py`: `prepare_zero_toda56_public_connection()` — the isolated source screen and existing general root/Hopf providers.
- `install.py`: `git`, `_full_function`, `patched_source`, `preflight`, `install`, `main` — full-function installer and exact-source guards.
- `verify.py`: `inspect_public_zero`, `main` — standard public Group query, root provenance, DB prior guards and Web trust gate.
- `tests/test_route.py`, `tests/test_install.py`: full focused tests, including isolated source verification and Web trust boundary **before** any tracked production code is modified.
- `run.ps1`, `README.md`, `監査計画.md` and the package initializer.

The normal run first executes isolated proof and Web trust-gate tests. **Only after those succeed** may the guarded installer replace the one production function. It then verifies the ordinary Group query and canonical Web model, followed by focused regression tests for the existing four completed public groups.

No Git commit, pull, reset, push or automatic cleanup is performed. Other untracked packages are preserved. The installer preserves CRLF/LF source line endings.

## PowerShell

From the repository root, extract `EHP_Phase173_R4_R11_ZERO_PUBLIC_CONNECTION.zip` and execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r11_zero_public_connection\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r11_zero_public_connection\run.ps1'
```

A successful result requires `PHASE173_R4_R11_PUBLIC_STATUS=complete`, `PHASE173_R4_R11_ROOT_CERTIFIED=True`, `PHASE173_R4_R11_OPEN=0`, `PHASE173_R4_R11_WEB_COMPLETE=True`, `PHASE173_R4_R11_WEB_KEY=generic-complete-proof`, and both focused pytest stages passing. A DryRun success alone is not proof of public completion.

## Next phase boundary

This phase does not assert `E epsilon_3 = epsilon_4`, authorize `pi_12^4`, or generalize the narrative projector. Next, the completed n=4 proof trees can be rendered with a unified, source-backed explanation of the general isomorphism, specialization, generator images and references. Run the whole pytest suite only when Phase 173 closes.
